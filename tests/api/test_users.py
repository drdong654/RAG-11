import importlib
import os
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient


API_TOKEN = "test-api-token"


class FakeUserRepository:
    def __init__(self, users):
        self.users = users

    async def list_all(self):
        return self.users

    async def get_by_telegram_id(self, telegram_id):
        return next(
            (user for user in self.users if user.telegram_id == telegram_id),
            None,
        )


@pytest.fixture(scope="module")
def api_module():
    os.environ["DATABASE_URL"] = "postgresql+asyncpg://bot:bot@localhost:5432/bot"
    os.environ["API_TOKEN"] = API_TOKEN
    return importlib.import_module("api.main")


@pytest_asyncio.fixture
async def api_client(api_module):
    users = [
        SimpleNamespace(
            telegram_id=1,
            username="operator-visible",
            first_name="Test",
            last_name="User",
            phone_number="+1234567890",
            email="private@example.com",
            created_at=datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc),
        )
    ]
    repository = FakeUserRepository(users)

    async def override_users():
        yield repository

    api_module.app.dependency_overrides[api_module.get_users] = override_users
    transport = ASGITransport(app=api_module.app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    api_module.app.dependency_overrides.clear()


def operator_headers(token=API_TOKEN):
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.parametrize(
    ("path", "headers"),
    [
        ("/users", {}),
        ("/users", operator_headers("wrong-token")),
        ("/users/1", {}),
        ("/users/1", operator_headers("wrong-token")),
    ],
)
@pytest.mark.asyncio
async def test_users_require_operator_token(api_client, path, headers):
    response = await api_client.get(path, headers=headers)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API token."}
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.asyncio
async def test_list_users_uses_public_response_schema(api_client):
    response = await api_client.get("/users", headers=operator_headers())

    assert response.status_code == 200
    assert response.json() == [
        {
            "telegram_id": 1,
            "username": "operator-visible",
            "first_name": "Test",
            "last_name": "User",
            "created_at": "2026-09-01T12:00:00Z",
        }
    ]
    assert "phone_number" not in response.text
    assert "private@example.com" not in response.text


@pytest.mark.asyncio
async def test_get_user_returns_404_with_stable_schema(api_client):
    response = await api_client.get("/users/999", headers=operator_headers())

    assert response.status_code == 404
    assert response.json() == {"detail": "Пользователь не найден"}


@pytest.mark.asyncio
async def test_get_user_returns_documented_schema(api_client):
    response = await api_client.get("/users/1", headers=operator_headers())

    assert response.status_code == 200
    assert response.json()["telegram_id"] == 1
    assert set(response.json()) == {
        "telegram_id",
        "username",
        "first_name",
        "last_name",
        "created_at",
    }


@pytest.mark.asyncio
async def test_openapi_user_schema_has_no_contact_data(api_client):
    response = await api_client.get("/openapi.json")

    assert response.status_code == 200
    properties = response.json()["components"]["schemas"]["UserResponse"]["properties"]
    assert "phone_number" not in properties
    assert "email" not in properties
    assert set(properties) == {
        "telegram_id",
        "username",
        "first_name",
        "last_name",
        "created_at",
    }
