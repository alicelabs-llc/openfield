"""PostFactory — AI client (optional, falls back to templates)."""
from __future__ import annotations
import json
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from postfactory.core.config import get_settings
from postfactory.core.models import PostRequest, Post, Platform, ContentType
from postfactory.templates import generate_posts as template_generate


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def call_ai(prompt: str) -> dict:
    """Call AI provider."""
    s = get_settings()
    if not s.ai_api_key:
        return {"error": "AI_API_KEY not configured"}

    headers = {"Authorization": f"Bearer {s.ai_api_key}", "Content-Type": "application/json"}
    payload = {
        "model": s.ai_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.85,
        "max_tokens": 3000,
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(s.ai_api_url, json=payload, headers=headers)
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}: {r.text[:200]}"}
    data = r.json()
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return {"error": "Invalid AI response"}
    try:
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        else:
            start = content.find("{")
            end = content.rfind("}") + 1
            json_str = content[start:end]
        return json.loads(json_str)
    except (json.JSONDecodeError, IndexError):
        return {"posts": [{"text": content.strip(), "platform": "instagram"}]}


def _build_prompt(req: PostRequest) -> str:
    s = get_settings()
    return f"""Eres un creador de contenido experto en redes sociales para {s.brand_name}.

Marca: {s.brand_name}
Voz de marca: {s.brand_voice}
Nicho: {s.brand_niche}
Idioma: {req.language or s.brand_language}

Tema: {req.topic}
Plataforma: {req.platform.value}
Tipo de contenido: {req.content_type.value}
Tono: {req.tone}
Público objetivo: {req.target_audience or 'general'}
Puntos clave: {", ".join(req.key_points) if req.key_points else 'genera 3 relevantes'}
CTA: {req.call_to_action or 'genera uno apropiado'}
Emojis: {'sí' if req.include_emojis else 'no'}
Hashtags: {'sí' if req.include_hashtags else 'no'}

REGLAS DE PLATAFORMA:
- Instagram: máxima interacción, hasta 2200 caracteres, 10-15 hashtags
- LinkedIn: tono profesional, hasta 3000 caracteres, 3-5 hashtags
- Twitter: máximo 280 caracteres, 2-3 hashtags
- TikTok: tono casual, descripción corta con tendencias

Genera {req.variations} variaciones del post en JSON:
{{
  "posts": [
    {{"text": "...", "hashtags": ["#x", "#y"], "best_posting_time": "12:00"}}
  ],
  "content_ideas": ["idea 1", "idea 2", "idea 3"],
  "suggested_hashtags": ["#tag1", "#tag2", "...15 total"]
}}

Devuelve SOLO el JSON.
"""


async def generate_with_ai(req: PostRequest) -> dict:
    """Generate posts using AI; fallback to templates on error."""
    s = get_settings()
    if not s.ai_api_key:
        # Fallback to templates
        posts = template_generate(req)
        return {
            "posts": [p.model_dump() for p in posts],
            "suggested_hashtags": posts[0].hashtags if posts else [],
            "model_used": "template-fallback",
        }

    prompt = _build_prompt(req)
    result = await call_ai(prompt)
    if "error" in result:
        # Fallback
        posts = template_generate(req)
        return {
            "posts": [p.model_dump() for p in posts],
            "suggested_hashtags": posts[0].hashtags if posts else [],
            "model_used": f"template-fallback ({result['error'][:50]})",
        }

    posts = []
    for p_data in result.get("posts", []):
        text = p_data.get("text", "")
        hashtags = p_data.get("hashtags", [])
        if not req.include_hashtags:
            hashtags = []
        posts.append(Post(
            text=text,
            platform=req.platform,
            content_type=req.content_type,
            hashtags=hashtags,
            word_count=len(text.split()),
            char_count=len(text),
            best_posting_time=p_data.get("best_posting_time", ""),
        ))

    return {
        "posts": [p.model_dump() for p in posts],
        "suggested_hashtags": result.get("suggested_hashtags", [])[:15],
        "content_ideas": result.get("content_ideas", []),
        "model_used": s.ai_model,
    }
