from app.schemas.bookings import BookingAddRequest, BookingAdd
from app.services.base import BaseService
from app.services.hotels import HotelService
from app.services.rooms import RoomService


class BookingService(BaseService):
    async def get_booking(self):
        return await self.db.bookings.get_all()

    async def get_my_booking(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def create_booking(self, user_id: int, data: BookingAddRequest):
        room = await RoomService(self.db).get_room_with_check(data.room_id)
        hotel = await HotelService(self.db).get_hotel_with_check(room.hotel_id)

        _data_booking = BookingAdd(user_id=user_id, price=room.price, **data.model_dump())
        booking = await self.db.bookings.add_booking(_data_booking, hotel.id)
        await self.db.commit()
        return booking
