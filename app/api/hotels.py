from datetime import date

from fastapi import APIRouter, Body, Query

from app.api.dependencies import PaginationDep, DBDep
from app.schemas.hotels import HotelAdd, HotelPATCH

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("", summary="Список отелей или отеля")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Локация"),
        date_from: date = Query(example="2025-12-10"),
        date_to: date = Query(example="2025-06-16"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        # title=title,
        # location=location,
        # limit=per_page,
        # offset=per_page * (pagination.page - 1),
        date_from=date_from,
        date_to=date_to,
    )

    # return await db.hotels.get_all(
    #     title=title,
    #     location=location,
    #     limit=per_page,
    #     offset=per_page * (pagination.page - 1),
    # )


@router.get("/{hotel_id}", summary="Один отель")
async def get_hotel(hotel_id: int, db: DBDep,):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("", summary="Добавление отеля")
async def post_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
            "1": {"summary": "Пекин", "value": {
                "title": "Дракон", "location": "Пекин"
            }},
            "2": {"summary": "Ошибка", "value": {
                "title": "Дракон"
            }},
        })
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное изменение отеля")
async def put_hotel(
        db: DBDep,
        hotel_id: int,
        data: HotelAdd = Body(openapi_examples={
            "1": {"summary": "Пекин -> Хайнань", "value": {
                "title": "Змея", "location": "Хайнань"
            }},
            "2": {"summary": "Ошибка", "value": {
                "title": "Змея"
            }},
        })
):
    await db.hotels.edit(data, id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное изменение отеля")
async def patch_hotel(
        db: DBDep,
        hotel_id: int,
        data: HotelPATCH = Body(openapi_examples={
            "1": {"summary": "Полное изменение", "value": {
                "title": "Змея", "location": "Хайнань"
            }},
            "2": {"summary": "Частичное изменение", "value": {
                "title": "Змея"
            }},
        })
):
    await db.hotels.edit(data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"status": "OK"}
