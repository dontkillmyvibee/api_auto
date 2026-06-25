from datetime import date
from enum import StrEnum

from pydantic import UUID4

from tools.schema.schema_helpers import CamelCaseModel


class CardType(StrEnum):
    VIRTUAL = "VIRTUAL"
    PHYSICAL = "PHYSICAL"


class CardStatus(StrEnum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"
    BLOCKED = "BLOCKED"


class CardPaymentSystem(StrEnum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"


class CardSchema(CamelCaseModel):
    id: UUID4
    pin: str
    cvv: str
    type: CardType
    status: CardStatus
    account_id: UUID4
    card_number: str
    card_holder: str
    expiry_date: date
    payment_system: CardPaymentSystem


class IssueCardRequestSchema(CamelCaseModel):
    user_id: UUID4
    account_id: UUID4


class IssueVirtualCardRequestSchema(IssueCardRequestSchema): ...


class IssuePhysicalCardRequestSchema(IssueCardRequestSchema): ...


class IssueCardResponseSchema(CamelCaseModel):
    card: CardSchema


class IssueVirtualCardResponseSchema(IssueCardResponseSchema): ...


class IssuePhysicalCardResponseSchema(IssueCardResponseSchema): ...
