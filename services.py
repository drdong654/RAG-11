from typing import Optional

from bot.db.repositories.users import UserRepository


class UserStorage:
    def __init__(self, sessionmaker):
        self._sessionmaker = sessionmaker

    async def is_registered(self, user_id: int) -> bool:
        async with self._sessionmaker() as session:
            return await UserRepository(session).is_registered(user_id)


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

    async def register(
        self,
        user_id: int,
        phone: str,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> str:
        if await self.storage.is_registered(user_id):
            return "You are already registered."


        await self.storage.add_user({
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone,
        })

        return "Registration completed! Welcome aboard."
