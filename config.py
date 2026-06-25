from enum import StrEnum
from functools import lru_cache

from pydantic import BaseModel, Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(StrEnum):
    """Допустимые уровни логирования."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingSettings(BaseSettings):
    """Настройки логирования, изолированные от основной конфигурации.

    Attributes:
        log_level (LogLevel): Минимальный уровень сообщений для вывода.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    log_level: LogLevel = LogLevel.INFO


class DatabaseSettings(BaseSettings):
    """Настройки подключения к PostgreSQL, общие для всех сервисных БД.

    Изолированы от корневой конфигурации (как LoggingSettings), чтобы HTTP-тесты
    не требовали наличия DB-кредов и наоборот. Имя конкретной БД (users_service_db
    и т. д.) передаётся в момент сборки клиента, а не хранится здесь.

    Attributes:
        host (str): Хост сервера PostgreSQL.
        port (int): Порт сервера PostgreSQL.
        user (str): Пользователь БД.
        password (str): Пароль пользователя БД.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DATABASE.",
        extra="ignore",
    )

    host: str = "localhost"
    port: int = Field(default=5432, gt=0)
    user: str
    password: str

    def dsn(self, db_name: str) -> str:
        """Формирует SQLAlchemy DSN для конкретной БД сервиса.

        Args:
            db_name (str): Имя базы данных (например, «users_service_db»).

        Returns:
            str: Строка подключения вида «postgresql+psycopg://user:pass@host:port/db».
        """
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{db_name}"


class KafkaSettings(BaseSettings):
    """Настройки подключения к Kafka, изолированные от корневой конфигурации.

    Attributes:
        bootstrap_servers (str): Адрес(а) брокеров Kafka.
        group_id (str): Базовый идентификатор группы консьюмеров (в билдере к нему
            добавляется уникальный суффикс, чтобы каждый консьюмер читал независимо).
        auto_offset_reset (str): Стартовая позиция чтения для новой группы (earliest/latest).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="KAFKA.",
        extra="ignore",
    )

    bootstrap_servers: str = "localhost:9093"
    group_id: str = "api-auto-tests"
    auto_offset_reset: str = "earliest"


class HTTPClientSettings(BaseModel):
    """Настройки конкретного HTTP-клиента (одного API-сервиса).

    Attributes:
        base_url (HttpUrl): Базовый URL сервиса, валидируется как корректный http(s)-адрес.
        timeout (float): Таймаут запроса в секундах.
    """

    base_url: HttpUrl
    timeout: float = Field(default=30.0, gt=0)

    @property
    def base_url_str(self) -> str:
        """Возвращает базовый URL в виде строки без завершающего слеша.

        Returns:
            str: Нормализованный базовый URL.
        """
        return str(self.base_url).rstrip("/")


class Settings(BaseSettings):
    """Корневая конфигурация фреймворка.

    Значения читаются из переменных окружения и файла .env. Для вложенных
    моделей используется разделитель «.», например: API.BASE_URL, API.TIMEOUT.

    Attributes:
        api (HTTPClientSettings): Настройки основного API-сервиса.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
        extra="ignore",
    )

    api: HTTPClientSettings


@lru_cache
def get_settings() -> Settings:
    """Возвращает единственный закешированный экземпляр конфигурации.

    Кеширование через lru_cache, окружение читается один раз.

    Returns:
        Settings: Загруженная и провалидированная конфигурация.
    """
    return Settings()
