from pydantic import BaseModel, ConfigDict, Field


class FacilityAdd(BaseModel):
    title: str = Field(description="Название удобства")


class Facility(FacilityAdd):
    id:  int = Field(description="Айди удобства")

    model_config = ConfigDict(from_attributes=True)


class RoomFacilityAdd(BaseModel):
    room_id: int = Field(description="Айди комнаты")
    facility_id: int = Field(description="Айди удобства")


class RoomFacility(RoomFacilityAdd):
    id: int = Field(description="Айди связи удобства и комнаты")

    model_config = ConfigDict(from_attributes=True)
