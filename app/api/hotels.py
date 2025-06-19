from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy import insert, select

from app.database import async_session
from app.models.hotels import HotelsOrm
from app.schemas.dependencies import PaginationDep, Status
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
        hotel = await HotelsRepository(session).add(
            data=hotel_data.model_dump()
        )
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное изменение отеля")
def put_hotel(
        hotel_id: int,
        data: HotelADD = Body(openapi_examples={
            "1": {"summary": "Москва -> Пекин", "value": {
                "title": "Пекин", "name": "beijing"
            }},
            "2": {"summary": "Ошибка", "value": {
                "title": "Пекин"
            }},
        })
) -> Status:
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = data.title
            hotel["name"] = data.name

    return Status.model_validate({"status": "OK"})


@router.patch("/{hotel_id}", summary="Частичное изменение отеля")
def patch_hotel(
        hotel_id: int,
        data: HotelPATCH = Body(openapi_examples={
            "1": {"summary": "Полное изменение", "value": {
                "title": "Пекин", "name": "beijing"
            }},
            "2": {"summary": "Частичное изменение", "value": {
                "title": "Хайнань"
            }},
        })
) -> Status:
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if data.title is not None:
                hotel["title"] = data.title
            if data.name is not None:
                hotel["name"] = data.name

    return Status.model_validate({"status": "OK"})


@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(hotel_id: int) -> Status:
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return Status.model_validate({"status": "OK"})
