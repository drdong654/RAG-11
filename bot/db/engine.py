# bot/db/engine.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

def make_sessionmaker(dsn: str):
    engine = create_async_engine(dsn)
    return engine, async_sessionmaker(
        engine,
        expire_on_commit=False
    )

def create_engine(dsn: str):
    return create_async_engine(dsn)