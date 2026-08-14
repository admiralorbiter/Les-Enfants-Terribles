"""Atomic filesystem storage and SHA-256 integrity verification."""

from __future__ import annotations

import hashlib
import os
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO
from let.config import Config


@dataclass
class StoredFileResult:
    """Result of an atomic file persistence operation."""

    file_path: Path
    file_hash: str
    size_bytes: int


class FileStore:
    """Manages immutable raw and derived file storage."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.config.ensure_directories()

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
                file_hash=file_hash,
                size_bytes=size_bytes,
            )

        finally:
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except OSError:
                    pass

    def verify_artifact_integrity(self, file_path: str | Path, expected_hash: str) -> bool:
        """Check if file exists and cryptographic hash matches."""
        path = Path(file_path)
        if not path.exists():
            return False
        return self.compute_hash_file(path) == expected_hash
