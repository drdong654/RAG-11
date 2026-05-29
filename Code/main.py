import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from keyboard import main_keyboard
from aiogram import F
from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.getenv("TOKEN")

users = [1234, 5678]


dp = Dispatcher()

@dp.message(Command("start"))
async def start(message:Message):
    await message.answer(
        "Hi, nice to meet you!\n",
        "Welcome to shool? my friend!\n",
        reply_markup=main_keyboard)
    

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


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












if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен...")

