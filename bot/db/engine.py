# bot/db/engine.py
import asyncio

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.db.models import Base

def make_sessionmaker(dsn: str):
    engine = create_async_engine(dsn)
    return engine, async_sessionmaker(
        engine,
        expire_on_commit=False
    )

def create_engine(dsn: str):
    return create_async_engine(dsn)

async def init_models(engine, retries: int = 5, delay: float = 1.0):
    # depends_on only waits for the container to start, not for Postgres to
    # be ready to accept connections, so the first attempt can lose that race.
    for attempt in range(1, retries + 1):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            return
        except (OperationalError, ConnectionRefusedError):
            if attempt == retries:
                raise
            await asyncio.sleep(delay)