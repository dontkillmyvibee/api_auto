from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient
from clients.http.gateway.accounts.schema import OpenCreditCardAccountRequestSchema
from fixtures.users import UserFixture
from tools.assertions.accounts.accounts import assert_account
from tools.assertions.accounts.templates import expected_credit_account


class TestOpenCreditCardAccount:
    def test_open_credit_card_account(
        self,
        function_user: UserFixture,
        http_gateway_account_client: AccountsGatewayHTTPClient,
    ) -> None:
        response = http_gateway_account_client.open_credit_card_account(
            OpenCreditCardAccountRequestSchema(
                user_id=function_user.user_id,
            )
        )

        assert_account(
            actual=response.account,
            expected=expected_credit_account(
                account_id=response.account.id,
                card_holder=function_user.response_full_name,
            ),
        )
