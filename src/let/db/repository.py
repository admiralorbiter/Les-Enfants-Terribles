"""Repository for typed persistence operations on Episodes, Artifacts, Events, and Jobs."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Optional
from let.models.entities import Artifact, Episode, Event, Job, utc_now_iso
from .connection import DatabaseManager


class Repository:
    """Data access repository for LET entities, single-transaction bundles, and leased job queue."""

    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    # ---------------- Episodes ----------------

    def create_episode(self, episode: Episode) -> Episode:
        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO episodes (id, title, domain, mode, status, prediction_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    episode.id,
                    episode.title,
                    episode.domain,
                    episode.mode,
                    episode.status,
                    episode.prediction_json,
                    episode.created_at,
                    episode.updated_at,
                ),
            )
        return episode

    def get_episode(self, episode_id: str) -> Optional[Episode]:
        with self.db.transaction() as conn:
            row = conn.execute(
                "SELECT * FROM episodes WHERE id = ?", (episode_id,)
            ).fetchone()
            if not row:
                return None
            return Episode(**dict(row))

    def list_episodes(self, limit: int = 50, domain: Optional[str] = None) -> list[Episode]:
        with self.db.transaction() as conn:
            if domain:
                rows = conn.execute(
                    """
                    SELECT * FROM episodes
                    WHERE domain = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                    """,
                    (domain, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT * FROM episodes
                    ORDER BY created_at DESC
                    LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
            return [Episode(**dict(row)) for row in rows]

    def update_episode(self, episode: Episode) -> Episode:
        episode.updated_at = utc_now_iso()
        with self.db.transaction() as conn:
            conn.execute(
                """
                UPDATE episodes
                SET title = ?, domain = ?, mode = ?, status = ?, prediction_json = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    episode.title,
                    episode.domain,
                    episode.mode,
                    episode.status,
                    episode.prediction_json,
                    episode.updated_at,
                    episode.id,
                ),
            )
        return episode

    def delete_episode(self, episode_id: str) -> bool:
        with self.db.transaction() as conn:
            cursor = conn.execute("DELETE FROM episodes WHERE id = ?", (episode_id,))
            return cursor.rowcount > 0

    # ---------------- Artifacts ----------------

    def create_artifact(self, artifact: Artifact) -> Artifact:
        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO artifacts (
                    id, episode_id, artifact_type, is_raw, file_path,
                    file_hash, mime_type, size_bytes, source_artifact_id,
                    processor_name, processor_version, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    artifact.id,
                    artifact.episode_id,
                    artifact.artifact_type,
                    1 if artifact.is_raw else 0,
                    artifact.file_path,
                    artifact.file_hash,
                    artifact.mime_type,
                    artifact.size_bytes,
                    artifact.source_artifact_id,
                    artifact.processor_name,
                    artifact.processor_version,
                    artifact.created_at,
                ),
            )
        return artifact

    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        with self.db.transaction() as conn:
            row = conn.execute(
                "SELECT * FROM artifacts WHERE id = ?", (artifact_id,)
            ).fetchone()
            if not row:
                return None
            data = dict(row)
            data["is_raw"] = bool(data["is_raw"])
            return Artifact(**data)

    def get_artifact_by_hash(self, file_hash: str) -> Optional[Artifact]:
        with self.db.transaction() as conn:
            row = conn.execute(
                "SELECT * FROM artifacts WHERE file_hash = ? ORDER BY created_at DESC LIMIT 1",
                (file_hash,),
            ).fetchone()
            if not row:
                return None
            data = dict(row)
            data["is_raw"] = bool(data["is_raw"])
            return Artifact(**data)

    def list_artifacts_for_episode(self, episode_id: str) -> list[Artifact]:
        with self.db.transaction() as conn:
            rows = conn.execute(
                """
                SELECT * FROM artifacts
                WHERE episode_id = ?
                ORDER BY created_at ASC
                """,
                (episode_id,),
            ).fetchall()
            results = []
            for row in rows:
                data = dict(row)
                data["is_raw"] = bool(data["is_raw"])
                results.append(Artifact(**data))
            return results

    def get_latest_transcript_for_episode(self, episode_id: str) -> Optional[Artifact]:
        with self.db.transaction() as conn:
            row = conn.execute(
                """
                SELECT * FROM artifacts
                WHERE episode_id = ? AND artifact_type = 'transcript'
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (episode_id,),
            ).fetchone()
            if not row:
                return None
            data = dict(row)
            data["is_raw"] = bool(data["is_raw"])
            return Artifact(**data)

    def get_latest_analysis_for_episode(self, episode_id: str) -> Optional[Artifact]:
        with self.db.transaction() as conn:
            row = conn.execute(
                """
                SELECT * FROM artifacts
                WHERE episode_id = ? AND artifact_type = 'analysis'
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (episode_id,),
            ).fetchone()
            if not row:
                return None
            data = dict(row)
            data["is_raw"] = bool(data["is_raw"])
            return Artifact(**data)

    def list_all_artifacts(self) -> list[Artifact]:
        with self.db.transaction() as conn:
            rows = conn.execute("SELECT * FROM artifacts ORDER BY created_at DESC").fetchall()
            results = []
            for row in rows:
                data = dict(row)
                data["is_raw"] = bool(data["is_raw"])
                results.append(Artifact(**data))
            return results

    # ---------------- Events ----------------

    def create_event(self, event: Event) -> Event:
        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO events (id, episode_id, event_type, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    event.id,
                    event.episode_id,
                    event.event_type,
                    event.payload_json,
                    event.created_at,
                ),
            )
        return event

    def list_events_for_episode(self, episode_id: str) -> list[Event]:
        with self.db.transaction() as conn:
            rows = conn.execute(
                """
                SELECT * FROM events
                WHERE episode_id = ?
                ORDER BY created_at ASC
                """,
                (episode_id,),
            ).fetchall()
            return [Event(**dict(row)) for row in rows]

    # ---------------- Atomic Capture Bundle ----------------

    def create_capture_bundle(
        self,
        artifact: Artifact,
        event: Event,
        episode: Optional[Episode] = None,
        job: Optional[Job] = None,
    ) -> None:
        """Atomically persist episode (if new), artifact, event, and job in one transaction."""
        with self.db.transaction() as conn:
            if episode is not None:
                conn.execute(
                    """
                    INSERT INTO episodes (id, title, domain, mode, status, prediction_json, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        episode.id,
                        episode.title,
                        episode.domain,
                        episode.mode,
                        episode.status,
                        episode.prediction_json,
                        episode.created_at,
                        episode.updated_at,
                    ),
                )

            conn.execute(
                """
                INSERT INTO artifacts (
                    id, episode_id, artifact_type, is_raw, file_path,
                    file_hash, mime_type, size_bytes, source_artifact_id,
                    processor_name, processor_version, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    artifact.id,
                    artifact.episode_id,
                    artifact.artifact_type,
                    1 if artifact.is_raw else 0,
                    artifact.file_path,
                    artifact.file_hash,
                    artifact.mime_type,
                    artifact.size_bytes,
                    artifact.source_artifact_id,
                    artifact.processor_name,
                    artifact.processor_version,
                    artifact.created_at,
                ),
            )

            conn.execute(
                """
                INSERT INTO events (id, episode_id, event_type, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    event.id,
                    event.episode_id,
                    event.event_type,
                    event.payload_json,
                    event.created_at,
                ),
            )

            if job is not None:
                conn.execute(
                    """
                    INSERT INTO jobs (
                        id, job_type, episode_id, artifact_id, payload_json,
                        status, attempts, max_attempts, error_message, worker_id,
                        leased_by, leased_at, lease_expires_at, created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        job.id,
                        job.job_type,
                        job.episode_id,
                        job.artifact_id,
                        job.payload_json,
                        job.status,
                        job.attempts,
                        job.max_attempts,
                        job.error_message,
                        job.worker_id,
                        job.leased_by,
                        job.leased_at,
                        job.lease_expires_at,
                        job.created_at,
                        job.updated_at,
                    ),
                )

    # ---------------- Jobs (Asynchronous Leased Queue) ----------------

    def create_job(self, job: Job) -> Job:
        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO jobs (
                    id, job_type, episode_id, artifact_id, payload_json,
                    status, attempts, max_attempts, error_message, worker_id,
                    leased_by, leased_at, lease_expires_at, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job.id,
                    job.job_type,
                    job.episode_id,
                    job.artifact_id,
                    job.payload_json,
                    job.status,
                    job.attempts,
                    job.max_attempts,
                    job.error_message,
                    job.worker_id,
                    job.leased_by,
                    job.leased_at,
                    job.lease_expires_at,
                    job.created_at,
                    job.updated_at,
                ),
            )
        return job

    def get_job(self, job_id: str) -> Optional[Job]:
        with self.db.transaction() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
            if not row:
                return None
            return Job(**dict(row))

    def claim_next_job(
        self,
        worker_id: str,
        lease_duration_seconds: float = 300.0,
        job_types: Optional[list[str]] = None,
    ) -> Optional[Job]:
        """Atomically claim the next queued or expired running job using a concurrency guard."""
        now = datetime.now(timezone.utc)
        now_iso = now.isoformat()
        lease_expires_iso = (now + timedelta(seconds=lease_duration_seconds)).isoformat()

        with self.db.transaction() as conn:
            query = """
                SELECT id FROM jobs
                WHERE (
                    status = 'queued'
                    OR (status = 'running' AND lease_expires_at IS NOT NULL AND lease_expires_at < ?)
                )
                AND attempts < max_attempts
            """
            params: list[object] = [now_iso]
            if job_types:
                placeholders = ",".join("?" for _ in job_types)
                query += f" AND job_type IN ({placeholders})"
                params.extend(job_types)

            query += " ORDER BY created_at ASC LIMIT 1"
            candidate = conn.execute(query, params).fetchone()
            if not candidate:
                return None

            job_id = candidate["id"]
            update_query = """
                UPDATE jobs
                SET status = 'running',
                    worker_id = ?,
                    leased_by = ?,
                    leased_at = ?,
                    lease_expires_at = ?,
                    attempts = attempts + 1,
                    updated_at = ?
                WHERE id = ?
                  AND (
                      status = 'queued'
                      OR (status = 'running' AND lease_expires_at IS NOT NULL AND lease_expires_at < ?)
                  )
            """
            cursor = conn.execute(
                update_query,
                (worker_id, worker_id, now_iso, lease_expires_iso, now_iso, job_id, now_iso),
            )
            if cursor.rowcount == 0:
                # Concurrent worker won the claim race
                return None

            row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
            return Job(**dict(row))

    def recover_stale_jobs(self) -> int:
        """Reset stale running jobs with expired leases back to queued or failed."""
        now_iso = utc_now_iso()
        with self.db.transaction() as conn:
            cursor = conn.execute(
                """
                UPDATE jobs
                SET status = 'queued',
                    worker_id = NULL,
                    leased_by = NULL,
                    leased_at = NULL,
                    lease_expires_at = NULL,
                    updated_at = ?
                WHERE status = 'running'
                  AND lease_expires_at IS NOT NULL
                  AND lease_expires_at < ?
                  AND attempts < max_attempts
                """,
                (now_iso, now_iso),
            )
            requeued = cursor.rowcount

            conn.execute(
                """
                UPDATE jobs
                SET status = 'failed',
                    error_message = 'Job lease expired and max attempts reached',
                    updated_at = ?
                WHERE status = 'running'
                  AND lease_expires_at IS NOT NULL
                  AND lease_expires_at < ?
                  AND attempts >= max_attempts
                """,
                (now_iso, now_iso),
            )
            return requeued

    def update_job(self, job: Job) -> Job:
        job.updated_at = utc_now_iso()
        with self.db.transaction() as conn:
            conn.execute(
                """
                UPDATE jobs
                SET status = ?, attempts = ?, error_message = ?, worker_id = ?,
                    leased_by = ?, leased_at = ?, lease_expires_at = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    job.status,
                    job.attempts,
                    job.error_message,
                    job.worker_id,
                    job.leased_by,
                    job.leased_at,
                    job.lease_expires_at,
                    job.updated_at,
                    job.id,
                ),
            )
        return job

    def list_jobs_for_episode(self, episode_id: str) -> list[Job]:
        with self.db.transaction() as conn:
            rows = conn.execute(
                """
                SELECT * FROM jobs
                WHERE episode_id = ?
                ORDER BY created_at DESC
                """,
                (episode_id,),
            ).fetchall()
            return [Job(**dict(row)) for row in rows]

    def list_jobs(self, limit: int = 100) -> list[Job]:
        with self.db.transaction() as conn:
            rows = conn.execute(
                "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
            return [Job(**dict(row)) for row in rows]
