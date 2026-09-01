import asyncio
import os

import pytest

from services import RegistrationService


# AAA style

@pytest.mark.asyncio
async def test_upsert_user(user_repository):
    # Arrange
    test_user_id = 123
    test_username = "test_user"
    test_first_name = "Test"

    # Act
    await user_repository.upsert(
        telegram_id=test_user_id,
        username=test_username,
        first_name=test_first_name 
    )

    user = await user_repository.get_by_telegram_id(test_user_id)

    # Assert
    assert user is not None
    assert user.telegram_id == test_user_id
    assert user.username == test_username
    assert user.first_name == test_first_name


@pytest.mark.asyncio
async def test_concurrent_registration_allows_email_once(database_user_storage):
    if not os.getenv("TEST_DATABASE_URL"):
        pytest.skip("TEST_DATABASE_URL is not set")

    first = RegistrationService(database_user_storage)
    second = RegistrationService(database_user_storage)

    results = await asyncio.gather(
        first.register(1, "+1234567890", "shared@example.com"),
        second.register(2, "+0987654321", "shared@example.com"),
    )

    assert sorted(results) == sorted([
        "Registration completed! Welcome aboard.",
        "This email is already registered.",
    ])
    registered = await asyncio.gather(
        database_user_storage.is_registered(1),
        database_user_storage.is_registered(2),
    )
    assert sum(registered) == 1
