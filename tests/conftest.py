import pytest
from pathlib import Path

from data.services import UserStorage


@pytest.fixture
def user_storage(tmp_path):
    db = tmp_path / "users.db"
    return UserStorage(db)
