"""Schema definitions for Audit Events."""

from datetime import datetime
from typing import Any

from pydantic import Field

from vorpal.core.api.schemas.common import BaseSchema, PaginatedResponse
from vorpal.core.models.audit import ActorType


class AuditEventResponse(BaseSchema):
    """Schema for Audit Event response."""

    id: str
    system_id: str | None
    event_type: str
    actor_id: str | None
    actor_type: ActorType
    actor_name: str | None
    action: str
    resource_type: str | None
    resource_id: str | None
    details: dict[str, Any]
    ip_address: str | None
    request_id: str | None
    previous_hash: str | None
    event_hash: str
    timestamp: datetime


class AuditListResponse(PaginatedResponse[AuditEventResponse]):
    """Paginated list of Audit Events."""

    pass


class AuditQueryParams(BaseSchema):
    """Query parameters for audit log search."""

    system_id: str | None = None
    event_type: str | None = None
    actor_id: str | None = None
    action: str | None = None
    resource_type: str | None = None
    from_date: datetime | None = Field(default=None, alias="from")
    to_date: datetime | None = Field(default=None, alias="to")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=100)


class AuditChainVerification(BaseSchema):
    """Result of audit chain integrity verification."""

    verified: bool
    total_events: int
    valid_events: int
    invalid_events: int
    first_invalid_event_id: str | None = None
    message: str
