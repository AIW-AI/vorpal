# Vorpal Architecture

This document describes the architecture of Vorpal, the AI governance platform.

## Design Principles

### 1. Runtime Enforcement Over Documentation

Unlike governance platforms that merely document policies, Vorpal enforces them at runtime:
- **LLM Gateway** blocks requests that violate DLP policies
- **Agent Sentinel** halts actions exceeding autonomy levels
- **MCP Arbiter** denies unauthorized tool invocations

### 2. Defense in Depth

Multiple enforcement points catch violations:
```
User Request → Gateway (DLP) → Agent (Sentinel) → Tools (Arbiter) → LLM (Gateway)
                   ↓               ↓                  ↓                ↓
              [Policy Check]  [Policy Check]    [Policy Check]   [Policy Check]
```

### 3. Audit Everything

Every action is recorded in a tamper-evident log:
- Hash-chained events prevent tampering
- Immutable storage for regulatory compliance
- Full context for incident investigation

### 4. Open Standards

- **MCP (Model Context Protocol)** for tool governance
- **OpenTelemetry** for observability
- **OPA/Rego** for policy language (planned)
- **OpenAPI** for API specifications

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              VORPAL STACK                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         vorpal-core                                  │    │
│  │                   (Registry + Policy + Audit)                        │    │
│  │                                                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │    │
│  │  │  Registry   │  │   Policy    │  │    Audit    │  │   Risk    │  │    │
│  │  │             │  │   Engine    │  │    Trail    │  │  Scoring  │  │    │
│  │  │ • Systems   │  │ • Rules     │  │ • Events    │  │ • Auto    │  │    │
│  │  │ • Controls  │  │ • Matching  │  │ • Hashing   │  │ • Tiers   │  │    │
│  │  │ • Evidence  │  │ • Evaluate  │  │ • Chain     │  │ • Review  │  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘  │    │
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
│  │ • Multi-LLM     │    │ • Pre-exec      │    │ • MCP proxy     │         │
│  │ • DLP/PII       │    │ • Autonomy      │    │ • Permissions   │         │
│  │ • Injection     │    │ • Kill switch   │    │ • Validation    │         │
│  │ • Rate limit    │    │ • HITL          │    │ • Budget        │         │
│  │ • Cost track    │    │ • Circuit break │    │ • Rate limit    │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│                                  │                                          │
│                                  ▼                                          │
│                        ┌─────────────────────┐                              │
│                        │    vorpal-eval      │                              │
│                        │                     │                              │
│                        │  Quality Assurance  │                              │
│                        │                     │                              │
│                        │ • Test suites       │                              │
│                        │ • LLM-as-judge      │                              │
│                        │ • Bias detection    │                              │
│                        │ • Regression        │                              │
│                        │ • Evidence export   │                              │
│                        └─────────────────────┘                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### vorpal-core

The central governance hub that all other components connect to.

**Responsibilities:**
- AI system registry and inventory
- Policy storage and evaluation
- Audit event collection and verification
- Risk scoring and classification
- Control tracking and evidence management

**Technology:**
- Python 3.11+ with FastAPI
- PostgreSQL for persistent storage
- SQLAlchemy async ORM
- Pydantic for validation

**Key Modules:**

| Module | Purpose |
|--------|---------|
| `models/system.py` | AI system registry model |
| `models/control.py` | Governance controls |
| `models/policy.py` | Policy definitions |
| `models/audit.py` | Audit events with hash chain |
| `api/routes/` | REST API endpoints |
| `cli/` | Command-line interface |

### vorpal-gateway (Planned)

LLM proxy providing security and observability.

**Capabilities:**
- Route requests to multiple LLM providers
- DLP scanning with PII detection/redaction
- Prompt injection detection
- Rate limiting per team/system
- Cost tracking and attribution
- Semantic caching (planned)

**Flow:**
```
Client → Auth → Policy → DLP → Rate Limit → Route → LLM → Filter → Audit
```

