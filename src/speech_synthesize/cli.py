"""Command-line entry point."""
from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_config
from .database import Database
from .engine import SpeechSynthesizer, synthesize_to_file
from .models import SynthesisOptions
from .service import SpeechService


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="speech-synthesize")
    parser.add_argument("text", nargs="?")
    parser.add_argument("--input", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--rate", type=int, default=180)
    parser.add_argument("--volume", type=float, default=1.0)
    parser.add_argument("--voice-id")
    parser.add_argument("--language", default="en-US")
    parser.add_argument("--list-voices", action="store_true")
    parser.add_argument("--sync-voices", action="store_true")
    parser.add_argument("--db-health", action="store_true")
    args = parser.parse_args(argv)

    if args.list_voices:
        for voice in SpeechSynthesizer().list_voices():
            print(f"{voice.id}\t{voice.name}\t{', '.join(voice.languages)}")
        return 0

    if args.db_health or args.sync_voices:
        database = Database()
        try:
            if not database.ping():
                return 1
            if args.db_health:
                print("database: ok")
            if args.sync_voices:
                from .db_sync import sync_english_voices
                count = sync_english_voices(database)
                print(f"synced English voices: {count}")
            return 0
        finally:
            database.dispose()

    if args.input:
        text = args.input.read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    else:
        parser.error("provide text or --input")

    options = SynthesisOptions(args.rate, args.volume, args.voice_id, args.language)
    if args.output:
        print(synthesize_to_file(text, args.output, options))
    else:
        config = load_config("config/default.toml")
        database = Database() if config.database_enabled else None
        try:
            print(SpeechService(config, database=database).synthesize(text, options).path)
        finally:
            if database:
                database.dispose()
    return 0
