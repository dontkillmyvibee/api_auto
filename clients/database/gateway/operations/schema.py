from datetime import datetime

from pydantic import UUID4, Field

from tools.fakers import fake
from tools.schema.schema_helpers import DatabaseSchema


class OperationsTableSchema(DatabaseSchema):
    """Строка таблицы operations_service_db.public.operations."""

    id: UUID4
    type: str
    status: str
    amount: float
    card_id: UUID4
    category: str
    created_at: datetime
    account_id: UUID4


class CreateOperationsTableSchema(DatabaseSchema):
    """Builder строки operations для seed через БД.

    Все поля имеют defaults — в тесте передаются только overrides
    (например account_id/card_id для связанных сценариев).
    """

    id: UUID4 = Field(default_factory=fake.uuid)
    type: str = "PURCHASE"
    status: str = "IN_PROGRESS"
    amount: float = Field(default_factory=fake.amount)
    card_id: UUID4 = Field(default_factory=fake.uuid)
    category: str = Field(default_factory=fake.category)
    created_at: datetime = Field(default_factory=fake.date_time)
    account_id: UUID4 = Field(default_factory=fake.uuid)
