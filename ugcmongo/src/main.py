import logging

import aioredis
import uvicorn
from api.v1 import film, user
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from core import config
from core.logger import LOGGING
from db import mongo, redis

app = FastAPI(
    title=config.PROJECT_NAME,
    version="1.0.0",
    description="Asychronus API for UGC database",
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json",
    redoc_url="/api/v1/redoc",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis.redis = aioredis.from_url(
        f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True,
    )

    mongo.mongo = AsyncIOMotorClient(
        "mongodb://{host}:{port}".format(
            host=config.MONGO_HOST,
            port=config.MONGO_PORT,
        )
    )


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()


app.include_router(film.router, prefix="/api/v1/film", tags=["film"])
app.include_router(user.router, prefix="/api/v1/user", tags=["user"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8888,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
