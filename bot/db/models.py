# bot/db/models.py
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    phone_number: Mapped[str | None]
    email: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


