from fastapi import APIRouter, Body, Response

from app.api.dependencies import UserIdDep, DBDep
from app.exceptions import (
    ObjectAlreadyExistsException,
    EmailAlreadyExistsHTTPException,
    UserNotExistException,
    UserNotExistHTTPException,
    PasswordNotCorrectHTTPException,
    PasswordNotCorrectException,
)
from app.schemas.users import UserRequestAdd
from app.services.users import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и авторизация"],
)


@router.post("/register", summary="Добавление пользователя")
async def register_user(
    db: DBDep,
    user_data: UserRequestAdd = Body(
        openapi_examples={
            "1": {"summary": "Альнур", "value": {"email": "alnur@mail.ru", "password": "12345"}},
            "2": {"summary": "Талгат", "value": {"email": "talga@mail.ru", "password": "12345"}},
        }
    ),
):
    try:
        await UserService(db).register_user(user_data)
    except ObjectAlreadyExistsException:
        raise EmailAlreadyExistsHTTPException

    return {"status": "OK"}


@router.post("/login", summary="Вход пользователя")
async def login_user(
    db: DBDep,
    response: Response,
    user_data: UserRequestAdd = Body(
        openapi_examples={
            "1": {"summary": "Альнур", "value": {"email": "alnur@mail.ru", "password": "12345"}},
            "2": {
                "summary": "Неверный логин",
                "value": {"email": "al@mail.ru", "password": "12345"},
            },
            "3": {
                "summary": "Неверный пароль",
                "value": {"email": "alnur@mail.ru", "password": "1"},
            },
            "4": {"summary": "Талгат", "value": {"email": "talga@mail.ru", "password": "12345"}},
        }
    ),
):
    try:
        access_token = await UserService(db).login_user(data=user_data)

    except UserNotExistException:
        raise UserNotExistHTTPException

    except PasswordNotCorrectException:
        raise PasswordNotCorrectHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me", summary="Получение токена")
async def get_me(db: DBDep, user_id: UserIdDep):
    return await UserService(db).get_me(user_id)


@router.post("/logout", summary="Выход пользователя")
async def logout_user(response: Response):
    await UserService.logout_user(response)
    return {"status": "OK"}
