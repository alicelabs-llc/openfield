"""PostFactory — CLI."""
from __future__ import annotations
import asyncio
import click
from rich.console import Console
from rich.table import Table
from rich import box

from postfactory import __version__
from postfactory.core.config import get_settings
from postfactory.core.models import PostRequest, Platform, ContentType, CalendarRequest
from postfactory.templates import generate_posts as template_generate
from postfactory.generators import generate_with_ai

console = Console()


@click.group()
@click.version_option(__version__, prog_name="postfactory")
def main():
    """PostFactory — Generador de contenido para redes sociales."""


@main.command()
def version():
    click.echo(f"PostFactory v{__version__}")


@main.command()
@click.argument("topic")
@click.option("--platform", type=click.Choice([p.value for p in Platform]), default="instagram")
@click.option("--type", "content_type", type=click.Choice([c.value for c in ContentType]), default="educational")
@click.option("--tone", default="profesional_amable")
@click.option("--variations", type=int, default=3)
@click.option("--no-emojis", is_flag=True)
@click.option("--no-hashtags", is_flag=True)
@click.option("--mode", type=click.Choice(["ai", "template"]), default="ai")
def generate(topic, platform, content_type, tone, variations, no_emojis, no_hashtags, mode):
    """Generate post variations."""
    req = PostRequest(
        topic=topic,
        platform=Platform(platform),
        content_type=ContentType(content_type),
        tone=tone,
        variations=variations,
        include_emojis=not no_emojis,
        include_hashtags=not no_hashtags,
    )
    if mode == "template":
        posts = template_generate(req)
        result = {"posts": [p.model_dump() for p in posts], "model_used": "template-fallback"}
    else:
        result = asyncio.run(generate_with_ai(req))

    console.print(f"[cyan]Modelo:[/cyan] {result.get('model_used', '?')}\n")

    for i, post in enumerate(result.get("posts", []), 1):
        console.print(f"[bold]Variación {i}[/bold] ({post.get('word_count', 0)}w, {post.get('char_count', 0)}c)")
        console.print(post["text"])
        if post.get("hashtags"):
            console.print(f"[dim]Hashtags:[/dim] {' '.join(post['hashtags'][:5])}")
        console.print(f"[dim]Best time: {post.get('best_posting_time', '?')}\n")


@main.command()
@click.argument("topic")
@click.option("--niche", default="marketing")
@click.option("--platform", default="instagram")
@click.option("--count", type=int, default=15)
def hashtags(topic, niche, platform, count):
    """Get hashtag suggestions."""
    from postfactory.core.hashtags import generate_hashtags
    tags = generate_hashtags(topic, niche, Platform(platform), count)
    console.print(" ".join(tags))


@main.command()
@click.option("--days", type=int, default=7)
@click.option("--platforms", default="instagram,linkedin")
def calendar(days, platforms):
    """Generate content calendar."""
    from postfactory.core.models import Platform
    plats = [Platform(p.strip()) for p in platforms.split(",")]
    req = CalendarRequest(days=days, platforms=plats)
    s = get_settings()
    # Use server logic
    from postfactory.server import generate_calendar as gen_cal
    import asyncio
    result = asyncio.run(gen_cal(req))

    table = Table(title=f"Calendario de contenido ({days} días)", box=box.ROUNDED)
    table.add_column("Fecha", style="bold")
    table.add_column("Día")
    table.add_column("Tema")
    table.add_column("Tipo")
    table.add_column("Plataformas")
    for entry in result["calendar"]:
        platforms_str = ", ".join([f"{p['platform']}@{p['best_time']}" for p in entry["posts"]])
        table.add_row(
            entry["date"],
            entry["weekday"],
            entry["topic"][:40],
            entry["content_type"],
            platforms_str,
        )
    console.print(table)


@main.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8007, type=int)
@click.option("--reload", is_flag=True)
def serve(host, port, reload):
    """Start FastAPI server."""
    import uvicorn
    uvicorn.run("postfactory.server:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    main()
