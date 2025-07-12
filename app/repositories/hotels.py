from datetime import date

from sqlalchemy import select

from app.models.rooms import RoomsOrm
from app.repositories.utils import rooms_ids_for_booking
from app.schemas.hotels import Hotel
from app.repositories.base import BaseRepository
from app.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

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

        filters = [HotelsOrm.id.in_(hotels_ids_to_get)]
        if title:
            filters.append(HotelsOrm.title.icontains(title))

        if location:
            filters.append(HotelsOrm.location.icontains(location))

        return await self.get_filtered(*filters, limit=limit, offset=offset)
