import pytest

from clients.http.gateway.documents.client import DocumentsGatewayHTTPClient, build_documents_gateway_http_client


@pytest.fixture
def get_http_gateway_documents_client() -> DocumentsGatewayHTTPClient:
    return build_documents_gateway_http_client()
