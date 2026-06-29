from http import HTTPStatus

import pytest

from clients.http.gateway.users.client import UsersGatewayHTTPClient
from clients.http.gateway.users.schema import CreateUserRequestSchema
from tools.assertions.http import assert_status_code
from tools.assertions.users import assert_create_user_response
from tools.fakers import fake


@pytest.mark.http_api
@pytest.mark.users
@pytest.mark.regression
class TestCreateUser:
    @pytest.mark.parametrize("domain", ["mail.ru", "gmail.com", "icloud.com", "outlook.com", "example.com"])
    def test_create_user(self, domain: str, http_gateway_users_client: UsersGatewayHTTPClient) -> None:
        request = CreateUserRequestSchema(email=fake.email(domain=domain))
        response = http_gateway_users_client.create_user(request=request)

        assert_create_user_response(request, response)


class TestCreateUserNegative:
    @pytest.mark.parametrize(
        "email",
        [
            "without_domain@",
            "without_specsgmail.com",
            "outlook.com",
            "",
            "1",
            "@gmail.com",
        ],
    )
    def test_create_user_with_invalid_email(
        self, email: str, http_gateway_users_client: UsersGatewayHTTPClient
    ) -> None:
        request = CreateUserRequestSchema.model_construct(email=email)
        response = http_gateway_users_client.create_user_api(request=request)

        assert_status_code(response, HTTPStatus.UNPROCESSABLE_ENTITY)
