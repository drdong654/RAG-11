import pytest


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
