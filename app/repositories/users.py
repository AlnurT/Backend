from pydantic import EmailStr
from sqlalchemy import select

from app.models.users import UsersOrm
from app.schemas.users import User, UserWithHashedPassword
from app.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None

        return UserWithHashedPassword.model_validate(res)
