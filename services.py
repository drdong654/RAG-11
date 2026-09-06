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

    def validate_phone(self, phone: str) -> Optional[str]:
        digits = phone.removeprefix("+")
        if not digits.isdigit() or len(digits) < 10:
            return "Invalid phone number. Must be at least 10 digits."
        return None

    def validate_email(self, email: str) -> Optional[str]:
        if "@" not in email or "." not in email:
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

        normalized_email = email.strip().lower()
        if await self.storage.email_exists(normalized_email):
            return "This email is already registered."

        try:
            await self.storage.add_user({
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone,
                "email": normalized_email,
            })
        except IntegrityError:
            return "This email is already registered."

        return "Registration completed! Welcome aboard."
