# Speech Synthesize

A Python text-to-speech application with a local `pyttsx3` backend, English-language defaults, CLI, FastAPI service, MySQL job/voice persistence, Docker deployment, tests, and CI.

## Features

- Local speech synthesis through `pyttsx3`.
- English-first locale validation (`en-US` by default).
- System voice discovery and English voice synchronization.
- WAV output with safe server-generated filenames.
- FastAPI HTTP API with OpenAPI documentation.
- Optional MySQL 8.4 persistence for voices and synthesis jobs.
- Docker Compose stack for MySQL + API.
- SQLAlchemy connection pooling and transaction management.
- GitHub Actions CI across Python 3.11, 3.12, and 3.13.

## Requirements

- Python 3.11+
- A speech engine supported by `pyttsx3`.
- Windows: SAPI5 is normally available.
- Linux: install `espeak-ng`.
- MySQL 8.x only when database persistence is enabled.

## Install

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
# macOS/Linux
# source .venv/bin/activate
python -m pip install -e ".[api,dev]"
```

## CLI

```bash
speech-synthesize "Hello world"
speech-synthesize "Hello world" --output output/hello.wav
speech-synthesize --input samples/hello.txt --output output/hello.wav
speech-synthesize --list-voices
```

Database administration commands require MySQL environment variables:

```bash
speech-synthesize --db-health
speech-synthesize --sync-voices
```

## MySQL

Create the schema:

```bash
mysql -u root -p < database/schema.sql
```

Set the application password without putting it in source control:

```bash
# PowerShell
$env:SPEECH_DB_PASSWORD = "your-password"
$env:SPEECH_DB_ENABLED = "true"
```

The database stores voice metadata and synthesis job history. Audio files remain on the filesystem; MySQL stores their paths rather than binary audio data.

See `config/mysql.toml`, `database/README.md`, and `.env.example` for connection settings.

## Docker

Start MySQL and the API together:

```bash
docker compose up --build
```

The API is then available at `http://127.0.0.1:8000/docs`.

## HTTP API

Start locally:

```bash
speech-synthesize-api
```

Endpoints:

- `GET /health`
- `GET /v1/voices`
- `POST /v1/synthesize`
- `GET /v1/jobs/{job_id}` when MySQL persistence is enabled

Example request:

```json
{
  "text": "Hello from Speech Synthesize.",
  "language": "en-US",
  "rate": 180,
  "volume": 1.0
}
```

Do not expose the development API directly to the public internet without authentication, authorization, rate limiting, request quotas, output retention controls, and operational monitoring.

## Architecture

```text
CLI / FastAPI
     |
 SpeechService
     |
 SpeechSynthesizer
     |
 Backend Registry
     +---- pyttsx3 / SAPI5 / eSpeak
     |
     +---- optional SQLAlchemy Database
                 |
                 +---- voices
                 +---- synthesis_jobs
                 +---- application_settings
```

## Development

```bash
ruff check src tests
pytest
```

## Project tree

```text
speech-synthesize/
├── .github/workflows/ci.yml
├── config/
│   ├── default.toml
│   └── mysql.toml
├── database/
│   ├── README.md
│   └── schema.sql
├── docs/architecture.md
├── samples/hello.txt
├── src/speech_synthesize/
│   ├── __init__.py
│   ├── __main__.py
│   ├── api.py
│   ├── cli.py
│   ├── config.py
│   ├── database.py
│   ├── db_models.py
│   ├── db_sync.py
│   ├── engine.py
│   ├── exceptions.py
│   ├── management.py
│   ├── models.py
│   ├── repositories.py
│   ├── service.py
│   ├── voices.py
│   └── backends/
│       ├── base.py
│       └── pyttsx3_backend.py
├── tests/
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## License

No license has been selected. Add a `LICENSE` file before redistribution.
