"""Job handlers for asynchronous task execution."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from let.config import Config
from let.db.repository import Repository
from let.models.entities import Artifact, Event, Job
from let.storage.file_store import FileStore
from let.transcription.base import Transcriber


def handle_transcribe_audio(
    job: Job,
    config: Config,
    repo: Repository,
    file_store: FileStore,
    transcriber: Transcriber,
) -> str:
    """Execute audio transcription job and persist derived transcript artifact."""
    if not job.artifact_id:
        raise ValueError(f"Job {job.id} has no artifact_id specified")

    audio_artifact = repo.get_artifact(job.artifact_id)
    if not audio_artifact:
        raise FileNotFoundError(f"Audio artifact {job.artifact_id} not found in database")

    audio_path = file_store.to_absolute_path(audio_artifact.file_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file missing on disk: {audio_path}")

    # Log transcription started event
    if job.episode_id:
        repo.create_event(
            Event(
                id=f"evt_{uuid.uuid4().hex[:12]}",
                episode_id=job.episode_id,
                event_type="transcription_started",
                payload_json=json.dumps(
                    {
                        "job_id": job.id,
                        "source_artifact_id": audio_artifact.id,
                        "processor": transcriber.name,
                        "version": transcriber.version,
                    }
                ),
            )
        )

    # Execute speech-to-text
    result = transcriber.transcribe(audio_path)
    json_str = result.model_dump_json(indent=2)
    json_bytes = json_str.encode("utf-8")
    transcript_hash = FileStore.compute_hash_bytes(json_bytes)

    # Persist derived transcript atomically via FileStore
    target_filename = f"transcript_{job.episode_id}_{transcript_hash[:16]}.json"
    rel_subpath = Path("derived") / "transcripts" / target_filename
    stored = file_store.save_derived_artifact(json_bytes, rel_subpath)

    # Register derived artifact in SQLite with lineage pointer and relative path
    transcript_artifact_id = f"art_tr_{uuid.uuid4().hex[:12]}"
    transcript_artifact = Artifact(
        id=transcript_artifact_id,
        episode_id=job.episode_id or audio_artifact.episode_id,
        artifact_type="transcript",
        is_raw=False,
        file_path=stored.relative_path,
        file_hash=transcript_hash,
        mime_type="application/json",
        size_bytes=stored.size_bytes,
        source_artifact_id=audio_artifact.id,
        processor_name=transcriber.name,
        processor_version=transcriber.version,
    )
    repo.create_artifact(transcript_artifact)

    # Log completion event
    if job.episode_id:
        repo.create_event(
            Event(
                id=f"evt_{uuid.uuid4().hex[:12]}",
                episode_id=job.episode_id,
                event_type="transcription_completed",
                payload_json=json.dumps(
                    {
                        "transcript_artifact_id": transcript_artifact_id,
                        "segments_count": len(result.segments),
                        "duration_sec": result.duration_sec,
                    }
                ),
            )
        )

    return f"Transcription completed. {len(result.segments)} segment(s) generated."
