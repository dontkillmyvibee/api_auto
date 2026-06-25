import allure

from clients.database.builder import build_database_client
from clients.database.client import DatabaseClient
from clients.database.gateway.accounts.schema import AccountsTableSchema
from tools.database.db_names import DatabaseName


class AccountsGatewayDatabaseClient:
    """Клиент для верификации данных в БД сервиса accounts (accounts_service_db.accounts)."""

    def __init__(self, client: DatabaseClient):
        self._client = client

    @allure.step('Get account from DB by id "{account_id}"')
    def get_account(self, account_id: str) -> AccountsTableSchema | None:
        """Возвращает строку счёта из БД по идентификатору.

        Args:
            account_id (str): Идентификатор счёта.

        Returns:
            AccountsTableSchema | None: Провалидированная строка или None, если счёта нет.
        """
        row = self._client.fetch_one(
            "SELECT * FROM accounts WHERE id = :account_id",
            {"account_id": account_id},
        )
        return AccountsTableSchema.model_validate(dict(row)) if row else None

    @allure.step('Get accounts from DB by user id "{user_id}"')
    def get_accounts_by_user_id(self, user_id: str) -> list[AccountsTableSchema]:
        """Возвращает список счетов пользователя из БД.

        Args:
            user_id (str): Идентификатор пользователя.

        Returns:
            list[AccountsTableSchema]: Список строк счетов (возможно пустой).
        """
        rows = self._client.fetch_all(
            "SELECT * FROM accounts WHERE user_id = :user_id",
            {"user_id": user_id},
        )
        return [AccountsTableSchema.model_validate(dict(row)) for row in rows]


def build_accounts_gateway_database_client() -> AccountsGatewayDatabaseClient:
    """Создаёт экземпляр AccountsGatewayDatabaseClient с подключением к accounts_service_db.

    Returns:
        AccountsGatewayDatabaseClient: Готовый к использованию клиент.
    """
    return AccountsGatewayDatabaseClient(client=build_database_client(DatabaseName.ACCOUNTS))
