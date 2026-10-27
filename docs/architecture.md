# Architecture

- `cli.py` parses text/file input and synthesis options.
- `engine.py` validates input and delegates audio rendering to `pyttsx3`.
- `api.py` provides an optional FastAPI adapter that generates server-side filenames.
- `tests/` verifies validation and API request contracts.

## Data flow
1. The caller supplies text and options.
2. The engine validates text length, rate, and volume.
3. The installed voice driver renders an audio file.
4. The caller receives the output path or API job metadata.

## Extension strategy
Add alternative local or cloud backends behind a common interface, normalize provider failures to `SynthesisError`, and store provider credentials in environment variables or a secret manager. Avoid logging raw speech text by default.

## Deployment security
The API is designed for local development. Before exposing it remotely, add authentication, quotas, rate limits, retention controls, request-size limits, and monitoring. Do not let clients choose arbitrary output paths.
