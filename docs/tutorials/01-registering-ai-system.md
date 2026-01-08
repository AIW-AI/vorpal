# Tutorial: Registering Your First AI System

This tutorial walks you through registering an AI system in Vorpal.

## Prerequisites

- Vorpal Core running (see [Getting Started](../getting-started.md))
- Python 3.11+ with `vorpal-sdk` installed

## What You'll Learn

1. Register an AI system via CLI and SDK
2. Understand system types and risk tiers
3. Add metadata and documentation
4. Query your registered systems

## Step 1: Understanding System Types

Vorpal supports four types of AI systems:

| Type | Description | Examples |
|------|-------------|----------|
| `model` | ML models | Fraud detection, sentiment analysis |
| `application` | AI-powered apps | Chatbots, recommendation engines |
| `agent` | Autonomous agents | Customer service, research assistants |
| `pipeline` | Processing flows | ETL with ML, data enrichment |

## Step 2: Understanding Risk Tiers

Based on the EU AI Act, systems are classified by risk:

| Tier | Implications | Examples |
|------|--------------|----------|
| `prohibited` | Not allowed | Social scoring, real-time biometric |
| `high` | Strict requirements | Employment decisions, credit scoring |
| `limited` | Transparency obligations | Chatbots, emotion recognition |
| `minimal` | No special requirements | Spam filters, game AI |

## Step 3: Register via CLI

The quickest way to register a system:

```bash
# Basic registration
vorpal systems create "my-chatbot" \
  --type application \
  --risk-tier limited

# With more details
vorpal systems create "fraud-detection-v2" \
  --type model \
  --risk-tier high \
  --description "ML model for detecting fraudulent transactions"
```

## Step 4: Register via Python SDK

For programmatic registration:

```python
from vorpal import VorpalClient, SystemType, RiskTier

# Initialize client
client = VorpalClient(base_url="http://localhost:8000")

# Register a model
model = client.systems.create(
    name="fraud-detection-v2",
    type=SystemType.MODEL,
    risk_tier=RiskTier.HIGH,
    description="ML model for detecting fraudulent transactions",
    version="2.0.0",
    metadata={
        "framework": "scikit-learn",
        "training_date": "2026-01-01",
        "features": ["amount", "merchant_category", "time_since_last"],
        "performance": {
            "accuracy": 0.95,
            "precision": 0.92,
            "recall": 0.89
        }
    },
    documentation={
        "model_card": "https://docs.example.com/fraud-model-card",
        "training_data": "https://docs.example.com/fraud-training-data",
        "risk_assessment": "https://docs.example.com/fraud-risk-assessment"
    },
    tags=["ml", "fraud", "financial", "production"]
)

print(f"Registered system: {model.id}")
print(f"Status: {model.status}")  # 'draft'
```

## Step 5: Register an Agent

Agents require an autonomy level (1-5):

```python
agent = client.systems.create(
    name="customer-service-agent",
    type=SystemType.AGENT,
    risk_tier=RiskTier.LIMITED,
    description="AI agent for handling customer inquiries",
    autonomy_level=3,  # L3: Supervised
    metadata={
        "model": "gpt-4o",
        "capabilities": ["answer_questions", "lookup_orders", "process_returns"],
        "hitl_enabled": True
    },
    tags=["customer-facing", "production"]
)

print(f"Agent registered with autonomy L{agent.autonomy_level}")
```

## Step 6: List Your Systems

### Via CLI

```bash
# List all systems
vorpal systems list

# Filter by risk tier
vorpal systems list --risk-tier high

# Filter by status
vorpal systems list --status deployed
```

### Via SDK

```python
# List all systems
systems, meta = client.systems.list()
print(f"Total systems: {meta.total}")

for system in systems:
    print(f"- {system.name} ({system.type.value}): {system.status.value}")

# Filter by risk tier
high_risk, _ = client.systems.list(risk_tier=RiskTier.HIGH)
print(f"High-risk systems: {len(high_risk)}")
```

## Step 7: Update System Status

Systems progress through a lifecycle:

```
draft → review → approved → deployed → deprecated
```

```python
# Submit for review
client.systems.update(
    model.id,
    status=SystemStatus.REVIEW
)

# After approval
client.systems.update(
    model.id,
    status=SystemStatus.APPROVED
)

# Deploy
client.systems.update(
    model.id,
    status=SystemStatus.DEPLOYED,
    version="2.0.1"
)
```

## Step 8: View System Details

```bash
# Get full details
vorpal systems get 550e8400-e29b-41d4-a716-446655440000
```

```python
# Via SDK
system = client.systems.get("550e8400-e29b-41d4-a716-446655440000")

print(f"Name: {system.name}")
print(f"Type: {system.type.value}")
print(f"Risk Tier: {system.risk_tier.value}")
print(f"Status: {system.status.value}")
print(f"Created: {system.created_at}")
print(f"Tags: {', '.join(system.tags)}")
```

## Next Steps

- [Creating Governance Controls](./02-creating-controls.md)
- [Writing Policies](./03-writing-policies.md)

## Complete Example

```python
"""Complete example: Registering an AI system inventory."""

from vorpal import VorpalClient, SystemType, RiskTier

client = VorpalClient(base_url="http://localhost:8000")

# Register multiple systems
systems_to_register = [
    {
        "name": "product-recommendations",
        "type": SystemType.MODEL,
        "risk_tier": RiskTier.MINIMAL,
        "description": "Collaborative filtering model for product recommendations",
        "tags": ["ml", "recommendations", "e-commerce"]
    },
    {
        "name": "resume-screening",
        "type": SystemType.MODEL,
        "risk_tier": RiskTier.HIGH,  # Employment decisions = high risk
        "description": "ML model for initial resume screening",
        "tags": ["ml", "hr", "employment"]
    },
    {
        "name": "customer-chatbot",
        "type": SystemType.AGENT,
        "risk_tier": RiskTier.LIMITED,
        "autonomy_level": 2,
        "description": "Customer service chatbot",
        "tags": ["agent", "customer-service"]
    }
]

for sys_data in systems_to_register:
    system = client.systems.create(**sys_data)
    print(f"✓ Registered: {system.name} (risk: {system.risk_tier.value})")

# List high-risk systems
print("\nHigh-risk systems requiring extra controls:")
high_risk, _ = client.systems.list(risk_tier=RiskTier.HIGH)
for system in high_risk:
    print(f"  - {system.name}: {system.description}")
```
