"""Configuration loading."""
from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SpeechConfig:
    backend: str = "pyttsx3"
    rate: int = 180
    volume: float = 1.0
    max_chars: int = 100_000
    output_directory: Path = Path("output")
    language: str = "en-US"
    database_enabled: bool = False


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_config(path: str | Path | None = None) -> SpeechConfig:
    data: dict = {}
    if path and Path(path).exists():
        with Path(path).open("rb") as f:
            data = tomllib.load(f)
    engine = data.get("engine", {})
    output = data.get("output", {})
    english = data.get("english", {})
    database = data.get("database", {})
    return SpeechConfig(
        backend=os.getenv("SPEECH_BACKEND", engine.get("backend", "pyttsx3")),
        rate=int(os.getenv("SPEECH_RATE", engine.get("rate", english.get("default_rate", 180)))),
        volume=float(os.getenv("SPEECH_VOLUME", engine.get("volume", english.get("default_volume", 1.0)))),
        max_chars=int(os.getenv("SPEECH_MAX_CHARS", engine.get("max_chars", 100000))),
        output_directory=Path(os.getenv("SPEECH_OUTPUT_DIR", output.get("directory", "output"))),
        language=os.getenv("SPEECH_LANGUAGE", english.get("language", "en-US")),
        database_enabled=_env_bool("SPEECH_DB_ENABLED", bool(database.get("enabled", False))),
    )
