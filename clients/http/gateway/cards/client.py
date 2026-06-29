import allure
from requests import Response

from clients.http.client import HTTPClient
from clients.http.gateway.cards.schema import (
    IssuePhysicalCardRequestSchema,
    IssuePhysicalCardResponseSchema,
    IssueVirtualCardRequestSchema,
    IssueVirtualCardResponseSchema,
)
from clients.http.gateway.public_builder import get_public_http_client
from tools.assertions.http import assert_response_schema
from tools.http.http_routes import HTTPRoutes


class CardsGatewayHTTPClient:
    """
    Клиент для взаимодействия с /api/v1/cards сервиса http-gateway.
    """

    def __init__(self, client: HTTPClient):
        self.__client = client

    @allure.step("Issue virtual card")
    def issue_virtual_card_api(self, request: IssueVirtualCardRequestSchema) -> Response:
        """Выпуск виртуальной карты.

        Args:
            request(IssueVirtualCardRequestSchema): Pydantic-модель с данными для выпуска виртуальной карты.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(f"{HTTPRoutes.CARDS}/issue-virtual-card", json=request.to_dict())

    @allure.step("Issue physical card")
    def issue_physical_card_api(self, request: IssuePhysicalCardRequestSchema) -> Response:
        """Выпуск физической карты.

        Args:
            request(IssuePhysicalCardRequestSchema): Pydantic-модель с данными для выпуска физической карты.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(f"{HTTPRoutes.CARDS}/issue-physical-card", json=request.to_dict())

    def issue_virtual_card(self, request: IssueVirtualCardRequestSchema) -> IssueVirtualCardResponseSchema:
        response = self.issue_virtual_card_api(request)
        return assert_response_schema(response, IssueVirtualCardResponseSchema)

    def issue_physical_card(self, request: IssuePhysicalCardRequestSchema) -> IssuePhysicalCardResponseSchema:
        response = self.issue_physical_card_api(request)
        return assert_response_schema(response, IssuePhysicalCardResponseSchema)


def build_cards_gateway_http_client() -> CardsGatewayHTTPClient:
    """Функция создает экземпляр CardsGatewayHTTPClient с настроенным HTTPClient.

    Returns:
        CardsGatewayHTTPClient: Готовый к использованию CardsGatewayHTTPClient.

    """
    return CardsGatewayHTTPClient(client=get_public_http_client())
