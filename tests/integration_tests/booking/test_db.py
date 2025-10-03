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

    new_booking = await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.user_id == new_booking.user_id
    assert booking.room_id == new_booking.room_id

    booking_data.price = 10000
    await db.bookings.edit(id=new_booking.id, data=booking_data)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.price == booking_data.price

    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking is None
