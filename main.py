import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Moscow", "name": "moscow"},
    {"id": 2, "title": "Almaty", "name": "almaty"},
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айди отеля"),
        title: str | None = Query(None, description="Заголовок отеля"),
        name: str | None = Query(None, description="Название отеля"),
) -> list:
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        if name and hotel["name"] != name:
            continue

        hotels_.append(hotel)

    return hotels_


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int) -> dict:
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.post("/hotels")
def post_hotel(
        title: str = Body(),
        name: str = Body(),
) -> dict:
    global hotels
    id = hotels[-1]["id"] + 1 if hotels else 1
    hotel = {
        "id": id,
        "title": title,
        "name": name
    }
    hotels.append(hotel)
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def put_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body(),
) -> dict:
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name

            return {"status": "OK"}

    return {"status": "Отель не существует"}


@app.patch("/hotels/{hotel_id}")
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None),
) -> dict:
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title if title else hotel["title"]
            hotel["name"] = name if name else hotel["name"]

            return {"status": "OK"}

    return {"status": "Отель не существует"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
