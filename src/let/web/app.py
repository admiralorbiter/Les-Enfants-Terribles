"""Flask application factory for LET."""

from __future__ import annotations

import os
from pathlib import Path
from flask import Flask
from let.config import Config, get_config
from let.db.connection import DatabaseManager
from let.db.repository import Repository
from let.jobs.runner import BackgroundWorkerRunner
from let.storage.file_store import FileStore
from .routes import bp as main_bp


def create_app(config: Config | None = None, start_worker: bool = True) -> Flask:
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

    # Start background worker if enabled and not in testing / reloader parent
    if start_worker and config.enable_background_worker:
        # In debug mode, only start worker in the child process
        if not config.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            worker_runner = BackgroundWorkerRunner(config, repo, file_store)
            worker_runner.start()
            app.extensions["let_worker_runner"] = worker_runner

    app.register_blueprint(main_bp)

    return app
