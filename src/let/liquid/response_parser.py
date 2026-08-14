"""Parser and storage manager for imported AI Mission Brief responses."""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path
from typing import Optional, Tuple
from let.config import Config
from let.db.repository import Repository
from let.models.entities import AnalysisData, Artifact, Event
from let.storage.file_store import FileStore


def parse_ai_response(raw_text: str, provider: str = "manual") -> AnalysisData:
    """Parse pasted external model response into structured synthesis and perturbations."""
    text = raw_text.strip()
    synthesis_text = ""
    perturbations: list[str] = []

    # Regex patterns for delimiter sections
    synthesis_match = re.search(
        r"(?:^|\n)#{1,4}\s*(?:Polished\s+Synthesis|Synthesis|Summary|Review\s+Note)[:\s]*\n([\s\S]*?)(?=(?:\n#{1,4}\s*(?:Liquid\s+Perturbations|Perturbations|Questions)|$))",
        text,
        re.IGNORECASE,
    )
    perturbations_match = re.search(
        r"(?:^|\n)#{1,4}\s*(?:Liquid\s+Perturbations|Perturbations|Questions)[:\s]*\n([\s\S]*)$",
        text,
        re.IGNORECASE,
    )

    if synthesis_match:
        synthesis_text = synthesis_match.group(1).strip()

    if perturbations_match:
        pert_raw = perturbations_match.group(1).strip()
        # Extract numbered items or bullet points
        lines = pert_raw.split("\n")
        current_item: list[str] = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            # Matches "1.", "2)", "-", "*"
            if re.match(r"^(?:\d+[\.\)]|[-*•])\s+", stripped):
                if current_item:
                    perturbations.append(" ".join(current_item))
                    current_item = []
                clean_line = re.sub(r"^(?:\d+[\.\)]|[-*•])\s+", "", stripped)
                current_item.append(clean_line)
            else:
                if current_item:
                    current_item.append(stripped)
                else:
                    current_item.append(stripped)
        if current_item:
            perturbations.append(" ".join(current_item))

    # Fallback if delimiters were not strictly followed
    if not synthesis_text and not perturbations:
        synthesis_text = text
        # Extract any sentences ending with a question mark as perturbations
        sentences = re.split(r"(?<=[.?!])\s+", text)
        for s in sentences:
            if s.strip().endswith("?"):
                perturbations.append(s.strip())

    return AnalysisData(
        synthesis_text=synthesis_text,
        perturbations=perturbations,
        provider=provider,
        raw_response=text,
    )


def import_analysis_response(
    raw_response: str,
    provider: str,
    episode_id: str,
    source_artifact_id: Optional[str],
    config: Config,
    repo: Repository,
    file_store: FileStore,
) -> Tuple[Artifact, AnalysisData]:
    """Persist imported external AI response as a derived artifact with relative path and SHA-256 integrity."""
    config.ensure_directories()
    analysis_data = parse_ai_response(raw_response, provider=provider)

    json_bytes = analysis_data.model_dump_json(indent=2).encode("utf-8")
    analysis_hash = FileStore.compute_hash_bytes(json_bytes)

    target_filename = f"analysis_{episode_id}_{analysis_hash[:16]}.json"
    rel_subpath = Path("derived") / "analyses" / target_filename
    stored = file_store.save_derived_artifact(json_bytes, rel_subpath)

    artifact_id = f"art_an_{uuid.uuid4().hex[:12]}"
    artifact = Artifact(
        id=artifact_id,
        episode_id=episode_id,
        artifact_type="analysis",
        is_raw=False,
        file_path=stored.relative_path,
        file_hash=analysis_hash,
        mime_type="application/json",
        size_bytes=stored.size_bytes,
        source_artifact_id=source_artifact_id,
        processor_name="mission_brief_bridge",
        processor_version="v1.0",
    )
    repo.create_artifact(artifact)

    # Log event
    repo.create_event(
        Event(
            id=f"evt_{uuid.uuid4().hex[:12]}",
            episode_id=episode_id,
            event_type="analysis_imported",
            payload_json=json.dumps(
                {
                    "artifact_id": artifact_id,
                    "provider": provider,
                    "file_hash": analysis_hash,
                    "source_artifact_id": source_artifact_id,
                    "perturbations_count": len(analysis_data.perturbations),
                }
            ),
        )
    )

    return artifact, analysis_data
