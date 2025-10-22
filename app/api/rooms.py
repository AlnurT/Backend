from datetime import date

from fastapi import APIRouter, Body, Query

from app.api.dependencies import DBDep
from app.exceptions import (
    IncorrectDateException,
    IncorrectDateHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
)
from app.schemas.rooms import RoomAddRequest, RoomPatchRequest
from app.services.rooms import RoomService

router = APIRouter(
    prefix="/hotels",
    tags=["Номера"],
)


@router.get("/{hotel_id}/rooms", summary="Список номеров отеля")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(default="2025-06-10"),
    date_to: date = Query(default="2025-12-16"),
):
    try:
        return await RoomService(db).get_filtered_by_time(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )
    except IncorrectDateException:
        raise IncorrectDateHTTPException

    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.get("/{hotel_id}/rooms/{room_id}", summary="Один номер отеля")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await RoomService(db).get_room_by_id(hotel_id=hotel_id, room_id=room_id)

    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms", summary="Добавление номера")
async def post_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Обычный номер",
                "value": {
                    "title": "Обычный",
                    "price": 4000,
                    "quantity": 10,
                    "facilities_ids": [3],
                },
            },
            "2": {
                "summary": "Вип номер",
                "value": {
                    "title": "Вип",
                    "description": "Номер с видом на реку",
                    "price": 9000,
                    "quantity": 5,
                    "facilities_ids": [1, 2],
                },
            },
        }
    ),
):
    try:
        room = await RoomService(db).create_room(hotel_id=hotel_id, data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное изменение номера")
async def put_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Вип -> Люкс",
                "value": {
                    "title": "Люкс",
                    "description": "Двухместный номер люкс",
                    "price": 15000,
                    "quantity": 3,
                    "facilities_ids": [1, 2, 3],
                },
            },
        }
    ),
):
    try:
        await RoomService(db).edit_room(hotel_id=hotel_id, room_id=room_id, data=room_data)

    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение номера")
async def patch_hotel(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Цена номера",
                "value": {
                    "price": 20000,
                },
            },
            "2": {
                "summary": "Количество номеров",
                "value": {
                    "quantity": 1,
                },
            },
            "3": {
                "summary": "Только удобства",
                "value": {
                    "facilities_ids": [1, 3],
                },
            },
        }
    ),
):
    try:
        await RoomService(db).edit_room(
            hotel_id=hotel_id,
            room_id=room_id,
            data=room_data,
            exclude_unset=True,
        )

    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomService(db).delete_room(hotel_id=hotel_id, room_id=room_id)

    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "OK"}
