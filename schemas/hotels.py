from pydantic import BaseModel, Field, ConfigDict


class ConfigModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class HotelPATCH(BaseModel):
    title: str | None = Field(None, description="Заголовок отеля")
    name: str | None = Field(None, description="Название отеля")


class HotelGET(HotelPATCH):
    id: int | None = Field(None, description="Айди отеля")
    page: int = Field(1, description="Страница")
    per_page: int = Field(3, description="Количество отелей за страницу")


class HotelADD(BaseModel):
    title: str = Field(description="Заголовок отеля")
    name: str = Field(description="Название отеля")


class Status(ConfigModel):
    status: str
