import pytest

from services import RegistrationService


@pytest.mark.asyncio
async def test_register_user(user_storage):
    service = RegistrationService(user_storage)

    result = await service.register(
        user_id=1,
        phone="+1234567890",
    )

    assert result == "Registration completed! Welcome aboard."
    assert await user_storage.is_registered(1)


@pytest.mark.asyncio
async def test_duplicate_registration(user_storage):
    service = RegistrationService(user_storage)

    await service.register(
        user_id=1,
        phone="+1234567890",
    )

    result = await service.register(
        user_id=1,
        phone="+1234567890",
    )

    assert result == "You are already registered."
