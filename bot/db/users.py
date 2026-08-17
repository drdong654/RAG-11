# bot/db/repositories/users.py
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from bot.db.models import User

class UserRepository:
    def __init__(self, session):
        self._session = session

    async def upsert(self, telegram_id, username, first_name):
        stmt = (
            insert(User)
            .values(telegram_id=telegram_id, username=username, first_name=first_name)
            .on_conflict_do_update(
                index_elements=["telegram_id"],
                set_={"username": username, "first_name": first_name, "last_name": None, "phoene_number": None, "email": None},
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