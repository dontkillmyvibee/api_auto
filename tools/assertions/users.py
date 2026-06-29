import allure

from clients.http.gateway.users.schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("USER_ASSERTIONS")


@allure.step("Check create user response")
def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema) -> None:
    """Проверяет, что ответ на создание/получение пользователя соответствует запросу.

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
