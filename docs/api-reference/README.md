# API Reference

Vorpal Core provides a REST API for all governance operations.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API endpoints (except health checks) require authentication.

### API Key Authentication

Include the API key in the `Authorization` header:

```bash
curl -H "Authorization: Bearer vp_sk_your_api_key" \
  http://localhost:8000/api/v1/systems
```

### JWT Authentication

For user sessions, use JWT tokens:

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  http://localhost:8000/api/v1/systems
```

## Response Format

### Success Response

```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### Error Response

```json
{
  "code": "not_found",
  "message": "System abc123 not found",
  "details": [
    {
      "field": "system_id",
      "message": "Invalid UUID format"
    }
  ],
  "request_id": "req_xyz789"
}
```

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (successful delete) |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict (duplicate resource) |
| 429 | Rate Limited |
| 500 | Internal Server Error |

## Rate Limiting

Default limits:
- 1000 requests per minute per IP
- 100 requests per minute per API key

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1704067200
```

## API Endpoints

- [Systems API](./systems.md) - Manage AI systems
- [Controls API](./controls.md) - Governance controls
- [Policies API](./policies.md) - Policy management and evaluation
- [Audit API](./audit.md) - Audit log queries
- [Configuration](./configuration.md) - Server configuration

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
