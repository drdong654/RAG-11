# RAG-11

## What matters

- This repo is a tiny aiogram bot, not a full RAG app yet. The only live app files are `main.py` and `keyboard.py`; `issues(2).md` is a task list, not implemented architecture.
- `main.py` is the real entrypoint. It calls `load_dotenv()`, reads `TOKEN` from the environment, creates the `Bot` inside `main()`, and starts polling with `asyncio.run(main())`.
- Handler registration happens via decorators on the module-level `dp = Dispatcher()`. If you refactor imports or split files, preserve import-time registration.

## Commands

- Run locally: `python main.py`
- Fast syntax check: `python -m py_compile main.py keyboard.py`

## Dependency and config drift

- `pyproject.toml` declares `requires-python = ">=3.14"` but does not list any dependencies, even though the code imports `aiogram` and `python-dotenv`. Do not assume environment setup is reproducible from project metadata alone.
- `amvera.yml` does not match the current app layout: it expects `requirements.txt`, runs `__main__.py`, and targets Python toolchain `3.11`. Treat it as stale until updated alongside deployment work.

## Verification limits

- There is no test suite, lint config, typecheck config, or CI workflow in the repo.
- The most reliable focused verification is `python -m py_compile main.py keyboard.py`; running `python main.py` also requires a valid Telegram bot `TOKEN` in `.env` or the process environment.
