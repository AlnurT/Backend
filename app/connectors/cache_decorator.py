import json
from functools import wraps

from app.init import redis_manager


def my_cache(expire):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            facilities_from_cache = await redis_manager.get("facilities")
            if facilities_from_cache is not None:
                facilities_dicts = json.loads(facilities_from_cache)
                return facilities_dicts

            facilities = await func(*args, **kwargs)
            facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
            facilities_json = json.dumps(facilities_schemas)
            await redis_manager.set("facilities", facilities_json, expire)

            return facilities

        return wrapper

    return decorator
