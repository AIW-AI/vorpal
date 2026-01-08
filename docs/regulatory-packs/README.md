# Regulatory Policy Packs

Vorpal includes pre-built policy packs for common AI regulations and frameworks.

## Available Packs

| Pack | Regulation | Status |
|------|------------|--------|
| [EU AI Act](./eu-ai-act.md) | European Union AI Act | ✅ Available |
| [NYC LL 144](./nyc-ll144.md) | NYC Local Law 144 | ✅ Available |
| [NIST AI RMF](./nist-ai-rmf.md) | NIST AI Risk Management Framework | ✅ Available |
| [Colorado SB 205](./colorado-sb205.md) | Colorado AI Transparency Act | 🚧 Coming Soon |
| [OSFI E-23](./osfi-e23.md) | Canadian Model Risk Management | 🚧 Coming Soon |

## Using Policy Packs

### Install a Pack

```python
from vorpal import VorpalClient
from vorpal.packs import install_pack

client = VorpalClient(base_url="http://localhost:8000")

# Install EU AI Act pack
install_pack(client, "eu-ai-act")

# Install NYC LL 144 pack
install_pack(client, "nyc-ll144")
```

### Apply Pack to System

```python
# Tag system for automatic policy matching
client.systems.update(
    system_id="...",
    tags=["eu-ai-act-high-risk", "employment-decision"]
)
```

### View Pack Contents

```bash
# List controls from a pack
vorpal controls list --regulation EU-AI-ACT

# List policies from a pack
vorpal policies list --pack-name eu-ai-act-high-risk
```

## Pack Structure

Each pack contains:

1. **Controls** - Specific requirements to track
2. **Policies** - Rules enforcing those requirements
3. **Documentation** - Guidance for implementation

```
regulatory-packs/
├── eu-ai-act/
│   ├── controls.yaml      # Control definitions
│   ├── policies.yaml      # Policy rules
│   └── README.md          # Implementation guide
├── nyc-ll144/
│   ├── controls.yaml
│   ├── policies.yaml
│   └── README.md
└── ...
```

## Customizing Packs

### Override a Policy

```python
# Disable a built-in policy
client.policies.update(
    policy_id="eu-ai-act-high-risk-gates",
    enabled=False
)

# Create custom version
client.policies.create(
    name="my-org-high-risk-gates",
    description="Custom high-risk requirements",
    match_criteria={...},
    rules=[...]
)
```

### Add Organization Controls

```python
# Add your own controls alongside regulatory ones
client.controls.create(
    id="CTRL-ORG-001",
    name="Internal Security Review",
    category="security",
    requirement_text="All AI systems require security team sign-off"
)
```

## Compliance Mapping

### How Vorpal Maps to Regulations

| Requirement | Regulation | Vorpal Component |
|-------------|------------|------------------|
| AI System Inventory | EU AI Act Art 9 | `vorpal-core` registry |
| Risk Classification | EU AI Act Annex III | Risk tier + controls |
| Human Oversight | EU AI Act Art 14 | `vorpal-sentinel` HITL |
| Audit Trail | EU AI Act Art 12 | `vorpal-core` audit |
| Bias Testing | NYC LL 144 | `vorpal-eval` metrics |
| Transparency | EU AI Act Art 13 | Documentation fields |

## Creating Custom Packs

### Pack Definition Format

```yaml
# my-org-pack/controls.yaml
apiVersion: vorpal.dev/v1
kind: ControlPack
metadata:
  name: my-organization
  version: "1.0"

controls:
  - id: CTRL-ORG-001
    name: Security Review
    category: security
    mandatory: true

  - id: CTRL-ORG-002
    name: Privacy Impact Assessment
    category: privacy
    mandatory: true
```

```yaml
# my-org-pack/policies.yaml
apiVersion: vorpal.dev/v1
kind: PolicyPack
metadata:
  name: my-organization
  version: "1.0"

policies:
  - name: org-deployment-gates
    match_criteria:
      action: ["deploy"]
    rules:
      - name: security-review-required
        condition: system.controls.exists(c, c.id == "CTRL-ORG-001" && c.status == "verified")
        message: Security review required before deployment
        severity: error
```

### Install Custom Pack

```python
from vorpal.packs import load_pack_from_file

# Load from YAML files
pack = load_pack_from_file("./my-org-pack/")

# Install to Vorpal
pack.install(client)
```

## Evidence Generation

Vorpal can generate compliance evidence:

```bash
# Generate compliance report
vorpal-eval evidence \
  --system-id "..." \
  --regulation EU-AI-ACT \
  --format pdf \
  --output evidence.pdf
```

This produces:
- Control status summary
- Policy evaluation results
- Audit log excerpts
- Test results (if available)
