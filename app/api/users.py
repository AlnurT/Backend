from fastapi import APIRouter, Body, HTTPException, Response, Request

from app.database import async_session
from app.schemas.users import UserRequestAdd, UserAdd
from app.repositories.users import UsersRepository
from app.services.auth import AuthServices

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и авторизация"],
)


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
    hashed_password = AuthServices().hash_password(data.password)
    hashed_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session() as session:
        await UsersRepository(session).add(hashed_data)
        await session.commit()

    return {"status": "OK"}


@router.post("/login", summary="Вход пользователя")
async def login_user(
        response: Response,
        data: UserRequestAdd = Body(openapi_examples={
            "1": {"summary": "Альнур", "value": {
                "email": "alnur@mail.ru", "password": "12345"
            }},
            "2": {"summary": "Неверный логин", "value": {
                "email": "al@mail.ru", "password": "12345"
            }},
            "3": {"summary": "Неверный пароль", "value": {
                "email": "alnur@mail.ru", "password": "1"
            }},
        }),
):
    async with async_session() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(data.email)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Такой пользователь не зарегистрирован",
            )
        if not AuthServices().verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Неверный пароль",
            )
        access_token = AuthServices().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.post("/only_auth", summary="Получение токена")
async def only_auth(
        request: Request,
):
    access_token = request.cookies.get("access_token")
    return {"access_token": access_token}
