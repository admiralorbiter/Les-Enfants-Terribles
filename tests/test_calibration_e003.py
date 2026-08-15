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
    assert len(fetched.predictions) == 1

    # Append revised prediction (FIX-01)
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
    assert len(refetched.predictions) == 2
    assert refetched.predictions[0].id == "pred_repo_1"
    assert refetched.predictions[1].id == "pred_repo_2"
    assert refetched.predictions[1].supersedes_prediction_id == "pred_repo_1"


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
            assert "id" in c and len(c["id"]) > 0


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
        target_concept_id="programming.state_invariants",
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
    assert "Structural conditions that must remain valid" in brief


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
    assert any("Composition" in c.term or "Pacing" in c.term or "Tone" in c.term for c in analysis.domain_concepts)


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
        "prediction_concept_id": "piano.tempo_rushing",
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
    assert ep.prediction.target_concept_id == "piano.tempo_rushing"
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
            "target_concept_id": "cod.cover_anchor",
            "confidence": "high",
        },
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert data["prediction"]["prediction_text"] == "Will maintain 60% hold time on P2."
    assert data["prediction"]["target_concept_id"] == "cod.cover_anchor"

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
        "prediction_concept_id": "piano.tension_posture",
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
        "target_concept_id": "cod.ego_challenging",
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


def test_multi_artifact_bundle_atomicity(repo):
    """Verify create_capture_bundle atomically registers multiple artifacts (FIX-03)."""
    ep = Episode(id="ep_multi_art", title="Multi Artifact Bundle", domain="piano")
    art1 = Artifact(
        id="art_1",
        episode_id="ep_multi_art",
        artifact_type="audio",
        is_raw=True,
        file_path="raw/audio/art1.wav",
        file_hash="hash1",
        mime_type="audio/wav",
        size_bytes=100,
    )
    art2 = Artifact(
        id="art_2",
        episode_id="ep_multi_art",
        artifact_type="audio",
        is_raw=True,
        file_path="raw/audio/art2.wav",
        file_hash="hash2",
        mime_type="audio/wav",
        size_bytes=50,
    )
    evt = Event(id="evt_1", episode_id="ep_multi_art", event_type="capture_saved")

    repo.create_capture_bundle(artifacts=[art1, art2], event=evt, episode=ep)

    saved_arts = repo.list_artifacts_for_episode("ep_multi_art")
    assert len(saved_arts) == 2
    assert {a.id for a in saved_arts} == {"art_1", "art_2"}


