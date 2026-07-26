from clients.http.gateway.accounts.schema import AccountType
from clients.http.gateway.cards.client import CardsGatewayHTTPClient
from clients.http.gateway.cards.schema import CardType, IssueVirtualCardRequestSchema
from fixtures.accounts import AccountFactory
from tools.assertions.cards.cards import assert_card
from tools.assertions.cards.templates import expected_card


class TestIssueVirtualCard:
    def test_issue_virtual_card(
        self, account_factory: AccountFactory, http_gateway_cards_client: CardsGatewayHTTPClient
    ) -> None:
        account = account_factory(AccountType.DEBIT_CARD)

        response = http_gateway_cards_client.issue_virtual_card(
            IssueVirtualCardRequestSchema(user_id=account.user.user_id, account_id=account.account_id)
        )

        assert_card(
            response.card,
            expected_card(
                card_type=CardType.VIRTUAL, account_id=account.account_id, card_holder=account.user.response_full_name
            ),
        )
