from datetime import date, timedelta

from pydantic import UUID4

from clients.http.gateway.accounts.schema import AccountStatus, AccountType
from clients.http.gateway.cards.schema import CardPaymentSystem, CardStatus, CardType
from tools.assertions.accounts.accounts import ExpectedAccount
from tools.assertions.cards.cards import ExpectedCard


def expected_debit_account(
    account_id: UUID4,
    card_holder: str,
) -> ExpectedAccount:
    return ExpectedAccount(
        type=AccountType.DEBIT_CARD,
        status=AccountStatus.ACTIVE,
        balance=0.0,
        cards=[
            ExpectedCard(
                type=CardType.VIRTUAL,
                status=CardStatus.ACTIVE,
                account_id=account_id,
                card_holder=card_holder,
                expiry_date=date.today() + timedelta(days=365 * 7),
                payment_system=CardPaymentSystem.MASTERCARD,
            ),
            ExpectedCard(
                type=CardType.PHYSICAL,
                status=CardStatus.ACTIVE,
                account_id=account_id,
                card_holder=card_holder,
                expiry_date=date.today() + timedelta(days=365 * 7),
                payment_system=CardPaymentSystem.MASTERCARD,
            ),
        ],
    )


def expected_deposit_account() -> ExpectedAccount:
    return ExpectedAccount(type=AccountType.DEPOSIT, cards=[], status=AccountStatus.ACTIVE, balance=0.0)


def expected_savings_account() -> ExpectedAccount:
    return ExpectedAccount(type=AccountType.SAVINGS, cards=[], status=AccountStatus.ACTIVE, balance=0.0)


def expected_credit_account(
    account_id: UUID4,
    card_holder: str,
) -> ExpectedAccount:
    return ExpectedAccount(
        type=AccountType.CREDIT_CARD,
        status=AccountStatus.ACTIVE,
        balance=25000.0,
        cards=[
            ExpectedCard(
                type=CardType.VIRTUAL,
                status=CardStatus.ACTIVE,
                account_id=account_id,
                card_holder=card_holder,
                expiry_date=date.today() + timedelta(days=365 * 7),
                payment_system=CardPaymentSystem.MASTERCARD,
            ),
            ExpectedCard(
                type=CardType.PHYSICAL,
                status=CardStatus.ACTIVE,
                account_id=account_id,
                card_holder=card_holder,
                expiry_date=date.today() + timedelta(days=365 * 7),
                payment_system=CardPaymentSystem.MASTERCARD,
            ),
        ],
    )
