# RAG-11

## What matters

- This repo is a small aiogram 3 Telegram bot, not a full RAG app yet. `issues(2).md` is a roadmap, not implemented architecture.
- Three live app files: `main.py` (entrypoint), `keyboard.py` (reply/inline keyboards), `services.py` (user storage + registration logic against `BD.json`).
- `main.py` is the entrypoint: `load_dotenv()` -> reads `TOKEN` from env -> `asyncio.run(main())` -> aiogram polling.
- Handler registration uses a module-level `Router` included into the `Dispatcher` at startup. If you refactor imports or split files, preserve import-time handler registration.
- `BD.json` is the user database (gitignored). `UserStorage` reads/writes it; passwords are SHA-256 hashed.

## Commands

- Run locally: `python main.py`
- Quick syntax check: `python -m py_compile main.py keyboard.py services.py`
- Build Docker image: `docker compose build`
- Run in Docker: `docker compose up` (reads `.env` for `TOKEN`)

## Dependency and config drift

- `pyproject.toml` declares `requires-python = ">=3.11"` and lists `aiogram` + `python-dotenv` as dependencies.
- `uv.lock` exists (uv-compatible), but no `[build-system]` or `[tool.uv]` section in `pyproject.toml`.
- `amvera.yml` targets Python 3.11 with pip and expects `__main__.py` as entrypoint. The actual entrypoint is `main.py`. Treat `amvera.yml` as stale until deployment is updated.
- `Dockerfile` uses `python:3.13-slim` and installs from `pyproject.toml`.

## Verification limits

- No test suite, linter config, typecheck config, or CI workflow exists.
- `py_compile` is the only fast static check available.
- Running the bot requires a valid Telegram `TOKEN` in `.env` or the process environment.
- `image/` directory contains PNG assets referenced by `main.py` via relative paths; missing images will crash the bot at runtime.
