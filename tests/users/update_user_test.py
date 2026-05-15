import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from users import User


@pytest.fixture
async def a_user_already_on_db(engine):
    async with AsyncSession(engine) as session:
        user = User(name="Alice", age=30, email="alice@example.com", password="secret123")
        session.add(user)
        await session.commit()


async def test_update_user(a_user_already_on_db, client):
    response = await client.put("/api/users/", params={"id": 1}, json={"name": "Bob"})
    assert response.status_code == 201
    assert response.json()["name"] == "Bob"


async def test_update_user_not_found(client):
    response = await client.put("/api/users/", params={"id": 999}, json={"name": "Bob"})
    assert response.status_code == 404


async def test_update_user_response_shape(a_user_already_on_db, client):
    response = await client.put("/api/users/", params={"id": 1}, json={"age": 25})
    assert response.status_code == 201
    user = response.json()
    assert "name" in user
    assert "age" in user
    assert "email" in user
    assert "password" not in user
