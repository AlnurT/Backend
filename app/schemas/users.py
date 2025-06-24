from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(description="Пароль")


class UserAdd(BaseModel):
    email: EmailStr = Field(description="Email пользователя")
    hashed_password: str = Field(description="Хэш пароль")


class User(BaseModel):
    id: int = Field(description="Айди пользователя")
    email: EmailStr = Field(description="Email пользователя")

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str = Field(description="Хэш пароль")

