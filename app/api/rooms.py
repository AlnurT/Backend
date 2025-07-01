from fastapi import APIRouter, Body

from app.api.dependencies import DBDep
from app.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(
    prefix="/hotels",
    tags=["Номера"],
)


@router.get("/{hotel_id}/rooms", summary="Список номеров отеля")
async def get_rooms(db: DBDep, hotel_id: int):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Один номер отеля")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(
        id=room_id, hotel_id=hotel_id
    )


@router.post("/{hotel_id}/rooms", summary="Добавление номера")
async def post_room(
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequest = Body(openapi_examples={
            "1": {"summary": "Обычный номер", "value": {
                "title": "Обычный",
                "description": "Номер с видом на реку",
                "price": 5000,
                "quantity": 2,
            }},
            "2": {"summary": "Ошибка", "value": {
                "title": "Обычный",
            }},
        })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное изменение номера")
async def put_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest = Body(openapi_examples={
            "1": {"summary": "Обычный -> Люкс", "value": {
                "title": "Люкс",
                "description": "Номер с видом на реку",
                "price": 12000,
                "quantity": 3,
            }},
            "2": {"summary": "Ошибка", "value": {
                "title": "Обычный",
            }},
        })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение номера")
async def patch_hotel(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest = Body(openapi_examples={
            "1": {"summary": "Цена номера", "value": {
                "price": 15000,
            }},
        })
):
    _room_data = RoomPatch(
        hotel_id=hotel_id,
        **room_data.model_dump(exclude_unset=True)
    )
    await db.rooms.edit(
        _room_data,
        exclude_unset=True,
        id=room_id,
        hotel_id=hotel_id,
    )
    await db.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "OK"}
