import hashlib
import json
from pathlib import Path
from typing import Optional


class UserStorage:
    """Отвечает только за чтение/запись BD.json."""

    def __init__(self, db_file: Path = Path("BD.json")):
        self.db_file = db_file

    def load(self) -> dict:
        if not self.db_file.exists():
            return {"users": []}
        with open(self.db_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"users": []}

    def save(self, data: dict) -> None:
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def is_registered(self, user_id: int) -> bool:
        data = self.load()
        return any (
            user.get("user_id") == user_id 
            for user in data.get("users", [])
        )

    def add_user(self, user_data: dict) -> None:
        data = self.load()
        data["users"].append(user_data)
        self.save(data)

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()


class RegistrationService:
    """Бизнес-логика регистрации (валидация + сохранение)."""

    def __init__(self, storage: UserStorage):
        self.storage = storage

    def is_registered(self, user_id: int) -> bool:
        return self.storage.is_registered(user_id)

    def validate_phone(self, phone: str) -> Optional[str]:
        """Возвращает None если ок, или строку с ошибкой."""
        if len(phone) < 7 or not phone.replace("+", "").isdigit():
            return "Enter a valid phone number."
        return None

    def validate_email(self, email: str) -> Optional[str]:
        if "@" not in email:
            return "Enter a valid email."
        return None

    def validate_password(self, password: str) -> Optional[str]:
        if not password:
            return "Password cannot be empty."
        return None

    def register(self, user_id: int, phone: str, email: str, password: str) -> str:
        """Возвращает сообщение для пользователя (успех/ошибка)."""
        if self.is_registered(user_id):
            return "You are already registered."

        user_data = {
            "user_id": user_id,
            "phone_number": phone,
            "email": email,
            "password_hash": self.storage.hash_password(password),
        }
        self.storage.add_user(user_data)
        return "Registration completed!"