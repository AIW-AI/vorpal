# Vorpal Implementation Plan

> **The sword that slays complexity in AI governance**
>
> Part of the **Alice in Wonderland AI** open source ecosystem

---

## Executive Summary

Vorpal is a collection of open source libraries providing comprehensive AI governance, evaluation, and runtime enforcement. Named after the blade from Lewis Carroll's *Jabberwocky* that defeats the incomprehensible monster ("*The vorpal blade went snicker-snack!*"), Vorpal cuts through the complexity of enterprise AI governance with surgical precision.

**Core Thesis**: AI governance today is either expensive (enterprise platforms like Credo.ai at $200K+/year) or incomplete (fragmented open source tools). Vorpal provides the missing middle: production-grade governance that any organization can deploy and operate.

**Key Differentiator**: Unlike governance platforms that merely *document* policies, Vorpal *enforces* them at runtime—at the LLM gateway, in agent execution, and at tool invocation boundaries.

---

## The Alice in Wonderland AI Ecosystem

### Vision

Build a complete, open source AI agent infrastructure stack where every component works independently but integrates seamlessly—like characters in Wonderland, each distinct yet part of a coherent world.

### Ecosystem Components

```
┌────────────────────────────────────────────────────────────────────────────┐
│                      ALICE IN WONDERLAND AI                                │
│                  "Curiouser and Curiouser"                                 │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │    ALICE     │  │   CHESHIRE   │  │    VORPAL    │  │  MAD HATTER  │   │
│  │              │  │              │  │              │  │              │   │
│  │ Chat & Agent │  │    Memory    │  │  Governance  │  │   Workflow   │   │
│  │  Interface   │  │    System    │  │ & Compliance │  │ Orchestrator │   │
│  │              │  │              │  │              │  │              │   │
│  │ • MCP-native │  │ • Short-term │  │ • Registry   │  │ • Task queue │   │
│  │ • Multi-modal│  │ • Long-term  │  │ • Policies   │  │ • Scheduling │   │
│  │ • Streaming  │  │ • Semantic   │  │ • Eval       │  │ • Triggers   │   │
│  │ • Extensible │  │ • Contextual │  │ • Enforce    │  │ • Webhooks   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                     │
│  │ LOOKING GLASS│  │  WHITE RABBIT│  │  CATERPILLAR │                     │
│  │              │  │              │  │              │                     │
│  │  Controllable│  │   Timing &   │  │ Transformation│                    │
│  │   Chat UI    │  │   Events     │  │   Pipeline   │                     │
│  │              │  │              │  │              │                     │
│  │ • MCP control│  │ • Cron/Timer │  │ • ETL        │                     │
│  │ • Adaptive   │  │ • Debounce   │  │ • Enrichment │                     │
│  │ • Expressive │  │ • Rate limit │  │ • Format     │                     │
│  │ • Dashboard  │  │ • Event bus  │  │ • Embedding  │                     │
│  └──────────────┘  └──────────────┘  └──────────────┘                     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Component Naming Philosophy

| Component | Reference | Metaphor |
|-----------|-----------|----------|
| **Alice** | The protagonist | The cognitive core—System 1/2 architecture |
| **Cheshire** | Cheshire Cat | Appears and disappears; knows everything; persistent yet ethereal (memory) |
| **Vorpal** | Vorpal sword | Cuts through complexity; defeats the incomprehensible (governance) |
| **Looking Glass** | Through the Looking-Glass | The window into Wonderland; controllable chat UI |
| **Mad Hatter** | Mad Hatter's tea party | Orchestrates chaos into order; timing and coordination |
| **White Rabbit** | "I'm late!" | Time-sensitive; events and scheduling |
| **Caterpillar** | "Who are you?" | Transformation; processing pipelines |

### Integration Points

Every component communicates through:
1. **MCP (Model Context Protocol)** — Tool invocation and context sharing
2. **OpenTelemetry** — Distributed tracing and metrics
3. **Shared auth** — SSO/JWT across the stack
4. **Common config format** — YAML/TOML with validated schemas

---

## Vorpal: Detailed Architecture

### The Five Libraries

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              VORPAL STACK                                   │
│                   "One, two! One, two! And through and through"             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                       vorpal-core                                    │   │
│  │                 (Registry + Policy + Audit)                          │   │
│  │  • AI System Registry — inventory of all AI components               │   │
│  │  • Policy Engine — OPA/Rego-based rule evaluation                    │   │
│  │  • Audit Trail — immutable, hash-chained event log                   │   │
│  │  • Risk Scoring — automated risk classification                      │   │
│  │  • Regulatory Packs — pre-built policies for EU AI Act, NIST, etc.   │   │
│  └─────────────────────────────────┬───────────────────────────────────┘   │
│                                    │                                        │
│           ┌────────────────────────┼────────────────────────┐              │
│           │                        │                        │              │
│           ▼                        ▼                        ▼              │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │  vorpal-gateway │    │ vorpal-sentinel │    │ vorpal-arbiter  │        │
│  │                 │    │                 │    │                 │        │
│  │  LLM Proxy &    │    │ Agent Runtime   │    │ MCP & Tool      │        │
│  │  Security       │    │ Guardrails      │    │ Governance      │        │
│  │                 │    │                 │    │                 │        │
│  │ • Multi-LLM     │    │ • Pre-exec check│    │ • MCP proxy     │        │
│  │ • DLP/PII       │    │ • Autonomy lvl  │    │ • Permission    │        │
│  │ • Injection     │    │ • Kill switch   │    │ • Param valid   │        │
│  │ • Rate limit    │    │ • HITL          │    │ • Budget        │        │
│  │ • Cost track    │    │ • Circuit break │    │ • Rate limit    │        │
│  │ • Semantic cache│    │ • Audit         │    │ • Audit         │        │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │
│                                    │                                        │
│                                    ▼                                        │
│                        ┌─────────────────────┐                             │
│                        │    vorpal-eval      │                             │
│                        │                     │                             │
│                        │  Quality Assurance  │                             │
│                        │                     │                             │
│                        │ • Test suites       │                             │
│                        │ • LLM-as-judge      │                             │
│                        │ • Bias detection    │                             │
│                        │ • Regression        │                             │
│                        │ • Evidence export   │                             │
│                        └─────────────────────┘                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Why "Vorpal"?

From *Jabberwocky*:

> *He took his vorpal sword in hand;*
> *Long time the manxome foe he sought—*
> *So rested he by the Tumtum tree*
> *And stood awhile in thought.*
>
> *And, as in uffish thought he stood,*
> *The Jabberwock, with eyes of flame,*
> *Came whiffling through the tulgey wood,*
> *And burbled as it came!*
>
> *One, two! One, two! And through and through*
> *The vorpal blade went snicker-snack!*
> *He left it dead, and with its head*
> *He went galumphing back.*

**The Jabberwock = AI governance complexity**
- Incomprehensible ("burbled")
- Threatening ("eyes of flame")
- Lurking in confusion ("tulgey wood")
- Requires decisive action to defeat

**The Vorpal sword = our stack**
- Cuts cleanly through confusion
- Swift and precise ("snicker-snack")
- Returns order from chaos ("galumphing back")

---

## Market Analysis

### The Governance Gap

```
                          COST
                           │
                     HIGH  │  ┌─────────────────────┐
                           │  │   ENTERPRISE        │
                           │  │   Credo.ai          │
                           │  │   IBM watsonx       │
                           │  │   OneTrust AI       │
                           │  │                     │
                           │  │   $200K-500K/year   │
                           │  └─────────────────────┘
                           │
                           │            ┌─────────────────────────┐
                           │            │    VORPAL TARGET        │
                           │            │                         │
                    MID    │            │    Complete governance  │
                           │            │    Self-hosted          │
                           │            │    $0 (OSS)             │
                           │            └─────────────────────────┘
                           │
                           │  ┌─────────────────────┐
                     LOW   │  │   FRAGMENTED OSS    │
                           │  │                     │
                           │  │   MLflow + Ragas +  │
                           │  │   Fairlearn + ???   │
                           │  │                     │
                           │  │   Incomplete        │
                           │  └─────────────────────┘
                           │
                           └────────────────────────────────────────
                                  INCOMPLETE ◄────► COMPLETE
                                          COVERAGE
