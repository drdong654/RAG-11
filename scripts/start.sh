#!/bin/sh
set -e

uv run --no-sync uvicorn api.main:app --host 0.0.0.0 --port 8000 &
api_pid="$!"

cleanup() {
    kill "$api_pid" 2>/dev/null || true
}

trap cleanup INT TERM EXIT

uv run --no-sync python -m bot.main
