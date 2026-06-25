import contextlib
import json
from http import HTTPMethod
from typing import Any

import allure
from requests import Request, Response, Session

from tools.http.curl import make_curl_from_prepared
from tools.logger import get_logger

logger = get_logger("HTTP_CLIENT")


class HTTPClient:
    """Базовый HTTP-клиент для работы с API(надстройка над requests).

    Использует объект Session для выполнения HTTP-запросов с заданным таймаутом и базовым URL.
    """

    def __init__(self, client: Session, base_url: str, timeout: float):
        self.__client = client
        self.__base_url = base_url
        self.__timeout = timeout

    def __request(self, method: str, url: str, **kwargs: Any) -> Response:
        """Внутренний метод для отправки HTTP-запроса.

        Формирует полный URL, объединяя базовый URL и путь, и отправляет запрос
        с использованием объекта requests.Session.

        Args:
            method (str): HTTP-метод (например, «GET», «POST»).
            url (str): Путь к ресурсу (например, «users/1»).
            **kwargs: Дополнительные аргументы для метода request (params, json, data и т. д.).

        Returns:
            Response: Объект Response с результатом запроса.
        """
        full_url = f"{self.__base_url}{url}"

        request = Request(method=method, url=full_url, **kwargs)
        prepared_request = self.__client.prepare_request(request)
        logger.info(f"Make '{prepared_request.method}' request to {prepared_request.url}")

        curl = make_curl_from_prepared(prepared_request)
        allure.attach(curl, "cURL", allure.attachment_type.TEXT)

        response = self.__client.send(prepared_request, timeout=self.__timeout)
        logger.info(f"Got response {response.status_code} {response.reason} from {response.url}")

        self.__attach_response(response)

        return response

    @staticmethod
    def __attach_response(response: Response) -> None:
        """Прикрепляет в Allure тело ответа со статусом в шапке.

        JSON форматируется с отступами для читаемости, остальное аттачится как есть.

        Args:
            response (Response): Ответ, который нужно приложить к отчёту.
        """
        body = response.text
        with contextlib.suppress(ValueError):
            body = json.dumps(response.json(), ensure_ascii=False, indent=2)

        content = f"Status: {response.status_code} {response.reason}\n\n{body}"
        allure.attach(content, "Response body", allure.attachment_type.TEXT)

    def get(self, url: str, params: Any | None = None) -> Response:
        """Метод для отправки GET-запроса к ресурсу.

        Args:
            url (str): Путь к ресурсу.
            params (Any | None): Параметры запроса, которые будут добавлены в URL как query-параметры.

        Returns:
            Response: Объект Response с результатом GET-запроса.
        """
        return self.__request(method=HTTPMethod.GET, url=url, params=params)

    def post(
        self,
        url: str,
        json: Any | None = None,
        data: Any | None = None,
        files: dict[str, Any] | None = None,
    ) -> Response:
        """Метод для отправки POST-запроса к ресурсу.

        Args:
            url (str): Путь к ресурсу.
            json (Any | None): Данные в формате JSON для тела запроса.
            data (Any | None): Данные для тела запроса в необработанном виде.
            files (dict[str, Any] | None): Словарь полей для multipart-загрузки файлов
                (значения — файловые объекты, байты или кортежи вида (имя, содержимое, тип)).

        Returns:
            Response: Объект Response с результатом POST-запроса.
        """
        return self.__request(method=HTTPMethod.POST, url=url, json=json, data=data, files=files)

    def patch(self, url: str, json: Any | None = None) -> Response:
        """Метод для отправки PATCH-запроса для частичного обновления ресурса.

        Args:
            url (str): Путь к ресурсу.
            json (Any | None): Данные в формате JSON для частичного обновления.

        Returns:
            Response: Объект Response с результатом PATCH-запроса.
        """
        return self.__request(method=HTTPMethod.PATCH, url=url, json=json)

    def delete(self, url: str) -> Response:
        """Метод для отправки DELETE-запрос для удаления ресурса.

        Args:
            url (str): Путь к ресурсу.

        Returns:
            Response: Объект Response с результатом DELETE-запроса.
        """

        return self.__request(method=HTTPMethod.DELETE, url=url)
