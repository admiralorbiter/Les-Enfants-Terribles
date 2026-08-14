"""Tests for SQLite-backed asynchronous job queue."""

from __future__ import annotations

from let.db.repository import Repository
from let.models.entities import Episode, Job


def test_job_lifecycle_and_atomic_claim(repo: Repository) -> None:
    # 1. Create episode & job
    ep = Episode(id="ep_job_001", title="Job Test")
    repo.create_episode(ep)

    job1 = Job(
        id="job_001",
        job_type="transcribe_audio",
        episode_id="ep_job_001",
        status="queued",
    )
    repo.create_job(job1)

    # 2. Claim job atomically
    claimed = repo.claim_next_job(worker_id="test_worker_A")
    assert claimed is not None
    assert claimed.id == "job_001"
    assert claimed.status == "running"
    assert claimed.worker_id == "test_worker_A"
    assert claimed.attempts == 1

    # 3. Subsequent claim while running must return None
    claimed_again = repo.claim_next_job(worker_id="test_worker_B")
    assert claimed_again is None

    # 4. Mark job succeeded
    claimed.status = "succeeded"
    repo.update_job(claimed)
    
    updated = repo.get_job("job_001")
    assert updated.status == "succeeded"


def test_job_retry_limit(repo: Repository) -> None:
    job = Job(
        id="job_retry_001",
        job_type="transcribe_audio",
        status="queued",
        attempts=2,
        max_attempts=3,
    )
    repo.create_job(job)

    # Claim attempt 3 (reaches max)
    claimed = repo.claim_next_job(worker_id="w1")
    assert claimed.attempts == 3

    # Mark failed
    claimed.status = "failed"
    claimed.error_message = "Permanent error"
    repo.update_job(claimed)

    # Further claims return None
    assert repo.claim_next_job(worker_id="w1") is None
