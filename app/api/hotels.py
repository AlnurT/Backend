from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy import insert, select

from app.database import async_session
from app.models.hotels import HotelsOrm
from app.schemas.dependencies import PaginationDep, Status
from app.schemas.hotels import HotelADD, HotelGET, HotelPATCH

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
        query = select(HotelsOrm)
        if hotels_data.title:
            query = query.filter(HotelsOrm.title.ilike(f"%{hotels_data.title}%"))

        if hotels_data.location:
            query = query.filter(HotelsOrm.location.ilike(f"%{hotels_data.location}%"))

        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all()

    return hotels


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
) -> Status:
    async with async_session() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return Status.model_validate({"status": "OK"})


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
