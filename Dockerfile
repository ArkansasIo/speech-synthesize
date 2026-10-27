FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends espeak-ng libespeak1 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src ./src
COPY config ./config
COPY database ./database

RUN pip install --upgrade pip \
    && pip install ".[api]"

RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /app/output \
    && chown -R appuser:appuser /app

USER appuser
EXPOSE 8000

CMD ["speech-synthesize-api"]
