import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

from keyboard import main_keyboard, command_keyboard, contact_keyboard


load_dotenv()

TOKEN = os.getenv("TOKEN")

users = [1234, 5678]


dp = Dispatcher()

@dp.message(Command("start"))
async def start(message:Message):
    await message.answer(
        text="Hi, nice to meet you!\n"
            "Welcome to school, my friend!\n",
        reply_markup=main_keyboard
    )
    await message.answer(
        "Choose command:",
        reply_markup=command_keyboard()
    )

@dp.message(Command("help"))
async def help(message:Message):
    await message.answer(
        text="/start - it is START bot function\n"
        "/help - these are the commands the bot knows"
    )
    

@dp.message(Command("profile"))
async def myprofile(message: Message):
    user_id = message.from_user.id

    if user_id in users:
        await message.answer("Welcome, home!")
    else:
        await message.answer("Please, log in!")

@dp.callback_query(F.data == "profile")
async def profile_button(callback):
    await callback.message.answer("Your profile")
    await callback.answer()


@dp.message(Command("login"))
async def login (message:Message):
    phone = message.contact.phone_number
    if message.contact:
        await message.answer(f"Your phone number: {phone}")
    else:
        await message.answer("No result!")

@dp.message(F.contact)
async def get_contact(message: Message):
    phone = message.contact.phone_number
    await message.answer(f"Your phone number: {phone}")







async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен...")

