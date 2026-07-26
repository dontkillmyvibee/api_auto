from datetime import date, timedelta

from pydantic import UUID4

from clients.http.gateway.cards.schema import CardPaymentSystem, CardStatus, CardType
from tools.assertions.cards.cards import ExpectedCard


def expected_card(card_type: CardType, account_id: UUID4, card_holder: str) -> ExpectedCard:
    return ExpectedCard(
        type=card_type,
        status=CardStatus.ACTIVE,
        account_id=account_id,
        card_holder=card_holder,
        expiry_date=date.today() + timedelta(days=365 * 7),
        payment_system=CardPaymentSystem.MASTERCARD,
    )
