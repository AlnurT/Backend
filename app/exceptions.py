from datetime import date

from fastapi import HTTPException


class MainException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MainException):
    detail = "Объект не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class ObjectAlreadyExistsException(MainException):
    detail = "Объект уже существует"


class HotelAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Отель уже существует"


class RoomAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Номер уже существует"


class EmailAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Email уже используется"


class AllRoomsAreBookedException(MainException):
    detail = "Не осталось свободных номеров"


class UserNotExistException(MainException):
    detail = "Пользователь не зарегистрирован"


class PasswordNotCorrectException(MainException):
    detail = "Неверный пароль"


class TokenNotCorrectException(MainException):
    detail = "Неверный токен"


class IncorrectDateException(MainException):
    detail = "Дата заезда позже даты выезда"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_from > date_to:
        raise IncorrectDateException


class MainHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(MainHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(MainHTTPException):
    status_code = 404
    detail = "Номер не найден"


class IncorrectDateHTTPException(MainHTTPException):
    status_code = 422
    detail = "Дата заезда позже даты выезда"


class HotelAlreadyExistsHTTPException(MainHTTPException):
    status_code = 409
    detail = "Отель уже существует"


class RoomAlreadyExistsHTTPException(MainHTTPException):
    status_code = 409
    detail = "Номер уже существует"


class EmailAlreadyExistsHTTPException(MainHTTPException):
    status_code = 409
    detail = "Email уже используется"


class UserNotFoundHTTPException(MainHTTPException):
    status_code = 401
    detail = "Нет доступа, войдите в систему"


class UserNotExistHTTPException(MainHTTPException):
    status_code = 401
    detail = "Пользователь не зарегистрирован"


class PasswordNotCorrectHTTPException(MainHTTPException):
    status_code = 401
    detail = "Неверный пароль"


class AllRoomsAreBookedHTTPException(MainHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"
