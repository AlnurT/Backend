from sqlalchemy import delete

from app.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from app.repositories.base import BaseRepository
from app.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def delete_bulk(self, ids, **filter_by):
        delete_stmt = (
            delete(self.model)
            .filter(self.model.facility_id.in_(ids))
            .filter_by(**filter_by)
        )
        await self.session.execute(delete_stmt)
