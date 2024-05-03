from typing import AsyncIterator

import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.fixture()
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture()
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        yield client
