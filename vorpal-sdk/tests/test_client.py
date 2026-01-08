"""Tests for vorpal-sdk client."""

import pytest
import respx
from httpx import Response

from vorpal import VorpalClient
from vorpal.types import RiskTier, SystemStatus, SystemType


@pytest.fixture
def client():
    """Create test client."""
    return VorpalClient(base_url="http://test-api")


class TestVorpalClient:
    """Tests for VorpalClient."""

    @respx.mock
    def test_health_check(self, client):
        """Test health check endpoint."""
        respx.get("http://test-api/health").mock(
            return_value=Response(200, json={"status": "healthy"})
        )

        result = client.health()
        assert result["status"] == "healthy"

    @respx.mock
    def test_ready_check(self, client):
        """Test readiness check endpoint."""
        respx.get("http://test-api/ready").mock(
            return_value=Response(
                200,
                json={
                    "status": "ready",
                    "version": "0.1.0",
                    "checks": {"database": "connected"},
                },
            )
        )

        result = client.ready()
        assert result["status"] == "ready"


class TestSystemsAPI:
    """Tests for Systems API."""

    @respx.mock
    def test_list_systems(self, client):
        """Test listing systems."""
        respx.get("http://test-api/api/v1/systems").mock(
            return_value=Response(
                200,
                json={
                    "data": [
                        {
                            "id": "test-id",
                            "name": "Test System",
                            "description": None,
                            "type": "agent",
                            "status": "draft",
                            "risk_tier": "limited",
                            "autonomy_level": 3,
                            "owner_id": "owner-id",
                            "team_id": None,
                            "version": None,
                            "metadata": {},
                            "documentation": {},
                            "tags": [],
                            "created_at": "2026-01-07T00:00:00Z",
                            "updated_at": "2026-01-07T00:00:00Z",
                        }
                    ],
                    "meta": {
                        "page": 1,
                        "page_size": 20,
                        "total": 1,
                        "total_pages": 1,
                    },
                },
            )
        )

        systems, meta = client.systems.list()
        assert len(systems) == 1
        assert systems[0].name == "Test System"
        assert systems[0].type == SystemType.AGENT
        assert meta.total == 1

    @respx.mock
    def test_create_system(self, client):
        """Test creating a system."""
        respx.post("http://test-api/api/v1/systems").mock(
            return_value=Response(
                201,
                json={
                    "id": "new-id",
                    "name": "New System",
                    "description": None,
                    "type": "model",
                    "status": "draft",
                    "risk_tier": "high",
                    "autonomy_level": None,
                    "owner_id": "owner-id",
                    "team_id": None,
                    "version": None,
                    "metadata": {},
                    "documentation": {},
                    "tags": [],
                    "created_at": "2026-01-07T00:00:00Z",
                    "updated_at": "2026-01-07T00:00:00Z",
                },
            )
        )

        system = client.systems.create(
            name="New System",
            type=SystemType.MODEL,
            risk_tier=RiskTier.HIGH,
        )
        assert system.id == "new-id"
        assert system.name == "New System"
        assert system.risk_tier == RiskTier.HIGH


class TestPoliciesAPI:
    """Tests for Policies API."""

    @respx.mock
    def test_evaluate_policies(self, client):
        """Test policy evaluation."""
        respx.post("http://test-api/api/v1/policies/evaluate").mock(
            return_value=Response(
                200,
                json={
                    "allowed": True,
                    "system_id": "test-id",
                    "action": "deploy",
                    "policies_evaluated": 2,
                    "policies_passed": 2,
                    "policies_failed": 0,
                    "results": [],
                    "blocking_failures": [],
                    "warnings": [],
                },
            )
        )

        result = client.policies.evaluate(
            system_id="test-id",
            action="deploy",
        )
        assert result.allowed is True
        assert result.policies_evaluated == 2
        assert result.policies_failed == 0
