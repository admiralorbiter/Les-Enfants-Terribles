"""Domain entity models for Episodes, Artifacts, and Events."""

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
    event_type: str  # "capture_started", "capture_stopped", "mark", "note_added", "mode_changed"
    payload_json: str = "{}"
    created_at: str = Field(default_factory=utc_now_iso)
