# Tutorial: Writing Policies

This tutorial shows how to create policies that enforce governance rules.

## What Are Policies?

Policies define rules that are evaluated when actions are performed on AI systems. They can:

- **Block** deployments that don't meet requirements
- **Warn** about potential issues
- **Enforce** controls before actions proceed

## Step 1: Policy Structure

A policy has three main parts:

1. **Match Criteria** - When should this policy apply?
2. **Rules** - What conditions must be met?
3. **Actions** - What happens when rules fail?

```yaml
name: high-risk-deployment-gates
match_criteria:
  risk_tier: ["high"]
  action: ["deploy"]
rules:
  - name: require-bias-testing
    condition: "CEL expression"
    message: "Error message"
    severity: error
```

## Step 2: Create a Simple Policy

```python
from vorpal import VorpalClient
from vorpal.types import PolicyRule, PolicySeverity

client = VorpalClient(base_url="http://localhost:8000")

# Policy: Require documentation for all deployments
policy = client.policies.create(
    name="deployment-requires-docs",
    description="All deployments must have documentation",
    match_criteria={
        "action": ["deploy"]
    },
    rules=[
        PolicyRule(
            name="has-technical-docs",
            condition="system.documentation.technical_doc != null",
            message="System must have technical documentation before deployment",
            severity=PolicySeverity.ERROR
        )
    ]
)

print(f"Created policy: {policy.id}")
```

## Step 3: Create a Risk-Based Policy

```python
# Policy: Extra requirements for high-risk systems
high_risk_policy = client.policies.create(
    name="high-risk-deployment-gates",
    description="High-risk systems require additional controls",
    match_criteria={
        "risk_tier": ["high"],
        "action": ["deploy", "update"]
    },
    rules=[
        PolicyRule(
            name="require-bias-testing",
            condition="system.controls.exists(c, c.id == 'CTRL-BIAS-001' && c.status == 'verified')",
            message="High-risk systems require verified bias testing",
            severity=PolicySeverity.ERROR
        ),
        PolicyRule(
            name="require-accuracy-testing",
            condition="system.controls.exists(c, c.id == 'CTRL-ACC-001' && c.status == 'verified')",
            message="High-risk systems require verified accuracy testing",
            severity=PolicySeverity.ERROR
        ),
        PolicyRule(
            name="require-risk-assessment",
            condition="system.documentation.risk_assessment != null",
            message="High-risk systems require risk assessment documentation",
            severity=PolicySeverity.ERROR
        ),
        PolicyRule(
            name="recommend-hitl",
            condition="system.metadata.hitl_enabled == true || system.autonomy_level <= 2",
            message="Consider enabling human-in-the-loop for high-risk systems",
            severity=PolicySeverity.WARNING
        )
    ],
    regulation="EU-AI-ACT",
    pack_name="eu-ai-act-high-risk"
)
```

## Step 4: Evaluate a Policy

```python
# Try to deploy a system
result = client.policies.evaluate(
    system_id="550e8400-e29b-41d4-a716-446655440000",
    action="deploy"
)

if result.allowed:
    print("✓ Deployment approved!")
    # Proceed with deployment
else:
    print("✗ Deployment blocked!")
    print(f"  Policies failed: {result.policies_failed}")
    for failure in result.blocking_failures:
        print(f"  - {failure}")

if result.warnings:
    print("\nWarnings:")
    for warning in result.warnings:
        print(f"  ⚠ {warning}")
```

## Step 5: Policy for Agents

```python
# Policy: Agent autonomy restrictions
agent_policy = client.policies.create(
    name="agent-autonomy-limits",
    description="Restrict agent autonomy levels based on capabilities",
    match_criteria={
        "type": ["agent"],
        "action": ["deploy", "update"]
    },
    rules=[
        PolicyRule(
            name="max-autonomy-level",
            condition="system.autonomy_level <= 4",
            message="L5 autonomy requires executive approval",
            severity=PolicySeverity.ERROR
        ),
        PolicyRule(
            name="production-requires-hitl",
            condition="'production' not in system.tags || system.metadata.hitl_enabled == true",
            message="Production agents require HITL enabled",
            severity=PolicySeverity.ERROR
        ),
        PolicyRule(
            name="high-autonomy-warning",
            condition="system.autonomy_level <= 3",
            message="Agents with L4+ autonomy should have enhanced monitoring",
            severity=PolicySeverity.WARNING
        )
    ]
)
```

## Step 6: Using Match Criteria

### Match by Risk Tier

```python
match_criteria={
    "risk_tier": ["high", "limited"]  # Both tiers
}
```

### Match by Action

```python
match_criteria={
    "action": ["deploy"]  # Only deployment
}

match_criteria={
    "action": ["deploy", "update", "delete"]  # Multiple actions
}
```

### Match by System Type

```python
match_criteria={
    "type": ["agent", "model"]
}
```

### Match by Tags

```python
match_criteria={
    "tags": {
        "contains": ["production", "customer-facing"]
    }
}
```

### Combined Criteria

