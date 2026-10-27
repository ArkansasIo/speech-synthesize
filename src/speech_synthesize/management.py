"""Administrative command helpers."""
from __future__ import annotations

from .database import Database
from .db_sync import sync_english_voices
from .engine import SpeechSynthesizer


def sync_voices() -> int:
    database = Database()
    try:
        return sync_english_voices(database, SpeechSynthesizer())
    finally:
        database.dispose()


def database_health() -> bool:
    database = Database()
    try:
        return database.ping()
    finally:
        database.dispose()
