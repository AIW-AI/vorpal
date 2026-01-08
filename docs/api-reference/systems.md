# Systems API

The Systems API manages the AI system registry.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/systems` | List systems |
| POST | `/api/v1/systems` | Create system |
| GET | `/api/v1/systems/{id}` | Get system |
| PATCH | `/api/v1/systems/{id}` | Update system |
| DELETE | `/api/v1/systems/{id}` | Archive system |
| GET | `/api/v1/systems/{id}/controls` | List system controls |
| POST | `/api/v1/systems/{id}/controls` | Assign control |

---

## List Systems

```
GET /api/v1/systems
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | integer | Page number (default: 1) |
| `page_size` | integer | Items per page (default: 20, max: 100) |
| `status` | string | Filter by status |
| `risk_tier` | string | Filter by risk tier |
| `type` | string | Filter by system type |
| `team_id` | string | Filter by team |

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v1/systems?risk_tier=high&status=deployed" \
  -H "Authorization: Bearer vp_sk_..."
```

### Example Response

```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "customer-service-agent",
      "description": "Customer service chatbot",
      "type": "agent",
      "status": "deployed",
      "risk_tier": "limited",
      "autonomy_level": 3,
      "owner_id": "user-123",
      "team_id": "team-456",
      "version": "1.2.0",
      "metadata": {
        "model": "gpt-4o",
        "deployment": "production"
      },
      "documentation": {
        "technical_doc": "https://docs.example.com/agent",
        "risk_assessment": "https://docs.example.com/risk"
      },
      "tags": ["production", "customer-facing"],
      "created_at": "2026-01-07T10:00:00Z",
      "updated_at": "2026-01-07T12:00:00Z"
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

## Create System

```
POST /api/v1/systems
```

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | System name (1-255 chars) |
| `type` | string | Yes | `model`, `application`, `agent`, `pipeline` |
| `risk_tier` | string | Yes | `prohibited`, `high`, `limited`, `minimal` |
| `description` | string | No | System description |
| `autonomy_level` | integer | No | 1-5, required for agents |
| `team_id` | string | No | Owning team ID |
| `version` | string | No | System version |
| `metadata` | object | No | Custom metadata |
| `documentation` | object | No | Documentation links |
| `tags` | array | No | Categorization tags |

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/systems" \
  -H "Authorization: Bearer vp_sk_..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "fraud-detection-model",
    "type": "model",
    "risk_tier": "high",
    "description": "ML model for detecting fraudulent transactions",
    "metadata": {
      "framework": "scikit-learn",
      "training_date": "2026-01-01"
    },
    "tags": ["ml", "fraud", "financial"]
  }'
```

### Example Response

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "name": "fraud-detection-model",
  "description": "ML model for detecting fraudulent transactions",
  "type": "model",
  "status": "draft",
  "risk_tier": "high",
  "autonomy_level": null,
  "owner_id": "user-123",
  "team_id": null,
  "version": null,
  "metadata": {
    "framework": "scikit-learn",
    "training_date": "2026-01-01"
  },
  "documentation": {},
  "tags": ["ml", "fraud", "financial"],
  "created_at": "2026-01-07T14:00:00Z",
  "updated_at": "2026-01-07T14:00:00Z"
}
```

---

## Get System

```
GET /api/v1/systems/{id}
```

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | System UUID |

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v1/systems/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer vp_sk_..."
```

### Errors

| Code | Description |
|------|-------------|
| 404 | System not found |

---

## Update System

```
PATCH /api/v1/systems/{id}
```

### Request Body

All fields are optional. Only provided fields are updated.

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | System name |
| `description` | string | System description |
| `type` | string | System type |
| `status` | string | `draft`, `review`, `approved`, `deployed`, `deprecated` |
| `risk_tier` | string | Risk tier |
| `autonomy_level` | integer | Autonomy level (1-5) |
| `version` | string | System version |
| `metadata` | object | Custom metadata |
| `documentation` | object | Documentation links |
| `tags` | array | Categorization tags |
| `team_id` | string | Owning team ID |

### Example Request

```bash
curl -X PATCH "http://localhost:8000/api/v1/systems/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer vp_sk_..." \
  -H "Content-Type: application/json" \
  -d '{
    "status": "deployed",
    "version": "1.3.0"
  }'
```

---

## Archive System

```
DELETE /api/v1/systems/{id}
```

Soft deletes a system by setting its status to `deprecated`.

### Example Request

```bash
curl -X DELETE "http://localhost:8000/api/v1/systems/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer vp_sk_..."
```

### Response

```
HTTP 204 No Content
```

---

## List System Controls

```
GET /api/v1/systems/{id}/controls
```

Lists all controls assigned to a system.

### Example Response

```json
[
  {
    "system_id": "550e8400-e29b-41d4-a716-446655440000",
    "control_id": "CTRL-BIAS-001",
    "status": "verified",
    "evidence_required": true,
    "notes": "Bias audit completed 2026-01-05",
    "last_updated_by": "user-123",
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-05T00:00:00Z",
    "control": {
      "id": "CTRL-BIAS-001",
      "name": "Bias Testing Required",
      "category": "bias",
      "regulation": "NYC-LL-144"
    }
  }
]
```

---

## Assign Control

```
POST /api/v1/systems/{id}/controls
```

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `control_id` | string | Yes | Control ID (e.g., `CTRL-BIAS-001`) |
| `evidence_required` | boolean | No | Whether evidence is needed (default: true) |
| `notes` | string | No | Implementation notes |

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/systems/550e8400-e29b-41d4-a716-446655440000/controls" \
  -H "Authorization: Bearer vp_sk_..." \
  -H "Content-Type: application/json" \
  -d '{
    "control_id": "CTRL-ACC-001",
    "notes": "Accuracy testing required before deployment"
  }'
```

---

## Data Types

### SystemType

```
model        - ML models
application  - AI-powered applications
agent        - Autonomous agents
pipeline     - Processing pipelines
```

### SystemStatus

```
draft       - Initial registration
review      - Under review
approved    - Approved for deployment
deployed    - Currently deployed
deprecated  - Archived/retired
```

### RiskTier

Based on EU AI Act classification:

```
prohibited  - Banned use cases
high        - Requires strict controls
limited     - Requires transparency
minimal     - No special requirements
```

### AutonomyLevel

For agents only:

```
1 - Informational (read-only)
2 - Constrained (safe zones only)
3 - Supervised (configurable HITL)
4 - Delegated (HITL for irreversible)
5 - Autonomous (full operation)
```
