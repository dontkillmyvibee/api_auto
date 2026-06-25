import allure
from requests import Response

from clients.http.client import HTTPClient
from clients.http.gateway.operations.schema import (
    CreateOperationResponseSchema,
    GetOperationResponseSchema,
    GetOperationsQuerySchema,
    GetOperationsResponseSchema,
    GetOperationsSummaryQuerySchema,
    GetOperationsSummaryResponseSchema,
    GetReceiptResponseSchema,
    MakeBillPaymentOperationRequestSchema,
    MakeCashbackOperationRequestSchema,
    MakeCashWithdrawalOperationRequestSchema,
    MakeFeeOperationRequestSchema,
    MakePurchaseOperationRequestSchema,
    MakeTopUpOperationRequestSchema,
    MakeTransferOperationRequestSchema,
)
from clients.http.gateway.public_builder import get_public_http_client
from tools.http.http_routes import HTTPRoutes


class OperationsGatewayHTTPClient:
    """
    Клиент для взаимодействия с /api/v1/operations сервиса http-gateway.
    """

    def __init__(self, client: HTTPClient):
        self.__client = client

    @allure.step("Get operations by {query.account_id}")
    def get_operations_api(self, query: GetOperationsQuerySchema) -> Response:
        """Выполняет GET-запрос на получение списка операций по счёту.

        Args:
            query(GetOperationsQuerySchema): Pydantic-модель с accountId.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.get(HTTPRoutes.OPERATIONS, params=query.to_dict())

    @allure.step("Get operations summary by {query.account_id}")
    def get_operations_summary_api(self, query: GetOperationsSummaryQuerySchema) -> Response:
        """Выполняет GET-запрос на получение статистики операций по счёту.

        Args:
            query(GetOperationsSummaryQuerySchema): Pydantic-модель с accountId.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.get(f"{HTTPRoutes.OPERATIONS}/operations-summary", params=query.to_dict())

    @allure.step('Get operation receipt by id "{operation_id}"')
    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """Выполняет GET-запрос на получение чека по операции.

        Args:
            operation_id(str): Идентификатор операции.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.get(f"{HTTPRoutes.OPERATIONS}/operation-receipt/{operation_id}")

    @allure.step('Get operation by id "{operation_id}"')
    def get_operation_api(self, operation_id: str) -> Response:
        """Выполняет GET-запрос на получение операции по идентификатору.

        Args:
            operation_id(str): Идентификатор операции.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.get(f"{HTTPRoutes.OPERATIONS}/{operation_id}")

    @allure.step("Make fee operation")
    def make_fee_operation_api(self, request: MakeFeeOperationRequestSchema) -> Response:
        """Выполняет POST-запрос для создания операции комиссии.

        Args:
            request(MakeFeeOperationRequestSchema): Pydantic-модель с данными операции.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(f"{HTTPRoutes.OPERATIONS}/make-fee-operation", json=request.to_dict())

    @allure.step("Make top up operation")
    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestSchema) -> Response:
        """Выполняет POST-запрос для создания операции пополнения.

        Args:
            request(MakeTopUpOperationRequestSchema): Pydantic-модель с данными операции.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(f"{HTTPRoutes.OPERATIONS}/make-top-up-operation", json=request.to_dict())

    @allure.step("Make cashback operation")
    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestSchema) -> Response:
        """Выполняет POST-запрос для создания операции кэшбэка.

        Args:
            request(MakeCashbackOperationRequestSchema): Pydantic-модель с данными операции.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(f"{HTTPRoutes.OPERATIONS}/make-cashback-operation", json=request.to_dict())

    @allure.step("Make transfer operation")
    def make_transfer_operation_api(self, request: MakeTransferOperationRequestSchema) -> Response:
        """Выполняет POST-запрос для создания операции перевода.

        Args:
            request(MakeTransferOperationRequestSchema): Pydantic-модель с данными операции.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(f"{HTTPRoutes.OPERATIONS}/make-transfer-operation", json=request.to_dict())

    @allure.step("Make purchase operation")
    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestSchema) -> Response:
        """Выполняет POST-запрос для создания операции покупки.

        Args:
            request(MakePurchaseOperationRequestSchema): Pydantic-модель с данными операции.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(f"{HTTPRoutes.OPERATIONS}/make-purchase-operation", json=request.to_dict())

    @allure.step("Make bill payment operation")
    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestSchema) -> Response:
        """Выполняет POST-запрос для создания операции оплаты по счёту.

        Args:
            request(MakeBillPaymentOperationRequestSchema): Pydantic-модель с данными операции.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(f"{HTTPRoutes.OPERATIONS}/make-bill-payment-operation", json=request.to_dict())

    @allure.step("Make cash withdrawal operation")
    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestSchema) -> Response:
        """Выполняет POST-запрос для создания операции снятия наличных.

        Args:
            request(MakeCashWithdrawalOperationRequestSchema): Pydantic-модель с данными операции.

        Returns:
            Response: Ответ от сервера в виде объекта Response.

        """
        return self.__client.post(f"{HTTPRoutes.OPERATIONS}/make-cash-withdrawal-operation", json=request.to_dict())

    def get_operations(self, query: GetOperationsQuerySchema) -> GetOperationsResponseSchema:
        response = self.get_operations_api(query)
        return GetOperationsResponseSchema.model_validate_json(response.text)

    def get_operations_summary(self, query: GetOperationsSummaryQuerySchema) -> GetOperationsSummaryResponseSchema:
        response = self.get_operations_summary_api(query)
        return GetOperationsSummaryResponseSchema.model_validate_json(response.text)

    def get_operation_receipt(self, operation_id: str) -> GetReceiptResponseSchema:
        response = self.get_operation_receipt_api(operation_id)
        return GetReceiptResponseSchema.model_validate_json(response.text)

    def get_operation(self, operation_id: str) -> GetOperationResponseSchema:
        response = self.get_operation_api(operation_id)
        return GetOperationResponseSchema.model_validate_json(response.text)

    def make_fee_operation(self, request: MakeFeeOperationRequestSchema) -> CreateOperationResponseSchema:
        response = self.make_fee_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)

    def make_top_up_operation(self, request: MakeTopUpOperationRequestSchema) -> CreateOperationResponseSchema:
        response = self.make_top_up_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)

    def make_cashback_operation(self, request: MakeCashbackOperationRequestSchema) -> CreateOperationResponseSchema:
        response = self.make_cashback_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)

    def make_transfer_operation(self, request: MakeTransferOperationRequestSchema) -> CreateOperationResponseSchema:
        response = self.make_transfer_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)

    def make_purchase_operation(self, request: MakePurchaseOperationRequestSchema) -> CreateOperationResponseSchema:
        response = self.make_purchase_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)

    def make_bill_payment_operation(
        self,
        request: MakeBillPaymentOperationRequestSchema,
    ) -> CreateOperationResponseSchema:
        response = self.make_bill_payment_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)

    def make_cash_withdrawal_operation(
        self,
        request: MakeCashWithdrawalOperationRequestSchema,
    ) -> CreateOperationResponseSchema:
        response = self.make_cash_withdrawal_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)


def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    """Функция создает экземпляр OperationsGatewayHTTPClient с настроенным HTTPClient.

    Returns:
        OperationsGatewayHTTPClient: Готовый к использованию OperationsGatewayHTTPClient.

    """
    return OperationsGatewayHTTPClient(client=get_public_http_client())
