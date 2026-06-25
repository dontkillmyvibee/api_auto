from pydantic import UUID4

from tools.schema.schema_helpers import KafkaEventSchema


class TariffDocumentEventSchema(KafkaEventSchema):
    """Событие топика documents-service.tariffs.inbox."""

    content: str
    account_id: UUID4


class ContractDocumentEventSchema(KafkaEventSchema):
    """Событие топика documents-service.contracts.inbox."""

    content: str
    account_id: UUID4


class ReceiptDocumentEventSchema(KafkaEventSchema):
    """Событие топика documents-service.receipts.inbox."""

    content: str
    operation_id: UUID4
