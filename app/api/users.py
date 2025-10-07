from fastapi import APIRouter, Body, HTTPException, Response

from app.api.dependencies import UserIdDep, DBDep
from app.schemas.users import UserRequestAdd, UserAdd
from app.services.auth import AuthServices

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и авторизация"],
)


@router.post("/register", summary="Добавление пользователя")
async def register_user(
        db: DBDep,
        data: UserRequestAdd = Body(openapi_examples={
            "1": {
                "summary": "Альнур",
                "value": {
                    "email": "alnur@mail.ru",
                    "password": "12345"
                }
            },
            "2": {
                "summary": "Талгат",
                "value": {
                    "email": "talga@mail.ru",
                    "password": "12345"
                }
            },
        })
):
    try:
        hashed_password = AuthServices().hash_password(data.password)
        hashed_data = UserAdd(email=data.email, hashed_password=hashed_password)

        await db.users.add(hashed_data)
        await db.commit()
    except:  # noqa: E722
        raise HTTPException(400)

    return {"status": "OK"}


@router.post("/login", summary="Вход пользователя")
async def login_user(
    db: DBDep,
    response: Response,
    data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Альнур",
                "value": {
                    "email": "alnur@mail.ru",
                    "password": "12345"
                }
            },
            "2": {
                "summary": "Неверный логин",
                "value": {
                    "email": "al@mail.ru",
                    "password": "12345"
                },
            },
            "3": {
                "summary": "Неверный пароль",
                "value": {
                    "email": "alnur@mail.ru",
                    "password": "1"
                },
            },
            "4": {
                "summary": "Талгат",
                "value": {
                    "email": "talga@mail.ru",
                    "password": "12345"
                }
            },
        }
    ),
):
    user = await db.users.get_user_with_hashed_password(data.email)
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


@router.get("/me", summary="Получение токена")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout", summary="Выход пользователя")
async def logout_user(
    response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "OK"}
