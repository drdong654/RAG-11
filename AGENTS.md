# RAG-11 Agent Notes

## Current Shape

- This is currently an aiogram 3 Telegram bot with a Postgres-backed data layer and a FastAPI read API, not the full RAG/Discord system described in the roadmap docs.
- Real app entrypoints: `bot/main.py` (Telegram polling) and `api/main.py` (FastAPI + SQLAdmin). `scripts/start.sh` runs both in one process for Docker/Amvera; `compose.yaml` runs them as separate `bot`/`api` services for local dev.
- Handler registration is module-level on `router`, then `main()` calls `init_models(engine)` before `dp.include_router(router)` + `dp.start_polling(bot)`.
- `services.py` (`UserStorage`, `RegistrationService`) is the storage-agnostic layer the bot and API both go through; the actual SQLAlchemy model and repository live in `bot/db/` (`models.py`, `engine.py`, `repositories/users.py`).
- `AI/` is only a stub (`RAG.py`, empty `ASK.py`) and is not wired into the bot.

## Commands

- Install/sync deps from the lockfile: `uv sync --frozen`.
- Run tests: `uv run python -m pytest` (or `.venv\Scripts\python.exe -m pytest` on Windows, see gotcha below).
- Run only the fast unit tests: `uv run python -m pytest tests/unit`.
- Run the Postgres integration test: needs `TEST_DATABASE_URL` pointed at a real database, e.g. `TEST_DATABASE_URL=postgresql+asyncpg://bot:test@localhost:5432/bot uv run python -m pytest tests/integration`. Without it, the integration test skips itself rather than failing.
- Quick syntax check: `uv run python -m py_compile bot/main.py bot/keyboard.py api/main.py services.py`.
- Run bot locally: `TOKEN=... DATABASE_URL=... uv run python -m bot.main` (both env vars are required, each raises immediately if missing).
- Run API locally: `DATABASE_URL=... uv run uvicorn api.main:app --reload`.
- Build/run everything together: `docker compose up --build` (services: `db`, `api`, `bot`).

## Local Environment Gotchas

- On Windows, `uv run pytest` can fail with `uv trampoline failed to canonicalize script path` in some workspace paths; prefer `.venv\Scripts\python.exe -m pytest` if that happens.
- On macOS (Apple Silicon), a bare local venv can be missing `greenlet` even though SQLAlchemy needs it for its async bridge — SQLAlchemy's dependency marker checks for `aarch64`, but macOS reports `platform_machine() == "arm64"` for the same chip, so the marker doesn't match and greenlet never installs. Linux (including inside Docker on an Apple Silicon host) reports `aarch64` and is unaffected; if you hit `ValueError: the greenlet library is required...` locally on Mac, `uv pip install greenlet` unblocks it.
- `TOKEN` and `DATABASE_URL` are both required; `bot/main.py` and `api/main.py` each raise immediately if either is missing.
- `image/start_img.png`, `image/help_img.png`, and `image/login_img.png` are loaded by relative paths from the repo root and will fail at runtime if missing or if the process is launched from another cwd.

## Database

- Postgres via SQLAlchemy async (`asyncpg`), not SQLite — the migration off file-based storage is complete.
- Nothing runs migrations; `init_models()` in `bot/db/engine.py` calls `Base.metadata.create_all` on startup (both from `bot/main.py`'s `main()` and from `api/main.py`'s FastAPI `lifespan`), with a short retry loop since `depends_on` in Compose only waits for the `db` container to start, not for Postgres to actually accept connections.
- `compose.yaml`'s `db` service currently has the Postgres password hardcoded (`POSTGRES_PASSWORD: 123`, matching literal `DATABASE_URL` values in `api`/`bot`) instead of read from `.env` — known, not yet cleaned up.

## Testing Notes

- `tests/unit/` covers `RegistrationService` against an in-memory fake storage — no database needed, runs everywhere.
- `tests/integration/` exercises the real `UserRepository` against Postgres and needs `TEST_DATABASE_URL`; it silently skips without one, so a green "unit" run alone doesn't prove the SQL layer works.
- CI (`.github/workflows/ci.yml`) has three jobs: `test` (the unit-covering matrix across ubuntu/windows/macos), `integration-test` (ubuntu-only, spins up a `pgvector/pgvector:pg16` service container and sets `TEST_DATABASE_URL`), and `deploy` (needs both, only runs on push to `main`, currently just `docker build`s the image with no push anywhere — real deployment is Amvera watching the repo directly, not this job).
- No linter, formatter, or typecheck config exists in this repo.

## Deployment Notes

- `pyproject.toml` requires Python `>=3.11`; the Docker image is `python:3.13-slim`.
- `amvera.yml` builds straight from `Dockerfile` and does not use `compose.yaml` at all — Amvera runs a single container via `scripts/start.sh` (bot + API together), so `DATABASE_URL`/`TOKEN` must be configured as environment variables in Amvera's own dashboard, not inferred from `.env` or `compose.yaml`.
- `scripts/start.sh` backgrounds both the API and the bot and exits (taking the container down) if either one dies, so a crashed API can't silently leave the container looking "healthy" with only half the app running.
