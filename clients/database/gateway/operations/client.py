import allure

from clients.database.builder import build_database_client
from clients.database.client import DatabaseClient
from clients.database.gateway.operations.schema import OperationsTableSchema
from tools.database.db_names import DatabaseName


class OperationsGatewayDatabaseClient:
    """Клиент для верификации данных в БД сервиса operations (operations_service_db.operations)."""

    def __init__(self, client: DatabaseClient):
        self._client = client

    @allure.step('Get operation from DB by id "{operation_id}"')
    def get_operation(self, operation_id: str) -> OperationsTableSchema | None:
        """Возвращает строку операции из БД по идентификатору.

        Args:
            operation_id (str): Идентификатор операции.

        Returns:
            OperationsTableSchema | None: Провалидированная строка или None, если операции нет.
        """
        row = self._client.fetch_one(
            "SELECT * FROM operations WHERE id = :operation_id",
            {"operation_id": operation_id},
        )
        return OperationsTableSchema.model_validate(dict(row)) if row else None

    @allure.step('Get operations from DB by account id "{account_id}"')
    def get_operations_by_account_id(self, account_id: str) -> list[OperationsTableSchema]:
        """Возвращает список операций счёта из БД.

        Args:
            account_id (str): Идентификатор счёта.

        Returns:
            list[OperationsTableSchema]: Список строк операций (возможно пустой).
        """
        rows = self._client.fetch_all(
            "SELECT * FROM operations WHERE account_id = :account_id",
            {"account_id": account_id},
        )
        return [OperationsTableSchema.model_validate(dict(row)) for row in rows]


def build_operations_gateway_database_client() -> OperationsGatewayDatabaseClient:
    """Создаёт экземпляр OperationsGatewayDatabaseClient с подключением к operations_service_db.

    Returns:
        OperationsGatewayDatabaseClient: Готовый к использованию клиент.
    """
    return OperationsGatewayDatabaseClient(client=build_database_client(DatabaseName.OPERATIONS))
