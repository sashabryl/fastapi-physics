import pytest
from httpx import AsyncClient

import dependencies
from problems import crud
from auth.utils import encode_jwt
from problems.schemas import ThemeBase


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
    @pytest.mark.parametrize(
        "user_id, status_code",
        [
            (2, 200),
            (1, 403),
            (None, 401)
        ]
    )
    async def test_create_theme(
            self, client: AsyncClient, user_id: int | None, status_code: int
    ):
        headers = {}
        if user_id is not None:
            token = encode_jwt({"sub": user_id})
            headers = {"Authorization": f"Bearer {token}"}
        theme_json = {"name": "Feynman", "description": "Richard"}
        response = await client.post(
            "/themes/", json=theme_json, headers=headers
        )
        assert response.status_code == status_code

    @pytest.mark.anyio
    async def test_read_one_theme(self, client: AsyncClient, session):
        themes = await crud.get_all_themes(db=session)
        response = await client.get(f"/themes/{themes[0].id}/")
        assert response.status_code == 200
        assert response.json().get("name") == themes[0].name

    @pytest.mark.anyio
    async def test_update_theme_by_guest(self, client: AsyncClient, session):
        token = encode_jwt({"sub": 2})
        headers = {"Authorization": f"Bearer {token}"}
        themes = await crud.get_all_themes(db=session)
        theme = themes[0]
        theme_json = {"name": "Nuclear fusion", "description": "This is about atoms"}
        response = await client.put(
            f"/themes/{theme.id}/",
            headers=headers,
            json=theme_json
        )
        assert response.status_code == 200
        assert response.json().get("name") == "Nuclear fusion"

    @pytest.mark.anyio
    @pytest.mark.parametrize(
        "user_id, status_code",
        [
            (2, 200),
            (1, 403),
            (None, 401)
        ]
    )
    async def test_delete_theme(
            self, client: AsyncClient, user_id: int | None, status_code: int, session
    ):
        await crud.create_theme(
            db=session, theme_schema=ThemeBase(name=f"some{user_id}", description=f"new{user_id}")
        )
        new_theme = await crud.get_theme_by_name(name=f"some{user_id}", db=session)
        headers = {}
        if user_id is not None:
            token = encode_jwt({"sub": user_id})
            headers = {"Authorization": f"Bearer {token}"}
        response = await client.delete(
            f"/themes/{new_theme.id}/", headers=headers
        )
        assert response.status_code == status_code
        deleted_theme = await crud.get_theme_by_name(db=session, name=f"some{user_id}")
