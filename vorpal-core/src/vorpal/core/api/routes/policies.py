"""Policies API endpoints."""

from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from vorpal.core.api.schemas.common import PaginationMeta
from vorpal.core.api.schemas.policy import (
    PolicyCreate,
    PolicyEvaluateRequest,
    PolicyEvaluateResponse,
    PolicyListResponse,
    PolicyResponse,
    PolicyResult,
    PolicyUpdate,
    RuleResult,
)
from vorpal.core.db import get_session
from vorpal.core.models.policy import Policy, PolicySeverity
from vorpal.core.models.system import AISystem

router = APIRouter()


@router.get("", response_model=PolicyListResponse)
async def list_policies(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    enabled: bool | None = None,
    regulation: str | None = None,
    pack_name: str | None = None,
    db: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """List policies with optional filtering."""
    query = select(Policy)

    # Apply filters
    if enabled is not None:
        query = query.where(Policy.enabled == enabled)
    if regulation:
        query = query.where(Policy.regulation == regulation)
    if pack_name:
        query = query.where(Policy.pack_name == pack_name)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0

    # Apply pagination
    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(Policy.created_at.desc())

    result = await db.execute(query)
    policies = result.scalars().all()

    return {
        "data": [PolicyResponse.model_validate(p) for p in policies],
        "meta": PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=(total + page_size - 1) // page_size,
        ),
    }


@router.post("", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    policy_in: PolicyCreate,
    db: AsyncSession = Depends(get_session),
) -> Policy:
    """Create a new policy."""
    # Check if policy name already exists
    existing = await db.execute(select(Policy).where(Policy.name == policy_in.name))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Policy '{policy_in.name}' already exists",
        )

    policy = Policy(
        id=str(uuid4()),
        name=policy_in.name,
        description=policy_in.description,
        version=policy_in.version,
        enabled=policy_in.enabled,
        match_criteria=policy_in.match_criteria,
        rules=[r.model_dump() for r in policy_in.rules],
        default_severity=policy_in.default_severity,
        regulation=policy_in.regulation,
        pack_name=policy_in.pack_name,
        metadata_=policy_in.metadata_,
    )

    db.add(policy)
    await db.flush()
    await db.refresh(policy)

    return policy


@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    policy_id: str,
    db: AsyncSession = Depends(get_session),
) -> Policy:
    """Get a specific policy by ID."""
    result = await db.execute(select(Policy).where(Policy.id == policy_id))
    policy = result.scalar_one_or_none()

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy {policy_id} not found",
        )

    return policy


@router.patch("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    policy_id: str,
    policy_in: PolicyUpdate,
    db: AsyncSession = Depends(get_session),
) -> Policy:
    """Update a policy."""
    result = await db.execute(select(Policy).where(Policy.id == policy_id))
    policy = result.scalar_one_or_none()

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy {policy_id} not found",
        )

    # Update only provided fields
    update_data = policy_in.model_dump(exclude_unset=True, by_alias=False)
    for field, value in update_data.items():
        if field == "rules" and value is not None:
            value = [r.model_dump() if hasattr(r, "model_dump") else r for r in value]
        if field == "metadata_":
            setattr(policy, "metadata_", value)
        else:
            setattr(policy, field, value)

    await db.flush()
    await db.refresh(policy)

    return policy


@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(
    policy_id: str,
    db: AsyncSession = Depends(get_session),
) -> None:
    """Delete a policy."""
    result = await db.execute(select(Policy).where(Policy.id == policy_id))
    policy = result.scalar_one_or_none()

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy {policy_id} not found",
        )

    await db.delete(policy)
    await db.flush()


