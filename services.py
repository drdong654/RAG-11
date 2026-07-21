import os
import sqlite3
from pathlib import Path
from typing import Optional


class UserStorage:
    def __init__(self, db_file: Path | None = None):
        self.db_file = db_file or Path(os.getenv("DB_FILE", "data/users.db"))
        self._init_schema()

    def _init_schema(self) -> None:
        self.db_file.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_file) as conn:
            ### Telegram ID is the authentication source for this bot.
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    phone_number TEXT,
                    email TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self._ensure_schema(conn)

    def _ensure_schema(self, conn: sqlite3.Connection) -> None:
        ### Existing local databases may have been created by the old password schema.
        columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(users)")
        }
        migrations = {
            "username": "ALTER TABLE users ADD COLUMN username TEXT",
            "first_name": "ALTER TABLE users ADD COLUMN first_name TEXT",
            "last_name": "ALTER TABLE users ADD COLUMN last_name TEXT",
            "created_at": "ALTER TABLE users ADD COLUMN created_at TEXT",
            "updated_at": "ALTER TABLE users ADD COLUMN updated_at TEXT",
        }
        for column, statement in migrations.items():
            if column not in columns:
                conn.execute(statement)



    def is_registered(self, user_id: int) -> bool:
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.execute(
                "SELECT 1 FROM users WHERE user_id = ?", (user_id,)
            )
            return cur.fetchone() is not None

    def email_exists(self, email: str) -> bool:
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.execute(
                "SELECT 1 FROM users WHERE lower(email) = lower(?)", (email,)
            )
            return cur.fetchone() is not None

    def add_user(self, user_data: dict) -> None:
        with sqlite3.connect(self.db_file) as conn:
            conn.execute(
                """
                INSERT INTO users (
                    user_id, username, first_name, last_name, phone_number, email
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user_data["user_id"],
                    user_data.get("username"),
                    user_data.get("first_name"),
                    user_data.get("last_name"),
                    user_data.get("phone_number"),
                    user_data.get("email"),
                ),
            )


class RegistrationService:
    def __init__(self, storage: UserStorage):
        self.storage = storage

    def validate_phone(self, phone: str) -> Optional[str]:
        digits = phone.removeprefix("+")
        if not digits.isdigit() or len(digits) < 10:
            return "Invalid phone number. Must be at least 10 digits."
        return None

    def validate_email(self, email: str) -> Optional[str]:
        if "@" not in email or "." not in email:
            return "Invalid email address."
        return None

    def register(
        self,
        user_id: int,
        phone: str,
        email: str,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> str:
        if self.storage.is_registered(user_id):
            return "You are already registered."

        normalized_email = email.strip().lower()
        if self.storage.email_exists(normalized_email):
            return "This email is already registered."

        ### Registration stores Telegram profile data and email, not a bot password.
        try:
            self.storage.add_user({
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone,
                "email": normalized_email,
            })
        except sqlite3.IntegrityError:
            return "This email is already registered."

        return "Registration completed! Welcome aboard."
