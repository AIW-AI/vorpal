# Policies API

The Policies API manages governance policies and evaluates them against system actions.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/policies` | List policies |
| POST | `/api/v1/policies` | Create policy |
| GET | `/api/v1/policies/{id}` | Get policy |
| PATCH | `/api/v1/policies/{id}` | Update policy |
| DELETE | `/api/v1/policies/{id}` | Delete policy |
| POST | `/api/v1/policies/evaluate` | Evaluate policies |

---

## List Policies

```
GET /api/v1/policies
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | integer | Page number (default: 1) |
| `page_size` | integer | Items per page (default: 20, max: 100) |
| `enabled` | boolean | Filter by enabled status |
| `regulation` | string | Filter by regulation |
| `pack_name` | string | Filter by policy pack |

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v1/policies?enabled=true&regulation=EU-AI-ACT" \
  -H "Authorization: Bearer vp_sk_..."
```

### Example Response

```json
{
  "data": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440000",
      "name": "high-risk-deployment-gates",
      "description": "Require approvals for high-risk AI systems",
      "version": "1.0.0",
      "enabled": true,
      "match_criteria": {
        "risk_tier": ["high"],
        "action": ["deploy"]
      },
      "rules": [
        {
          "name": "require-bias-testing",
          "condition": "system.controls.exists(c, c.id == 'CTRL-BIAS-001' && c.status == 'verified')",
          "message": "High-risk systems require verified bias testing",
          "severity": "error"
        }
      ],
      "default_severity": "error",
      "regulation": "EU-AI-ACT",
      "pack_name": "eu-ai-act-high-risk",
      "metadata": {},
      "created_by": "user-123",
      "created_at": "2026-01-01T00:00:00Z",
      "updated_at": "2026-01-01T00:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 1,
    "total_pages": 1
  }
}
```

---

## Create Policy

```
POST /api/v1/policies
```

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Policy name (unique) |
| `description` | string | No | Policy description |
| `version` | string | No | Version string (default: "1.0.0") |
| `enabled` | boolean | No | Is policy active (default: true) |
| `match_criteria` | object | No | When to evaluate this policy |
| `rules` | array | No | List of policy rules |
| `default_severity` | string | No | Default rule severity |
| `regulation` | string | No | Source regulation |
| `pack_name` | string | No | Policy pack name |
| `metadata` | object | No | Custom metadata |

### Match Criteria

Define when a policy should be evaluated:

```json
{
  "match_criteria": {
    "risk_tier": ["high", "limited"],
    "action": ["deploy", "update"],
    "type": ["agent", "model"],
    "tags": {
      "contains": ["production"]
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `risk_tier` | array | Match system risk tiers |
| `action` | array | Match actions (deploy, update, delete) |
| `type` | array | Match system types |
| `tags.contains` | array | System must have any of these tags |

### Rule Structure

```json
{
  "rules": [
    {
      "name": "rule-name",
      "condition": "CEL expression",
      "message": "Message shown when rule fails",
      "severity": "error"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Rule identifier |
| `condition` | string | Yes | CEL expression to evaluate |
| `message` | string | Yes | Failure message |
| `severity` | string | No | `error`, `warning`, `info` |

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/policies" \
  -H "Authorization: Bearer vp_sk_..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "require-human-oversight",
    "description": "Require human oversight for high-autonomy agents",
    "match_criteria": {
      "type": ["agent"],
      "action": ["deploy"]
    },
    "rules": [
      {
        "name": "autonomy-limit",
        "condition": "system.autonomy_level <= 3",
        "message": "Agents with autonomy > L3 require explicit approval",
        "severity": "error"
      },
      {
        "name": "recommend-hitl",
        "condition": "system.metadata.hitl_enabled == true || system.autonomy_level <= 2",
        "message": "Consider enabling HITL for production agents",
        "severity": "warning"
      }
    ]
  }'
```

---

## Get Policy

```
GET /api/v1/policies/{id}
```

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v1/policies/770e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer vp_sk_..."
```

---

## Update Policy

```
PATCH /api/v1/policies/{id}
```

### Request Body

All fields are optional.

### Example Request

```bash
curl -X PATCH "http://localhost:8000/api/v1/policies/770e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer vp_sk_..." \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": false
  }'
```

---

## Delete Policy

```
DELETE /api/v1/policies/{id}
```

### Example Request

```bash
curl -X DELETE "http://localhost:8000/api/v1/policies/770e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer vp_sk_..."
```

---

## Evaluate Policies

```
POST /api/v1/policies/evaluate
```

Evaluates all matching policies against a system action.

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `system_id` | string | Yes | System UUID to evaluate |
| `action` | string | Yes | Action being performed |
| `context` | object | No | Additional context for rules |

### Actions

| Action | Description |
|--------|-------------|
| `deploy` | Deploying to production |
| `update` | Updating deployed system |
| `delete` | Removing system |
| `approve` | Approving for deployment |
| `review` | Submitting for review |

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/policies/evaluate" \
  -H "Authorization: Bearer vp_sk_..." \
  -H "Content-Type: application/json" \
  -d '{
    "system_id": "550e8400-e29b-41d4-a716-446655440000",
    "action": "deploy",
    "context": {
      "environment": "production",
      "requested_by": "user-123"
    }
  }'
```

### Example Response

```json
{
  "allowed": false,
  "system_id": "550e8400-e29b-41d4-a716-446655440000",
  "action": "deploy",
  "policies_evaluated": 2,
  "policies_passed": 1,
  "policies_failed": 1,
  "results": [
    {
      "policy_id": "770e8400-e29b-41d4-a716-446655440000",
      "policy_name": "high-risk-deployment-gates",
      "passed": false,
      "rule_results": [
        {
          "rule_name": "require-bias-testing",
          "passed": false,
          "message": "High-risk systems require verified bias testing",
          "severity": "error"
        }
      ]
    },
    {
      "policy_id": "880e8400-e29b-41d4-a716-446655440001",
      "policy_name": "documentation-required",
      "passed": true,
      "rule_results": [
        {
          "rule_name": "has-technical-docs",
          "passed": true,
          "message": null,
          "severity": "error"
        }
      ]
    }
  ],
  "blocking_failures": [
    "High-risk systems require verified bias testing"
  ],
  "warnings": []
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `allowed` | boolean | Whether the action is permitted |
| `system_id` | string | Evaluated system |
| `action` | string | Evaluated action |
| `policies_evaluated` | integer | Number of matching policies |
| `policies_passed` | integer | Policies that passed |
| `policies_failed` | integer | Policies that failed |
| `results` | array | Detailed results per policy |
| `blocking_failures` | array | Error messages that blocked |
| `warnings` | array | Warning messages |

---

## CEL Expression Reference

Rules use CEL (Common Expression Language) for conditions.

### Available Variables

| Variable | Type | Description |
|----------|------|-------------|
| `system` | object | The AI system being evaluated |
| `system.name` | string | System name |
| `system.type` | string | System type |
| `system.risk_tier` | string | Risk tier |
| `system.status` | string | Current status |
| `system.autonomy_level` | int | Autonomy level (1-5) |
| `system.controls` | list | Assigned controls |
| `system.tags` | list | System tags |
| `system.metadata` | object | Custom metadata |
| `context` | object | Request context |

### Operators

```
==, !=, <, <=, >, >=    - Comparison
&&, ||, !               - Logical
in                      - Membership
+, -, *, /              - Arithmetic
```

### Functions

```
exists(list, predicate)  - True if any element matches
all(list, predicate)     - True if all elements match
size(list)               - List length
contains(string, sub)    - String contains
startsWith(string, pre)  - String starts with
```

### Example Conditions

```cel
# Check risk tier
system.risk_tier == "high"

# Check autonomy level
system.autonomy_level <= 3

# Check for specific control
system.controls.exists(c, c.id == "CTRL-BIAS-001")

# Check control status
system.controls.exists(c, c.id == "CTRL-BIAS-001" && c.status == "verified")

# Check metadata
system.metadata.hitl_enabled == true

# Check tags
"production" in system.tags

# Complex condition
system.risk_tier == "high" &&
system.controls.exists(c, c.id == "CTRL-ACC-001" && c.status == "verified") &&
system.controls.exists(c, c.id == "CTRL-BIAS-001" && c.status == "verified")
```

---

## Severity Levels

| Level | Effect | Use Case |
|-------|--------|----------|
| `error` | Blocks the action | Critical requirements |
| `warning` | Logs warning, allows action | Best practices |
| `info` | Informational only | Recommendations |
