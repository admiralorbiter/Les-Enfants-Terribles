"""Unit and integration tests for Slice 2A Mission Brief Bridge and Polished Synthesis."""

from __future__ import annotations

import io
from pathlib import Path
from flask.testing import FlaskClient
from let.config import Config
from let.db.repository import Repository
from let.liquid.brief_generator import generate_mission_brief
from let.liquid.response_parser import parse_ai_response
from let.models.entities import Episode, TranscriptData, TranscriptSegment
from let.storage.file_store import FileStore


def test_generate_mission_brief() -> None:
    ep = Episode(
        id="ep_brief_001",
        title="MGS2 Meta Commentary",
        domain="movie",
        mode="challenge",
    )
    transcript = TranscriptData(
        text="I think the ending of MGS2 was intentionally disorienting to force the player to think.",
        duration_sec=12.5,
        segments=[
            TranscriptSegment(
                start_sec=0.0,
                end_sec=12.5,
                text="I think the ending of MGS2 was intentionally disorienting to force the player to think.",
            )
        ],
    )

    brief = generate_mission_brief(ep, transcript)
    assert "MISSION BRIEF" in brief
    assert "MGS2 Meta Commentary" in brief
    assert "MOVIE" in brief
    assert "CHALLENGE" in brief
    assert "Polished Synthesis" in brief
    assert "Liquid Perturbations" in brief
    assert "intentionally disorienting" in brief


def test_parse_ai_response_structured() -> None:
    sample_response = """
### Polished Synthesis
The climax of Metal Gear Solid 2 serves as a deliberate meta-narrative destabilization. Kojima dismantles the player's reliance on digital certainty, forcing an active philosophical reckoning with memetic control.

### Liquid Perturbations
1. What specific evidence from the Arsenal Gear sequence differentiates intentional disorientation from fragmented development pacing?
2. How does the player's loss of control challenge your own definition of authorship in interactive media?
"""
    parsed = parse_ai_response(sample_response, provider="ChatGPT Plus")
    assert "deliberate meta-narrative destabilization" in parsed.synthesis_text
    assert len(parsed.perturbations) == 2
    assert "Arsenal Gear sequence" in parsed.perturbations[0]
    assert "interactive media" in parsed.perturbations[1]
    assert parsed.provider == "ChatGPT Plus"


def test_parse_ai_response_freeform_fallback() -> None:
    freeform = "This was a fascinating session on Chopin Nocturne Op 9 No 2. Why did the left-hand rubato falter at measure 14? Can you isolate the fifth finger transition tomorrow?"
    parsed = parse_ai_response(freeform, provider="manual")
    assert "Chopin Nocturne" in parsed.synthesis_text
    assert len(parsed.perturbations) >= 2
    assert any("measure 14?" in q for q in parsed.perturbations)


def test_import_analysis_lifecycle(
    client: FlaskClient,
    test_config: Config,
    repo: Repository,
    file_store: FileStore,
    synthetic_audio_bytes: bytes,
) -> None:
    # 1. Capture episode
    data = {
        "audio": (io.BytesIO(synthetic_audio_bytes), "reflection.wav"),
        "title": "Piano Polyrhythm Practice",
        "domain": "piano",
        "mode": "improve",
    }
    res = client.post("/api/capture/audio", data=data, content_type="multipart/form-data")
    assert res.status_code == 201
    ep_id = res.get_json()["episode"]["id"]

    # 2. Get Mission Brief via endpoint
    brief_res = client.get(f"/episodes/{ep_id}/brief")
    assert brief_res.status_code == 200
    assert b"Piano Polyrhythm Practice" in brief_res.data

    # 3. Import AI Response
    ai_output = """### Polished Synthesis
Focused practice on 3:2 polyrhythms. Hand independence achieved at 72 BPM, but tension escalated in the right wrist during transition bars.

### Liquid Perturbations
1. Did the right wrist tension stem from forearm angle or finger over-extension?
2. What specific tempo reduction restores zero-tension execution?
"""
    import_res = client.post(
        f"/api/episodes/{ep_id}/import_analysis",
        data={"response_text": ai_output, "provider": "Claude 3.7"},
    )
    assert import_res.status_code == 201
    payload = import_res.get_json()
    art_id = payload["artifact"]["id"]

    # 4. Verify derived analysis artifact on disk and DB
    artifact = repo.get_artifact(art_id)
    assert artifact is not None
    assert artifact.artifact_type == "analysis"
    assert artifact.is_raw is False
    assert artifact.processor_version == "Claude 3.7"
    assert Path(artifact.file_path).exists()

    # 5. Cryptographic hash check
    assert file_store.verify_artifact_integrity(artifact.file_path, artifact.file_hash) is True

    # 6. Verify detail view displays synthesis & liquid card
    detail_res = client.get(f"/episodes/{ep_id}")
    assert detail_res.status_code == 200
    assert b"Polished Synthesis" in detail_res.data
    assert b"Hand independence achieved" in detail_res.data
    assert b"Liquid Cognitive Perturbations" in detail_res.data
    assert b"right wrist tension stem" in detail_res.data


def test_update_episode_title(
    client: FlaskClient,
    synthetic_audio_bytes: bytes,
) -> None:
    data = {"audio": (io.BytesIO(synthetic_audio_bytes), "test.wav"), "title": "Old Title"}
    res = client.post("/api/capture/audio", data=data, content_type="multipart/form-data")
    ep_id = res.get_json()["episode"]["id"]

    update_res = client.post(
        f"/api/episodes/{ep_id}/update_title",
        json={"title": "Mastering the Chopin Nocturne"},
    )
    assert update_res.status_code == 200
    assert update_res.get_json()["episode"]["title"] == "Mastering the Chopin Nocturne"

    detail_res = client.get(f"/episodes/{ep_id}")
    assert b"Mastering the Chopin Nocturne" in detail_res.data
