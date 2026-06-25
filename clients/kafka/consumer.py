import json
import time
from collections.abc import Callable
from typing import Any

import allure
from confluent_kafka import Consumer

from tools.logger import get_logger

logger = get_logger("KAFKA_CONSUMER")

EventPredicate = Callable[[dict[str, Any]], bool]


class KafkaConsumerClient:
    """Низкоуровневый консьюмер: поллит топик до дедлайна и отдаёт первый JSON-payload,
    удовлетворяющий предикату.

    Один экземпляр подписан на один топик (offset продвигается независимо благодаря
    уникальному group.id, выставляемому в билдере).
    """

    def __init__(self, consumer: Consumer):
        self._consumer = consumer

    def consume(self, predicate: EventPredicate | None = None, timeout: float = 10.0) -> dict[str, Any] | None:
        """Ожидает сообщение, подходящее под предикат, в пределах таймаута.

        Args:
            predicate (EventPredicate | None): Условие на распарсенный payload. Если None —
                возвращается первое же сообщение.
            timeout (float): Максимальное время ожидания в секундах.

        Returns:
            dict[str, Any] | None: Распарсенный payload или None, если за таймаут ничего не пришло.
        """
        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            message = self._consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                logger.warning(f"Kafka consume error: {message.error()}")
                continue

            raw = message.value()
            if raw is None:
                continue

            value: dict[str, Any] = json.loads(raw)
            logger.info(f"Consumed from '{message.topic()}': {value}")

            if predicate is None or predicate(value):
                allure.attach(
                    json.dumps(value, ensure_ascii=False, indent=2),
                    f"Kafka message ({message.topic()})",
                    allure.attachment_type.JSON,
                )
                return value

        logger.warning(f"No matching message within {timeout}s")
        return None

    def close(self) -> None:
        """Закрывает консьюмер и освобождает ресурсы (отписка от группы)."""
        self._consumer.close()
