from datetime import datetime

from pydantic import UUID4

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
