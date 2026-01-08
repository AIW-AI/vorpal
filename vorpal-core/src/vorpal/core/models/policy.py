"""Policy model for governance rules."""

from datetime import datetime
from enum import Enum
from typing import Any

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from vorpal.core.models.base import Base


class PolicySeverity(str, Enum):
    """Severity level when a policy rule fails."""

    ERROR = "error"  # Blocks the action
    WARNING = "warning"  # Logs warning, allows action
    INFO = "info"  # Informational only


class Policy(Base):
    """Governance policy definition.

    Policies define rules that are evaluated when
    actions are taken on AI systems (deploy, update, etc.).
    """

    __tablename__ = "policies"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
    )

    # Policy identification
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0.0")

    # Whether policy is active
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Matching criteria - when should this policy be evaluated
    match_criteria: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    # Example:
    # {
    #   "risk_tier": ["high", "limited"],
    #   "action": ["deploy", "update"],
    #   "tags": {"contains": ["production"]}
    # }

    # Rules to evaluate (CEL expressions)
    rules: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )
    # Example:
    # [
    #   {
    #     "name": "require-bias-testing",
    #     "condition": "system.controls.exists(c, c.id == 'CTRL-BIAS-001' && c.status == 'verified')",
    #     "message": "High-risk systems require verified bias testing",
    #     "severity": "error"
    #   }
    # ]

    # Default severity for rules that don't specify
    default_severity: Mapped[PolicySeverity] = mapped_column(
        String(20),
        nullable=False,
        default=PolicySeverity.ERROR,
    )

    # Source regulation (if applicable)
    regulation: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )

    # Policy pack this belongs to
    pack_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    # Who created/owns this policy
    created_by: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Metadata
    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        default=dict,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Policy(id={self.id}, name={self.name})>"
