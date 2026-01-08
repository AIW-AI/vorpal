"""User, Team, and API Key models."""

from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vorpal.core.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from vorpal.core.models.system import AISystem


class User(Base, UUIDMixin, TimestampMixin):
    """User account for the governance platform."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # For SSO/OAuth
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    provider: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Role
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="viewer",
    )  # viewer, editor, admin, compliance_officer

    # Relationships
    owned_systems: Mapped[list["AISystem"]] = relationship("AISystem", back_populates="owner")
    api_keys: Mapped[list["APIKey"]] = relationship("APIKey", back_populates="user")
    team_memberships: Mapped[list["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="user",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


class Team(Base, UUIDMixin, TimestampMixin):
    """Team/organization for grouping users and systems."""

    __tablename__ = "teams"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Settings
    settings: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    systems: Mapped[list["AISystem"]] = relationship("AISystem", back_populates="team")
    members: Mapped[list["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="team",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Team(id={self.id}, name={self.name})>"


class TeamMember(Base):
    """Association between users and teams."""

    __tablename__ = "team_members"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    team_id: Mapped[str] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"),
        primary_key=True,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="member",
    )  # member, admin, owner

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="team_memberships")
    team: Mapped["Team"] = relationship("Team", back_populates="members")


class APIKey(Base, UUIDMixin, TimestampMixin):
    """API key for programmatic access."""

    __tablename__ = "api_keys"

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # The hashed key (we never store the raw key)
    key_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Key prefix for identification (first 8 chars)
    key_prefix: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    # Owner
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Scopes (what this key can do)
    scopes: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )  # e.g., ["systems:read", "systems:write", "policies:read"]

    # Restrictions
    allowed_ips: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    rate_limit: Mapped[int | None] = mapped_column(nullable=True)  # requests per minute

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Expiration
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Usage tracking
    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    use_count: Mapped[int] = mapped_column(default=0, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="api_keys")

    def __repr__(self) -> str:
        return f"<APIKey(id={self.id}, prefix={self.key_prefix})>"
