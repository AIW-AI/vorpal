# Development Guide

This guide covers setting up a development environment and contributing to Vorpal.

## Development Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git
- Make (optional, for convenience commands)

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/alice-in-wonderland-ai/vorpal.git
cd vorpal

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install all packages in development mode
pip install -e "./vorpal-core[dev]"
pip install -e "./vorpal-sdk[dev]"

# Start dependencies
docker compose up -d postgres redis

# Initialize database
vorpal init-db

# Run the development server
vorpal serve --reload
```

### Verify Setup

```bash
# Check health
curl http://localhost:8000/health

# Run tests
pytest vorpal-core/tests
pytest vorpal-sdk/tests

# Run linting
ruff check .
ruff format --check .

# Run type checking
mypy vorpal-core/src
mypy vorpal-sdk/src
```

## Project Structure

```
vorpal/
├── vorpal-core/           # Main governance API
│   ├── src/vorpal/core/
│   │   ├── api/           # FastAPI routes
│   │   ├── models/        # SQLAlchemy models
│   │   ├── cli/           # CLI commands
│   │   └── ...
│   └── tests/
├── vorpal-sdk/            # Python client SDK
│   ├── src/vorpal/
│   │   ├── client.py      # API client
│   │   └── types.py       # Type definitions
│   └── tests/
├── vorpal-gateway/        # LLM proxy (planned)
├── vorpal-sentinel/       # Agent guardrails (planned)
├── vorpal-arbiter/        # MCP governance (planned)
├── vorpal-eval/           # Quality testing (planned)
├── docs/                  # Documentation
├── charts/                # Helm charts
└── examples/              # Usage examples
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow the code style guidelines (see below).

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=vorpal.core --cov-report=html

# Run specific tests
pytest vorpal-core/tests/test_api.py
pytest -k "test_create_system"
```

### 4. Run Linting

```bash
# Check for issues
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

### 5. Run Type Checking

```bash
mypy vorpal-core/src
```

### 6. Commit Changes

```bash
git add .
git commit -m "feat: add new feature"
```

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance

### 7. Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a PR on GitHub.

## Code Style

### Python

- **Formatter**: Ruff
- **Line length**: 100 characters
- **Imports**: Sorted by ruff (isort compatible)
- **Type hints**: Required for all public functions
- **Docstrings**: Google style

```python
def calculate_risk_score(
    system: AISystem,
    context: dict[str, Any],
) -> RiskScore:
    """Calculate risk score for an AI system.

    Args:
        system: The AI system to evaluate.
        context: Additional evaluation context.

    Returns:
        Calculated risk score with breakdown.

    Raises:
        ValidationError: If system data is incomplete.
    """
    ...
```

### Configuration

Linting and formatting are configured in `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]

[tool.mypy]
python_version = "3.11"
strict = true
```

## Testing

### Test Structure

```
tests/
├── __init__.py
├── conftest.py        # Shared fixtures
├── test_api.py        # API endpoint tests
├── test_models.py     # Model unit tests
├── test_policies.py   # Policy evaluation tests
└── integration/       # Integration tests
    └── test_workflow.py
```

### Writing Tests

```python
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client with test database."""
    from vorpal.core.api.app import create_app
    app = create_app()
    with TestClient(app) as client:
        yield client


class TestSystemsAPI:
    """Tests for Systems API."""

    def test_create_system(self, client):
        """Test creating a new system."""
        response = client.post(
            "/api/v1/systems",
            json={
                "name": "test-system",
                "type": "model",
                "risk_tier": "limited"
            }
        )
        assert response.status_code == 201
        assert response.json()["name"] == "test-system"

    def test_create_system_validation(self, client):
        """Test validation errors."""
        response = client.post(
            "/api/v1/systems",
            json={"name": ""}  # Invalid
        )
        assert response.status_code == 422
```

### Test Database

Tests use a separate database:

```python
# conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine

@pytest.fixture(scope="session")
def test_db():
    """Create test database."""
    engine = create_async_engine(
        "postgresql+asyncpg://vorpal:vorpal@localhost:5432/vorpal_test"
    )
    # Setup...
    yield engine
    # Teardown...
```

## Database Migrations

We use Alembic for migrations:

```bash
# Create a new migration
cd vorpal-core
alembic revision --autogenerate -m "add new field"

# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# View history
alembic history
```

### Migration Guidelines

1. Always test migrations both up and down
2. Never modify existing migrations after merge
3. Handle data migrations carefully
4. Document breaking changes

## API Development

### Adding a New Endpoint

1. **Create schema** in `api/schemas/`:

```python
# api/schemas/new_feature.py
from pydantic import BaseModel

class NewFeatureCreate(BaseModel):
    name: str
    value: int
```

2. **Create route** in `api/routes/`:

```python
# api/routes/new_feature.py
from fastapi import APIRouter

router = APIRouter()

@router.post("", response_model=NewFeatureResponse)
async def create_feature(data: NewFeatureCreate):
    ...
```

3. **Register route** in `api/app.py`:

```python
from vorpal.core.api.routes import new_feature

app.include_router(
    new_feature.router,
    prefix="/api/v1/features",
    tags=["Features"]
)
```

4. **Add tests** in `tests/`:

```python
def test_create_feature(client):
    response = client.post("/api/v1/features", json={...})
    assert response.status_code == 201
```

## Documentation

### Building Docs

```bash
# Install docs dependencies
pip install mkdocs mkdocs-material

# Serve locally
mkdocs serve

# Build static site
mkdocs build
```

### Documentation Style

- Use clear, concise language
- Include code examples
- Keep examples runnable
- Update docs with code changes

## Debugging

### Local Debugging

```python
# Enable debug mode
VORPAL_DEBUG=true vorpal serve --reload

# Use debugger
import pdb; pdb.set_trace()

# Or with VS Code
# Add breakpoints and use "Python: Attach" configuration
```

### Logging

```python
import structlog

logger = structlog.get_logger()

logger.info("Processing request", system_id=system.id)
logger.error("Failed to evaluate", error=str(e))
```

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create PR with changes
4. After merge, tag release:

```bash
git tag v0.1.0
git push origin v0.1.0
```

5. GitHub Actions will:
   - Run tests
   - Build Docker images
   - Publish to PyPI
   - Create GitHub release

## Getting Help

- **Discord**: Join #vorpal-dev
- **GitHub Issues**: Bug reports and features
- **GitHub Discussions**: Questions and ideas
