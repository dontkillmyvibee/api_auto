import allure
from requests import Response

from clients.http.client import HTTPClient
from clients.http.gateway.accounts.schema import (
    GetAccountsQuerySchema,
    GetAccountsResponseSchema,
    OpenCreditCardAccountRequestSchema,
    OpenCreditCardAccountResponseSchema,
    OpenDebitCardAccountRequestSchema,
    OpenDebitCardAccountResponseSchema,
    OpenDepositAccountRequestSchema,
    OpenDepositAccountResponseSchema,
    OpenSavingsAccountRequestSchema,
    OpenSavingsAccountResponseSchema,
)
from clients.http.gateway.public_builder import get_public_http_client
from tools.http.http_routes import HTTPRoutes


class AccountsGatewayHTTPClient:
    """
    Клиент для взаимодействия с /api/v1/accounts сервиса http-gateway.
    """

    def __init__(self, client: HTTPClient):
        self.__client = client

    @allure.step("Get accounts by {query.user_id}")
    def get_accounts_api(self, query: GetAccountsQuerySchema) -> Response:
        """Выполняет GET-запрос на получение списка счетов пользователя.

        Args:
            query(GetAccountsQuerySchema): Pydantic-модель с user_id.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.get(HTTPRoutes.ACCOUNTS, params=query.to_dict())

    @allure.step("Open deposit account")
    def open_deposit_account_api(self, request: OpenDepositAccountRequestSchema) -> Response:
        """Выполняет POST-запрос для открытия депозитного счёта.

        Args:
            request(OpenDepositAccountRequestSchema): Pydantic-модель с userId.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(f"{HTTPRoutes.ACCOUNTS}/open-deposit-account", json=request.to_dict())

    @allure.step("Open saving account")
    def open_savings_account_api(self, request: OpenSavingsAccountRequestSchema) -> Response:
        """Выполняет POST-запрос для открытия сберегательного счёта.

        Args:
            request(OpenSavingsAccountRequestSchema): Pydantic-модель с userId.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(f"{HTTPRoutes.ACCOUNTS}/open-savings-account", json=request.to_dict())

    @allure.step("Open debit card account")
    def open_debit_card_account_api(self, request: OpenDebitCardAccountRequestSchema) -> Response:
        """Выполняет POST-запрос для открытия дебетовой карты.

        Args:
            request(OpenDebitCardAccountRequestSchema): Pydantic-модель с userId.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(f"{HTTPRoutes.ACCOUNTS}/open-debit-card-account", json=request.to_dict())

    @allure.step("Open credit card account")
    def open_credit_card_account_api(self, request: OpenCreditCardAccountRequestSchema) -> Response:
        """Выполняет POST-запрос для открытия кредитной карты.

        Args:
            request(OpenCreditCardAccountRequestSchema): Pydantic-модель с userId.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(f"{HTTPRoutes.ACCOUNTS}/open-credit-card-account", json=request.to_dict())

    def get_accounts(self, query: GetAccountsQuerySchema) -> GetAccountsResponseSchema:
        response = self.get_accounts_api(query)
        return GetAccountsResponseSchema.model_validate_json(response.text)

    def open_deposit_account(self, request: OpenDepositAccountRequestSchema) -> OpenDepositAccountResponseSchema:
        response = self.open_deposit_account_api(request)
        return OpenDepositAccountResponseSchema.model_validate_json(response.text)

    def open_savings_account(self, request: OpenSavingsAccountRequestSchema) -> OpenSavingsAccountResponseSchema:
        response = self.open_savings_account_api(request)
        return OpenSavingsAccountResponseSchema.model_validate_json(response.text)

    def open_debit_card_account(self, request: OpenDebitCardAccountRequestSchema) -> OpenDebitCardAccountResponseSchema:
        response = self.open_debit_card_account_api(request)
        return OpenDebitCardAccountResponseSchema.model_validate_json(response.text)

    def open_credit_card_account(
        self, request: OpenCreditCardAccountRequestSchema
    ) -> OpenCreditCardAccountResponseSchema:
        response = self.open_credit_card_account_api(request)
        return OpenCreditCardAccountResponseSchema.model_validate_json(response.text)


def build_accounts_gateway_http_client() -> AccountsGatewayHTTPClient:
    """Функция создает экземпляр AccountsGatewayHTTPClient с настроенным HTTPClient.

    Returns:
        AccountsGatewayHTTPClient: Готовый к использованию AccountsGatewayHTTPClient.

    """
    return AccountsGatewayHTTPClient(client=get_public_http_client())
