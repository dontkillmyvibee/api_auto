import pytest
from pydantic import UUID4, BaseModel

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


@pytest.fixture
def function_user(http_gateway_users_client: UsersGatewayHTTPClient) -> UserFixture:
    request = CreateUserRequestSchema()
    response = http_gateway_users_client.create_user(request)

    return UserFixture(request=request, response=response)
