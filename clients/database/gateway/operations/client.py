from typing import Any

import allure

from clients.database.builder import build_database_client
from clients.database.client import DatabaseClient
from clients.database.gateway.operations.schema import (
    CreateOperationsTableSchema,
    OperationsTableSchema,
)
from tools.database.db_names import DatabaseName

_INSERT_OPERATION_SQL = """
INSERT INTO operations (id, type, status, amount, card_id, category, created_at, account_id)
VALUES (:id, :type, :status, :amount, :card_id, :category, :created_at, :account_id)
RETURNING *
"""


class OperationsGatewayDatabaseClient:
    """Клиент БД сервиса operations: verification (get_*) и seed (insert_*)."""

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

    @allure.step("Insert operation into DB")
    def insert_operation(self, operation: CreateOperationsTableSchema | None = None) -> OperationsTableSchema:
        """Вставляет операцию в БД и возвращает сохранённую строку.

        Args:
            operation (CreateOperationsTableSchema | None): Данные для seed.
                Если None — создаётся строка с defaults builder'а.

        Returns:
            OperationsTableSchema: Строка после INSERT ... RETURNING *.
        """
        payload = operation or CreateOperationsTableSchema()
        row = self._client.execute_returning_one(_INSERT_OPERATION_SQL, payload.model_dump())
        if row is None:
            raise RuntimeError("INSERT INTO operations did not return a row")
        return OperationsTableSchema.model_validate(dict(row))

    @allure.step("Insert in-progress purchase operation into DB")
    def insert_in_progress_purchase_operation(self, **overrides: Any) -> OperationsTableSchema:
        """Seed PURCHASE / IN_PROGRESS. Overrides — поля CreateOperationsTableSchema."""
        return self.insert_operation(CreateOperationsTableSchema(type="PURCHASE", status="IN_PROGRESS", **overrides))

    @allure.step("Insert completed purchase operation into DB")
    def insert_completed_purchase_operation(self, **overrides: Any) -> OperationsTableSchema:
        """Seed PURCHASE / COMPLETED. Overrides — поля CreateOperationsTableSchema."""
        return self.insert_operation(CreateOperationsTableSchema(type="PURCHASE", status="COMPLETED", **overrides))


def build_operations_gateway_database_client() -> OperationsGatewayDatabaseClient:
    """Создаёт экземпляр OperationsGatewayDatabaseClient с подключением к operations_service_db.

    Returns:
        OperationsGatewayDatabaseClient: Готовый к использованию клиент.
    """
    return OperationsGatewayDatabaseClient(client=build_database_client(DatabaseName.OPERATIONS))
