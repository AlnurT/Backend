from typing import Annotated

from fastapi import Query, Depends, HTTPException, Request
from pydantic import BaseModel

from app.database import async_session
from app.services.auth import AuthServices
from app.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Страница")]
    per_page: Annotated[
        int | None,
        Query(None, ge=1, le=20, description="Количество отелей за страницу"),
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Вы не предоставили токен доступа",
        )
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthServices().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
