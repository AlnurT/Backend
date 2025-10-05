from datetime import date

from fastapi import HTTPException
from sqlalchemy import select

from app.models.bookings import BookingsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import BookingDataMapper


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

    async def add_booking(self, data, quantity):
        if quantity <= 0:
            raise HTTPException(
                status_code=401,
                detail="Больше нет номеров",
        )
        return await self.add(data)
