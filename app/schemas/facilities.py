from pydantic import BaseModel, Field


class FacilityAdd(BaseModel):
    title: str = Field(description="Название удобства")


class Facility(FacilityAdd):
    id: int = Field(description="Айди удобства")


class RoomFacilityAdd(BaseModel):
    room_id: int = Field(description="Айди комнаты")
    facility_id: int = Field(description="Айди удобства")


class RoomFacility(RoomFacilityAdd):
    id: int = Field(description="Айди связи удобства и комнаты")
