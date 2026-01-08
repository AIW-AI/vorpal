"""Audit API endpoints."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vorpal.core.api.schemas.audit import (
    AuditChainVerification,
    AuditEventResponse,
    AuditListResponse,
)
from vorpal.core.api.schemas.common import PaginationMeta
from vorpal.core.db import get_session
from vorpal.core.models.audit import AuditEvent

router = APIRouter()


@router.get("", response_model=AuditListResponse)
async def list_audit_events(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    system_id: str | None = None,
    event_type: str | None = None,
    actor_id: str | None = None,
    action: str | None = None,
    resource_type: str | None = None,
    from_date: datetime | None = Query(default=None, alias="from"),
    to_date: datetime | None = Query(default=None, alias="to"),
    db: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Query audit log with filtering."""
    query = select(AuditEvent)

    # Apply filters
    if system_id:
        query = query.where(AuditEvent.system_id == system_id)
    if event_type:
        query = query.where(AuditEvent.event_type == event_type)
    if actor_id:
        query = query.where(AuditEvent.actor_id == actor_id)
    if action:
        query = query.where(AuditEvent.action == action)
    if resource_type:
        query = query.where(AuditEvent.resource_type == resource_type)
    if from_date:
        query = query.where(AuditEvent.timestamp >= from_date)
    if to_date:
        query = query.where(AuditEvent.timestamp <= to_date)

    # Get total count (approximate for performance)
    # In production, consider caching or estimating for large datasets
    from sqlalchemy import func

    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0

    # Apply pagination and ordering
    query = query.order_by(AuditEvent.timestamp.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    events = result.scalars().all()

    return {
        "data": [AuditEventResponse.model_validate(e) for e in events],
        "meta": PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=(total + page_size - 1) // page_size,
        ),
    }


@router.get("/{event_id}", response_model=AuditEventResponse)
async def get_audit_event(
    event_id: str,
    db: AsyncSession = Depends(get_session),
) -> AuditEvent:
    """Get a specific audit event by ID."""
    from fastapi import HTTPException, status

    result = await db.execute(select(AuditEvent).where(AuditEvent.id == event_id))
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit event {event_id} not found",
        )

    return event


@router.get("/verify/chain", response_model=AuditChainVerification)
async def verify_audit_chain(
    system_id: str | None = None,
    from_date: datetime | None = Query(default=None, alias="from"),
    to_date: datetime | None = Query(default=None, alias="to"),
    db: AsyncSession = Depends(get_session),
) -> AuditChainVerification:
    """Verify the integrity of the audit event chain.

    This checks that the hash chain is unbroken, which would
    indicate no tampering has occurred.
    """
    query = select(AuditEvent).order_by(AuditEvent.timestamp.asc())

    if system_id:
        query = query.where(AuditEvent.system_id == system_id)
    if from_date:
        query = query.where(AuditEvent.timestamp >= from_date)
    if to_date:
        query = query.where(AuditEvent.timestamp <= to_date)

    result = await db.execute(query)
    events = result.scalars().all()

    if not events:
        return AuditChainVerification(
            verified=True,
            total_events=0,
            valid_events=0,
            invalid_events=0,
            message="No events to verify",
        )

    valid_count = 0
    invalid_count = 0
    first_invalid_id = None
    previous_hash = None

    for event in events:
        # First event should have no previous hash
        if previous_hash is None and event.previous_hash is not None:
            # Could be valid if we're starting mid-chain
            pass

        # Verify this event's hash
        if event.verify_hash():
            # Verify chain continuity
            if previous_hash is not None and event.previous_hash != previous_hash:
                if first_invalid_id is None:
                    first_invalid_id = event.id
                invalid_count += 1
            else:
                valid_count += 1
        else:
            if first_invalid_id is None:
                first_invalid_id = event.id
            invalid_count += 1

        previous_hash = event.event_hash

    is_verified = invalid_count == 0

    return AuditChainVerification(
        verified=is_verified,
        total_events=len(events),
        valid_events=valid_count,
        invalid_events=invalid_count,
        first_invalid_event_id=first_invalid_id,
        message=(
            "Audit chain integrity verified"
            if is_verified
            else f"Chain integrity compromised: {invalid_count} invalid events"
        ),
    )
