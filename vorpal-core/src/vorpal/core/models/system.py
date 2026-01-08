"""AI System model for the registry."""

from enum import Enum
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, ForeignKey, String, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vorpal.core.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from vorpal.core.models.control import SystemControl
    from vorpal.core.models.user import User, Team


class SystemType(str, Enum):
    """Types of AI systems that can be registered."""

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


class AISystem(Base, UUIDMixin, TimestampMixin):
    """AI System registry entry.

    Represents any AI component that needs governance:
    - ML models
    - AI-powered applications
    - Autonomous agents
    - Processing pipelines
    """

    __tablename__ = "ai_systems"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    type: Mapped[SystemType] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )
    status: Mapped[SystemStatus] = mapped_column(
        String(20),
        nullable=False,
        default=SystemStatus.DRAFT,
        index=True,
    )
    risk_tier: Mapped[RiskTier] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    # Autonomy level (1-5) for agents
    autonomy_level: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Ownership
    owner_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    team_id: Mapped[str | None] = mapped_column(
        ForeignKey("teams.id"),
        nullable=True,
        index=True,
    )

    # Versioning
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Flexible metadata storage
    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        default=dict,
    )

    # Documentation references
    documentation: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    # Tags for categorization
    tags: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="owned_systems")
    team: Mapped["Team | None"] = relationship("Team", back_populates="systems")
    controls: Mapped[list["SystemControl"]] = relationship(
        "SystemControl",
        back_populates="system",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint(
            "autonomy_level IS NULL OR (autonomy_level >= 1 AND autonomy_level <= 5)",
            name="check_autonomy_level_range",
        ),
    )

    def __repr__(self) -> str:
        return f"<AISystem(id={self.id}, name={self.name}, type={self.type})>"
