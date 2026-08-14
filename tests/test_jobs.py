"""Tests for SQLite-backed asynchronous job queue with worker leases and stale recovery."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
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

    # 2. Claim job atomically with lease
    claimed = repo.claim_next_job(worker_id="test_worker_A", lease_duration_seconds=60.0)
    assert claimed is not None
    assert claimed.id == "job_001"
    assert claimed.status == "running"
    assert claimed.worker_id == "test_worker_A"
    assert claimed.leased_by == "test_worker_A"
    assert claimed.lease_expires_at is not None
    assert claimed.attempts == 1

    # 3. Subsequent claim while running must return None
    claimed_again = repo.claim_next_job(worker_id="test_worker_B")
    assert claimed_again is None

    # 4. Mark job succeeded
    claimed.status = "succeeded"
    repo.update_job(claimed)

    updated = repo.get_job("job_001")
    assert updated.status == "succeeded"


def test_stale_job_lease_recovery(repo: Repository) -> None:
    # Create a job that expired in the past
    past_iso = (datetime.now(timezone.utc) - timedelta(seconds=600)).isoformat()
    job = Job(
        id="job_stale_001",
        job_type="transcribe_audio",
        status="running",
        worker_id="crashed_worker",
        leased_by="crashed_worker",
        lease_expires_at=past_iso,
        attempts=1,
        max_attempts=3,
    )
    repo.create_job(job)

    # 1. Test claim_next_job directly recovers and claims expired lease
    claimed = repo.claim_next_job(worker_id="new_worker", lease_duration_seconds=300.0)
    assert claimed is not None
    assert claimed.id == "job_stale_001"
    assert claimed.worker_id == "new_worker"
    assert claimed.attempts == 2

    # 2. Test recover_stale_jobs method explicitly
    job2 = Job(
        id="job_stale_002",
        job_type="transcribe_audio",
        status="running",
        worker_id="dead_worker",
        leased_by="dead_worker",
        lease_expires_at=past_iso,
        attempts=1,
        max_attempts=3,
    )
    repo.create_job(job2)
    requeued = repo.recover_stale_jobs()
    assert requeued >= 1
    assert repo.get_job("job_stale_002").status == "queued"


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
