import asyncio
import logging

import uvicorn
from aiokafka import AIOKafkaProducer
from api.v1 import ugc_loader
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from storage import kafka

from core.logger import LOGGING
from core.settings import get_settings
from services.ugc_kafka_producer import UGCKafkaProducer

app = FastAPI(
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    title="Post-only API UGC для онлайн-кинотеатра",
    description="Сбор различной аналитики",
    version="1.0.0",
)

loop = asyncio.get_event_loop()

# aioproducer = get_aioproducer(loop=loop)
kafka.aioproducer = AIOKafkaProducer(
    loop=loop,
    client_id=get_settings().kafka_settings.project_name,
    bootstrap_servers=",".join(get_settings().kafka_settings.hosts),
    value_serializer=UGCKafkaProducer.serializer,
    compression_type="gzip",
)


@app.on_event("startup")
async def startup_event():
    await kafka.aioproducer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka.aioproducer.stop()


if get_settings().app.should_check_jwt:
    from core.middleware import apply_middleware

    apply_middleware(app=app)

app.include_router(ugc_loader.router, prefix="/api/v1", tags=["UGC Loader"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=get_settings().app.host,
        port=get_settings().app.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=get_settings().app.should_reload,
    )
