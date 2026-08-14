"""Asynchronous job worker loop."""

from __future__ import annotations

import logging
import threading
import time
import uuid
from typing import Optional
from let.config import Config
from let.db.repository import Repository
from let.models.entities import Job
from let.storage.file_store import FileStore
from let.transcription.base import Transcriber
from let.transcription.faster_whisper_engine import FasterWhisperTranscriber
from .handlers import handle_transcribe_audio

logger = logging.getLogger("let.worker")


class JobWorker:
    """Processes queued background tasks."""

    def __init__(
        self,
        config: Config,
        repo: Repository,
        file_store: FileStore,
        transcriber: Optional[Transcriber] = None,
        worker_id: Optional[str] = None,
    ) -> None:
        self.config = config
        self.repo = repo
        self.file_store = file_store
        self.worker_id = worker_id or f"worker_{uuid.uuid4().hex[:8]}"

        if transcriber is None:
            self.transcriber = FasterWhisperTranscriber(
                model_size=config.whisper_model_size,
                device=config.whisper_device,
                compute_type=config.whisper_compute_type,
            )
        else:
            self.transcriber = transcriber

    def run_once(self) -> bool:
        """Attempt to claim and process one job. Returns True if work was done."""
        job = self.repo.claim_next_job(self.worker_id)
        if not job:
            return False

        logger.info(f"Worker {self.worker_id} claimed job {job.id} ({job.job_type})")

        try:
            if job.job_type == "transcribe_audio":
                handle_transcribe_audio(
                    job=job,
                    config=self.config,
                    repo=self.repo,
                    file_store=self.file_store,
                    transcriber=self.transcriber,
                )
            else:
                raise ValueError(f"Unknown job type: {job.job_type}")

            job.status = "succeeded"
            job.error_message = None
            self.repo.update_job(job)
            logger.info(f"Job {job.id} completed successfully.")
            return True

        except Exception as e:
            logger.error(f"Job {job.id} failed: {e}", exc_info=True)
            if job.attempts >= job.max_attempts:
                job.status = "failed"
            else:
                job.status = "queued"  # Will be retried
            job.error_message = str(e)
            self.repo.update_job(job)
            return True

    def run_loop(
        self,
        poll_interval: float = 1.0,
        stop_event: Optional[threading.Event] = None,
    ) -> None:
        """Run worker loop until stopped."""
        logger.info(f"Starting LET Job Worker [{self.worker_id}] (poll={poll_interval}s)...")
        while stop_event is None or not stop_event.is_set():
            did_work = self.run_once()
            if not did_work:
                if stop_event:
                    stop_event.wait(poll_interval)
                else:
                    time.sleep(poll_interval)
