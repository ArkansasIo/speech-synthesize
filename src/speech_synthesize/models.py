"""Domain models for speech synthesis."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SynthesisOptions:
    rate: int = 180
    volume: float = 1.0
    voice_id: str | None = None
    language: str | None = None
    output_format: str = "wav"
    def validate(self) -> None:
        if not 80 <= self.rate <= 400: raise ValueError("rate must be between 80 and 400")
        if not 0.0 <= self.volume <= 1.0: raise ValueError("volume must be between 0.0 and 1.0")
        if self.output_format.lower() not in {"wav"}: raise ValueError("only wav output is currently supported")

@dataclass(frozen=True, slots=True)
class VoiceInfo:
    id: str
    name: str
    languages: tuple[str, ...] = ()
    gender: str | None = None

@dataclass(frozen=True, slots=True)
class SynthesisResult:
    path: str
    voice_id: str | None = None
