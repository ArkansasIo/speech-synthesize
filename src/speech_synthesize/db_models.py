"""SQLAlchemy persistence models matching database/schema.sql."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, BigInteger, Boolean, DateTime, Float, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.mysql import LONGTEXT


class Base(DeclarativeBase):
    pass


class VoiceRecord(Base):
    __tablename__ = "voices"
    __table_args__ = (UniqueConstraint("backend", "voice_id", name="uq_voice_backend_id"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    backend: Mapped[str] = mapped_column(String(64), nullable=False)
    voice_id: Mapped[str] = mapped_column(String(512), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    language: Mapped[str] = mapped_column(String(32), default="en-US", nullable=False)
    gender: Mapped[str | None] = mapped_column(String(32))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    metadata_json: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class SynthesisJobRecord(Base):
    __tablename__ = "synthesis_jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    backend: Mapped[str] = mapped_column(String(64), nullable=False)
    text_content: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    language: Mapped[str] = mapped_column(String(32), default="en-US", nullable=False)
    voice_id: Mapped[str | None] = mapped_column(String(512))
    rate: Mapped[int] = mapped_column(Integer, default=180, nullable=False)
    volume: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    output_format: Mapped[str] = mapped_column(String(16), default="wav", nullable=False)
    output_path: Mapped[str | None] = mapped_column(String(1024))
    status: Mapped[str] = mapped_column(String(16), default="queued", nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text)
    duration: Mapped[float | None] = mapped_column("duration_seconds", Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
