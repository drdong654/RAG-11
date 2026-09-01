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


@pytest.mark.asyncio
async def test_registration_normalizes_phone_and_email(user_storage):
    service = RegistrationService(user_storage)

    result = await service.register(
        user_id=1,
        phone="+1 (234) 567-8901",
        email="  Test.User@Example.COM  ",
    )

    assert result == "Registration completed! Welcome aboard."
    assert user_storage._users[1]["phone_number"] == "+12345678901"
    assert user_storage._users[1]["email"] == "test.user@example.com"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("phone", "email", "expected"),
    [
        ("12345", "user@example.com", "Invalid phone number. Must be between 10 and 15 digits."),
        ("123456789x", "user@example.com", "Invalid phone number. Must contain only digits and common separators."),
        ("+1234567890", "invalid-email", "Invalid email address."),
    ],
)
async def test_invalid_registration_does_not_change_storage(
    user_storage, phone, email, expected
):
    service = RegistrationService(user_storage)

    result = await service.register(user_id=1, phone=phone, email=email)

    assert result == expected
    assert user_storage._users == {}


@pytest.mark.asyncio
async def test_duplicate_email_check_uses_normalized_email(user_storage):
    service = RegistrationService(user_storage)
    await service.register(
        user_id=1,
        phone="+1234567890",
        email="TestUser@Example.com",
    )

    result = await service.register(
        user_id=2,
        phone="+0987654321",
        email="  testuser@example.COM ",
    )

    assert result == "This email is already registered."
    assert not await user_storage.is_registered(2)
