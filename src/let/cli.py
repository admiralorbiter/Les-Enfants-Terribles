"""Command-line interface and diagnostic doctor for LET."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from let.config import get_config
from let.db.connection import DatabaseManager
from let.db.repository import Repository
from let.storage.file_store import FileStore
from let.web.app import create_app


def run_server(args: argparse.Namespace) -> None:
    """Launch local LET web server."""
    config = get_config(data_dir_override=args.data_dir)
    app = create_app(config)
    
    port = args.port or config.port
    host = args.host or config.host
    debug = args.debug or config.debug

    print(f"\n=======================================================")
    print(f" Les Enfants Terribles (LET) — Foundation Substrate")
    print(f" Local Data Root : {config.data_dir}")
    print(f" SQLite Database  : {config.db_path}")
    print(f" Server URL       : http://{host}:{port}")
    print(f"=======================================================\n")

    app.run(host=host, port=port, debug=debug)


def run_doctor(args: argparse.Namespace) -> None:
    """Run diagnostic checks on storage, database, and artifact cryptographic integrity."""
    config = get_config(data_dir_override=args.data_dir)
    print("\n--- LET System Doctor ---")
    print(f"Data Root: {config.data_dir}")

    # 1. Directory Checks
    print("\n[1/4] Checking filesystem directories...")
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
    print("\n[2/4] Checking SQLite database...")
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

    # 3. Artifact Cryptographic Hash Verification
    print("\n[3/4] Verifying artifact hashes against disk...")
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
                print(f"  [OK] Artifact {art.id} ({art.artifact_type}): SHA-256 verified ({art.size_bytes} bytes)")
            else:
                print(f"  [FAIL] Artifact {art.id}: HASH MISMATCH! DB={art.file_hash} Disk={disk_hash}")
                artifacts_ok = False

    # 4. Summary
    print("\n[4/4] Summary Result:")
    if all_dirs_ok and db_ok and artifacts_ok:
        print("  [OK] ALL SYSTEMS HEALTHY. Trustworthy capture invariant satisfied.\n")
    else:
        print("  [FAIL] ISSUES DETECTED. Please review the errors above.\n")
        sys.exit(1)


def run_status(args: argparse.Namespace) -> None:
    """Print high-level statistics about stored episodes and storage footprint."""
    config = get_config(data_dir_override=args.data_dir)
    db = DatabaseManager(config)
    repo = Repository(db)

    episodes = repo.list_episodes(limit=1000)
    artifacts = repo.list_all_artifacts()

    total_bytes = sum(art.size_bytes for art in artifacts)
    raw_audio_count = sum(1 for art in artifacts if art.artifact_type == "audio" and art.is_raw)

    print("\n--- LET Storage Status ---")
    print(f"Data Root          : {config.data_dir}")
    print(f"Total Episodes     : {len(episodes)}")
    print(f"Raw Audio Captures : {raw_audio_count}")
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

    # doctor command
    subparsers.add_parser("doctor", help="Run diagnostics and verify artifact checksums")

    # status command
    subparsers.add_parser("status", help="Show system and storage status")

    args = parser.parse_args()

    if args.command == "run" or args.command is None:
        run_server(args)
    elif args.command == "doctor":
        run_doctor(args)
    elif args.command == "status":
        run_status(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
