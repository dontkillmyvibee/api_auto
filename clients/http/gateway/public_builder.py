from clients.http.builder import build_http_client
from clients.http.client import HTTPClient
from config import get_settings


def get_public_http_client() -> HTTPClient:
    """Создает экземпляр HTTPClient с использованием base_url и timeout из  .env файла.

    Returns:
        HTTPClient: Настроенный экземпляр HTTPClient, готовый к использованию в HTTP клиентах требующих
        неавторизованного пользователя.

    """
    settings = get_settings()
    return build_http_client(
        base_url=settings.api.base_url_str,
        timeout=settings.api.timeout,
    )
