"""SQLite connection manager with WAL mode, migration runner, and online backup."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from let.config import Config
from .schema import initialize_and_migrate


class DatabaseManager:
    """Manages SQLite database connections, schema migrations, and backups."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.db_path = config.db_path
        self.initialize_schema()

    def get_connection(self) -> sqlite3.Connection:
        """Create a configured SQLite connection."""
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        return conn

    @contextmanager
    def transaction(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager yielding a transactional connection."""
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def initialize_schema(self) -> None:
        """Ensure data directories exist and execute all pending migrations."""
        self.config.ensure_directories()
        with self.transaction() as conn:
            initialize_and_migrate(conn)

    def backup_to(self, target_path: Path | str) -> None:
        """Perform a clean online SQLite backup using the native SQLite backup API.

        This avoids file-copy corruption on active WAL databases.
        """
        target_path = Path(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if target_path.exists():
            target_path.unlink()

        source_conn = self.get_connection()
        try:
            dest_conn = sqlite3.connect(str(target_path))
            try:
                source_conn.backup(dest_conn)
            finally:
                dest_conn.close()
        finally:
            source_conn.close()

    def check_integrity(self) -> bool:
        """Run SQLite PRAGMA integrity_check and return True if healthy."""
        with self.transaction() as conn:
            result = conn.execute("PRAGMA integrity_check;").fetchone()
            if result and result[0] == "ok":
                return True
        return False
