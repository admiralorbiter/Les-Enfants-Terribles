"""Disaster recovery, verified restore rehearsal, and cryptographic backup manifests."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from let.config import Config
from let.db.connection import DatabaseManager


def _compute_hash(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def create_backup(config: Config, output_dir: Path | str) -> Dict[str, Any]:
    """Create a self-contained, verified backup folder with a cryptographic manifest."""
    out_path = Path(output_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    db_manager = DatabaseManager(config)

    # 1. Safe online SQLite backup
    backup_db_path = out_path / "let.sqlite"
    db_manager.backup_to(backup_db_path)

    # Verify backup database integrity
    conn = sqlite3.connect(str(backup_db_path))
    try:
        integrity_row = conn.execute("PRAGMA integrity_check;").fetchone()
        db_integrity = integrity_row[0] if integrity_row else "unknown"
        schema_version_row = conn.execute(
            "SELECT MAX(version) FROM schema_migrations;"
        ).fetchone()
        schema_version = schema_version_row[0] if schema_version_row else 1
    finally:
        conn.close()

    # 2. Copy raw and derived files
    files_manifest: List[Dict[str, Any]] = []
    total_bytes = 0

    # Include database in manifest
    db_hash = _compute_hash(backup_db_path)
    db_size = backup_db_path.stat().st_size
    files_manifest.append(
        {
            "relative_path": "let.sqlite",
            "sha256": db_hash,
            "size_bytes": db_size,
        }
    )
    total_bytes += db_size

    # Copy files from raw and derived folders
    for folder_name in ["raw", "derived"]:
        src_folder = config.data_dir / folder_name
        dest_folder = out_path / folder_name
        if src_folder.exists():
            for src_file in src_folder.rglob("*"):
                if src_file.is_file() and not src_file.name.endswith(".tmp"):
                    rel_to_data = src_file.relative_to(config.data_dir)
                    target_file = out_path / rel_to_data
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, target_file)

                    file_hash = _compute_hash(target_file)
                    file_size = target_file.stat().st_size
                    files_manifest.append(
                        {
                            "relative_path": rel_to_data.as_posix(),
                            "sha256": file_hash,
                            "size_bytes": file_size,
                        }
                    )
                    total_bytes += file_size

    # 3. Create manifest.json
    manifest = {
        "backup_timestamp": datetime.now(timezone.utc).isoformat(),
        "schema_version": schema_version,
        "database_integrity": db_integrity,
        "total_files": len(files_manifest),
        "total_bytes": total_bytes,
        "files": files_manifest,
    }

    manifest_path = out_path / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return manifest


def verify_and_restore(
    backup_dir: Path | str,
    target_data_dir: Path | str,
    verify_only: bool = False,
) -> Dict[str, Any]:
    """Verify backup integrity against manifest.json and optionally restore into target_data_dir."""
    b_path = Path(backup_dir).resolve()
    manifest_file = b_path / "manifest.json"

    if not manifest_file.exists():
        raise FileNotFoundError(f"Backup manifest not found in {b_path}")

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # 1. Verify checksums of all files in manifest
    verified_files = 0
    for item in manifest.get("files", []):
        rel = item["relative_path"]
        expected_hash = item["sha256"]
        file_path = b_path / rel
        if not file_path.exists():
            raise FileNotFoundError(f"Missing file declared in manifest: {rel}")
        actual_hash = _compute_hash(file_path)
        if actual_hash != expected_hash:
            raise ValueError(
                f"Checksum mismatch for {rel}: expected {expected_hash}, got {actual_hash}"
            )
        verified_files += 1

    # 2. Check SQLite integrity on backup file
    backup_db = b_path / "let.sqlite"
    conn = sqlite3.connect(str(backup_db))
    try:
        integrity_row = conn.execute("PRAGMA integrity_check;").fetchone()
        db_integrity = integrity_row[0] if integrity_row else "error"
        if db_integrity != "ok":
            raise ValueError(f"SQLite backup database integrity check failed: {db_integrity}")
    finally:
        conn.close()

    # 3. If verify_only, test a trial dry-run in a temporary directory
    if verify_only:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_target = Path(tmp_dir)
            for item in manifest.get("files", []):
                rel = item["relative_path"]
                src = b_path / rel
                dst = tmp_target / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

            # Test connecting and reading tables from restored DB
            test_conn = sqlite3.connect(str(tmp_target / "let.sqlite"))
            try:
                ep_count = test_conn.execute("SELECT COUNT(*) FROM episodes;").fetchone()[0]
                art_count = test_conn.execute("SELECT COUNT(*) FROM artifacts;").fetchone()[0]
            finally:
                test_conn.close()

        return {
            "status": "verified",
            "files_verified": verified_files,
            "database_integrity": db_integrity,
            "test_episodes_found": ep_count,
            "test_artifacts_found": art_count,
        }

    # 4. Actual restoration into target_data_dir
    target_path = Path(target_data_dir).resolve()
    target_path.mkdir(parents=True, exist_ok=True)

    for item in manifest.get("files", []):
        rel = item["relative_path"]
        src = b_path / rel
        dst = target_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    return {
        "status": "restored",
        "files_restored": verified_files,
        "database_integrity": db_integrity,
        "target_path": str(target_path),
    }
