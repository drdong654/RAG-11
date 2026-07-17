import hashlib
import sqlite3
from pathlib import Path
from typing import Optional

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
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.execute(
                "SELECT 1 FROM users WHERE user_id = ?", (user_id,)
            )
            return cur.fetchone() is not None

    def add_user(self, user_data: dict) -> None:
        with sqlite3.connect(self.db_file) as conn:
            conn.execute(
                "INSERT INTO users (user_id, phone_number, email, password_hash) VALUES (?, ?, ?, ?)",
                (
                    user_data["user_id"],
                    user_data.get("phone_number"),
                    user_data.get("email"),
                    self.hash_password(user_data["password"]) if "password" in user_data else None,
                ),
            )

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()


class RegistrationService:
    def __init__(self, storage: UserStorage):
        self.storage = storage

    def validate_phone(self, phone: str) -> Optional[str]:
        if not phone.isdigit() or len(phone) < 10:
            return "Invalid phone number. Must be at least 10 digits."
        return None

    def validate_email(self, email: str) -> Optional[str]:
        if "@" not in email or "." not in email:
            return "Invalid email address."
        return None

    def validate_password(self, password: str) -> Optional[str]:
        if len(password) < 6:
            return "Password must be at least 6 characters."
        return None

    def register(self, user_id: int, phone: str, email: str, password: str) -> str:
        if self.storage.is_registered(user_id):
            return "You are already registered."

        self.storage.add_user({
            "user_id": user_id,
            "phone_number": phone,
            "email": email,
            "password": password,
        })
        return "Registration completed! Welcome aboard."