"""ReviewReply AI — CLI."""
from __future__ import annotations
import asyncio
import json
import click
from rich.console import Console
from rich.table import Table
from rich import box

from reviewreply import __version__
from reviewreply.core.config import get_settings
from reviewreply.core.models import ReviewRequest, Platform
from reviewreply.generators import generate_replies, template_reply

console = Console()


@click.group()
@click.version_option(__version__, prog_name="reviewreply")
def main():
    """ReviewReply AI — Generador de respuestas a reseñas."""


@main.command()
def version():
    click.echo(f"ReviewReply AI v{__version__}")


@main.command()
@click.option("--rating", type=int, prompt="Rating (1-5)")
@click.option("--text", prompt="Texto de la reseña")
@click.option("--author", default="", prompt="Autor (opcional)")
@click.option("--mode", type=click.Choice(["ai", "template"]), default="ai")
def generate(rating, text, author, mode):
    """Generate replies for a single review."""
    req = ReviewRequest(rating=rating, text=text, author_name=author)
    if mode == "template":
        s = get_settings()
        suggestions = template_reply(req, business_name=s.business_name)
    else:
        result = asyncio.run(generate_replies(req))
        if "error" in result:
            console.print(f"[red]✗ Error: {result['error']}[/red]")
            return
        suggestions = result.get("suggestions", [])
        console.print(f"\n[cyan]Sentiment detected:[/cyan] {result.get('detected_sentiment', '?')}")
        console.print(f"[cyan]Summary:[/cyan] {result.get('review_summary', '')[:100]}\n")

    for i, s in enumerate(suggestions, 1):
        console.print(f"[bold]Opción {i} — {s.tone}[/bold] ({s.word_count} palabras)")
        console.print(s.text)
        console.print()


@main.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8006, type=int)
@click.option("--reload", is_flag=True)
def serve(host, port, reload):
    """Start FastAPI server."""
    import uvicorn
    uvicorn.run("reviewreply.server:app", host=host, port=port, reload=reload)


@main.command()
def config():
    """Show configuration."""
    s = get_settings()
    table = Table(title="Configuration", box=box.ROUNDED)
    table.add_column("Variable", style="bold")
    table.add_column("Valor")
    table.add_row("Business name", s.business_name)
    table.add_row("Business type", s.business_type)
    table.add_row("Tone", s.business_tone)
    table.add_row("Language", s.business_language)
    table.add_row("AI provider", s.ai_provider)
    table.add_row("AI model", s.ai_model)
    table.add_row("AI configured", "✓" if s.ai_api_key else "✗ (will use template fallback)")
    console.print(table)


if __name__ == "__main__":
    main()
