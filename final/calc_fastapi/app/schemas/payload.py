from typing import Literal

from pydantic import BaseModel, Field


class CalculateRequest(BaseModel):
    """Схема входящего запроса на вычисление."""

    expression: str = Field(
        ...,
        description="Математическое выражение для вычисления",
        examples=["2 + 2 * 2"],
    )


class CalculateSuccessResponse(BaseModel):
    """Схема успешного ответа."""

    status: Literal["success"] = "success"
    result: int | float


class CalculateErrorResponse(BaseModel):
    """Схема ответа при ошибке вычисления."""

    status: Literal["error"] = "error"
    message: str
