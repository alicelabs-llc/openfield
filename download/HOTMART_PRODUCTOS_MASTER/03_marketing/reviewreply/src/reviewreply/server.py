"""ReviewReply AI — FastAPI server."""
from __future__ import annotations
import asyncio
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from reviewreply import __version__
from reviewreply.core.config import get_settings
from reviewreply.core.models import ReviewRequest, GeneratedReply, BatchRequest
from reviewreply.generators import generate_replies, template_reply
from reviewreply.generators.templates import template_reply as template_fn

app = FastAPI(
    title="ReviewReply AI",
    description="Generador de respuestas a reseñas con IA. Google Reviews, Yelp, App Store, Trustpilot.",
    version=__version__,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

WEB_DIR = Path(__file__).parent.parent.parent / "web"


@app.get("/", response_class=HTMLResponse)
async def root():
    idx = WEB_DIR / "index.html"
    if idx.exists():
        return HTMLResponse(idx.read_text(encoding="utf-8"))
    return HTMLResponse(f"<h1>ReviewReply AI v{__version__}</h1>")


@app.get("/healthz")
async def healthz():
    s = get_settings()
    return {
        "status": "ok",
        "version": __version__,
        "ai_provider": s.ai_provider,
        "ai_configured": bool(s.ai_api_key),
        "business_name": s.business_name,
    }


@app.post("/v1/generate")
async def generate(req: ReviewRequest, mode: str = "ai"):
    """Generate reply suggestions for a review.

    mode: 'ai' (uses AI provider) or 'template' (free, no AI required).
    """
    if mode == "template":
        s = get_settings()
        suggestions = template_fn(req, business_name=s.business_name)
        return GeneratedReply(
            review_summary="",
            detected_sentiment=suggestions[0].sentiment_addressed if suggestions else "neutral",
            suggestions=suggestions,
            model_used="template-fallback",
        ).model_dump()

    # AI mode
    result = await generate_replies(req)
    if "error" in result:
        raise HTTPException(502, result["error"])
    return result


@app.post("/v1/generate/batch")
async def generate_batch(req: BatchRequest, mode: str = "ai"):
    """Generate replies for multiple reviews."""
    if mode == "ai":
        results = await asyncio.gather(*[generate_replies(r) for r in req.reviews])
        return [r for r in results if "error" not in r]
    else:
        s = get_settings()
        out = []
        for review in req.reviews:
            suggestions = template_fn(review, business_name=s.business_name)
            out.append({
                "suggestions": [s.model_dump() for s in suggestions],
                "model_used": "template-fallback",
                "detected_sentiment": suggestions[0].sentiment_addressed.value if suggestions else "neutral",
            })
        return out


@app.get("/v1/templates")
async def list_templates():
    """List available template tones."""
    from reviewreply.generators.templates import TEMPLATES
    from reviewreply.core.models import Sentiment
    return {
        sentiment.value: list(templates.keys())
        for sentiment, templates in TEMPLATES.items()
    }
