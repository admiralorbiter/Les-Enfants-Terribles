"""Local speech-to-text engine using faster-whisper with resilient CPU/CUDA fallback."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional
from let.models.entities import TranscriptData, TranscriptSegment
from .base import Transcriber

logger = logging.getLogger("let.transcription")


class FasterWhisperTranscriber(Transcriber):
    """Local, offline transcriber powered by faster-whisper with automatic CPU fallback."""

    def __init__(
        self,
        model_size: str = "base.en",
        device: str = "auto",
        compute_type: str = "default",
    ) -> None:
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self._model = None
        self._active_device = device

    @property
    def name(self) -> str:
        return "faster-whisper"

    @property
    def version(self) -> str:
        return f"{self.model_size}:{self._active_device}"

    def _init_model(self, device: str, compute_type: str):
        from faster_whisper import WhisperModel

        return WhisperModel(
            self.model_size,
            device=device,
            compute_type=compute_type,
        )

    def _get_model(self):
        """Lazy load model with graceful CPU fallback on CUDA initialization failure."""
        if self._model is None:
            try:
                self._model = self._init_model(self.device, self.compute_type)
                self._active_device = self.device
            except Exception as e:
                logger.warning(f"Failed to initialize Whisper on device '{self.device}': {e}. Falling back to CPU.")
                self._model = self._init_model("cpu", "int8")
                self._active_device = "cpu"
        return self._model

    def transcribe(self, audio_path: Path | str) -> TranscriptData:
        """Transcribe an audio file into timestamped segments with robust fallback safety."""
        path = Path(audio_path)
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {path}")

        try:
            model = self._get_model()
            segments_gen, info = model.transcribe(str(path), beam_size=5)
            segments: list[TranscriptSegment] = []
            full_text_parts: list[str] = []

            for seg in segments_gen:
                text = seg.text.strip()
                if text:
                    segments.append(
                        TranscriptSegment(
                            start_sec=round(seg.start, 2),
                            end_sec=round(seg.end, 2),
                            text=text,
                        )
                    )
                    full_text_parts.append(text)

        except Exception as e:
            logger.warning(f"Whisper transcription failed on '{self._active_device}': {e}. Retrying on CPU fallback...")
            try:
                self._model = self._init_model("cpu", "int8")
                self._active_device = "cpu"
                model = self._model
                segments_gen, info = model.transcribe(str(path), beam_size=5)
                segments = []
                full_text_parts = []
                for seg in segments_gen:
                    text = seg.text.strip()
                    if text:
                        segments.append(
                            TranscriptSegment(
                                start_sec=round(seg.start, 2),
                                end_sec=round(seg.end, 2),
                                text=text,
                            )
                        )
                        full_text_parts.append(text)
            except Exception as cpu_err:
                logger.error(f"CPU transcription fallback also failed: {cpu_err}")
                raise cpu_err

        full_text = " ".join(full_text_parts)

        return TranscriptData(
            text=full_text,
            language=getattr(info, "language", "en"),
            duration_sec=round(getattr(info, "duration", 0.0), 2),
            segments=segments,
            processor_name=self.name,
            processor_version=self.version,
        )
