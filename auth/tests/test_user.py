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
