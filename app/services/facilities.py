from datetime import date

from app.api.dependencies import PaginationDep
from app.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException, \
    ObjectAlreadyExistsException, HotelAlreadyExistsException, RoomNotFoundException, RoomAlreadyExistsException
from app.schemas.bookings import BookingAddRequest, BookingAdd
from app.schemas.facilities import RoomFacilityAdd, FacilityAdd
from app.schemas.hotels import HotelAdd
from app.schemas.rooms import RoomAddRequest, RoomAdd
from app.services.base import BaseService
from app.services.hotels import HotelService
from app.services.rooms import RoomService
from app.tasks.tasks import test_task


class FacilityService(BaseService):
    async def get_facilities(self):
        test_task.delay()
        return await self.db.facilities.get_all()

    async def create_facility(self, data: FacilityAdd):
        facility = await self.db.facilities.add(data)
        await self.db.commit()
        return facility
