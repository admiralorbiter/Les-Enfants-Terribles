"""Tests for Slice 2D / E003 — Pre-Session Prediction, Calibration Loop, and Domain Vocabulary Scaffolding."""

from __future__ import annotations

import io
import json
import uuid
import pytest
from let.liquid.brief_generator import generate_mission_brief
from let.liquid.heuristics import (
    DOMAIN_CONCEPT_GLOSSARY,
    DOMAIN_CONCEPT_PALETTES,
    create_local_heuristic_analysis,
    generate_local_perturbations,
    get_domain_concepts,
)
from let.liquid.response_parser import import_analysis_response, parse_ai_response
from let.models.entities import (
    AnalysisData,
    Artifact,
    Episode,
    Event,
    PredictionData,
    TranscriptData,
)


def test_episode_prediction_model_and_serialization():
    """Verify PredictionData model serialization and deserialization via Episode properties."""
    pred = PredictionData(
        id="pred_123",
        target_concept="Tempo / Rushing",
        prediction_text="Left hand jumps will slip because of tempo rushing.",
        confidence="high",
    )
    episode = Episode(
        id="ep_test_pred",
        title="Piano Nocturne Practice",
        domain="piano",
        mode="improve",
    )
    assert episode.prediction is None
    episode.set_prediction(pred)

    assert episode.prediction is not None
    assert episode.prediction.id == "pred_123"
    assert episode.prediction.target_concept == "Tempo / Rushing"
    assert episode.prediction.prediction_text == "Left hand jumps will slip because of tempo rushing."
    assert episode.prediction.confidence == "high"
    assert "pred_123" in episode.prediction_json


def test_repository_crud_with_prediction(repo):
    """Verify Episode persistence with prediction_json across create, get, list, and update."""
    pred = PredictionData(
        id="pred_repo_1",
        target_concept="Centering / Aim",
        prediction_text="Testing centering on corners; predict KD will rise if I stop sprint-challenging.",
        confidence="medium",
    )
    ep = Episode(
        id="ep_repo_pred",
        title="COD Ranked Match",
        domain="cod",
        mode="challenge",
    )
    ep.set_prediction(pred)

    repo.create_episode(ep)

    fetched = repo.get_episode("ep_repo_pred")
    assert fetched is not None
    assert fetched.prediction is not None
    assert fetched.prediction.target_concept == "Centering / Aim"
    assert fetched.prediction.confidence == "medium"
    assert "centering" in fetched.prediction.prediction_text

    # Update prediction
    pred2 = PredictionData(
        id="pred_repo_2",
        target_concept="Rotation Timing",
        prediction_text="Updated prediction text.",
        confidence="low",
    )
    fetched.set_prediction(pred2)
    repo.update_episode(fetched)

    refetched = repo.get_episode("ep_repo_pred")
    assert refetched.prediction.target_concept == "Rotation Timing"
    assert refetched.prediction.confidence == "low"


def test_domain_concept_palettes_and_glossary():
    """Verify all 6 core domains have starter concept palettes and glossary definitions."""
    domains = ["piano", "cod", "programming", "research", "movie", "general"]
    for d in domains:
        assert d in DOMAIN_CONCEPT_PALETTES
        assert len(DOMAIN_CONCEPT_PALETTES[d]) >= 4
        assert d in DOMAIN_CONCEPT_GLOSSARY
        assert len(DOMAIN_CONCEPT_GLOSSARY[d]) >= 2

        concepts = get_domain_concepts(d)
        assert len(concepts) >= 2
        for c in concepts:
            assert "term" in c and len(c["term"]) > 0
            assert "definition" in c and len(c["definition"]) > 0


