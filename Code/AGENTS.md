# RAG-11

aiogram Telegram bot. Python 3.14.

## Setup & Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install aiogram python-dotenv
```

Requires `TOKEN` in `.env` at repo root (already present).

```bash
python main.py
```

## Project structure

| File | Purpose |
|------|---------|
| `main.py` | Entrypoint — bot init, dispatcher setup, handlers |
| `keyboard.py` | Keyboard layouts (reply + inline) |

## Known issues (code has bugs)

- `dp = Dispatcher` missing `()` — object not instantiated
- `F` (magic filter) used in `callback_query` without `from aiogram import F`
- `main_keyboard` on line 25 is dangling (not attached to any message call)
- `message.from_user_id` should be `message.from_user.id`
- `message.contact.phone_number` is read but unused
- `command_keyboard()` in `keyboard.py` is defined but never called

## Project is incomplete

No tests, no CI, no lint/typecheck config. Fix bugs and add features as needed.
