"""Repository for typed persistence operations on Episodes, Artifacts, Events, and Jobs."""

from __future__ import annotations

import json
from typing import Optional
from let.models.entities import Artifact, Episode, Event, Job, utc_now_iso
from .connection import DatabaseManager


class Repository:
    """Data access repository for LET entities and asynchronous job queue."""

    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    # ---------------- Episodes ----------------

    def create_episode(self, episode: Episode) -> Episode:
        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO episodes (id, title, domain, mode, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    episode.id,
                    episode.title,
                    episode.domain,
                    episode.mode,
                    episode.status,
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
                SET title = ?, domain = ?, mode = ?, status = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    episode.title,
                    episode.domain,
                    episode.mode,
                    episode.status,
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

    # ---------------- Jobs (Asynchronous Queue) ----------------

    def create_job(self, job: Job) -> Job:
        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO jobs (
                    id, job_type, episode_id, artifact_id, payload_json,
                    status, attempts, max_attempts, error_message, worker_id,
                    created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        job_types: Optional[list[str]] = None,
    ) -> Optional[Job]:
        """Atomically claim the next queued job for execution."""
        now = utc_now_iso()
        with self.db.transaction() as conn:
            query = """
                SELECT * FROM jobs
                WHERE status = 'queued' AND attempts < max_attempts
            """
            params: list[object] = []
            if job_types:
                placeholders = ",".join("?" for _ in job_types)
                query += f" AND job_type IN ({placeholders})"
                params.extend(job_types)

            query += " ORDER BY created_at ASC LIMIT 1"
            row = conn.execute(query, params).fetchone()
            if not row:
                return None

            job_id = row["id"]
            conn.execute(
                """
                UPDATE jobs
                SET status = 'running',
                    worker_id = ?,
                    attempts = attempts + 1,
                    updated_at = ?
                WHERE id = ?
                """,
                (worker_id, now, job_id),
            )
            # Re-fetch updated row
            updated_row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
            return Job(**dict(updated_row))

    def update_job(self, job: Job) -> Job:
        job.updated_at = utc_now_iso()
        with self.db.transaction() as conn:
            conn.execute(
                """
                UPDATE jobs
                SET status = ?, attempts = ?, error_message = ?, worker_id = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    job.status,
                    job.attempts,
                    job.error_message,
                    job.worker_id,
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
