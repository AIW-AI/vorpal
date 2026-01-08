"""Schema definitions for Controls."""

from datetime import datetime

from pydantic import Field

from vorpal.core.api.schemas.common import BaseSchema, PaginatedResponse
from vorpal.core.models.control import ControlCategory, ControlStatus


class ControlBase(BaseSchema):
    """Base schema for Control."""

    id: str = Field(..., pattern=r"^CTRL-[A-Z]+-\d{3}$")
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    category: ControlCategory
    regulation: str | None = None
    requirement_text: str | None = None
    test_guidance: str | None = None
    mandatory: bool = True
    applies_to_risk_tiers: str | None = None


class ControlCreate(ControlBase):
    """Schema for creating a new Control."""

    pass


class ControlUpdate(BaseSchema):
    """Schema for updating a Control."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    requirement_text: str | None = None
    test_guidance: str | None = None
    mandatory: bool | None = None
    applies_to_risk_tiers: str | None = None


class ControlResponse(ControlBase):
    """Schema for Control response."""

    created_at: datetime


class ControlListResponse(PaginatedResponse[ControlResponse]):
    """Paginated list of Controls."""

    pass


class SystemControlCreate(BaseSchema):
    """Schema for assigning a control to a system."""

    control_id: str
    evidence_required: bool = True
    notes: str | None = None


class SystemControlUpdate(BaseSchema):
    """Schema for updating a system-control assignment."""

    status: ControlStatus | None = None
    evidence_required: bool | None = None
    notes: str | None = None


class SystemControlResponse(BaseSchema):
    """Schema for system-control assignment response."""

    system_id: str
    control_id: str
    status: ControlStatus
    evidence_required: bool
    notes: str | None
    last_updated_by: str | None
    created_at: datetime
    updated_at: datetime

    # Include control details
    control: ControlResponse | None = None
