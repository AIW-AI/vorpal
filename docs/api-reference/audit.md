# Audit API

The Audit API provides access to the tamper-evident audit log.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/audit` | Query audit events |
| GET | `/api/v1/audit/{id}` | Get specific event |
| GET | `/api/v1/audit/verify/chain` | Verify chain integrity |

---

## Query Audit Events

```
GET /api/v1/audit
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | integer | Page number (default: 1) |
| `page_size` | integer | Items per page (default: 50, max: 100) |
| `system_id` | string | Filter by system |
| `event_type` | string | Filter by event type |
| `actor_id` | string | Filter by actor |
| `action` | string | Filter by action |
| `resource_type` | string | Filter by resource type |
| `from` | datetime | Start time (ISO 8601) |
| `to` | datetime | End time (ISO 8601) |

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v1/audit?system_id=550e8400-e29b-41d4-a716-446655440000&from=2026-01-01T00:00:00Z" \
  -H "Authorization: Bearer vp_sk_..."
```

### Example Response

```json
{
  "data": [
    {
      "id": "990e8400-e29b-41d4-a716-446655440000",
      "system_id": "550e8400-e29b-41d4-a716-446655440000",
      "event_type": "policy.evaluated",
      "actor_id": "user-123",
      "actor_type": "user",
      "actor_name": "John Doe",
      "action": "evaluate",
      "resource_type": "policy",
      "resource_id": "770e8400-e29b-41d4-a716-446655440000",
      "details": {
        "action_evaluated": "deploy",
        "result": "blocked",
        "blocking_failures": ["High-risk systems require verified bias testing"]
      },
      "ip_address": "192.168.1.100",
      "request_id": "req_abc123",
      "previous_hash": "a1b2c3d4e5f6...",
      "event_hash": "f6e5d4c3b2a1...",
      "timestamp": "2026-01-07T14:30:00Z"
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

## Get Audit Event

```
GET /api/v1/audit/{id}
```

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Event UUID |

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v1/audit/990e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer vp_sk_..."
```

---

## Verify Chain Integrity

```
GET /api/v1/audit/verify/chain
```

Verifies that the audit log hash chain is intact.

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `system_id` | string | Filter by system (optional) |
| `from` | datetime | Start time (optional) |
| `to` | datetime | End time (optional) |

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v1/audit/verify/chain" \
  -H "Authorization: Bearer vp_sk_..."
```

### Example Response (Valid Chain)

```json
{
  "verified": true,
  "total_events": 1000,
  "valid_events": 1000,
  "invalid_events": 0,
  "first_invalid_event_id": null,
  "message": "Audit chain integrity verified"
}
```

### Example Response (Tampered Chain)

```json
{
  "verified": false,
  "total_events": 1000,
  "valid_events": 847,
  "invalid_events": 153,
  "first_invalid_event_id": "990e8400-e29b-41d4-a716-446655440500",
  "message": "Chain integrity compromised: 153 invalid events"
}
```

---

## Event Types

| Event Type | Description |
|------------|-------------|
| `system.created` | AI system registered |
| `system.updated` | AI system modified |
| `system.deleted` | AI system archived |
| `system.deployed` | AI system deployed |
| `control.assigned` | Control assigned to system |
| `control.updated` | Control status changed |
| `policy.created` | Policy created |
| `policy.updated` | Policy modified |
| `policy.deleted` | Policy deleted |
| `policy.evaluated` | Policy evaluated |
| `auth.login` | User logged in |
| `auth.logout` | User logged out |
| `auth.api_key_created` | API key created |
| `auth.api_key_revoked` | API key revoked |

---

## Actor Types

| Type | Description |
|------|-------------|
| `user` | Human user |
| `system` | System/service account |
| `api_key` | API key access |
| `agent` | AI agent |
| `scheduler` | Scheduled task |

---

## Hash Chain Integrity

### How It Works

Each audit event contains:
1. `event_hash` - SHA-256 hash of the event content
2. `previous_hash` - SHA-256 hash of the previous event

The hash is computed from:
```json
{
  "id": "event-uuid",
  "event_type": "system.created",
  "action": "create",
  "actor_id": "user-123",
  "resource_type": "ai_system",
  "resource_id": "system-456",
  "details": { ... },
  "timestamp": "2026-01-07T14:30:00Z",
  "previous_hash": "..."
}
```

### Chain Verification

```
Event 1              Event 2              Event 3
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ hash: A      │ ←── │ prev: A      │ ←── │ prev: B      │
│ prev: null   │     │ hash: B      │     │ hash: C      │
└──────────────┘     └──────────────┘     └──────────────┘
```

If any event is modified, its hash changes, breaking the chain.

### Verification Process

1. Fetch events in chronological order
2. For each event:
   - Recompute hash from content
   - Verify computed hash matches stored hash
   - Verify previous_hash matches prior event's hash
3. Report any mismatches

---

## Audit Retention

Default retention periods:

| Environment | Retention |
|-------------|-----------|
| Development | 30 days |
| Staging | 90 days |
| Production | 7 years |

Configure via `VORPAL_AUDIT_RETENTION_DAYS` environment variable.

---

## Compliance Exports

Export audit logs for compliance:

```bash
# Export to JSON
curl -X GET "http://localhost:8000/api/v1/audit?from=2026-01-01&to=2026-01-31" \
  -H "Authorization: Bearer vp_sk_..." \
  -H "Accept: application/json" \
  > audit_january_2026.json

# Export with verification
curl -X GET "http://localhost:8000/api/v1/audit/verify/chain?from=2026-01-01&to=2026-01-31" \
  -H "Authorization: Bearer vp_sk_..." \
  > audit_verification_january_2026.json
```

For PDF export (regulatory evidence), use the `vorpal-eval` component.
