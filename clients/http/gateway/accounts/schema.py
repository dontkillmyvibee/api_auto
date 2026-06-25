from enum import StrEnum

from pydantic import UUID4

from clients.http.gateway.cards.schema import CardSchema
from tools.schema.schema_helpers import CamelCaseModel


class AccountType(StrEnum):
    DEPOSIT = "DEPOSIT"
    SAVINGS = "SAVINGS"
    DEBIT_CARD = "DEBIT_CARD"
    CREDIT_CARD = "CREDIT_CARD"


class AccountStatus(StrEnum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    PENDING_CLOSURE = "PENDING_CLOSURE"


class AccountViewSchema(CamelCaseModel):
    id: UUID4
    type: AccountType
    cards: list[CardSchema]
    status: AccountStatus
    balance: float


class GetAccountsQuerySchema(CamelCaseModel):
    user_id: UUID4


class GetAccountsResponseSchema(CamelCaseModel):
    accounts: list[AccountViewSchema]


class OpenAccountRequestSchema(CamelCaseModel):
    user_id: UUID4


class OpenAccountResponseSchema(CamelCaseModel):
    account: AccountViewSchema


class OpenDepositAccountRequestSchema(OpenAccountRequestSchema): ...


class OpenDepositAccountResponseSchema(OpenAccountResponseSchema): ...


class OpenSavingsAccountRequestSchema(OpenAccountRequestSchema): ...


class OpenSavingsAccountResponseSchema(OpenAccountResponseSchema): ...


class OpenDebitCardAccountRequestSchema(OpenAccountRequestSchema): ...


class OpenDebitCardAccountResponseSchema(OpenAccountResponseSchema): ...


class OpenCreditCardAccountRequestSchema(OpenAccountRequestSchema): ...


class OpenCreditCardAccountResponseSchema(OpenAccountResponseSchema): ...
