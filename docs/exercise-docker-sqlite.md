# Exercise: Docker Fundamentals + Persistent Storage with SQLite

A hands-on exercise using this repo's actual `Dockerfile`, `compose.yaml`, and
`services.py`. Nothing here is hypothetical — every command runs against the
real bot.

**You'll need:** Docker Desktop running, a terminal in this repo, and about
60–90 minutes.

---

## Part 1 — Understanding Docker

### 1.1 The five concepts you actually need

| Term | What it is |
|---|---|
| **Image** | A frozen filesystem snapshot: your code + a Python runtime + installed deps. Built once, run many times. |
| **Container** | A running instance of an image. Like a process, but with its own filesystem view. |
| **Dockerfile** | The recipe for building an image — a list of steps ("start from this base, copy these files, run this command"). |
| **Volume** | Storage that lives *outside* the container's filesystem, so it survives when the container is removed or rebuilt. |
| **Compose** | A YAML file (`compose.yaml`) that describes one or more containers + their volumes/networks, so you don't have to type long `docker run` commands. |

### 1.2 Read your own Dockerfile

Open `Dockerfile` in this repo and answer these before moving on (no wrong
answers graded here — this is to check your mental model):

1. `FROM python:3.13-slim` — why start from an existing image instead of a bare
   Linux image?
2. `COPY requirements.txt .` happens *before* `COPY . .`. Why copy just one
   file first instead of copying everything in one step?
3. `RUN useradd ... && chown -R appuser:appuser /app` then `USER appuser` —
   what would break if you deleted the `chown` line but kept `USER appuser`?
   (Try it if you're not sure — that's what Part 2 will build on.)

