"""Application service layer."""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from .config import SpeechConfig
from .engine import SpeechSynthesizer
from .models import SynthesisOptions, SynthesisResult
class SpeechService:
    def __init__(self, config:SpeechConfig, synthesizer:SpeechSynthesizer|None=None): self.config=config; self.synthesizer=synthesizer or SpeechSynthesizer()
    def synthesize(self,text:str,options:SynthesisOptions|None=None)->SynthesisResult:
        if len(text)>self.config.max_chars: raise ValueError(f"text exceeds {self.config.max_chars} characters")
        opts=options or SynthesisOptions(self.config.rate,self.config.volume)
        stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path=self.config.output_directory/f"speech-{stamp}-{uuid4().hex[:8]}.wav"
        return self.synthesizer.synthesize(text,path,opts)
