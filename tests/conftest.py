import pytest

from app.config import settings
from app.database import engine_null_pool, Base
from app.models import *


@pytest.fixture(scope="session", autouse=True)
async def check_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def async_main(check_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
