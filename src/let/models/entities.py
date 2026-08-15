"""Core domain entities and data transfer objects for LET."""

from __future__ import annotations

import uuid
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
ArtifactType = Literal["audio", "video", "transcript", "analysis", "mission_brief", "text", "event_log"]
JobStatus = Literal["queued", "running", "succeeded", "failed"]


class Episode(BaseModel):
    """An episode is the primary organizing unit for cognitive reflections."""

    id: str
    title: str
    domain: DomainType = "general"
    mode: ModeType = "capture"
    status: str = "active"
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)


class Artifact(BaseModel):
    """An immutable file or structured output with cryptographic provenance."""

    id: str
    episode_id: str
    artifact_type: ArtifactType
    is_raw: bool
    file_path: str
    file_hash: str
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
    event_type: str  # "capture_saved", "mark", "transcription_started", "analysis_imported", "perturbation_answered", "perturbation_rated", etc.
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
    leased_by: Optional[str] = None
    leased_at: Optional[str] = None
    lease_expires_at: Optional[str] = None
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


class PerturbationItem(BaseModel):
    """An individual cognitive challenge/question with interactive response state."""

    id: str
    question_text: str
    rating: Optional[str] = None  # "sharp", "already_knew", "irrelevant"
    answer_text: Optional[str] = None
    answer_artifact_id: Optional[str] = None
    answered_at: Optional[str] = None


class AnalysisData(BaseModel):
    """Structured dual output parsed from external AI Mission Brief response or local heuristic generator."""

    synthesis_text: str = ""
    perturbations: list[str] = Field(default_factory=list)
    items: list[PerturbationItem] = Field(default_factory=list)
    provider: str = "manual"
    raw_response: str = ""
    created_at: str = Field(default_factory=utc_now_iso)

    def get_items(self) -> list[PerturbationItem]:
        """Return structured items, normalizing legacy string lists on the fly."""
        if self.items:
            return self.items
        items = []
        for i, q in enumerate(self.perturbations):
            items.append(PerturbationItem(id=f"pert_{i+1}", question_text=q))
        return items
