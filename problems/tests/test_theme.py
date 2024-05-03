import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_home(client: AsyncClient):
    response = await client.get("/themes/")
    assert response.status_code == 200