from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel, ConfigDict


class ConfigModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Status(BaseModel):
    status: str


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, ge=1, description="Страница")]
    per_page: Annotated[int | None, Query(
        None, ge=1, le=10, description="Количество отелей за страницу"
    )]


PaginationDep = Annotated[PaginationParams, Depends()]
