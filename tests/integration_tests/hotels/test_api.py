async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2025-07-01",
            "date_to": "2025-07-31",
        }
    )
    assert response.status_code == 200
