import pytest
from pydantic import UUID4, BaseModel, EmailStr

from clients.http.gateway.users.client import UsersGatewayHTTPClient, build_users_gateway_http_client
from clients.http.gateway.users.schema import CreateUserRequestSchema, CreateUserResponseSchema


@pytest.fixture
def http_gateway_users_client() -> UsersGatewayHTTPClient:
    return build_users_gateway_http_client()


class UserFixture(BaseModel):
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema

    @property
    def user_id(self) -> UUID4:
        return self.response.user.id

    @property
    def response_email(self) -> EmailStr:
        return self.response.user.email

    @property
    def response_last_name(self) -> str:
        return self.response.user.last_name

    @property
    def response_first_name(self) -> str:
        return self.response.user.first_name

    @property
    def response_middle_name(self) -> str:
        return self.response.user.middle_name

    @property
    def response_phone_number(self) -> str:
        return self.response.user.phone_number


@pytest.fixture
def function_user(http_gateway_users_client: UsersGatewayHTTPClient) -> UserFixture:
    request = CreateUserRequestSchema()
    response = http_gateway_users_client.create_user(request)

    return UserFixture(request=request, response=response)
