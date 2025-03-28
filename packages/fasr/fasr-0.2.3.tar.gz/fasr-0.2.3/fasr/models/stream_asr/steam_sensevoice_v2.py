from .base import StreamASRModel
from funasr import AutoModel
from fasr.data import AudioToken, Waveform
import numpy as np
from typing import List
from typing_extensions import Self
from pathlib import Path
from fasr.config import registry


@registry.stream_asr_models.register("stream_sensevoice_v2")
class SensevoiceForStreamASRV2(StreamASRModel):
    """Sensevoice流式语音识别模型"""

    checkpoint: str = "iic/SenseVoiceSmall"
    endpoint: str = "modelscope"

    chunk_size_ms: int = 600  # chunk size in ms
    encoder_chunk_look_back: int = (
        4  # number of chunks to lookback for encoder self-attention
    )
    decoder_chunk_look_back: int = 1
    state: dict = {}

    sensevoice: AutoModel | None = None

    def transcribe_chunk(
        self, waveform: Waveform, is_last: bool = False, **kwargs
    ) -> List[AudioToken]:
        sample_rate = waveform.sample_rate
        data = waveform.data
        chunk_size = int(self.chunk_size_ms * sample_rate / 1000)
        state: dict = kwargs.get("state", self.state)
        buffer = state.pop("buffer", np.array([], dtype=np.float32))
        buffer = np.concatenate([buffer, data], axis=0)
        tokens = []
        if is_last:
            chunk = buffer
            stream = self.sensevoice.generate(
                input=chunk,
                fs=sample_rate,
                cache=state,
                is_final=True,
                chunk_size=[0, 10, 5],
                encoder_chunk_look_back=self.encoder_chunk_look_back,
                decoder_chunk_look_back=self.decoder_chunk_look_back,
            )
            for result in stream:
                if result["text"]:
                    tokens.append(AudioToken(text=result["text"]))
            self.reset_state(state)
        else:
            while len(buffer) > chunk_size:
                chunk = buffer[:chunk_size]
                buffer = buffer[chunk_size:]
                stream = self.sensevoice.generate(
                    input=chunk,
                    fs=sample_rate,
                    cache=state,
                    is_final=False,
                    chunk_size=[0, 10, 5],  # chunk size 10 * 60ms
                    encoder_chunk_look_back=self.encoder_chunk_look_back,
                    decoder_chunk_look_back=self.decoder_chunk_look_back,
                )
                for result in stream:
                    if result["text"]:
                        tokens.append(AudioToken(text=result["text"]))
            state["buffer"] = buffer
        return tokens

    def reset(self):
        self.reset_state(self.state)

    def reset_state(self, state: dict) -> dict:
        state.clear()
        buffer = np.array([], dtype=np.float32)
        return state.update({"buffer": buffer})

    def create_state(self) -> dict:
        buffer = np.array([])
        return {"buffer": buffer}

    def from_checkpoint(
        self,
        checkpoint_dir: str | Path | None = None,
        disable_update: bool = True,
        disable_log: bool = True,
        disable_pbar: bool = True,
        **kwargs,
    ) -> Self:
        if not checkpoint_dir:
            checkpoint_dir = self.download_checkpoint()
        checkpoint_dir = Path(checkpoint_dir)
        if not checkpoint_dir.exists():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_dir}")
        model = AutoModel(
            model=checkpoint_dir,
            disable_update=disable_update,
            disable_log=disable_log,
            disable_pbar=disable_pbar,
            **kwargs,
        )
        self.sensevoice = model
        return self
