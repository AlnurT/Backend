import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email, password, status_code", [
    ("abc@mail.ru", "12345", 200),
])
async def test_auth(
        email: str,
        password: str,
        status_code: int,
        authenticated_ac: AsyncClient,
):
    reg_response = await authenticated_ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        }
    )
    assert reg_response.status_code == status_code

    login_response = await authenticated_ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        }
    )
    assert login_response.status_code == status_code
    login_res = login_response.json()
    assert isinstance(login_res, dict)
    assert "access_token" in login_res
    assert authenticated_ac.cookies.get("access_token") == login_res["access_token"]

    response = await authenticated_ac.get("/auth/me")
    assert response.status_code == status_code
    res = response.json()
    assert isinstance(res, dict)
    assert "email" in res
    assert res["email"] == email

    logout_response = await authenticated_ac.post("/auth/logout")
    assert logout_response.status_code == status_code
    assert not authenticated_ac.cookies.get("access_token")

    response = await authenticated_ac.get("/auth/me")
    assert response.status_code == 401
