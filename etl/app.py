import json
import logging
from logging import config

from clickhouse_driver.errors import Error
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from modules.ch import ETLClickhouseDriver
from modules.kafka import ETLKafkaConsumer
from modules.transform import order_batches, transform

from settings.config import get_settings
from settings.logging import LOGGING


def run(
    kafka_consumer: KafkaConsumer, ch_driver: ETLClickhouseDriver, batch_size: int = 100
):
    ch_driver.init_ch_database()
    while True:
        try:
            batches = []
            while len(batches) < batch_size:
                for msg in kafka_consumer:
                    value = json.loads(msg.value)
                    batches.append(transform(value))
            res = ch_driver.load(order_batches(batches))
            if not res:
                continue

        except KafkaError as kafka_error:
            logging.error("Got Kafka error: {0}".format(kafka_error))

        except Error as ch_error:
            logging.error("Got ClickHouse error: {0}".format(ch_error))


if __name__ == "__main__":
    config.dictConfig(LOGGING)
    settings = get_settings()
    consumer = ETLKafkaConsumer(**settings.kafka_settings.dict()).get_consumer()
    ch_driver = ETLClickhouseDriver(**settings.ch_settings.dict())
    run(consumer, ch_driver, batch_size=settings.app.batch_size)
