import pytest

from clients.http.gateway.cards.client import CardsGatewayHTTPClient, build_cards_gateway_http_client


@pytest.fixture
def get_http_gateway_cards_client() -> CardsGatewayHTTPClient:
    return build_cards_gateway_http_client()
