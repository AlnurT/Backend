from httpx import AsyncClient


async def test_post_facilities(ac: AsyncClient):
    response = await ac.post(
        "/facilities",
        json={
            "facility_data": {
                "title": "Джакузи",
            }
        }
    )
    assert response.status_code == 200


async def test_get_facilities(ac: AsyncClient):
    response = await ac.get(
        "/facilities",
    )
    assert response.status_code == 200
