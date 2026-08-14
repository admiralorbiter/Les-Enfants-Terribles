"""Tests for disaster recovery, backup creation, and verified restore rehearsal."""

from __future__ import annotations

import tempfile
from pathlib import Path
from let.config import Config
from let.db.connection import DatabaseManager
from let.db.repository import Repository
from let.models.entities import Artifact, Episode, Event, Job
from let.storage.backup import create_backup, verify_and_restore
from let.storage.file_store import FileStore


def test_create_backup_and_manifest(test_config: Config, synthetic_audio_bytes: bytes) -> None:
    db = DatabaseManager(test_config)
    repo = Repository(db)
    file_store = FileStore(test_config)

    # 1. Populate test data
    episode = Episode(id="ep_bk_1", title="Backup Test Episode", domain="movie", mode="explore")
    repo.create_episode(episode)

    stored = file_store.save_raw_audio(synthetic_audio_bytes, "test_bk.webm", episode_id=episode.id)
    artifact = Artifact(
        id="art_bk_1",
        episode_id=episode.id,
        artifact_type="audio",
        is_raw=True,
        file_path=stored.relative_path,
        file_hash=stored.file_hash,
        mime_type="audio/webm",
        size_bytes=stored.size_bytes,
    )
    repo.create_artifact(artifact)

    # 2. Create backup in a temporary folder
    with tempfile.TemporaryDirectory() as backup_tmp:
        backup_dir = Path(backup_tmp) / "backup_001"
        manifest = create_backup(test_config, backup_dir)

        assert manifest["database_integrity"] == "ok"
        assert manifest["total_files"] >= 2  # let.sqlite + raw audio file
        assert (backup_dir / "manifest.json").exists()
        assert (backup_dir / "let.sqlite").exists()

        # 3. Perform verify-only rehearsal
        verify_report = verify_and_restore(backup_dir, target_data_dir="unused", verify_only=True)
        assert verify_report["status"] == "verified"
        assert verify_report["database_integrity"] == "ok"
        assert verify_report["test_episodes_found"] >= 1

        # 4. Perform actual live restoration into a separate target directory
        with tempfile.TemporaryDirectory() as restore_target_tmp:
            restore_target = Path(restore_target_tmp) / "restored_data"
            restore_report = verify_and_restore(backup_dir, target_data_dir=restore_target, verify_only=False)

            assert restore_report["status"] == "restored"
            assert (restore_target / "let.sqlite").exists()

            # Validate restored database content
            restored_config = Config(data_dir=restore_target)
            restored_db = DatabaseManager(restored_config)
            restored_repo = Repository(restored_db)

            restored_ep = restored_repo.get_episode("ep_bk_1")
            assert restored_ep is not None
            assert restored_ep.title == "Backup Test Episode"

            restored_art = restored_repo.get_artifact("art_bk_1")
            assert restored_art is not None
            assert restored_art.file_hash == stored.file_hash
