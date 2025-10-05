from fastapi import APIRouter, Body

from app.api.dependencies import DBDep, UserIdDep
from app.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.get("", summary="Получение всех данных бронирования")
async def get_booking(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получение своих данных бронирования")
async def get_my_booking(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Добавление бронирования")
async def post_booking(
        user_id: UserIdDep,
        db: DBDep,
        data_booking: BookingAddRequest = Body(openapi_examples={
            "1": {"summary": "Бронь обычного", "value": {
                "date_from": "2025-09-01",
                "date_to": "2025-09-11",
                "room_id": 3,
            }},
            "2": {"summary": "Бронь випа", "value": {
                "date_from": "2025-09-05",
                "date_to": "2025-09-15",
                "room_id": 4,
            }},
        }),
):
    room = await db.rooms.get_one_or_none(id=data_booking.room_id)
    _data_booking = BookingAdd(
        user_id=user_id,
        price=room.price,
        **data_booking.model_dump()
    )
    booking = await db.bookings.add_booking(_data_booking, room.quantity)
    await db.commit()

    return {"status": "OK", "data": booking}
