"""Tests for SQLite persistence, transactions, and entity relations."""

from __future__ import annotations

import sqlite3
import pytest
from let.db.repository import Repository
from let.models.entities import Artifact, Episode, Event


def test_episode_crud(repo: Repository) -> None:
    episode = Episode(
        id="ep_test_001",
        title="Test Movie Reaction",
        domain="movie",
        mode="explore",
    )
    repo.create_episode(episode)

    retrieved = repo.get_episode("ep_test_001")
    assert retrieved is not None
    assert retrieved.id == "ep_test_001"
    assert retrieved.title == "Test Movie Reaction"
    assert retrieved.domain == "movie"
    assert retrieved.mode == "explore"

    # List
    episodes = repo.list_episodes(domain="movie")
    assert len(episodes) == 1
    assert episodes[0].id == "ep_test_001"

    # Update
    retrieved.title = "Updated Title"
    repo.update_episode(retrieved)
    assert repo.get_episode("ep_test_001").title == "Updated Title"

    # Delete
    assert repo.delete_episode("ep_test_001") is True
    assert repo.get_episode("ep_test_001") is None


def test_artifact_and_lineage(repo: Repository) -> None:
    ep = Episode(id="ep_art_001", title="Piano Episode", domain="piano")
    repo.create_episode(ep)

    # Raw artifact
    raw_art = Artifact(
        id="art_raw_001",
        episode_id="ep_art_001",
        artifact_type="audio",
        is_raw=True,
        file_path="/tmp/raw.wav",
        file_hash="a" * 64,
        mime_type="audio/wav",
        size_bytes=1024,
    )
    repo.create_artifact(raw_art)

    # Derived artifact pointing to raw source
    derived_art = Artifact(
        id="art_der_001",
        episode_id="ep_art_001",
        artifact_type="transcript",
        is_raw=False,
        file_path="/tmp/transcript.json",
        file_hash="b" * 64,
        mime_type="application/json",
        size_bytes=256,
        source_artifact_id="art_raw_001",
        processor_name="faster-whisper",
        processor_version="0.1.0",
    )
    repo.create_artifact(derived_art)

    artifacts = repo.list_artifacts_for_episode("ep_art_001")
    assert len(artifacts) == 2
    assert artifacts[0].id == "art_raw_001"
    assert artifacts[0].is_raw is True
    assert artifacts[1].id == "art_der_001"
    assert artifacts[1].source_artifact_id == "art_raw_001"


def test_event_logging(repo: Repository) -> None:
    ep = Episode(id="ep_evt_001", title="COD Reflection", domain="cod")
    repo.create_episode(ep)

    evt = Event(
        id="evt_001",
        episode_id="ep_evt_001",
        event_type="mark",
        payload_json='{"note": "flanked on B", "timestamp_sec": 42.5}',
    )
    repo.create_event(evt)

    events = repo.list_events_for_episode("ep_evt_001")
    assert len(events) == 1
    assert events[0].event_type == "mark"
    assert "flanked" in events[0].payload_json


def test_foreign_key_enforcement(repo: Repository) -> None:
    # Attempt to insert artifact without valid episode must fail
    orphan_artifact = Artifact(
        id="art_orphan",
        episode_id="non_existent_ep",
        artifact_type="audio",
        is_raw=True,
        file_path="/tmp/orphan.wav",
        file_hash="c" * 64,
        mime_type="audio/wav",
        size_bytes=512,
    )
    with pytest.raises(sqlite3.IntegrityError):
        repo.create_artifact(orphan_artifact)
