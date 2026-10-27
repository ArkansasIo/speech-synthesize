"""Command-line entry point."""
from __future__ import annotations
import argparse
from .config import load_config
from .engine import SpeechSynthesizer
from .models import SynthesisOptions
from .service import SpeechService
def main(argv=None)->int:
 p=argparse.ArgumentParser(prog="speech-synthesize"); sub=p.add_subparsers(dest="command",required=True)
 s=sub.add_parser("synthesize"); s.add_argument("text"); s.add_argument("-o","--output",default=None); s.add_argument("--rate",type=int,default=180); s.add_argument("--volume",type=float,default=1.0); s.add_argument("--voice-id")
 sub.add_parser("voices")
 a=p.parse_args(argv); cfg=load_config("config/default.toml")
 if a.command=="voices":
  for v in SpeechSynthesizer().list_voices(): print(f"{v.id}\t{v.name}\t{', '.join(v.languages)}")
  return 0
 opts=SynthesisOptions(a.rate,a.volume,a.voice_id)
 if a.output: print(SpeechSynthesizer().synthesize(a.text,a.output,opts).path)
 else: print(SpeechService(cfg).synthesize(a.text,opts).path)
 return 0
