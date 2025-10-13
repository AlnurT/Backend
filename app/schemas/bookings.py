from datetime import date

from pydantic import BaseModel, Field


class BookingAddRequest(BaseModel):
    date_from: date = Field(description="Дата начала брони")
    date_to: date = Field(description="Дата конца брони")
    room_id: int = Field(description="Айди номера")


class BookingAdd(BookingAddRequest):
    user_id: int = Field(description="Айди пользователя")
    price: int = Field(description="Цена за сутки")


class Booking(BookingAdd):
    id: int = Field(description="Айди брони")
