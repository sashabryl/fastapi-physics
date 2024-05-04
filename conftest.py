from typing import AsyncIterator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
import nest_asyncio

from database import SessionLocal
from main import app
from auth.utils import encode_jwt


nest_asyncio.apply()

@pytest.fixture(scope="session")
async def session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="module")
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        yield client
