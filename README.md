# Vorpal

> **The sword that slays complexity in AI governance**
>
> *"One, two! One, two! And through and through / The vorpal blade went snicker-snack!"*
> — Lewis Carroll, *Jabberwocky*

[![CI](https://github.com/alice-in-wonderland-ai/vorpal/actions/workflows/ci.yml/badge.svg)](https://github.com/alice-in-wonderland-ai/vorpal/actions)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)

Part of the **Alice in Wonderland AI** open source ecosystem.

---

## Why Vorpal?

AI governance today faces a critical gap:

| Approach | Problem |
|----------|---------|
| **Enterprise Platforms** (Credo.ai, IBM watsonx) | $200K+/year, complex, often just documentation |
| **DIY with OSS** (MLflow + Fairlearn + custom) | Fragmented, incomplete, high maintenance |

**Vorpal fills the gap**: Production-grade governance that's free, complete, and actually *enforces* policies at runtime.

### Key Differentiators

- **Runtime Enforcement**: Policies are enforced at the LLM gateway, in agent execution, and at tool invocation—not just documented
- **Complete Stack**: Registry, policies, audit, evaluation, and enforcement in one coherent system
- **Regulatory Ready**: Pre-built policy packs for EU AI Act, NYC LL 144, NIST AI RMF
- **MCP-First**: First governance layer for Model Context Protocol tool access
- **Open Source**: Apache 2.0, self-hosted, no vendor lock-in

---

## Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              VORPAL STACK                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         vorpal-core                                  │    │
│  │                   (Registry + Policy + Audit)                        │    │
│  │                                                                      │    │
│  │  • AI System Registry    • Policy Engine      • Audit Trail          │    │
│  │  • Control Tracking      • Risk Scoring       • Evidence Export      │    │
│  └───────────────────────────────┬─────────────────────────────────────┘    │
│                                  │                                          │
│         ┌────────────────────────┼────────────────────────┐                 │
│         │                        │                        │                 │
│         ▼                        ▼                        ▼                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │ vorpal-gateway  │    │ vorpal-sentinel │    │ vorpal-arbiter  │         │
│  │                 │    │                 │    │                 │         │
│  │   LLM Proxy &   │    │  Agent Runtime  │    │   MCP & Tool    │         │
│  │    Security     │    │   Guardrails    │    │   Governance    │         │
│  │                 │    │                 │    │                 │         │
│  │ • Multi-LLM     │    │ • Autonomy L1-5 │    │ • MCP Proxy     │         │
│  │ • DLP/PII       │    │ • Kill Switch   │    │ • Permissions   │         │
│  │ • Cost Track    │    │ • HITL          │    │ • Rate Limits   │         │
│  │ • Rate Limit    │    │ • Circuit Break │    │ • Budget Caps   │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│                                  │                                          │
│                                  ▼                                          │
│                        ┌─────────────────────┐                              │
│                        │    vorpal-eval      │                              │
│                        │  Quality Assurance  │                              │
│                        │                     │                              │
│                        │ • Test Suites       │                              │
│                        │ • LLM-as-Judge      │                              │
│                        │ • Bias Detection    │                              │
│                        │ • CI/CD Gates       │                              │
│                        └─────────────────────┘                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Component | Description | Status |
|-----------|-------------|--------|
| **vorpal-core** | AI registry, policy engine, tamper-evident audit | ✅ Available |
| **vorpal-sdk** | Python client SDK | ✅ Available |
| **vorpal-gateway** | LLM proxy with DLP, cost tracking, rate limiting | 🚧 Q1 2026 |
| **vorpal-sentinel** | Agent guardrails, HITL, kill switch | 🚧 Q2 2026 |
| **vorpal-arbiter** | MCP/tool governance and permissions | 🚧 Q2 2026 |
| **vorpal-eval** | Quality evaluation, bias testing, CI/CD gates | 🚧 Q3 2026 |

---

## Quick Start

### Option 1: Docker (Fastest)

```bash
# Clone and start
git clone https://github.com/alice-in-wonderland-ai/vorpal.git
cd vorpal
docker compose up -d

# Verify it's running
curl http://localhost:8000/health
# {"status": "healthy"}

# View API docs
open http://localhost:8000/docs
```

### Option 2: Python Package

```bash
# Install packages
pip install vorpal-core vorpal-sdk

# Or from source
pip install -e ./vorpal-core -e ./vorpal-sdk

# Start dependencies
docker compose up -d postgres redis

# Run server
vorpal serve
```

### Basic Usage

```python
from vorpal import VorpalClient, SystemType, RiskTier

# Connect to Vorpal
client = VorpalClient(base_url="http://localhost:8000")

# 1. Register an AI system
system = client.systems.create(
    name="customer-service-agent",
    type=SystemType.AGENT,
    risk_tier=RiskTier.LIMITED,
    description="AI agent for customer inquiries",
    autonomy_level=3,
    tags=["production", "customer-facing"]
)
print(f"Registered: {system.id}")

# 2. Check if deployment is allowed
result = client.policies.evaluate(
    system_id=system.id,
    action="deploy"
)

if result.allowed:
    print("✓ Deployment approved")
else:
    print("✗ Deployment blocked:")
    for failure in result.blocking_failures:
        print(f"  - {failure}")
```

### CLI Usage

```bash
# List systems
vorpal systems list

# Register a system
vorpal systems create "my-model" --type model --risk-tier high

# Evaluate deployment
vorpal policies evaluate <system-id> deploy

# View audit log
vorpal audit list --system-id <id>

# Verify audit integrity
vorpal audit verify
```

---

## Core Features

### AI System Registry

Track all AI components in your organization:

```python
# Register different system types
model = client.systems.create(
    name="fraud-detection-v2",
    type=SystemType.MODEL,
    risk_tier=RiskTier.HIGH,
    metadata={
        "framework": "scikit-learn",
        "accuracy": 0.95,
        "training_date": "2026-01-01"
    }
)

agent = client.systems.create(
    name="research-assistant",
    type=SystemType.AGENT,
    risk_tier=RiskTier.LIMITED,
    autonomy_level=3,  # L3: Supervised
    metadata={"model": "gpt-4o", "hitl_enabled": True}
)
```

### Governance Controls

Define and track compliance requirements:

```python
# Create controls from regulations
client.controls.create(
    id="CTRL-BIAS-001",
    name="Annual Bias Audit",
    category="bias",
    regulation="NYC-LL-144",
    requirement_text="Employment AI requires annual bias audit",
    mandatory=True
)

# Assign to systems
client.systems.assign_control(system.id, "CTRL-BIAS-001")

# Track implementation status
client.systems.update_control(
    system.id,
    "CTRL-BIAS-001",
    status="verified",
    notes="Audit completed by external firm"
)
```

### Policy Enforcement

Define policies that are evaluated at runtime:

```python
# Create a deployment policy
client.policies.create(
    name="high-risk-deployment-gates",
    match_criteria={
        "risk_tier": ["high"],
        "action": ["deploy"]
    },
    rules=[
        {
            "name": "require-bias-testing",
            "condition": "system.controls.exists(c, c.id == 'CTRL-BIAS-001' && c.status == 'verified')",
            "message": "High-risk systems require verified bias testing",
            "severity": "error"  # Blocks deployment
        },
        {
            "name": "recommend-hitl",
            "condition": "system.metadata.hitl_enabled == true",
            "message": "Consider enabling HITL for high-risk systems",
            "severity": "warning"  # Warns but allows
        }
    ]
)
```

### Tamper-Evident Audit Log

Every action is recorded with hash-chain integrity:

```python
# Query audit events
events, meta = client.audit.list(
    system_id=system.id,
    from_date="2026-01-01"
)

for event in events:
    print(f"{event.timestamp}: {event.action} by {event.actor_name}")

# Verify chain integrity
verification = client.audit.verify_chain()
if verification.verified:
    print(f"✓ {verification.total_events} events verified")
else:
    print(f"✗ Chain compromised at event {verification.first_invalid_event_id}")
```

---

## Regulatory Coverage

### Pre-built Policy Packs

| Regulation | Status | Controls | Policies |
|------------|--------|----------|----------|
| [EU AI Act](./docs/regulatory-packs/eu-ai-act.md) | ✅ | 7 | 3 |
| [NYC Local Law 144](./docs/regulatory-packs/nyc-ll144.md) | ✅ | 3 | 2 |
| [NIST AI RMF](./docs/regulatory-packs/nist-ai-rmf.md) | ✅ | 4 | 2 |
| Colorado SB 205 | 🚧 | - | - |
| OSFI E-23 | 🚧 | - | - |

### Compliance Mapping

| Requirement | Regulation | Vorpal Component |
|-------------|------------|------------------|
| AI System Inventory | EU AI Act Art 9 | vorpal-core registry |
| Risk Classification | EU AI Act Annex III | Risk tiers + controls |
| Human Oversight | EU AI Act Art 14 | vorpal-sentinel HITL |
| Audit Trail | EU AI Act Art 12 | vorpal-core audit |
| Performance Monitoring | EU AI Act Art 9(7) | vorpal-eval |
| Bias Testing | NYC LL 144 | vorpal-eval metrics |
| Data Protection | GDPR Art 22, 35 | vorpal-gateway DLP |

---

## Documentation

### Getting Started
- [Installation & Setup](./docs/getting-started.md)
- [Configuration Reference](./docs/api-reference/configuration.md)

### Concepts
- [Architecture Overview](./docs/architecture.md)
- [Risk Tiers & Autonomy Levels](./docs/architecture.md#autonomy-levels)

### API Reference
- [Systems API](./docs/api-reference/systems.md)
- [Controls API](./docs/api-reference/controls.md)
- [Policies API](./docs/api-reference/policies.md)
- [Audit API](./docs/api-reference/audit.md)

### Tutorials
- [Registering Your First AI System](./docs/tutorials/01-registering-ai-system.md)
- [Creating Governance Controls](./docs/tutorials/02-creating-controls.md)
- [Writing Policies](./docs/tutorials/03-writing-policies.md)

### Regulatory Guides
- [EU AI Act Compliance](./docs/regulatory-packs/eu-ai-act.md)
- [NYC Local Law 144](./docs/regulatory-packs/nyc-ll144.md)

### Development
- [Development Guide](./docs/development/)
- [Contributing](./CONTRIBUTING.md)

---

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/alice-in-wonderland-ai/vorpal.git
cd vorpal

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install with dev dependencies
pip install -e "./vorpal-core[dev]" -e "./vorpal-sdk[dev]"

# Start dependencies
docker compose up -d postgres redis

# Run tests
pytest

# Run linting
ruff check .
mypy vorpal-core/src vorpal-sdk/src
```

### Project Structure

```
vorpal/
├── vorpal-core/           # Main API and policy engine
│   ├── src/vorpal/core/
│   │   ├── api/           # FastAPI routes
│   │   ├── models/        # SQLAlchemy models
│   │   ├── cli/           # CLI commands
│   │   └── ...
│   └── tests/
├── vorpal-sdk/            # Python client SDK
├── vorpal-gateway/        # LLM proxy (planned)
├── vorpal-sentinel/       # Agent guardrails (planned)
├── vorpal-arbiter/        # MCP governance (planned)
├── vorpal-eval/           # Quality testing (planned)
├── docs/                  # Documentation
└── charts/                # Helm charts
```

---

## Roadmap

### Phase 1: Foundation (Current)
- ✅ vorpal-core: Registry, policies, audit
- ✅ vorpal-sdk: Python client
- ✅ Docker deployment
- ✅ Basic regulatory packs

### Phase 2: Enforcement (Q1-Q2 2026)
- 🚧 vorpal-gateway: LLM proxy with DLP
- 🚧 vorpal-sentinel: Agent guardrails
- 🚧 vorpal-arbiter: MCP tool governance

### Phase 3: Evaluation (Q3-Q4 2026)
- 📋 vorpal-eval: Quality testing
- 📋 vorpal-dashboard: Web UI
- 📋 Helm charts for Kubernetes
- 📋 v1.0 release

---

## Community

- **GitHub Issues**: [Bug reports & features](https://github.com/alice-in-wonderland-ai/vorpal/issues)
- **GitHub Discussions**: [Questions & ideas](https://github.com/alice-in-wonderland-ai/vorpal/discussions)
- **Discord**: [Join #vorpal](https://discord.gg/vorpal)

---

## Related Projects

Part of the **Alice in Wonderland AI** ecosystem:

| Project | Description |
|---------|-------------|
| **Alice** | Cognitive core with System 1/2 architecture |
| **Cheshire** | Memory system (short-term, long-term, semantic) |
| **Vorpal** | AI governance and compliance (this project) |
| **Looking Glass** | Controllable chat UI |
| **Mad Hatter** | Workflow orchestration |
| **White Rabbit** | Timing and events |
| **Caterpillar** | Transformation pipelines |

---

## License

Apache License 2.0 - see [LICENSE](./LICENSE) for details.

---

*"Beware the Jabberwock, my son! / The jaws that bite, the claws that catch!"*

*Vorpal defeats the incomprehensible monster of AI governance—with surgical precision.*
