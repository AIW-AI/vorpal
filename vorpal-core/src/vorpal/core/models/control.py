"""Control models for regulatory compliance tracking."""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vorpal.core.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from vorpal.core.models.system import AISystem


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
    """Implementation status of a control for a system."""

    PENDING = "pending"
    IMPLEMENTED = "implemented"
    TESTED = "tested"
    VERIFIED = "verified"
    FAILED = "failed"
    NOT_APPLICABLE = "not_applicable"


class Control(Base, TimestampMixin):
    """Regulatory control definition.

    Controls are requirements from regulations or frameworks
    that AI systems must satisfy.
    """

    __tablename__ = "controls"

    # Control ID follows pattern: CTRL-{CATEGORY}-{NUMBER}
    id: Mapped[str] = mapped_column(String(50), primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    category: Mapped[ControlCategory] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    # Source regulation/framework
    regulation: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )  # e.g., 'EU-AI-ACT', 'NYC-LL-144', 'NIST-AI-RMF'

    # The actual requirement text
    requirement_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Guidance for testing/verification
    test_guidance: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Whether this control is mandatory
    mandatory: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Risk tiers this control applies to
    applies_to_risk_tiers: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )  # Comma-separated: "high,limited"

    # Relationships
    system_controls: Mapped[list["SystemControl"]] = relationship(
        "SystemControl",
        back_populates="control",
    )

    def __repr__(self) -> str:
        return f"<Control(id={self.id}, name={self.name})>"


class SystemControl(Base):
    """Association between AI systems and controls.

    Tracks the implementation status of each control
    for each registered AI system.
    """

    __tablename__ = "system_controls"

    system_id: Mapped[str] = mapped_column(
        ForeignKey("ai_systems.id", ondelete="CASCADE"),
        primary_key=True,
    )
    control_id: Mapped[str] = mapped_column(
        ForeignKey("controls.id"),
        primary_key=True,
    )

    status: Mapped[ControlStatus] = mapped_column(
        String(20),
        nullable=False,
        default=ControlStatus.PENDING,
    )

    # Whether evidence is required for this control
    evidence_required: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Implementation notes
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Who last updated this
    last_updated_by: Mapped[str | None] = mapped_column(String(255), nullable=True)

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

    # Relationships
    system: Mapped["AISystem"] = relationship("AISystem", back_populates="controls")
    control: Mapped["Control"] = relationship("Control", back_populates="system_controls")

    def __repr__(self) -> str:
        return f"<SystemControl(system={self.system_id}, control={self.control_id})>"
