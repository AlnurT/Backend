from fastapi import Response

from app.api.dependencies import UserIdDep
from app.exceptions import ObjectAlreadyExistsException, EmailAlreadyExistsException
from app.schemas.users import UserRequestAdd, UserAdd
from app.services.auth import AuthServices
from app.services.base import BaseService


class UserService(BaseService):
    async def register_user(self, data: UserRequestAdd):
        hashed_password = AuthServices().hash_password(data.password)
        hashed_data = UserAdd(email=data.email, hashed_password=hashed_password)

        try:
            await self.db.users.add(hashed_data)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise EmailAlreadyExistsException

    async def login_user(self, response: Response, data: UserRequestAdd):
        user = await self.db.users.get_user_with_hashed_password(data.email)
        AuthServices().verify_password(
            plain_password=data.password,
            hashed_password=user.hashed_password,
        )
        access_token = AuthServices().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return access_token

    async def get_me(self, user_id: UserIdDep):
        return await self.db.users.get_one(id=user_id)

    @staticmethod
    async def logout_user(response: Response):
        response.delete_cookie("access_token")
