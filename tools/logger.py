import logging
import sys

from config import LoggingSettings

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_ROOT_NAME = "autotests"


def _configure_root() -> None:
    """Однократно настраивает корневой логгер приложения.

    Хендлер вешается на именованный логгер «autotests», а не на root,
    чтобы не конфликтовать с логированием pytest и сторонних библиотек.
    Уровень логирования берётся из LoggingSettings (переменная окружения LOG_LEVEL или ключ из .env).

    Returns:
        None: Функция ничего не возвращает, выполняет настройку как побочный эффект.
    """
    root = logging.getLogger(_ROOT_NAME)
    if root.handlers:
        return

    root.setLevel(LoggingSettings().log_level)
    root.propagate = False

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT))
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Возвращает настроенный логгер для указанного компонента.

    Все логгеры являются дочерними от «autotests» и наследуют единый
    обработчик и формат.

    Args:
        name (str): Имя компонента (например, «HTTP_CLIENT»).

    Returns:
        logging.Logger: Готовый к использованию логгер.
    """
    _configure_root()
    return logging.getLogger(_ROOT_NAME).getChild(name)
