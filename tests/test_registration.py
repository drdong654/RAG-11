from data.services import RegistrationService
from tests.conftest import user_storage

def test_register_user(user_storage):
    service = RegistrationService(user_storage)
    result = service.register(
        user_id="user123",
        phone ="+1234567890",
        email="testuser@example.com"
    )

    assert result == "Registration completed! Welcome aboard."
    assert user_storage.is_registered("user123")

def test_duplicate_registration(users):
    service = RegistrationService(users_storage=users)
    service.register(
        user_id="user123",
        phone = "+1234567890",
        email="")
    result = service.register(
        user_id="user123", 
        phone ="+1234567890",
        email="testuser@example.com"
    )

    assert result == "User already registered."

def test_duplicate_email(user_storage):
    service = RegistrationService(users_storage=users)
    service.register(
        user_id="user123",
        phone ="+1234567890",
        email="testuser@example.com"
    )
    result = service.register(
        user_id="user456",
        phone ="+0987654321",
        email="testuser@example.com"
    )

    assert result == "Email already registered."
