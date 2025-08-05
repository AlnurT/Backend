from pydantic import EmailStr
from sqlalchemy import select

from app.models.users import UsersOrm
from app.repositories.mappers.mappers import UserDataMapper, \
    UserDataWithHashedPasswordMapper
from app.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None

        return UserDataWithHashedPasswordMapper.map_to_domain_entity(res)
