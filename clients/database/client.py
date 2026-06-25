from collections.abc import Mapping, Sequence
from typing import Any

import allure
from sqlalchemy import Engine, RowMapping, text

from tools.logger import get_logger

logger = get_logger("DATABASE_CLIENT")


class DatabaseClient:
    """Низкоуровневый клиент для выполнения SQL-запросов (надстройка над SQLAlchemy Engine).

    Открывает соединение из пула на каждый запрос и возвращает строки в виде
    маппингов (имя_колонки -> значение). Маппинг строк в Pydantic-схемы — задача
    доменных gateway-клиентов.
    """

    def __init__(self, engine: Engine):
        self._engine = engine

    @staticmethod
    def _attach(query: str, params: Mapping[str, Any] | None) -> None:
        """Прикрепляет к Allure текст запроса и параметры."""
        content = query if not params else f"{query}\n\n-- params: {dict(params)}"
        allure.attach(content, "SQL", allure.attachment_type.TEXT)

    def fetch_one(self, query: str, params: Mapping[str, Any] | None = None) -> RowMapping | None:
        """Выполняет запрос и возвращает первую строку или None.

        Args:
            query (str): SQL-запрос с именованными плейсхолдерами (:name).
            params (Mapping[str, Any] | None): Значения для плейсхолдеров.

        Returns:
            RowMapping | None: Первая строка как маппинг колонок или None, если строк нет.
        """
        logger.info(f"Execute fetch_one: {query} | params: {params}")
        self._attach(query, params)

        with self._engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            return result.mappings().first()

    def fetch_all(self, query: str, params: Mapping[str, Any] | None = None) -> Sequence[RowMapping]:
        """Выполняет запрос и возвращает все строки.

        Args:
            query (str): SQL-запрос с именованными плейсхолдерами (:name).
            params (Mapping[str, Any] | None): Значения для плейсхолдеров.

        Returns:
            Sequence[RowMapping]: Список строк как маппингов колонок (возможно пустой).
        """
        logger.info(f"Execute fetch_all: {query} | params: {params}")
        self._attach(query, params)

        with self._engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            return result.mappings().all()
