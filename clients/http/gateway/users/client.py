import allure
from requests import Response

from clients.http.client import HTTPClient
from clients.http.gateway.public_builder import get_public_http_client
from clients.http.gateway.users.schema import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
    GetUserResponseSchema,
)
from tools.assertions.http import assert_response_schema
from tools.http.http_routes import HTTPRoutes


class UsersGatewayHTTPClient:
    """
    Клиент для взаимодействия с /api/v1/users сервиса http-gateway.
    """

    def __init__(self, client: HTTPClient):
        self.__client = client

    @allure.step('Get user by id "{user_id}"')
    def get_user_api(self, user_id: str) -> Response:
        """Метод получения юзера.

        Args:
            user_id(str): Идентификатор пользователя.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.get(f"{HTTPRoutes.USERS}/{user_id}")

    @allure.step("Create user")
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """Метод создания юзера.

        Args:
            request(CreateUserRequestSchema): Запрос на сервер в виде объекта CreateUserRequestSchema.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(HTTPRoutes.USERS, json=request.to_dict())

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        """Высокоуровневый метод получения юзера.

        Args:
            user_id (str): Идентификатор пользователя.

        Returns:
            GetUserResponseSchema: Ответ от сервера в виде объекта GetUserResponseSchema.
        """
        response = self.get_user_api(user_id)
        return assert_response_schema(response, GetUserResponseSchema)

    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        """Высокоуровневый метод создания юзера.

        Args:
            request(CreateUserRequestSchema): Запрос на сервер в виде объекта CreateUserRequestSchema.

        Returns:
            CreateUserResponseSchema: Ответ от сервера в виде объекта CreateUserResponseSchema.

        """
        response = self.create_user_api(request)
        return assert_response_schema(response, CreateUserResponseSchema)


def build_users_gateway_http_client() -> UsersGatewayHTTPClient:
    """Функция создает экземпляр UsersGatewayHTTPClient с настроенным HTTPClient.

    Returns:
        UsersGatewayHTTPClient: Готовый к использованию UsersGatewayHTTPClient.

    """
    return UsersGatewayHTTPClient(client=get_public_http_client())
