import os

from pydantic import BaseSettings


class TestSettings(BaseSettings):
    mongo_host: str
    mongo_port: int
    redis_host: str
    redis_port: int
    service_protocol: str
    service_host: str
    service_port: str
    service_api_version: int


test_settings = {
    "mongo_host": os.getenv("MONGO_HOST"),
    "mongo_port": os.getenv("MONGO_PORT"),
    "redis_host": os.getenv("REDIS_HOST"),
    "redis_port": os.getenv("REDIS_PORT"),
    "service_protocol": os.getenv("SERVICE_PROTOCOL"),
    "service_host": os.getenv("SERVICE_HOST"),
    "service_port": os.getenv("SERVICE_PORT"),
    "service_api_version": os.getenv("SERVICE_API_VERSION"),
}
config = TestSettings.parse_obj(test_settings)
