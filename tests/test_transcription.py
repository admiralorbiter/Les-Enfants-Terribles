"""Tests for speech-to-text transcriber implementations."""

from __future__ import annotations

import pytest
from pathlib import Path
from let.storage.file_store import FileStore
from let.transcription.faster_whisper_engine import FasterWhisperTranscriber
from let.transcription.mock_engine import MockTranscriber


def test_mock_transcriber(file_store: FileStore, synthetic_audio_bytes: bytes) -> None:
    stored = file_store.save_raw_audio(synthetic_audio_bytes, "test.wav")
    
    transcriber = MockTranscriber("Simulated movie reaction about pacing.")
    result = transcriber.transcribe(stored.file_path)

    assert result.text == "Simulated movie reaction about pacing."
    assert len(result.segments) == 1
    assert result.segments[0].text == "Simulated movie reaction about pacing."
    assert result.processor_name == "mock-whisper"


def test_transcriber_file_not_found() -> None:
    transcriber = MockTranscriber()
    with pytest.raises(FileNotFoundError):
        transcriber.transcribe(Path("non_existent_audio.wav"))
