"""ScamShield Pro — CLI."""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from scamshield import __version__
from scamshield.core.models import ScanRequest
from scamshield.scanner import Scanner

console = Console()


def _print_report(result, json_out: bool = False) -> None:
    if json_out:
        click.echo(result.model_dump_json(indent=2))
        return

    ts = result.trust_score
    panel = Panel.fit(
        f"[bold]{ts.verdict.emoji}  Trust Score: {ts.value}/100[/bold]\n"
        f"Verdict: [bold]{ts.verdict.value}[/bold]\n"
        f"Recommendation: {ts.verdict.recommendation}\n"
        f"Confidence: {ts.confidence}%  "
        f"(+{ts.positive_signals} positives / -{ts.negative_signals} negatives)\n\n"
        f"[dim]URL:[/dim] {result.url}\n"
        f"[dim]Domain:[/dim] {result.domain}\n"
        f"[dim]IP:[/dim] {result.ip_address or 'N/A'}  "
        f"[dim]Country:[/dim] {result.server_country or 'N/A'}  "
        f"[dim]SSL:[/dim] {'✓' if result.ssl_valid else '✗'}\n"
        f"[dim]Duration:[/dim] {result.duration_ms} ms",
        title=f"ScamShield Pro — {result.domain}",
        border_style="cyan",
    )
    console.print(panel)

    table = Table(title="Detector Results", box=box.ROUNDED, show_lines=False)
    table.add_column("#", style="dim", width=3)
    table.add_column("Check", style="bold")
    table.add_column("Result")
    table.add_column("Severity")
    table.add_column("Message", overflow="fold")

    severity_colors = {
        "critical": "bright_red",
        "high": "red",
        "medium": "yellow",
        "low": "green",
        "info": "dim",
    }
    for i, c in enumerate(result.checks, 1):
        result_str = "[green]✓ pass[/green]" if c.passed else "[red]✗ FAIL[/red]"
        severity_str = f"[{severity_colors.get(c.severity, 'white')}]{c.severity}[/{severity_colors.get(c.severity, 'white')}]"
        table.add_row(
            str(i),
            c.name,
            result_str,
            severity_str,
            c.message,
        )
    console.print(table)


@click.group()
@click.version_option(__version__, prog_name="scamshield")
def main() -> None:
    """ScamShield Pro — self-hosted URL fraud & phishing detector."""


@main.command()
@click.argument("url")
@click.option("--json", "json_out", is_flag=True, help="Output JSON instead of rich text")
@click.option("--no-content", is_flag=True, help="Skip HTML content analysis")
@click.option("--no-redirects", is_flag=True, help="Do not follow redirects")
@click.option("--timeout", type=float, default=10.0, help="Per-request timeout")
def scan(url, json_out, no_content, no_redirects, timeout):
    """Scan a single URL."""
    req = ScanRequest(
        url=url,
        follow_redirects=not no_redirects,
        fetch_content=not no_content,
        timeout=timeout,
    )
    scanner = Scanner()
    result = asyncio.run(scanner.scan(req))
    _print_report(result, json_out=json_out)


@main.command(name="scan-file")
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--json", "json_out", is_flag=True)
def scan_file(file: Path, json_out: bool):
    """Scan all URLs from a file (one per line)."""
    urls = [l.strip() for l in file.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    if not urls:
        click.echo("No URLs found in file", err=True)
        sys.exit(1)
    scanner = Scanner()
    for url in urls:
        try:
            req = ScanRequest(url=url)
            result = asyncio.run(scanner.scan(req))
            _print_report(result, json_out=json_out)
            console.print()
        except Exception as e:
            console.print(f"[red]Error scanning {url}:[/red] {e}")


@main.command()
@click.option("--host", default="0.0.0.0", show_default=True)
@click.option("--port", default=8000, show_default=True, type=int)
@click.option("--reload", is_flag=True, help="Auto-reload on file changes (dev mode)")
def serve(host, port, reload):
    """Start the FastAPI server."""
    import uvicorn

    uvicorn.run(
        "scamshield.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )


@main.command()
def version():
    """Show version."""
    click.echo(f"ScamShield Pro v{__version__}")


@main.command()
def checks():
    """List all available detectors."""
    from scamshield.checks import ALL_CHECKS

    table = Table(title="Available Detectors", box=box.ROUNDED)
    table.add_column("Name", style="bold")
    table.add_column("Severity", style="yellow")
    table.add_column("Weight", justify="right")
    table.add_column("Network")
    table.add_column("Description")

    for cls in ALL_CHECKS:
        table.add_row(
            cls.name,
            cls.severity,
            str(cls.weight),
            "yes" if cls.requires_network else "no",
            (cls.__doc__ or "").strip().split("\n")[0],
        )
    console.print(table)


if __name__ == "__main__":
    main()
