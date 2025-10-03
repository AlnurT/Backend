from httpx import AsyncClient


async def test_post_facilities(ac: AsyncClient):
    facility_name = "Джакузи"
    response = await ac.post(
        "/facilities",
        json={
            "title": facility_name,
        }
    )
    res = response.json()
    assert response.status_code == 200

    assert isinstance(res, dict)
    assert "data" in res
    assert res["data"]["title"] == facility_name


async def test_get_facilities(ac: AsyncClient):
    response = await ac.get("/facilities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
