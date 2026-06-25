from enum import StrEnum


class DatabaseName(StrEnum):
    """Имена баз данных микросервисов (одна БД на сервис)."""

    USERS = "users_service_db"
    ACCOUNTS = "accounts_service_db"
    CARDS = "cards_service_db"
    OPERATIONS = "operations_service_db"
