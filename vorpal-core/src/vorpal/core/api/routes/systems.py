"""AI Systems API endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from vorpal.core.api.schemas.common import PaginationMeta
from vorpal.core.api.schemas.system import (
    SystemCreate,
    SystemListResponse,
    SystemResponse,
    SystemUpdate,
)
from vorpal.core.api.schemas.control import SystemControlCreate, SystemControlResponse
from vorpal.core.db import get_session
from vorpal.core.models.system import AISystem, RiskTier, SystemStatus, SystemType
from vorpal.core.models.control import SystemControl, ControlStatus

router = APIRouter()


@router.get("", response_model=SystemListResponse)
async def list_systems(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status: SystemStatus | None = None,
    risk_tier: RiskTier | None = None,
    type: SystemType | None = None,
    team_id: str | None = None,
    db: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """List AI systems with optional filtering."""
    query = select(AISystem)

    # Apply filters
    if status:
        query = query.where(AISystem.status == status)
    if risk_tier:
        query = query.where(AISystem.risk_tier == risk_tier)
    if type:
        query = query.where(AISystem.type == type)
    if team_id:
        query = query.where(AISystem.team_id == team_id)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0

    # Apply pagination
    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(AISystem.created_at.desc())

    result = await db.execute(query)
    systems = result.scalars().all()

    return {
        "data": [SystemResponse.model_validate(s) for s in systems],
        "meta": PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=(total + page_size - 1) // page_size,
        ),
    }


@router.post("", response_model=SystemResponse, status_code=status.HTTP_201_CREATED)
async def create_system(
    system_in: SystemCreate,
    db: AsyncSession = Depends(get_session),
) -> AISystem:
    """Register a new AI system."""
    # For now, use a placeholder owner_id (would come from auth in production)
    owner_id = system_in.owner_id or "00000000-0000-0000-0000-000000000000"

    system = AISystem(
        name=system_in.name,
        description=system_in.description,
        type=system_in.type,
        status=SystemStatus.DRAFT,
        risk_tier=system_in.risk_tier,
        autonomy_level=system_in.autonomy_level,
        owner_id=owner_id,
        team_id=system_in.team_id,
        version=system_in.version,
        metadata_=system_in.metadata_,
        documentation=system_in.documentation,
        tags=system_in.tags,
    )

    db.add(system)
    await db.flush()
    await db.refresh(system)

    return system


@router.get("/{system_id}", response_model=SystemResponse)
async def get_system(
    system_id: str,
    db: AsyncSession = Depends(get_session),
) -> AISystem:
    """Get a specific AI system by ID."""
    result = await db.execute(select(AISystem).where(AISystem.id == system_id))
    system = result.scalar_one_or_none()

    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"System {system_id} not found",
        )

    return system


@router.patch("/{system_id}", response_model=SystemResponse)
async def update_system(
    system_id: str,
    system_in: SystemUpdate,
    db: AsyncSession = Depends(get_session),
) -> AISystem:
    """Update an AI system."""
    result = await db.execute(select(AISystem).where(AISystem.id == system_id))
    system = result.scalar_one_or_none()

    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"System {system_id} not found",
        )

    # Update only provided fields
    update_data = system_in.model_dump(exclude_unset=True, by_alias=False)
    for field, value in update_data.items():
        if field == "metadata_":
            setattr(system, "metadata_", value)
        else:
            setattr(system, field, value)

    await db.flush()
    await db.refresh(system)

    return system


@router.delete("/{system_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system(
    system_id: str,
    db: AsyncSession = Depends(get_session),
) -> None:
    """Archive (soft delete) an AI system."""
    result = await db.execute(select(AISystem).where(AISystem.id == system_id))
    system = result.scalar_one_or_none()

    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"System {system_id} not found",
        )

    # Soft delete by setting status to deprecated
    system.status = SystemStatus.DEPRECATED
    await db.flush()


@router.get("/{system_id}/controls", response_model=list[SystemControlResponse])
async def list_system_controls(
    system_id: str,
    db: AsyncSession = Depends(get_session),
) -> list[SystemControl]:
    """List controls assigned to a system."""
    # Verify system exists
    system_result = await db.execute(select(AISystem).where(AISystem.id == system_id))
    if not system_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"System {system_id} not found",
        )

    result = await db.execute(
        select(SystemControl)
        .where(SystemControl.system_id == system_id)
        .options(selectinload(SystemControl.control))
    )
    return list(result.scalars().all())


@router.post(
    "/{system_id}/controls",
    response_model=SystemControlResponse,
    status_code=status.HTTP_201_CREATED,
)
async def assign_control(
    system_id: str,
    control_in: SystemControlCreate,
    db: AsyncSession = Depends(get_session),
) -> SystemControl:
    """Assign a control to a system."""
    # Verify system exists
    system_result = await db.execute(select(AISystem).where(AISystem.id == system_id))
    if not system_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"System {system_id} not found",
        )

    # Check if already assigned
    existing = await db.execute(
        select(SystemControl).where(
            SystemControl.system_id == system_id,
            SystemControl.control_id == control_in.control_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Control {control_in.control_id} already assigned to system",
        )

    system_control = SystemControl(
        system_id=system_id,
        control_id=control_in.control_id,
        status=ControlStatus.PENDING,
        evidence_required=control_in.evidence_required,
        notes=control_in.notes,
    )

    db.add(system_control)
    await db.flush()
    await db.refresh(system_control)

    return system_control
