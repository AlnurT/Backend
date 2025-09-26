from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from app.api.dependencies import DBDep
from app.schemas.facilities import FacilityAdd

router = APIRouter(
    prefix="/facilities",
    tags=["Удобства"]
)


@router.get("", summary="Все удобства")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("БАЗА")
    return await db.facilities.get_all()


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
            "3": {"summary": "Мини бар", "value": {
                "title": "Мини бар"
            }},
        })
):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}
