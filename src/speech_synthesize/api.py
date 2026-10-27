"""Optional local HTTP adapter. Run with uvicorn speech_synthesize.api:app."""
from __future__ import annotations

import os
import uuid
from pathlib import Path

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field
except ImportError as exc:
    raise RuntimeError("Install the optional API dependencies with pip install -e '.[api]'.") from exc

from .engine import SynthesisError, SynthesisOptions, synthesize_to_file

OUTPUT_DIR = Path(os.environ.get("SPEECH_SYNTHESIZE_OUTPUT_DIR", "output")).resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
app = FastAPI(title="Speech Synthesize API", version="0.1.0", description="Local text-to-speech service.")


class SynthesisRequest(BaseModel):
    text: str = Field(min_length=1, max_length=100_000)
    rate: int = Field(default=180, ge=80, le=400)
    volume: float = Field(default=1.0, ge=0.0, le=1.0)
    voice_id: str | None = Field(default=None, max_length=500)


class SynthesisResponse(BaseModel):
    job_id: str
    file_name: str
    output_path: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/synthesize", response_model=SynthesisResponse)
def synthesize(request: SynthesisRequest) -> SynthesisResponse:
    job_id = uuid.uuid4().hex
    target = OUTPUT_DIR / f"{job_id}.wav"
    try:
        result = synthesize_to_file(request.text, target, SynthesisOptions(rate=request.rate, volume=request.volume, voice_id=request.voice_id))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except SynthesisError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return SynthesisResponse(job_id=job_id, file_name=result.name, output_path=str(result))
