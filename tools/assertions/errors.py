import allure

from clients.http.gateway.error_schema import HTTPInternalErrorSchema, ValidationErrorSchema
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("ERRORS_ASSERTIONS")


@allure.step("Check validation error")
def assert_validation_error(actual: ValidationErrorSchema, expected: ValidationErrorSchema) -> None:
    """Проверяет, что объект ошибки валидации соответствует ожидаемому значению.

    Args:
        actual: Фактическая ошибка.
        expected: Ожидаемая ошибка.

    Raises:
        AssertionError: Если значения полей не совпадают.

    """
    logger.info("Check validation error")
    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.msg, expected.msg, "msg")
    assert_equal(actual.loc, expected.loc, "loc")


# @allure.step("Check validation error response")
# def assert_validation_error_response(actual: HTTPValidationErrorSchema, expected: HTTPValidationErrorSchema):
#     """Проверяет, что объект ответа API с ошибками валидации соответствует ожидаемому значению.
#
#     Args:
#         actual: Фактический ответ API.
#         expected: Ожидаемый ответ API.
#
#     Raises:
#         AssertionError: Если значения полей не совпадают.
#
#     """
#     logger.info("Check validation error response")
#     assert_length_with_two_sized(actual.detail, expected.detail, "detail")
#
#     for index, detail in enumerate(actual.detail):
#         assert_validation_error(actual.detail[index], detail)


@allure.step("Check internal error response")
def assert_internal_error_response(actual: HTTPInternalErrorSchema, expected: HTTPInternalErrorSchema) -> None:
    """Функция для проверки внутренней ошибки. Например, ошибки 404.

    Args:
        actual: Фактический ответ API.
        expected: Ожидаемый ответ API.

    Raises:
        AssertionError: Если значения полей не совпадают.

    """
    logger.info("Check internal error response")
    assert_equal(actual.detail, expected.detail, "detail")
