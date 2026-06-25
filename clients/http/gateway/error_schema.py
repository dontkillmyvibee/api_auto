from tools.schema.schema_helpers import CamelCaseModel


class ValidationErrorSchema(CamelCaseModel):
    """Единичная ошибка валидации FastAPI (элемент detail в ответе 422)."""

    loc: list[str | int]
    msg: str
    type: str


class HTTPValidationErrorSchema(CamelCaseModel):
    """Тело ответа 422 Unprocessable Entity."""

    detail: list[ValidationErrorSchema] | None = None
