from datetime import date

from fastapi import APIRouter, Body, Query

from app.api.dependencies import DBDep
from app.schemas.facilities import RoomFacilityAdd
from app.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(
    prefix="/hotels",
    tags=["Номера"],
)


@router.get("/{hotel_id}/rooms", summary="Список номеров отеля")
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2025-12-10"),
        date_to: date = Query(example="2025-06-16"),
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{hotel_id}/rooms/{room_id}", summary="Один номер отеля")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none_with_rels(
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
                "facilities_ids": [1, 2],
            }},
            "2": {"summary": "Ошибка", "value": {
                "title": "Обычный",
            }},
        })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
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
                "description": "Двухместный номер люкс",
                "price": 15000,
                "quantity": 3,
                "facilities_ids": [2, 3],
            }},
            "2": {"summary": "Ошибка", "value": {
                "title": "Обычный",
            }},
        })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)

    await db.rooms_facilities.set_room_facilities(room_id, room_data.facilities_ids)
    await db.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение номера")
async def patch_hotel(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest = Body(openapi_examples={
            "1": {"summary": "Цена номера", "value": {
                "price": 16000,
            }},
            "2": {"summary": "Только удобства", "value": {
                "facilities_ids": [1, 3],
            }},
        })
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

    await db.rooms.edit(
        _room_data,
        exclude_unset=True,
        id=room_id,
        hotel_id=hotel_id,
    )

    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id,
            _room_data_dict["facilities_ids"],
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
