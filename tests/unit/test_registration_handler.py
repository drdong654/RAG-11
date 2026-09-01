import importlib
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest


def load_bot_main(monkeypatch):
    monkeypatch.setenv("TOKEN", "test-token")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+asyncpg://bot:bot@localhost:5432/bot",
    )
    return importlib.import_module("bot.main")


@pytest.mark.asyncio
async def test_phone_handler_rejects_foreign_contact(monkeypatch):
    bot_main = load_bot_main(monkeypatch)
    message = SimpleNamespace(
        from_user=SimpleNamespace(id=1),
        text=None,
        contact=SimpleNamespace(user_id=2, phone_number="+1234567890"),
        answer=AsyncMock(),
    )
    state = AsyncMock()

    await bot_main.get_phone(message, state)

    message.answer.assert_awaited_once_with(
        "Please use the button to share your own phone number."
    )
    state.update_data.assert_not_awaited()
    state.set_state.assert_not_awaited()


@pytest.mark.asyncio
async def test_phone_handler_accepts_own_contact(monkeypatch):
    bot_main = load_bot_main(monkeypatch)
    message = SimpleNamespace(
        from_user=SimpleNamespace(id=1),
        text=None,
        contact=SimpleNamespace(user_id=1, phone_number="+1 (234) 567-8901"),
        answer=AsyncMock(),
    )
    state = AsyncMock()

    await bot_main.get_phone(message, state)

    state.update_data.assert_awaited_once_with(phone_number="+1 (234) 567-8901")
    state.set_state.assert_awaited_once_with(bot_main.RegisterState.waiting_for_email)


@pytest.mark.asyncio
async def test_book_lesson_shows_placeholder_for_registered_user(monkeypatch):
    bot_main = load_bot_main(monkeypatch)
    storage = AsyncMock()
    storage.is_registered.return_value = True
    monkeypatch.setattr(bot_main, "user_storage", storage)
    message = SimpleNamespace(
        from_user=SimpleNamespace(id=1),
        answer=AsyncMock(),
    )

    await bot_main.show_lesson_signup(message)

    message.answer.assert_awaited_once_with(
        "🚧 Запись на занятия находится в разработке."
    )


@pytest.mark.asyncio
async def test_book_lesson_requires_registration(monkeypatch):
    bot_main = load_bot_main(monkeypatch)
    storage = AsyncMock()
    storage.is_registered.return_value = False
    monkeypatch.setattr(bot_main, "user_storage", storage)
    message = SimpleNamespace(
        from_user=SimpleNamespace(id=1),
        answer=AsyncMock(),
    )

    await bot_main.show_lesson_signup(message)

    message.answer.assert_awaited_once_with(
        "You must complete registration first.\n\nUse /login to continue."
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("registered", "expected_keyboard_name"),
    [(True, "command_keyboard"), (False, "main_keyboard")],
)
async def test_back_selects_keyboard_by_registration(
    monkeypatch, registered, expected_keyboard_name
):
    bot_main = load_bot_main(monkeypatch)
    storage = AsyncMock()
    storage.is_registered.return_value = registered
    monkeypatch.setattr(bot_main, "user_storage", storage)
    message = SimpleNamespace(
        from_user=SimpleNamespace(id=1),
        answer=AsyncMock(),
    )
    state = AsyncMock()

    await bot_main.back_button(message, state)

    state.clear.assert_awaited_once_with()
    message.answer.assert_awaited_once_with(
        "Main menu",
        reply_markup=getattr(bot_main, expected_keyboard_name),
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("handler_name", ["get_phone", "get_email"])
async def test_back_works_inside_registration_state(monkeypatch, handler_name):
    bot_main = load_bot_main(monkeypatch)
    storage = AsyncMock()
    storage.is_registered.return_value = False
    monkeypatch.setattr(bot_main, "user_storage", storage)
    message = SimpleNamespace(
        text="Back",
        contact=None,
        from_user=SimpleNamespace(id=1),
        answer=AsyncMock(),
    )
    state = AsyncMock()

    await getattr(bot_main, handler_name)(message, state)

    state.clear.assert_awaited_once_with()
    message.answer.assert_awaited_once_with(
        "Main menu",
        reply_markup=bot_main.main_keyboard,
    )
    state.update_data.assert_not_awaited()
    state.get_data.assert_not_awaited()


@pytest.mark.asyncio
async def test_every_unavailable_course_callback_is_answered(monkeypatch):
    bot_main = load_bot_main(monkeypatch)
    keyboard_callbacks = {
        button.callback_data
        for row in bot_main.courses_keyboard().inline_keyboard
        for button in row
    }
    assert keyboard_callbacks - {"course_python"} == bot_main.UNAVAILABLE_COURSE_CALLBACKS

    for callback_data in bot_main.UNAVAILABLE_COURSE_CALLBACKS:
        callback = SimpleNamespace(
            data=callback_data,
            message=SimpleNamespace(answer=AsyncMock()),
            answer=AsyncMock(),
        )

        await bot_main.unavailable_course(callback)

        callback.message.answer.assert_awaited_once_with(
            "🚧 Информация о курсе находится в разработке."
        )
        callback.answer.assert_awaited_once_with()
