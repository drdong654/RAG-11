from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)





main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Start")],

    ],
    resize_keyboard=True
)

def command_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text="Profile", callback_data="profile")]
        ]
        )