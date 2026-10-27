"""FastAPI application."""
from __future__ import annotations
from .config import load_config
from .engine import SpeechSynthesizer
from .models import SynthesisOptions
from .service import SpeechService

def create_app():
 try:
  from fastapi import FastAPI, HTTPException
  from pydantic import BaseModel, Field
 except ImportError as exc: raise RuntimeError("Install API extras: pip install -e '.[api]'") from exc
 app=FastAPI(title="Speech Synthesize API",version="1.0.0"); service=SpeechService(load_config("config/default.toml"))
 class Request(BaseModel):
  text:str=Field(min_length=1,max_length=100000); rate:int=Field(default=180,ge=80,le=400); volume:float=Field(default=1.0,ge=0,le=1); voice_id:str|None=None
 @app.get("/health")
 def health(): return {"status":"ok","backend":service.synthesizer.backend.name}
 @app.get("/v1/voices")
 def voices(): return [v.__dict__ if hasattr(v,"__dict__") else {"id":v.id,"name":v.name,"languages":v.languages,"gender":v.gender} for v in service.synthesizer.list_voices()]
 @app.post("/v1/synthesize")
 def synthesize(req:Request):
  try: return {"path":service.synthesize(req.text,SynthesisOptions(req.rate,req.volume,req.voice_id)).path}
  except Exception as exc: raise HTTPException(500,str(exc)) from exc
 return app
try: app=create_app()
except RuntimeError: app=None
