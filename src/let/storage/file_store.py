"""Atomic filesystem storage, path relativity, and SHA-256 integrity verification."""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Set, Tuple
from let.config import Config


@dataclass
class StoredFileResult:
    """Result of an atomic file persistence operation."""

    file_path: Path
    relative_path: str
    file_hash: str
    size_bytes: int


class FileStore:
    """Manages immutable raw and derived file storage with relative path normalization."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.config.ensure_directories()
        self.receipts_dir = self.config.data_dir / "raw" / "receipts"
        self.receipts_dir.mkdir(parents=True, exist_ok=True)

    def to_relative_path(self, path: str | Path) -> str:
        """Convert an absolute or relative path to a normalized relative path from data_dir."""
        p = Path(path)
        if p.is_absolute():
            try:
                rel = p.relative_to(self.config.data_dir)
                return rel.as_posix()
            except ValueError:
                # Path is outside data_dir; return its posix name
                return p.as_posix()
        return p.as_posix()

    def to_absolute_path(self, rel_path: str | Path) -> Path:
        """Resolve a relative or absolute path against config.data_dir."""
        p = Path(rel_path)
        if p.is_absolute():
            return p
        return (self.config.data_dir / p).resolve()

    @staticmethod
    def compute_hash_bytes(data: bytes) -> str:
        """Compute SHA-256 hash of byte buffer."""
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def compute_hash_file(file_path: Path) -> str:
        """Compute SHA-256 hash of a file on disk."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    def save_raw_audio(
        self,
        data: bytes | BinaryIO,
        original_filename: str = "audio.webm",
        episode_id: str | None = None,
    ) -> StoredFileResult:
        """Atomically persist raw audio to disk with SHA-256 calculation."""
        temp_id = uuid.uuid4().hex
        temp_file = self.config.temp_dir / f"{temp_id}.tmp"

        hasher = hashlib.sha256()
        size_bytes = 0

        try:
            with open(temp_file, "wb") as f:
                if isinstance(data, bytes):
                    f.write(data)
                    hasher.update(data)
                    size_bytes = len(data)
                else:
                    while chunk := data.read(65536):
                        f.write(chunk)
                        hasher.update(chunk)
                        size_bytes += len(chunk)

            file_hash = hasher.hexdigest()

            # Determine extension
            ext = Path(original_filename).suffix or ".webm"
            prefix = f"{episode_id}_" if episode_id else ""
            target_filename = f"{prefix}{file_hash[:16]}{ext}"
            final_path = self.config.raw_audio_dir / target_filename

            # Immutability check: if target exists with different content, error
            if final_path.exists():
                existing_hash = self.compute_hash_file(final_path)
                if existing_hash == file_hash:
                    # Content is identical, safe idempotent reuse
                    if temp_file.exists():
                        temp_file.unlink()
                    return StoredFileResult(
                        file_path=final_path,
                        relative_path=self.to_relative_path(final_path),
                        file_hash=file_hash,
                        size_bytes=size_bytes,
                    )
                raise FileExistsError(
                    f"Conflict: target file {final_path} exists with different hash!"
                )

            # Atomic replace into place
            os.replace(temp_file, final_path)
            return StoredFileResult(
                file_path=final_path,
                relative_path=self.to_relative_path(final_path),
                file_hash=file_hash,
                size_bytes=size_bytes,
            )

        finally:
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except OSError:
                    pass

    def save_derived_artifact(
        self,
        data: bytes | str,
        relative_subpath: str | Path,
    ) -> StoredFileResult:
        """Atomically persist a derived text/JSON/binary artifact into data_dir."""
        final_path = (self.config.data_dir / relative_subpath).resolve()
        final_path.parent.mkdir(parents=True, exist_ok=True)

        temp_id = uuid.uuid4().hex
        temp_file = self.config.temp_dir / f"{temp_id}.tmp"

        payload = data.encode("utf-8") if isinstance(data, str) else data
        file_hash = self.compute_hash_bytes(payload)
        size_bytes = len(payload)

        try:
            with open(temp_file, "wb") as f:
                f.write(payload)
            os.replace(temp_file, final_path)
            return StoredFileResult(
                file_path=final_path,
                relative_path=self.to_relative_path(final_path),
                file_hash=file_hash,
                size_bytes=size_bytes,
            )
        finally:
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except OSError:
                    pass

    def write_capture_receipt(
        self,
        relative_file_path: str | list[str],
        episode_id: str,
        metadata: dict,
        raw_files: Optional[list[dict]] = None,
    ) -> Path:
        """Write a disk recovery receipt if database persistence fails, tracking all raw files."""
        receipt_id = f"receipt_{uuid.uuid4().hex[:12]}.json"
        receipt_path = self.receipts_dir / receipt_id

        if isinstance(relative_file_path, list):
            rel_paths = relative_file_path
            primary_rel = rel_paths[0] if rel_paths else ""
        else:
            primary_rel = relative_file_path
            rel_paths = [relative_file_path] if relative_file_path else []

        payload = {
            "relative_file_path": primary_rel,
            "relative_file_paths": rel_paths,
            "raw_files": raw_files or [],
            "episode_id": episode_id,
            "metadata": metadata,
        }
        with open(receipt_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return receipt_path

    def remove_capture_receipt(self, receipt_path: Path | str) -> None:
        """Remove a processed recovery receipt."""
        p = Path(receipt_path)
        if p.exists():
            try:
                p.unlink()
            except OSError:
                pass

    def verify_artifact_integrity(self, file_path: str | Path, expected_hash: str) -> bool:
        """Check if file exists and cryptographic hash matches."""
        abs_path = self.to_absolute_path(file_path)
        if not abs_path.exists():
            return False
        return self.compute_hash_file(abs_path) == expected_hash

    def scan_orphans_and_receipts(
        self,
        known_relative_paths: Set[str],
    ) -> Tuple[list[Path], list[Path]]:
        """Scan disk for files not in database records and unconsumed receipts."""
        orphans: list[Path] = []
        receipts: list[Path] = []

        # Scan raw and derived directories
        for root_dir in [self.config.raw_dir, self.config.derived_dir]:
            if not root_dir.exists():
                continue
            for path in root_dir.rglob("*"):
                if path.is_file() and not path.name.endswith(".tmp"):
                    if "receipts" in path.parts:
                        receipts.append(path)
                    else:
                        rel = self.to_relative_path(path)
                        if rel not in known_relative_paths:
                            orphans.append(path)

        return orphans, receipts
