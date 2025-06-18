from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, Field


class HotelGET(BaseModel):
    title: Annotated[str | None, Query(None, description="Заголовок отеля")]
    location: Annotated[str | None, Query(None, description="Название отеля")]


class HotelPATCH(BaseModel):
    title: str | None = Field(None, description="Заголовок отеля")
    location: str | None = Field(None, description="Название отеля")


class HotelADD(BaseModel):
    title: str = Field(description="Заголовок отеля")
    location: str = Field(description="Название отеля")
