import allure

from clients.database.builder import build_database_client
from clients.database.client import DatabaseClient
from clients.database.gateway.users.schema import UsersTableSchema
from tools.database.db_names import DatabaseName


class UsersGatewayDatabaseClient:
    """Клиент для верификации данных в БД сервиса users (users_service_db.users)."""

    def __init__(self, client: DatabaseClient):
        self._client = client

    @allure.step('Get user from DB by id "{user_id}"')
    def get_user(self, user_id: str) -> UsersTableSchema | None:
        """Возвращает строку пользователя из БД по идентификатору.

        Args:
            user_id (str): Идентификатор пользователя.

        Returns:
            UsersTableSchema | None: Провалидированная строка или None, если пользователя нет.
        """
        row = self._client.fetch_one(
            "SELECT * FROM users WHERE id = :user_id",
            {"user_id": user_id},
        )
        return UsersTableSchema.model_validate(dict(row)) if row else None


def build_users_gateway_database_client() -> UsersGatewayDatabaseClient:
    """Создаёт экземпляр UsersGatewayDatabaseClient с подключением к users_service_db.

    Returns:
        UsersGatewayDatabaseClient: Готовый к использованию клиент.
    """
    return UsersGatewayDatabaseClient(client=build_database_client(DatabaseName.USERS))
