from uuid import uuid4

from confluent_kafka import Consumer, Producer

from clients.kafka.consumer import KafkaConsumerClient
from clients.kafka.producer import KafkaProducerClient
from config import KafkaSettings


def build_kafka_consumer_client(topic: str) -> KafkaConsumerClient:
    """Создаёт консьюмер, подписанный на один топик.

    Каждому консьюмеру назначается уникальный group.id, поэтому он читает топик
    независимо от других (с позиции auto_offset_reset), не конкурируя за партиции.

    Args:
        topic (str): Имя топика (значение KafkaTopic).

    Returns:
        KafkaConsumerClient: Готовый к использованию консьюмер.
    """
    settings = KafkaSettings()
    consumer = Consumer(
        {
            "bootstrap.servers": settings.bootstrap_servers,
            "group.id": f"{settings.group_id}-{uuid4()}",
            "auto.offset.reset": settings.auto_offset_reset,
            "enable.auto.commit": True,
        }
    )
    consumer.subscribe([topic])
    return KafkaConsumerClient(consumer=consumer)


def build_kafka_producer_client() -> KafkaProducerClient:
    """Создаёт продьюсер Kafka.

    Returns:
        KafkaProducerClient: Готовый к использованию продьюсер.
    """
    settings = KafkaSettings()
    producer = Producer({"bootstrap.servers": settings.bootstrap_servers})
    return KafkaProducerClient(producer=producer)
