import allure
from pydantic import UUID4
from requests import Response

from clients.http.gateway.error_schema import HTTPInternalErrorSchema
from clients.http.gateway.users.schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from fixtures.users import UserFixture
from tools.assertions.base import assert_equal, assert_in
from tools.logger import get_logger

logger = get_logger("USER_ASSERTIONS")


@allure.step("Check create user response")
def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema) -> None:
    """Проверяет, что ответ на создание пользователя соответствует запросу.

    Args:
        request: Исходный запрос на создание пользователя.
        response: Ответ API с данными пользователя.

    Returns:
        None

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает.

    """
    logger.info("Check create user response")

    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")
    assert_equal(response.user.phone_number, request.phone_number, "phone_number")


@allure.step("Check get user response")
def assert_get_user_response(user: UserFixture, response: GetUserResponseSchema) -> None:
    """Проверяет, что ответ на получение пользователя соответствует запросу.

    Args:
        user: Фикстурный пользователь.
        response: Ответ API с данными пользователя.

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает.

    """
    logger.info("Check get user response")

    assert_equal(response.user.id, user.user_id, "user_id")
    assert_equal(response.user.email, user.response_email, "email")
    assert_equal(response.user.last_name, user.response_last_name, "last_name")
    assert_equal(response.user.first_name, user.response_first_name, "first_name")
    assert_equal(response.user.middle_name, user.response_middle_name, "middle_name")
    assert_equal(response.user.phone_number, user.response_phone_number, "phone_number")


@allure.step("Check user not found response")
def assert_user_not_found(actual: Response, user_id: UUID4 | str) -> None:
    """Проверяет, что ответ API содержит ошибку 'User with id ... not found'.

    Args:
        actual: Фактический ответ API.
        user_id: ID пользователя для динамической генерации ошибки.

    Raises:
        AssertionError: Если текст ошибки не соответствует ожидаемому.

    """
    logger.info("Check user not found response")

    expected = f"User with id {user_id} not found"
    prep_actual = HTTPInternalErrorSchema.model_validate_json(actual.text)

    assert_in(expected, prep_actual.detail, "detail")
