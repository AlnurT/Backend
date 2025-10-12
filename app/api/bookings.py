

from fastapi import APIRouter, Body, HTTPException

from app.api.dependencies import DBDep, UserIdDep
from app.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
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
    data_booking: BookingAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Бронь обычного",
                "value": {
                    "date_from": "2025-07-01",
                    "date_to": "2025-07-31",
                    "room_id": 3,
                },
            },
            "2": {
                "summary": "Бронь випа",
                "value": {
                    "date_from": "2025-07-01",
                    "date_to": "2025-07-31",
                    "room_id": 4,
                },
            },
        }
    ),
):
    try:
        room = await db.rooms.get_one(id=data_booking.room_id)
    except ObjectNotFoundException:
        raise HTTPException(400, "Номер не найден")

    hotel = await db.hotels.get_one(id=room.hotel_id)
    _data_booking = BookingAdd(
        user_id=user_id,
        price=room.price,
        **data_booking.model_dump()
    )
    try:
        booking = await db.bookings.add_booking(_data_booking, hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(409, ex.detail)

    await db.commit()

    return {"status": "OK", "data": booking}
