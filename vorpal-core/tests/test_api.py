"""Tests for vorpal-core API."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client."""
    from vorpal.core.api.app import create_app

    app = create_app()
    with TestClient(app) as client:
        yield client


def test_health_endpoint(client):
    """Test health endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint(client):
    """Test root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert data["name"] == "Vorpal Core"
    assert "version" in data
    assert "docs" in data


def test_openapi_available(client):
    """Test OpenAPI schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema


class TestSystemsAPI:
    """Tests for Systems API endpoints."""

    def test_list_systems_empty(self, client):
        """Test listing systems when none exist."""
        response = client.get("/api/v1/systems")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "meta" in data
        assert isinstance(data["data"], list)


class TestControlsAPI:
    """Tests for Controls API endpoints."""

    def test_list_controls_empty(self, client):
        """Test listing controls when none exist."""
        response = client.get("/api/v1/controls")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)


class TestPoliciesAPI:
    """Tests for Policies API endpoints."""

    def test_list_policies_empty(self, client):
        """Test listing policies when none exist."""
        response = client.get("/api/v1/policies")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
