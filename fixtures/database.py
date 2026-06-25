import pytest

from clients.database.gateway.accounts.client import (
    AccountsGatewayDatabaseClient,
    build_accounts_gateway_database_client,
)
from clients.database.gateway.cards.client import (
    CardsGatewayDatabaseClient,
    build_cards_gateway_database_client,
)
from clients.database.gateway.operations.client import (
    OperationsGatewayDatabaseClient,
    build_operations_gateway_database_client,
)
from clients.database.gateway.users.client import (
    UsersGatewayDatabaseClient,
    build_users_gateway_database_client,
)


@pytest.fixture
def users_gateway_database_client() -> UsersGatewayDatabaseClient:
    return build_users_gateway_database_client()


@pytest.fixture
def accounts_gateway_database_client() -> AccountsGatewayDatabaseClient:
    return build_accounts_gateway_database_client()


@pytest.fixture
def cards_gateway_database_client() -> CardsGatewayDatabaseClient:
    return build_cards_gateway_database_client()


@pytest.fixture
def operations_gateway_database_client() -> OperationsGatewayDatabaseClient:
    return build_operations_gateway_database_client()
