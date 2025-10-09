class MainException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MainException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(MainException):
    detail = "Не осталось свободных номеров"


class ObjectAlreadyExistsException(MainException):
    detail = "Объект уже существует"
