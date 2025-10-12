from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.exceptions import UserNotExistException
from app.models.users import UsersOrm
from app.repositories.mappers.mappers import UserDataMapper, UserDataWithHashedPasswordMapper
from app.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        try:
            res = result.scalar_one()
        except NoResultFound:
            raise UserNotExistException

        return UserDataWithHashedPasswordMapper.map_to_domain_entity(res)
