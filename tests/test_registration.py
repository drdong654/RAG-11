from services import RegistrationService


def test_register_user(user_storage):
    
    service = RegistrationService(user_storage)
    result = service.register(
        user_id=1,
        phone ="+1234567890",
        email="testuser@example.com"
    )

    assert result == "Registration completed! Welcome aboard."
    assert user_storage.is_registered(1) 

def test_duplicate_registration(user_storage):
    service = RegistrationService(user_storage)
    
    service.register(
        user_id=1,
        phone = "+1234567890",
        email="testuser@example.com")
    result = service.register(
        user_id=1, 
        phone ="+1234567890",
        email="testuser@example.com"
    )

    assert result == "You are already registered."

def test_duplicate_email(user_storage):
    service = RegistrationService(user_storage)
    service.register(
        user_id=1,
        phone ="+1234567890",
        email="testuser@example.com"
    )
    result = service.register(
        user_id=2,
        phone ="+0987654321",
        email="testuser@example.com"
    )

    assert result == "This email is already registered."
