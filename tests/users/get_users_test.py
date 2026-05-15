import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from users.user_entity import User


@pytest.fixture
async def two_users(engine):
    async with AsyncSession(engine) as session:
        users = [
            User(name="Alice", age=30, email="alice@example.com", password="secret123"),
            User(name="Bob", age=25, email="bob@example.com", password="secret456"),
        ]
        for user in users:
            session.add(user)
        await session.commit()


async def test_get_users_empty_db_returns_empty_list(client):
    response = await client.get("/api/users/")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_users_returns_all_users(client, two_users):
    response = await client.get("/api/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    names = {u["name"] for u in data}
    assert names == {"Alice", "Bob"}


async def test_get_users_response_shape(client, two_users):
    response = await client.get("/api/users/")
    user = response.json()[0]
    assert "name" in user
    assert "age" in user
    assert "email" in user
    assert "password" not in user
    assert "id" not in user


async def test_get_users_limit(client, two_users):
    response = await client.get("/api/users/?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_users_offset(client, two_users):
    response = await client.get("/api/users/?offset=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_users_offset_beyond_total_returns_empty(client, two_users):
    response = await client.get("/api/users/?offset=10")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_users_limit_over_100_returns_422(client):
    response = await client.get("/api/users/?limit=101")
    assert response.status_code == 422
