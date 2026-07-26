from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient
from clients.http.gateway.accounts.schema import OpenSavingsAccountRequestSchema
from fixtures.users import UserFixture
from tools.assertions.accounts.accounts import assert_account
from tools.assertions.accounts.templates import expected_savings_account


class TestOpenSavingsAccount:
    def test_open_savings_account(
        self, function_user: UserFixture, http_gateway_account_client: AccountsGatewayHTTPClient
    ) -> None:
        response = http_gateway_account_client.open_savings_account(
            OpenSavingsAccountRequestSchema(user_id=function_user.user_id)
        )

        assert_account(actual=response.account, expected=expected_savings_account())