```

### Competitive Landscape

| Vendor | Strength | Weakness | Price |
|--------|----------|----------|-------|
| **Credo.ai** | Comprehensive, regulatory focus | No runtime enforcement | $200K+ |
| **IBM watsonx.governance** | Enterprise integration | IBM-centric, complex | $300K+ |
| **Holistic AI** | Bias auditing | Limited scope | $150K+ |
| **ModelOp** | MLOps integration | Dated architecture | $200K+ |
| **Arize Phoenix** | Evaluation/observability | No governance | OSS + Enterprise |
| **LangSmith** | LangChain ecosystem | Vendor lock-in | $0-400/mo |
| **Portkey** | LLM gateway | No broader governance | $0-500/mo |

### Vorpal Positioning

**Not competing with**: Enterprise governance platforms (different buyer, different sale cycle)

**Competing with**: DIY governance stacks cobbled from multiple tools

**Target users**:
- Startups building AI products who need governance from day one
- Mid-market companies who can't justify $200K+ platforms
- Regulated industries (financial services, healthcare) who need compliance but have limited budgets
- Open source projects that need to demonstrate governance

---

## Regulatory Motivation

### Why Now?

| Regulation | Deadline | Impact |
|------------|----------|--------|
| **EU AI Act** | Aug 2026 | All high-risk AI systems need registration, oversight, documentation |
| **Colorado SB 205** | June 2026 | Algorithmic discrimination disclosure for "consequential decisions" |
| **NYC Local Law 144** | Active | Annual bias audits for automated employment decisions |
| **OSFI E-23** | May 2027 | Model risk management for Canadian financial institutions |

### What Regulators Require → What Vorpal Provides

| Requirement | Regulation | Vorpal Component |
|-------------|------------|------------------|
| AI System Inventory | EU AI Act Art 9 | vorpal-core registry |
| Risk Classification | EU AI Act Annex III | vorpal-core risk scoring |
| Human Oversight | EU AI Act Art 14 | vorpal-sentinel HITL |
| Audit Trail | EU AI Act Art 12 | vorpal-core audit log |
| Performance Monitoring | EU AI Act Art 9(7) | vorpal-eval continuous |
| Data Protection | GDPR Art 22, 35 | vorpal-gateway DLP |
| Bias Testing | NYC LL 144, Colorado | vorpal-eval bias metrics |
| Vendor Assessment | EU AI Act deployer obligations | vorpal-core vendor registry |

---

## Implementation Plan

### Overview Timeline

```
2026           Q1                    Q2                    Q3                    Q4
─────────────────────────────────────────────────────────────────────────────────────
             │ PHASE 1              │ PHASE 2             │ PHASE 3              │
             │ Foundation           │ Enforcement         │ Evaluation           │
             │                      │                     │                      │
Week 1-4     │ ┌──────────────────┐ │                     │                      │
             │ │ vorpal-core v0.1 │ │                     │                      │
             │ │ • Data model     │ │                     │                      │
             │ │ • Basic API      │ │                     │                      │
             │ │ • YAML policies  │ │                     │                      │
             │ └──────────────────┘ │                     │                      │
             │                      │                     │                      │
Week 5-8     │ ┌──────────────────┐ │                     │                      │
             │ │ vorpal-gateway   │ │                     │                      │
             │ │ v0.1             │ │                     │                      │
             │ │ • LLM proxy      │ │                     │                      │
             │ │ • Cost tracking  │ │                     │                      │
             │ │ • Basic DLP      │ │                     │                      │
             │ └──────────────────┘ │                     │                      │
             │                      │                     │                      │
Week 9-12    │                      │ ┌──────────────────┐│                      │
             │                      │ │ vorpal-sentinel  ││                      │
             │                      │ │ v0.1             ││                      │
             │                      │ │ • LangChain      ││                      │
             │                      │ │ • Kill switch    ││                      │
             │                      │ │ • HITL           ││                      │
             │                      │ └──────────────────┘│                      │
             │                      │                     │                      │
Week 13-16   │                      │ ┌──────────────────┐│                      │
             │                      │ │ vorpal-arbiter   ││                      │
             │                      │ │ v0.1             ││                      │
             │                      │ │ • MCP proxy      ││                      │
             │                      │ │ • Permissions    ││                      │
             │                      │ │ • Rate limit     ││                      │
             │                      │ └──────────────────┘│                      │
             │                      │                     │                      │
Week 17-20   │                      │                     │ ┌──────────────────┐ │
             │                      │                     │ │ vorpal-eval v0.1 │ │
             │                      │                     │ │ • Test runner    │ │
             │                      │                     │ │ • LLM judge      │ │
             │                      │                     │ │ • Bias metrics   │ │
             │                      │                     │ └──────────────────┘ │
             │                      │                     │                      │
Week 21-24   │                      │                     │ ┌──────────────────┐ │
             │                      │                     │ │ Integration &    │ │
             │                      │                     │ │ Polish           │ │
             │                      │                     │ │ • Dashboard      │ │
             │                      │                     │ │ • Helm charts    │ │
             │                      │                     │ │ • Docs           │ │
             │                      │                     │ └──────────────────┘ │
