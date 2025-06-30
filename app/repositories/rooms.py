from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.models.rooms import RoomsOrm
from app.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self, hotel_id: int):
        query = select(self.model).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]
