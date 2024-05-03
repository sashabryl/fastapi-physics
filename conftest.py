from typing import AsyncIterator

import pytest
from httpx import AsyncClient

from main import app


@pytest.fixture()
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
