from fastapi import APIRouter, Body

from app.api.dependencies import DBDep
from app.schemas.facilities import FacilityAdd

router = APIRouter(
    prefix="/facilities",
    tags=["Удобства"]
)


@router.get("", summary="Все удобства")
async def get_facilities(db: DBDep):
    return await db.facilities.get_filtered()


@router.post("", summary="Добавить удобство")
async def post_facility(
        db: DBDep,
        facility_data: FacilityAdd = Body(openapi_examples={
            "1": {"summary": "Джакузи", "value": {
                "title": "Джакузи",
            }},
            "2": {"summary": "Бильярд", "value": {
                "title": "Бильярд"
            }},
        })
):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}