def test_calibration_discrepancy_heuristic_generation():
    """Verify that when an episode has a prediction, heuristic probes generate calibration discrepancy questions."""
    pred = PredictionData(
        id="pred_calib",
        target_concept="Tension / Posture",
        prediction_text="Right forearm will lock up during the octave run.",
        confidence="high",
    )
    ep_with_pred = Episode(
        id="ep_calib_1",
        title="Piano Etude Practice",
        domain="piano",
        mode="improve",
    )
    ep_with_pred.set_prediction(pred)

    probes = generate_local_perturbations(ep_with_pred)
    assert len(probes) == 2
    assert "You predicted" in probes[0].question_text
    assert "Right forearm will lock up" in probes[0].question_text
    assert "High confidence on Tension / Posture" in probes[0].question_text

    analysis = create_local_heuristic_analysis(ep_with_pred)
    assert analysis.prediction_discrepancy is not None
    assert "Right forearm will lock up" in analysis.prediction_discrepancy
    assert len(analysis.domain_concepts) >= 3
    assert any("Pedal" in c.term or "Legato" in c.term or "Arm-Weight" in c.term for c in analysis.domain_concepts)


def test_mission_brief_includes_prediction_snapshot():
    """Verify that Mission Brief Markdown export includes the immutable prediction snapshot and calibration directives."""
    pred = PredictionData(
        id="pred_mb",
        target_concept="State Invariants",
        prediction_text="Refactoring SQLite transaction will break lease renewal edge case.",
        confidence="high",
    )
    episode = Episode(
        id="ep_mb_pred",
        title="Async Queue Refactor",
        domain="programming",
        mode="understand",
    )
    episode.set_prediction(pred)

    brief = generate_mission_brief(
        episode=episode,
        transcript_text="Completed the transaction refactor. Leases worked but foreign keys caused an error.",
    )

    assert "Immutable Pre-Session Prediction Snapshot" in brief
    assert "Refactoring SQLite transaction will break lease renewal" in brief
    assert "Calibration & Discrepancy Directive" in brief


def test_import_analysis_attaches_domain_concepts_and_discrepancy(test_config, repo, file_store):
    """Verify importing an external AI response into an episode with prediction populates concepts and discrepancy."""
    pred = PredictionData(
        id="pred_imp",
        target_concept="Formalist Framing",
        prediction_text="Expected the ending sequence to feel unearned.",
        confidence="medium",
    )
    ep = Episode(
        id="ep_imp_pred",
        title="Blade Runner Reflection",
        domain="movie",
        mode="explore",
    )
    ep.set_prediction(pred)
    repo.create_episode(ep)

    raw_ai_text = """### Polished Synthesis
The ending formal geometry and lighting framed the dilemma beautifully.

### Liquid Perturbations
1. Did the rain motif serve as an aesthetic amplifier or narrative mask?
2. What specific camera distance created the emotional rupture?
"""

    art, analysis = import_analysis_response(
        raw_response=raw_ai_text,
        provider="Claude 3.7",
        episode_id=ep.id,
        source_artifact_id=None,
        config=test_config,
        repo=repo,
        file_store=file_store,
    )

    assert analysis.prediction_discrepancy is not None
    assert "Expected the ending sequence to feel unearned" in analysis.prediction_discrepancy
    assert len(analysis.domain_concepts) >= 2
    assert any("Framing" in c.term or "Sound" in c.term for c in analysis.domain_concepts)


def test_api_capture_with_pre_prediction(client, repo):
    """Verify POST /api/capture/audio seamlessly saves pre-prediction form fields into the new Episode."""
    audio_data = io.BytesIO(b"RIFF....WAVEfmt ....data....test audio")
    audio_data.seek(0)

    data = {
        "audio": (audio_data, "test.wav", "audio/wav"),
        "title": "Calibration Session 1",
        "domain": "piano",
        "mode": "improve",
        "prediction_text": "I predict bar 20 will rush due to awkward fingering.",
        "prediction_concept": "⏱️ Tempo / Rushing",
        "prediction_confidence": "high",
    }

    res = client.post(
        "/api/capture/audio",
        data=data,
        content_type="multipart/form-data",
        headers={"HX-Request": "true"},
    )
    assert res.status_code == 200

    episodes = repo.list_episodes(limit=10)
    assert len(episodes) == 1
    ep = episodes[0]
    assert ep.title == "Calibration Session 1"
    assert ep.prediction is not None
    assert ep.prediction.target_concept == "⏱️ Tempo / Rushing"
    assert ep.prediction.prediction_text == "I predict bar 20 will rush due to awkward fingering."
    assert ep.prediction.confidence == "high"


