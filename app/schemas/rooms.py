from pydantic import BaseModel, Field, ConfigDict

from app.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str = Field(description="Название номера")
    description: str | None = Field(None, description="Описание")
    price: int = Field(description="Цена за сутки")
    quantity: int = Field(description="Вместительность")
    facilities_ids: list[int] = Field([], description="Список удобств")


class RoomAdd(BaseModel):
    hotel_id: int = Field(description="Айди отеля")
    title: str = Field(description="Название номера")
    description: str | None = Field(None, description="Описание")
    price: int = Field(description="Цена за сутки")
    quantity: int = Field(description="Вместительность")


class Room(RoomAdd):
    id: int = Field(description="Айди номера")

    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility] = Field(description="Список удобств")


class RoomPatchRequest(BaseModel):
    title: str | None = Field(None, description="Название номера")
    description: str | None = Field(None, description="Описание")
    price: int | None = Field(None, description="Цена за сутки")
    quantity: int | None = Field(None, description="Вместительность")
    facilities_ids: list[int] = Field([], description="Список удобств")


class RoomPatch(BaseModel):
    hotel_id: int | None = Field(None, description="Айди отеля")
    title: str | None = Field(None, description="Название номера")
    description: str | None = Field(None, description="Описание")
    price: int | None = Field(None, description="Цена за сутки")
    quantity: int | None = Field(None, description="Вместительность")
