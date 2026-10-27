"""Persistence repositories for voices and synthesis jobs."""
from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from .db_models import SynthesisJobRecord, VoiceRecord
from .models import SynthesisOptions, VoiceInfo


class VoiceRepository:
    def __init__(self, session: Session):
        self.session = session

    def upsert(self, voice: VoiceInfo, backend: str = "pyttsx3", language: str = "en-US") -> VoiceRecord:
        record = self.session.scalar(
            select(VoiceRecord).where(VoiceRecord.backend == backend, VoiceRecord.voice_id == voice.id)
        )
        if record is None:
            record = VoiceRecord(backend=backend, voice_id=voice.id, name=voice.name)
            self.session.add(record)
        record.name = voice.name
        record.language = language or (voice.languages[0] if voice.languages else "en-US")
        record.gender = voice.gender
        record.enabled = True
        return record

    def list_enabled(self, language_prefix: str | None = "en") -> list[VoiceRecord]:
        stmt = select(VoiceRecord).where(VoiceRecord.enabled.is_(True)).order_by(VoiceRecord.name)
        if language_prefix:
            stmt = stmt.where(VoiceRecord.language.like(f"{language_prefix}%"))
        return list(self.session.scalars(stmt))


class JobRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, text: str, options: SynthesisOptions, backend: str) -> SynthesisJobRecord:
        record = SynthesisJobRecord(
            id=str(uuid4()),
            backend=backend,
            text_content=text,
            language=options.language or "en-US",
            voice_id=options.voice_id,
            rate=options.rate,
            volume=options.volume,
            output_format=options.output_format,
            status="queued",
        )
        self.session.add(record)
        self.session.flush()
        return record

    def mark_running(self, job_id: str) -> None:
        record = self.get(job_id)
        if record:
            record.status = "running"
            record.started_at = datetime.now(timezone.utc).replace(tzinfo=None)

    def mark_completed(self, job_id: str, output_path: str, duration: float | None = None) -> None:
        record = self.get(job_id)
        if record:
            record.status = "completed"
            record.output_path = output_path
            record.duration = duration
            record.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)

    def mark_failed(self, job_id: str, error: str) -> None:
        record = self.get(job_id)
        if record:
            record.status = "failed"
            record.error_message = error[:65535]
            record.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)

    def get(self, job_id: str) -> SynthesisJobRecord | None:
        return self.session.get(SynthesisJobRecord, job_id)
