from datetime import date

from app.exceptions import check_date_to_after_date_from, ObjectNotFoundException, RoomNotFoundException
from app.schemas.facilities import RoomFacilityAdd
from app.schemas.hotels import HotelAdd
from app.schemas.rooms import RoomAddRequest, RoomAdd
from app.services.base import BaseService
from app.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)
        await HotelService(self.db).get_hotel_with_check(hotel_id)

        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )

    async def get_room_by_id(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        return await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)

    async def create_room(self, hotel_id: int, data: RoomAddRequest):
        await HotelService(self.db).get_hotel_with_check(hotel_id)

        _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        room = await self.db.rooms.add(_room_data)

        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=f_id)
            for f_id in data.facilities_ids
        ]
        if rooms_facilities_data:
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()

        return room

    async def edit_room(
            self,
            hotel_id: int,
            room_id: int,
            data: HotelAdd,
            exclude_unset: bool = False,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)

        _room_data_dict = data.model_dump(exclude_unset=exclude_unset)
        _room_data = RoomAdd(hotel_id=hotel_id, **_room_data_dict)
        try:
            await self.db.rooms.edit(_room_data, id=room_id, exclude_unset=exclude_unset)
            if "facilities_ids" in _room_data_dict:
                await self.db.rooms_facilities.set_room_facilities(
                    room_id,
                    _room_data_dict["facilities_ids"],
                )
            await self.db.commit()
        except ObjectNotFoundException:
            raise RoomNotFoundException

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id)

        try:
            await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
            await self.db.commit()
        except ObjectNotFoundException:
            raise RoomNotFoundException

        return {"status": "OK"}

    async def get_room_with_check(self, room_id: int):
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
