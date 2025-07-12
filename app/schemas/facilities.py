from pydantic import BaseModel, ConfigDict, Field


class FacilityAdd(BaseModel):
    title: str = Field(description="Название удобства")


class Facility(FacilityAdd):
    id:  int = Field(description="Айди удобства")

    model_config = ConfigDict(from_attributes=True)
