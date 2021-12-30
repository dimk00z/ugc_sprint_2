from typing import Optional

from aiokafka import AIOKafkaProducer

aioproducer: Optional[AIOKafkaProducer] = None


async def get_aioproducer() -> Optional[AIOKafkaProducer]:
    return aioproducer
