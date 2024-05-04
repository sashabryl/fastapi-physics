import pytest
from httpx import AsyncClient

import dependencies
from problems import crud


@pytest.mark.anyio
@pytest.mark.usefixtures("create_themes", "delete_themes")
class TestTheme:
    @pytest.mark.anyio
    async def test_home(self, client: AsyncClient):
        response = await client.get("/themes/")
        assert response.status_code == 200
        assert response.json()[0].get("name") == "Mechanics"
        assert response.json()[1].get("name") == "Electronics"

    @pytest.mark.anyio
    async def test_create_theme_by_admin(self, admin_client: AsyncClient):
        theme_json = {"name": "Feynman", "description": "Richard"}
        response = await admin_client.post(
            "/themes/", json=theme_json
        )
        assert response.json().get("success")

    @pytest.mark.anyio
    async def test_create_theme_by_user(self, user_client: AsyncClient):
        theme_json = {"name": "Feynman", "description": "Richard"}
        response = await user_client.post(
            "/themes/", json=theme_json
        )
        assert response.status_code == 403
