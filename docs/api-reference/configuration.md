# Configuration Reference

Vorpal is configured via environment variables. All variables use the `VORPAL_` prefix.

## Configuration Methods

### Environment Variables

```bash
export VORPAL_DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/vorpal
export VORPAL_SECRET_KEY=your-secret-key
```

### .env File

Create a `.env` file in the project root:

```bash
VORPAL_DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/vorpal
VORPAL_SECRET_KEY=your-secret-key
```

### Docker Compose

```yaml
services:
  vorpal-core:
    environment:
      VORPAL_DATABASE_URL: postgresql+asyncpg://user:pass@host:5432/vorpal
      VORPAL_SECRET_KEY: your-secret-key
```

---

## Application Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VORPAL_APP_NAME` | string | `vorpal-core` | Application name |
| `VORPAL_APP_VERSION` | string | `0.1.0` | Application version |
| `VORPAL_DEBUG` | boolean | `false` | Enable debug mode |
| `VORPAL_ENVIRONMENT` | string | `development` | Environment: `development`, `staging`, `production` |

---

## Server Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VORPAL_HOST` | string | `0.0.0.0` | Server bind address |
| `VORPAL_PORT` | integer | `8000` | Server port |
| `VORPAL_WORKERS` | integer | `1` | Number of worker processes |

### Example

```bash
VORPAL_HOST=0.0.0.0
VORPAL_PORT=8000
VORPAL_WORKERS=4
```

---

## Database Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VORPAL_DATABASE_URL` | string | `postgresql+asyncpg://vorpal:vorpal@localhost:5432/vorpal` | PostgreSQL connection URL |
| `VORPAL_DATABASE_POOL_SIZE` | integer | `5` | Connection pool size |
| `VORPAL_DATABASE_MAX_OVERFLOW` | integer | `10` | Max overflow connections |

### Connection URL Format

```
postgresql+asyncpg://username:password@host:port/database
```

**Important**: The URL must use the `postgresql+asyncpg://` scheme for async support.

### Example

```bash
# Local development
VORPAL_DATABASE_URL=postgresql+asyncpg://vorpal:vorpal@localhost:5432/vorpal

# Production with SSL
VORPAL_DATABASE_URL=postgresql+asyncpg://user:pass@db.example.com:5432/vorpal?ssl=require
```

---

## Redis Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VORPAL_REDIS_URL` | string | `None` | Redis connection URL (optional) |

Redis is used for:
- Rate limiting
- Caching
- Session storage

### Example

```bash
# Local
VORPAL_REDIS_URL=redis://localhost:6379/0

# With password
VORPAL_REDIS_URL=redis://:password@localhost:6379/0

# Cluster
VORPAL_REDIS_URL=redis://node1:6379,node2:6379,node3:6379/0
```

---

## Authentication Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VORPAL_SECRET_KEY` | string | `change-me-in-production` | JWT signing key |
| `VORPAL_ALGORITHM` | string | `HS256` | JWT algorithm |
| `VORPAL_ACCESS_TOKEN_EXPIRE_MINUTES` | integer | `30` | Token expiration |
| `VORPAL_API_KEY_PREFIX` | string | `vp_sk_` | API key prefix |

### Security Warning

**Never use the default `SECRET_KEY` in production!**

Generate a secure key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Example

```bash
VORPAL_SECRET_KEY=your-32-byte-secret-key-here
VORPAL_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## CORS Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VORPAL_CORS_ORIGINS` | list | `["*"]` | Allowed origins |

### Example

```bash
# Development (allow all)
VORPAL_CORS_ORIGINS=*

# Production (specific origins)
VORPAL_CORS_ORIGINS=https://dashboard.vorpal.dev,https://app.example.com
```

---

## Logging Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VORPAL_LOG_LEVEL` | string | `INFO` | Log level |
| `VORPAL_LOG_FORMAT` | string | `console` | Format: `console` or `json` |

### Log Levels

```
DEBUG    - Detailed debugging information
INFO     - General operational messages
WARNING  - Warning messages
ERROR    - Error messages
CRITICAL - Critical failures
```

### Example

