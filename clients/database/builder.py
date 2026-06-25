from functools import lru_cache

from sqlalchemy import Engine, create_engine

from clients.database.client import DatabaseClient
from config import DatabaseSettings


@lru_cache
def _get_engine(db_name: str) -> Engine:
    """Создаёт (и кеширует) Engine для конкретной БД.

    Кеширование через lru_cache гарантирует один Engine на БД за прогон, поэтому
    пул соединений переиспользуется, а не создаётся заново на каждый клиент.

    Args:
        db_name (str): Имя базы данных сервиса.

    Returns:
        Engine: Готовый к работе SQLAlchemy Engine с включённым pool_pre_ping.
    """
    settings = DatabaseSettings()
    return create_engine(settings.dsn(db_name), pool_pre_ping=True)


def build_database_client(db_name: str) -> DatabaseClient:
    """Создаёт DatabaseClient для указанной БД сервиса.

    Args:
        db_name (str): Имя базы данных (значение DatabaseName).

    Returns:
        DatabaseClient: Готовый к использованию клиент в доменных gateway-клиентах.
    """
    return DatabaseClient(engine=_get_engine(db_name))
