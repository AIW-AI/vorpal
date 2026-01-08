"""Audit event model for immutable logging."""

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from vorpal.core.models.base import Base


class ActorType(str, Enum):
    """Type of entity that performed an action."""

    USER = "user"
    SYSTEM = "system"
    API_KEY = "api_key"
    AGENT = "agent"
    SCHEDULER = "scheduler"


class AuditEvent(Base):
    """Immutable audit event with hash chain integrity.

    Each event contains a hash of the previous event,
    creating a tamper-evident chain. Any modification
    to historical events will break the chain.
    """

    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
    )

    # Which AI system this event relates to (optional)
    system_id: Mapped[str | None] = mapped_column(
        ForeignKey("ai_systems.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Event classification
    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )  # e.g., 'system.created', 'policy.evaluated', 'control.updated'

    # Who performed the action
    actor_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    actor_type: Mapped[ActorType] = mapped_column(
        String(20),
        nullable=False,
    )
    actor_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # What happened
    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )  # e.g., 'create', 'update', 'delete', 'evaluate', 'approve'

    # What was affected
    resource_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )  # e.g., 'ai_system', 'control', 'policy'
    resource_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Additional context
    details: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    # Request context
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Hash chain for integrity
    previous_hash: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )  # SHA-256 of previous event
    event_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
    )

    # Timestamp (immutable after creation)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("idx_audit_system_timestamp", "system_id", "timestamp"),
        Index("idx_audit_event_type_timestamp", "event_type", "timestamp"),
        Index("idx_audit_actor_timestamp", "actor_id", "timestamp"),
    )

    @staticmethod
    def compute_hash(
        event_id: str,
        event_type: str,
        action: str,
        actor_id: str | None,
        resource_type: str | None,
        resource_id: str | None,
        details: dict[str, Any],
        timestamp: datetime,
        previous_hash: str | None,
    ) -> str:
        """Compute SHA-256 hash for event integrity.

        The hash includes all critical fields to ensure
        tampering with any field is detectable.
        """
        payload = {
            "id": event_id,
            "event_type": event_type,
            "action": action,
            "actor_id": actor_id,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details,
            "timestamp": timestamp.isoformat(),
            "previous_hash": previous_hash,
        }
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode()).hexdigest()

    def verify_hash(self) -> bool:
        """Verify this event's hash is correct."""
        computed = self.compute_hash(
            event_id=self.id,
            event_type=self.event_type,
            action=self.action,
            actor_id=self.actor_id,
            resource_type=self.resource_type,
            resource_id=self.resource_id,
            details=self.details,
            timestamp=self.timestamp,
            previous_hash=self.previous_hash,
        )
        return computed == self.event_hash

    def __repr__(self) -> str:
        return f"<AuditEvent(id={self.id}, type={self.event_type}, action={self.action})>"
