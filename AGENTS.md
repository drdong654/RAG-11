# RAG-11 Agent Notes

## Current Shape

- This is currently an aiogram 3 Telegram bot, not the full RAG/Discord/Postgres system described in the roadmap docs.
- Real app entrypoint is `bot/main.py`; Docker runs `uv run --no-sync python -m bot.main`.
- Handler registration is module-level on `router`, then `main()` creates `Dispatcher()` and calls `dp.include_router(router)` before polling.
- `services.py` owns registration logic and SQLite user storage; `bot/main.py` imports it from the repo root, so run commands from the repo root.
- `AI/` is only a stub (`RAG.py`, empty `ASK.py`) and is not wired into the bot.

## Commands

- Install/sync deps from the lockfile: `uv sync --frozen`.
- Run tests with the local venv on Windows: `.venv\Scripts\python.exe -m pytest`.
- Run a single test file: `.venv\Scripts\python.exe -m pytest tests/test_registration.py`.
- Quick syntax check: `.venv\Scripts\python.exe -m py_compile bot/main.py bot/keyboard.py services.py`.
- Run bot locally after setting `TOKEN`: `.venv\Scripts\python.exe -m bot.main`.
- Build/run Docker: `docker compose build` and `docker compose up`.

## Local Environment Gotchas

- In this workspace path (`D:\it\Vildly bot`), `uv run pytest` failed with `uv trampoline failed to canonicalize script path`; prefer `.venv\Scripts\python.exe -m pytest` unless the path issue is fixed.
- `py` on this machine resolved to Python 3.14 without pytest; the checked local venv used Python 3.13 and passed the tests.
- Running the bot requires `TOKEN` in `.env` or the process environment; `bot/main.py` raises immediately if it is missing.
- User data defaults to `data/users.db`; Docker overrides `DB_FILE=/app/data/users.db` and persists it through the `vildly_data` named volume.
- `image/start_img.png`, `image/help_img.png`, and `image/login_img.png` are loaded by relative paths from the repo root and will fail at runtime if missing or if the bot is launched from another cwd.

## Testing Notes

- The current test suite only covers `RegistrationService`/`UserStorage`; tests use a pytest `tmp_path` SQLite DB and do not need `TOKEN`.
- No linter, formatter, typecheck config, CI workflow, or pre-commit config exists in this repo.

## Deployment Notes

- `pyproject.toml` requires Python `>=3.11`, while the Docker image is `python:3.13-slim`.
- `amvera.yml` delegates to `Dockerfile`; do not infer a separate Python entrypoint from it.
