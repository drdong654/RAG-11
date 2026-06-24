from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(
keyboard=[
    [KeyboardButton(text="Start")],
    [KeyboardButton(text="Help")],
    [KeyboardButton(text="Profile")],
    [KeyboardButton(text="Login")],
],
resize_keyboard=True
)

command_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Book a Lesson")],
        [KeyboardButton(text="Courses")],
        [KeyboardButton(text="Back")],
    ],
    resize_keyboard=True
)
def courses_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🐍 Python", callback_data="course_python")],
            [InlineKeyboardButton(text="⚙️ Backend", callback_data="course_backend")],
            [InlineKeyboardButton(text="🎨 Frontend", callback_data="course_frontend")],
            [InlineKeyboardButton(text="🤖 AI & RAG", callback_data="course_ai")],
            [InlineKeyboardButton(text="💬 Discord Bots", callback_data="course_discord")],
            [InlineKeyboardButton(text="📨 Telegram Bots", callback_data="course_telegram")],
        ]
    )