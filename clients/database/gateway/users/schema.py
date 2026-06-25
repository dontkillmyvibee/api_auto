from pydantic import UUID4, EmailStr

from tools.schema.schema_helpers import DatabaseSchema


class UsersTableSchema(DatabaseSchema):
    """Строка таблицы users_service_db.public.users."""

    id: UUID4
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str
    phone_number: str
