from datetime import datetime
from enum import StrEnum

from pydantic import UUID4, Field, HttpUrl

from tools.fakers import fake
from tools.schema.schema_helpers import CamelCaseModel


class OperationType(StrEnum):
    FEE = "FEE"
    TOP_UP = "TOP_UP"
    CASHBACK = "CASHBACK"
    TRANSFER = "TRANSFER"
    PURCHASE = "PURCHASE"
    BILL_PAYMENT = "BILL_PAYMENT"
    CASH_WITHDRAWAL = "CASH_WITHDRAWAL"


class OperationStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    UNSPECIFIED = "UNSPECIFIED"


class OperationSchema(CamelCaseModel):
    id: UUID4
    type: OperationType
    status: OperationStatus
    amount: float
    card_id: UUID4
    category: str
    created_at: datetime
    account_id: UUID4


class ReceiptSchema(CamelCaseModel):
    url: HttpUrl
    document: str


class OperationsSummarySchema(CamelCaseModel):
    spent_amount: float
    received_amount: float
    cashback_amount: float


class GetOperationsQuerySchema(CamelCaseModel):
    account_id: UUID4


class GetOperationsSummaryQuerySchema(CamelCaseModel):
    account_id: UUID4


class MakeOperationRequestSchema(CamelCaseModel):
    status: OperationStatus = OperationStatus.IN_PROGRESS
    amount: float = Field(default_factory=fake.amount)
    card_id: UUID4
    account_id: UUID4


class MakeFeeOperationRequestSchema(MakeOperationRequestSchema): ...


class MakeTopUpOperationRequestSchema(MakeOperationRequestSchema): ...


class MakeCashbackOperationRequestSchema(MakeOperationRequestSchema): ...


class MakeTransferOperationRequestSchema(MakeOperationRequestSchema): ...


class MakeBillPaymentOperationRequestSchema(MakeOperationRequestSchema): ...


class MakeCashWithdrawalOperationRequestSchema(MakeOperationRequestSchema): ...


class MakePurchaseOperationRequestSchema(MakeOperationRequestSchema):
    category: str = Field(default_factory=fake.category)


class CreateOperationResponseSchema(CamelCaseModel):
    operation: OperationSchema


class GetOperationResponseSchema(CamelCaseModel):
    operation: OperationSchema


class GetOperationsResponseSchema(CamelCaseModel):
    operations: list[OperationSchema]


class GetOperationsSummaryResponseSchema(CamelCaseModel):
    summary: OperationsSummarySchema


class GetReceiptResponseSchema(CamelCaseModel):
    receipt: ReceiptSchema
