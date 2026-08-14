"""Abstract base class for transcription engines."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from let.models.entities import TranscriptData


class Transcriber(ABC):
    """Abstract speech-to-text transcriber interface."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the transcription provider / engine."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Model or engine version descriptor."""
        ...

    @abstractmethod
    def transcribe(self, audio_path: Path | str) -> TranscriptData:
        """Transcribe an audio file and return structured segments."""
        ...
