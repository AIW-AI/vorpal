"""Schema definitions for AI Systems."""

from datetime import datetime
from typing import Any

from pydantic import Field, field_validator

from vorpal.core.api.schemas.common import BaseSchema, PaginatedResponse
from vorpal.core.models.system import RiskTier, SystemStatus, SystemType


class SystemBase(BaseSchema):
    """Base schema for AI System."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    type: SystemType
    risk_tier: RiskTier
    autonomy_level: int | None = Field(default=None, ge=1, le=5)
    version: str | None = None
    metadata_: dict[str, Any] = Field(default_factory=dict, alias="metadata")
    documentation: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)

    @field_validator("autonomy_level")
    @classmethod
    def validate_autonomy_for_agents(cls, v: int | None, info) -> int | None:
        """Autonomy level should typically be set for agents."""
        return v


class SystemCreate(SystemBase):
    """Schema for creating a new AI System."""

    owner_id: str | None = None  # Set from auth context if not provided
    team_id: str | None = None


class SystemUpdate(BaseSchema):
    """Schema for updating an AI System."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    type: SystemType | None = None
    status: SystemStatus | None = None
    risk_tier: RiskTier | None = None
    autonomy_level: int | None = Field(default=None, ge=1, le=5)
    version: str | None = None
    metadata_: dict[str, Any] | None = Field(default=None, alias="metadata")
    documentation: dict[str, Any] | None = None
    tags: list[str] | None = None
    team_id: str | None = None


class SystemResponse(SystemBase):
    """Schema for AI System response."""

    id: str
    status: SystemStatus
    owner_id: str
    team_id: str | None = None
    created_at: datetime
    updated_at: datetime


class SystemListResponse(PaginatedResponse[SystemResponse]):
    """Paginated list of AI Systems."""

    pass


class SystemControlAssignment(BaseSchema):
    """Schema for assigning a control to a system."""

    control_id: str
    notes: str | None = None
    evidence_required: bool = True
