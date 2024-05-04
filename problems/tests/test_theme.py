import pytest
from httpx import AsyncClient

from problems import crud


@pytest.mark.anyio
@pytest.mark.usefixtures("delete_themes", "create_themes")
async def test_home(client: AsyncClient):
    response = await client.get("/themes/")
    assert response.status_code == 200
    assert response.json()[0].get("name") == "Mechanics"
    assert response.json()[1].get("name") == "Electronics"


@pytest.mark.anyio
@pytest.mark.usefixtures("delete_themes")
async def test_create_theme_by_admin(admin_client: AsyncClient):
    theme_json = {"name": "Feynman", "description": "Richard"}
    response = await admin_client.post(
        "/themes/", json=theme_json
    )
    assert response.json().get("success")


@pytest.mark.anyio
@pytest.mark.usefixtures("delete_themes")
async def test_create_theme_by_admin(user_client: AsyncClient):
    theme_json = {"name": "Feynman", "description": "Richard"}
    response = await user_client.post(
        "/themes/", json=theme_json
    )
    assert response.status_code == 403
