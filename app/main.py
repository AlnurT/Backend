from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

from fastapi_cache import FastAPICache
from starlette.responses import RedirectResponse

sys.path.append(str(Path(__file__).parent.parent))

from app.init import redis_manager
from app.api.hotels import router as router_hotels
from app.api.users import router as router_users
from app.api.rooms import router as router_rooms
from app.api.bookings import router as router_bookings
from app.api.facilities import router as router_facilities


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(redis_manager.redis, prefix="fastapi-cache")

    yield

    await redis_manager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
