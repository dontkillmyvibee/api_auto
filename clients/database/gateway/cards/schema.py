from datetime import date

from pydantic import UUID4

from tools.schema.schema_helpers import DatabaseSchema


class CardsTableSchema(DatabaseSchema):
    """Строка таблицы cards_service_db.public.cards."""

    id: UUID4
    pin: str
    cvv: str
    type: str
    status: str
    account_id: UUID4
    card_number: str
    card_holder: str
    expiry_date: date
    payment_system: str
