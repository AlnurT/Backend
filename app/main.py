import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.api.hotels import router as router_hotels
from app.api.users import router as router_users


app = FastAPI()
app.include_router(router_users)
app.include_router(router_hotels)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
