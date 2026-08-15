"""HTTP routes and API endpoints for LET."""

from __future__ import annotations

import html
import json
import uuid
from pathlib import Path
from flask import (
    Blueprint,
    abort,
    current_app,
    jsonify,
    render_template,
    request,
    Response,
    send_file,
)
from let.liquid.brief_generator import generate_mission_brief
from let.liquid.heuristics import create_local_heuristic_analysis
from let.liquid.response_parser import import_analysis_response
from let.models.entities import (
    AnalysisData,
    Artifact,
    Episode,
    Event,
    Job,
    TranscriptData,
    utc_now_iso,
)

bp = Blueprint("main", __name__)


def _get_repo():
    return current_app.extensions["let_repo"]


def _get_store():
    return current_app.extensions["let_store"]


def _get_config():
    return current_app.extensions["let_config"]


def _load_transcript_data(artifact: Artifact) -> TranscriptData | None:
    """Helper to read and parse derived transcript JSON file using relative path resolution."""
    try:
        file_store = _get_store()
        path = file_store.to_absolute_path(artifact.file_path)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return TranscriptData(**data)
    except Exception:
        pass
    return None


def _load_analysis_data(artifact: Artifact) -> AnalysisData | None:
    """Helper to read and parse derived analysis JSON file using relative path resolution."""
    try:
        file_store = _get_store()
        path = file_store.to_absolute_path(artifact.file_path)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return AnalysisData(**data)
    except Exception:
        pass
    return None


@bp.route("/")
def index():
    """Main capture station and episode feed."""
    repo = _get_repo()
    domain_filter = request.args.get("domain")
    episodes = repo.list_episodes(limit=30, domain=domain_filter)

    episodes_with_data = []
    for ep in episodes:
        artifacts = repo.list_artifacts_for_episode(ep.id)
        latest_transcript_art = repo.get_latest_transcript_for_episode(ep.id)
        transcript_data = (
            _load_transcript_data(latest_transcript_art)
            if latest_transcript_art
            else None
        )
        latest_analysis_art = repo.get_latest_analysis_for_episode(ep.id)
        analysis_data = (
            _load_analysis_data(latest_analysis_art)
            if latest_analysis_art
            else None
        )
        jobs = repo.list_jobs_for_episode(ep.id)
        latest_job = jobs[0] if jobs else None

        episodes_with_data.append(
            {
                "episode": ep,
                "artifacts": artifacts,
                "transcript_art": latest_transcript_art,
                "transcript_data": transcript_data,
                "analysis_art": latest_analysis_art,
                "analysis_data": analysis_data,
                "latest_job": latest_job,
            }
        )

    return render_template(
        "index.html",
        episodes_with_data=episodes_with_data,
        current_domain=domain_filter or "",
    )


@bp.route("/episodes/<episode_id>")
def episode_detail(episode_id: str):
    """Detailed episode view with artifact lineage, transcript segments, analysis, and events."""
    repo = _get_repo()
    episode = repo.get_episode(episode_id)
    if not episode:
        abort(404, description="Episode not found")

    artifacts = repo.list_artifacts_for_episode(episode_id)
    events = repo.list_events_for_episode(episode_id)
    jobs = repo.list_jobs_for_episode(episode_id)
    latest_job = jobs[0] if jobs else None

    latest_transcript_art = repo.get_latest_transcript_for_episode(episode_id)
    transcript_data = (
        _load_transcript_data(latest_transcript_art)
        if latest_transcript_art
        else None
    )

    latest_analysis_art = repo.get_latest_analysis_for_episode(episode_id)
    analysis_data = (
        _load_analysis_data(latest_analysis_art)
        if latest_analysis_art
        else None
    )

    return render_template(
        "episode_detail.html",
        episode=episode,
        artifacts=artifacts,
        events=events,
        transcript_art=latest_transcript_art,
        transcript_data=transcript_data,
        analysis_art=latest_analysis_art,
        analysis_data=analysis_data,
        latest_job=latest_job,
    )


