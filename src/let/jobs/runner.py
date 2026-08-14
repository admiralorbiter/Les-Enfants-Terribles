"""In-process background worker supervisor."""

from __future__ import annotations

import atexit
import logging
import threading
from typing import Optional
from let.config import Config
from let.db.repository import Repository
from let.storage.file_store import FileStore
from let.transcription.base import Transcriber
from .worker import JobWorker

logger = logging.getLogger("let.runner")


class BackgroundWorkerRunner:
    """Manages an in-process worker thread alongside Flask."""

    def __init__(
        self,
        config: Config,
        repo: Repository,
        file_store: FileStore,
        transcriber: Optional[Transcriber] = None,
    ) -> None:
        self.worker = JobWorker(
            config=config,
            repo=repo,
            file_store=file_store,
            transcriber=transcriber,
        )
        self.stop_event = threading.Event()
        self.thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start background worker thread."""
        if self.thread is not None and self.thread.is_alive():
            return

        self.stop_event.clear()
        self.thread = threading.Thread(
            target=self.worker.run_loop,
            kwargs={"poll_interval": 1.0, "stop_event": self.stop_event},
            name="LET-JobWorker-Thread",
            daemon=True,
        )
        self.thread.start()
        logger.info("Background worker thread started.")
        atexit.register(self.stop)

    def stop(self, timeout: float = 3.0) -> None:
        """Stop background worker thread."""
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join(timeout=timeout)
            logger.info("Background worker thread stopped.")
