from datetime import date

from fastapi import HTTPException


class MainException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MainException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(MainException):
    detail = "Объект уже существует"


class AllRoomsAreBookedException(MainException):
    detail = "Не осталось свободных номеров"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_from > date_to:
        raise HTTPException(422, "Дата заезда позже даты выезда")


class MainHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


def HotelNotFoundHTTPException(MainHTTPException):
    status_code = 404
    detail = "Отель не найден"


def RoomNotFoundHTTPException(MainHTTPException):
    status_code = 404
    detail = "Номер не найден"
