"""ReviewReply AI — Prompt builder + AI client."""
from __future__ import annotations
import json
from typing import AsyncIterator
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from reviewreply.core.config import get_settings
from reviewreply.core.models import ReviewRequest, Sentiment, ReplySuggestion, Platform
from reviewreply.core.sentiment import detect_sentiment, extract_topics


# Platform-specific guidance
PLATFORM_RULES = {
    Platform.GOOGLE_REVIEWS: "Google Reviews: respuesta pública, máx 4096 caracteres, tono profesional.",
    Platform.YELP: "Yelp: respuesta pública, máx 5000 caracteres, tono genuino y empático.",
    Platform.TRUSTPILOT: "Trustpilot: respuesta pública, máx 10000 caracteres, tono formal.",
    Platform.APP_STORE: "App Store: respuesta del desarrollador, máx 300 caracteres, conciso.",
    Platform.FACEBOOK: "Facebook: respuesta pública, máx 8000 caracteres, tono cercano.",
    Platform.AMAZON: "Amazon: respuesta pública, máx 250 caracteres, directo y profesional.",
    Platform.GENERIC: "Respuesta pública, máx 1000 caracteres, tono profesional.",
}


def build_prompt(req: ReviewRequest, tone: str = "profesional_amable", business_name: str = "") -> str:
    """Build the system+user prompt for the AI."""
    sentiment = detect_sentiment(req.text, req.rating)
    topics = extract_topics(req.text)

    platform_rule = PLATFORM_RULES.get(req.platform, PLATFORM_RULES[Platform.GENERIC])

    sentiment_instruction = {
        Sentiment.POSITIVE: "El cliente está satisfecho. Agradece, refuerza lo positivo, invita a volver.",
        Sentiment.NEGATIVE: "El cliente está insatisfecho. Empatiza, pide disculpas si corresponde, ofrece solución concreta, da contacto directo.",
        Sentiment.NEUTRAL: "El cliente tiene mixed/neutral feelings. Agradece el feedback, menciona mejoras, invita a volver.",
        Sentiment.MIXED: "El cliente tiene sentimientos encontrados. Reconoce lo positivo, aborda lo negativo con propuesta concreta.",
    }[sentiment]

    rating_display = "★" * req.rating
    prompt = f"""Eres un experto en atención al cliente para {business_name or 'un negocio'}. 
Responde a la siguiente reseña con tono: {tone}.

TONO: {tone}
IDIOMA: {req.language or 'español'}
PLATAFORMA: {req.platform.value}

REGLAS DE PLATAFORMA:
{platform_rule}

INSTRUCCIONES SEGÚN SENTIMIENTO:
{sentiment_instruction}

DATOS DE LA RESEÑA:
- Cliente: {req.author_name or 'Anónimo'}
- Rating: {req.rating} estrellas ({rating_display})
- Título: {req.title or '(sin título)'}
- Texto: "{req.text}"
- Temas detectados: {", ".join(topics) or "ninguno específico"}
- Contexto adicional: {req.business_context or 'ninguno'}

GENERA 3 RESPUESTAS DIFERENTES (corta, media, detallada):
1. Corta (30-50 palabras): directa, con emoji opcional.
2. Media (60-100 palabras): con empatía y detalle.
3. Larga (120-180 palabras): incluye solución específica + invitación a volver.

Cada respuesta debe:
- Saludar al cliente por nombre si está disponible.
- Mencionar el tema principal de la reseña.
- Ajustarse al sentimiento detectado ({sentiment.value}).
- Incluir CTA (invitar a contactar/volver).
- No inventar features del negocio que no se mencionen.

Devuelve SOLO JSON con esta estructura exacta:
{{
  "responses": [
    {{"text": "...", "tone": "corto"}},
    {{"text": "...", "tone": "medio"}},
    {{"text": "...", "tone": "detallado"}}
  ]
}}
"""
    return prompt


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def call_ai(prompt: str) -> dict:
    """Call AI provider (zai/openai/anthropic)."""
    s = get_settings()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {s.ai_api_key}",
    }
    payload = {
        "model": s.ai_model,
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 2000,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(s.ai_api_url, json=payload, headers=headers)

    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}: {r.text[:200]}"}

    data = r.json()

    # Parse response (z.ai/openai compatible)
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return {"error": "Invalid AI response structure", "raw": data}

    # Try to extract JSON from content
    try:
        # Look for JSON block
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
        else:
            # Find first { ... }
            start = content.find("{")
            end = content.rfind("}") + 1
            json_str = content[start:end]
        return json.loads(json_str)
    except (json.JSONDecodeError, IndexError):
        # Fallback: return raw content as single response
        return {"responses": [{"text": content.strip(), "tone": "fallback"}]}


async def generate_replies(req: ReviewRequest) -> dict:
    """Generate 3 reply suggestions (corto, medio, detallado)."""
    s = get_settings()
    prompt = build_prompt(req, tone=s.business_tone, business_name=s.business_name)
    result = await call_ai(prompt)
    if "error" in result:
        return {"error": result["error"], "suggestions": []}

    suggestions = []
    for r in result.get("responses", []):
        text = r.get("text", "").strip()
        tone = r.get("tone", "fallback")
        if text:
            suggestions.append(ReplySuggestion(
                text=text,
                tone=tone,
                sentiment_addressed=detect_sentiment(req.text, req.rating),
                word_count=len(text.split()),
            ))
    return {
        "suggestions": suggestions,
        "model_used": s.ai_model,
        "review_summary": _summarize(req.text),
        "detected_sentiment": detect_sentiment(req.text, req.rating).value,
    }


def _summarize(text: str, max_words: int = 30) -> str:
    """Quick text summary (first sentence + topics)."""
    first_sentence = text.split(".")[0].strip()
    if len(first_sentence.split()) > max_words:
        return " ".join(first_sentence.split()[:max_words]) + "..."
    return first_sentence