@router.post("/evaluate", response_model=PolicyEvaluateResponse)
async def evaluate_policies(
    request: PolicyEvaluateRequest,
    db: AsyncSession = Depends(get_session),
) -> PolicyEvaluateResponse:
    """Evaluate policies against a system action.

    This endpoint checks all matching policies and returns
    whether the action is allowed based on rule evaluation.
    """
    # Get the system
    system_result = await db.execute(
        select(AISystem).where(AISystem.id == request.system_id)
    )
    system = system_result.scalar_one_or_none()

    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"System {request.system_id} not found",
        )

    # Get all enabled policies
    policies_result = await db.execute(
        select(Policy).where(Policy.enabled == True)  # noqa: E712
    )
    policies = policies_result.scalars().all()

    # Evaluate each policy
    results: list[PolicyResult] = []
    blocking_failures: list[str] = []
    warnings: list[str] = []

    for policy in policies:
        # Check if policy matches this system/action
        if not _policy_matches(policy, system, request.action):
            continue

        # Evaluate rules
        rule_results: list[RuleResult] = []
        policy_passed = True

        for rule in policy.rules:
            # For now, use a simple evaluation (CEL integration would go here)
            rule_passed = _evaluate_rule(rule, system, request.context)
            severity = PolicySeverity(rule.get("severity", policy.default_severity))

            rule_result = RuleResult(
                rule_name=rule["name"],
                passed=rule_passed,
                message=rule.get("message") if not rule_passed else None,
                severity=severity,
            )
            rule_results.append(rule_result)

            if not rule_passed:
                if severity == PolicySeverity.ERROR:
                    policy_passed = False
                    blocking_failures.append(rule["message"])
                elif severity == PolicySeverity.WARNING:
                    warnings.append(rule["message"])

        results.append(
            PolicyResult(
                policy_id=policy.id,
                policy_name=policy.name,
                passed=policy_passed,
                rule_results=rule_results,
            )
        )

    # Determine overall result
    policies_failed = sum(1 for r in results if not r.passed)
    allowed = policies_failed == 0

    return PolicyEvaluateResponse(
        allowed=allowed,
        system_id=request.system_id,
        action=request.action,
        policies_evaluated=len(results),
        policies_passed=len(results) - policies_failed,
        policies_failed=policies_failed,
        results=results,
        blocking_failures=blocking_failures,
        warnings=warnings,
    )


def _policy_matches(policy: Policy, system: AISystem, action: str) -> bool:
    """Check if a policy's match criteria apply to this system/action."""
    criteria = policy.match_criteria

    # Check risk_tier match
    if "risk_tier" in criteria:
        allowed_tiers = criteria["risk_tier"]
        if isinstance(allowed_tiers, str):
            allowed_tiers = [allowed_tiers]
        if system.risk_tier.value not in allowed_tiers:
            return False

    # Check action match
    if "action" in criteria:
        allowed_actions = criteria["action"]
        if isinstance(allowed_actions, str):
            allowed_actions = [allowed_actions]
        if action not in allowed_actions:
            return False

    # Check type match
    if "type" in criteria:
        allowed_types = criteria["type"]
        if isinstance(allowed_types, str):
            allowed_types = [allowed_types]
        if system.type.value not in allowed_types:
            return False

    # Check tags match
    if "tags" in criteria:
        tag_criteria = criteria["tags"]
        if "contains" in tag_criteria:
            required_tags = tag_criteria["contains"]
            if not any(tag in system.tags for tag in required_tags):
                return False

    return True


def _evaluate_rule(
    rule: dict[str, Any],
    system: AISystem,
    context: dict[str, Any],
) -> bool:
    """Evaluate a policy rule.

    This is a simplified evaluation. In production, this would
    use CEL (Common Expression Language) for complex conditions.
    """
    condition = rule.get("condition", "true")

    # For now, implement some basic patterns
    # In production, integrate with cel-python or OPA

    # Simple always-pass/fail conditions
    if condition == "true":
        return True
    if condition == "false":
        return False

    # Basic autonomy level check
    if "autonomy_level" in condition and "<=" in condition:
        if system.autonomy_level is not None:
            try:
                # Extract number from condition like "system.autonomy_level <= 3"
                parts = condition.split("<=")
                if len(parts) == 2:
                    threshold = int(parts[1].strip())
                    return system.autonomy_level <= threshold
            except (ValueError, IndexError):
                pass

    # Default to passing (permissive by default for demo)
    # In production, default to fail for security
    return True
