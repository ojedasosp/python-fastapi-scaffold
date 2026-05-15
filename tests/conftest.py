import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import SQLModel

from main import app
from database import get_session
import users.user_entity  # noqa: F401 — registers User with SQLModel.metadata
from users import User


@pytest.fixture
async def engine():
    engine = create_async_engine("sqlite+aiosqlite://", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def client(engine):
    async def get_test_session():
        async with AsyncSession(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.fixture
async def a_user_already_on_db(engine):
    async with AsyncSession(engine) as session:
        user = User(id=1, name="Alice", age=30, email="alice@example.com", password="secret123")
        session.add(user)
        await session.commit()
