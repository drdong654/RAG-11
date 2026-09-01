# api/main.py
from contextlib import asynccontextmanager
from datetime import datetime
import os
import secrets

from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict
from dotenv import load_dotenv

from bot.db.engine import make_sessionmaker, init_models
from bot.db.repositories.users import UserRepository

from sqladmin import Admin
from api.admin import UserAdmin

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Add DATABASE_URL to environment variables.")

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise RuntimeError("API_TOKEN is not set. Add API_TOKEN to environment variables.")

engine, Session = make_sessionmaker(DATABASE_URL)
bearer_scheme = HTTPBearer(auto_error=False, scheme_name="OperatorBearer")


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    telegram_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    created_at: datetime


class ErrorResponse(BaseModel):
    detail: str


async def require_operator(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
):
    if (
        credentials is None
        or credentials.scheme.lower() != "bearer"
        or not secrets.compare_digest(credentials.credentials, API_TOKEN)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token.",
            headers={"WWW-Authenticate": "Bearer"},
        )


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

@app.get(
    "/users",
    response_model=list[UserResponse],
    responses={401: {"model": ErrorResponse}},
)
async def list_users(
    _operator: None = Depends(require_operator),
    users: UserRepository = Depends(get_users),
):
    return await users.list_all()

@app.get(
    "/users/{telegram_id}",
    response_model=UserResponse,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def get_user(
    telegram_id: int,
    _operator: None = Depends(require_operator),
    users: UserRepository = Depends(get_users),
):
    user = await users.get_by_telegram_id(telegram_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
