"""SQLite schema definition, versioning, and migration runner."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Callable, List, Tuple


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# Migration 1: Base Schema
MIGRATION_V1_SQL = """
CREATE TABLE IF NOT EXISTS episodes (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    domain TEXT NOT NULL DEFAULT 'general',
    mode TEXT NOT NULL DEFAULT 'capture',
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS artifacts (
    id TEXT PRIMARY KEY,
    episode_id TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    is_raw INTEGER NOT NULL DEFAULT 1,
    file_path TEXT NOT NULL,
    file_hash TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    size_bytes INTEGER NOT NULL,
    source_artifact_id TEXT,
    processor_name TEXT,
    processor_version TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE,
    FOREIGN KEY (source_artifact_id) REFERENCES artifacts(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    episode_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    job_type TEXT NOT NULL,
    episode_id TEXT,
    artifact_id TEXT,
    payload_json TEXT NOT NULL DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'queued',
    attempts INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 3,
    error_message TEXT,
    worker_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE,
    FOREIGN KEY (artifact_id) REFERENCES artifacts(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_episodes_created_at ON episodes(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_artifacts_episode_id ON artifacts(episode_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_file_hash ON artifacts(file_hash);
CREATE INDEX IF NOT EXISTS idx_events_episode_id ON events(episode_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status_created ON jobs(status, created_at ASC);
CREATE INDEX IF NOT EXISTS idx_jobs_episode_id ON jobs(episode_id);
"""


def _migrate_v2(conn: sqlite3.Connection) -> None:
    """Migration 2: Add lease columns to jobs table."""
    # Check existing columns in jobs
    columns = [row[1] for row in conn.execute("PRAGMA table_info(jobs)").fetchall()]
    if "leased_by" not in columns:
        conn.execute("ALTER TABLE jobs ADD COLUMN leased_by TEXT;")
    if "leased_at" not in columns:
        conn.execute("ALTER TABLE jobs ADD COLUMN leased_at TEXT;")
    if "lease_expires_at" not in columns:
        conn.execute("ALTER TABLE jobs ADD COLUMN lease_expires_at TEXT;")

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_jobs_lease ON jobs(status, lease_expires_at);"
    )


# Ordered registry of migrations: (version, description, SQL string or callable)
MIGRATIONS: List[Tuple[int, str, str | Callable[[sqlite3.Connection], None]]] = [
    (1, "Base schema (episodes, artifacts, events, jobs)", MIGRATION_V1_SQL),
    (2, "Add worker lease fields to jobs", _migrate_v2),
]

CURRENT_SCHEMA_VERSION = 2


def initialize_and_migrate(conn: sqlite3.Connection) -> int:
    """Ensure schema_migrations exists and apply all pending migrations in order."""
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            applied_at TEXT NOT NULL,
            description TEXT NOT NULL
        );
        """
    )

    applied_rows = conn.execute(
        "SELECT version FROM schema_migrations ORDER BY version ASC"
    ).fetchall()
    applied_versions = {row[0] for row in applied_rows}

    for version, description, action in MIGRATIONS:
        if version not in applied_versions:
            if isinstance(action, str):
                conn.executescript(action)
            elif callable(action):
                action(conn)
            conn.execute(
                """
                INSERT INTO schema_migrations (version, applied_at, description)
                VALUES (?, ?, ?)
                """,
                (version, _utc_now_iso(), description),
            )

    latest_version = conn.execute(
        "SELECT MAX(version) FROM schema_migrations"
    ).fetchone()[0]
    return latest_version or 0
