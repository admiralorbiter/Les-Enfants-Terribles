"""Deterministic mock transcriber for testing."""

from __future__ import annotations

from pathlib import Path
from let.models.entities import TranscriptData, TranscriptSegment
from .base import Transcriber


class MockTranscriber(Transcriber):
    """Mock transcriber returning deterministic synthetic segments."""

    def __init__(self, simulated_text: str = "This is a synthetic test reflection.") -> None:
        self.simulated_text = simulated_text

    @property
    def name(self) -> str:
        return "mock-whisper"

    @property
    def version(self) -> str:
        return "v0-mock"

    def transcribe(self, audio_path: Path | str) -> TranscriptData:
        path = Path(audio_path)
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {path}")

        segments = [
            TranscriptSegment(
                start_sec=0.0,
                end_sec=2.5,
                text=self.simulated_text,
            )
        ]

        return TranscriptData(
            text=self.simulated_text,
            language="en",
            duration_sec=2.5,
            segments=segments,
            processor_name=self.name,
            processor_version=self.version,
        )
