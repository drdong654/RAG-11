import pytest

from services import RegistrationService, UserStorage

@pytest.fixture
def user_storage(tmp_path):
    db_file = tmp_path / "users.db"
    return UserStorage(db_file)

@pytest.fixture
def registration_service(user_storage):
    return RegistrationService(user_storage)