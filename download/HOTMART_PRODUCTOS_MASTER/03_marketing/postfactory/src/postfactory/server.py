"""PostFactory — FastAPI server."""
from __future__ import annotations
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from postfactory import __version__
from postfactory.core.config import get_settings
from postfactory.core.models import PostRequest, CalendarRequest
from postfactory.templates import generate_posts as template_generate, BEST_TIMES
from postfactory.generators import generate_with_ai

app = FastAPI(
    title="PostFactory",
    description="Generador de contenido para redes sociales con IA. Post generators, hashtags, calendar.",
    version=__version__,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

WEB_DIR = Path(__file__).parent.parent.parent / "web"


@app.get("/", response_class=HTMLResponse)
async def root():
    idx = WEB_DIR / "index.html"
    if idx.exists():
        return HTMLResponse(idx.read_text(encoding="utf-8"))
    return HTMLResponse(f"<h1>PostFactory v{__version__}</h1>")


@app.get("/healthz")
async def healthz():
    s = get_settings()
    return {
        "status": "ok",
        "version": __version__,
        "brand": s.brand_name,
        "ai_configured": bool(s.ai_api_key),
        "ai_provider": s.ai_provider,
    }


@app.post("/v1/generate")
async def generate(req: PostRequest, mode: str = "ai"):
    """Generate post variations. mode: 'ai' or 'template'."""
    if mode == "template":
        posts = template_generate(req)
        return {
            "posts": [p.model_dump() for p in posts],
            "suggested_hashtags": posts[0].hashtags if posts else [],
            "model_used": "template-fallback",
        }
    return await generate_with_ai(req)


@app.get("/v1/hashtags")
async def get_hashtags(topic: str, niche: str = "marketing", platform: str = "instagram", count: int = 15):
    """Get hashtag suggestions only."""
    from postfactory.core.hashtags import generate_hashtags
    from postfactory.core.models import Platform
    try:
        p = Platform(platform)
    except ValueError:
        p = Platform.INSTAGRAM
    return generate_hashtags(topic, niche, p, count)


@app.post("/v1/calendar")
async def generate_calendar(req: CalendarRequest):
    """Generate a content calendar for N days."""
    s = get_settings()
    calendar = []
    today = datetime.utcnow().date()

    # Topic ideas by day (rotating)
    base_topics = req.topics or [
        f"consejo del día sobre {s.brand_niche}",
        f"tendencia en {s.brand_niche}",
        f"caso de éxito en {s.brand_niche}",
        f"pregunta frecuente sobre {s.brand_niche}",
        f"behind the scenes de {s.brand_name}",
        f"tip profesional sobre {s.brand_niche}",
        f"motivación del día",
    ]

    for i in range(req.days):
        day = today + timedelta(days=i)
        topic = base_topics[i % len(base_topics)]
        # Pick content type rotating
        content_types = ["educational", "promotional", "engagement", "storytelling", "inspirational", "listicle", "how_to"]
        ct = content_types[i % len(content_types)]

        entry = {
            "date": day.isoformat(),
            "weekday": day.strftime("%A"),
            "topic": topic,
            "content_type": ct,
            "posts": [],
        }

        for platform in req.platforms:
            best_times = BEST_TIMES.get(platform, ["10:00"])
            entry["posts"].append({
                "platform": platform.value,
                "best_time": best_times[0] if best_times else "10:00",
                "status": "pending",
            })

        calendar.append(entry)

    return {
        "calendar": calendar,
        "days": req.days,
        "platforms": [p.value for p in req.platforms],
        "brand": s.brand_name,
    }
