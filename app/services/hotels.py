from datetime import date

from app.api.dependencies import PaginationDep
from app.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException, \
    ObjectAlreadyExistsException, HotelAlreadyExistsException
from app.schemas.hotels import HotelAdd
from app.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
            self,
            pagination: PaginationDep,
            title: str | None,
            location: str | None,
            date_from: date,
            date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5

        return await self.db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            date_from=date_from,
            date_to=date_to,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel_by_id(self, hotel_id: int):
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException

    async def create_hotel(self, hotel_data: HotelAdd):
        try:
            hotel = await self.db.hotels.add(hotel_data)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise HotelAlreadyExistsException

        return hotel

    async def edit_hotel(
            self,
            hotel_id: int,
            data: HotelAdd,
            exclude_unset: bool = False,
    ):
        try:
            await self.db.hotels.edit(
                data=data, exclude_unset=exclude_unset, id=hotel_id
            )
            await self.db.commit()
        except ObjectNotFoundException:
            raise HotelNotFoundException

    async def delete_hotel(self, hotel_id: int):
        try:
            await self.db.hotels.delete(id=hotel_id)
            await self.db.commit()
        except ObjectNotFoundException:
            raise HotelNotFoundException

        return {"status": "OK"}
