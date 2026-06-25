import pytest

from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient, build_accounts_gateway_http_client


@pytest.fixture
def get_http_gateway_account_client() -> AccountsGatewayHTTPClient:
    return build_accounts_gateway_http_client()
