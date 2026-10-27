"""Configuration loading."""
from __future__ import annotations
import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
@dataclass(frozen=True, slots=True)
class SpeechConfig:
    backend: str="pyttsx3"; rate:int=180; volume:float=1.0; max_chars:int=100_000; output_directory:Path=Path("output")
def load_config(path: str|Path|None=None) -> SpeechConfig:
    data={}
    if path and Path(path).exists():
        with Path(path).open("rb") as f: data=tomllib.load(f)
    e=data.get("engine",{}); o=data.get("output",{})
    return SpeechConfig(os.getenv("SPEECH_BACKEND",e.get("backend","pyttsx3")), int(os.getenv("SPEECH_RATE",e.get("rate",180))), float(os.getenv("SPEECH_VOLUME",e.get("volume",1.0))), int(os.getenv("SPEECH_MAX_CHARS",e.get("max_chars",100000))), Path(os.getenv("SPEECH_OUTPUT_DIR",o.get("directory","output"))))
