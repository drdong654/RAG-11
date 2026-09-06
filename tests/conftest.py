import os

import pytest
import pytest_asyncio

from bot.db.repositories.users import UserRepository
from bot.db.engine import make_sessionmaker
from bot.db.models import Base
from dotenv import load_dotenv
from services import UserStorage

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


class InMemoryUserStorage:
    def __init__(self):
        self._users = {}

    async def is_registered(self, user_id: int) -> bool:
        return user_id in self._users

    async def email_exists(self, email: str) -> bool:
        return any(user["email"] == email for user in self._users.values())

    async def add_user(self, user_data: dict) -> None:
        self._users[user_data["user_id"]] = user_data

#Создаём UserRepository с тестовой сессией БД
@pytest_asyncio.fixture
async def user_repository(db_session):
    repository = UserRepository(db_session)
    yield repository


@pytest_asyncio.fixture
async def user_storage():
    if not TEST_DATABASE_URL:
        yield InMemoryUserStorage()
        return

    engine, Session = make_sessionmaker(TEST_DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield UserStorage(Session)

    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await engine.dispose()

#Создаем таблицу и открываем сессию БД
@pytest_asyncio.fixture
async def db_session():
    if not TEST_DATABASE_URL:
        pytest.skip("TEST_DATABASE_URL is not set")

    engine, Session = make_sessionmaker(TEST_DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        async with Session() as session:
            yield session

    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await engine.dispose()
    
