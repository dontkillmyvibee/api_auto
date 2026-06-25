from pydantic import UUID4

from tools.schema.schema_helpers import DatabaseSchema


class AccountsTableSchema(DatabaseSchema):
    """Строка таблицы accounts_service_db.public.accounts."""

    id: UUID4
    type: str
    status: str
    user_id: UUID4
    balance: float
