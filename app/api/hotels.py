from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from app.api.dependencies import PaginationDep, DBDep
from app.exceptions import (
    IncorrectDateException,
    IncorrectDateHTTPException,
    HotelNotFoundHTTPException,
    HotelNotFoundException,
    HotelAlreadyExistsException,
    HotelAlreadyExistsHTTPException,
)
from app.schemas.hotels import HotelAdd, HotelPATCH
from app.services.hotels import HotelService

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("", summary="Список отелей или отеля")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Локация"),
    date_from: date = Query(default="2025-06-10"),
    date_to: date = Query(default="2025-12-16"),
):
    try:
        return await HotelService(db).get_filtered_by_time(
            pagination=pagination,
            title=title,
            location=location,
            date_from=date_from,
            date_to=date_to,
        )
    except IncorrectDateException:
        raise IncorrectDateHTTPException


@router.get("/{hotel_id}", summary="Один отель")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel_by_id(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("", summary="Добавление отеля")
async def post_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {"summary": "Пекин", "value": {"title": "Дракон", "location": "Пекин"}},
            "2": {"summary": "Токио", "value": {"title": "Сакура", "location": "Токио"}},
        }
    ),
):
    try:
        hotel = await HotelService(db).create_hotel(hotel_data)
    except HotelAlreadyExistsException:
        raise HotelAlreadyExistsHTTPException

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное изменение отеля")
async def put_hotel(
    db: DBDep,
    hotel_id: int,
    data: HotelAdd = Body(
        openapi_examples={
            "1": {"summary": "Пекин -> Хайнань", "value": {"title": "Змея", "location": "Хайнань"}},
        }
    ),
):
    try:
        await HotelService(db).edit_hotel(data=data, hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное изменение отеля")
async def patch_hotel(
    db: DBDep,
    hotel_id: int,
    data: HotelPATCH = Body(
        openapi_examples={
            "1": {"summary": "Частичное изменение", "value": {"title": "Уж"}},
        }
    ),
):
    try:
        await HotelService(db).edit_hotel(data=data, exclude_unset=True, hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(db: DBDep, hotel_id: int):
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK"}
