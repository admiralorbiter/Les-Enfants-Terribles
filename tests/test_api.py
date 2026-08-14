"""Tests for Flask HTTP routes, audio capture upload, and media streaming."""

from __future__ import annotations

import io
from pathlib import Path
from flask.testing import FlaskClient
from let.config import Config


def test_index_page(client: FlaskClient) -> None:
    res = client.get("/")
    assert res.status_code == 200
    assert b"Les Enfants Terribles" in res.data
    assert b"Click microphone to begin intentional capture" in res.data


def test_capture_audio_json(
    client: FlaskClient,
    test_config: Config,
    synthetic_audio_bytes: bytes,
) -> None:
    data = {
        "audio": (io.BytesIO(synthetic_audio_bytes), "spontaneous_thought.wav"),
        "title": "Novel Insight on Cognition",
        "domain": "research",
        "mode": "challenge",
    }
    res = client.post("/api/capture/audio", data=data, content_type="multipart/form-data")
    assert res.status_code == 201
    
    json_data = res.get_json()
    assert json_data["status"] == "success"
    assert json_data["episode"]["title"] == "Novel Insight on Cognition"
    assert json_data["episode"]["domain"] == "research"
    assert json_data["episode"]["mode"] == "challenge"
    
    artifact = json_data["artifact"]
    assert artifact["artifact_type"] == "audio"
    assert artifact["is_raw"] is True
    assert Path(artifact["file_path"]).exists()


def test_capture_audio_htmx(
    client: FlaskClient,
    synthetic_audio_bytes: bytes,
) -> None:
    data = {
        "audio": (io.BytesIO(synthetic_audio_bytes), "film_reaction.webm"),
        "title": "MGS2 Ending Reflection",
        "domain": "movie",
        "mode": "explore",
    }
    headers = {"HX-Request": "true"}
    res = client.post(
        "/api/capture/audio",
        data=data,
        content_type="multipart/form-data",
        headers=headers,
    )
    assert res.status_code == 200
    assert b"MGS2 Ending Reflection" in res.data
    assert b"RAW" in res.data
    assert b"controls" in res.data


def test_stream_media_and_detail(
    client: FlaskClient,
    synthetic_audio_bytes: bytes,
) -> None:
    # 1. Capture episode
    data = {
        "audio": (io.BytesIO(synthetic_audio_bytes), "test.wav"),
        "title": "Detail Stream Test",
        "domain": "programming",
    }
    capture_res = client.post("/api/capture/audio", data=data, content_type="multipart/form-data")
    assert capture_res.status_code == 201
    ep_id = capture_res.get_json()["episode"]["id"]
    art_id = capture_res.get_json()["artifact"]["id"]

    # 2. Detail view
    detail_res = client.get(f"/episodes/{ep_id}")
    assert detail_res.status_code == 200
    assert b"Detail Stream Test" in detail_res.data

    # 3. Stream media
    media_res = client.get(f"/media/{art_id}")
    assert media_res.status_code == 200
    assert media_res.data == synthetic_audio_bytes


def test_attach_followup_audio(
    client: FlaskClient,
    synthetic_audio_bytes: bytes,
) -> None:
    # 1. Capture initial
    data1 = {
        "audio": (io.BytesIO(synthetic_audio_bytes), "first.wav"),
        "title": "Multi-part Episode",
    }
    res1 = client.post("/api/capture/audio", data=data1, content_type="multipart/form-data")
    ep_id = res1.get_json()["episode"]["id"]

    # 2. Attach follow-up to same episode
    data2 = {
        "audio": (io.BytesIO(synthetic_audio_bytes), "followup.wav"),
        "episode_id": ep_id,
    }
    res2 = client.post("/api/capture/audio", data=data2, content_type="multipart/form-data")
    assert res2.status_code == 201
    assert res2.get_json()["episode"]["id"] == ep_id

    # 3. Detail view should now have 2 artifacts
    detail_res = client.get(f"/episodes/{ep_id}")
    assert detail_res.status_code == 200
    assert b"All Artifacts (2)" in detail_res.data


def test_add_mark_event(
    client: FlaskClient,
    synthetic_audio_bytes: bytes,
) -> None:
    # Create episode
    data = {"audio": (io.BytesIO(synthetic_audio_bytes), "test.wav")}
    res = client.post("/api/capture/audio", data=data, content_type="multipart/form-data")
    ep_id = res.get_json()["episode"]["id"]

    # Add MARK event
    mark_res = client.post(
        f"/api/episodes/{ep_id}/mark",
        json={"note": "Surprise ending realization", "timestamp_sec": 12.4},
    )
    assert mark_res.status_code == 201
    assert mark_res.get_json()["event"]["event_type"] == "mark"