─────────────────────────────────────────────────────────────────────────────────────
```

---

## Phase 1: Foundation (Weeks 1-8)

### Milestone 1.1: vorpal-core v0.1 (Weeks 1-4)

**Goal**: Ship a working AI registry with basic policy evaluation

**Deliverables**:

| Deliverable | Description | Acceptance Criteria |
|-------------|-------------|---------------------|
| Data Model | PostgreSQL schema for systems, controls, evidence | Schema migration runs cleanly |
| REST API | CRUD for systems, policies, audit events | OpenAPI spec, all endpoints tested |
| YAML Policy Engine | Simple rule evaluation | Can block/allow based on rules |
| CLI | `vorpal` command line tool | Register, list, query systems |
| Docker Image | Production-ready container | `docker run` works out of box |

**Data Model**:

```sql
-- Core entities
CREATE TABLE ai_systems (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type ENUM('model', 'application', 'agent', 'pipeline') NOT NULL,
    status ENUM('draft', 'review', 'approved', 'deployed', 'deprecated') NOT NULL,
    risk_tier ENUM('prohibited', 'high', 'limited', 'minimal') NOT NULL,
    autonomy_level INTEGER CHECK (autonomy_level BETWEEN 1 AND 5),
    owner_id UUID NOT NULL REFERENCES users(id),
    team_id UUID REFERENCES teams(id),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE controls (
    id VARCHAR(50) PRIMARY KEY,  -- e.g., 'CTRL-ACC-001'
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category ENUM('accuracy', 'bias', 'security', 'privacy', 'safety', 'transparency'),
    regulation VARCHAR(50),  -- e.g., 'EU-AI-ACT', 'NYC-LL-144'
    requirement_text TEXT,
    test_guidance TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE system_controls (
    system_id UUID REFERENCES ai_systems(id) ON DELETE CASCADE,
    control_id VARCHAR(50) REFERENCES controls(id),
    status ENUM('pending', 'implemented', 'tested', 'verified', 'failed') NOT NULL,
    evidence_required BOOLEAN DEFAULT true,
    notes TEXT,
    PRIMARY KEY (system_id, control_id)
);

CREATE TABLE audit_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    system_id UUID REFERENCES ai_systems(id),
    event_type VARCHAR(50) NOT NULL,
    actor_id UUID,
    actor_type ENUM('user', 'system', 'api_key'),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(255),
    details JSONB DEFAULT '{}',
    previous_hash VARCHAR(64),  -- SHA-256 of previous event (chain integrity)
    event_hash VARCHAR(64) NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_audit_system ON audit_events(system_id, timestamp DESC);
CREATE INDEX idx_audit_hash ON audit_events(event_hash);
```

**API Endpoints**:

```yaml
# OpenAPI summary
paths:
  /api/v1/systems:
    get:
      summary: List AI systems
      parameters:
        - name: status
        - name: risk_tier
        - name: team_id
    post:
      summary: Register new AI system

  /api/v1/systems/{id}:
    get:
      summary: Get system details
    patch:
      summary: Update system
    delete:
      summary: Archive system (soft delete)

  /api/v1/systems/{id}/controls:
    get:
      summary: List controls for system
    post:
      summary: Assign control to system

  /api/v1/policies:
    get:
      summary: List policies
    post:
      summary: Create policy

  /api/v1/policies/evaluate:
    post:
      summary: Evaluate policy against input
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                system_id:
                  type: string
                action:
                  type: string
                context:
                  type: object

  /api/v1/audit:
    get:
      summary: Query audit log
      parameters:
        - name: system_id
        - name: from
        - name: to
        - name: event_type
```

**Policy Format (YAML v1)**:

```yaml
# policies/high-risk-systems.yaml
apiVersion: vorpal.dev/v1
kind: Policy
metadata:
  name: high-risk-deployment-gates
  description: Require approvals for high-risk AI systems
spec:
  match:
    risk_tier: high
    action: deploy
  rules:
    - name: require-bias-testing
      condition: |
        system.controls.exists(c, c.id == "CTRL-BIAS-001" && c.status == "verified")
      message: "High-risk systems require verified bias testing"

    - name: require-human-approval
      condition: |
        system.approvals.exists(a, a.role == "compliance_officer" && a.status == "approved")
      message: "High-risk deployment requires compliance officer approval"

    - name: require-documentation
      condition: |
        system.documentation.technical_doc != null &&
        system.documentation.risk_assessment != null
      message: "High-risk systems require technical documentation and risk assessment"
```

**Technical Decisions**:

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Python 3.11+ | Ecosystem compatibility, async support |
| Framework | FastAPI | Modern, async, auto-docs |
| Database | PostgreSQL 15+ | JSONB, reliability, free |
| Policy eval | CEL initially → OPA later | CEL is simpler; OPA when needed |
| Auth | API keys + JWT | Simple to start, SSO-ready |
| Container | Alpine-based | Minimal attack surface |

**Week-by-Week Breakdown**:

| Week | Focus | Deliverables |
|------|-------|--------------|
| 1 | Project setup | Repo, CI/CD, dev environment, schema v1 |
| 2 | Core API | Systems CRUD, basic auth, OpenAPI |
| 3 | Policy engine | YAML parsing, CEL evaluation, policy CRUD |
| 4 | Audit + CLI | Audit logging, hash chain, CLI tool, Docker |

---

### Milestone 1.2: vorpal-gateway v0.1 (Weeks 5-8)

**Goal**: Ship an LLM proxy with cost tracking and basic DLP

**Deliverables**:

| Deliverable | Description | Acceptance Criteria |
|-------------|-------------|---------------------|
| LLM Proxy | Forward to OpenAI, Anthropic, Azure | All major providers work |
| Cost Tracking | Token counts, cost attribution | Per-request cost logged |
| Basic DLP | PII detection and redaction | Presidio integration works |
| Rate Limiting | Per-team, per-system limits | Configurable, Redis-backed |
| SDK | Python client library | Drop-in replacement for `openai` |

**Architecture**:

```
┌─────────────────────────────────────────────────────────────────────┐
│                       vorpal-gateway                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Request Flow:                                                      │
│                                                                     │
│  [Client] ──▶ [Auth] ──▶ [Policy Check] ──▶ [DLP Scan] ──▶         │
│              │           │                  │                       │
│              │           │                  ▼                       │
│              │           │           [Rate Limit] ──▶ [Route]       │
│              │           │                              │           │
│              │           │                              ▼           │
│              │           │                        [LLM Provider]    │
│              │           │                              │           │
│              │           │                              ▼           │
│              │           │                     [Response Filter]    │
│              │           │                              │           │
│              ▼           ▼                              ▼           │
│         [Audit Log] ◀───────────────────────────── [Cost Tag]      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Configuration**:

```yaml
# vorpal-gateway.yaml
apiVersion: vorpal.dev/v1
kind: GatewayConfig
metadata:
  name: production

spec:
  # LLM provider configuration
  providers:
    - name: openai
      type: openai
      api_key: ${OPENAI_API_KEY}
      models:
        - gpt-4o
        - gpt-4o-mini

    - name: anthropic
      type: anthropic
      api_key: ${ANTHROPIC_API_KEY}
      models:
        - claude-3-5-sonnet-20241022
        - claude-3-5-haiku-20241022

    - name: azure-openai
      type: azure
      endpoint: ${AZURE_OPENAI_ENDPOINT}
      api_key: ${AZURE_OPENAI_KEY}
      deployment_map:
        gpt-4o: gpt-4o-deployment

  # Routing rules
  routing:
    default_provider: openai
    rules:
      - match:
          team: finance
        provider: azure-openai
        reason: "Finance team requires Azure for compliance"

      - match:
          model: claude-*
        provider: anthropic

  # DLP configuration
  dlp:
    enabled: true
    scan_requests: true
    scan_responses: false  # Usually not needed
    entities:
      - PERSON
      - EMAIL_ADDRESS
      - PHONE_NUMBER
      - CREDIT_CARD
      - US_SSN
    action: redact  # or 'block', 'log'
    redaction_char: "█"

  # Rate limiting
  rate_limits:
    global:
      requests_per_minute: 1000
      tokens_per_minute: 500000
    per_team:
      default:
        requests_per_minute: 100
        tokens_per_minute: 50000

  # Cost tracking
  cost:
    enabled: true
    alert_threshold_daily: 1000  # USD
    budget_enforcement: warn  # or 'block'
```

**SDK Usage**:

```python
# Drop-in replacement for OpenAI
from vorpal.gateway import VorpalClient

# Initialize with gateway URL
client = VorpalClient(
    gateway_url="https://gateway.vorpal.dev",
    api_key="vp_sk_...",
    system_id="agent_customer_service"  # For attribution
)

# Same API as OpenAI
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Hello!"}
    ],
    metadata={
        "request_id": "req_123",
        "user_id": "user_456"
    }
)

# Cost information attached to response
print(f"Cost: ${response.usage.cost:.4f}")
print(f"Request ID: {response.vorpal_request_id}")
```

**Week-by-Week Breakdown**:

| Week | Focus | Deliverables |
|------|-------|--------------|
| 5 | LLM proxy core | Async proxy, OpenAI/Anthropic support, basic routing |
| 6 | DLP + Security | Presidio integration, injection detection |
| 7 | Cost + Rate limiting | Token counting, cost attribution, Redis rate limits |
| 8 | SDK + Integration | Python SDK, vorpal-core integration, Docker |

---

## Phase 2: Enforcement (Weeks 9-16)

### Milestone 2.1: vorpal-sentinel v0.1 (Weeks 9-12)

**Goal**: Ship runtime guardrails for LangChain agents with HITL

**Deliverables**:

| Deliverable | Description | Acceptance Criteria |
|-------------|-------------|---------------------|
| LangChain Adapter | Callback handler for LangChain agents | Works with standard agent types |
| Autonomy Levels | L1-L5 enforcement | Actions blocked based on level |
| Kill Switch | Emergency stop capability | Sub-second response time |
| HITL Manager | Human approval workflows | WebSocket + REST API |
| Session Tracking | Agent session lifecycle | Full audit trail per session |

**Autonomy Level Framework**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AUTONOMY LEVELS                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  L1: INFORMATIONAL                                                          │
│  ├─ Allowed: Read-only queries, search, retrieval                           │
│  ├─ Blocked: Any write operation, external API calls                        │
│  └─ HITL: Never (fully autonomous within read scope)                        │
│                                                                              │
│  L2: CONSTRAINED                                                            │
│  ├─ Allowed: L1 + writes to designated safe zones                           │
│  ├─ Blocked: External APIs, financial operations, PII access                │
│  └─ HITL: On scope boundary crossing                                        │
│                                                                              │
│  L3: SUPERVISED                                                              │
│  ├─ Allowed: L2 + external read APIs, limited tool set                      │
│  ├─ Blocked: Financial transactions, credential access                      │
│  └─ HITL: On high-risk actions (configurable)                               │
│                                                                              │
│  L4: DELEGATED                                                               │
│  ├─ Allowed: L3 + most tools, external write APIs                           │
│  ├─ Blocked: Irreversible operations without approval                       │
│  └─ HITL: On irreversible/high-impact actions                               │
│                                                                              │
│  L5: AUTONOMOUS                                                              │
│  ├─ Allowed: All operations within budget/scope                             │
│  ├─ Blocked: Only explicit blacklist                                        │
│  └─ HITL: Emergency only (budget breach, anomaly)                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**LangChain Integration**:

```python
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from vorpal.sentinel import Sentinel, SentinelCallback

# Initialize sentinel
sentinel = Sentinel(
    governance_url="http://localhost:8000",
    system_id="agent_research",
    autonomy_level=3,  # L3: Supervised
    hitl_config={
        "mode": "async",  # 'sync', 'async', 'webhook'
        "timeout": 300,   # 5 minutes for human response
        "default_action": "block"  # if timeout: 'block' or 'allow'
    }
)

# Start session
session = sentinel.start_session(
    user_id="user_123",
    context={"task": "Research AI governance regulations"}
)

# Create agent with sentinel
agent = initialize_agent(
    tools=[...],
    llm=ChatOpenAI(model="gpt-4o"),
    agent=AgentType.OPENAI_FUNCTIONS,
    callbacks=[SentinelCallback(sentinel, session)]
)

# Run agent (sentinel enforces guardrails)
try:
    result = agent.run("Find and summarize EU AI Act requirements")
except SentinelBlockedError as e:
    print(f"Action blocked: {e.reason}")
except SentinelHITLRequired as e:
    print(f"Human approval required: {e.action}")
    # Handle HITL flow

# End session
session.end(outcome="success")
```

**HITL Flow**:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Agent     │────▶│   Sentinel   │────▶│  HITL Queue  │
│              │     │              │     │              │
│ (attempts    │     │ (checks if   │     │ (stores      │
│  action)     │     │  HITL needed)│     │  pending)    │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                            ┌─────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│                    HUMAN REVIEWER                         │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Action Pending Approval                           │  │
│  │                                                    │  │
│  │  Agent: agent_research                             │  │
│  │  Session: ses_abc123                               │  │
│  │  User: user_456                                    │  │
│  │                                                    │  │
│  │  Action: tool_call                                 │  │
│  │  Tool: web_search                                  │  │
│  │  Query: "EU AI Act financial services"            │  │
│  │                                                    │  │
│  │  Risk: MEDIUM (external API, no writes)           │  │
│  │  Context: Researching governance regulations       │  │
│  │                                                    │  │
│  │  [✓ Approve]  [✗ Deny]  [Approve All Similar]     │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
                   ┌──────────────┐
                   │   Decision   │──▶ Agent continues or blocked
                   │   recorded   │
                   │   in audit   │
                   └──────────────┘
```

**Week-by-Week Breakdown**:

| Week | Focus | Deliverables |
|------|-------|--------------|
| 9 | Core sentinel | Action checking, autonomy levels, session management |
| 10 | LangChain adapter | Callback handler, error handling, retry logic |
| 11 | Kill switch + HITL | Emergency stop, WebSocket queue, approval flow |
| 12 | Integration + Polish | vorpal-core integration, UI stub, Docker |

---

### Milestone 2.2: vorpal-arbiter v0.1 (Weeks 13-16)

**Goal**: Ship MCP proxy with permission-based tool governance

**Motivation**: MCP (Model Context Protocol) is becoming standard for tool access, but **no governance layer exists**. This is a greenfield opportunity.

**Deliverables**:

| Deliverable | Description | Acceptance Criteria |
|-------------|-------------|---------------------|
| MCP Proxy | Sits between agent and MCP servers | Transparent proxying works |
| Permission Model | Tool-level, param-level permissions | Deny unauthorized tools |
| Rate Limiting | Per-tool, per-agent limits | Redis-backed |
| Param Validation | Type and value constraints | JSON Schema validation |
| Budget Control | Cost caps for expensive tools | Block on budget exceeded |

**Architecture**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         vorpal-arbiter                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────┐           ┌────────────────┐           ┌───────────────┐     │
│  │   Agent   │──────────▶│  Arbiter Proxy │──────────▶│  MCP Server   │     │
│  │           │           │                │           │               │     │
│  │ (MCP      │           │ 1. Authenticate│           │ (filesystem,  │     │
│  │  client)  │           │ 2. Check perms │           │  database,    │     │
│  │           │           │ 3. Validate    │           │  web, etc.)   │     │
│  │           │◀──────────│ 4. Rate limit  │◀──────────│               │     │
│  │           │           │ 5. Forward     │           │               │     │
│  │           │           │ 6. Log         │           │               │     │
│  └───────────┘           └────────────────┘           └───────────────┘     │
│                                  │                                           │
│                                  ▼                                           │
│                          ┌──────────────┐                                   │
│                          │ vorpal-core  │                                   │
│                          │ (policies,   │                                   │
│                          │  audit)      │                                   │
│                          └──────────────┘                                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Permission Model**:

```yaml
# tool-permissions.yaml
apiVersion: vorpal.dev/v1
kind: ToolPermissions
metadata:
  name: agent-research-tools

spec:
  system_id: agent_research
  autonomy_level: 3

  # Default behavior
  default_action: deny
  default_log: true

  # Tool-specific permissions
  tools:
    # Full access to search
    - server: brave-search
      tool: search
      action: allow
      rate_limit:
        requests_per_minute: 60

    # Read-only filesystem
    - server: filesystem
      tool: read_file
      action: allow
      params:
        path:
          pattern: "^/workspace/.*"  # Only workspace directory
          deny_pattern: ".*\\.(env|key|pem)$"  # No secrets

    - server: filesystem
      tool: write_file
      action: hitl  # Requires approval
      hitl_reason: "File writes require human approval"

    - server: filesystem
      tool: delete_file
      action: deny
      deny_reason: "Delete operations not permitted"

    # Database with row limits
    - server: postgres
      tool: query
      action: allow
      params:
        query:
          max_length: 1000
          deny_pattern: "(DROP|DELETE|TRUNCATE|ALTER)"
      rate_limit:
        requests_per_minute: 30
      budget:
        max_rows_per_request: 1000
        max_rows_per_session: 10000

    # External API with budget
    - server: github
      tool: "*"  # All tools
      action: allow
      budget:
        api_calls_per_hour: 100
```

**SDK Usage**:

```python
from vorpal.arbiter import ArbiterClient

# Create arbiter-wrapped MCP client
mcp = ArbiterClient(
    arbiter_url="http://localhost:8081",
    api_key="vp_sk_...",
    system_id="agent_research",
    session_id="ses_abc123"  # For attribution
)

# Connect to MCP servers through arbiter
await mcp.connect("filesystem", "stdio://mcp-server-filesystem")
await mcp.connect("github", "http://localhost:3000/mcp/github")

# Tool calls go through arbiter
try:
    result = await mcp.call_tool(
        server="filesystem",
        tool="read_file",
        params={"path": "/workspace/readme.md"}
    )
except PermissionDenied as e:
    print(f"Not allowed: {e.reason}")
except BudgetExceeded as e:
    print(f"Budget exceeded: {e.limit} {e.current}")
```

**Week-by-Week Breakdown**:

| Week | Focus | Deliverables |
|------|-------|--------------|
| 13 | MCP proxy core | stdio + SSE transport, request forwarding |
| 14 | Permission engine | Tool matching, param validation, deny logic |
| 15 | Rate limit + Budget | Redis limits, budget tracking, alerts |
| 16 | Integration + Polish | vorpal-core integration, SDK, Docker |

---

## Phase 3: Evaluation & Polish (Weeks 17-24)

### Milestone 3.1: vorpal-eval v0.1 (Weeks 17-20)

**Goal**: Ship quality evaluation with bias testing and CI/CD integration

**Deliverables**:

| Deliverable | Description | Acceptance Criteria |
|-------------|-------------|---------------------|
| Test Runner | Execute eval suites | YAML-defined tests work |
| LLM Judge | AI-powered quality scoring | Configurable criteria |
| Bias Metrics | Demographic parity, etc. | Standard metrics implemented |
| CI/CD Integration | GitHub Actions, quality gates | Block deploy on regression |
| Evidence Export | Compliance artifacts | PDF/JSON export |

**Eval Definition Format**:

```yaml
# evals/customer_service_agent.yaml
apiVersion: vorpal.dev/v1
kind: Evaluation
metadata:
  name: customer_service_quality
  system_id: agent_customer_service

spec:
  # Regulatory controls this eval addresses
  controls:
    - CTRL-ACC-001  # Response accuracy
    - CTRL-BIAS-001  # Demographic fairness
    - CTRL-SAFE-001  # Safety guidelines

  # Test datasets
  datasets:
    - name: golden_qa
      source: s3://vorpal-evals/customer_service/golden_qa.jsonl
      format: jsonl
      fields:
        input: question
        expected: ideal_response

    - name: bias_test_set
      source: s3://vorpal-evals/customer_service/bias_test.jsonl
      fields:
        input: question
        demographic: demographic_group

  # Metrics to compute
  metrics:
    # Accuracy via LLM judge
    - name: response_quality
      type: llm_judge
      config:
        model: claude-3-5-haiku-20241022
        criteria:
          - name: accuracy
            description: "Is the response factually correct?"
            scale: 1-5
          - name: helpfulness
            description: "Does the response address the user's need?"
            scale: 1-5
          - name: safety
            description: "Is the response safe and appropriate?"
            scale: 1-5
        threshold:
          accuracy: 4.0
          helpfulness: 3.5
          safety: 4.5

    # Bias metrics
    - name: demographic_parity
      type: bias
      config:
        method: demographic_parity
        group_field: demographic
        favorable_outcome: response_quality.accuracy >= 4
        threshold: 0.1  # Max 10% disparity

    - name: equalized_odds
      type: bias
      config:
        method: equalized_odds
        group_field: demographic

    # Regression detection
    - name: regression
      type: regression
      config:
        baseline: s3://vorpal-evals/customer_service/baseline_v1.json
        tolerance: 0.05  # 5% degradation threshold

  # Quality gates
  gates:
    - name: accuracy_gate
      condition: response_quality.accuracy >= 4.0
      severity: error

    - name: bias_gate
      condition: demographic_parity <= 0.1
      severity: error

    - name: regression_gate
      condition: regression.degradation <= 0.05
      severity: warning

  # Evidence generation
  evidence:
    enabled: true
    format: pdf
    include:
      - summary
      - metric_details
      - sample_failures
      - recommendations
```

**CLI Usage**:

```bash
# Run evaluation
vorpal-eval run evals/customer_service_agent.yaml \
  --system-endpoint http://localhost:8080/agent \
  --output results.json \
  --parallel 10

# Check gates
vorpal-eval gate \
  --results results.json \
  --fail-on error

# Generate evidence
vorpal-eval evidence \
  --results results.json \
  --format pdf \
  --output evidence/customer_service_2026_01.pdf

# Upload to governance
vorpal-eval submit \
  --results results.json \
  --governance-url http://localhost:8000 \
  --system-id agent_customer_service
```

**GitHub Actions Integration**:

```yaml
# .github/workflows/deploy-agent.yml
name: Deploy AI Agent

on:
  push:
    branches: [main]
    paths:
      - 'agents/customer_service/**'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run AI Evaluations
        run: |
          vorpal-eval run evals/customer_service_agent.yaml \
            --output results.json

      - name: Check Quality Gates
        run: |
          vorpal-eval gate \
            --results results.json \
            --fail-on regression \
            --fail-on threshold_violation

      - name: Export Evidence
        if: success()
        run: |
          vorpal-eval evidence \
            --system agent_customer_service \
            --results results.json \
            --governance-url ${{ secrets.GOVERNANCE_URL }}

  deploy:
    needs: evaluate
    runs-on: ubuntu-latest
    steps:
      - name: Update System Status
        run: |
          curl -X PATCH $GOVERNANCE_URL/api/v1/systems/$SYSTEM_ID \
            -H "Authorization: Bearer ${{ secrets.GOVERNANCE_TOKEN }}" \
            -d '{"status": "deployed", "version": "${{ github.sha }}"}'

      - name: Deploy Agent
        run: |
          # Your deployment steps
```

**Week-by-Week Breakdown**:

| Week | Focus | Deliverables |
|------|-------|--------------|
| 17 | Test runner | YAML parsing, dataset loading, parallel execution |
| 18 | LLM judge | Criteria evaluation, scoring, aggregation |
| 19 | Bias metrics | Demographic parity, equalized odds, threshold checking |
| 20 | CI/CD + Evidence | GitHub Action, gates, PDF export |

---

### Milestone 3.2: Integration & Polish (Weeks 21-24)

**Goal**: Ship unified dashboard, Helm charts, and documentation

**Deliverables**:

| Deliverable | Description | Acceptance Criteria |
|-------------|-------------|---------------------|
| Dashboard UI | Unified view of all components | Basic React dashboard |
| Helm Charts | Production Kubernetes deployment | Works on standard k8s |
| Documentation | User guides, API docs, tutorials | Read-the-Docs site |
| Demo | End-to-end demo environment | `docker compose up` works |
| v1.0 Release | All components tagged v1.0 | Published to PyPI, ghcr.io |

**Dashboard Features**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  VORPAL DASHBOARD                                    [Settings] [Docs]     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐               │
│  │  AI SYSTEMS     │ │  GATEWAY        │ │  AGENTS         │               │
│  │                 │ │                 │ │                 │               │
│  │  Total: 24      │ │  Req/min: 1.2K  │ │  Active: 12     │               │
│  │  High Risk: 3   │ │  Cost/hr: $42   │ │  HITL Queue: 2  │               │
│  │  Pending: 5     │ │  DLP blocks: 7  │ │  Kill: 0        │               │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘               │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  RECENT ACTIVITY                                                      │ │
│  │                                                                       │ │
│  │  12:34  agent_research deployed to production           [View]       │ │
│  │  12:31  HITL approval: filesystem write by agent_writer [Review]     │ │
│  │  12:28  DLP blocked: credit card in prompt              [Details]    │ │
│  │  12:25  Eval passed: customer_service 94.2% accuracy    [Report]     │ │
│  │  12:20  New system registered: agent_finance            [Configure]  │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────┐ ┌─────────────────────────────────┐   │
│  │  COST BY TEAM (24h)             │ │  EVAL TRENDS                    │   │
│  │  ████████████████████ Finance   │ │  Accuracy ───────────────▲      │   │
│  │  ████████████ Engineering       │ │  Bias     ─────────▼────────    │   │
│  │  ██████ Research                │ │  Safety   ────────────────────  │   │
│  │  ███ Marketing                  │ │                                 │   │
│  └─────────────────────────────────┘ └─────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Helm Chart Structure**:

```
charts/vorpal/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── configmap.yaml
│   ├── deployment-core.yaml
│   ├── deployment-gateway.yaml
│   ├── deployment-arbiter.yaml
│   ├── deployment-dashboard.yaml
│   ├── service-core.yaml
│   ├── service-gateway.yaml
│   ├── ingress.yaml
│   ├── networkpolicy.yaml
│   ├── pdb.yaml
│   └── hpa.yaml
├── charts/
│   ├── postgresql/
│   ├── redis/
│   └── clickhouse/
└── ci/
    └── test-values.yaml
```

**Week-by-Week Breakdown**:

| Week | Focus | Deliverables |
|------|-------|--------------|
| 21 | Dashboard | React app, API integration, basic visualizations |
| 22 | Helm charts | Production charts, ingress, scaling |
| 23 | Documentation | User guides, API reference, tutorials |
| 24 | Release | v1.0 tagging, PyPI publish, blog post |

---

## Technical Architecture Decisions

### Language & Framework Choices

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Primary language | **Python 3.11+** | Ecosystem compatibility (LangChain, etc.), async, typing |
| API framework | **FastAPI** | Modern, async, auto OpenAPI, great typing |
| Database | **PostgreSQL 15+** | JSONB, reliability, ACID, free |
| Cache/queue | **Redis 7+** | Rate limiting, sessions, pub/sub |
| Analytics | **ClickHouse** | High-volume logs, cheap storage, fast queries |
| Policy engine | **OPA/Rego** | Industry standard, flexible, testable |
| DLP | **Presidio** | Microsoft-backed, extensible, free |
| Observability | **OpenTelemetry** | Standard, vendor-neutral |
| Container | **Alpine Linux** | Minimal attack surface |

### API Design Principles

1. **REST-first, gRPC-later**: Start with REST for accessibility, add gRPC when performance matters
2. **OpenAPI always**: Auto-generated docs, client SDKs
3. **Versioned URLs**: `/api/v1/...` from day one
4. **Consistent pagination**: Cursor-based, max 100 items
5. **Structured errors**: JSON with `code`, `message`, `details`

### Security Model

| Layer | Mechanism |
|-------|-----------|
| **Authentication** | API keys (simple), JWT (SSO), mTLS (service mesh) |
| **Authorization** | RBAC in vorpal-core, propagated via tokens |
| **Data at rest** | AES-256 encryption for secrets |
| **Data in transit** | TLS 1.3 required |
| **Secrets** | External secrets support (Vault, AWS SM, k8s secrets) |
| **Audit** | Immutable, hash-chained logs |

---

## Repository Structure

```
github.com/alice-in-wonderland-ai/vorpal/
├── README.md
├── LICENSE                  # Apache 2.0
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
│
├── vorpal-core/
│   ├── pyproject.toml
│   ├── src/vorpal/core/
│   │   ├── __init__.py
│   │   ├── api/
│   │   ├── models/
│   │   ├── policy/
│   │   ├── audit/
│   │   └── cli/
│   ├── tests/
│   ├── migrations/
│   └── Dockerfile
│
├── vorpal-gateway/
│   ├── pyproject.toml
│   ├── src/vorpal/gateway/
│   │   ├── __init__.py
│   │   ├── proxy/
│   │   ├── dlp/
│   │   ├── routing/
│   │   └── cost/
│   ├── tests/
│   └── Dockerfile
│
├── vorpal-sentinel/
│   ├── pyproject.toml
│   ├── src/vorpal/sentinel/
│   │   ├── __init__.py
│   │   ├── guardrails/
│   │   ├── adapters/
│   │   │   ├── langchain.py
│   │   │   ├── crewai.py
│   │   │   └── autogen.py
│   │   └── hitl/
│   ├── tests/
│   └── Dockerfile
│
├── vorpal-arbiter/
│   ├── pyproject.toml
│   ├── src/vorpal/arbiter/
│   │   ├── __init__.py
│   │   ├── proxy/
│   │   ├── permissions/
│   │   └── budget/
│   ├── tests/
│   └── Dockerfile
│
├── vorpal-eval/
│   ├── pyproject.toml
│   ├── src/vorpal/eval/
│   │   ├── __init__.py
│   │   ├── runner/
│   │   ├── metrics/
│   │   ├── judges/
│   │   └── evidence/
│   ├── tests/
│   └── Dockerfile
│
├── vorpal-sdk/                   # Shared Python SDK
│   ├── pyproject.toml
│   └── src/vorpal/
│       ├── __init__.py
│       ├── client.py
│       └── types.py
│
├── vorpal-dashboard/
│   ├── package.json
│   ├── src/
│   └── Dockerfile
│
├── charts/
│   └── vorpal/
│       ├── Chart.yaml
│       └── templates/
│
├── docker-compose.yml            # Local development
├── docker-compose.prod.yml       # Production reference
│
├── docs/
│   ├── getting-started.md
│   ├── architecture.md
│   ├── api-reference/
│   ├── tutorials/
│   └── regulatory-packs/
│
└── examples/
    ├── langchain-agent/
    ├── crewai-agent/
    └── ci-cd-integration/
```

---

## Go-to-Market Strategy

### Target Audiences

| Segment | Pain Point | Value Proposition |
|---------|------------|-------------------|
| **Startups** | "We need governance but can't afford Credo" | Free, production-ready, grows with you |
| **Mid-market** | "DIY governance is fragmented" | Unified stack, works together |
| **Regulated industries** | "We need compliance evidence" | Built-in regulatory packs, audit trail |
| **OSS projects** | "How do we show we're responsible?" | Public governance dashboard |

### Launch Strategy

**Phase 1: Developer Preview (End of Phase 1)**
- GitHub release with basic docs
- Hacker News, Reddit /r/MachineLearning
- Target: 100 GitHub stars, 20 users

**Phase 2: Community Building (End of Phase 2)**
- Documentation site
- Discord community
- Blog: "Why we built Vorpal"
- Conference talks (AI Engineer, PyCon)
- Target: 500 stars, 100 users, 5 contributors

**Phase 3: Production Launch (End of Phase 3)**
- v1.0 release
- Case studies from early adopters
- Integration partnerships (LangChain, LlamaIndex)
- Target: 2000 stars, 500 users, 20 contributors

### Success Metrics

| Metric | 3 months | 6 months | 12 months |
|--------|----------|----------|-----------|
| GitHub stars | 500 | 2,000 | 5,000 |
| Monthly downloads | 1,000 | 10,000 | 50,000 |
| Production deployments | 5 | 50 | 200 |
| Contributors | 5 | 20 | 50 |
| Discord members | 100 | 500 | 2,000 |

---

## Resource Requirements

### Staffing Model

**Minimum Viable Team** (6 months to v1.0):

| Role | FTE | Responsibilities |
|------|-----|------------------|
| **Lead Engineer** | 1.0 | Architecture, core/gateway, code review |
| **Backend Engineer** | 1.0 | Sentinel, arbiter, integrations |
| **Platform Engineer** | 0.5 | Helm, CI/CD, deployment |
| **Technical Writer** | 0.5 | Docs, tutorials, examples |

**Enhanced Team** (faster delivery, broader scope):

| Role | FTE | Responsibilities |
|------|-----|------------------|
| **Lead Engineer** | 1.0 | Architecture, code review, community |
| **Backend Engineer** | 2.0 | Core components |
| **Frontend Engineer** | 1.0 | Dashboard, UX |
| **Platform Engineer** | 1.0 | Helm, operators, scale testing |
| **DevRel** | 0.5 | Community, content, talks |
| **Technical Writer** | 0.5 | Docs |

### Infrastructure Costs

**Development/Staging**:

| Resource | Monthly Cost |
|----------|-------------|
| CI/CD (GitHub Actions) | $0 (OSS minutes) |
| Container registry (ghcr.io) | $0 |
| Test cluster (local k3d) | $0 |
| Domain + DNS | $20 |
| **Total** | **$20/month** |

**Demo/Reference Environment**:

| Resource | Monthly Cost |
|----------|-------------|
| DigitalOcean Droplet (8GB) | $48 |
| Managed PostgreSQL (small) | $15 |
| Managed Redis (small) | $10 |
| S3/R2 storage (100GB) | $5 |
| **Total** | **$78/month** |

---

## Risk Analysis

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| OPA complexity blocks adoption | Medium | High | Start with YAML policies, add OPA optional |
| MCP protocol changes | Medium | Medium | Abstract MCP layer, version pin |
| LangChain breaking changes | High | Medium | Version matrix, adapter pattern |
| Performance at scale | Low | High | Load testing from Phase 2 |

### Market Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Major vendor releases OSS competitor | Medium | High | Move fast, community moat |
| Regulations change significantly | Low | Medium | Pluggable policy packs |
| AI agents don't take off | Low | High | Gateway/eval still valuable standalone |

### Execution Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Scope creep | High | Medium | Strict milestone scope, MVP focus |
| Key person dependency | Medium | High | Documentation, pair programming |
| Community doesn't form | Medium | Medium | Active DevRel, genuine engagement |

---

## Integration with Alice in Wonderland AI

### How Components Work Together

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    COMPLETE AGENT ARCHITECTURE                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────┐                                                         │
│  │    USER      │                                                         │
│  │              │                                                         │
│  └──────┬───────┘                                                         │
│         │                                                                  │
│         ▼                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
│  │LOOKING GLASS │────▶│   CHESHIRE   │────▶│  MAD HATTER  │               │
│  │   (chat UI)  │     │   (memory)   │     │  (workflow)  │               │
│  └──────────────┘     └──────────────┘     └──────┬───────┘               │
│                                                   │                        │
│         ┌─────────────────────────────────────────┘                        │
│         │                                                                  │
│         ▼                                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐      │
│  │                        VORPAL (governance)                        │      │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐     │      │
│  │  │vorpal-core│  │  gateway  │  │ sentinel  │  │  arbiter  │     │      │
│  │  │(registry) │◀─│(LLM calls)│◀─│ (agent)   │◀─│(MCP/tools)│     │      │
│  │  └───────────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘     │      │
│  │                       │              │              │            │      │
│  └───────────────────────┼──────────────┼──────────────┼────────────┘      │
│                          │              │              │                    │
│         ┌────────────────┼──────────────┼──────────────┘                    │
│         │                │              │                                   │
│         ▼                ▼              ▼                                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                        │
│  │ MCP SERVERS  │ │ LLM PROVIDERS│ │   EXTERNAL   │                        │
│  │ (filesystem, │ │ (OpenAI,     │ │   SERVICES   │                        │
│  │  database,   │ │  Anthropic,  │ │ (GitHub,     │                        │
│  │  web, etc.)  │ │  Azure)      │ │  Slack, etc.)│                        │
│  └──────────────┘ └──────────────┘ └──────────────┘                        │
│                                                                            │
│         │                                                                  │
│         └─────────────────────────────────────────────────┐                │
│                                                           │                │
│                                                           ▼                │
│                                                ┌──────────────────┐        │
│                                                │     ALICE        │        │
│                                                │  (cognitive core)│        │
│                                                │                  │        │
│                                                │  • System 1/2    │        │
│                                                │  • Planning      │        │
│                                                │  • Reasoning     │        │
│                                                └──────────────────┘        │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Shared Standards

All Alice in Wonderland AI components share:

1. **Configuration format**: YAML with JSON Schema validation
2. **Auth tokens**: JWT with standard claims, scopes
3. **Tracing**: OpenTelemetry with W3C trace context
4. **Logging**: Structured JSON, common fields
5. **API versioning**: `/api/v1/`, semantic versioning
6. **Health checks**: `/health` and `/ready` endpoints
7. **Metrics**: Prometheus format on `/metrics`

### Cross-Component Flows

**Example: Agent executes with full governance**

```
1. User sends message via Looking Glass
2. Looking Glass routes to Alice (cognitive core)
3. Alice checks Cheshire for context
4. Alice dispatches to Mad Hatter workflow
5. Mad Hatter starts agent session

6. Agent makes LLM call
   → vorpal-gateway intercepts
   → Checks policy (vorpal-core)
   → DLP scan
   → Routes to provider
   → Logs cost

7. Agent calls MCP tool
   → vorpal-arbiter intercepts
   → Checks permissions
   → Rate limit check
   → Forwards to MCP server
   → Logs invocation

8. Agent attempts high-risk action
   → vorpal-sentinel intercepts
   → Autonomy level check
   → HITL queue if needed
   → Human approves/denies
   → Audit logged

9. Task completes
   → Results to Cheshire (memory)
   → Response to Looking Glass
   → User sees result

10. vorpal-eval runs async quality checks
```

---

## Appendix A: Regulatory Control Mappings

### EU AI Act → Vorpal Components

| EU AI Act Article | Requirement | Vorpal Component | How |
|-------------------|-------------|------------------|-----|
| Art 9(1) | Risk management system | vorpal-core | Risk scoring, controls |
| Art 9(7) | Continuous monitoring | vorpal-eval | Scheduled evals |
| Art 12 | Record-keeping | vorpal-core | Audit trail |
| Art 13 | Transparency | vorpal-core | Documentation |
| Art 14 | Human oversight | vorpal-sentinel | HITL, kill switch |
| Art 15 | Accuracy, robustness | vorpal-eval | Quality metrics |
| Art 17 | Quality management | vorpal-core | Policies, controls |

### NIST AI RMF → Vorpal Components

| NIST Function | Requirement | Vorpal Component |
|---------------|-------------|------------------|
| GOVERN | Policies and roles | vorpal-core |
| MAP | AI inventory | vorpal-core registry |
| MEASURE | Testing and metrics | vorpal-eval |
| MANAGE | Risk mitigation | vorpal-sentinel, vorpal-arbiter |

---

## Appendix B: Comparison with Existing Tools

### vorpal-core vs Existing Solutions

| Feature | vorpal-core | Credo.ai | IBM watsonx | MLflow |
|---------|-------------|----------|-------------|--------|
| AI registry | ✓ | ✓ | ✓ | Partial |
| Policy engine | ✓ (OPA) | ✓ | ✓ | ✗ |
| Risk scoring | ✓ | ✓ | ✓ | ✗ |
| Audit trail | ✓ | ✓ | ✓ | Partial |
| Runtime enforcement | **✓** | ✗ | ✗ | ✗ |
| Self-hosted | ✓ | ✗ | Partial | ✓ |
| Cost | Free | $200K+ | $300K+ | Free |

### vorpal-gateway vs Existing Solutions

| Feature | vorpal-gateway | Portkey | LiteLLM | Custom |
|---------|----------------|---------|---------|--------|
| Multi-LLM | ✓ | ✓ | ✓ | DIY |
| DLP | ✓ | ✗ | ✗ | DIY |
| Injection detection | ✓ | Partial | ✗ | DIY |
| Policy integration | **✓** | ✗ | ✗ | DIY |
| Cost attribution | ✓ | ✓ | Partial | DIY |
| Self-hosted | ✓ | Partial | ✓ | ✓ |

### vorpal-arbiter vs Existing Solutions

| Feature | vorpal-arbiter | Nothing | |
|---------|----------------|---------|-----|
| MCP governance | **✓** | ✗ | First mover |
| Tool permissions | ✓ | ✗ | |
| Rate limiting | ✓ | ✗ | |
| Budget control | ✓ | ✗ | |

**Note**: No existing solution governs MCP tool access. This is a greenfield opportunity.

---

## Appendix C: Sample Policies

### EU AI Act High-Risk Deployment

```yaml
apiVersion: vorpal.dev/v1
kind: PolicyPack
metadata:
  name: eu-ai-act-high-risk
  version: "1.0"
  regulation: EU-AI-ACT

policies:
  - name: require-risk-assessment
    description: "Art 9: High-risk systems require risk assessment"
    match:
      risk_tier: high
      action: deploy
    rule: |
      system.documentation.risk_assessment != null &&
      system.documentation.risk_assessment.status == "approved"
    message: "High-risk deployment requires approved risk assessment"
    severity: error

  - name: require-human-oversight
    description: "Art 14: High-risk systems require human oversight"
    match:
      risk_tier: high
      action: deploy
    rule: |
      system.config.autonomy_level <= 3 ||
      system.config.hitl_enabled == true
    message: "High-risk systems require human oversight (autonomy L3 or below, or HITL enabled)"
    severity: error

  - name: require-accuracy-testing
    description: "Art 15: Accuracy and robustness requirements"
    match:
      risk_tier: high
      action: deploy
    rule: |
      system.evaluations.exists(e,
        e.control_id == "CTRL-ACC-001" &&
        e.status == "passed" &&
        e.timestamp > now() - duration("30d")
      )
    message: "High-risk systems require accuracy evaluation within last 30 days"
    severity: error
```

### NYC Local Law 144 Bias Audit

```yaml
apiVersion: vorpal.dev/v1
kind: PolicyPack
metadata:
  name: nyc-ll-144
  version: "1.0"
  regulation: NYC-LL-144

policies:
  - name: annual-bias-audit
    description: "Annual bias audit for automated employment decisions"
    match:
      tags:
        contains: "employment-decision"
      action: deploy
    rule: |
      system.evaluations.exists(e,
        e.type == "bias_audit" &&
        e.status == "passed" &&
        e.timestamp > now() - duration("365d") &&
        e.auditor.independent == true
      )
    message: "Employment decision AI requires annual independent bias audit"
    severity: error

  - name: candidate-disclosure
    description: "Disclosure to candidates"
    match:
      tags:
        contains: "employment-decision"
      action: deploy
    rule: |
      system.documentation.candidate_disclosure != null
    message: "Must have candidate disclosure documentation"
    severity: error
```

---

## Appendix D: Glossary

| Term | Definition |
|------|------------|
| **Autonomy Level** | L1-L5 classification of agent independence |
| **Control** | Specific requirement from regulation or framework |
| **DLP** | Data Loss Prevention |
| **Evidence** | Artifact demonstrating compliance |
| **HITL** | Human-in-the-Loop |
| **MCP** | Model Context Protocol |
| **OPA** | Open Policy Agent |
| **Policy Pack** | Pre-built policies for a regulation |
| **Risk Tier** | EU AI Act classification: prohibited/high/limited/minimal |
| **Sentinel** | Runtime guardian for agent actions |
| **Arbiter** | Decision-maker for tool access |

---

## Related Documents

- [AI Governance Platforms Research](./2026-01-07-ai-governance-platforms.md) — Market analysis and feature mapping
- [OSS AI Governance Stack Spec](./2026-01-07-oss-ai-governance-stack-spec.md) — Technical specification
- [Looking Glass Implementation Plan](./2026-01-07-looking-glass-implementation-plan.md) — Chat UI component

---

*Document Version: 1.0*
*Created: 2026-01-07*
*Part of the Alice in Wonderland AI Project*
