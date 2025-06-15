from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, Field


class HotelGET(BaseModel):
    id: Annotated[int | None, Query(None, description="Айди отеля")]
    title: Annotated[str | None, Query(None, description="Заголовок отеля")]
    name: Annotated[str | None, Query(None, description="Название отеля")]


class HotelPATCH(BaseModel):
    title: str | None = Field(None, description="Заголовок отеля")
    name: str | None = Field(None, description="Название отеля")


class HotelADD(BaseModel):
    title: str = Field(description="Заголовок отеля")
    name: str = Field(description="Название отеля")
