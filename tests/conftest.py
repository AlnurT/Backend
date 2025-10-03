import json

import pytest
from httpx import AsyncClient, ASGITransport

from app.config import settings
from app.database import engine_null_pool, Base, async_session_maker_null_pool
from app.main import app
from app.models import *
from app.schemas.hotels import HotelAdd
from app.schemas.rooms import RoomAdd
from app.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="function", autouse=True)
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", "r", encoding="utf-8") as file:
        hotels_list: list[dict] = json.load(file)

    with open("tests/mock_rooms.json", "r", encoding="utf-8") as file:
        rooms_list: list[dict] = json.load(file)

    hotels_models = [HotelAdd(**hotel) for hotel in hotels_list]
    rooms_models = [RoomAdd(**room) for room in rooms_list]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels_models)
        await db_.rooms.add_bulk(rooms_models)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    await ac.post(
        "/auth/register",
        json={
            "email": "alnur@mail.ru",
            "password": "12345",
        }
    )
