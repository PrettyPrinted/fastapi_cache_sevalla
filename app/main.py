from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi import FastAPI, Response
from app.core.config import settings
from fastapi_cache.decorator import cache
from datetime import datetime 

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan=lifespan) 

@app.get("/cached") 
@cache(expire=120)
def index(response: Response):
    return {"message": f"Last generated at {datetime.now()}"}