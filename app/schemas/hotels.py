from pydantic import BaseModel, Field, ConfigDict


class HotelAdd(BaseModel):
    title: str = Field(description="Название отеля")
    location: str = Field(description="Локация")


class Hotel(HotelAdd):
    id: int = Field(description="Айди отеля")


class HotelPATCH(BaseModel):
    title: str | None = Field(None, description="Название отеля")
    location: str | None = Field(None, description="Локация")