@bp.route("/episodes/<episode_id>/transcript")
def get_transcript_partial(episode_id: str):
    """HTMX endpoint returning transcript status or rendered segments."""
    repo = _get_repo()
    episode = repo.get_episode(episode_id)
    if not episode:
        return "Episode not found", 404

    latest_transcript_art = repo.get_latest_transcript_for_episode(episode_id)
    transcript_data = (
        _load_transcript_data(latest_transcript_art)
        if latest_transcript_art
        else None
    )
    jobs = repo.list_jobs_for_episode(episode_id)
    latest_job = jobs[0] if jobs else None

    return render_template(
        "partials/transcript_view.html",
        episode=episode,
        transcript_art=latest_transcript_art,
        transcript_data=transcript_data,
        latest_job=latest_job,
    )


@bp.route("/episodes/<episode_id>/brief")
def get_mission_brief(episode_id: str):
    """Generate, persist, and return structured Mission Brief Markdown packet."""
    repo = _get_repo()
    file_store = _get_store()
    episode = repo.get_episode(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    artifacts = repo.list_artifacts_for_episode(episode_id)
    audio_artifacts = [a for a in artifacts if a.artifact_type == "audio"]
    latest_audio = audio_artifacts[-1] if audio_artifacts else None
    latest_transcript_art = repo.get_latest_transcript_for_episode(episode_id)
    transcript_data = (
        _load_transcript_data(latest_transcript_art)
        if latest_transcript_art
        else None
    )

    brief_text = generate_mission_brief(
        episode=episode,
        transcript=transcript_data,
        transcript_artifact=latest_transcript_art,
        audio_artifact=latest_audio,
    )

    brief_bytes = brief_text.encode("utf-8")
    brief_hash = file_store.compute_hash_bytes(brief_bytes)
    target_filename = f"brief_{episode_id}_{brief_hash[:16]}.md"
    rel_subpath = Path("derived") / "analyses" / target_filename
    stored = file_store.save_derived_artifact(brief_bytes, rel_subpath)

    brief_artifact_id = f"art_br_{uuid.uuid4().hex[:12]}"
    brief_art = Artifact(
        id=brief_artifact_id,
        episode_id=episode_id,
        artifact_type="mission_brief",
        is_raw=False,
        file_path=stored.relative_path,
        file_hash=brief_hash,
        mime_type="text/markdown",
        size_bytes=stored.size_bytes,
        source_artifact_id=latest_transcript_art.id if latest_transcript_art else None,
        processor_name="mission_brief_generator",
        processor_version="v1.0",
    )
    repo.create_artifact(brief_art)

    repo.create_event(
        Event(
            id=f"evt_{uuid.uuid4().hex[:12]}",
            episode_id=episode_id,
            event_type="mission_brief_exported",
            payload_json=json.dumps(
                {
                    "brief_artifact_id": brief_artifact_id,
                    "brief_hash": brief_hash,
                }
            ),
        )
    )

    if request.args.get("format") == "json":
        return jsonify(
            {
                "episode_id": episode.id,
                "brief_artifact_id": brief_artifact_id,
                "brief_markdown": brief_text,
            }
        )

    return Response(brief_text, mimetype="text/markdown")


@bp.route("/api/episodes/<episode_id>/import_analysis", methods=["POST"])
def import_analysis(episode_id: str):
    """Ingest external AI Mission Brief response and save derived artifact."""
    repo = _get_repo()
    config = _get_config()
    file_store = _get_store()

    episode = repo.get_episode(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    payload = request.get_json(silent=True) or {}
    raw_response = request.form.get("response_text", "").strip() or payload.get("response_text", "").strip()
    if not raw_response:
        return jsonify({"error": "No response text provided"}), 400

    provider = (
        request.form.get("provider")
        or payload.get("provider")
        or "manual"
    ).strip()

    artifacts = repo.list_artifacts_for_episode(episode_id)
    brief_artifacts = [a for a in artifacts if a.artifact_type == "mission_brief"]
    latest_transcript = repo.get_latest_transcript_for_episode(episode_id)
    latest_analysis = repo.get_latest_analysis_for_episode(episode_id)
    existing_analysis_data = _load_analysis_data(latest_analysis) if latest_analysis else None

    source_artifact_id = (
        brief_artifacts[-1].id
        if brief_artifacts
        else (latest_transcript.id if latest_transcript else None)
    )

    artifact, analysis_data = import_analysis_response(
        raw_response=raw_response,
        provider=provider,
        episode_id=episode_id,
        source_artifact_id=source_artifact_id,
        config=config,
        repo=repo,
        file_store=file_store,
        existing_analysis=existing_analysis_data,
    )

    if request.headers.get("HX-Request"):
        return render_template(
            "partials/analysis_view.html",
            episode=episode,
            analysis_art=artifact,
            analysis_data=analysis_data,
        )

    return (
        jsonify(
            {
                "status": "success",
                "artifact": artifact.model_dump(),
                "analysis": analysis_data.model_dump(),
            }
        ),
        201,
    )


@bp.route("/api/episodes/<episode_id>/generate_local_questions", methods=["POST"])
def generate_local_questions(episode_id: str):
    """Generate instant offline cognitive questions using local domain heuristics."""
    repo = _get_repo()
    config = _get_config()
    file_store = _get_store()

    episode = repo.get_episode(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    latest_transcript_art = repo.get_latest_transcript_for_episode(episode_id)
    transcript_data = _load_transcript_data(latest_transcript_art) if latest_transcript_art else None
    transcript_text = transcript_data.text if transcript_data else ""

    latest_analysis_art = repo.get_latest_analysis_for_episode(episode_id)
    existing_analysis = _load_analysis_data(latest_analysis_art) if latest_analysis_art else None

    analysis_data = create_local_heuristic_analysis(episode, transcript_text)
    if existing_analysis and existing_analysis.synthesis_text:
        analysis_data.synthesis_text = existing_analysis.synthesis_text
        if existing_analysis.provider and existing_analysis.provider != "Local Heuristic Engine":
            analysis_data.provider = existing_analysis.provider

    json_bytes = analysis_data.model_dump_json(indent=2).encode("utf-8")
    analysis_hash = file_store.compute_hash_bytes(json_bytes)

    target_filename = f"analysis_local_{episode_id}_{analysis_hash[:16]}.json"
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
        source_artifact_id=latest_transcript_art.id if latest_transcript_art else None,
        processor_name="local_heuristic_engine",
        processor_version="v1.0",
    )
    repo.create_artifact(artifact)

    repo.create_event(
        Event(
            id=f"evt_{uuid.uuid4().hex[:12]}",
            episode_id=episode_id,
            event_type="local_questions_generated",
            payload_json=json.dumps({"artifact_id": artifact_id, "questions_count": len(analysis_data.items)}),
        )
    )

    if request.headers.get("HX-Request"):
        return render_template(
            "partials/analysis_view.html",
            episode=episode,
            analysis_art=artifact,
            analysis_data=analysis_data,
        )

    return jsonify({"status": "success", "artifact": artifact.model_dump(), "analysis": analysis_data.model_dump()}), 201


@bp.route("/api/episodes/<episode_id>/perturbations/<question_id>/rate", methods=["POST"])
def rate_perturbation(episode_id: str, question_id: str):
    """Save 1-tap rating (sharp, already_knew, irrelevant) on a specific perturbation question."""
    repo = _get_repo()
    config = _get_config()
    file_store = _get_store()

    episode = repo.get_episode(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    payload = request.get_json(silent=True) or {}
    rating = (
        request.args.get("rating", "").strip()
        or request.form.get("rating", "").strip()
        or payload.get("rating", "").strip()
    )
    if not rating:
        return jsonify({"error": "No rating specified"}), 400

    latest_analysis_art = repo.get_latest_analysis_for_episode(episode_id)
    if not latest_analysis_art:
        return jsonify({"error": "No analysis found for episode"}), 404

    analysis_data = _load_analysis_data(latest_analysis_art)
    if not analysis_data:
        return jsonify({"error": "Could not read analysis data"}), 500

    items = analysis_data.get_items()
    target_item = None
    for idx, item in enumerate(items):
        if (
            item.id == question_id
            or (question_id.isdigit() and int(question_id) == idx + 1)
            or question_id == f"pert_{idx + 1}"
            or item.id.startswith(f"{question_id}_")
            or question_id.startswith(f"{item.id}_")
            or (question_id.startswith("pert_") and len(question_id.split("_")) > 1 and question_id.split("_")[1] == str(idx + 1))
        ):
            # Toggle rating if clicked twice
            if item.rating == rating:
                item.rating = None
            else:
                item.rating = rating
            target_item = item
            break

    if not target_item:
        return jsonify({"error": f"Question {question_id} not found"}), 404

    analysis_data.items = items
    json_bytes = analysis_data.model_dump_json(indent=2).encode("utf-8")
    rel_path = file_store.to_relative_path(latest_analysis_art.file_path)
    file_store.save_derived_artifact(json_bytes, Path(rel_path))

    repo.create_event(
        Event(
            id=f"evt_{uuid.uuid4().hex[:12]}",
            episode_id=episode_id,
            event_type="perturbation_rated",
            payload_json=json.dumps({"question_id": question_id, "rating": rating}),
        )
    )

    if request.headers.get("HX-Request"):
        return render_template(
            "partials/analysis_view.html",
            episode=episode,
            analysis_art=latest_analysis_art,
            analysis_data=analysis_data,
        )

    return jsonify({"status": "success", "question_id": question_id, "rating": rating})


@bp.route("/api/episodes/<episode_id>/perturbations/<question_id>/answer", methods=["POST"])
def answer_perturbation(episode_id: str, question_id: str):
    """Attach an inline voice recording or typed text note answer to a specific perturbation."""
    repo = _get_repo()
    config = _get_config()
    file_store = _get_store()

    episode = repo.get_episode(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    latest_analysis_art = repo.get_latest_analysis_for_episode(episode_id)
    if not latest_analysis_art:
        return jsonify({"error": "No analysis found for episode"}), 404

    analysis_data = _load_analysis_data(latest_analysis_art)
    if not analysis_data:
        return jsonify({"error": "Could not read analysis data"}), 500

    items = analysis_data.get_items()
    target_item = None
    for idx, item in enumerate(items):
        if (
            item.id == question_id
            or (question_id.isdigit() and int(question_id) == idx + 1)
            or question_id == f"pert_{idx + 1}"
            or item.id.startswith(f"{question_id}_")
            or question_id.startswith(f"{item.id}_")
            or (question_id.startswith("pert_") and len(question_id.split("_")) > 1 and question_id.split("_")[1] == str(idx + 1))
        ):
            target_item = item
            break

    if not target_item:
        return jsonify({"error": f"Question {question_id} not found"}), 404

    answer_art_id = None
    answer_text = None

    if "audio" in request.files:
        audio_file = request.files["audio"]
        if not audio_file.filename:
            audio_file.filename = "answer.webm"

        stored = file_store.save_raw_audio(
            data=audio_file.stream,
            original_filename=audio_file.filename,
            episode_id=episode_id,
        )
        answer_art_id = f"art_{uuid.uuid4().hex[:12]}"
        answer_art = Artifact(
            id=answer_art_id,
            episode_id=episode_id,
            artifact_type="audio",
            is_raw=True,
            file_path=stored.relative_path,
            file_hash=stored.file_hash,
            mime_type=audio_file.content_type or "audio/webm",
            size_bytes=stored.size_bytes,
            source_artifact_id=latest_analysis_art.id,
            processor_name="perturbation_voice_response",
            processor_version="v1.0",
        )
        repo.create_artifact(answer_art)
        target_item.answer_artifact_id = answer_art_id
        target_item.answered_at = utc_now_iso()

    else:
        payload = request.get_json(silent=True) or {}
        answer_text = request.form.get("answer_text", "").strip() or payload.get("answer_text", "").strip()
        if not answer_text:
            return jsonify({"error": "No audio or text answer provided"}), 400
        target_item.answer_text = answer_text
        target_item.answered_at = utc_now_iso()

    analysis_data.items = items
    json_bytes = analysis_data.model_dump_json(indent=2).encode("utf-8")
    rel_path = file_store.to_relative_path(latest_analysis_art.file_path)
    file_store.save_derived_artifact(json_bytes, Path(rel_path))

    repo.create_event(
        Event(
            id=f"evt_{uuid.uuid4().hex[:12]}",
            episode_id=episode_id,
            event_type="perturbation_answered",
            payload_json=json.dumps(
                {
                    "question_id": question_id,
                    "answer_artifact_id": answer_art_id,
                    "has_text": bool(answer_text),
                }
            ),
        )
    )

    if request.headers.get("HX-Request"):
        return render_template(
            "partials/analysis_view.html",
            episode=episode,
            analysis_art=latest_analysis_art,
            analysis_data=analysis_data,
        )

    return jsonify({"status": "success", "question_id": question_id, "item": target_item.model_dump()}), 201


@bp.route("/api/episodes/<episode_id>/update_title", methods=["POST"])
def update_title(episode_id: str):
    """In-place episode title rename endpoint with HTML escaping."""
    repo = _get_repo()
    episode = repo.get_episode(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    payload = request.get_json(silent=True) or {}
    new_title = request.form.get("title", "").strip() or payload.get("title", "").strip()

    if new_title:
        episode.title = new_title
        repo.update_episode(episode)

    if request.headers.get("HX-Request"):
        safe_title = html.escape(episode.title)
        return f'<a href="/episodes/{episode.id}" class="episode-title-link">{safe_title}</a>'

    return jsonify({"status": "success", "episode": episode.model_dump()})


@bp.route("/api/capture/audio", methods=["POST"])
def capture_audio():
    """Atomic raw audio ingestion endpoint with single-transaction persistence and disk receipts."""
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    if not audio_file.filename:
        audio_file.filename = "recording.webm"

    title = request.form.get("title", "").strip()
    domain = request.form.get("domain", "general").strip() or "general"
    mode = request.form.get("mode", "capture").strip() or "capture"
    episode_id = request.form.get("episode_id", "").strip()

    repo = _get_repo()
    file_store = _get_store()

    # 1. Determine episode
    is_new_episode = False
    episode = None
    if episode_id:
        episode = repo.get_episode(episode_id)
        if not episode:
            return jsonify({"error": f"Episode {episode_id} not found"}), 404
    else:
        is_new_episode = True
        episode_id = f"ep_{uuid.uuid4().hex[:12]}"
        if not title:
            domain_label = domain.capitalize() if domain != "general" else "Thought"
            title = f"{domain_label} Reflection"
        episode = Episode(
            id=episode_id,
            title=title,
            domain=domain,
            mode=mode,
        )

    # 2. Atomically save raw audio to immutable store FIRST
    stored = file_store.save_raw_audio(
        data=audio_file.stream,
        original_filename=audio_file.filename,
        episode_id=episode_id,
    )

    mime_type = audio_file.content_type or "audio/webm"
    artifact_id = f"art_{uuid.uuid4().hex[:12]}"
    artifact = Artifact(
        id=artifact_id,
        episode_id=episode_id,
        artifact_type="audio",
        is_raw=True,
        file_path=stored.relative_path,
        file_hash=stored.file_hash,
        mime_type=mime_type,
        size_bytes=stored.size_bytes,
    )

    event = Event(
        id=f"evt_{uuid.uuid4().hex[:12]}",
        episode_id=episode_id,
        event_type="capture_saved",
        payload_json=json.dumps(
            {
                "artifact_id": artifact_id,
                "file_hash": stored.file_hash,
                "size_bytes": stored.size_bytes,
                "is_new_episode": is_new_episode,
            }
        ),
    )

    job_id = f"job_{uuid.uuid4().hex[:12]}"
    job = Job(
        id=job_id,
        job_type="transcribe_audio",
        episode_id=episode_id,
        artifact_id=artifact_id,
        status="queued",
    )

    # 3. Commit entire capture bundle in a SINGLE atomic database transaction
    try:
        repo.create_capture_bundle(
            artifact=artifact,
            event=event,
            episode=episode if is_new_episode else None,
            job=job,
        )
    except Exception as exc:
        file_store.write_capture_receipt(
            relative_file_path=stored.relative_path,
            episode_id=episode_id,
            metadata={
                "title": title or "Recovered Capture",
                "domain": domain,
                "mode": mode,
                "artifact_id": artifact_id,
                "file_hash": stored.file_hash,
                "mime_type": mime_type,
                "size_bytes": stored.size_bytes,
                "error": str(exc),
            },
        )
        return jsonify({"error": f"Database commit failed, recovery receipt saved: {exc}"}), 500

    # Return HTMX partial or JSON
    if request.headers.get("HX-Request"):
        artifacts = repo.list_artifacts_for_episode(episode_id)
        return render_template(
            "partials/episode_card.html",
            item={
                "episode": episode,
                "artifacts": artifacts,
                "transcript_art": None,
                "transcript_data": None,
                "analysis_art": None,
                "analysis_data": None,
                "latest_job": job,
            },
        )

    return (
        jsonify(
            {
                "status": "success",
                "episode": episode.model_dump(),
                "artifact": artifact.model_dump(),
                "job": job.model_dump(),
            }
        ),
        201,
    )


@bp.route("/api/episodes/<episode_id>/transcribe", methods=["POST"])
def retranscribe_episode(episode_id: str):
    """Manual replay / re-transcription endpoint."""
    repo = _get_repo()
    episode = repo.get_episode(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    artifacts = repo.list_artifacts_for_episode(episode_id)
    audio_artifacts = [a for a in artifacts if a.artifact_type == "audio"]
    if not audio_artifacts:
        return jsonify({"error": "No audio artifact to transcribe"}), 400

    target_audio = audio_artifacts[-1]
    job_id = f"job_{uuid.uuid4().hex[:12]}"
    job = Job(
        id=job_id,
        job_type="transcribe_audio",
        episode_id=episode_id,
        artifact_id=target_audio.id,
        status="queued",
    )
    repo.create_job(job)

    if request.headers.get("HX-Request"):
        return render_template(
            "partials/transcript_view.html",
            episode=episode,
            transcript_art=None,
            transcript_data=None,
            latest_job=job,
        )

    return jsonify({"status": "queued", "job": job.model_dump()}), 201


@bp.route("/media/<artifact_id>")
def stream_media(artifact_id: str):
    """Secure range-request streaming for audio/video artifacts using relative path resolution."""
    repo = _get_repo()
    file_store = _get_store()
    artifact = repo.get_artifact(artifact_id)
    if not artifact:
        abort(404, description="Artifact not found")

    file_path = file_store.to_absolute_path(artifact.file_path)
    if not file_path.exists():
        abort(404, description="Raw media file missing from disk store")

    return send_file(
        str(file_path),
        mimetype=artifact.mime_type,
        conditional=True,
        as_attachment=False,
    )


@bp.route("/api/episodes/<episode_id>/mark", methods=["POST"])
def add_mark_event(episode_id: str):
    """Add a timestamped MARK event to an episode."""
    repo = _get_repo()
    episode = repo.get_episode(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    data = request.get_json(silent=True) or request.form
    note = data.get("note", "Manual MARK").strip()
    timestamp_sec = data.get("timestamp_sec", None)

    event = Event(
        id=f"evt_{uuid.uuid4().hex[:12]}",
        episode_id=episode_id,
        event_type="mark",
        payload_json=json.dumps({"note": note, "timestamp_sec": timestamp_sec}),
    )
    repo.create_event(event)

    return jsonify({"status": "success", "event": event.model_dump()}), 201
