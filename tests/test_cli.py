"""Tests for LET CLI commands, bare execution, doctor repairs, and backup/restore."""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path
from unittest.mock import patch
from let.cli import main, run_backup, run_doctor, run_restore, run_status
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
        file_path=stored.relative_path,
        file_hash=stored.file_hash,
        mime_type="audio/wav",
        size_bytes=stored.size_bytes,
    )
    repo.create_artifact(art)

    # Run Doctor
    args = argparse.Namespace(data_dir=str(test_config.data_dir), repair=False)
    run_doctor(args)
    captured = capsys.readouterr().out
    assert "[OK] ALL SYSTEMS HEALTHY" in captured
    assert "SHA-256 verified" in captured

    # Run Status
    run_status(args)
    captured_status = capsys.readouterr().out
    assert "Total Episodes     : 1" in captured_status
    assert "Raw Audio Captures : 1" in captured_status


def test_cli_doctor_repair_receipt(test_config: Config, capsys) -> None:
    db = DatabaseManager(test_config)
    repo = Repository(db)
    store = FileStore(test_config)

    receipt = store.write_capture_receipt(
        relative_file_path="raw/audio/repaired.webm",
        episode_id="ep_repaired_01",
        metadata={"title": "Repaired Episode", "domain": "movie"},
    )
    assert receipt.exists()

    args = argparse.Namespace(data_dir=str(test_config.data_dir), repair=True)
    run_doctor(args)
    captured = capsys.readouterr().out
    assert "Successfully repaired" in captured
    assert not receipt.exists()
    assert repo.get_episode("ep_repaired_01") is not None


def test_cli_backup_and_restore(test_config: Config, synthetic_audio_bytes: bytes, capsys) -> None:
    db = DatabaseManager(test_config)
    repo = Repository(db)
    store = FileStore(test_config)

    stored = store.save_raw_audio(synthetic_audio_bytes, "test.wav", "ep_bk_cli")
    ep = Episode(id="ep_bk_cli", title="Backup CLI Episode")
    repo.create_episode(ep)
    art = Artifact(
        id="art_bk_cli",
        episode_id="ep_bk_cli",
        artifact_type="audio",
        is_raw=True,
        file_path=stored.relative_path,
        file_hash=stored.file_hash,
        mime_type="audio/wav",
        size_bytes=stored.size_bytes,
    )
    repo.create_artifact(art)

    with tempfile.TemporaryDirectory() as tmp_dir:
        backup_out = Path(tmp_dir) / "test_backup"
        args_bk = argparse.Namespace(data_dir=str(test_config.data_dir), output=str(backup_out))
        run_backup(args_bk)
        captured = capsys.readouterr().out
        assert "Backup successfully created" in captured

        args_rst = argparse.Namespace(
            data_dir=str(test_config.data_dir),
            backup_dir=str(backup_out),
            target_dir=None,
            verify_only=True,
        )
        run_restore(args_rst)
        captured_rst = capsys.readouterr().out
        assert "Backup verification PASSED" in captured_rst


def test_bare_cli_dispatch() -> None:
    # Test that bare execution without subcommand calls run_server with safe default namespace
    with patch("sys.argv", ["let"]), patch("let.cli.run_server") as mock_run_server:
        main()
        assert mock_run_server.called
        call_args = mock_run_server.call_args[0][0]
        assert call_args.command is None
