"""Tests for LET CLI doctor and status commands."""

from __future__ import annotations

import argparse
from pathlib import Path
from let.cli import run_doctor, run_status
from let.config import Config
from let.db.connection import DatabaseManager
from let.db.repository import Repository
from let.models.entities import Artifact, Episode
from let.storage.file_store import FileStore


def test_cli_doctor_and_status(test_config: Config, synthetic_audio_bytes: bytes, capsys) -> None:
    # Set up sample data in test config
    db = DatabaseManager(test_config)
    repo = Repository(db)
    store = FileStore(test_config)

    # Save real artifact
    stored = store.save_raw_audio(synthetic_audio_bytes, "test.wav", "ep_cli_001")
    
    ep = Episode(id="ep_cli_001", title="CLI Test Episode", domain="general")
    repo.create_episode(ep)

    art = Artifact(
        id="art_cli_001",
        episode_id="ep_cli_001",
        artifact_type="audio",
        is_raw=True,
        file_path=str(stored.file_path),
        file_hash=stored.file_hash,
        mime_type="audio/wav",
        size_bytes=stored.size_bytes,
    )
    repo.create_artifact(art)

    # Run Doctor
    args = argparse.Namespace(data_dir=str(test_config.data_dir))
    run_doctor(args)
    captured = capsys.readouterr().out
    assert "[OK] ALL SYSTEMS HEALTHY" in captured
    assert "SHA-256 verified" in captured

    # Run Status
    run_status(args)
    captured_status = capsys.readouterr().out
    assert "Total Episodes     : 1" in captured_status
    assert "Raw Audio Captures : 1" in captured_status
