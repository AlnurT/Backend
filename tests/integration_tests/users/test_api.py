import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("abc@mail.ru", "12345", 200),
        ("abc@mail.ru", "12345", 400),
        ("abc@mail", "12345", 422),
        ("abc", "12345", 422),
    ],
)
async def test_auth(
    email: str,
    password: str,
    status_code: int,
    ac: AsyncClient,
):
    reg_response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert reg_response.status_code == status_code
    if status_code != 200:
        return

    login_response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == 200
    login_res = login_response.json()
    assert isinstance(login_res, dict)
    assert ac.cookies.get("access_token") == login_res["access_token"]

    response = await ac.get("/auth/me")
    assert response.status_code == 200
    user = response.json()
    assert isinstance(user, dict)
    assert "id" in user
    assert user["email"] == email
    assert "password" not in user
    assert "hashed_password" not in user

    logout_response = await ac.post("/auth/logout")
    assert logout_response.status_code == 200
    assert "access_token" not in ac.cookies

    response = await ac.get("/auth/me")
    assert response.status_code == 401
