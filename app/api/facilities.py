from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from app.api.dependencies import DBDep
from app.schemas.facilities import FacilityAdd
from app.services.facilities import FacilityService
from app.tasks.tasks import test_task

router = APIRouter(
    prefix="/facilities",
    tags=["Удобства"]
)


@router.get("", summary="Все удобства")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post("", summary="Добавить удобство")
async def post_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Джакузи",
                "value": {"title": "Джакузи"},
            },
            "2": {
                "summary": "Бильярд",
                "value": {"title": "Бильярд"}
            },
            "3": {
                "summary": "Мини бар",
                "value": {"title": "Мини бар"}
            },
        }
    ),
):
    facility = await FacilityService(db).create_facility(facility_data)
    return {"status": "OK", "data": facility}
