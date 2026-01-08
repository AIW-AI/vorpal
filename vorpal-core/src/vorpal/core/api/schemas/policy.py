"""Schema definitions for Policies."""

from datetime import datetime
from typing import Any

from pydantic import Field

from vorpal.core.api.schemas.common import BaseSchema, PaginatedResponse
from vorpal.core.models.policy import PolicySeverity


class PolicyRuleSchema(BaseSchema):
    """Schema for a policy rule."""

    name: str
    condition: str  # CEL expression
    message: str
    severity: PolicySeverity = PolicySeverity.ERROR


class PolicyBase(BaseSchema):
    """Base schema for Policy."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    version: str = "1.0.0"
    enabled: bool = True
    match_criteria: dict[str, Any] = Field(default_factory=dict)
    rules: list[PolicyRuleSchema] = Field(default_factory=list)
    default_severity: PolicySeverity = PolicySeverity.ERROR
    regulation: str | None = None
    pack_name: str | None = None
    metadata_: dict[str, Any] = Field(default_factory=dict, alias="metadata")


class PolicyCreate(PolicyBase):
    """Schema for creating a new Policy."""

    pass


class PolicyUpdate(BaseSchema):
    """Schema for updating a Policy."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    version: str | None = None
    enabled: bool | None = None
    match_criteria: dict[str, Any] | None = None
    rules: list[PolicyRuleSchema] | None = None
    default_severity: PolicySeverity | None = None
    regulation: str | None = None
    pack_name: str | None = None
    metadata_: dict[str, Any] | None = Field(default=None, alias="metadata")


class PolicyResponse(PolicyBase):
    """Schema for Policy response."""

    id: str
    created_by: str | None
    created_at: datetime
    updated_at: datetime


class PolicyListResponse(PaginatedResponse[PolicyResponse]):
    """Paginated list of Policies."""

    pass


class PolicyEvaluateRequest(BaseSchema):
    """Request schema for policy evaluation."""

    system_id: str
    action: str  # e.g., 'deploy', 'update', 'delete'
    context: dict[str, Any] = Field(default_factory=dict)


class RuleResult(BaseSchema):
    """Result of evaluating a single rule."""

    rule_name: str
    passed: bool
    message: str | None = None
    severity: PolicySeverity


class PolicyResult(BaseSchema):
    """Result of evaluating a single policy."""

    policy_id: str
    policy_name: str
    passed: bool
    rule_results: list[RuleResult]


class PolicyEvaluateResponse(BaseSchema):
    """Response schema for policy evaluation."""

    allowed: bool
    system_id: str
    action: str
    policies_evaluated: int
    policies_passed: int
    policies_failed: int
    results: list[PolicyResult]
    blocking_failures: list[str]  # Messages from rules that blocked
    warnings: list[str]  # Messages from warning-severity rules
