"""Command-line entry point with backwards-compatible flags."""
from __future__ import annotations
import argparse
from pathlib import Path
from .config import load_config
from .engine import SpeechSynthesizer, synthesize_to_file
from .models import SynthesisOptions
from .service import SpeechService

def main(argv=None)->int:
 p=argparse.ArgumentParser(prog="speech-synthesize")
 p.add_argument("text",nargs="?"); p.add_argument("--input",type=Path); p.add_argument("-o","--output",type=Path); p.add_argument("--rate",type=int,default=180); p.add_argument("--volume",type=float,default=1.0); p.add_argument("--voice-id"); p.add_argument("--list-voices",action="store_true")
 a=p.parse_args(argv)
 if a.list_voices:
  for v in SpeechSynthesizer().list_voices(): print(f"{v.id}\t{v.name}\t{', '.join(v.languages)}")
  return 0
 if a.input:
  text=a.input.read_text(encoding="utf-8")
 elif a.text: text=a.text
 else: p.error("provide text or --input")
 opts=SynthesisOptions(a.rate,a.volume,a.voice_id)
 if a.output: print(synthesize_to_file(text,a.output,opts))
 else: print(SpeechService(load_config("config/default.toml")).synthesize(text,opts).path)
 return 0
