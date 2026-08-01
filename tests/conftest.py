import pytest
from pathlib import Path

from services import RegistrationService, UserStorage



@pytest.fixture
def user_storage(tmp_path):
    db = tmp_path / "users.db"
    return UserStorage(db)

@pytest.fixture
def registration_service(user_storage):
    return RegistrationService(user_storage)