def test_multi_file_recovery_receipt(file_store):
    """Verify write_capture_receipt supports multi-file lists and raw_files metadata (FIX-03)."""
    receipt_path = file_store.write_capture_receipt(
        relative_file_path=["raw/audio/ep1_main.wav", "raw/audio/ep1_pred.wav"],
        episode_id="ep_receipt_test",
        metadata={"title": "Crash Recovery Test"},
        raw_files=[
            {"artifact_id": "art_main", "relative_path": "raw/audio/ep1_main.wav"},
            {"artifact_id": "art_pred", "relative_path": "raw/audio/ep1_pred.wav"},
        ],
    )
    assert receipt_path.exists()
    with open(receipt_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["episode_id"] == "ep_receipt_test"
    assert len(data["relative_file_paths"]) == 2
    assert len(data["raw_files"]) == 2
    file_store.remove_capture_receipt(receipt_path)
    assert not receipt_path.exists()


def test_api_concept_exposure_telemetry(client, repo):
    """Verify POST /api/telemetry/concept_exposure records concept_exposed event (FIX-06)."""
    ep = Episode(id="ep_telemetry_1", title="Telemetry Test Episode", domain="piano")
    repo.create_episode(ep)

    res = client.post(
        "/api/telemetry/concept_exposure",
        json={
            "episode_id": "ep_telemetry_1",
            "concept_id": "piano.tempo_rushing",
            "concept_term": "Tempo / Rushing",
            "domain": "piano",
            "phase": "before_activity",
            "presentation": "chip",
            "user_requested": True,
            "context": {"view": "recorder", "action": "chip_selected"},
        },
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["status"] == "logged"

    events = repo.list_events_for_episode("ep_telemetry_1")
    assert len(events) == 1
    assert events[0].event_type == "concept_exposed"
    payload = json.loads(events[0].payload_json)
    assert payload["concept_id"] == "piano.tempo_rushing"
    assert payload["user_requested"] is True


def test_prediction_voice_transcription_derived_artifact_lineage(test_config, repo, file_store):
    """Verify handle_transcribe_audio persists derived transcript for prediction voice note with lineage (FIX-02)."""
    from let.jobs.handlers import handle_transcribe_audio
    from let.models.entities import Job
    from let.transcription.mock_engine import MockTranscriber

    ep = Episode(id="ep_pred_tr_lineage", title="Voice Lineage Test", domain="piano")
    pred_audio_stored = file_store.save_raw_audio(
        data=io.BytesIO(b"RIFF....WAVEfmt ....data....prediction voice audio"),
        original_filename="pred.wav",
        episode_id=ep.id,
    )
    pred_art = Artifact(
        id="art_pred_voice_1",
        episode_id=ep.id,
        artifact_type="audio",
        is_raw=True,
        file_path=pred_audio_stored.relative_path,
        file_hash=pred_audio_stored.file_hash,
        mime_type="audio/wav",
        size_bytes=pred_audio_stored.size_bytes,
    )
    pred = PredictionData(
        id="pred_voice_1",
        target_concept="Tempo / Rushing",
        prediction_text="(Spoken Voice Prediction)",
        prediction_artifact_id=pred_art.id,
        confidence="high",
    )
    ep.set_prediction(pred)

    main_audio_stored = file_store.save_raw_audio(
        data=io.BytesIO(b"RIFF....WAVEfmt ....data....main capture audio"),
        original_filename="main.wav",
        episode_id=ep.id,
    )
    main_art = Artifact(
        id="art_main_1",
        episode_id=ep.id,
        artifact_type="audio",
        is_raw=True,
        file_path=main_audio_stored.relative_path,
        file_hash=main_audio_stored.file_hash,
        mime_type="audio/wav",
        size_bytes=main_audio_stored.size_bytes,
    )

    evt = Event(id="evt_init", episode_id=ep.id, event_type="capture_saved")
    job = Job(id="job_tr_main", job_type="transcribe_audio", episode_id=ep.id, artifact_id=main_art.id)

    repo.create_capture_bundle(
        artifacts=[main_art, pred_art],
        event=evt,
        episode=ep,
        job=job,
    )

    transcriber = MockTranscriber(
        simulated_text="I predict my tempo will rush during the difficult leap transition."
    )

    # Run transcription handler
    msg = handle_transcribe_audio(
        job=job,
        config=test_config,
        repo=repo,
        file_store=file_store,
        transcriber=transcriber,
    )
    assert "Transcription completed" in msg

    # Verify derived artifacts exist
    artifacts = repo.list_artifacts_for_episode(ep.id)
    transcripts = [a for a in artifacts if a.artifact_type == "transcript"]
    assert len(transcripts) == 2  # 1 main transcript + 1 prediction voice transcript

    pred_transcript = next((t for t in transcripts if t.source_artifact_id == pred_art.id), None)
    assert pred_transcript is not None
    assert pred_transcript.is_raw is False

    # Verify episode prediction points to derived transcript
    updated_ep = repo.get_episode(ep.id)
    assert updated_ep.prediction.transcript_artifact_id == pred_transcript.id
    assert "rush" in updated_ep.prediction.prediction_text

    # Verify event logged
    events = repo.list_events_for_episode(ep.id)
    pred_completed_evts = [e for e in events if e.event_type == "prediction_transcription_completed"]
    assert len(pred_completed_evts) == 1
    ev_payload = json.loads(pred_completed_evts[0].payload_json)
    assert ev_payload["source_artifact_id"] == pred_art.id
    assert ev_payload["transcript_artifact_id"] == pred_transcript.id



