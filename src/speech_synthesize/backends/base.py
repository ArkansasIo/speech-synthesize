"""Backend contract."""
from __future__ import annotations
from pathlib import Path
from typing import Protocol
from ..models import SynthesisOptions, VoiceInfo
class SpeechBackend(Protocol):
    name: str
    def list_voices(self) -> list[VoiceInfo]: ...
    def synthesize(self, text: str, output_path: Path, options: SynthesisOptions) -> None: ...
