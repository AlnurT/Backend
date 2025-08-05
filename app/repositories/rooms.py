from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.repositories.base import BaseRepository
from app.models.rooms import RoomsOrm
from app.repositories.utils import rooms_ids_for_booking
from app.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)
        return [
            RoomWithRels.model_validate(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_or_none_with_rels(self, hotel_id: int, id: int):
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(id=id, hotel_id=hotel_id)
        )
        result = await self.session.execute(query)
        res = result.unique().scalars().one_or_none()
        if res is None:
            return None

        return RoomWithRels.model_validate(res)
