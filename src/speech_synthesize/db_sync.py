"""Synchronize installed English system voices into MySQL."""
from __future__ import annotations

from .database import Database
from .engine import SpeechSynthesizer
from .repositories import VoiceRepository


def sync_english_voices(database: Database, synthesizer: SpeechSynthesizer | None = None) -> int:
    engine = synthesizer or SpeechSynthesizer()
    voices = engine.list_voices()
    count = 0
    with database.session() as session:
        repository = VoiceRepository(session)
        for voice in voices:
            languages = tuple(v.lower() for v in voice.languages)
            if languages and not any(value.startswith("en") for value in languages):
                continue
            repository.upsert(voice, backend=engine.backend.name, language="en-US")
            count += 1
    return count
