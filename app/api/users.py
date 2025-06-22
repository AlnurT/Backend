from fastapi import APIRouter, Body
from passlib.context import CryptContext

from app.database import async_session
from app.schemas.users import UserRequestAdd, UserAdd
from app.repositories.users import UsersRepository

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и авторизация"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", summary="Добавление пользователя")
async def register_user(
        data: UserRequestAdd = Body(openapi_examples={
            "1": {"summary": "Альнур", "value": {
                "email": "alnur@mail.ru", "password": "12345"
            }},
            "2": {"summary": "Ошибка", "value": {
                "email": "alnur", "password": "12345"
            }},
        })
):
    hashed_password = pwd_context.hash(data.password)
    hashed_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session() as session:
        await UsersRepository(session).add(hashed_data)
        await session.commit()

    return {"status": "OK"}
