import contextlib

from requests import PreparedRequest

ignore_headers = [
    "user-agent",
    "accept-encoding",
    "connection",
    "content-length",
]


def _single_quote(value: str) -> str:
    """Безопасно оборачивает значение в одинарные кавычки.

    Args:
        value (str): Произвольное значение для подстановки в команду.

    Returns:
        str: Значение, безопасно обёрнутое в одинарные кавычки.
    """
    escaped = value.replace("'", "'\\''")
    return f"'{escaped}'"


def make_curl_from_prepared(prepared: PreparedRequest) -> str:
    result: list[str] = [
        f"curl -X {_single_quote(prepared.method or '')}",
        _single_quote(prepared.url or ""),
    ]

    for header, value in prepared.headers.items():
        if header.lower() not in ignore_headers:
            result.append(f"-H {_single_quote(f'{header}: {value}')}")

    if body := prepared.body:
        with contextlib.suppress(UnicodeDecodeError):
            decoded = body.decode("utf-8") if isinstance(body, bytes) else body
            result.append(f"-d {_single_quote(decoded)}")

    return " \\\n     ".join(result)
