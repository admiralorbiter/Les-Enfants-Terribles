"""Flask application factory for LET."""

from __future__ import annotations

from pathlib import Path
from flask import Flask
from let.config import Config, get_config
from let.db.connection import DatabaseManager
from let.db.repository import Repository
from let.storage.file_store import FileStore
from .routes import bp as main_bp


def create_app(config: Config | None = None) -> Flask:
    """Create and configure the LET Flask application."""
    if config is None:
        config = get_config()

    template_folder = Path(__file__).parent / "templates"
    static_folder = Path(__file__).parent / "static"

    app = Flask(
        __name__,
        template_folder=str(template_folder),
        static_folder=str(static_folder),
    )

    app.config["SECRET_KEY"] = "let-dev-secret-key"
    app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500 MB max upload

    db_manager = DatabaseManager(config)
    repo = Repository(db_manager)
    file_store = FileStore(config)

    app.extensions["let_config"] = config
    app.extensions["let_db"] = db_manager
    app.extensions["let_repo"] = repo
    app.extensions["let_store"] = file_store

    app.register_blueprint(main_bp)

    return app
