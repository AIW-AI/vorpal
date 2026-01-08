# Contributing to Vorpal

Thank you for your interest in contributing to Vorpal! This document provides guidelines and information for contributors.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code.

## Getting Started

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/vorpal.git
   cd vorpal
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e "./vorpal-core[dev]"
   pip install -e "./vorpal-sdk[dev]"
   ```

4. **Start local services**
   ```bash
   docker compose up -d postgres redis
   ```

5. **Run migrations**
   ```bash
   cd vorpal-core
   alembic upgrade head
   ```

6. **Run tests**
   ```bash
   pytest
   ```

### Project Structure

```
vorpal/
├── vorpal-core/      # Registry, policy engine, audit
├── vorpal-gateway/   # LLM proxy
├── vorpal-sentinel/  # Agent guardrails
├── vorpal-arbiter/   # MCP/tool governance
├── vorpal-eval/      # Quality evaluation
├── vorpal-sdk/       # Shared Python SDK
├── vorpal-dashboard/ # Web UI
├── charts/           # Helm charts
├── docs/             # Documentation
└── examples/         # Usage examples
```

## How to Contribute

### Reporting Bugs

- Search existing issues first to avoid duplicates
- Use the bug report template
- Include:
  - Vorpal version
  - Python version
  - Operating system
  - Steps to reproduce
  - Expected vs actual behavior
  - Error messages/stack traces

### Suggesting Features

- Open an issue with the feature request template
- Describe the use case and motivation
- Consider how it fits with existing architecture

### Pull Requests

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the code style guidelines below
   - Add tests for new functionality
   - Update documentation as needed

3. **Run checks locally**
   ```bash
   # Linting
   ruff check .
   ruff format --check .

   # Type checking
   mypy vorpal-core/src vorpal-sdk/src

   # Tests
   pytest
   ```

4. **Commit your changes**
   ```bash
   git commit -m "feat: add new feature description"
   ```

   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation only
   - `style:` Code style (formatting, etc.)
   - `refactor:` Code change that neither fixes nor adds
   - `test:` Adding tests
   - `chore:` Maintenance tasks

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

   Then open a pull request on GitHub.

## Code Style Guidelines

### Python

- **Formatter**: Ruff (configured in `pyproject.toml`)
- **Linter**: Ruff
- **Type checking**: mypy with strict mode
- **Docstrings**: Google style
- **Line length**: 100 characters

```python
def calculate_risk_score(
    system: AISystem,
    context: EvaluationContext,
) -> RiskScore:
    """Calculate risk score for an AI system.

    Args:
        system: The AI system to evaluate.
        context: Additional context for evaluation.

    Returns:
        Calculated risk score with breakdown.

    Raises:
        ValidationError: If system data is incomplete.
    """
    ...
```

### API Design

- REST endpoints follow `/api/v1/resource` pattern
- Use plural nouns for resources (`/systems`, `/policies`)
- HTTP methods: GET (read), POST (create), PATCH (update), DELETE (remove)
- Return JSON with consistent structure:
  ```json
  {
    "data": { ... },
    "meta": { "page": 1, "total": 100 }
  }
  ```
- Errors include `code`, `message`, `details`

### Testing

- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`
- Use pytest fixtures for common setup
- Aim for >80% coverage on new code
- Mock external services

```python
@pytest.fixture
def sample_system(db_session):
    """Create a sample AI system for testing."""
    system = AISystem(
        name="test-agent",
        type=SystemType.AGENT,
        risk_tier=RiskTier.LIMITED,
    )
    db_session.add(system)
    db_session.commit()
    return system


def test_system_creation(client, sample_system):
    """Test that systems can be retrieved."""
    response = client.get(f"/api/v1/systems/{sample_system.id}")
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "test-agent"
```

## Component-Specific Guidelines

### vorpal-core

- Database migrations use Alembic
- All changes to models require migrations
- Audit events must be immutable

### vorpal-gateway

- LLM provider adapters implement `BaseLLMProvider`
- DLP rules are configurable via YAML
- Rate limiting uses Redis

### vorpal-sentinel

- Agent adapters implement `BaseAgentAdapter`
- HITL flows must have timeout handling
- Kill switch must be sub-second latency

### vorpal-arbiter

- MCP transport handlers implement `BaseTransport`
- Permission rules support regex patterns
- Budget tracking is eventually consistent

### vorpal-eval

- Metrics implement `BaseMetric` interface
- LLM judges are configurable
- Evidence export supports PDF and JSON

## Documentation

- API documentation is auto-generated from OpenAPI specs
- User guides go in `docs/`
- Code comments explain "why", not "what"
- Update README if adding major features

## Release Process

1. Version bumps follow [Semantic Versioning](https://semver.org/)
2. Changelog is maintained in `CHANGELOG.md`
3. Releases are tagged as `v1.2.3`
4. Docker images are published to `ghcr.io`
5. Python packages are published to PyPI

## Getting Help

- **Discord**: [Join our community](https://discord.gg/vorpal)
- **GitHub Discussions**: For questions and ideas
- **Issues**: For bugs and feature requests

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
