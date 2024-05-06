import pytest
from httpx import AsyncClient


@pytest.mark.anyio
@pytest.mark.usefixtures("clear_users")
@pytest.mark.parametrize(
    "username, email, password1, password2, status_code",
    [
        (
            "test_user",
            "some_email123@gmail.com",
            "somePassword1234",
            "somePassword1234",
            400
        ),
        (
            "validUsername123",
            "testuser@gmail.com",
            "somePassword1234",
            "somePassword1234",
            400
        ),
        (
            "validUsername123",
            "some_email213@gmail.com",
            "somePassword13342",
            "somePassword1234",
            400
        ),
        (
            "validUsername123",
            "some_email213@gmail.com",
            "somePasswordLetters",
            "somePasswordLetters",
            400
        ),
        (
            "validUsername123",
            "some_email213@gmail.com",
            "1234567890",
            "1234567890",
            400
        ),
        (
            "validUsername123",
            "some_email213@gmail.com",
            "tooShort9",
            "tooShort9",
            400
        ),
        (
            "validUsername123",
            "some_email213@gmail.com",
            "SomeValidPassword123",
            "SomeValidPassword123",
            200
        )
    ]
)
async def test_user_register(
    client: AsyncClient,
    username: str,
    email: str,
    password1: str,
    password2: str,
    status_code: int
):
    json = {
        "username": username,
        "email": email,
        "password1": password1,
        "password2": password2
    }
    response = await client.post("/users/", json=json)
    assert response.status_code == status_code


@pytest.mark.anyio
@pytest.mark.parametrize(
    "username_or_email, password, status_code",
    [
        ("test_user", "asdf!qwe123", 200),
        ("testuser@gmail.com", "asdf!qwe123", 200),
        ("test_user", "asdf!qwe12", 400)
    ]
)
async def test_user_login(
    client: AsyncClient,
    username_or_email: str,
    password: str,
    status_code: int
):
    json = {"username_or_email": username_or_email, "password": password}
    response = await client.post("/jwt/login/", data=json)
    assert response.status_code == status_code


@pytest.mark.anyio
@pytest.mark.parametrize(
    "user_id, username, status_code",
    [
        (1, "test_user", 200),
        (2, "test_admin", 200),
        (3, None, 404)
    ]
)
async def test_read_one_user(
    client: AsyncClient,
    user_id: int,
    username: str | None,
    status_code: int
):
    response = await client.get(f"/users/{user_id}/")
    assert response.status_code == status_code
    if username is not None:
        assert response.json().get("username") == username
