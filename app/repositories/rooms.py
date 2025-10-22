from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from app.exceptions import RoomNotFoundException
from app.repositories.base import BaseRepository
from app.models.rooms import RoomsOrm
from app.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from app.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

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
            RoomDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_with_rels(self, hotel_id: int, id: int):
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(id=id, hotel_id=hotel_id)
        )
        result = await self.session.execute(query)

        try:
            res = result.unique().scalar_one()
        except NoResultFound:
            raise RoomNotFoundException

        return RoomDataWithRelsMapper.map_to_domain_entity(res)
