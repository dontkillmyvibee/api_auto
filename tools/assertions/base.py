from collections.abc import Sized
from typing import Any

import allure

from tools.logger import get_logger

logger = get_logger("BASE_ASSERTIONS")


@allure.step("Check that {name} equals to {expected}")
def assert_equal(actual: Any, expected: Any, name: str) -> None:
    """Проверяет, что актуальное значение == ожидаемому значению.

    Args:
        actual(Any): Актуальное значение.
        expected(Any): Ожидаемое значение.
        name: Название проверяемого значения.

    Returns:
        None

    Raises:
        AssertionError: Если фактическое значение не равно ожидаемому.

    """
    logger.info(f'Check that "{name}" equals to {expected}')

    assert actual == expected, f'Incorrect value: "{name}". Expected value: {expected}. Actual value: {actual}'


@allure.step("Check that {name} is true")
def assert_is_true(actual: Any, name: str) -> None:
    """Проверяет, что фактическое значение является истинным.

    Args:
        actual: Фактическое значение.
        name: Название проверяемого значения.

    Returns:
        None

    Raises:
        AssertionError: Если фактическое значение ложно.

    """
    logger.info(f'Check that "{name}" is true')

    assert actual, f'Incorrect value: "{name}". Expected true value but got: {actual}'


def assert_length_with_two_sized(actual: Sized, expected: Sized, name: str) -> None:
    """Проверяет, что длины двух объектов совпадают.

    Args:
        actual: Фактический объект.
        expected: Ожидаемый объект.
        name: Название проверяемого объекта.

    Returns:
        None

    Raises:
        AssertionError: Если длины не совпадают.

    """
    with allure.step(f"Check that length of {name} equals to {len(expected)}"):
        logger.info(f'Check that length of "{name}" equals to {len(expected)}')

        assert len(actual) == len(expected), (
            f'Incorrect object length: "{name}". Expected length: {len(expected)}. Actual length: {len(actual)}'
        )


def assert_length(actual: Sized, expected: int, name: str) -> None:
    assert len(actual) == expected, (
        f'Incorrect object length: "{name}". Expected length: {expected}. Actual length: {len(actual)}'
    )
