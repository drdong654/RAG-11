# Vildly Agent Notes

## Current System

- Runtime consists of an aiogram 3 Telegram bot, FastAPI/SQLAdmin API, and PostgreSQL 16 with pgvector.
- Bot and API are separate processes sharing SQLAlchemy models, repositories, and one database.
- RAG, Discord, hybrid search, and MCP are roadmap items. `AI/RAG.py` is incomplete; `AI/ASK.py` is empty.
- Run commands from repository root: the bot loads images by relative path and imports root-level `services.py`.

## Entry Points

- Bot: `uv run --no-sync python -m bot.main`.
- API: `uv run --no-sync uvicorn api.main:app --host 0.0.0.0 --port 8000`.
- Dockerfile default: `scripts/start.sh`, starting API in background and bot in foreground.
- Compose overrides the image command and runs `db`, `api`, and `bot` separately.
- Amvera delegates to `Dockerfile`; `amvera.yml` has no separate Python entry point.

## Architecture

- `bot/main.py`: router, handlers, registration FSM, polling startup.
- `bot/keyboard.py`: Telegram reply and inline keyboards.
- `services.py`: `RegistrationService` and session-owning `UserStorage`.
- `bot/db/models.py`: SQLAlchemy models.
- `bot/db/engine.py`: async engine/session factory and startup table initialization.
- `bot/db/repositories/users.py`: PostgreSQL-specific user persistence.
- `api/main.py`: FastAPI app, user endpoints, SQLAdmin registration.
- `api/admin.py`: SQLAdmin user view.
- `tests/unit/`: service tests using in-memory storage.
- `tests/integration/`: PostgreSQL repository tests.

Registration flow: aiogram handler -> `RegistrationService` -> `UserStorage` -> `UserRepository` -> PostgreSQL.

## Environment

- `TOKEN`: required by `bot/main.py` at import time.
- `DATABASE_URL`: async SQLAlchemy DSN required by bot and API.
- `TEST_DATABASE_URL`: optional dedicated PostgreSQL database for integration tests.
- `EMBEDDING`: read only by incomplete `AI/RAG.py`.

Never commit real secrets. Compose credentials are development-only values.

## Commands

```bash
uv sync --frozen
uv run --no-sync python -m bot.main
uv run --no-sync uvicorn api.main:app --host 0.0.0.0 --port 8000
docker compose build
docker compose up
.venv-linux/bin/python -m pytest
.venv-linux/bin/python -m pytest tests/unit/test_registration.py
.venv-linux/bin/python -m pytest tests/integration/test_user_repository.py
```

Windows: `.venv\Scripts\python.exe -m pytest`.

Unit-only Linux run without PostgreSQL:

```bash
TEST_DATABASE_URL= .venv-linux/bin/python -m pytest -p no:cacheprovider -q
```

## Database and Test Safety

- Integration fixtures create and drop all tables in `TEST_DATABASE_URL`. Never point it at development or production data.
- `UserRepository` uses PostgreSQL `insert`; it is not database-agnostic.
- Schema creation uses `Base.metadata.create_all()`. Alembic is not configured.
- Compose `depends_on` does not wait for database health. `init_models()` retries five times.
- Unit tests cover registration rules, Telegram contact ownership, course callbacks, lesson placeholder, and Back navigation.
- Integration tests cover user upsert/read and skip without `TEST_DATABASE_URL`.
- No API, admin, migration, security, or RAG tests exist.

## Known Gaps

- `User.email` is declared unique in the model, but existing databases still need an Alembic migration to receive the constraint.
- `/users`, `/users/{telegram_id}`, and SQLAdmin expose PII without authentication.
- Compose has hardcoded development DB credentials and no healthcheck.
- Non-Python course buttons intentionally return a development placeholder.
- `Book a Lesson` intentionally returns a development placeholder for registered users.
- Inline `profile` and `help` callbacks have no matching current inline buttons.
- API returns ORM objects without explicit response schemas.
- API lifespan does not dispose engine on shutdown.
- `aiosqlite`, `data/users.db`, and SQLite documentation are legacy; active persistence is PostgreSQL.

## Change Guidelines

- Keep changes scoped; do not refactor adjacent code without approval.
- Preserve async database access and add tests for changed behavior.
- Do not change schema without a migration plan.
- Never expose tokens, credentials, phone numbers, or emails in logs or unauthenticated responses.
- Distinguish implemented behavior from roadmap intent.
- Update this file and `docs/1.md`/`docs/2.md` when architecture or scope changes.
