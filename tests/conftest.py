import os

import pytest_asyncio

from bot.db.repositories.users import UserRepository
from bot.db.engine import make_sessionmaker
from bot.db.models import Base
from dotenv import load_dotenv
from services import UserStorage

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL: 
    raise RuntimeError("TEST_DATABASE_URL is not set")

#Создаём UserRepository с тестовой сессией БД
@pytest_asyncio.fixture
async def user_repository(db_session):
    repository = UserRepository(db_session)
    yield repository


@pytest_asyncio.fixture
async def user_storage():
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
    
