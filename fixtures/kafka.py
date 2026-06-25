from collections.abc import Iterator

import pytest

from clients.kafka.gateway.documents.client import (
    DocumentsKafkaGatewayClient,
    build_documents_kafka_gateway_client,
)


@pytest.fixture
def documents_kafka_gateway_client() -> Iterator[DocumentsKafkaGatewayClient]:
    client = build_documents_kafka_gateway_client()
    yield client
    client.close()
