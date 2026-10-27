"""Command-line interface for Speech Synthesize."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .engine import SynthesisError, SynthesisOptions, list_voices, synthesize_to_file


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="speech-synthesize", description="Convert text to audio using a local voice engine.")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text", help="Text to synthesize.")
    source.add_argument("--input", type=Path, help="UTF-8 text file to synthesize.")
    parser.add_argument("--output", type=Path, default=Path("output/speech.wav"))
    parser.add_argument("--rate", type=int, default=180, help="Speech rate (80-400).")
    parser.add_argument("--volume", type=float, default=1.0, help="Volume (0.0-1.0).")
    parser.add_argument("--voice-id", help="Installed system voice ID.")
    parser.add_argument("--list-voices", action="store_true", help="List installed system voices.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.list_voices:
        try:
            for voice in list_voices():
                print(f'{voice["id"]}\t{voice["name"]}\t{voice["languages"]}')
            return 0
        except SynthesisError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
    if args.text is None and args.input is None:
        parser.error("provide --text, --input, or --list-voices")
    try:
        text = args.text if args.text is not None else args.input.read_text(encoding="utf-8")
        result = synthesize_to_file(text, args.output, SynthesisOptions(rate=args.rate, volume=args.volume, voice_id=args.voice_id))
        print(result)
        return 0
    except (OSError, ValueError, SynthesisError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
