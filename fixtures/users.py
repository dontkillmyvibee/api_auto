import pytest

from clients.http.gateway.users.client import UsersGatewayHTTPClient, build_users_gateway_http_client


@pytest.fixture
def get_http_gateway_users_client() -> UsersGatewayHTTPClient:
    return build_users_gateway_http_client()
