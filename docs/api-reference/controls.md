# Controls API

The Controls API manages governance control definitions.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/controls` | List controls |
| POST | `/api/v1/controls` | Create control |
| GET | `/api/v1/controls/{id}` | Get control |
| PATCH | `/api/v1/controls/{id}` | Update control |
| DELETE | `/api/v1/controls/{id}` | Delete control |

---

## List Controls

```
GET /api/v1/controls
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | integer | Page number (default: 1) |
| `page_size` | integer | Items per page (default: 50, max: 100) |
| `category` | string | Filter by category |
| `regulation` | string | Filter by regulation |

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v1/controls?category=bias&regulation=NYC-LL-144" \
  -H "Authorization: Bearer vp_sk_..."
```

### Example Response

```json
{
  "data": [
    {
      "id": "CTRL-BIAS-001",
      "name": "Annual Bias Audit",
      "description": "Automated employment decision tools require annual bias audits",
      "category": "bias",
      "regulation": "NYC-LL-144",
      "requirement_text": "Employers using AEDT must conduct an annual bias audit...",
      "test_guidance": "Calculate selection rates and impact ratios...",
      "mandatory": true,
      "applies_to_risk_tiers": "high,limited",
      "created_at": "2026-01-01T00:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 50,
    "total": 1,
    "total_pages": 1
  }
}
```

---

## Create Control

```
POST /api/v1/controls
```

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Control ID (pattern: `CTRL-{CATEGORY}-{NUMBER}`) |
| `name` | string | Yes | Control name |
| `category` | string | Yes | Control category |
| `description` | string | No | Detailed description |
| `regulation` | string | No | Source regulation |
| `requirement_text` | string | No | Full requirement text |
| `test_guidance` | string | No | Testing instructions |
| `mandatory` | boolean | No | Is control mandatory (default: true) |
| `applies_to_risk_tiers` | string | No | Comma-separated tiers |

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/controls" \
  -H "Authorization: Bearer vp_sk_..." \
  -H "Content-Type: application/json" \
  -d '{
    "id": "CTRL-ACC-001",
    "name": "Model Accuracy Threshold",
    "category": "accuracy",
    "regulation": "EU-AI-ACT",
    "requirement_text": "High-risk AI systems shall achieve accuracy appropriate to their intended purpose",
    "test_guidance": "Run evaluation suite on held-out test set. Accuracy must exceed 95% for production deployment.",
    "mandatory": true,
    "applies_to_risk_tiers": "high"
  }'
```

### Control ID Format

Control IDs follow the pattern `CTRL-{CATEGORY}-{NUMBER}`:

- `CTRL-ACC-001` - Accuracy control #1
- `CTRL-BIAS-001` - Bias control #1
- `CTRL-SEC-001` - Security control #1

---

## Get Control

```
GET /api/v1/controls/{id}
```

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Control ID |

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v1/controls/CTRL-BIAS-001" \
  -H "Authorization: Bearer vp_sk_..."
```

---

## Update Control

```
PATCH /api/v1/controls/{id}
```

### Request Body

All fields are optional.

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Control name |
| `description` | string | Detailed description |
| `requirement_text` | string | Full requirement text |
| `test_guidance` | string | Testing instructions |
| `mandatory` | boolean | Is control mandatory |
| `applies_to_risk_tiers` | string | Comma-separated tiers |

### Example Request

```bash
curl -X PATCH "http://localhost:8000/api/v1/controls/CTRL-ACC-001" \
  -H "Authorization: Bearer vp_sk_..." \
  -H "Content-Type: application/json" \
  -d '{
    "test_guidance": "Updated testing procedure..."
  }'
```

---

## Delete Control

```
DELETE /api/v1/controls/{id}
```

**Note**: Controls with system assignments cannot be deleted.

### Example Request

```bash
curl -X DELETE "http://localhost:8000/api/v1/controls/CTRL-ACC-001" \
  -H "Authorization: Bearer vp_sk_..."
```

---

## Data Types

### ControlCategory

```
accuracy       - Model accuracy and performance
bias           - Fairness and bias testing
security       - Security controls
privacy        - Data privacy controls
safety         - Safety guidelines
transparency   - Explainability and disclosure
robustness     - System reliability
accountability - Governance and oversight
```

### ControlStatus (for SystemControl)

```
pending         - Not yet implemented
implemented     - Implementation complete
tested          - Testing complete
verified        - Independently verified
failed          - Failed verification
not_applicable  - Control doesn't apply
```

---

## Pre-built Controls

Vorpal includes pre-built controls for common regulations:

### EU AI Act Controls

| ID | Name | Category |
|----|------|----------|
| `CTRL-EUAI-001` | Risk Management System | accountability |
| `CTRL-EUAI-002` | Data Governance | privacy |
| `CTRL-EUAI-003` | Technical Documentation | transparency |
| `CTRL-EUAI-004` | Record-Keeping | accountability |
| `CTRL-EUAI-005` | Transparency | transparency |
| `CTRL-EUAI-006` | Human Oversight | safety |
| `CTRL-EUAI-007` | Accuracy & Robustness | accuracy |

### NYC Local Law 144 Controls

| ID | Name | Category |
|----|------|----------|
| `CTRL-LL144-001` | Annual Bias Audit | bias |
| `CTRL-LL144-002` | Candidate Disclosure | transparency |
| `CTRL-LL144-003` | Independent Auditor | accountability |

### NIST AI RMF Controls

| ID | Name | Category |
|----|------|----------|
| `CTRL-NIST-001` | AI Impact Assessment | accountability |
| `CTRL-NIST-002` | Continuous Monitoring | accuracy |
| `CTRL-NIST-003` | Incident Response | security |

See [Regulatory Packs](../regulatory-packs/) for complete control definitions.
