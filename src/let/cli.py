"""Command-line interface and diagnostic doctor for LET."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path
from let.config import get_config
from let.db.connection import DatabaseManager
from let.db.repository import Repository
from let.jobs.worker import JobWorker
from let.models.entities import Job
from let.storage.file_store import FileStore
from let.transcription.faster_whisper_engine import FasterWhisperTranscriber
from let.web.app import create_app


def run_server(args: argparse.Namespace) -> None:
    """Launch local LET web server."""
    config = get_config(data_dir_override=args.data_dir)
    app = create_app(config, start_worker=not args.no_worker)

    port = args.port or config.port
    host = args.host or config.host
    debug = args.debug or config.debug

    print(f"\n=======================================================")
    print(f" Les Enfants Terribles (LET) — Capture & Audio Substrate")
    print(f" Local Data Root  : {config.data_dir}")
    print(f" SQLite Database   : {config.db_path}")
    print(f" Whisper Model     : {config.whisper_model_size} ({config.whisper_device})")
    print(f" Server URL        : http://{host}:{port}")
    print(f" Background Worker : {'Enabled' if not args.no_worker else 'Disabled'}")
    print(f"=======================================================\n")

    app.run(host=host, port=port, debug=debug)


def run_worker(args: argparse.Namespace) -> None:
    """Run standalone background worker process."""
    config = get_config(data_dir_override=args.data_dir)
    db = DatabaseManager(config)
    repo = Repository(db)
    file_store = FileStore(config)

    worker = JobWorker(config=config, repo=repo, file_store=file_store)
    print(f"\n--- LET Background Worker [{worker.worker_id}] ---")
    print(f"Data Root     : {config.data_dir}")
    print(f"Whisper Model : {config.whisper_model_size} ({config.whisper_device})")
    print("Listening for queued jobs... Press Ctrl+C to exit.\n")
    try:
        worker.run_loop(poll_interval=args.interval)
    except KeyboardInterrupt:
        print("\nWorker stopped cleanly.")


def run_transcribe(args: argparse.Namespace) -> None:
    """Trigger manual transcription for an episode from the CLI."""
    config = get_config(data_dir_override=args.data_dir)
    db = DatabaseManager(config)
    repo = Repository(db)
    file_store = FileStore(config)

    episode = repo.get_episode(args.episode_id)
    if not episode:
        print(f"Error: Episode {args.episode_id} not found.")
        sys.exit(1)

    artifacts = repo.list_artifacts_for_episode(args.episode_id)
    audio_artifacts = [a for a in artifacts if a.artifact_type == "audio"]
    if not audio_artifacts:
        print(f"Error: No audio artifact found in episode {args.episode_id}.")
        sys.exit(1)

    target_audio = audio_artifacts[-1]
    model_size = args.model or config.whisper_model_size
    transcriber = FasterWhisperTranscriber(
        model_size=model_size,
        device=config.whisper_device,
        compute_type=config.whisper_compute_type,
    )

    print(f"Transcribing episode '{episode.title}' ({target_audio.id}) using {transcriber.name} ({model_size})...")
    
    import uuid
    job = Job(
        id=f"job_cli_{uuid.uuid4().hex[:8]}",
        job_type="transcribe_audio",
        episode_id=episode.id,
        artifact_id=target_audio.id,
        status="queued",
    )
    repo.create_job(job)

    worker = JobWorker(config, repo, file_store, transcriber=transcriber)
    worker.run_once()

    latest_tr = repo.get_latest_transcript_for_episode(episode.id)
    if latest_tr:
        print(f"[OK] Transcription complete. Artifact: {latest_tr.id} (SHA-256: {latest_tr.file_hash[:16]}...)")
    else:
        print("[FAIL] Transcription failed to produce artifact.")


def run_doctor(args: argparse.Namespace) -> None:
    """Run diagnostic checks on storage, database, speech tools, and artifact integrity."""
    config = get_config(data_dir_override=args.data_dir)
    print("\n--- LET System Doctor ---")
    print(f"Data Root: {config.data_dir}")

    # 1. Directory Checks
    print("\n[1/5] Checking filesystem directories...")
    dirs = [
        config.data_dir,
        config.raw_audio_dir,
        config.raw_text_dir,
        config.raw_video_dir,
        config.derived_transcripts_dir,
        config.derived_analyses_dir,
        config.backups_dir,
        config.temp_dir,
    ]
    all_dirs_ok = True
    for d in dirs:
        if d.exists() and os.access(d, os.W_OK):
            rel = d.relative_to(config.data_dir) if d != config.data_dir else '.'
            print(f"  [OK] {rel}")
        else:
            print(f"  [FAIL] {d} (missing or not writable)")
            all_dirs_ok = False

    # 2. Database Checks
    print("\n[2/5] Checking SQLite database...")
    db_ok = False
    try:
        db = DatabaseManager(config)
        with db.transaction() as conn:
            integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
            if integrity == "ok":
                print(f"  [OK] Database integrity: {integrity}")
                db_ok = True
            else:
                print(f"  [FAIL] Integrity error: {integrity}")
    except Exception as e:
        print(f"  [FAIL] Database connection error: {e}")

    # 3. Audio & Transcription Tool Checks
    print("\n[3/5] Checking transcription runtime dependencies...")
    ffmpeg_path = shutil.which("ffmpeg")
    ffmpeg_ok = bool(ffmpeg_path)
    if ffmpeg_ok:
        print(f"  [OK] FFmpeg found: {ffmpeg_path}")
    else:
        print("  [FAIL] FFmpeg not found on PATH! Audio decoding may fail.")

    whisper_ok = False
    try:
        import faster_whisper
        print(f"  [OK] faster-whisper package available (version {faster_whisper.__version__})")
        whisper_ok = True
    except Exception as e:
        print(f"  [FAIL] faster-whisper import error: {e}")

    # 4. Artifact Cryptographic Hash Verification
    print("\n[4/5] Verifying artifact hashes against disk...")
    store = FileStore(config)
    repo = Repository(db) if db_ok else None

    artifacts_ok = True
    if repo:
        artifacts = repo.list_all_artifacts()
        print(f"  Found {len(artifacts)} registered artifact(s).")
        for art in artifacts:
            path = Path(art.file_path)
            if not path.exists():
                print(f"  [FAIL] Artifact {art.id}: File missing at {path}")
                artifacts_ok = False
                continue

            disk_hash = store.compute_hash_file(path)
            if disk_hash == art.file_hash:
                badge = "RAW" if art.is_raw else "DERIVED"
                print(f"  [OK] Artifact {art.id} [{badge}] ({art.artifact_type}): SHA-256 verified ({art.size_bytes} bytes)")
            else:
                print(f"  [FAIL] Artifact {art.id}: HASH MISMATCH! DB={art.file_hash} Disk={disk_hash}")
                artifacts_ok = False

    # 5. Summary
    print("\n[5/5] Summary Result:")
    all_ok = all_dirs_ok and db_ok and ffmpeg_ok and whisper_ok and artifacts_ok
    if all_ok:
        print("  [OK] ALL SYSTEMS HEALTHY. Trustworthy capture and transcription satisfied.\n")
    else:
        print("  [FAIL] ISSUES DETECTED. Please review the warnings above.\n")
        sys.exit(1)


def run_status(args: argparse.Namespace) -> None:
    """Print high-level statistics about stored episodes, transcripts, and storage footprint."""
    config = get_config(data_dir_override=args.data_dir)
    db = DatabaseManager(config)
    repo = Repository(db)

    episodes = repo.list_episodes(limit=1000)
    artifacts = repo.list_all_artifacts()
    jobs = repo.list_jobs(limit=1000) if hasattr(repo, "list_jobs") else []

    total_bytes = sum(art.size_bytes for art in artifacts)
    raw_audio_count = sum(1 for art in artifacts if art.artifact_type == "audio" and art.is_raw)
    transcripts_count = sum(1 for art in artifacts if art.artifact_type == "transcript")

    print("\n--- LET Storage & Lineage Status ---")
    print(f"Data Root          : {config.data_dir}")
    print(f"Total Episodes     : {len(episodes)}")
    print(f"Raw Audio Captures : {raw_audio_count}")
    print(f"Transcripts        : {transcripts_count}")
    print(f"Total Artifacts    : {len(artifacts)}")
    print(f"Storage Footprint  : {total_bytes / (1024 * 1024):.2f} MB\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Les Enfants Terribles CLI")
    parser.add_argument("--data-dir", help="Override data directory path", default=None)
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # run command
    run_parser = subparsers.add_parser("run", help="Run the local web server")
    run_parser.add_argument("--host", help="Host address to bind", default=None)
    run_parser.add_argument("--port", type=int, help="Port to bind", default=None)
    run_parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    run_parser.add_argument("--no-worker", action="store_true", help="Disable in-process worker")

    # worker command
    worker_parser = subparsers.add_parser("worker", help="Run standalone background job worker")
    worker_parser.add_argument("--interval", type=float, default=1.0, help="Polling interval in seconds")

    # transcribe command
    tr_parser = subparsers.add_parser("transcribe", help="Transcribe an episode via CLI")
    tr_parser.add_argument("episode_id", help="Episode ID to transcribe")
    tr_parser.add_argument("--model", help="Whisper model size (e.g. tiny.en, base.en, small.en)", default=None)

    # doctor command
    subparsers.add_parser("doctor", help="Run diagnostics and verify artifact checksums")

    # status command
    subparsers.add_parser("status", help="Show system and storage status")

    args = parser.parse_args()

    if args.command == "run" or args.command is None:
        run_server(args)
    elif args.command == "worker":
        run_worker(args)
    elif args.command == "transcribe":
        run_transcribe(args)
    elif args.command == "doctor":
        run_doctor(args)
    elif args.command == "status":
        run_status(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
