from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="start")],
        [KeyboardButton(text="help")],
        [KeyboardButton(text="profile")], [KeyboardButton(text="login")],
    ],
    resize_keyboard=True
)

contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Send contact", request_contact=True)]
    ],
    resize_keyboard=True
)

def command_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="profile", callback_data="profile")],
            [InlineKeyboardButton(text="help", callback_data="help")],
        ]
    )