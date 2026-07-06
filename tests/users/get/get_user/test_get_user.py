from http import HTTPStatus

from clients.http.gateway.users.client import UsersGatewayHTTPClient
from fixtures.users import UserFixture
from tools.assertions.http import assert_status_code
from tools.assertions.users import assert_get_user_response, assert_user_not_found
from tools.fakers import fake


class TestGetUser:
    def test_get_user(self, http_gateway_users_client: UsersGatewayHTTPClient, function_user: UserFixture) -> None:
        response = http_gateway_users_client.get_user(user_id=function_user.user_id)

        assert_get_user_response(user=function_user, response=response)


class TestGetUserNegative:
    def test_get_user_with_invalid_user_id(self, http_gateway_users_client: UsersGatewayHTTPClient) -> None:
        user_id = fake.uuid4()
        response = http_gateway_users_client.get_user_api(user_id=user_id)

        assert_status_code(response=response, expected=HTTPStatus.NOT_FOUND)
        assert_user_not_found(actual=response, user_id=user_id)
