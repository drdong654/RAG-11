# api/main.py
from fastapi import FastAPI, Depends, HTTPException
from bot.db.engine import make_sessionmaker
from bot.db.users import UserRepository
import os

from sqladmin import Admin
from api.admin import UserAdmin

engine, Session = make_sessionmaker(DATABASE_URL)
app = FastAPI(title="vildly-rag-bot API")


admin = Admin(app, engine)
admin.add_view(UserAdmin)

DATABASE_URL = os.getenv("DATABASE_URL")

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