from datetime import date

from app.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=7, day=1),
        date_to=date(year=2025, month=7, day=31),
        price=5000,
    )

    await db.bookings.add(booking_data)

    db_booking = await db.bookings.get_filtered(user_id=user_id, room_id=room_id)
    assert db_booking
    assert db_booking[0].user_id == user_id
    assert db_booking[0].room_id == room_id

    booking_data.price = 10000
    await db.bookings.edit(user_id=user_id, data=booking_data)

    await db.bookings.delete(user_id=user_id)

    await db.commit()
