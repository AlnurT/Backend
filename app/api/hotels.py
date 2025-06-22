from fastapi import APIRouter, Body, Query

from app.database import async_session
from app.schemas.dependencies import PaginationDep
from app.schemas.hotels import HotelAdd, HotelPATCH
from app.repositories.hotels import HotelsRepository

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("", summary="Список отелей или отеля")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Локация"),
):
    per_page = pagination.per_page or 5
    async with async_session() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )


@router.get("/{hotel_id}", summary="Один отель")
async def get_hotel(hotel_id: int):
    async with async_session() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("", summary="Добавление отеля")
async def post_hotel(
        hotel_data: HotelAdd = Body(openapi_examples={
            "1": {"summary": "Пекин", "value": {
                "title": "Дракон", "location": "Пекин"
            }},
            "2": {"summary": "Ошибка", "value": {
                "title": "Дракон"
            }},
        })
):
    async with async_session() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное изменение отеля")
async def put_hotel(
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
    async with async_session() as session:
        await HotelsRepository(session).edit(data, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное изменение отеля")
async def patch_hotel(
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
    async with async_session() as session:
        await HotelsRepository(session).edit(data, exclude_unset=True, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int):
    async with async_session() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {"status": "OK"}