```python
match_criteria={
    "risk_tier": ["high"],
    "type": ["agent"],
    "action": ["deploy"],
    "tags": {
        "contains": ["production"]
    }
}
```

## Step 7: Writing CEL Conditions

### Basic Comparisons

```cel
# String equality
system.risk_tier == "high"

# Numeric comparison
system.autonomy_level <= 3
system.autonomy_level >= 1 && system.autonomy_level <= 5

# Null checks
system.description != null
system.documentation.risk_assessment != null
```

### List Operations

```cel
# Check if tag exists
"production" in system.tags

# Check if any control exists
system.controls.exists(c, c.id == "CTRL-BIAS-001")

# Check control with status
system.controls.exists(c, c.id == "CTRL-BIAS-001" && c.status == "verified")

# Check all controls verified
system.controls.all(c, c.status == "verified")

# Count verified controls
size(system.controls.filter(c, c.status == "verified")) >= 3
```

### Metadata Access

```cel
# Check metadata field
system.metadata.hitl_enabled == true

# Check nested metadata
system.metadata.performance.accuracy >= 0.95
```

### Complex Conditions

```cel
# Multiple conditions
system.risk_tier == "high" &&
system.controls.exists(c, c.id == "CTRL-BIAS-001" && c.status == "verified") &&
system.documentation.risk_assessment != null

# Conditional logic
system.type != "agent" || system.autonomy_level <= 3

# Check for any of multiple controls
system.controls.exists(c, c.id == "CTRL-BIAS-001") ||
system.controls.exists(c, c.id == "CTRL-BIAS-002")
```

## Step 8: Severity Levels

| Severity | Effect | Use Case |
|----------|--------|----------|
| `error` | Blocks action | Must-have requirements |
| `warning` | Logs warning | Best practices |
| `info` | Informational | Recommendations |

```python
# Error: Blocks deployment
PolicyRule(
    name="critical-control",
    condition="...",
    message="This is required",
    severity=PolicySeverity.ERROR  # Blocks if fails
)

# Warning: Logs but allows
PolicyRule(
    name="recommended-practice",
    condition="...",
    message="Consider doing this",
    severity=PolicySeverity.WARNING  # Warns if fails
)
```

## Complete Example

```python
"""Complete example: Comprehensive deployment policy."""

from vorpal import VorpalClient
from vorpal.types import PolicyRule, PolicySeverity

client = VorpalClient(base_url="http://localhost:8000")

# Create comprehensive deployment policy
deployment_policy = client.policies.create(
    name="comprehensive-deployment-gates",
    description="Complete deployment requirements based on risk tier",
    match_criteria={
        "action": ["deploy"]
    },
    rules=[
        # Documentation requirements (all systems)
        PolicyRule(
            name="has-description",
            condition="system.description != null && size(system.description) > 10",
            message="All systems must have a meaningful description",
            severity=PolicySeverity.ERROR
        ),

        # High-risk specific
        PolicyRule(
            name="high-risk-bias-testing",
            condition="system.risk_tier != 'high' || system.controls.exists(c, c.id == 'CTRL-BIAS-001' && c.status == 'verified')",
            message="High-risk systems require verified bias testing",
            severity=PolicySeverity.ERROR
        ),
        PolicyRule(
            name="high-risk-accuracy-testing",
            condition="system.risk_tier != 'high' || system.controls.exists(c, c.id == 'CTRL-ACC-001' && c.status == 'verified')",
            message="High-risk systems require verified accuracy testing",
            severity=PolicySeverity.ERROR
        ),

        # Agent specific
        PolicyRule(
            name="agent-autonomy-limit",
            condition="system.type != 'agent' || system.autonomy_level <= 4",
            message="Agent autonomy level cannot exceed L4 without approval",
            severity=PolicySeverity.ERROR
        ),
        PolicyRule(
            name="agent-hitl-recommended",
            condition="system.type != 'agent' || system.metadata.hitl_enabled == true || system.autonomy_level <= 2",
            message="Consider enabling HITL for production agents",
            severity=PolicySeverity.WARNING
        ),

        # Version tracking
        PolicyRule(
            name="has-version",
            condition="system.version != null",
            message="Systems should have version tracking",
            severity=PolicySeverity.WARNING
        )
    ]
)

# Test the policy
test_systems = [
    "550e8400-e29b-41d4-a716-446655440000",  # High-risk model
    "550e8400-e29b-41d4-a716-446655440001",  # Agent
]

for system_id in test_systems:
    result = client.policies.evaluate(
        system_id=system_id,
        action="deploy"
    )

    system = client.systems.get(system_id)
    print(f"\n{system.name}:")
    print(f"  Allowed: {result.allowed}")
    print(f"  Policies evaluated: {result.policies_evaluated}")

    if result.blocking_failures:
        print("  Blocking issues:")
        for f in result.blocking_failures:
            print(f"    ❌ {f}")

    if result.warnings:
        print("  Warnings:")
        for w in result.warnings:
            print(f"    ⚠️ {w}")
```

## Next Steps

- [Integrating with CI/CD](./04-cicd-integration.md)
- [Advanced Policy Rules](./advanced-policy-rules.md)
