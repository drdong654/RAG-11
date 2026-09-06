# api/main.py
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv

from bot.db.engine import make_sessionmaker, init_models
from bot.db.repositories.users import UserRepository

from sqladmin import Admin
from api.admin import UserAdmin

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Add DATABASE_URL to environment variables.")

engine, Session = make_sessionmaker(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models(engine)
    yield


app = FastAPI(title="vildly-rag-bot API", lifespan=lifespan)


admin = Admin(app, engine)
admin.add_view(UserAdmin)

async def get_users():
    async with Session() as session:
        yield UserRepository(session)             # тот же репозиторий, что у бота

@app.get("/users")
async def list_users(users: UserRepository = Depends(get_users)):
    return await users.list_all()

@app.get("/users/{telegram_id}")
async def get_user(telegram_id: int, users: UserRepository = Depends(get_users)):
    user = await users.get_by_telegram_id(telegram_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
