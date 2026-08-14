"""SQLite schema definition and initialization."""

SCHEMA_V1_SQL = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

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

CREATE INDEX IF NOT EXISTS idx_episodes_created_at ON episodes(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_artifacts_episode_id ON artifacts(episode_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_file_hash ON artifacts(file_hash);
CREATE INDEX IF NOT EXISTS idx_events_episode_id ON events(episode_id);
"""
