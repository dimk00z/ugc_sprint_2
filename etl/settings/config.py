from functools import lru_cache

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    host: str = Field("localhost", env="APP_HOST")
    port: int = Field(5000, env="APP_PORT")
    batch_size: int = Field(100, env="BATCH_SIZE")


class KafkaSettings(BaseSettings):
    host: list[str] = Field(["localhost:29092"], env="KAFKA_HOST")
    topics: list[str] = Field(["movie_topic"], env="EVENT_TYPES")
    group_id: str = Field("", env="KAFKA_GROUP_ID")


class ClickHouseSettings(BaseSettings):
    host: str = Field("localhost:9000", env="CH_HOST")
    db: str = Field("movies", env="CH_DB")
    tables: list[str] = Field(["movie_topic"], env="EVENT_TYPES")


class Settings(BaseSettings):
    app = AppSettings()
    kafka_settings = KafkaSettings()
    ch_settings = ClickHouseSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
