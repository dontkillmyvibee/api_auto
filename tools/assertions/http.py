import contextlib
import json
from http import HTTPStatus

import allure
from pydantic import BaseModel
from requests import Response

from tools.logger import get_logger

logger = get_logger("HTTP_ASSERTIONS")


def _format_status_error(response: Response, expected: set[int]) -> str:
    expected_str = ", ".join(map(str, sorted(expected)))
    body = response.text
    with contextlib.suppress(ValueError):
        body = json.dumps(response.json(), ensure_ascii=False, indent=2)

    return (
        f"Expected status code: {expected_str}\n"
        f"Actual status code: {response.status_code} {response.reason}\n"
        f"URL: {response.url}\n\n"
        f"Response body:\n{body}"
    )


def assert_status_code(response: Response, expected: int | set[int]) -> None:
    """Проверяет HTTP-статус ответа и падает с телом ответа при несовпадении.

    Args:
        response (Response): Ответ requests.
        expected (int | set[int]): Ожидаемый код или множество допустимых кодов.
    """
    expected_codes = {expected} if isinstance(expected, int) else set(expected)
    label = expected if isinstance(expected, int) else sorted(expected_codes)

    logger.info(f"Assert status code is {label}")
    with allure.step(f"Assert status code is {label}"):
        if response.status_code not in expected_codes:
            raise AssertionError(_format_status_error(response, expected_codes))


def assert_response_schema[T: BaseModel](
    response: Response,
    schema: type[T],
    *,
    status: int = HTTPStatus.OK,
) -> T:
    """Проверяет статус ответа и парсит тело в Pydantic-схему.

    Args:
        response (Response): Ответ requests.
        schema (type[T]): Ожидаемая Pydantic-модель ответа.
        status (int): Ожидаемый HTTP-статус для happy path.

    Returns:
        T: Провалидированная модель ответа.
    """
    assert_status_code(response, status)
    logger.info(f"Validate response schema: {schema.__name__}")
    with allure.step(f"Validate response schema: {schema.__name__}"):
        return schema.model_validate_json(response.text)
