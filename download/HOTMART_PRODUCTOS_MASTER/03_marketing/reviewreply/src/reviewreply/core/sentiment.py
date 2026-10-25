"""ReviewReply AI — Sentiment analysis (heuristic, no external AI)."""
from __future__ import annotations
import re
from reviewreply.core.models import Sentiment, Review


# Positive / negative word lists (Spanish + English)
POSITIVE_WORDS = [
    "excelente", "increíble", "increible", "perfecto", "perfecta", "amable", "rápido", "rapido",
    "recomiendo", "encantado", "encantada", "feliz", "satisfecho", "satisfecha", "genial",
    "maravilloso", "maravillosa", "buena atención", "buen servicio", "óptimo", "optimo",
    "excelente atención", "profesional", "limpio", "cómodo", "comodo", "agradable",
    "fantastic", "amazing", "great", "love", "perfect", "excellent", "wonderful", "happy",
    "best", "awesome", "highly recommend", "delicious", "fresh", "friendly",
]

NEGATIVE_WORDS = [
    "terrible", "horrible", "pésimo", "pesimo", "malo", "mala", "lento", "lenta", "caro",
    "cara", "sucio", "sucia", "grosero", "grosera", "no recomiendo", "nunca", "decepcionado",
    "decepcionada", "fracaso", "desastre", "pérdida", "perdida", "tiempo perdido",
    "bad", "terrible", "horrible", "worst", "awful", "disappointed", "rude", "slow",
    "dirty", "overpriced", "never", "waste of", "broken", "damaged", "poor",
]

MIXED_INDICATORS = ["pero", "aunque", "sin embargo", "but", "however", "although", "no obstante"]


def detect_sentiment(review: Review | str, rating: int | None = None) -> Sentiment:
    """Detect sentiment from text + rating."""
    if isinstance(review, Review):
        text = f"{review.title} {review.text}".lower()
        rating = review.rating
    else:
        text = review.lower()

    # Quick check on rating
    if rating is not None:
        if rating >= 4:
            sentiment_hint = Sentiment.POSITIVE
        elif rating <= 2:
            sentiment_hint = Sentiment.NEGATIVE
        else:
            sentiment_hint = Sentiment.NEUTRAL
    else:
        sentiment_hint = Sentiment.NEUTRAL

    # Find all negative matches (and their spans)
    neg_matches = [w for w in NEGATIVE_WORDS if w in text]
    # For positive matches, exclude those that are substring of a negative match
    # (e.g. "recomiendo" is inside "no recomiendo")
    pos_matches = []
    for w in POSITIVE_WORDS:
        if w in text:
            # Check if this positive word is part of a negative phrase
            if any(w in neg for neg in neg_matches):
                continue
            pos_matches.append(w)

    pos_count = len(pos_matches)
    neg_count = len(neg_matches)
    has_mixed = any(w in text for w in MIXED_INDICATORS)

    # Strong rating signal overrides text-only analysis
    if rating is not None and rating <= 2 and neg_count >= pos_count:
        return Sentiment.NEGATIVE if not has_mixed or neg_count > pos_count else Sentiment.MIXED
    if rating is not None and rating >= 4 and pos_count >= neg_count:
        return Sentiment.POSITIVE if not has_mixed or pos_count > neg_count else Sentiment.MIXED

    if pos_count > 0 and neg_count > 0:
        return Sentiment.MIXED
    if has_mixed and pos_count != neg_count:
        return Sentiment.MIXED
    if pos_count > neg_count:
        return Sentiment.POSITIVE if sentiment_hint != Sentiment.NEGATIVE else Sentiment.MIXED
    if neg_count > pos_count:
        return Sentiment.NEGATIVE if sentiment_hint != Sentiment.POSITIVE else Sentiment.MIXED
    return sentiment_hint


def extract_topics(text: str) -> list[str]:
    """Extract main topics mentioned in the review."""
    text_lower = text.lower()
    topics = []
    topic_map = {
        "servicio": ["servicio", "atención", "atencion", "trato", "staff", "empleado", "mesero"],
        "producto": ["producto", "compra", "artículo", "articulo", "calidad"],
        "comida": ["comida", "plato", "sabor", "delicioso", "rico", "frío", "frio"],
        "precio": ["precio", "caro", "barato", "vale la pena", "costoso"],
        "entrega": ["entrega", "envío", "envio", "delivery", "demora", "rápido", "rapido", "lento"],
        "limpieza": ["limpio", "sucio", "limpieza"],
        "ambiente": ["ambiente", "decoración", "decoracion", "música", "musica", "ruidoso"],
        "ubicación": ["ubicación", "ubicacion", "lugar", "fácil", "facil", "parking", "estacionamiento"],
    }
    for topic, keywords in topic_map.items():
        if any(kw in text_lower for kw in keywords):
            topics.append(topic)
    return topics
