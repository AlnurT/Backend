from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from starlette.responses import RedirectResponse
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))
logging.basicConfig(level=logging.INFO)

from app.init import redis_manager  # noqa:E402
from app.api.hotels import router as router_hotels  # noqa:E402
from app.api.users import router as router_users  # noqa:E402
from app.api.rooms import router as router_rooms  # noqa:E402
from app.api.bookings import router as router_bookings  # noqa:E402
from app.api.facilities import router as router_facilities  # noqa:E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(redis_manager.redis, prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
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
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
