import asyncio
import hashlib
import json
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv

from keyboard import command_keyboard, main_keyboard


load_dotenv()

TOKEN = os.getenv("TOKEN")
DB_FILE = Path("BD.json")

router = Router()


def load_users():
    if not DB_FILE.exists():
        return {"users": []}

    with open(DB_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"users": []}


def save_users(data):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def is_registered(user_id: int) -> bool:
    users_data = load_users()
    return any(user["user_id"] == user_id for user in users_data["users"])


class RegisterState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_password = State()


async def show_start(message: Message):
    await message.answer(
        text=(
            "Hi, nice to meet you!\n"
            "Welcome to school, my friend!\n\n"
            "Use the buttons below 👇"
        ),
        reply_markup=main_keyboard,
    )
    await message.answer(
        text="Choose comand👇",
        reply_markup=command_keyboard(),
    )


async def show_help(message: Message):
    await message.answer(
        text=(
            "/start - start bot\n"
            "/help - show commands\n"
            "/profile - show profile\n"
            "/login - register user"
        )
    )


async def show_profile(message: Message):
    user_id = message.from_user.id

    if is_registered(user_id):
        await message.answer("Welcome, home!")
    else:
        await message.answer("Please, log in!")


@router.message(Command("start"))
async def start_command(message: Message):
    await show_start(message)


@router.message(F.text == "start")
async def start_button(message: Message):
    await show_start(message)


@router.message(Command("help"))
async def show_command(message: Message):
    await show_help(message)


@router.message(F.text == "help")
async def help_button_text(message: Message):
    await show_help(message)


@router.message(Command("profile"))
async def profile_command(message: Message):
    await show_profile(message)


@router.message(F.text == "profile")
async def profile_button_text(message: Message):
    await show_profile(message)


@router.message(Command("login"))
async def login_command(message: Message, state: FSMContext):
    await state.set_state(RegisterState.waiting_for_phone)
    await message.answer("Enter your phone number:")


@router.message(F.text == "login")
async def login_button_text(message: Message, state: FSMContext):
    await state.set_state(RegisterState.waiting_for_phone)
    await message.answer("Enter your phone number:")


@router.message(RegisterState.waiting_for_phone)
async def get_phone(message: Message, state: FSMContext):
    phone = message.text.strip()

    if len(phone) < 7:
        await message.answer("Enter a valid phone number.")
        return

    await state.update_data(phone_number=phone)
    await state.set_state(RegisterState.waiting_for_email)
    await message.answer("Now enter your email:")


@router.message(RegisterState.waiting_for_email)
async def get_email(message: Message, state: FSMContext):
    email = message.text.strip()

    if "@" not in email:
        await message.answer("Enter a valid email.")
        return

    await state.update_data(email=email)
    await state.set_state(RegisterState.waiting_for_password)
    await message.answer("Now enter your password:")


@router.message(RegisterState.waiting_for_password)
async def get_password(message: Message, state: FSMContext):
    password = message.text.strip()

    if not password:
        await message.answer("Password cannot be empty.")
        return

    data = await state.get_data()
    phone_number = data["phone_number"]
    email = data["email"]
    password_hash = hash_password(password)

    users_data = load_users()

    if any(user["user_id"] == message.from_user.id for user in users_data["users"]):
        await message.answer("You are already registered.")
        await state.clear()
        return

    users_data["users"].append(
        {
            "user_id": message.from_user.id,
            "phone_number": phone_number,
            "email": email,
            "password_hash": password_hash,
        }
    )

    save_users(users_data)

    await message.answer("Registration completed!", reply_markup=main_keyboard)
    await state.clear()


@router.callback_query(F.data == "profile")
async def profile_inline_button(callback: CallbackQuery):
    await show_profile(callback.message)
    await callback.answer()


@router.callback_query(F.data == "help")
async def help_inline_button(callback: CallbackQuery):
    await show_help(callback.message)
    await callback.answer()


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен...")
