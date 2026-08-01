import asyncio
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.types import FSInputFile
from dotenv import load_dotenv

from bot.keyboard import main_keyboard, command_keyboard, contact_keyboard, courses_keyboard
from services import UserStorage, RegistrationService

load_dotenv()

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN is not set. Add TOKEN to .env or environment variables.")

user_storage = UserStorage()
registration_service = RegistrationService(user_storage)
if not TOKEN:
    raise RuntimeError("TOKEN is not set. Add TOKEN to .env or environment variables.")

user_storage = UserStorage()
registration_service = RegistrationService(user_storage)

router = Router()

async def show_lesson_signup(message: Message):
    user_id = message.from_user.id

    if not user_storage.is_registered(user_id):
    if not user_storage.is_registered(user_id):
        await message.answer(
            "You must complete registration first.\n\n"
            "Use /login to continue."
        )
        return

    await message.answer(
        "Great! 🎓\n\n"
        "Please enter your preferred day and time for the lesson."
    )


class RegisterState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_email = State()


async def show_start(message: Message):
    photo = FSInputFile("image/start_img.png")
    reply_markup = command_keyboard if user_storage.is_registered(message.from_user.id) else main_keyboard
    reply_markup = command_keyboard if user_storage.is_registered(message.from_user.id) else main_keyboard

    await message.answer_photo(
        photo=photo,
        caption=(
            "Hi, nice to meet you!\n"
            "Welcome to school, my friend!\n\n"
            "Use the buttons below 👇"
        ),
        reply_markup=reply_markup,
    )


async def show_help(message: Message):
    photo = FSInputFile("image/help_img.png")
    await message.answer_photo(
        photo=photo,
        caption=(
            "/start - start bot\n"
            "/help - show commands\n"
            "/profile - show profile\n"
            "/login - register user\n"
            "/courses - show courses\n"
        )
    )


async def show_profile(message: Message):
    user_id = message.from_user.id
    if user_storage.is_registered(user_id):
    if user_storage.is_registered(user_id):
        await message.answer("Welcome, home!", reply_markup=command_keyboard)
    else:
        await message.answer("Please, log in!", reply_markup=main_keyboard)

#Добавляем команду start и кнопку Start
@router.message(Command("start"))
async def start_command(message: Message):
    await show_start(message)


@router.message(F.text == "Start")
async def start_button(message: Message):
    await show_start(message)


#Добавляем команду help и кнопку Help
@router.message(Command("help"))
async def show_command(message: Message):
    await show_help(message)


@router.message(F.text == "Help")
async def help_button_text(message: Message):
    await show_help(message)


#Добавляем команду profile и кнопку Profile
@router.message(Command("profile"))
async def profile_command(message: Message):
    await show_profile(message)


@router.message(F.text == "Profile")
async def profile_button_text(message: Message):
    await show_profile(message)


#Добавляем команду login и кнопку Login
async def show_login(message: Message, state: FSMContext):
    if user_storage.is_registered(message.from_user.id):
    if user_storage.is_registered(message.from_user.id):
        await message.answer("You are already registered.", reply_markup=command_keyboard)
        return

    photo = FSInputFile("image/login_img.png")
    await state.set_state(RegisterState.waiting_for_phone)
    await message.answer_photo(
        photo=photo,
        caption="Share your phone number using the button below:",
        reply_markup=contact_keyboard,
        caption="Share your phone number using the button below:",
        reply_markup=contact_keyboard,
    )


@router.message(Command("login"))
async def login_command(message: Message, state: FSMContext):
    await show_login(message, state)


@router.message(F.text == "Login")
async def login_button_text(message: Message, state: FSMContext):
    await show_login(message, state)


#Добавляем команду courses и кнопку Courses
@router.message(Command("courses"))
async def courses_command(message: Message):
    await message.answer(
        "🎓 Vildly Academy Courses\n\n"
        "Choose a course to learn more.",
        reply_markup=courses_keyboard()
    )


@router.message(F.text == "Courses")
async def courses_button(message: Message):
    await courses_command(message)


@router.callback_query(F.data == "course_python")
async def python_course(callback: CallbackQuery):
    await callback.message.answer(
        "🐍 Python Programming\n\n"
        "Learn Python from scratch and build real projects."
    )
    await callback.answer()


##################   Регистрация пользователя    ##################
###################################################################

#Добавляем обработчик для получения номера телефона и перехода к следующему шагу регистрации
@router.message(RegisterState.waiting_for_phone)
async def get_phone(message: Message, state: FSMContext):
    ### Accept only Telegram contact sharing from the same account.
    if not message.contact or message.contact.user_id != message.from_user.id:
        await message.answer("Please use the button to share your own phone number.")
    ### Accept only Telegram contact sharing from the same account.
    if not message.contact or message.contact.user_id != message.from_user.id:
        await message.answer("Please use the button to share your own phone number.")
        return

    phone = message.contact.phone_number.strip()
    error = registration_service.validate_phone(phone)
    if error:
        await message.answer(error)
        return
    phone = message.contact.phone_number.strip()
    error = registration_service.validate_phone(phone)
    if error:
        await message.answer(error)
        return
    await state.update_data(phone_number=phone)
    await state.set_state(RegisterState.waiting_for_email)
    await message.answer("Now enter your email:", reply_markup=ReplyKeyboardRemove())

    await message.answer("Now enter your email:", reply_markup=ReplyKeyboardRemove())


@router.message(RegisterState.waiting_for_email)
async def get_email(message: Message, state: FSMContext):
    ### Email must be typed as text because it will be used for future mailings.
    if not message.text:
        await message.answer("Please enter your email as text.")
    ### Email must be typed as text because it will be used for future mailings.
    if not message.text:
        await message.answer("Please enter your email as text.")
        return

    email = message.text.strip()
    error = registration_service.validate_email(email)
    if error:
        await message.answer(error)
    email = message.text.strip()
    error = registration_service.validate_email(email)
    if error:
        await message.answer(error)
        return

    data = await state.get_data()
    user = message.from_user
    result = registration_service.register(
        user_id=user.id,
        phone=data["phone_number"],
        email=email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    user = message.from_user
    result = registration_service.register(
        user_id=user.id,
        phone=data["phone_number"],
        email=email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    await message.answer(result, reply_markup=command_keyboard if "completed" in result else None)
    await message.answer(result, reply_markup=command_keyboard if "completed" in result else None)
    await state.clear()


###################################################################
###################################################################

@router.callback_query(F.data == "profile")
async def profile_inline_button(callback: CallbackQuery):
    await show_profile(callback.message)
    await callback.answer()


@router.callback_query(F.data == "help")
async def help_inline_button(callback: CallbackQuery):
    await show_help(callback.message)
    await callback.answer()


@router.message(F.text == "Book a Lesson")
async def lesson_signup_button(message: Message):
    await show_lesson_signup(message)


@router.message(F.text == "Back")
async def back_button(message: Message):
    await message.answer("Main menu", reply_markup=main_keyboard)


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
