# Getting Started with Vorpal

This guide will help you get Vorpal up and running in your environment.

## Prerequisites

Before installing Vorpal, ensure you have:

- **Python 3.11+** - Required for all Vorpal components
- **PostgreSQL 15+** - Primary database for the registry and audit log
- **Redis 7+** (optional) - For rate limiting and caching
- **Docker** (optional) - For containerized deployment

## Installation Options

### Option 1: Docker Compose (Recommended for Getting Started)

The fastest way to try Vorpal:

```bash
# Clone the repository
git clone https://github.com/alice-in-wonderland-ai/vorpal.git
cd vorpal

# Start all services
docker compose up -d

# Verify it's running
curl http://localhost:8000/health
```

This starts:
- **vorpal-core** on port 8000
- **PostgreSQL** on port 5432
- **Redis** on port 6379

### Option 2: Python Package Installation

Install vorpal-core and the SDK:

```bash
# Install from PyPI (when published)
pip install vorpal-core vorpal-sdk

# Or install from source
git clone https://github.com/alice-in-wonderland-ai/vorpal.git
cd vorpal
pip install -e ./vorpal-core
pip install -e ./vorpal-sdk
```

### Option 3: Development Installation

For contributing or customizing:

```bash
# Clone and set up development environment
git clone https://github.com/alice-in-wonderland-ai/vorpal.git
cd vorpal

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with development dependencies
pip install -e "./vorpal-core[dev]"
pip install -e "./vorpal-sdk[dev]"

# Start dependencies
docker compose up -d postgres redis

# Run the server
vorpal serve --reload
```

## Configuration

Vorpal is configured via environment variables. Create a `.env` file:

```bash
cp .env.example .env
```

Key configuration options:

| Variable | Description | Default |
|----------|-------------|---------|
| `VORPAL_DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://vorpal:vorpal@localhost:5432/vorpal` |
| `VORPAL_REDIS_URL` | Redis connection string | `None` |
| `VORPAL_SECRET_KEY` | JWT signing key | `change-me-in-production` |
| `VORPAL_DEBUG` | Enable debug mode | `false` |
| `VORPAL_LOG_LEVEL` | Logging level | `INFO` |

See [Configuration Reference](./api-reference/configuration.md) for all options.

## Quick Start Tutorial

### 1. Register an AI System

Using the CLI:

```bash
vorpal systems create "customer-service-agent" \
  --type agent \
  --risk-tier limited \
  --description "Customer service chatbot"
```

Or using Python:

```python
from vorpal import VorpalClient, SystemType, RiskTier

client = VorpalClient(base_url="http://localhost:8000")

system = client.systems.create(
    name="customer-service-agent",
    type=SystemType.AGENT,
    risk_tier=RiskTier.LIMITED,
    description="Customer service chatbot",
    autonomy_level=3,
)

print(f"Created system: {system.id}")
```

### 2. Define a Governance Control

```python
control = client.controls.create(
    id="CTRL-BIAS-001",
    name="Bias Testing Required",
    category="bias",
    regulation="NYC-LL-144",
    requirement_text="Annual bias audit for employment decisions",
    mandatory=True,
)
```

### 3. Create a Policy

```python
from vorpal.types import PolicyRule, PolicySeverity

policy = client.policies.create(
    name="high-risk-deployment-gates",
    description="Require approvals for high-risk AI systems",
    match_criteria={
        "risk_tier": ["high"],
        "action": ["deploy"],
    },
    rules=[
        PolicyRule(
            name="require-bias-testing",
            condition="system.controls.exists(c, c.id == 'CTRL-BIAS-001' && c.status == 'verified')",
            message="High-risk systems require verified bias testing",
            severity=PolicySeverity.ERROR,
        ),
    ],
)
```

### 4. Evaluate Policies Before Deployment

```python
result = client.policies.evaluate(
    system_id=system.id,
    action="deploy",
)

if result.allowed:
    print("✓ Deployment approved")
    # Proceed with deployment
else:
    print("✗ Deployment blocked:")
    for failure in result.blocking_failures:
        print(f"  - {failure}")
```

## API Documentation

Access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## CLI Reference

The `vorpal` CLI provides commands for all operations:

```bash
# System management
vorpal systems list
vorpal systems get <system-id>
vorpal systems create <name> --type <type> --risk-tier <tier>

# Policy management
vorpal policies list
vorpal policies evaluate <system-id> <action>

# Audit log
vorpal audit list --system-id <id>
vorpal audit verify

# Server management
vorpal serve --port 8000
vorpal init-db
```

Run `vorpal --help` for full command reference.

## Next Steps

- [Architecture Overview](./architecture.md) - Understand Vorpal's design
- [API Reference](./api-reference/) - Complete API documentation
- [Tutorials](./tutorials/) - Step-by-step guides
- [Regulatory Packs](./regulatory-packs/) - Pre-built compliance policies

## Getting Help

- **Documentation**: https://vorpal.dev/docs
- **GitHub Issues**: https://github.com/alice-in-wonderland-ai/vorpal/issues
- **Discord**: https://discord.gg/vorpal
