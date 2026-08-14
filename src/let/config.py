"""Configuration and directory resolution for LET."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load local .env if present
load_dotenv()


@dataclass(frozen=True)
class Config:
    """System configuration parameters."""

    data_dir: Path
    host: str = "127.0.0.1"
    port: int = 5000
    debug: bool = False

    @property
    def db_path(self) -> Path:
        return self.data_dir / "let.sqlite"

    @property
    def raw_audio_dir(self) -> Path:
        return self.data_dir / "raw" / "audio"

    @property
    def raw_text_dir(self) -> Path:
        return self.data_dir / "raw" / "text"

    @property
    def raw_video_dir(self) -> Path:
        return self.data_dir / "raw" / "video"

    @property
    def derived_transcripts_dir(self) -> Path:
        return self.data_dir / "derived" / "transcripts"

    @property
    def derived_analyses_dir(self) -> Path:
        return self.data_dir / "derived" / "analyses"

    @property
    def backups_dir(self) -> Path:
        return self.data_dir / "backups"

    @property
    def temp_dir(self) -> Path:
        return self.data_dir / "temp"

    def ensure_directories(self) -> None:
        """Ensure all required filesystem directories exist."""
        for directory in [
            self.data_dir,
            self.raw_audio_dir,
            self.raw_text_dir,
            self.raw_video_dir,
            self.derived_transcripts_dir,
            self.derived_analyses_dir,
            self.backups_dir,
            self.temp_dir,
        ]:
            directory.mkdir(parents=True, exist_ok=True)


def get_config(data_dir_override: str | Path | None = None) -> Config:
    """Resolve and return system configuration."""
    if data_dir_override:
        base_dir = Path(data_dir_override).expanduser().resolve()
    else:
        env_path = os.getenv("LET_DATA_DIR")
        if env_path:
            base_dir = Path(env_path).expanduser().resolve()
        else:
            base_dir = (Path.home() / ".let_data").resolve()

    host = os.getenv("LET_HOST", "127.0.0.1")
    port = int(os.getenv("LET_PORT", "5000"))
    debug = os.getenv("LET_DEBUG", "false").lower() in ("true", "1", "yes")

    config = Config(data_dir=base_dir, host=host, port=port, debug=debug)
    config.ensure_directories()
    return config
