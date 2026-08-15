"""Tests for Slice 2B: Liquid Interaction, Inline Perturbation Responses, Ratings, and Local Heuristics."""

from __future__ import annotations

import io
import json
from pathlib import Path
import pytest
from let.config import Config
from let.db.connection import DatabaseManager
from let.db.repository import Repository
from let.liquid.heuristics import create_local_heuristic_analysis, generate_local_perturbations
from let.liquid.response_parser import import_analysis_response, parse_ai_response
from let.models.entities import AnalysisData, Episode, PerturbationItem
from let.storage.file_store import FileStore
from let.web.app import create_app


@pytest.fixture
def temp_env(tmp_path: Path):
    config = Config(data_dir=tmp_path / "let_test_data", whisper_model_size="tiny.en")
    config.ensure_directories()
    db_manager = DatabaseManager(config)
    repo = Repository(db_manager)
    file_store = FileStore(config)
    return config, repo, file_store, db_manager


@pytest.fixture
def app_client(temp_env):
    config, repo, file_store, db_manager = temp_env
    app = create_app(config, start_worker=False)
    app.config["TESTING"] = True
    return app.test_client(), repo, file_store, config


def test_local_heuristics_all_domains_and_modes(temp_env):
    """Test that all supported domains and modes generate non-empty, high-quality cognitive probes."""
    _, repo, _, _ = temp_env
    domains = ["movie", "piano", "cod", "research", "programming", "general"]
    modes = ["explore", "challenge", "understand", "improve", "surprise", "decide", "capture"]

    for d in domains:
        for m in modes:
            ep = Episode(id=f"ep_{d}_{m}", title=f"{d} {m}", domain=d, mode=m)
            items = generate_local_perturbations(ep)
            assert len(items) >= 2, f"Failed for domain {d} mode {m}"
            assert all(isinstance(item, PerturbationItem) for item in items)
            assert all(item.question_text.endswith("?") for item in items)

            analysis = create_local_heuristic_analysis(ep)
            assert isinstance(analysis, AnalysisData)
            assert len(analysis.items) == len(items)
            assert "Local Heuristic Engine" in analysis.provider


def test_legacy_analysis_data_normalization():
    """Test that AnalysisData without items gracefully normalizes perturbations."""
    legacy = AnalysisData(
        synthesis_text="Great summary",
        perturbations=["Is this working?", "What is next?"],
        provider="manual",
    )
    items = legacy.get_items()
    assert len(items) == 2
    assert items[0].id == "pert_1"
    assert items[0].question_text == "Is this working?"
    assert items[1].id == "pert_2"
    assert items[1].question_text == "What is next?"


def test_generate_local_questions_endpoint(app_client):
    """Test POST /api/episodes/<id>/generate_local_questions generates and stores derived artifact."""
    client, repo, file_store, config = app_client
    ep = Episode(id="ep_heur_1", title="Piano Sonata No. 14", domain="piano", mode="challenge")
    repo.create_episode(ep)

    res = client.post("/api/episodes/ep_heur_1/generate_local_questions")
    assert res.status_code == 201
    data = res.get_json()
    assert data["status"] == "success"
    assert data["artifact"]["artifact_type"] == "analysis"
    assert len(data["analysis"]["items"]) >= 2

    # Verify event logged
    events = repo.list_events_for_episode("ep_heur_1")
    assert any(e.event_type == "local_questions_generated" for e in events)


def test_rate_perturbation_endpoint(app_client):
    """Test 1-tap metacognitive rating on a perturbation."""
    client, repo, file_store, config = app_client
    ep = Episode(id="ep_rate_1", title="Film Reflection", domain="movie", mode="explore")
    repo.create_episode(ep)

    # Generate initial questions
    client.post("/api/episodes/ep_rate_1/generate_local_questions")
    art = repo.get_latest_analysis_for_episode("ep_rate_1")
    assert art is not None

    with open(file_store.to_absolute_path(art.file_path), "r", encoding="utf-8") as f:
        analysis_data = AnalysisData(**json.load(f))
    target_q_id = analysis_data.items[0].id

    # Rate as sharp
    res = client.post(
        f"/api/episodes/ep_rate_1/perturbations/{target_q_id}/rate",
        data={"rating": "sharp"},
    )
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data["rating"] == "sharp"

    # Verify updated on disk
    with open(file_store.to_absolute_path(art.file_path), "r", encoding="utf-8") as f:
        updated_data = AnalysisData(**json.load(f))
    assert updated_data.items[0].rating == "sharp"

    # Verify event
    events = repo.list_events_for_episode("ep_rate_1")
    assert any(e.event_type == "perturbation_rated" for e in events)


