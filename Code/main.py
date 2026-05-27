import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.getenv("TOKEN")

ID = {

}


dp = Dispatcher

@dp.message(Command("start"))
async def start(message:Message):
    await message.answer(
        "Hi, nice to meet you!\n", 
        "Welcome to shool? my friend!\n",)

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


@dp.message(Command("My proffile"))
async def MyProffile(message:Message):
    await message.answer("Do you have any account?")











if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен...")

