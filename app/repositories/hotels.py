from datetime import date

from sqlalchemy import select

from app.models.rooms import RoomsOrm
from app.repositories.mappers.mappers import HotelDataMapper
from app.repositories.utils import rooms_ids_for_booking
from app.repositories.base import BaseRepository
from app.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        title: str,
        location: str,
        limit: int,
        offset: int,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to,
        )
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        query = select(self.model).filter(HotelsOrm.id.in_(hotels_ids_to_get))

        if title:
            query = query.filter(HotelsOrm.title.icontains(title))

        if location:
            query = query.filter(HotelsOrm.location.icontains(location))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
