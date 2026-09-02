#!/bin/sh
set -e

uv run --no-sync uvicorn api.main:app --host 0.0.0.0 --port 8000 &
api_pid="$!"

uv run --no-sync python -m bot.main &
bot_pid="$!"

cleanup() {
    kill "$api_pid" "$bot_pid" 2>/dev/null || true
}

trap cleanup INT TERM EXIT

# /bin/sh is dash here, which has no `wait -n`, so poll until either
# process exits instead of silently running with only the other alive.
while kill -0 "$api_pid" 2>/dev/null && kill -0 "$bot_pid" 2>/dev/null; do
    sleep 1
done

exit 1
