from enum import StrEnum


class KafkaTopic(StrEnum):
    """Топики Kafka, используемые в тестах."""

    DOCUMENTS_TARIFFS = "documents-service.tariffs.inbox"
    DOCUMENTS_CONTRACTS = "documents-service.contracts.inbox"
    DOCUMENTS_RECEIPTS = "documents-service.receipts.inbox"
