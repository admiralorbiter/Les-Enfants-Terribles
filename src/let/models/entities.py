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


import re


class PredictionData(BaseModel):
    """An immutable pre-session prediction snapshot to compare against later evidence."""

    id: str
    target_concept_id: Optional[str] = None  # Stable concept ID e.g. "piano.tempo_rushing"
    target_concept: Optional[str] = None  # Backward compatibility / display label e.g., "Tempo / Rushing"
    prediction_text: str = ""
    prediction_artifact_id: Optional[str] = None  # Raw audio artifact for voice predictions
    transcript_artifact_id: Optional[str] = None  # Derived transcript artifact (FIX-02)
    confidence: Literal["low", "medium", "high"] = "medium"
    supersedes_prediction_id: Optional[str] = None  # Previous prediction ID if revised (FIX-01)
    created_at: str = Field(default_factory=utc_now_iso)

    @property
    def effective_concept_name(self) -> str:
        """Return clean concept name without UI glyphs."""
        if self.target_concept:
            return re.sub(r"^[^\w\s/]+", "", self.target_concept).strip()
        if self.target_concept_id:
            parts = self.target_concept_id.split(".")
            return parts[-1].replace("_", " ").title()
        return "General"


class DomainConcept(BaseModel):
    """A domain-specific concept term backed by epistemic provenance and stable identity."""

    id: str = ""  # Stable canonical ID, e.g. "cod.centering", "piano.tempo_rushing"
    term: str  # Clean display term, e.g., "Centering", "Tempo / Rushing"
    domain: DomainType = "general"
    icon: Optional[str] = None  # UI glyph, e.g., "🎯", "⏱️", "🔒"
    definition: str = ""  # Concise mechanistic explanation
    aliases: list[str] = Field(default_factory=list)  # ["crosshair placement", "pre-aim"]
    scope: str = "core"  # "core", "tactical", "pedagogical", "hypothesis"
    confidence: float = 1.0  # Epistemic confidence

    @property
    def display_label(self) -> str:
        """Formatted label with icon for UI rendering."""
        return f"{self.icon} {self.term}".strip() if self.icon else self.term


class Episode(BaseModel):
    """An episode is the primary organizing unit for cognitive reflections."""

    id: str
    title: str
    domain: DomainType = "general"
    mode: ModeType = "capture"
    status: str = "active"
    prediction_json: Optional[str] = None
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)

    @property
    def predictions(self) -> list[PredictionData]:
        """Deserialize prediction_json supporting legacy single-dict and append-only lists."""
        if not self.prediction_json:
            return []
        try:
            import json
            data = json.loads(self.prediction_json)
            if isinstance(data, list):
                return [PredictionData(**item) for item in data]
            elif isinstance(data, dict):
                return [PredictionData(**data)]
        except Exception:
            return []
        return []

    @property
    def prediction(self) -> Optional[PredictionData]:
        """Return the active (latest non-superseded) prediction for backward compatibility."""
        preds = self.predictions
        return preds[-1] if preds else None

    def append_prediction(self, pred: PredictionData) -> None:
        """Append a prediction to history, automatically linking supersedes pointer if revising."""
        current_preds = self.predictions
        if current_preds and not pred.supersedes_prediction_id:
            pred.supersedes_prediction_id = current_preds[-1].id
        
        current_preds.append(pred)
        import json
        self.prediction_json = json.dumps([p.model_dump() for p in current_preds])
        self.updated_at = utc_now_iso()

    def set_prediction(self, pred: PredictionData) -> None:
        """Backward-compatible setter that routes to append_prediction."""
        self.append_prediction(pred)


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
    event_type: str  # "capture_saved", "mark", "transcription_started", "analysis_imported", "perturbation_answered", "perturbation_rated", "self_prediction_recorded", etc.
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
    prediction_discrepancy: Optional[str] = None
    domain_concepts: list[DomainConcept] = Field(default_factory=list)
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

