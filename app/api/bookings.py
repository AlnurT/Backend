

from fastapi import APIRouter, Body, HTTPException

from app.api.dependencies import DBDep, UserIdDep
from app.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundException, \
    RoomNotFoundHTTPException, HotelNotFoundHTTPException, HotelNotFoundException, AllRoomsAreBookedHTTPException
from app.schemas.bookings import BookingAddRequest, BookingAdd
from app.services.bookings import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.get("", summary="Получение всех данных бронирования")
async def get_booking(db: DBDep):
    return await BookingService(db).get_booking()


@router.get("/me", summary="Получение своих данных бронирования")
async def get_my_booking(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_my_booking(user_id)


@router.post("", summary="Добавление бронирования")
async def post_booking(
    db: DBDep,
    user_id: UserIdDep,
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
        booking = await BookingService(db).create_booking(user_id=user_id, data=data_booking)

    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking}
