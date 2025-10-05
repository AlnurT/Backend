from datetime import date

from fastapi import HTTPException
from sqlalchemy import select

from app.models.bookings import BookingsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import BookingDataMapper
from app.repositories.utils import rooms_ids_for_booking
from app.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id,
            date_from=data.date_from,
            date_to=data.date_to,
        )

        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book = rooms_ids_to_book_res.scalars().all()

        if data.room_id not in rooms_ids_to_book:
            raise HTTPException(
                status_code=401,
                detail="Больше нет номеров",
        )
        return await self.add(data)
