from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class BookingAddRequest(BaseModel):
    date_from: str = Field(description="Дата начала брони")
    date_to: str = Field(description="Дата конца брони")
    room_id: int = Field(description="Айди номера")


class BookingAdd(BaseModel):
    user_id: int = Field(description="Айди пользователя")
    room_id: int = Field(description="Айди номера")
    date_from: date = Field(description="Дата начала брони")
    date_to: date = Field(description="Дата конца брони")
    price: int = Field(description="Цена за сутки")
    # total_cost: int = Field(0, description="Общая стоимость")


class Booking(BookingAdd):
    id: int = Field(description="Айди брони")
    total_cost: int = Field(description="Общая стоимость")

    model_config = ConfigDict(from_attributes=True)
