"""Type definitions for Vorpal SDK."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SystemType(str, Enum):
    """Types of AI systems."""

    MODEL = "model"
    APPLICATION = "application"
    AGENT = "agent"
    PIPELINE = "pipeline"


class SystemStatus(str, Enum):
    """Lifecycle status of an AI system."""

    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    DEPLOYED = "deployed"
    DEPRECATED = "deprecated"


class RiskTier(str, Enum):
    """EU AI Act risk classification tiers."""

    PROHIBITED = "prohibited"
    HIGH = "high"
    LIMITED = "limited"
    MINIMAL = "minimal"


class ControlCategory(str, Enum):
    """Categories of governance controls."""

    ACCURACY = "accuracy"
    BIAS = "bias"
    SECURITY = "security"
    PRIVACY = "privacy"
    SAFETY = "safety"
    TRANSPARENCY = "transparency"
    ROBUSTNESS = "robustness"
    ACCOUNTABILITY = "accountability"


class ControlStatus(str, Enum):
    """Implementation status of a control."""

    PENDING = "pending"
    IMPLEMENTED = "implemented"
    TESTED = "tested"
    VERIFIED = "verified"
    FAILED = "failed"
    NOT_APPLICABLE = "not_applicable"


class PolicySeverity(str, Enum):
    """Severity level for policy rules."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class BaseType(BaseModel):
    """Base type with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="ignore",
    )


class AISystem(BaseType):
    """AI System representation."""

    id: str
    name: str
    description: str | None = None
    type: SystemType
    status: SystemStatus
    risk_tier: RiskTier
    autonomy_level: int | None = None
    owner_id: str
    team_id: str | None = None
    version: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    documentation: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class Control(BaseType):
    """Governance control representation."""

    id: str
    name: str
    description: str | None = None
    category: ControlCategory
    regulation: str | None = None
    requirement_text: str | None = None
    test_guidance: str | None = None
    mandatory: bool = True
    applies_to_risk_tiers: str | None = None
    created_at: datetime


class SystemControl(BaseType):
    """System-control assignment."""

    system_id: str
    control_id: str
    status: ControlStatus
    evidence_required: bool
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class PolicyRule(BaseType):
    """Policy rule definition."""

    name: str
    condition: str
    message: str
    severity: PolicySeverity = PolicySeverity.ERROR


class Policy(BaseType):
    """Governance policy representation."""

    id: str
    name: str
    description: str | None = None
    version: str
    enabled: bool
    match_criteria: dict[str, Any]
    rules: list[PolicyRule]
    default_severity: PolicySeverity
    regulation: str | None = None
    pack_name: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class RuleResult(BaseType):
    """Result of evaluating a single rule."""

    rule_name: str
    passed: bool
    message: str | None = None
    severity: PolicySeverity


class PolicyResult(BaseType):
    """Result of evaluating a single policy."""

    policy_id: str
    policy_name: str
    passed: bool
    rule_results: list[RuleResult]


class PolicyEvaluationResult(BaseType):
    """Result of policy evaluation."""

    allowed: bool
    system_id: str
    action: str
    policies_evaluated: int
    policies_passed: int
    policies_failed: int
    results: list[PolicyResult]
    blocking_failures: list[str]
    warnings: list[str]


class PaginationMeta(BaseType):
    """Pagination metadata."""

    page: int
    page_size: int
    total: int
    total_pages: int


class PaginatedResponse(BaseType):
    """Generic paginated response."""

    meta: PaginationMeta
