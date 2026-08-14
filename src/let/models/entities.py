"""Domain entity models for Episodes, Artifacts, Events, Jobs, Transcripts, and Analyses."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal, Optional
from pydantic import BaseModel, Field


def utc_now_iso() -> str:
    """Return current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


DomainType = Literal["movie", "piano", "cod", "research", "programming", "general"]
ModeType = Literal[
    "capture",
    "explore",
    "challenge",
    "understand",
    "improve",
    "surprise",
    "decide",
]
JobStatus = Literal["queued", "running", "succeeded", "failed"]


class Episode(BaseModel):
    """An intentional episode container uniting lived evidence, derivations, and interventions."""

    id: str
    title: str = "Untitled Episode"
    domain: DomainType = "general"
    mode: ModeType = "capture"
    status: str = "active"
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)


class Artifact(BaseModel):
    """A durable file record—raw or derived—linked cryptographically via SHA-256."""

    id: str
    episode_id: str
    artifact_type: str  # "audio", "transcript", "text", "analysis", "mission_brief"
    is_raw: bool = True
    file_path: str
    file_hash: str  # SHA-256
    mime_type: str
    size_bytes: int
    source_artifact_id: Optional[str] = None
    processor_name: Optional[str] = None
    processor_version: Optional[str] = None
    created_at: str = Field(default_factory=utc_now_iso)


class Event(BaseModel):
    """A point-in-time occurrence within an episode."""

    id: str
    episode_id: str
    event_type: str  # "capture_saved", "mark", "transcription_started", "analysis_imported", etc.
    payload_json: str = "{}"
    created_at: str = Field(default_factory=utc_now_iso)


class Job(BaseModel):
    """An asynchronous task managed by the SQLite job queue."""

    id: str
    job_type: str  # e.g., "transcribe_audio"
    episode_id: Optional[str] = None
    artifact_id: Optional[str] = None
    payload_json: str = "{}"
    status: JobStatus = "queued"
    attempts: int = 0
    max_attempts: int = 3
    error_message: Optional[str] = None
    worker_id: Optional[str] = None
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)


class TranscriptSegment(BaseModel):
    """A timestamped segment within a transcript."""

    start_sec: float
    end_sec: float
    text: str


class TranscriptData(BaseModel):
    """Complete structured transcription result."""

    text: str
    language: str = "en"
    duration_sec: float = 0.0
    segments: list[TranscriptSegment] = Field(default_factory=list)
    processor_name: str = "faster-whisper"
    processor_version: str = "small.en"


class AnalysisData(BaseModel):
    """Structured dual output parsed from external AI Mission Brief response."""

    synthesis_text: str = ""
    perturbations: list[str] = Field(default_factory=list)
    provider: str = "manual"
    raw_response: str = ""
    created_at: str = Field(default_factory=utc_now_iso)