<details>
<summary>Hints (expand after you've tried answering)</summary>

1. Building Python from scratch would take forever and be error-prone. The
   `-slim` variant is a trimmed-down Debian with Python preinstalled.
2. Docker caches each layer. If you `COPY . .` first, then *any* file change
   (even editing `keyboard.py`) invalidates the cache and forces a full
   `pip install` on every rebuild. Copying `requirements.txt` first means the
   slow `pip install` layer is only re-run when dependencies actually change.
3. `appuser` wouldn't own `/app`, so it couldn't write `BD.json` at runtime —
   you'd get a `PermissionError` the first time someone tries to register.
</details>

### 1.3 Build and run without Compose

Do this manually once so Compose doesn't feel like magic later.

```bash
# Build an image, tag it "exercise"
docker build -t vildly-bot:exercise .

# Run it, passing TOKEN directly instead of via .env
docker run --rm -e TOKEN=$(grep TOKEN .env | cut -d= -f2) vildly-bot:exercise
```

While it's running, open a **second terminal** and try:

```bash
docker ps                     # see the running container + its name
docker exec -it <name> sh     # get a shell inside the running container
whoami                        # inside the container — should print "appuser"
ls -la /app                   # see the copied files
exit
docker logs <name>            # see stdout from the bot process
```

Stop it with `Ctrl+C` in the first terminal, then confirm it's gone:

```bash
docker ps -a    # container should show "Exited"
docker rm <name>
```

**Checkpoint:** in one sentence, what's the difference between `docker build`
and `docker run`?

### 1.4 Now do the same thing with Compose

```bash
docker compose up --build -d   # build + start, detached
docker compose ps              # see status
docker compose logs -f         # follow logs (Ctrl+C to stop watching, container keeps running)
docker compose down            # stop and remove
```

**Checkpoint:** open `compose.yaml`. It's 12 lines and replaces the
`docker build` + `docker run -e TOKEN=... --rm ...` dance above. Name two
things Compose is doing for you that you'd otherwise have to remember to type
by hand.

---

## Part 2 — Persistent storage: SQLite + a Docker volume

### 2.1 First, reproduce the actual bug

Right now user data has a problem. Let's see it before fixing it.

```bash
docker compose up --build -d
```

In Telegram, message your bot and register (`/login` or whatever your
registration flow is) so `BD.json` gets created inside the container. Then:

```bash
docker compose down
docker compose up --build -d
```

Register again, or check — **your registration from before is gone.** Why?
Because `BD.json` is `.gitignore`d (never in the image) *and* not mounted as a
volume — it only ever exists inside the writable layer of a container that
Compose just deleted.

### 2.2 Why isn't SQLite "a microservice" the way Postgres would be?

Postgres/MySQL run as a long-lived **server process** that other containers
talk to over the network — that's a real separate service, and it earns its
own entry in `compose.yaml`. **SQLite has no server process.** It's a library
that reads/writes a single `.db` file directly from inside your bot's own
process. There's nothing to put in a second container.

What SQLite *does* need from Docker is the same thing `BD.json` needed and
didn't get: a place to live that survives `docker compose down`. That's a
**named volume**, not a second service.

### 2.3 Step 1 — add a named volume

Edit `compose.yaml` to mount a `/data` directory backed by a named volume:

```yaml
services:
  bot:
    build:
      context: .
      dockerfile: Dockerfile

    image: vildly-bot:latest
    container_name: vildly-bot

    restart: unless-stopped

    env_file:
      - .env

    volumes:
      - bot_data:/data

volumes:
  bot_data:
```

**Checkpoint:** run `docker compose up --build -d`, then
`docker volume ls | grep bot_data`. You should see it listed. This volume now
exists independently of any container.

### 2.4 Step 2 — migrate `UserStorage` from JSON to SQLite

Open `services.py`. `UserStorage` currently does `json.load`/`json.dump`
against a `Path`. Your job: keep the exact same **public interface**
(`is_registered`, `add_user`, `hash_password`) so `main.py` and
`RegistrationService` don't need to change at all — only the storage
mechanism underneath changes. This is the same reason the previous
JSON-backed class was worth extracting on its own (see git history: `Refactor:
extract UserStorage and RegistrationService into OOP classes`) — swapping the
storage engine should be a one-file change.

Use Python's built-in `sqlite3` (no new dependency needed). Skeleton to fill
in:

```python
import sqlite3
from pathlib import Path

class UserStorage:
    def __init__(self, db_file: Path = Path("/data/users.db")):
        self.db_file = db_file
        self._init_schema()

    def _init_schema(self) -> None:
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    phone_number TEXT,
                    email TEXT,
                    password_hash TEXT
                )
            """)

    def is_registered(self, user_id: int) -> bool:
        # TODO: SELECT 1 FROM users WHERE user_id = ?
        ...

    def add_user(self, user_data: dict) -> None:
        # TODO: INSERT INTO users (...) VALUES (...)
        ...

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()  # unchanged
```

Notes for filling in the TODOs:
- Always use `?` placeholders (`WHERE user_id = ?`, params as a tuple) — never
  f-string values into SQL. That's a SQL injection hole even in a toy bot.
- `sqlite3.connect(...)` as a context manager commits automatically on a clean
  exit.

### 2.5 Step 3 — point it at the volume, and prove persistence

The default path above (`/data/users.db`) already targets the mount point
from step 2.3. Rebuild and re-test the exact scenario from 2.1:

```bash
docker compose up --build -d
# register in Telegram
docker compose down
docker compose up --build -d
# check — are you still registered?
```

If yes, the volume did its job. You can also inspect the file directly
without going through Telegram:

```bash
docker compose exec bot sqlite3 /data/users.db "SELECT * FROM users;"
```

(If `sqlite3` isn't installed in the slim image, add it to the Dockerfile with
`RUN apt-get update && apt-get install -y --no-install-recommends sqlite3` —
optional, only needed for this kind of manual inspection.)

### 2.6 Stretch goals (optional)

- Add a `UNIQUE` constraint on `user_id` and handle the
  `sqlite3.IntegrityError` it raises if `add_user` is ever called twice for
  the same user — right now `RegistrationService.register` already checks
  `is_registered` first, but the DB layer shouldn't silently trust the caller.
- Back up the volume from the host: `docker run --rm -v vildly-rag-bot_bot_data:/data -v $(pwd):/backup alpine cp /data/users.db /backup/`
- Delete the volume (`docker volume rm vildly-rag-bot_bot_data`) and confirm
  the bot starts clean with an empty `users` table — this is what "wiping
  prod data" looks like, so it's worth seeing once deliberately.

---

## What you should walk away knowing

- The difference between an image and a container, and why layer order in a
  Dockerfile affects build speed.
- Why a container's filesystem is disposable by default, and volumes are the fix.
- Why SQLite is "just a file" from Docker's point of view, not a service —
  and when you'd actually reach for a real client-server database (Postgres) instead, which *would* get its own entry in `compose.yaml`.
