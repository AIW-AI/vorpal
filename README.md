# Vorpal

> **The sword that slays complexity in AI governance**
>
> *"One, two! One, two! And through and through / The vorpal blade went snicker-snack!"*
> — Lewis Carroll, *Jabberwocky*

Part of the **Alice in Wonderland AI** open source ecosystem.

---

## Overview

Vorpal is a collection of open source libraries providing comprehensive AI governance, evaluation, and runtime enforcement. Unlike governance platforms that merely *document* policies, Vorpal *enforces* them at runtime—at the LLM gateway, in agent execution, and at tool invocation boundaries.

## Components

| Component | Description | Status |
|-----------|-------------|--------|
| **vorpal-core** | Registry, policy engine, audit trail | In Development |
| **vorpal-gateway** | LLM proxy with DLP, cost tracking, rate limiting | Planned |
| **vorpal-sentinel** | Agent runtime guardrails, HITL, kill switch | Planned |
| **vorpal-arbiter** | MCP/tool governance and permissions | Planned |
| **vorpal-eval** | Quality evaluation, bias testing, CI/CD gates | Planned |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           VORPAL STACK                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                       vorpal-core                            │    │
│  │                 (Registry + Policy + Audit)                  │    │
│  └───────────────────────────┬─────────────────────────────────┘    │
│                              │                                       │
│         ┌────────────────────┼────────────────────┐                 │
│         │                    │                    │                 │
│         ▼                    ▼                    ▼                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐             │
│  │vorpal-gateway│   │vorpal-sentinel│  │vorpal-arbiter│            │
│  │ LLM Proxy   │    │ Agent Guards │   │ MCP/Tool Gov │            │
│  └─────────────┘    └─────────────┘    └─────────────┘             │
│                              │                                       │
│                              ▼                                       │
│                      ┌─────────────┐                                │
│                      │ vorpal-eval │                                │
│                      │  Quality QA │                                │
│                      └─────────────┘                                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+ (optional, for rate limiting)

### Installation

```bash
# Install vorpal-core
pip install vorpal-core

# Or install from source
git clone https://github.com/alice-in-wonderland-ai/vorpal.git
cd vorpal
pip install -e ./vorpal-core
```

### Run with Docker

```bash
# Start all services
docker compose up -d

# Run migrations
docker compose exec vorpal-core alembic upgrade head

# Access the API
curl http://localhost:8000/health
```

### Basic Usage

```python
from vorpal.core import VorpalClient

# Initialize client
client = VorpalClient(base_url="http://localhost:8000")

# Register an AI system
system = client.systems.create(
    name="customer-service-agent",
    type="agent",
    risk_tier="limited",
    autonomy_level=3
)

# Evaluate a policy
result = client.policies.evaluate(
    system_id=system.id,
    action="deploy",
    context={"environment": "production"}
)

if result.allowed:
    print("Deployment approved")
else:
    print(f"Blocked: {result.reason}")
```

## Documentation

- [Getting Started](./docs/getting-started.md)
- [Architecture](./docs/architecture.md)
- [API Reference](./docs/api-reference/)
- [Tutorials](./docs/tutorials/)
- [Regulatory Packs](./docs/regulatory-packs/)

## Regulatory Coverage

Vorpal provides pre-built policy packs for:

| Regulation | Coverage |
|------------|----------|
| EU AI Act | Art 9, 12, 13, 14, 15, 17 |
| NYC Local Law 144 | Bias auditing, disclosure |
| Colorado SB 205 | Algorithmic discrimination |
| NIST AI RMF | GOVERN, MAP, MEASURE, MANAGE |

## Development

```bash
# Clone the repository
git clone https://github.com/alice-in-wonderland-ai/vorpal.git
cd vorpal

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install -e "./vorpal-core[dev]"
pip install -e "./vorpal-sdk[dev]"

# Run tests
pytest vorpal-core/tests

# Run linting
ruff check .
mypy vorpal-core/src
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

Apache License 2.0 - see [LICENSE](./LICENSE) for details.

## Related Projects

Part of the **Alice in Wonderland AI** ecosystem:

- **Alice** — Cognitive core with System 1/2 architecture
- **Cheshire** — Memory system (short-term, long-term, semantic)
- **Looking Glass** — Controllable chat UI
- **Mad Hatter** — Workflow orchestration
- **White Rabbit** — Timing and events
- **Caterpillar** — Transformation pipelines

---

*"Beware the Jabberwock, my son! / The jaws that bite, the claws that catch!"*
