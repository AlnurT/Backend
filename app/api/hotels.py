from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app.database import async_session
from app.schemas.dependencies import PaginationDep
from app.schemas.hotels import HotelADD, HotelGET, HotelPATCH
from repositories.hotels import HotelsRepository

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("", summary="Список отелей или отеля")
async def get_hotels(
        hotels_data: Annotated[HotelGET, Depends()],
        pagination: PaginationDep,
) -> list[HotelGET]:
    per_page = pagination.per_page or 5
    async with async_session() as session:
        return await HotelsRepository(session).get_all(
            title=hotels_data.title,
            location=hotels_data.location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )


@router.post("", summary="Добавление отеля")
async def post_hotel(
        hotel_data: HotelADD = Body(openapi_examples={
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
        data: HotelADD = Body(openapi_examples={
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

