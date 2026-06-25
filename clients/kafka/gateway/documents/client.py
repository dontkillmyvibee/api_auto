import allure

from clients.kafka.builder import build_kafka_consumer_client, build_kafka_producer_client
from clients.kafka.consumer import KafkaConsumerClient
from clients.kafka.gateway.documents.schema import (
    ContractDocumentEventSchema,
    ReceiptDocumentEventSchema,
    TariffDocumentEventSchema,
)
from clients.kafka.producer import KafkaProducerClient
from tools.kafka.topics import KafkaTopic


class DocumentsKafkaGatewayClient:
    """Клиент для работы с событиями documents-сервиса в Kafka.

    consume_* — дождаться публикации события (основной сценарий: проверить, что
    после действия в API событие улетело в топик). publish_* — опубликовать событие
    (для тестов самого documents-сервиса, который эти топики потребляет).
    """

    def __init__(
        self,
        producer: KafkaProducerClient,
        tariffs_consumer: KafkaConsumerClient,
        contracts_consumer: KafkaConsumerClient,
        receipts_consumer: KafkaConsumerClient,
    ):
        self._producer = producer
        self._tariffs_consumer = tariffs_consumer
        self._contracts_consumer = contracts_consumer
        self._receipts_consumer = receipts_consumer

    @allure.step('Consume tariff document event by account id "{account_id}"')
    def consume_tariff_document_event(self, account_id: str, timeout: float = 10.0) -> TariffDocumentEventSchema | None:
        """Ожидает событие тарифа по account_id."""
        value = self._tariffs_consumer.consume(lambda v: v.get("account_id") == account_id, timeout)
        return TariffDocumentEventSchema.model_validate(value) if value else None

    @allure.step('Consume contract document event by account id "{account_id}"')
    def consume_contract_document_event(
        self, account_id: str, timeout: float = 10.0
    ) -> ContractDocumentEventSchema | None:
        """Ожидает событие договора по account_id."""
        value = self._contracts_consumer.consume(lambda v: v.get("account_id") == account_id, timeout)
        return ContractDocumentEventSchema.model_validate(value) if value else None

    @allure.step('Consume receipt document event by operation id "{operation_id}"')
    def consume_receipt_document_event(
        self, operation_id: str, timeout: float = 10.0
    ) -> ReceiptDocumentEventSchema | None:
        """Ожидает событие чека по operation_id."""
        value = self._receipts_consumer.consume(lambda v: v.get("operation_id") == operation_id, timeout)
        return ReceiptDocumentEventSchema.model_validate(value) if value else None

    @allure.step("Publish tariff document event")
    def publish_tariff_document_event(self, event: TariffDocumentEventSchema) -> None:
        """Публикует событие тарифа в documents-service.tariffs.inbox."""
        self._producer.publish(KafkaTopic.DOCUMENTS_TARIFFS, event)

    @allure.step("Publish contract document event")
    def publish_contract_document_event(self, event: ContractDocumentEventSchema) -> None:
        """Публикует событие договора в documents-service.contracts.inbox."""
        self._producer.publish(KafkaTopic.DOCUMENTS_CONTRACTS, event)

    @allure.step("Publish receipt document event")
    def publish_receipt_document_event(self, event: ReceiptDocumentEventSchema) -> None:
        """Публикует событие чека в documents-service.receipts.inbox."""
        self._producer.publish(KafkaTopic.DOCUMENTS_RECEIPTS, event)

    def close(self) -> None:
        """Закрывает все консьюмеры клиента."""
        self._tariffs_consumer.close()
        self._contracts_consumer.close()
        self._receipts_consumer.close()


def build_documents_kafka_gateway_client() -> DocumentsKafkaGatewayClient:
    """Создаёт DocumentsKafkaGatewayClient с продьюсером и консьюмерами на все documents-топики.

    Returns:
        DocumentsKafkaGatewayClient: Готовый к использованию клиент.
    """
    return DocumentsKafkaGatewayClient(
        producer=build_kafka_producer_client(),
        tariffs_consumer=build_kafka_consumer_client(KafkaTopic.DOCUMENTS_TARIFFS),
        contracts_consumer=build_kafka_consumer_client(KafkaTopic.DOCUMENTS_CONTRACTS),
        receipts_consumer=build_kafka_consumer_client(KafkaTopic.DOCUMENTS_RECEIPTS),
    )
