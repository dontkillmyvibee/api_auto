from datetime import date

import allure
from pydantic import UUID4, BaseModel, ConfigDict

from clients.http.gateway.cards.schema import CardPaymentSystem, CardSchema, CardStatus, CardType
from tools.assertions.base import assert_equal, assert_length, assert_not_none
from tools.logger import get_logger

logger = get_logger("CARD_ASSERTIONS")


class ExpectedCard(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: CardType
    status: CardStatus
    account_id: UUID4
    card_holder: str
    expiry_date: date
    payment_system: CardPaymentSystem


@allure.step("Assert card")
def assert_card(
    actual: CardSchema,
    expected: ExpectedCard,
) -> None:
    logger.info(f"Assert card {actual.id}")

    assert_not_none(actual.id, "id")
    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.status, expected.status, "status")
    assert_equal(actual.account_id, expected.account_id, "account_id")
    assert_equal(actual.card_holder, expected.card_holder, "card_holder")
    assert_equal(actual.expiry_date, expected.expiry_date, "expiry_date")
    assert_equal(actual.payment_system, expected.payment_system, "payment_system")


@allure.step("Assert cards")
def assert_cards(
    actual: list[CardSchema],
    expected: list[ExpectedCard],
) -> None:
    logger.info("Assert cards")

    assert_length(actual, len(expected), "cards")

    for actual_card, expected_card in zip(actual, expected, strict=True):
        assert_card(actual_card, expected_card)
