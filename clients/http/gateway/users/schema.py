from pydantic import UUID4, EmailStr, Field

from tools.fakers import fake
from tools.schema.schema_helpers import CamelCaseModel


class UserSchema(CamelCaseModel):
    id: UUID4
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str
    phone_number: str


class GetUserResponseSchema(CamelCaseModel):
    user: UserSchema


class CreateUserRequestSchema(CamelCaseModel):
    email: EmailStr = Field(default_factory=fake.email)
    last_name: str = Field(default_factory=fake.last_name)
    first_name: str = Field(default_factory=fake.first_name)
    middle_name: str = Field(default_factory=fake.middle_name)
    phone_number: str = Field(default_factory=fake.phone_number)


class CreateUserResponseSchema(GetUserResponseSchema): ...
