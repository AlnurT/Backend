import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("date_from, date_to, room_id, status_code", [
    ("2025-07-01", "2025-07-25", 1, 200),
    ("2025-07-02", "2025-07-26", 1, 200),
    ("2025-07-03", "2025-07-27", 1, 200),
    ("2025-07-04", "2025-07-28", 1, 200),
    ("2025-07-05", "2025-07-29", 1, 200),
    ("2025-07-06", "2025-07-30", 1, 500),
    ("2025-07-30", "2025-08-01", 1, 200),
])
async def test_post_booking(
        date_from: str,
        date_to: str,
        room_id: int,
        status_code: int,
        db,
        authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "date_from": date_from,
            "date_to": date_to,
            "room_id": room_id,
        }
    )
    assert response.status_code == status_code
    if response.status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture()
async def reset_bookings(db):
    await db.bookings.delete()
    await db.commit()


@pytest.mark.parametrize("date_from, date_to, room_id, count", [
    ("2025-07-01", "2025-07-25", 1, 1),
    ("2025-07-02", "2025-07-26", 1, 2),
    ("2025-07-03", "2025-07-27", 1, 3),
])
async def test_add_and_get_bookings(
        date_from: str,
        date_to: str,
        room_id: int,
        count: int,
        db,
        authenticated_ac: AsyncClient,
        reset_bookings,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "date_from": date_from,
            "date_to": date_to,
            "room_id": room_id,
        }
    )
    user_id = response.json()["data"]["user_id"]
    response = await authenticated_ac.get(
        "/bookings/me",
        params={"user_id": user_id},
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == count
