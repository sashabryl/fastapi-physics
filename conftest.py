import asyncio
from typing import AsyncIterator

import nest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport

from database import SessionLocal
from main import app
from auth.utils import encode_jwt


@pytest.fixture(scope="session")
async def session():
    async with SessionLocal() as session:
        yield session


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture()
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        yield client


@pytest.fixture()
async def user_client() -> AsyncIterator[AsyncClient]:
    jwt_payload = {
        "sub": 1,
        "username": "test_user",
        "email": "testuser@gmail.com"
    }
    access_token = encode_jwt(payload=jwt_payload)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        headers={"Authorization": f"Bearer {access_token}"}
    ) as client:
        yield client


@pytest.fixture()
async def admin_client() -> AsyncIterator[AsyncClient]:
    jwt_payload = {
        "sub": 2,
        "username": "test_admin",
        "email": "testadmin@gmail.com"
    }
    access_token = encode_jwt(payload=jwt_payload)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        headers={"Authorization": f"Bearer {access_token}"}
    ) as client:
        yield client
