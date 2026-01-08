# Tutorial: Creating Governance Controls

This tutorial shows how to define and manage governance controls.

## What Are Controls?

Controls are specific requirements that AI systems must satisfy. They come from:

- **Regulations** (EU AI Act, NYC LL 144)
- **Frameworks** (NIST AI RMF, ISO 42001)
- **Internal policies** (your organization's standards)

## Step 1: Understanding Control Structure

Each control has:

```yaml
id: CTRL-BIAS-001          # Unique identifier
name: Annual Bias Audit    # Human-readable name
category: bias             # Type of control
regulation: NYC-LL-144     # Source regulation
requirement_text: "..."    # Full requirement
test_guidance: "..."       # How to verify
mandatory: true            # Is it required?
applies_to_risk_tiers: "high,limited"  # Which tiers
```

## Step 2: Create a Control via CLI

```bash
# This would be done via API - CLI example for illustration
curl -X POST "http://localhost:8000/api/v1/controls" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "CTRL-BIAS-001",
    "name": "Annual Bias Audit",
    "category": "bias",
    "regulation": "NYC-LL-144",
    "requirement_text": "Employers using automated employment decision tools must conduct an annual bias audit",
    "test_guidance": "Calculate selection rates by demographic group and compute impact ratios",
    "mandatory": true,
    "applies_to_risk_tiers": "high,limited"
  }'
```

## Step 3: Create Controls via SDK

```python
from vorpal import VorpalClient

client = VorpalClient(base_url="http://localhost:8000")

# Create an accuracy control
accuracy_control = client.controls.create(
    id="CTRL-ACC-001",
    name="Model Accuracy Threshold",
    category="accuracy",
    regulation="EU-AI-ACT",
    requirement_text="High-risk AI systems shall achieve levels of accuracy appropriate to their intended purpose",
    test_guidance="""
    1. Run model on held-out test set (minimum 10,000 samples)
    2. Calculate accuracy, precision, recall, F1
    3. Compare against baseline and threshold
    4. Document any significant degradation
    """,
    mandatory=True,
)

# Create a bias control
bias_control = client.controls.create(
    id="CTRL-BIAS-001",
    name="Demographic Parity Testing",
    category="bias",
    regulation="NYC-LL-144",
    requirement_text="Selection rates must not show adverse impact against protected groups",
    test_guidance="""
    1. Collect predictions by demographic group
    2. Calculate selection rate for each group
    3. Compute impact ratio (min rate / max rate)
    4. Flag if impact ratio < 0.8 (4/5ths rule)
    """,
    mandatory=True,
)

# Create a transparency control
transparency_control = client.controls.create(
    id="CTRL-TRANS-001",
    name="User Disclosure",
    category="transparency",
    regulation="EU-AI-ACT",
    requirement_text="Users must be informed when interacting with AI systems",
    test_guidance="""
    1. Review UI/UX for clear AI disclosure
    2. Verify disclosure appears before interaction
    3. Test disclosure visibility and clarity
    """,
    mandatory=True,
)

print(f"Created controls: {accuracy_control.id}, {bias_control.id}, {transparency_control.id}")
```

## Step 4: Assign Controls to Systems

```python
# Get a system
system = client.systems.get("550e8400-e29b-41d4-a716-446655440000")

# Assign controls based on risk tier
if system.risk_tier.value == "high":
    # Assign all mandatory controls for high-risk
    client.systems.assign_control(
        system.id,
        control_id="CTRL-ACC-001",
        notes="Required for high-risk deployment"
    )
    client.systems.assign_control(
        system.id,
        control_id="CTRL-BIAS-001",
        notes="Required by NYC LL 144 for employment decisions"
    )

# Assign transparency control for customer-facing
if "customer-facing" in system.tags:
    client.systems.assign_control(
        system.id,
        control_id="CTRL-TRANS-001",
        notes="User-facing AI requires disclosure"
    )
```

## Step 5: Update Control Status

As you implement and verify controls:

```python
# After implementing
client.systems.update_control(
    system_id="550e8400-...",
    control_id="CTRL-ACC-001",
    status="implemented",
    notes="Accuracy testing suite added in PR #123"
)

# After testing
client.systems.update_control(
    system_id="550e8400-...",
    control_id="CTRL-ACC-001",
    status="tested",
    notes="All tests passing, accuracy at 96.2%"
)

# After independent verification
client.systems.update_control(
    system_id="550e8400-...",
    control_id="CTRL-ACC-001",
    status="verified",
    notes="Verified by compliance team on 2026-01-15"
)
```

## Step 6: List System Controls

```python
# Get all controls for a system
system_controls = client.systems.get_controls("550e8400-...")

print(f"Controls for {system.name}:")
for sc in system_controls:
    status_emoji = {
        "pending": "⏳",
        "implemented": "🔧",
        "tested": "🧪",
        "verified": "✅",
        "failed": "❌"
    }.get(sc.status, "❓")

    print(f"  {status_emoji} {sc.control_id}: {sc.status}")
```

## Control Categories

| Category | Description |
|----------|-------------|
| `accuracy` | Model performance requirements |
| `bias` | Fairness and discrimination testing |
| `security` | Data security and access controls |
| `privacy` | Data protection and PII handling |
| `safety` | Physical and operational safety |
| `transparency` | Explainability and disclosure |
| `robustness` | Reliability and error handling |
| `accountability` | Governance and oversight |

## Pre-built Control Libraries

Vorpal includes control libraries for common regulations:

```python
# List available controls
controls, _ = client.controls.list()

# Filter by regulation
eu_controls, _ = client.controls.list(regulation="EU-AI-ACT")
nyc_controls, _ = client.controls.list(regulation="NYC-LL-144")
nist_controls, _ = client.controls.list(regulation="NIST-AI-RMF")
```

## Next Steps

- [Writing Policies](./03-writing-policies.md)
- [EU AI Act Compliance](./eu-ai-act-compliance.md)

## Complete Example

```python
"""Complete example: Setting up controls for an HR AI system."""

from vorpal import VorpalClient, SystemType, RiskTier

client = VorpalClient(base_url="http://localhost:8000")

# 1. Register the HR screening system
hr_system = client.systems.create(
    name="resume-screening-ai",
    type=SystemType.MODEL,
    risk_tier=RiskTier.HIGH,  # Employment = high risk
    description="AI model for initial resume screening",
    metadata={
        "use_case": "employment_decision",
        "jurisdiction": "NYC"
    },
    tags=["hr", "employment", "nyc"]
)

# 2. Create NYC LL 144 required controls
controls = [
    {
        "id": "CTRL-LL144-001",
        "name": "Annual Bias Audit",
        "category": "bias",
        "regulation": "NYC-LL-144",
        "requirement_text": "Annual independent bias audit required",
        "mandatory": True
    },
    {
        "id": "CTRL-LL144-002",
        "name": "Candidate Notification",
        "category": "transparency",
        "regulation": "NYC-LL-144",
        "requirement_text": "Candidates must be notified of AEDT use",
        "mandatory": True
    },
    {
        "id": "CTRL-LL144-003",
        "name": "Audit Publication",
        "category": "transparency",
        "regulation": "NYC-LL-144",
        "requirement_text": "Audit results must be publicly available",
        "mandatory": True
    }
]

for ctrl in controls:
    try:
        client.controls.create(**ctrl)
        print(f"✓ Created control: {ctrl['id']}")
    except Exception as e:
        print(f"  Control {ctrl['id']} may already exist")

# 3. Assign controls to system
for ctrl in controls:
    client.systems.assign_control(
        hr_system.id,
        control_id=ctrl["id"],
        notes=f"Required by {ctrl['regulation']}"
    )
    print(f"✓ Assigned {ctrl['id']} to {hr_system.name}")

# 4. Check compliance status
system_controls = client.systems.get_controls(hr_system.id)
pending = [sc for sc in system_controls if sc.status == "pending"]
print(f"\n{len(pending)} controls pending implementation")
```
