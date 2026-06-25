import allure
from confluent_kafka import Producer

from tools.logger import get_logger
from tools.schema.schema_helpers import KafkaEventSchema

logger = get_logger("KAFKA_PRODUCER")


class KafkaProducerClient:
    """Низкоуровневый продьюсер: публикует Pydantic-событие в топик как JSON."""

    def __init__(self, producer: Producer):
        self._producer = producer

    def publish(self, topic: str, event: KafkaEventSchema, key: str | None = None) -> None:
        """Публикует событие в топик и дожидается доставки (flush).

        Args:
            topic (str): Имя топика (значение KafkaTopic).
            event (KafkaEventSchema): Событие-схема, сериализуется в JSON-байты.
            key (str | None): Ключ сообщения (опционально).
        """
        payload = event.to_json_bytes()
        logger.info(f"Publish to '{topic}': {payload.decode('utf-8')}")
        allure.attach(payload.decode("utf-8"), f"Kafka publish ({topic})", allure.attachment_type.JSON)

        key_bytes = key.encode("utf-8") if key is not None else None
        self._producer.produce(topic=topic, value=payload, key=key_bytes)
        self._producer.flush(timeout=10.0)
