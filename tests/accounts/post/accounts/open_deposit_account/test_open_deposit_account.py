from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient
from clients.http.gateway.accounts.schema import OpenDepositAccountRequestSchema
from fixtures.users import UserFixture
from tools.assertions.accounts.accounts import assert_account
from tools.assertions.accounts.templates import expected_deposit_account


class TestOpenDepositAccount:
    def test_open_deposit_account(
        self, function_user: UserFixture, http_gateway_account_client: AccountsGatewayHTTPClient
    ) -> None:
        response = http_gateway_account_client.open_deposit_account(
            OpenDepositAccountRequestSchema(user_id=function_user.user_id)
        )

        assert_account(actual=response.account, expected=expected_deposit_account())
