"""Vorpal CLI main entry point."""

import asyncio
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="vorpal",
    help="Vorpal - AI Governance CLI",
    no_args_is_help=True,
)

console = Console()


@app.command()
def version() -> None:
    """Show version information."""
    from vorpal import __version__

    console.print(f"vorpal-core v{__version__}")


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
    reload: bool = typer.Option(False, help="Enable auto-reload"),
    workers: int = typer.Option(1, help="Number of workers"),
) -> None:
    """Start the Vorpal Core API server."""
    import uvicorn

    console.print(f"Starting Vorpal Core on {host}:{port}")

    uvicorn.run(
        "vorpal.core.api.app:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers,
    )


@app.command()
def init_db() -> None:
    """Initialize the database (create tables)."""
    from vorpal.core.db import init_db as do_init

    console.print("Initializing database...")
    asyncio.run(do_init())
    console.print("[green]Database initialized successfully[/green]")


# Systems subcommand group
systems_app = typer.Typer(help="Manage AI systems")
app.add_typer(systems_app, name="systems")


@systems_app.command("list")
def list_systems(
    api_url: str = typer.Option("http://localhost:8000", help="API base URL"),
    status: Optional[str] = typer.Option(None, help="Filter by status"),
    risk_tier: Optional[str] = typer.Option(None, help="Filter by risk tier"),
) -> None:
    """List registered AI systems."""
    import httpx

    params = {}
    if status:
        params["status"] = status
    if risk_tier:
        params["risk_tier"] = risk_tier

    try:
        response = httpx.get(f"{api_url}/api/v1/systems", params=params)
        response.raise_for_status()
        data = response.json()

        table = Table(title="AI Systems")
        table.add_column("ID", style="cyan")
        table.add_column("Name")
        table.add_column("Type")
        table.add_column("Status")
        table.add_column("Risk Tier", style="yellow")

        for system in data["data"]:
            table.add_row(
                system["id"][:8] + "...",
                system["name"],
                system["type"],
                system["status"],
                system["risk_tier"],
            )

        console.print(table)
        console.print(f"\nTotal: {data['meta']['total']} systems")

    except httpx.HTTPError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@systems_app.command("get")
def get_system(
    system_id: str = typer.Argument(..., help="System ID"),
    api_url: str = typer.Option("http://localhost:8000", help="API base URL"),
) -> None:
    """Get details of a specific AI system."""
    import httpx
    from rich.json import JSON

    try:
        response = httpx.get(f"{api_url}/api/v1/systems/{system_id}")
        response.raise_for_status()
        data = response.json()

        console.print(JSON.from_data(data))

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            console.print(f"[red]System {system_id} not found[/red]")
        else:
            console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@systems_app.command("create")
def create_system(
    name: str = typer.Argument(..., help="System name"),
    type: str = typer.Option(..., help="System type (model, application, agent, pipeline)"),
    risk_tier: str = typer.Option(..., help="Risk tier (prohibited, high, limited, minimal)"),
    description: Optional[str] = typer.Option(None, help="Description"),
    api_url: str = typer.Option("http://localhost:8000", help="API base URL"),
) -> None:
    """Register a new AI system."""
    import httpx

    payload = {
        "name": name,
        "type": type,
        "risk_tier": risk_tier,
    }
    if description:
        payload["description"] = description

    try:
        response = httpx.post(f"{api_url}/api/v1/systems", json=payload)
        response.raise_for_status()
        data = response.json()

        console.print(f"[green]Created system: {data['id']}[/green]")
        console.print(f"Name: {data['name']}")
        console.print(f"Type: {data['type']}")
        console.print(f"Risk Tier: {data['risk_tier']}")

    except httpx.HTTPError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


# Policies subcommand group
policies_app = typer.Typer(help="Manage governance policies")
app.add_typer(policies_app, name="policies")


