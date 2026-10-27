"""Local text-to-speech engine built on pyttsx3."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


class SynthesisError(RuntimeError):
    """Raised when speech synthesis fails or the engine cannot be initialized."""


@dataclass(frozen=True, slots=True)
class SynthesisOptions:
    """Options supported by the local pyttsx3 backend."""
    rate: int = 180
    volume: float = 1.0
    voice_id: str | None = None

    def validate(self) -> None:
        if not 80 <= self.rate <= 400:
            raise ValueError("rate must be between 80 and 400 words per minute")
        if not 0.0 <= self.volume <= 1.0:
            raise ValueError("volume must be between 0.0 and 1.0")


def _create_engine() -> Any:
    try:
        import pyttsx3
    except ImportError as exc:
        raise SynthesisError("pyttsx3 is missing; install dependencies with pip install -e .") from exc
    try:
        return pyttsx3.init()
    except Exception as exc:
        raise SynthesisError("Could not initialize the local voice engine. Check system speech support.") from exc


def list_voices() -> list[dict[str, str]]:
    """List installed voices as dictionaries."""
    engine = _create_engine()
    try:
        result = []
        for voice in (engine.getProperty("voices") or []):
            languages = getattr(voice, "languages", []) or []
            result.append({"id": str(getattr(voice, "id", "")), "name": str(getattr(voice, "name", "")), "languages": ", ".join(map(str, languages))})
        return result
    except Exception as exc:
        raise SynthesisError("Unable to enumerate installed voices.") from exc
    finally:
        engine.stop()


def synthesize_to_file(text: str, output_path: str | Path, options: SynthesisOptions | None = None) -> Path:
    """Synthesize non-empty text to an audio file, returning its absolute path."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")
    if len(text) > 100_000:
        raise ValueError("text exceeds the 100,000-character limit")
    selected = options or SynthesisOptions()
    selected.validate()
    target = Path(output_path).expanduser()
    if not target.name or (target.exists() and target.is_dir()):
        raise ValueError("output_path must identify a file")
    target.parent.mkdir(parents=True, exist_ok=True)
    engine = _create_engine()
    try:
        engine.setProperty("rate", selected.rate)
        engine.setProperty("volume", selected.volume)
        if selected.voice_id:
            engine.setProperty("voice", selected.voice_id)
        engine.save_to_file(text.strip(), str(target))
        engine.runAndWait()
    except (ValueError, SynthesisError):
        raise
    except Exception as exc:
        raise SynthesisError(f"Speech synthesis failed for output '{target}'.") from exc
    finally:
        engine.stop()
    if not target.exists() or target.stat().st_size == 0:
        raise SynthesisError(f"Voice engine did not produce audio at '{target}'. Check platform support.")
    return target.resolve()
