import pytest

from clients.http.gateway.operations.client import OperationsGatewayHTTPClient, build_operations_gateway_http_client


@pytest.fixture
def get_http_gateway_operations_client() -> OperationsGatewayHTTPClient:
    return build_operations_gateway_http_client()
