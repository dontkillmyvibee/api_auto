import allure
from requests import Response

from clients.http.client import HTTPClient
from clients.http.gateway.documents.schema import (
    GetContractDocumentResponseSchema,
    GetTariffDocumentResponseSchema,
)
from clients.http.gateway.public_builder import get_public_http_client
from tools.http.http_routes import HTTPRoutes


class DocumentsGatewayHTTPClient:
    """
    Клиент для взаимодействия с /api/v1/documents сервиса http-gateway.
    """

    def __init__(self, client: HTTPClient):
        self.__client = client

    @allure.step('Get tariff document by account id "{account_id}"')
    def get_tariff_document_api(self, account_id: str) -> Response:
        """Выполняет GET-запрос на получение тарифного документа по счёту.

        Args:
            account_id(str): Идентификатор счёта.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.get(f"{HTTPRoutes.DOCUMENTS}/tariff-document/{account_id}")

    @allure.step('Get contract document by account id "{account_id}"')
    def get_contract_document_api(self, account_id: str) -> Response:
        """Выполняет GET-запрос на получение договора по счёту.

        Args:
            account_id(str): Идентификатор счёта.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.get(f"{HTTPRoutes.DOCUMENTS}/contract-document/{account_id}")

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseSchema:
        response = self.get_tariff_document_api(account_id)
        return GetTariffDocumentResponseSchema.model_validate_json(response.text)

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseSchema:
        response = self.get_contract_document_api(account_id)
        return GetContractDocumentResponseSchema.model_validate_json(response.text)


def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """Функция создает экземпляр DocumentsGatewayHTTPClient с настроенным HTTPClient.

    Returns:
        DocumentsGatewayHTTPClient: Готовый к использованию DocumentsGatewayHTTPClient.

    """
    return DocumentsGatewayHTTPClient(client=get_public_http_client())
