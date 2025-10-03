from app.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Дракон", location="Пекин")

    await db.hotels.add(hotel_data)
    await db.commit()
