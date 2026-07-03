from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient
from clients.http.gateway.accounts.schema import GetAccountsQuerySchema
from fixtures.users import UserFixture
from tools.assertions.base import assert_length


class TestGetAccounts:
    def test_get_accounts(
        self, function_user: UserFixture, http_gateway_account_client: AccountsGatewayHTTPClient
    ) -> None:
        response = http_gateway_account_client.get_accounts(GetAccountsQuerySchema(user_id=function_user.user_id))

        assert_length(response.accounts, 0, "accounts")
