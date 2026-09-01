import re
from typing import Optional

from sqlalchemy.exc import IntegrityError

from bot.db.repositories.users import UserRepository


class UserStorage:
    def __init__(self, sessionmaker):
        self._sessionmaker = sessionmaker

    async def is_registered(self, user_id: int) -> bool:
        async with self._sessionmaker() as session:
            return await UserRepository(session).is_registered(user_id)

    async def email_exists(self, email: str) -> bool:
        async with self._sessionmaker() as session:
            return await UserRepository(session).email_exists(email)

    async def add_user(self, user_data: dict) -> None:
        async with self._sessionmaker() as session:
            await UserRepository(session).add_user(user_data)


class RegistrationService:
    def __init__(self, storage: UserStorage):
        self.storage = storage

    def normalize_phone(self, phone: str) -> str:
        digits = "".join(character for character in phone if character in "0123456789")
        return f"+{digits}"

    def normalize_email(self, email: str) -> str:
        return email.strip().lower()

    def validate_phone(self, phone: str) -> Optional[str]:
        if not re.fullmatch(r"\+?[0-9\s()-]+", phone):
            return "Invalid phone number. Must contain only digits and common separators."
        digits = self.normalize_phone(phone).removeprefix("+")
        if not 10 <= len(digits) <= 15:
            return "Invalid phone number. Must be between 10 and 15 digits."
        return None

    def validate_email(self, email: str) -> Optional[str]:
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return "Invalid email address."
        return None

    async def register(
        self,
        user_id: int,
        phone: str,
        email: str,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> str:
        if await self.storage.is_registered(user_id):
            return "You are already registered."

        phone_error = self.validate_phone(phone)
        if phone_error:
            return phone_error

        normalized_email = self.normalize_email(email)
        email_error = self.validate_email(normalized_email)
        if email_error:
            return email_error

        normalized_phone = self.normalize_phone(phone)
        if await self.storage.email_exists(normalized_email):
            return "This email is already registered."

        try:
            await self.storage.add_user({
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": normalized_phone,
                "email": normalized_email,
            })
        except IntegrityError:
            return "This email is already registered."

        return "Registration completed! Welcome aboard."
