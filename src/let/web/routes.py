"""HTTP routes and API endpoints for LET."""

from __future__ import annotations

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
from let.liquid.response_parser import import_analysis_response
from let.models.entities import (
    AnalysisData,
    Artifact,
    Episode,
    Event,
    Job,
    TranscriptData,
)

bp = Blueprint("main", __name__)


def _get_repo():
    return current_app.extensions["let_repo"]


def _get_store():
    return current_app.extensions["let_store"]


def _get_config():
    return current_app.extensions["let_config"]


def _load_transcript_data(artifact: Artifact) -> TranscriptData | None:
    """Helper to read and parse derived transcript JSON file."""
    try:
        path = Path(artifact.file_path)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return TranscriptData(**data)
    except Exception:
        pass
    return None


def _load_analysis_data(artifact: Artifact) -> AnalysisData | None:
    """Helper to read and parse derived analysis JSON file."""
    try:
        path = Path(artifact.file_path)
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
    """Generate and return structured Mission Brief Markdown text."""
    repo = _get_repo()
    episode = repo.get_episode(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    latest_transcript_art = repo.get_latest_transcript_for_episode(episode_id)
    transcript_data = (
        _load_transcript_data(latest_transcript_art)
        if latest_transcript_art
        else None
    )

    brief_text = generate_mission_brief(
        episode=episode,
        transcript=transcript_data,
    )

    if request.args.get("format") == "json":
        return jsonify(
            {
                "episode_id": episode.id,
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

    raw_response = request.form.get("response_text", "").strip()
    if not raw_response:
        data = request.get_json(silent=True) or {}
        raw_response = data.get("response_text", "").strip()

    if not raw_response:
        return jsonify({"error": "No response text provided"}), 400

    provider = (
        request.form.get("provider", "manual").strip()
        or request.get_json(silent=True, default={}).get("provider", "manual")
    )

    # Link back to latest transcript as source artifact
    latest_transcript = repo.get_latest_transcript_for_episode(episode_id)
    source_artifact_id = latest_transcript.id if latest_transcript else None

    # Persist derived analysis artifact
    artifact, analysis_data = import_analysis_response(
        raw_response=raw_response,
        provider=provider,
        episode_id=episode_id,
        source_artifact_id=source_artifact_id,
        config=config,
        repo=repo,
        file_store=file_store,
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


@bp.route("/api/episodes/<episode_id>/update_title", methods=["POST"])
def update_title(episode_id: str):
    """In-place episode title rename endpoint."""
    repo = _get_repo()
    episode = repo.get_episode(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    new_title = request.form.get("title", "").strip()
    if not new_title:
        data = request.get_json(silent=True) or {}
        new_title = data.get("title", "").strip()

    if new_title:
        episode.title = new_title
        repo.update_episode(episode)

    if request.headers.get("HX-Request"):
        return f'<a href="/episodes/{episode.id}" class="episode-title-link">{episode.title}</a>'

    return jsonify({"status": "success", "episode": episode.model_dump()})


@bp.route("/api/capture/audio", methods=["POST"])
def capture_audio():
    """Atomic raw audio ingestion endpoint with automatic background transcribe enqueue."""
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

    # Determine or create episode
    is_new_episode = False
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
        repo.create_episode(episode)

    # Atomically save raw audio to immutable store
    stored = file_store.save_raw_audio(
        data=audio_file.stream,
        original_filename=audio_file.filename,
        episode_id=episode_id,
    )

    # Determine mime type
    mime_type = audio_file.content_type or "audio/webm"

    # Create raw artifact record
    artifact_id = f"art_{uuid.uuid4().hex[:12]}"
    artifact = Artifact(
        id=artifact_id,
        episode_id=episode_id,
        artifact_type="audio",
        is_raw=True,
        file_path=str(stored.file_path),
        file_hash=stored.file_hash,
        mime_type=mime_type,
        size_bytes=stored.size_bytes,
    )
    repo.create_artifact(artifact)

    # Log capture event
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
    repo.create_event(event)

    # Automatically enqueue background transcription job
    job_id = f"job_{uuid.uuid4().hex[:12]}"
    job = Job(
        id=job_id,
        job_type="transcribe_audio",
        episode_id=episode_id,
        artifact_id=artifact_id,
        status="queued",
    )
    repo.create_job(job)

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

    target_audio = audio_artifacts[-1]  # Latest audio artifact
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
    """Secure range-request streaming for audio/video artifacts."""
    repo = _get_repo()
    artifact = repo.get_artifact(artifact_id)
    if not artifact:
        abort(404, description="Artifact not found")

    file_path = Path(artifact.file_path)
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