def test_api_set_prediction_endpoint(client, repo):
    """Verify POST /api/episodes/<id>/set_prediction sets prediction and logs event."""
    ep = Episode(id="ep_set_pred", title="Empty Episode", domain="cod", mode="improve")
    repo.create_episode(ep)

    # Set prediction
    res = client.post(
        "/api/episodes/ep_set_pred/set_prediction",
        json={
            "prediction_text": "Will maintain 60% hold time on P2.",
            "target_concept": "🛡️ Cover / Anchor",
            "confidence": "high",
        },
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert data["prediction"]["prediction_text"] == "Will maintain 60% hold time on P2."

    updated = repo.get_episode("ep_set_pred")
    assert updated.prediction is not None
    assert updated.prediction.confidence == "high"

    events = repo.list_events_for_episode("ep_set_pred")
    pred_events = [e for e in events if e.event_type == "self_prediction_recorded"]
    assert len(pred_events) == 1


def test_api_capture_with_voice_prediction(client, repo):
    """Verify capturing an episode with a separate voice prediction audio file."""
    primary_audio = io.BytesIO(b"RIFF....WAVEfmt ....data....primary audio")
    pred_audio = io.BytesIO(b"RIFF....WAVEfmt ....data....prediction voice note")

    data = {
        "audio": (primary_audio, "practice.wav", "audio/wav"),
        "prediction_audio": (pred_audio, "pred_note.wav", "audio/wav"),
        "title": "Piano Voice Calibration",
        "domain": "piano",
        "mode": "improve",
        "prediction_concept": "🦾 Tension / Posture",
        "prediction_confidence": "high",
    }

    res = client.post(
        "/api/capture/audio",
        data=data,
        content_type="multipart/form-data",
        headers={"HX-Request": "true"},
    )
    assert res.status_code == 200

    episodes = repo.list_episodes(limit=10)
    ep = episodes[0]
    assert ep.title == "Piano Voice Calibration"
    assert ep.prediction is not None
    assert ep.prediction.prediction_artifact_id is not None
    assert ep.prediction.target_concept == "🦾 Tension / Posture"
    assert ep.prediction.confidence == "high"

    # Verify both audio artifacts exist in database
    artifacts = repo.list_artifacts_for_episode(ep.id)
    raw_audios = [a for a in artifacts if a.is_raw and a.artifact_type == "audio"]
    assert len(raw_audios) == 2
    pred_art = next(a for a in raw_audios if a.id == ep.prediction.prediction_artifact_id)
    assert pred_art is not None


def test_api_set_prediction_with_voice_audio(client, repo):
    """Verify attaching a voice note via /api/episodes/<id>/set_prediction."""
    ep = Episode(id="ep_voice_pred_set", title="COD Voice Pred", domain="cod", mode="challenge")
    repo.create_episode(ep)

    pred_audio = io.BytesIO(b"RIFF....WAVEfmt ....data....prediction audio")
    data = {
        "audio": (pred_audio, "voice_prediction.wav", "audio/wav"),
        "target_concept": "⚔️ Ego-Challenging",
        "confidence": "high",
    }

    res = client.post(
        f"/api/episodes/{ep.id}/set_prediction",
        data=data,
        content_type="multipart/form-data",
    )
    assert res.status_code == 200

    updated = repo.get_episode(ep.id)
    assert updated.prediction is not None
    assert updated.prediction.prediction_artifact_id is not None
    assert updated.prediction.target_concept == "⚔️ Ego-Challenging"
    assert updated.prediction.confidence == "high"


