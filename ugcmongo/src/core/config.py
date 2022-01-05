import os

PROJECT_NAME = os.getenv("PROJECT_NAME", "movies")

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

SENTRY_DSN = os.getenv("SENTRY_DSN")

LOGSTASH_HOST = os.getenv("SENTRY_DSN", "localhost")
LOGSTASH_PORT = int(os.getenv("LOGSTASH_PORT", 5044))