def test_answer_perturbation_with_text(app_client):
    """Test submitting a text note answer to a specific perturbation question."""
    client, repo, file_store, config = app_client
    ep = Episode(id="ep_ans_text", title="Research Insight", domain="research", mode="challenge")
    repo.create_episode(ep)

    client.post("/api/episodes/ep_ans_text/generate_local_questions")
    art = repo.get_latest_analysis_for_episode("ep_ans_text")

    with open(file_store.to_absolute_path(art.file_path), "r", encoding="utf-8") as f:
        analysis_data = AnalysisData(**json.load(f))
    target_q_id = analysis_data.items[0].id

    res = client.post(
        f"/api/episodes/ep_ans_text/perturbations/{target_q_id}/answer",
        data={"answer_text": "The discriminating test is measuring latency under load."},
    )
    assert res.status_code == 201
    res_data = res.get_json()
    assert res_data["item"]["answer_text"] == "The discriminating test is measuring latency under load."
    assert res_data["item"]["answered_at"] is not None

    # Verify event
    events = repo.list_events_for_episode("ep_ans_text")
    assert any(e.event_type == "perturbation_answered" for e in events)


def test_answer_perturbation_with_voice(app_client):
    """Test attaching a voice recording answer to a specific perturbation question with lineage."""
    client, repo, file_store, config = app_client
    ep = Episode(id="ep_ans_voice", title="COD Match Review", domain="cod", mode="improve")
    repo.create_episode(ep)

    client.post("/api/episodes/ep_ans_voice/generate_local_questions")
    art = repo.get_latest_analysis_for_episode("ep_ans_voice")

    with open(file_store.to_absolute_path(art.file_path), "r", encoding="utf-8") as f:
        analysis_data = AnalysisData(**json.load(f))
    target_q_id = analysis_data.items[0].id

    fake_audio = io.BytesIO(b"RIFF_FAKE_VOICE_ANSWER_AUDIO_DATA_BYTES")
    res = client.post(
        f"/api/episodes/ep_ans_voice/perturbations/{target_q_id}/answer",
        data={"audio": (fake_audio, "voice_ans.webm", "audio/webm")},
        content_type="multipart/form-data",
    )
    assert res.status_code == 201
    res_data = res.get_json()
    ans_art_id = res_data["item"]["answer_artifact_id"]
    assert ans_art_id is not None

    # Verify audio artifact exists and points to analysis as source
    ans_artifact = repo.get_artifact(ans_art_id)
    assert ans_artifact is not None
    assert ans_artifact.artifact_type == "audio"
    assert ans_artifact.is_raw is True
    assert ans_artifact.source_artifact_id == art.id

    # Verify event
    events = repo.list_events_for_episode("ep_ans_voice")
    assert any(e.event_type == "perturbation_answered" for e in events)


def test_generate_local_probes_preserves_existing_synthesis(app_client):
    """Test that generating local probes on an episode with a synthesis preserves that synthesis."""
    client, repo, file_store, config = app_client
    ep = Episode(id="ep_pres_synth", title="Pangram Note", domain="general", mode="capture")
    repo.create_episode(ep)

    # 1. Import a synthesis-only response
    raw_synth = "### Polished Synthesis\nRight now, Pangram is useful precisely because it creates friction."
    client.post(
        "/api/episodes/ep_pres_synth/import_analysis",
        data={"response_text": raw_synth, "provider": "ChatGPT Plus"},
    )

    # 2. Click Generate Local Probes
    res = client.post("/api/episodes/ep_pres_synth/generate_local_questions")
    assert res.status_code == 201
    data = res.get_json()

    # Verify synthesis is preserved AND questions are attached
    assert data["analysis"]["synthesis_text"] == "Right now, Pangram is useful precisely because it creates friction."
    assert data["analysis"]["provider"] == "ChatGPT Plus"
    assert len(data["analysis"]["items"]) >= 2


def test_import_questions_only_merges_with_existing_synthesis(app_client):
    """Test importing question-only text merges with existing synthesis."""
    client, repo, file_store, config = app_client
    ep = Episode(id="ep_merge_q", title="Film Thought", domain="movie", mode="explore")
    repo.create_episode(ep)

    # 1. Import synthesis
    client.post(
        "/api/episodes/ep_merge_q/import_analysis",
        data={"response_text": "### Polished Synthesis\nGreat film with vivid tone."},
    )

    # 2. Import question-only text
    raw_questions = "1. Did the friction lead to higher quality expression?\n2. What is the boundary?"
    res = client.post(
        "/api/episodes/ep_merge_q/import_analysis",
        data={"response_text": raw_questions, "provider": "ChatGPT Plus"},
    )
    assert res.status_code == 201
    data = res.get_json()

    # Verify synthesis is retained and 2 questions are added
    assert data["analysis"]["synthesis_text"] == "Great film with vivid tone."
    assert len(data["analysis"]["items"]) == 2
    assert "Did the friction lead to higher quality expression?" in data["analysis"]["items"][0]["question_text"]
