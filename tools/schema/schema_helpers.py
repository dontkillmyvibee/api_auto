from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelCaseModel(BaseModel):
    """Базовая модель с автоматическими camelCase-алиасами."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        serialize_by_alias=True,
    )

    def to_dict(self) -> dict[str, Any]:
        """JSON-совместимый dict для отправки в API.

        Использует mode="json", поэтому UUID, datetime/date, HttpUrl, Decimal и
        Enum превращаются в JSON-примитивы, а ключи остаются в camelCase.
        Единая точка сериализации.
        """
        return self.model_dump(mode="json")


class DatabaseSchema(BaseModel):
    """Базовая модель для строк БД (snake_case, как имена колонок в PostgreSQL)."""

    model_config = ConfigDict(from_attributes=True)


class KafkaEventSchema(BaseModel):
    """Базовая модель для событий Kafka (snake_case JSON-payload)."""

    def to_json_bytes(self) -> bytes:
        """Сериализует событие в JSON-байты для публикации в топик."""
        return self.model_dump_json().encode("utf-8")
