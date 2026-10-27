"""FastAPI application."""
from __future__ import annotations

from .config import load_config
from .database import Database
from .engine import SpeechSynthesizer
from .models import SynthesisOptions
from .service import SpeechService


def create_app():
    try:
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel, Field
    except ImportError as exc:
        raise RuntimeError("Install API extras: pip install -e '.[api]'") from exc

    config = load_config("config/default.toml")
    database = None
    if config.database_enabled:
        database = Database()
    service = SpeechService(config, SpeechSynthesizer(), database)
    app = FastAPI(title="Speech Synthesize API", version="0.2.0")

    class SynthesisRequest(BaseModel):
        text: str = Field(min_length=1, max_length=100000)
        rate: int = Field(default=180, ge=80, le=400)
        volume: float = Field(default=1.0, ge=0, le=1)
        voice_id: str | None = None
        language: str = Field(default="en-US", pattern=r"^en(-[A-Za-z0-9]+)*$")

    @app.get("/health")
    def health():
        result = {"status": "ok", "backend": service.synthesizer.backend.name, "database": False}
        if database is not None:
            try:
                result["database"] = database.ping()
            except Exception:
                result["status"] = "degraded"
        return result

    @app.get("/v1/voices")
    def voices():
        values = service.synthesizer.list_voices()
        return [{"id": v.id, "name": v.name, "languages": v.languages, "gender": v.gender} for v in values]

    @app.post("/v1/synthesize")
    def synthesize(req: SynthesisRequest):
        try:
            result = service.synthesize(
                req.text,
                SynthesisOptions(req.rate, req.volume, req.voice_id, req.language),
            )
            return {"job_id": result.job_id, "path": result.path, "voice_id": result.voice_id}
        except ValueError as exc:
            raise HTTPException(400, str(exc)) from exc
        except Exception as exc:
            raise HTTPException(500, str(exc)) from exc

    @app.get("/v1/jobs/{job_id}")
    def get_job(job_id: str):
        if database is None:
            raise HTTPException(503, "database persistence is disabled")
        from .repositories import JobRepository
        with database.session() as session:
            job = JobRepository(session).get(job_id)
            if job is None:
                raise HTTPException(404, "job not found")
            return {
                "id": job.id,
                "status": job.status,
                "language": job.language,
                "voice_id": job.voice_id,
                "output_format": job.output_format,
                "output_path": job.output_path,
                "error_message": job.error_message,
                "duration_seconds": job.duration,
            }

    return app


try:
    app = create_app()
except RuntimeError:
    app = None


def run() -> None:
    import uvicorn
    uvicorn.run("speech_synthesize.api:app", host="0.0.0.0", port=8000, reload=False)
