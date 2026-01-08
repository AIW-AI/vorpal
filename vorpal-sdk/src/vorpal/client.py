"""Vorpal SDK client for interacting with Vorpal Core API."""

from typing import Any

import httpx

from vorpal.types import (
    AISystem,
    Control,
    PaginatedResponse,
    PaginationMeta,
    Policy,
    PolicyEvaluationResult,
    RiskTier,
    SystemStatus,
    SystemType,
)


class VorpalError(Exception):
    """Base exception for Vorpal SDK errors."""

    def __init__(self, message: str, code: str | None = None, details: Any = None):
        super().__init__(message)
        self.code = code
        self.details = details


class VorpalNotFoundError(VorpalError):
    """Resource not found error."""

    pass


class VorpalConflictError(VorpalError):
    """Resource conflict error."""

    pass


class SystemsAPI:
    """API for managing AI systems."""

    def __init__(self, client: "VorpalClient"):
        self._client = client

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        status: SystemStatus | None = None,
        risk_tier: RiskTier | None = None,
        type: SystemType | None = None,
        team_id: str | None = None,
    ) -> tuple[list[AISystem], PaginationMeta]:
        """List AI systems with optional filtering."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if status:
            params["status"] = status.value
        if risk_tier:
            params["risk_tier"] = risk_tier.value
        if type:
            params["type"] = type.value
        if team_id:
            params["team_id"] = team_id

        response = self._client._request("GET", "/api/v1/systems", params=params)
        systems = [AISystem.model_validate(s) for s in response["data"]]
        meta = PaginationMeta.model_validate(response["meta"])
        return systems, meta

    def get(self, system_id: str) -> AISystem:
        """Get a specific AI system by ID."""
        response = self._client._request("GET", f"/api/v1/systems/{system_id}")
        return AISystem.model_validate(response)

    def create(
        self,
        name: str,
        type: SystemType,
        risk_tier: RiskTier,
        description: str | None = None,
        autonomy_level: int | None = None,
        team_id: str | None = None,
        version: str | None = None,
        metadata: dict[str, Any] | None = None,
        documentation: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> AISystem:
        """Register a new AI system."""
        payload: dict[str, Any] = {
            "name": name,
            "type": type.value,
            "risk_tier": risk_tier.value,
        }
        if description:
            payload["description"] = description
        if autonomy_level is not None:
            payload["autonomy_level"] = autonomy_level
        if team_id:
            payload["team_id"] = team_id
        if version:
            payload["version"] = version
        if metadata:
            payload["metadata"] = metadata
        if documentation:
            payload["documentation"] = documentation
        if tags:
            payload["tags"] = tags

        response = self._client._request("POST", "/api/v1/systems", json=payload)
        return AISystem.model_validate(response)

    def update(
        self,
        system_id: str,
        name: str | None = None,
        description: str | None = None,
        type: SystemType | None = None,
        status: SystemStatus | None = None,
        risk_tier: RiskTier | None = None,
        autonomy_level: int | None = None,
        version: str | None = None,
        metadata: dict[str, Any] | None = None,
        documentation: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> AISystem:
        """Update an AI system."""
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if type is not None:
            payload["type"] = type.value
        if status is not None:
            payload["status"] = status.value
        if risk_tier is not None:
            payload["risk_tier"] = risk_tier.value
        if autonomy_level is not None:
            payload["autonomy_level"] = autonomy_level
        if version is not None:
            payload["version"] = version
        if metadata is not None:
            payload["metadata"] = metadata
        if documentation is not None:
            payload["documentation"] = documentation
        if tags is not None:
            payload["tags"] = tags

        response = self._client._request("PATCH", f"/api/v1/systems/{system_id}", json=payload)
        return AISystem.model_validate(response)

    def delete(self, system_id: str) -> None:
        """Archive (soft delete) an AI system."""
        self._client._request("DELETE", f"/api/v1/systems/{system_id}")


class ControlsAPI:
    """API for managing governance controls."""

    def __init__(self, client: "VorpalClient"):
        self._client = client

    def list(
        self,
        page: int = 1,
        page_size: int = 50,
        category: str | None = None,
        regulation: str | None = None,
    ) -> tuple[list[Control], PaginationMeta]:
        """List governance controls."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if category:
            params["category"] = category
        if regulation:
            params["regulation"] = regulation

        response = self._client._request("GET", "/api/v1/controls", params=params)
        controls = [Control.model_validate(c) for c in response["data"]]
        meta = PaginationMeta.model_validate(response["meta"])
        return controls, meta

    def get(self, control_id: str) -> Control:
        """Get a specific control by ID."""
        response = self._client._request("GET", f"/api/v1/controls/{control_id}")
        return Control.model_validate(response)

    def create(
        self,
        id: str,
        name: str,
        category: str,
        description: str | None = None,
        regulation: str | None = None,
        requirement_text: str | None = None,
        test_guidance: str | None = None,
        mandatory: bool = True,
    ) -> Control:
        """Create a new governance control."""
        payload: dict[str, Any] = {
            "id": id,
            "name": name,
            "category": category,
            "mandatory": mandatory,
        }
        if description:
            payload["description"] = description
        if regulation:
            payload["regulation"] = regulation
        if requirement_text:
            payload["requirement_text"] = requirement_text
        if test_guidance:
            payload["test_guidance"] = test_guidance

        response = self._client._request("POST", "/api/v1/controls", json=payload)
        return Control.model_validate(response)