### vorpal-sentinel (Planned)

Runtime guardrails for AI agents.

**Capabilities:**
- Autonomy level enforcement (L1-L5)
- Pre-execution action checking
- Human-in-the-loop workflows
- Emergency kill switch
- Circuit breaker patterns
- Session lifecycle management

**Autonomy Levels:**
```
L1: INFORMATIONAL  - Read-only queries
L2: CONSTRAINED    - Writes to safe zones only
L3: SUPERVISED     - External APIs, configurable HITL
L4: DELEGATED      - Most tools, HITL for irreversible
L5: AUTONOMOUS     - Full operation within budget
```

### vorpal-arbiter (Planned)

MCP proxy for tool governance.

**Capabilities:**
- Intercept all MCP tool calls
- Permission-based access control
- Parameter validation and sanitization
- Rate limiting per tool
- Budget tracking for expensive operations
- Audit logging

**Permission Model:**
```yaml
tools:
  - server: filesystem
    tool: read_file
    action: allow
    params:
      path:
        pattern: "^/workspace/.*"
        deny_pattern: ".*\\.(env|key)$"
```

### vorpal-eval (Planned)

Quality assurance and testing framework.

**Capabilities:**
- Test suite execution
- LLM-as-judge evaluation
- Bias metric calculation
- Regression detection
- CI/CD integration
- Evidence export for compliance

## Data Model

### Core Entities

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    AI System    │────<│ System Control  │>────│     Control     │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id              │     │ system_id       │     │ id              │
│ name            │     │ control_id      │     │ name            │
│ type            │     │ status          │     │ category        │
│ status          │     │ evidence_req    │     │ regulation      │
│ risk_tier       │     │ notes           │     │ requirement     │
│ autonomy_level  │     └─────────────────┘     └─────────────────┘
│ owner_id        │
│ team_id         │
│ metadata        │
└─────────────────┘
        │
        │ audits
        ▼
┌─────────────────┐     ┌─────────────────┐
│  Audit Event    │     │     Policy      │
├─────────────────┤     ├─────────────────┤
│ id              │     │ id              │
│ system_id       │     │ name            │
│ event_type      │     │ match_criteria  │
│ actor_id        │     │ rules[]         │
│ action          │     │ enabled         │
│ details         │     │ regulation      │
│ previous_hash   │     └─────────────────┘
│ event_hash      │
│ timestamp       │
└─────────────────┘
```

### Audit Chain Integrity

Each audit event contains:
1. SHA-256 hash of the previous event
2. SHA-256 hash of its own content

This creates a tamper-evident chain:
```
Event 1          Event 2          Event 3
┌──────────┐     ┌──────────┐     ┌──────────┐
│ hash: A  │ ←── │ prev: A  │ ←── │ prev: B  │
│ prev: ∅  │     │ hash: B  │     │ hash: C  │
└──────────┘     └──────────┘     └──────────┘
```

Any modification to Event 1 or 2 breaks the chain at Event 3.

## Policy Evaluation

### Match Criteria

Policies define when they should be evaluated:

```yaml
match_criteria:
  risk_tier: ["high", "limited"]  # System risk tier
  action: ["deploy", "update"]     # Action being performed
  type: ["agent", "model"]         # System type
  tags:
    contains: ["production"]       # System tags
```

### Rule Evaluation

Rules use CEL-like expressions:

```yaml
rules:
  - name: require-bias-testing
    condition: |
      system.controls.exists(c,
        c.id == "CTRL-BIAS-001" &&
        c.status == "verified"
      )
    message: "High-risk systems require verified bias testing"
    severity: error
```

### Evaluation Flow

```
1. Receive evaluate request (system_id, action, context)
2. Load system from registry
3. Find all enabled policies
4. Filter to matching policies (by criteria)
5. For each matching policy:
   a. Evaluate each rule condition
   b. Collect results and failures
6. Aggregate results:
   - allowed = no ERROR-severity failures
   - blocking_failures = ERROR messages
   - warnings = WARNING messages
