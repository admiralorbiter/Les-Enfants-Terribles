"""Command-line interface and diagnostic doctor for LET."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import uuid
from pathlib import Path
from let.config import get_config
from let.db.connection import DatabaseManager
from let.db.repository import Repository
from let.jobs.worker import JobWorker
from let.models.entities import Artifact, Episode, Event, Job
from let.storage.backup import create_backup, verify_and_restore
from let.storage.file_store import FileStore
from let.transcription.faster_whisper_engine import FasterWhisperTranscriber
from let.web.app import create_app


def run_server(args: argparse.Namespace) -> None:
    """Launch local LET web server with safe CLI argument defaults."""
    config = get_config(data_dir_override=args.data_dir)

    port = getattr(args, "port", None) or config.port
    host = getattr(args, "host", None) or config.host
    debug = getattr(args, "debug", False) or config.debug
    no_worker = getattr(args, "no_worker", False)

    # In debug mode, start the in-process worker only in the Werkzeug reloader child
    should_start_worker = (not no_worker) and (not debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true")
    app = create_app(config, start_worker=should_start_worker)

    print(f"\n=======================================================")
    print(f" Les Enfants Terribles (LET) — Capture & Audio Substrate")
    print(f" Local Data Root  : {config.data_dir}")
    print(f" SQLite Database   : {config.db_path}")
    print(f" Whisper Model     : {config.whisper_model_size} ({config.whisper_device})")
    print(f" Server URL        : http://{host}:{port}")
    print(f" Background Worker : {'Enabled' if should_start_worker else 'Disabled'}")
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


def run_backup(args: argparse.Namespace) -> None:
    """Create a standalone, verified backup folder with a cryptographic manifest."""
    config = get_config(data_dir_override=args.data_dir)
    output_dir = args.output or (config.backups_dir / f"backup_{int(os.path.getmtime(config.db_path) if config.db_path.exists() else 0)}")
    print(f"\n--- Creating LET Backup ---")
    print(f"Source Data Root : {config.data_dir}")
    print(f"Backup Output Dir: {output_dir}")

    try:
        manifest = create_backup(config, output_dir)
        print(f"\n[OK] Backup successfully created!")
        print(f"  Total Files       : {manifest['total_files']}")
        print(f"  Total Size        : {manifest['total_bytes'] / (1024 * 1024):.2f} MB")
        print(f"  Database Integrity: {manifest['database_integrity']}")
        print(f"  Manifest Location : {Path(output_dir) / 'manifest.json'}\n")
    except Exception as e:
        print(f"\n[FAIL] Backup creation failed: {e}\n")
        sys.exit(1)


def run_restore(args: argparse.Namespace) -> None:
    """Verify and restore an existing backup folder."""
    config = get_config(data_dir_override=args.data_dir)
    target_dir = args.target_dir or config.data_dir
    verify_only = args.verify_only

    print(f"\n--- LET Backup Verification & Restore ---")
    print(f"Backup Folder: {args.backup_dir}")
    print(f"Target Root  : {target_dir} ({'Trial Verification Only' if verify_only else 'Live Restoration'})")

    try:
        result = verify_and_restore(args.backup_dir, target_dir, verify_only=verify_only)
        if verify_only:
            print(f"\n[OK] Backup verification PASSED! All checksums and trial database queries succeeded.")
            print(f"  Files Verified    : {result['files_verified']}")
            print(f"  Database Integrity: {result['database_integrity']}")
            print(f"  Trial Episodes    : {result['test_episodes_found']}\n")
        else:
            print(f"\n[OK] Backup successfully restored into {target_dir}!")
            print(f"  Files Restored    : {result['files_restored']}")
            print(f"  Database Integrity: {result['database_integrity']}\n")
    except Exception as e:
        print(f"\n[FAIL] Restore failed: {e}\n")
        sys.exit(1)


def run_doctor(args: argparse.Namespace) -> None:
    """Run diagnostic checks on storage, database, dependencies, and artifact integrity."""
    config = get_config(data_dir_override=args.data_dir)
    repair = getattr(args, "repair", False)
    print("\n--- LET System Doctor ---")
    print(f"Data Root: {config.data_dir} ({'Repair Mode ON' if repair else 'Read-Only'})")

    # 1. Directory Checks
    print("\n[1/6] Checking filesystem directories...")
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
    print("\n[2/6] Checking SQLite database...")
    db_ok = False
    try:
        db = DatabaseManager(config)
        with db.transaction() as conn:
            integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
            schema_ver = conn.execute("SELECT MAX(version) FROM schema_migrations").fetchone()[0]
            if integrity == "ok":
                print(f"  [OK] Database integrity: {integrity} (Schema version {schema_ver})")
                db_ok = True
            else:
                print(f"  [FAIL] Integrity error: {integrity}")
    except Exception as e:
        print(f"  [FAIL] Database connection error: {e}")

    # 3. Audio & Transcription Tool Checks
    print("\n[3/6] Checking transcription runtime dependencies...")
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
        print(f"  [WARN] faster-whisper import: {e} (local transcription will use fallback if not installed)")

    # 4. Artifact Cryptographic Hash Verification
    print("\n[4/6] Verifying artifact hashes against disk...")
    store = FileStore(config)
    repo = Repository(db) if db_ok else None

    artifacts_ok = True
    known_rel_paths: set[str] = set()
    if repo:
        artifacts = repo.list_all_artifacts()
        print(f"  Found {len(artifacts)} registered artifact(s).")
        for art in artifacts:
            abs_path = store.to_absolute_path(art.file_path)
            known_rel_paths.add(store.to_relative_path(art.file_path))
            if not abs_path.exists():
                print(f"  [FAIL] Artifact {art.id}: File missing at {abs_path}")
                artifacts_ok = False
                continue

            disk_hash = store.compute_hash_file(abs_path)
            if disk_hash == art.file_hash:
                badge = "RAW" if art.is_raw else "DERIVED"
                print(f"  [OK] Artifact {art.id} [{badge}] ({art.artifact_type}): SHA-256 verified ({art.size_bytes} bytes)")
            else:
                print(f"  [FAIL] Artifact {art.id}: HASH MISMATCH! DB={art.file_hash} Disk={disk_hash}")
                artifacts_ok = False

    # 5. Orphans and Recovery Receipts Check
    print("\n[5/6] Scanning for untracked files and crash recovery receipts...")
    orphans, receipts = store.scan_orphans_and_receipts(known_rel_paths)
    if receipts:
        print(f"  [WARN] Found {len(receipts)} unconsumed recovery receipt(s):")
        for r in receipts:
            print(f"    - {r.name}")
            if repair and repo:
                try:
                    with open(r, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    rel_p = data["relative_file_path"]
                    ep_id = data["episode_id"]
                    meta = data.get("metadata", {})
                    ep = repo.get_episode(ep_id)
                    if not ep:
                        ep = Episode(id=ep_id, title=meta.get("title", "Recovered Episode"), domain=meta.get("domain", "general"), mode=meta.get("mode", "capture"))
                        repo.create_episode(ep)
                    file_abs = store.to_absolute_path(rel_p)
                    file_hash = meta.get("file_hash")
                    if not file_hash:
                        if file_abs.exists():
                            file_hash = store.compute_hash_file(file_abs)
                        else:
                            file_hash = "0" * 64
                    size_bytes = meta.get("size_bytes")
                    if size_bytes is None:
                        size_bytes = file_abs.stat().st_size if file_abs.exists() else 0

                    art = Artifact(
                        id=meta.get("artifact_id", f"art_{uuid.uuid4().hex[:12]}"),
                        episode_id=ep_id,
                        artifact_type="audio",
                        is_raw=True,
                        file_path=rel_p,
                        file_hash=file_hash,
                        mime_type=meta.get("mime_type", "audio/webm"),
                        size_bytes=size_bytes,
                    )
                    repo.create_artifact(art)
                    store.remove_capture_receipt(r)
                    print(f"      -> Successfully repaired and registered {art.id} into episode {ep_id}")
                except Exception as ex:
                    print(f"      -> Repair failed: {ex}")
    else:
        print("  [OK] No unconsumed capture receipts found.")

    if orphans:
        print(f"  [INFO] Found {len(orphans)} untracked file(s) on disk:")
        for o in orphans:
            print(f"    - {store.to_relative_path(o)}")
    else:
        print("  [OK] No orphaned media files found on disk.")

    # 6. Summary
    print("\n[6/6] Summary Result:")
    all_ok = all_dirs_ok and db_ok and ffmpeg_ok and artifacts_ok and not receipts
    if all_ok:
        print("  [OK] ALL SYSTEMS HEALTHY. Trustworthy capture, durability, and lineage satisfied.\n")
    else:
        print("  [WARN] Issues or warnings detected. Review the items above.\n")
        if not artifacts_ok or not db_ok or not all_dirs_ok:
            sys.exit(1)


def run_status(args: argparse.Namespace) -> None:
    """Print high-level statistics about stored episodes, transcripts, and storage footprint."""
    config = get_config(data_dir_override=args.data_dir)
    db = DatabaseManager(config)
    repo = Repository(db)

    episodes = repo.list_episodes(limit=1000)
    artifacts = repo.list_all_artifacts()
    jobs = repo.list_jobs(limit=1000)

    total_bytes = sum(art.size_bytes for art in artifacts)
    raw_audio_count = sum(1 for art in artifacts if art.artifact_type == "audio" and art.is_raw)
    transcripts_count = sum(1 for art in artifacts if art.artifact_type == "transcript")
    analyses_count = sum(1 for art in artifacts if art.artifact_type == "analysis")

    print("\n--- LET Storage & Lineage Status ---")
    print(f"Data Root          : {config.data_dir}")
    print(f"Total Episodes     : {len(episodes)}")
    print(f"Raw Audio Captures : {raw_audio_count}")
    print(f"Transcripts        : {transcripts_count}")
    print(f"Imported Analyses  : {analyses_count}")
    print(f"Total Artifacts    : {len(artifacts)}")
    print(f"Total Jobs Tracked : {len(jobs)}")
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

    # backup command
    bk_parser = subparsers.add_parser("backup", help="Create verified standalone backup")
    bk_parser.add_argument("--output", "-o", help="Target backup directory path", default=None)

    # restore command
    rst_parser = subparsers.add_parser("restore", help="Verify and restore backup folder")
    rst_parser.add_argument("backup_dir", help="Path to backup folder containing manifest.json")
    rst_parser.add_argument("--target-dir", help="Target data directory to restore into", default=None)
    rst_parser.add_argument("--verify-only", action="store_true", help="Perform trial rehearsal verification without writing live data")

    # doctor command
    doc_parser = subparsers.add_parser("doctor", help="Run diagnostics and verify artifact checksums")
    doc_parser.add_argument("--repair", action="store_true", help="Automatically repair unconsumed receipts and missing registrations")

    # status command
    subparsers.add_parser("status", help="Show system and storage status")

    args = parser.parse_args()

    if args.command == "run" or args.command is None:
        run_server(args)
    elif args.command == "worker":
        run_worker(args)
    elif args.command == "transcribe":
        run_transcribe(args)
    elif args.command == "backup":
        run_backup(args)
    elif args.command == "restore":
        run_restore(args)
    elif args.command == "doctor":
        run_doctor(args)
    elif args.command == "status":
        run_status(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
