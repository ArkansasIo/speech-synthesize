"""Compatibility facade for local speech synthesis."""
from __future__ import annotations
from pathlib import Path
from .backends import Pyttsx3Backend
from .exceptions import SynthesisError
from .models import SynthesisOptions
from .models import SynthesisResult

def list_voices():
    return [{"id":v.id,"name":v.name,"languages":", ".join(v.languages)} for v in Pyttsx3Backend().list_voices()]

def synthesize_to_file(text:str, output_path:str|Path, options:SynthesisOptions|None=None)->Path:
    if not isinstance(text,str) or not text.strip(): raise ValueError("text must be a non-empty string")
    if len(text)>100_000: raise ValueError("text exceeds the 100,000-character limit")
    opts=options or SynthesisOptions(); opts.validate(); target=Path(output_path).expanduser(); target.parent.mkdir(parents=True,exist_ok=True)
    Pyttsx3Backend().synthesize(text,target,opts); return target.resolve()
class SpeechSynthesizer:
    def __init__(self,backend=None): self.backend=backend or Pyttsx3Backend()
    def list_voices(self): return self.backend.list_voices()
    def synthesize(self,text,output_path,options=None):
        opts=options or SynthesisOptions(); opts.validate(); target=Path(output_path); target.parent.mkdir(parents=True,exist_ok=True); self.backend.synthesize(text,target,opts); return SynthesisResult(str(target.resolve()),opts.voice_id)
