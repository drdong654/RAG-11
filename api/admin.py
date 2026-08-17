# api/admin.py
from sqladmin import Admin, ModelView
from bot.db.models import User

class UserAdmin(ModelView, model=User):
    column_list = [User.telegram_id, User.username, User.first_name, User.created_at]
    name = "Пользователь"
    name_plural = "Пользователи"