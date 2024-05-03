import pytest
from httpx import AsyncClient


@pytest.mark.anyio
@pytest.mark.usefixtures("delete_themes", "create_themes")
async def test_home(client: AsyncClient):
    response = await client.get("/themes/")
    assert response.status_code == 200
    assert response.json()[0].get("name") == "Mechanics"
    assert response.json()[1].get("name") == "Electronics"
