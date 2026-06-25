from requests import Session

from clients.http.client import HTTPClient


def build_http_client(base_url: str, timeout: float, headers: dict[str, str] | None = None) -> HTTPClient:
    """Создаёт экземпляр HTTPClient.

    Формирует экземпляр HTTPClient с заданными базовым URL, таймаутом и заголовками.
    Использует Session из библиотеки requests для выполнения HTTP-запросов.

    Args:
        base_url (str): Базовый URL для API-запросов (например, «https://api.example.com»).
            Должен включать схему (http:// или https://).
        timeout (int): Таймаут для запросов в секундах. Должен быть положительным целым числом.
        headers (dict | None): Словарь HTTP-заголовков, которые будут установлены в объекте Session.
            Если None — кастомные заголовки не добавляются. Существующие заголовки обновляются, а не заменяются.

    Returns:
        HTTPClient: Настроенный экземпляр HTTPClient, готовый к использованию в public/private builders.

    """
    session = Session()

    if headers:
        session.headers.update(headers)

    return HTTPClient(client=session, base_url=base_url, timeout=timeout)