@policies_app.command("list")
def list_policies(
    api_url: str = typer.Option("http://localhost:8000", help="API base URL"),
    enabled: Optional[bool] = typer.Option(None, help="Filter by enabled status"),
) -> None:
    """List governance policies."""
    import httpx

    params = {}
    if enabled is not None:
        params["enabled"] = str(enabled).lower()

    try:
        response = httpx.get(f"{api_url}/api/v1/policies", params=params)
        response.raise_for_status()
        data = response.json()

        table = Table(title="Policies")
        table.add_column("ID", style="cyan")
        table.add_column("Name")
        table.add_column("Enabled")
        table.add_column("Regulation")
        table.add_column("Rules")

        for policy in data["data"]:
            table.add_row(
                policy["id"][:8] + "...",
                policy["name"],
                "Yes" if policy["enabled"] else "No",
                policy.get("regulation") or "-",
                str(len(policy.get("rules", []))),
            )

        console.print(table)

    except httpx.HTTPError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@policies_app.command("evaluate")
def evaluate_policy(
    system_id: str = typer.Argument(..., help="System ID to evaluate"),
    action: str = typer.Argument(..., help="Action to evaluate (e.g., deploy)"),
    api_url: str = typer.Option("http://localhost:8000", help="API base URL"),
) -> None:
    """Evaluate policies for a system action."""
    import httpx

    payload = {
        "system_id": system_id,
        "action": action,
        "context": {},
    }

    try:
        response = httpx.post(f"{api_url}/api/v1/policies/evaluate", json=payload)
        response.raise_for_status()
        data = response.json()

        if data["allowed"]:
            console.print(f"[green]✓ Action '{action}' is ALLOWED[/green]")
        else:
            console.print(f"[red]✗ Action '{action}' is BLOCKED[/red]")

        console.print(f"\nPolicies evaluated: {data['policies_evaluated']}")
        console.print(f"Policies passed: {data['policies_passed']}")
        console.print(f"Policies failed: {data['policies_failed']}")

        if data["blocking_failures"]:
            console.print("\n[red]Blocking failures:[/red]")
            for msg in data["blocking_failures"]:
                console.print(f"  • {msg}")

        if data["warnings"]:
            console.print("\n[yellow]Warnings:[/yellow]")
            for msg in data["warnings"]:
                console.print(f"  • {msg}")

    except httpx.HTTPError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


# Audit subcommand group
audit_app = typer.Typer(help="Query audit logs")
app.add_typer(audit_app, name="audit")


@audit_app.command("list")
def list_audit(
    api_url: str = typer.Option("http://localhost:8000", help="API base URL"),
    system_id: Optional[str] = typer.Option(None, help="Filter by system ID"),
    event_type: Optional[str] = typer.Option(None, help="Filter by event type"),
    limit: int = typer.Option(20, help="Number of events to show"),
) -> None:
    """List audit events."""
    import httpx

    params = {"page_size": limit}
    if system_id:
        params["system_id"] = system_id
    if event_type:
        params["event_type"] = event_type

    try:
        response = httpx.get(f"{api_url}/api/v1/audit", params=params)
        response.raise_for_status()
        data = response.json()

        table = Table(title="Audit Events")
        table.add_column("Timestamp")
        table.add_column("Type")
        table.add_column("Action")
        table.add_column("Actor")
        table.add_column("Resource")

        for event in data["data"]:
            table.add_row(
                event["timestamp"][:19],
                event["event_type"],
                event["action"],
                event.get("actor_name") or event.get("actor_id", "-")[:8],
                f"{event.get('resource_type', '-')}/{event.get('resource_id', '-')[:8]}",
            )

        console.print(table)

    except httpx.HTTPError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@audit_app.command("verify")
def verify_audit(
    api_url: str = typer.Option("http://localhost:8000", help="API base URL"),
    system_id: Optional[str] = typer.Option(None, help="Filter by system ID"),
) -> None:
    """Verify audit chain integrity."""
    import httpx

    params = {}
    if system_id:
        params["system_id"] = system_id

    try:
        response = httpx.get(f"{api_url}/api/v1/audit/verify/chain", params=params)
        response.raise_for_status()
        data = response.json()

        if data["verified"]:
            console.print(f"[green]✓ {data['message']}[/green]")
        else:
            console.print(f"[red]✗ {data['message']}[/red]")

        console.print(f"\nTotal events: {data['total_events']}")
        console.print(f"Valid events: {data['valid_events']}")
        console.print(f"Invalid events: {data['invalid_events']}")

        if data.get("first_invalid_event_id"):
            console.print(f"\nFirst invalid event: {data['first_invalid_event_id']}")

    except httpx.HTTPError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
