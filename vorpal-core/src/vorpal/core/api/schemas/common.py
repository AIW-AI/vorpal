"""Common schema definitions."""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    page: int
    page_size: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""

    data: list[T]
    meta: PaginationMeta


class ErrorDetail(BaseModel):
    """Error detail information."""

    field: str | None = None
    message: str


class ErrorResponse(BaseModel):
    """Standard error response."""

    code: str
    message: str
    details: list[ErrorDetail] | None = None
    request_id: str | None = None


class SuccessResponse(BaseModel):
    """Generic success response."""

    success: bool = True
    message: str | None = None
    data: dict[str, Any] | None = None
