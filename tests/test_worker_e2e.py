"""End-to-end integration tests for audio capture, async worker, and transcript replay."""

from __future__ import annotations

import io
from pathlib import Path
from flask.testing import FlaskClient
from let.config import Config
from let.db.repository import Repository
from let.jobs.worker import JobWorker
from let.storage.file_store import FileStore
from let.transcription.mock_engine import MockTranscriber


def test_end_to_end_capture_and_async_transcription(
    client: FlaskClient,
    test_config: Config,
    repo: Repository,
    file_store: FileStore,
    synthetic_audio_bytes: bytes,
) -> None:
    # 1. Capture audio
    data = {
        "audio": (io.BytesIO(synthetic_audio_bytes), "spontaneous_reflection.wav"),
        "title": "Async Worker Pipeline Test",
        "domain": "research",
    }
    res = client.post("/api/capture/audio", data=data, content_type="multipart/form-data")
    assert res.status_code == 201

    payload = res.get_json()
    ep_id = payload["episode"]["id"]
    raw_art_id = payload["artifact"]["id"]
    job_id = payload["job"]["id"]

    # 2. Worker executes job
    mock_transcriber = MockTranscriber(simulated_text="This is an automated test transcript.")
    worker = JobWorker(test_config, repo, file_store, transcriber=mock_transcriber)

    did_work = worker.run_once()
    assert did_work is True

    # 3. Verify job status
    job = repo.get_job(job_id)
    assert job.status == "succeeded"
    assert job.error_message is None

    # 4. Verify derived transcript artifact
    latest_tr = repo.get_latest_transcript_for_episode(ep_id)
    assert latest_tr is not None
    assert latest_tr.artifact_type == "transcript"
    assert latest_tr.is_raw is False
    assert latest_tr.source_artifact_id == raw_art_id
    assert latest_tr.processor_name == "mock-whisper"
    assert file_store.to_absolute_path(latest_tr.file_path).exists()

    # 5. Verify cryptographic hash
    assert file_store.verify_artifact_integrity(latest_tr.file_path, latest_tr.file_hash) is True

    # 6. Verify HTML transcript endpoint
    tr_html_res = client.get(f"/episodes/{ep_id}/transcript")
    assert tr_html_res.status_code == 200
    assert b"This is an automated test transcript." in tr_html_res.data
    assert b"seekAudio" in tr_html_res.data


def test_transcription_replay_preserves_both_versions(
    client: FlaskClient,
    test_config: Config,
    repo: Repository,
    file_store: FileStore,
    synthetic_audio_bytes: bytes,
) -> None:
    # 1. Initial capture and transcription
    data = {"audio": (io.BytesIO(synthetic_audio_bytes), "test_audio.wav")}
    res = client.post("/api/capture/audio", data=data, content_type="multipart/form-data")
    ep_id = res.get_json()["episode"]["id"]
    raw_art_id = res.get_json()["artifact"]["id"]

    worker_v1 = JobWorker(test_config, repo, file_store, transcriber=MockTranscriber("Version 1 Transcript"))
    worker_v1.run_once()

    tr1 = repo.get_latest_transcript_for_episode(ep_id)
    assert tr1 is not None

    # 2. Trigger Replay (re-transcribe)
    replay_res = client.post(f"/api/episodes/{ep_id}/transcribe")
    assert replay_res.status_code == 201

    worker_v2 = JobWorker(test_config, repo, file_store, transcriber=MockTranscriber("Version 2 Replayed Transcript"))
    worker_v2.run_once()

    # 3. Verify that BOTH derived artifacts exist and link to same raw audio
    all_artifacts = repo.list_artifacts_for_episode(ep_id)
    transcripts = [a for a in all_artifacts if a.artifact_type == "transcript"]
    assert len(transcripts) == 2
    assert transcripts[0].source_artifact_id == raw_art_id
    assert transcripts[1].source_artifact_id == raw_art_id
    assert transcripts[0].file_hash != transcripts[1].file_hash
    assert file_store.to_absolute_path(transcripts[0].file_path).exists()
    assert file_store.to_absolute_path(transcripts[1].file_path).exists()
