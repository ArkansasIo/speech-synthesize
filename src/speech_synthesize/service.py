"""Application service layer with optional MySQL job persistence."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from uuid import uuid4

from .config import SpeechConfig
from .engine import SpeechSynthesizer
from .models import SynthesisOptions, SynthesisResult


class SpeechService:
    def __init__(self, config: SpeechConfig, synthesizer: SpeechSynthesizer | None = None, database=None):
        self.config = config
        self.synthesizer = synthesizer or SpeechSynthesizer()
        self.database = database

    def synthesize(self, text: str, options: SynthesisOptions | None = None) -> SynthesisResult:
        if not text.strip():
            raise ValueError("text must not be empty")
        if len(text) > self.config.max_chars:
            raise ValueError(f"text exceeds {self.config.max_chars} characters")
        opts = options or SynthesisOptions(self.config.rate, self.config.volume, language="en-US")
        opts.validate()
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = self.config.output_directory / f"speech-{stamp}-{uuid4().hex[:8]}.wav"
        job_id = None
        repo = None
        if self.database is not None:
            from .repositories import JobRepository
            with self.database.session() as session:
                repo = JobRepository(session)
                job = repo.create(text, opts, self.synthesizer.backend.name)
                job_id = job.id
                repo.mark_running(job_id)
        started = perf_counter()
        try:
            result = self.synthesizer.synthesize(text, path, opts)
            elapsed = perf_counter() - started
            if self.database is not None and job_id:
                with self.database.session() as session:
                    from .repositories import JobRepository
                    JobRepository(session).mark_completed(job_id, result.path, elapsed)
            return SynthesisResult(result.path, result.voice_id, job_id)
        except Exception as exc:
            if self.database is not None and job_id:
                with self.database.session() as session:
                    from .repositories import JobRepository
                    JobRepository(session).mark_failed(job_id, str(exc))
            raise
