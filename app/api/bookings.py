from datetime import datetime

from fastapi import APIRouter, Body
from fastapi import Request

from app.api.dependencies import DBDep
from app.schemas.bookings import BookingAddRequest, BookingAdd
from app.services.auth import AuthServices

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.post("", summary="Добавление бронирования")
async def post_booking(
        request: Request,
        db: DBDep,
        data_booking: BookingAddRequest = Body(openapi_examples={
            "1": {"summary": "Бронь", "value": {
                "date_from": "01.09.2025",
                "date_to": "11.09.2025",
                "room_id": 4,
            }},
        }),
):
    token = request.cookies.get("access_token")
    user = AuthServices().decode_token(token)
    room = await db.rooms.get_one_or_none(id=data_booking.room_id)
    format_string = "%d.%m.%Y"
    date_from = datetime.strptime(data_booking.date_from, format_string)
    date_to = datetime.strptime(data_booking.date_to, format_string)
    _data_booking = BookingAdd(
        user_id=user["user_id"],
        room_id=data_booking.room_id,
        date_from=date_from,
        date_to=date_to,
        price=room.price,
        # total_cost=room.price * (date_to - date_from).days,
    )
    booking = await db.bookings.add(_data_booking)
    await db.commit()

    return {"status": "OK", "data": booking}
