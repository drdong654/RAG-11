from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from bot.db.models import User

class UserRepository:
    def __init__(self, session):
        self._session = session

    async def upsert(self, telegram_id, username, first_name, last_name=None):
        stmt = (
            insert(User)
            .values(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            .on_conflict_do_update(
                index_elements=["telegram_id"],
                set_={
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                },
            )
            .returning(User)
        )
        user = (await self._session.execute(stmt)).scalar_one()
        await self._session.commit()
        return user

    async def get_by_telegram_id(self, telegram_id):
        return await self._session.get(User, telegram_id)

    async def list_all(self):
        return list((await self._session.execute(select(User))).scalars())

    async def is_registered(self, telegram_id):
        user = await self.get_by_telegram_id(telegram_id)
        return user is not None and user.phone_number is not None


    async def add_user(self, user_data):
        stmt = (
            insert(User)
            .values(
                telegram_id=user_data["user_id"],
                username=user_data.get("username"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                phone_number=user_data.get("phone_number"),
            )
            .on_conflict_do_update(
                index_elements=["telegram_id"],
                set_={
                    "username": user_data.get("username"),
                    "first_name": user_data.get("first_name"),
                    "last_name": user_data.get("last_name"),
                    "phone_number": user_data.get("phone_number"),
                },
            )
        )
        await self._session.execute(stmt)
        await self._session.commit()
