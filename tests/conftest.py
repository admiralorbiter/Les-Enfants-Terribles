"""Pytest fixtures for LET tests."""

from __future__ import annotations

import io
import pytest
from pathlib import Path
from flask import Flask
from flask.testing import FlaskClient
from let.config import Config
from let.db.connection import DatabaseManager
from let.db.repository import Repository
from let.storage.file_store import FileStore
from let.web.app import create_app


@pytest.fixture
def test_config(tmp_path: Path) -> Config:
    """Provide isolated configuration rooted in a temporary test directory."""
    data_dir = tmp_path / "test_let_data"
    cfg = Config(data_dir=data_dir, host="127.0.0.1", port=5000, debug=True)
    cfg.ensure_directories()
    return cfg


@pytest.fixture
def db_manager(test_config: Config) -> DatabaseManager:
    """Provide isolated database manager."""
    return DatabaseManager(test_config)


@pytest.fixture
def repo(db_manager: DatabaseManager) -> Repository:
    """Provide repository pointing to isolated database."""
    return Repository(db_manager)


@pytest.fixture
def file_store(test_config: Config) -> FileStore:
    """Provide storage instance pointing to isolated temporary directory."""
    return FileStore(test_config)


@pytest.fixture
def app(test_config: Config) -> Flask:
    """Provide test Flask application instance."""
    app_instance = create_app(test_config)
    app_instance.config["TESTING"] = True
    return app_instance


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Provide test HTTP client."""
    return app.test_client()


@pytest.fixture
def synthetic_audio_bytes() -> bytes:
    """Provide deterministic mock audio payload with a minimal WAV header."""
    # 44-byte minimal WAV header + 100 bytes of silence/noise
    header = (
        b"RIFF\x94\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00"
        b"\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x70\x00\x00\x00"
    )
    payload = b"\x00" * 100
    return header + payload
