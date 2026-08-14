"""Tests for atomic file storage and hash verification."""

from __future__ import annotations

import io
from pathlib import Path
from let.config import Config
from let.storage.file_store import FileStore


def test_ensure_directories(test_config: Config) -> None:
    assert test_config.data_dir.exists()
    assert test_config.raw_audio_dir.exists()
    assert test_config.derived_transcripts_dir.exists()
    assert test_config.backups_dir.exists()


def test_save_raw_audio_bytes(file_store: FileStore, synthetic_audio_bytes: bytes) -> None:
    res = file_store.save_raw_audio(synthetic_audio_bytes, "test.wav", episode_id="ep_123")
    
    assert res.file_path.exists()
    assert res.size_bytes == len(synthetic_audio_bytes)
    assert res.file_hash == file_store.compute_hash_bytes(synthetic_audio_bytes)
    assert "ep_123_" in res.file_path.name


def test_save_raw_audio_stream(file_store: FileStore, synthetic_audio_bytes: bytes) -> None:
    stream = io.BytesIO(synthetic_audio_bytes)
    res = file_store.save_raw_audio(stream, "sample.webm")

    assert res.file_path.exists()
    assert res.size_bytes == len(synthetic_audio_bytes)
    assert res.file_hash == file_store.compute_hash_bytes(synthetic_audio_bytes)


def test_verify_artifact_integrity(file_store: FileStore, synthetic_audio_bytes: bytes) -> None:
    res = file_store.save_raw_audio(synthetic_audio_bytes, "test.wav")
    
    # Valid check
    assert file_store.verify_artifact_integrity(res.file_path, res.file_hash) is True
    
    # Corrupted / mismatched check
    assert file_store.verify_artifact_integrity(res.file_path, "0" * 64) is False
    
    # Non-existent file check
    assert file_store.verify_artifact_integrity(Path("non_existent_file.wav"), res.file_hash) is False


def test_idempotent_save(file_store: FileStore, synthetic_audio_bytes: bytes) -> None:
    res1 = file_store.save_raw_audio(synthetic_audio_bytes, "test.wav", episode_id="ep_idem")
    res2 = file_store.save_raw_audio(synthetic_audio_bytes, "test.wav", episode_id="ep_idem")

    assert res1.file_path == res2.file_path
    assert res1.file_hash == res2.file_hash
