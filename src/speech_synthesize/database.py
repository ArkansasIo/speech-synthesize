"""Database connectivity and SQLAlchemy session management."""
from __future__ import annotations

import os
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    host: str = "127.0.0.1"
    port: int = 3306
    name: str = "speech_synthesize"
    user: str = "speech_app"
    password: str = ""
    charset: str = "utf8mb4"
    pool_size: int = 5
    max_overflow: int = 10
    connect_timeout: int = 10

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        return cls(
            host=os.getenv("SPEECH_DB_HOST", "127.0.0.1"),
            port=int(os.getenv("SPEECH_DB_PORT", "3306")),
            name=os.getenv("SPEECH_DB_NAME", "speech_synthesize"),
            user=os.getenv("SPEECH_DB_USER", "speech_app"),
            password=os.getenv("SPEECH_DB_PASSWORD", ""),
            charset=os.getenv("SPEECH_DB_CHARSET", "utf8mb4"),
            pool_size=int(os.getenv("SPEECH_DB_POOL_SIZE", "5")),
            max_overflow=int(os.getenv("SPEECH_DB_MAX_OVERFLOW", "10")),
            connect_timeout=int(os.getenv("SPEECH_DB_CONNECT_TIMEOUT", "10")),
        )

    @property
    def url(self) -> str:
        from urllib.parse import quote_plus
        return (
            f"mysql+pymysql://{quote_plus(self.user)}:{quote_plus(self.password)}"
            f"@{self.host}:{self.port}/{self.name}?charset={self.charset}"
        )


def create_database_engine(config: DatabaseConfig | None = None) -> Engine:
    cfg = config or DatabaseConfig.from_env()
    return create_engine(
        cfg.url,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_size=cfg.pool_size,
        max_overflow=cfg.max_overflow,
        connect_args={"connect_timeout": cfg.connect_timeout},
    )


class Database:
    """Small application database facade."""

    def __init__(self, engine: Engine | None = None, config: DatabaseConfig | None = None):
        self.engine = engine or create_database_engine(config)
        self.sessions = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)

    @contextmanager
    def session(self) -> Iterator[Session]:
        session = self.sessions()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def ping(self) -> bool:
        with self.engine.connect() as connection:
            return bool(connection.execute(text("SELECT 1")).scalar_one() == 1)

    def dispose(self) -> None:
        self.engine.dispose()
