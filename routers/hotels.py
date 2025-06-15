from fastapi import APIRouter, Body, Query

from schemas.hotels import HotelADD, Status, HotelGET, HotelPATCH

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


hotels = [
    {"id": 1, "title": "Москва", "name": "moscow"},
    {"id": 2, "title": "Алматы", "name": "almaty"},
    {"id": 3, "title": "Токио", "name": "tokyo"},
    {"id": 4, "title": "Минск", "name": "minsk"},
    {"id": 5, "title": "Берлин", "name": "berlin"},
    {"id": 6, "title": "Париж", "name": "paris"},
    {"id": 7, "title": "Рим", "name": "rome"},
]


@router.get("", summary="Список отелей или отеля")
def get_hotels(data: HotelGET = Query()) -> list[HotelGET]:
    hotels_ = []
    for hotel in hotels:
        if data.id and hotel["id"] != data.id:
            continue
        if data.title and hotel["title"] != data.title:
            continue
        if data.name and hotel["name"] != data.name:
            continue

        hotel_model = HotelGET.model_validate(hotel)
        hotels_.append(hotel_model)

    start = data.per_page * (data.page - 1)
    end = data.per_page * data.page

    return hotels_[start: end]


@router.post("", summary="Добавление отеля")
def post_hotel(
        data: HotelADD = Body(openapi_examples={
            "1": {"summary": "Пекин", "value": {
                "title": "Пекин", "name": "beijing"
            }},
            "2": {"summary": "Ошибка", "value": {
                "title": "Пекин"
            }},
        })
) -> Status:
    global hotels
    id = hotels[-1]["id"] + 1 if hotels else 1
    hotel = {
        "id": id,
        "title": data.title,
        "name": data.name
    }
    hotels.append(hotel)

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
