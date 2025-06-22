from app.models.users import UsersOrm
from app.schemas.users import User
from app.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User
