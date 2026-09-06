import pytest

from services import RegistrationService


@pytest.mark.asyncio
async def test_register_user(user_storage):
    service = RegistrationService(user_storage)

    result = await service.register(
        user_id=1,
        phone="+1234567890",
        email="testuser@example.com",
    )

    assert result == "Registration completed! Welcome aboard."
    assert await user_storage.is_registered(1)


@pytest.mark.asyncio
async def test_duplicate_registration(user_storage):
    service = RegistrationService(user_storage)

    await service.register(
        user_id=1,
        phone="+1234567890",
        email="testuser@example.com",
    )

    result = await service.register(
        user_id=1,
        phone="+1234567890",
        email="testuser@example.com",
    )

    assert result == "You are already registered."


@pytest.mark.asyncio
async def test_duplicate_email(user_storage):
    service = RegistrationService(user_storage)

    await service.register(
        user_id=1,
        phone="+1234567890",
        email="testuser@example.com",
    )

    result = await service.register(
        user_id=2,
        phone="+0987654321",
        email="testuser@example.com",
    )

    assert result == "This email is already registered."