7. Log evaluation to audit trail
8. Return result
```

## Security Model

### Authentication

| Method | Use Case |
|--------|----------|
| API Keys | Programmatic access, CI/CD |
| JWT | User sessions, SSO integration |
| mTLS | Service-to-service (planned) |

### Authorization

Role-based access control (RBAC):

| Role | Permissions |
|------|-------------|
| `viewer` | Read systems, controls, policies |
| `editor` | Create/update systems, controls |
| `admin` | All operations, user management |
| `compliance_officer` | Approve high-risk deployments |

### Data Protection

- All secrets encrypted at rest (AES-256)
- TLS 1.3 required for transit
- PII detection and redaction in gateway
- Audit logs tamper-evident

## Deployment Architecture

### Single Node (Development)

```
┌─────────────────────────────────────────┐
│              Docker Host                 │
│  ┌─────────────┐  ┌─────────────┐       │
│  │ vorpal-core │  │  PostgreSQL │       │
│  │   :8000     │  │    :5432    │       │
│  └─────────────┘  └─────────────┘       │
│  ┌─────────────┐                        │
│  │    Redis    │                        │
│  │    :6379    │                        │
│  └─────────────┘                        │
└─────────────────────────────────────────┘
```

### Production (Kubernetes)

```
┌─────────────────────────────────────────────────────────────────┐
│                        Kubernetes Cluster                        │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Ingress    │  │   Ingress    │  │   Ingress    │          │
│  │  /api/*      │  │  /gateway/*  │  │  /dashboard  │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                   │
│         ▼                 ▼                 ▼                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ vorpal-core  │  │vorpal-gateway│  │  dashboard   │          │
│  │  (3 replicas)│  │  (3 replicas)│  │  (2 replicas)│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                 │                                     │
│         └────────┬────────┘                                     │
│                  ▼                                              │
│  ┌──────────────────────────────────────────────────────┐      │
│  │               PostgreSQL (HA)  │  Redis Cluster      │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Integration Points

### OpenTelemetry

All components emit traces and metrics:

```python
# Automatic instrumentation
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
FastAPIInstrumentor.instrument_app(app)

# Custom spans
with tracer.start_as_current_span("policy_evaluation"):
    result = evaluate_policies(system_id, action)
```

### Webhooks (Planned)

External systems can subscribe to events:

```yaml
webhooks:
  - url: https://slack.com/webhook/...
    events: ["system.deployed", "policy.blocked"]

  - url: https://pagerduty.com/...
    events: ["sentinel.kill_switch"]
```

### MCP Integration

Arbiter acts as MCP proxy:

```
Agent ──MCP──> Arbiter ──MCP──> MCP Server
                 │
                 ├── Check permissions
                 ├── Validate params
                 ├── Rate limit
                 └── Audit log
```

## Scalability Considerations

### Horizontal Scaling

- **vorpal-core**: Stateless, scale with replicas
- **PostgreSQL**: Use read replicas for queries
- **Redis**: Cluster mode for rate limiting

### Performance Optimizations

- Policy evaluation cached by (system_id, action) hash
- Audit writes batched and async
- Database connection pooling
- Prepared statements for hot paths

### Limits

| Resource | Default Limit |
|----------|---------------|
| API requests/min | 1000 per IP |
| Systems per org | 10,000 |
| Policies per org | 1,000 |
| Audit retention | 7 years |

## Future Architecture

### Planned Components

1. **vorpal-gateway** - LLM proxy (Q1 2026)
2. **vorpal-sentinel** - Agent guardrails (Q2 2026)
3. **vorpal-arbiter** - MCP governance (Q2 2026)
4. **vorpal-eval** - Quality testing (Q3 2026)
5. **vorpal-dashboard** - Web UI (Q4 2026)

### Integration Roadmap

- OPA/Rego policy language support
- Kubernetes operator for CRD-based policies
- GitOps workflow for policy-as-code
- Terraform provider for infrastructure integration