```bash
# Development
VORPAL_LOG_LEVEL=DEBUG
VORPAL_LOG_FORMAT=console

# Production
VORPAL_LOG_LEVEL=INFO
VORPAL_LOG_FORMAT=json
```

---

## OpenTelemetry Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VORPAL_OTEL_ENABLED` | boolean | `false` | Enable OpenTelemetry |
| `VORPAL_OTEL_SERVICE_NAME` | string | `vorpal-core` | Service name |
| `VORPAL_OTEL_EXPORTER_ENDPOINT` | string | `None` | OTLP exporter endpoint |

### Example

```bash
VORPAL_OTEL_ENABLED=true
VORPAL_OTEL_SERVICE_NAME=vorpal-core-production
VORPAL_OTEL_EXPORTER_ENDPOINT=http://otel-collector:4317
```

---

## Rate Limiting Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VORPAL_RATE_LIMIT_REQUESTS_PER_MINUTE` | integer | `1000` | Global rate limit |
| `VORPAL_RATE_LIMIT_PER_API_KEY` | integer | `100` | Per-key rate limit |

---

## Audit Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VORPAL_AUDIT_RETENTION_DAYS` | integer | `2555` | Audit log retention (7 years) |
| `VORPAL_AUDIT_BATCH_SIZE` | integer | `100` | Batch size for writes |

---

## Complete Example

### Development (.env)

```bash
# Application
VORPAL_DEBUG=true
VORPAL_ENVIRONMENT=development
VORPAL_LOG_LEVEL=DEBUG

# Server
VORPAL_HOST=0.0.0.0
VORPAL_PORT=8000
VORPAL_WORKERS=1

# Database
VORPAL_DATABASE_URL=postgresql+asyncpg://vorpal:vorpal@localhost:5432/vorpal

# Redis
VORPAL_REDIS_URL=redis://localhost:6379/0

# Auth
VORPAL_SECRET_KEY=dev-secret-key-not-for-production

# CORS
VORPAL_CORS_ORIGINS=*
```

### Production (.env)

```bash
# Application
VORPAL_DEBUG=false
VORPAL_ENVIRONMENT=production
VORPAL_LOG_LEVEL=INFO
VORPAL_LOG_FORMAT=json

# Server
VORPAL_HOST=0.0.0.0
VORPAL_PORT=8000
VORPAL_WORKERS=4

# Database
VORPAL_DATABASE_URL=postgresql+asyncpg://vorpal:${DB_PASSWORD}@db.internal:5432/vorpal?ssl=require
VORPAL_DATABASE_POOL_SIZE=10
VORPAL_DATABASE_MAX_OVERFLOW=20

# Redis
VORPAL_REDIS_URL=redis://:${REDIS_PASSWORD}@redis.internal:6379/0

# Auth
VORPAL_SECRET_KEY=${JWT_SECRET_KEY}
VORPAL_ACCESS_TOKEN_EXPIRE_MINUTES=15

# CORS
VORPAL_CORS_ORIGINS=https://dashboard.vorpal.dev

# Observability
VORPAL_OTEL_ENABLED=true
VORPAL_OTEL_SERVICE_NAME=vorpal-core-production
VORPAL_OTEL_EXPORTER_ENDPOINT=http://otel-collector:4317

# Rate Limiting
VORPAL_RATE_LIMIT_REQUESTS_PER_MINUTE=5000
```

---

## Kubernetes ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: vorpal-config
data:
  VORPAL_ENVIRONMENT: "production"
  VORPAL_LOG_LEVEL: "INFO"
  VORPAL_LOG_FORMAT: "json"
  VORPAL_HOST: "0.0.0.0"
  VORPAL_PORT: "8000"
  VORPAL_WORKERS: "4"
  VORPAL_DATABASE_POOL_SIZE: "10"
  VORPAL_OTEL_ENABLED: "true"
  VORPAL_OTEL_SERVICE_NAME: "vorpal-core"
```

### Kubernetes Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: vorpal-secrets
type: Opaque
stringData:
  VORPAL_DATABASE_URL: postgresql+asyncpg://user:pass@db:5432/vorpal
  VORPAL_SECRET_KEY: your-production-secret-key
  VORPAL_REDIS_URL: redis://:password@redis:6379/0
```
