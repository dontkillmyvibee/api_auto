import allure

from clients.database.builder import build_database_client
from clients.database.client import DatabaseClient
from clients.database.gateway.cards.schema import CardsTableSchema
from tools.database.db_names import DatabaseName


class CardsGatewayDatabaseClient:
    """Клиент для верификации данных в БД сервиса cards (cards_service_db.cards)."""

    def __init__(self, client: DatabaseClient):
        self._client = client

    @allure.step('Get card from DB by id "{card_id}"')
    def get_card(self, card_id: str) -> CardsTableSchema | None:
        """Возвращает строку карты из БД по идентификатору.

        Args:
            card_id (str): Идентификатор карты.

        Returns:
            CardsTableSchema | None: Провалидированная строка или None, если карты нет.
        """
        row = self._client.fetch_one(
            "SELECT * FROM cards WHERE id = :card_id",
            {"card_id": card_id},
        )
        return CardsTableSchema.model_validate(dict(row)) if row else None

    @allure.step('Get cards from DB by account id "{account_id}"')
    def get_cards_by_account_id(self, account_id: str) -> list[CardsTableSchema]:
        """Возвращает список карт счёта из БД.

        Args:
            account_id (str): Идентификатор счёта.

        Returns:
            list[CardsTableSchema]: Список строк карт (возможно пустой).
        """
        rows = self._client.fetch_all(
            "SELECT * FROM cards WHERE account_id = :account_id",
            {"account_id": account_id},
        )
        return [CardsTableSchema.model_validate(dict(row)) for row in rows]


def build_cards_gateway_database_client() -> CardsGatewayDatabaseClient:
    """Создаёт экземпляр CardsGatewayDatabaseClient с подключением к cards_service_db.

    Returns:
        CardsGatewayDatabaseClient: Готовый к использованию клиент.
    """
    return CardsGatewayDatabaseClient(client=build_database_client(DatabaseName.CARDS))