class PoliciesAPI:
    """API for managing governance policies."""

    def __init__(self, client: "VorpalClient"):
        self._client = client

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        enabled: bool | None = None,
        regulation: str | None = None,
    ) -> tuple[list[Policy], PaginationMeta]:
        """List governance policies."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if enabled is not None:
            params["enabled"] = str(enabled).lower()
        if regulation:
            params["regulation"] = regulation

        response = self._client._request("GET", "/api/v1/policies", params=params)
        policies = [Policy.model_validate(p) for p in response["data"]]
        meta = PaginationMeta.model_validate(response["meta"])
        return policies, meta

    def get(self, policy_id: str) -> Policy:
        """Get a specific policy by ID."""
        response = self._client._request("GET", f"/api/v1/policies/{policy_id}")
        return Policy.model_validate(response)

    def evaluate(
        self,
        system_id: str,
        action: str,
        context: dict[str, Any] | None = None,
    ) -> PolicyEvaluationResult:
        """Evaluate policies for a system action."""
        payload = {
            "system_id": system_id,
            "action": action,
            "context": context or {},
        }
        response = self._client._request("POST", "/api/v1/policies/evaluate", json=payload)
        return PolicyEvaluationResult.model_validate(response)


class VorpalClient:
    """Client for interacting with Vorpal Core API."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_key: str | None = None,
        timeout: float = 30.0,
    ):
        """Initialize the Vorpal client.

        Args:
            base_url: Base URL of the Vorpal Core API.
            api_key: Optional API key for authentication.
            timeout: Request timeout in seconds.
        """
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._timeout = timeout

        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=timeout,
            headers=self._get_headers(),
        )

        # API namespaces
        self.systems = SystemsAPI(self)
        self.controls = ControlsAPI(self)
        self.policies = PoliciesAPI(self)

    def _get_headers(self) -> dict[str, str]:
        """Get default headers for requests."""
        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        return headers

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Make an HTTP request to the API."""
        try:
            response = self._client.request(
                method=method,
                url=path,
                params=params,
                json=json,
            )
            response.raise_for_status()

            if response.status_code == 204:
                return None

            return response.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise VorpalNotFoundError(
                    f"Resource not found: {path}",
                    code="not_found",
                ) from e
            elif e.response.status_code == 409:
                raise VorpalConflictError(
                    "Resource conflict",
                    code="conflict",
                ) from e
            else:
                error_data = e.response.json() if e.response.content else {}
                raise VorpalError(
                    error_data.get("message", str(e)),
                    code=error_data.get("code"),
                    details=error_data.get("details"),
                ) from e

    def health(self) -> dict[str, str]:
        """Check API health."""
        return self._request("GET", "/health")

    def ready(self) -> dict[str, Any]:
        """Check API readiness."""
        return self._request("GET", "/ready")

    def close(self) -> None:
        """Close the client connection."""
        self._client.close()

    def __enter__(self) -> "VorpalClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
