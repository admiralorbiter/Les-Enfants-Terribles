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

    # Auto-transcribe prediction voice note if attached to episode
    if job.episode_id:
        episode = repo.get_episode(job.episode_id)
        if episode and episode.prediction and episode.prediction.prediction_artifact_id:
            pred_art = repo.get_artifact(episode.prediction.prediction_artifact_id)
            if pred_art and not episode.prediction.transcript_artifact_id:
                pred_path = file_store.to_absolute_path(pred_art.file_path)
                if pred_path.exists():
                    try:
                        pred_result = transcriber.transcribe(pred_path)
                        pred_json_str = pred_result.model_dump_json(indent=2)
                        pred_json_bytes = pred_json_str.encode("utf-8")
                        pred_tr_hash = FileStore.compute_hash_bytes(pred_json_bytes)

                        pred_target_filename = f"transcript_pred_{job.episode_id}_{pred_tr_hash[:16]}.json"
                        pred_rel_subpath = Path("derived") / "transcripts" / pred_target_filename
                        stored_pred_tr = file_store.save_derived_artifact(pred_json_bytes, pred_rel_subpath)

                        pred_tr_artifact_id = f"art_tr_pred_{uuid.uuid4().hex[:12]}"
                        pred_tr_artifact = Artifact(
                            id=pred_tr_artifact_id,
                            episode_id=episode.id,
                            artifact_type="transcript",
                            is_raw=False,
                            file_path=stored_pred_tr.relative_path,
                            file_hash=pred_tr_hash,
                            mime_type="application/json",
                            size_bytes=stored_pred_tr.size_bytes,
                            source_artifact_id=pred_art.id,
                            processor_name=transcriber.name,
                            processor_version=transcriber.version,
                        )
                        repo.create_artifact(pred_tr_artifact)

                        # Update prediction with derived transcript pointer without overwriting raw prediction identity
                        preds = episode.predictions
                        active_pred_id = episode.prediction.id
                        for p in preds:
                            if p.id == active_pred_id:
                                p.transcript_artifact_id = pred_tr_artifact_id
                                if not p.prediction_text or p.prediction_text == "(Spoken Voice Prediction)":
                                    p.prediction_text = pred_result.text.strip() or "(Spoken Voice Prediction)"
                        
                        episode.prediction_json = json.dumps([p.model_dump() for p in preds])
                        repo.update_episode(episode)

                        repo.create_event(
                            Event(
                                id=f"evt_{uuid.uuid4().hex[:12]}",
                                episode_id=episode.id,
                                event_type="prediction_transcription_completed",
                                payload_json=json.dumps(
                                    {
                                        "prediction_id": active_pred_id,
                                        "source_artifact_id": pred_art.id,
                                        "transcript_artifact_id": pred_tr_artifact_id,
                                        "processor": transcriber.name,
                                        "version": transcriber.version,
                                    }
                                ),
                            )
                        )
                    except Exception:
                        pass

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
