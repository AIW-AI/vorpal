# EU AI Act Policy Pack

This pack implements requirements from the European Union Artificial Intelligence Act.

## Overview

The EU AI Act establishes a risk-based framework for AI regulation:

| Risk Level | Examples | Requirements |
|------------|----------|--------------|
| **Prohibited** | Social scoring, real-time biometric | Banned |
| **High-Risk** | Employment, credit, healthcare | Full compliance |
| **Limited** | Chatbots, emotion recognition | Transparency |
| **Minimal** | Spam filters, games | No requirements |

## When It Applies

- **Effective Date**: August 2, 2026 (high-risk provisions)
- **Scope**: AI systems deployed in or affecting EU citizens
- **Applies To**: Both providers and deployers of AI systems

## Controls Included

### High-Risk System Controls

| Control ID | Article | Requirement |
|------------|---------|-------------|
| `CTRL-EUAI-001` | Art 9 | Risk Management System |
| `CTRL-EUAI-002` | Art 10 | Data Governance |
| `CTRL-EUAI-003` | Art 11 | Technical Documentation |
| `CTRL-EUAI-004` | Art 12 | Record-Keeping |
| `CTRL-EUAI-005` | Art 13 | Transparency |
| `CTRL-EUAI-006` | Art 14 | Human Oversight |
| `CTRL-EUAI-007` | Art 15 | Accuracy & Robustness |

### Control Details

#### CTRL-EUAI-001: Risk Management System

```yaml
id: CTRL-EUAI-001
name: Risk Management System
category: accountability
regulation: EU-AI-ACT
article: "Article 9"
requirement_text: |
  A risk management system shall be established, implemented, documented
  and maintained in relation to high-risk AI systems.
test_guidance: |
  1. Verify risk management process exists
  2. Check risk identification documentation
  3. Review mitigation measures
  4. Confirm ongoing monitoring plan
mandatory: true
applies_to_risk_tiers: "high"
```

#### CTRL-EUAI-006: Human Oversight

```yaml
id: CTRL-EUAI-006
name: Human Oversight Measures
category: safety
regulation: EU-AI-ACT
article: "Article 14"
requirement_text: |
  High-risk AI systems shall be designed and developed in such a way that
  they can be effectively overseen by natural persons.
test_guidance: |
  1. Verify human can understand AI outputs
  2. Check override/intervention capability
  3. Review monitoring tools available
  4. Confirm stop functionality exists
mandatory: true
applies_to_risk_tiers: "high"
```

## Policies Included

### High-Risk Deployment Gate

```yaml
name: eu-ai-act-high-risk-deployment
match_criteria:
  risk_tier: ["high"]
  action: ["deploy"]
rules:
  - name: risk-management-verified
    condition: |
      system.controls.exists(c,
        c.id == "CTRL-EUAI-001" &&
        c.status == "verified"
      )
    message: "High-risk systems require verified risk management system"
    severity: error

  - name: technical-documentation
    condition: |
      system.documentation.technical_doc != null
    message: "High-risk systems require technical documentation"
    severity: error

  - name: human-oversight
    condition: |
      system.controls.exists(c,
        c.id == "CTRL-EUAI-006" &&
        c.status == "verified"
      )
    message: "High-risk systems require human oversight measures"
    severity: error

  - name: accuracy-testing
    condition: |
      system.controls.exists(c,
        c.id == "CTRL-EUAI-007" &&
        c.status == "verified"
      )
    message: "High-risk systems require accuracy and robustness testing"
    severity: error
```

### Limited Risk Transparency

```yaml
name: eu-ai-act-limited-risk-transparency
match_criteria:
  risk_tier: ["limited"]
  action: ["deploy"]
rules:
  - name: user-disclosure
    condition: |
      system.documentation.user_disclosure != null ||
      system.metadata.disclosure_implemented == true
    message: "Limited-risk systems require user disclosure of AI interaction"
    severity: error
```

## Installation

```python
from vorpal import VorpalClient
from vorpal.packs import EUAIActPack

client = VorpalClient(base_url="http://localhost:8000")

# Install the pack
pack = EUAIActPack()
pack.install(client)

print(f"Installed {len(pack.controls)} controls")
print(f"Installed {len(pack.policies)} policies")
```

## Usage Example

```python
# 1. Register a high-risk system
system = client.systems.create(
    name="credit-scoring-model",
    type=SystemType.MODEL,
    risk_tier=RiskTier.HIGH,
    description="ML model for consumer credit decisions",
    tags=["financial", "eu-ai-act-high-risk"]
)

# 2. Assign EU AI Act controls
for ctrl_id in ["CTRL-EUAI-001", "CTRL-EUAI-003", "CTRL-EUAI-006", "CTRL-EUAI-007"]:
    client.systems.assign_control(system.id, ctrl_id)

# 3. Implement and verify controls
# ... implementation work ...

client.systems.update_control(
    system.id,
    "CTRL-EUAI-001",
    status="verified",
    notes="Risk management process documented in Confluence"
)

# 4. Attempt deployment
result = client.policies.evaluate(system.id, "deploy")

if not result.allowed:
    print("Deployment blocked. Outstanding requirements:")
    for failure in result.blocking_failures:
        print(f"  - {failure}")
```

## Compliance Checklist

### For High-Risk Systems

- [ ] System registered with `risk_tier: high`
- [ ] Risk management system documented (CTRL-EUAI-001)
- [ ] Data governance procedures in place (CTRL-EUAI-002)
- [ ] Technical documentation complete (CTRL-EUAI-003)
- [ ] Audit logging enabled (CTRL-EUAI-004)
- [ ] User transparency measures (CTRL-EUAI-005)
- [ ] Human oversight capability (CTRL-EUAI-006)
- [ ] Accuracy testing passed (CTRL-EUAI-007)
- [ ] All controls verified
- [ ] Policy evaluation passes

### For Limited-Risk Systems

- [ ] System registered with `risk_tier: limited`
- [ ] User disclosure implemented
- [ ] Policy evaluation passes

## Annex III: High-Risk Categories

The EU AI Act defines high-risk AI in Annex III:

1. **Biometric identification** (remote, real-time)
2. **Critical infrastructure** management
3. **Education and vocational training** access
4. **Employment** decisions
5. **Essential services** access
6. **Law enforcement** applications
7. **Migration and border** management
8. **Justice and democracy** processes

### Mapping to Vorpal Tags

```python
HIGH_RISK_TAGS = [
    "biometric-identification",
    "critical-infrastructure",
    "education-access",
    "employment-decision",
    "essential-services",
    "law-enforcement",
    "migration-border",
    "justice-democracy"
]

# Tag your system appropriately
client.systems.update(
    system_id="...",
    tags=["employment-decision", "eu-ai-act-high-risk"]
)
```

## Evidence Generation

Generate EU AI Act compliance evidence:

```bash
vorpal-eval evidence \
  --system-id "..." \
  --regulation EU-AI-ACT \
  --format pdf \
  --output eu-ai-act-compliance.pdf
```

## References

- [EU AI Act Full Text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [European Commission AI Act Overview](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- [EU AI Act Timeline](https://artificialintelligenceact.eu/timeline/)
