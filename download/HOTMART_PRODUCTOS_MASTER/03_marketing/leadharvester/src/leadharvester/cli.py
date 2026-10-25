"""LeadHarvester — CLI."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
import click
from rich.console import Console
from rich.table import Table
from rich import box

from leadharvester import __version__
from leadharvester.core.config import get_settings
from leadharvester.core.models import ScrapeRequest, LeadList
from leadharvester.scrapers import scrape
from leadharvester.export import to_csv, to_json, to_excel

console = Console()


@click.group()
@click.version_option(__version__, prog_name="leadharvester")
def main():
    """LeadHarvester — Instagram lead scraper."""


@main.command()
def version():
    click.echo(f"LeadHarvester v{__version__}")


@main.command()
@click.argument("target")
@click.option("--type", "target_type", default="username", type=click.Choice(["username", "hashtag", "followers_of"]))
@click.option("--max", "max_results", default=50, type=int, help="Max results")
@click.option("--no-contact", is_flag=True, help="Skip contact extraction")
@click.option("--only-business", is_flag=True)
@click.option("--format", "fmt", default="csv", type=click.Choice(["csv", "json", "excel"]))
@click.option("-o", "--out", type=click.Path(), default="leads", help="Output prefix")
def scrape_cmd(target, target_type, max_results, no_contact, only_business, fmt, out):
    """Scrape leads from a target (username, hashtag, or followers_of)."""
    req = ScrapeRequest(
        target=target,
        target_type=target_type,
        max_results=max_results,
        extract_contact=not no_contact,
        only_business=only_business,
    )
    console.print(f"[cyan]Scraping[/cyan] {target_type}={target} (max {max_results}) ...")
    leads = asyncio.run(scrape(req))

    if not leads:
        console.print("[yellow]No leads found[/yellow]")
        return

    lead_list = LeadList(name=out, query=target, leads=leads)

    table = Table(title=f"Leads ({lead_list.count})", box=box.ROUNDED)
    table.add_column("Username", style="bold")
    table.add_column("Followers", justify="right")
    table.add_column("Email")
    table.add_column("Business")
    table.add_column("Category")
    for l in leads[:20]:
        table.add_row(
            l.username,
            str(l.followers),
            l.email or "[dim]-[/dim]",
            "✓" if l.is_business else "",
            l.category,
        )
    console.print(table)

    # Export
    if fmt == "csv":
        path = to_csv(lead_list, f"{out}.csv")
    elif fmt == "json":
        path = to_json(lead_list, f"{out}.json")
    else:
        path = to_excel(lead_list, f"{out}.xlsx")
    console.print(f"\n[green]✓ Exported to {path}[/green]")
    console.print(f"  Total: {lead_list.count} leads")
    console.print(f"  With email: {lead_list.with_email}")
    console.print(f"  Business: {lead_list.business_count}")


@main.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8002, type=int)
@click.option("--reload", is_flag=True)
def serve(host, port, reload):
    """Start FastAPI server."""
    import uvicorn
    uvicorn.run("leadharvester.server:app", host=host, port=port, reload=reload)


@main.command()
def config():
    """Show configuration."""
    s = get_settings()
    table = Table(title="Configuración", box=box.ROUNDED)
    table.add_column("Variable", style="bold")
    table.add_column("Valor")
    table.add_row("IG username", s.ig_username or "(no seteado)")
    table.add_row("IG session file", s.ig_session_file)
    table.add_row("Max per run", str(s.max_profiles_per_run))
    table.add_row("Delay range", f"{s.delay_min_seconds}-{s.delay_max_seconds}s")
    table.add_row("Proxy", s.proxy_url or "(no)")
    table.add_row("Data dir", str(s.data_path))
    console.print(table)


if __name__ == "__main__":
    main()
