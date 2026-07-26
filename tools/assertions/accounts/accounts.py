import allure
from pydantic import BaseModel, ConfigDict

from clients.http.gateway.accounts.schema import AccountStatus, AccountType, AccountViewSchema
from tools.assertions.base import assert_equal, assert_not_none
from tools.assertions.cards.cards import ExpectedCard, assert_cards
from tools.logger import get_logger

logger = get_logger("ACCOUNT_ASSERTIONS")


class ExpectedAccount(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: AccountType
    status: AccountStatus
    balance: float
    cards: list[ExpectedCard]


@allure.step("Assert account")
def assert_account(
    actual: AccountViewSchema,
    expected: ExpectedAccount,
) -> None:
    logger.info(f"Assert account {actual.id}")

    assert_not_none(actual.id, "id")
    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.status, expected.status, "status")
    assert_equal(actual.balance, expected.balance, "balance")

    assert_cards(
        actual.cards,
        expected.cards,
    )
