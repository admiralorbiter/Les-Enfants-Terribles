"""SQLite connection manager with WAL mode and foreign key enforcement."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from let.config import Config
from .schema import SCHEMA_V1_SQL


class DatabaseManager:
    """Manages SQLite database connections and transactions."""

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
        """Apply schema scripts if tables do not exist."""
        self.config.ensure_directories()
        with self.transaction() as conn:
            conn.executescript(SCHEMA_V1_SQL)
