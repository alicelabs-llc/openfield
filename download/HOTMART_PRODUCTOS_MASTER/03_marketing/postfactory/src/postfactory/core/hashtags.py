"""PostFactory — Hashtag generator (heuristic + AI).

Heuristic mode: free, based on topic + niche + platform.
AI mode: generates creative hashtags via LLM.
"""
from __future__ import annotations
import re
from collections import Counter

from postfactory.core.config import get_settings
from postfactory.core.models import Platform


# Default hashtag pools by niche
NICHE_HASHTAGS = {
    "marketing": ["#marketing", "#marketingdigital", "#redessociales", "#contentmarketing",
                  "#seo", "#smm", "#growthhacking", "#marketingtips", "#socialmedia",
                  "#digitalmarketing", "#branding", "#estrategia", "#copywriting"],
    "fitness": ["#fitness", "#gym", "#workout", "#training", "#fit", "#saludable",
                "#deporte", "#vidasana", "#nutricion", "#motivacion", "#ejercicio",
                "#fitnessmotivation", "#health", "#wellness", "#fitfam"],
    "comida": ["#comida", "#food", "#receta", "#recetas", "#cocina", "#foodie",
               "#foodporn", "#instafood", "#delicioso", "#cocinacasera",
               "#comidacasera", "#chef", "#gastronomia", "#foodlover", "#tasty"],
    "moda": ["#moda", "#fashion", "#style", "#outfit", "#ootd", "#look",
             "#trend", "#modafemenina", "#modamasculina", "#estilo",
             "#fashionista", "#fashionblogger", "#chic", "#glamour"],
    "tecnologia": ["#tecnologia", "#tech", "#programacion", "#desarrollo",
                   "#dev", "#software", "#ai", "#machinelearning", "#python",
                   "#javascript", "#startup", "#innovation", "#coding",
                   "#developer", "#techtwitter"],
    "viajes": ["#viajes", "#travel", "#wanderlust", "#travelgram",
               "#instatravel", "#viajar", "#aventura", "#explorar",
               "#mundo", "#destinos", "#travelling", "#globetrotter",
               "#viaje", "#travellife"],
    "negocios": ["#negocios", "#business", "#emprendimiento", "#emprendedor",
                 "#startup", "#negocio", "#finanzas", "#inversion",
                 "#exito", "#liderazgo", "#motivacion", "#networking",
                 "#businessowner", "#entrepreneur", "#hustle"],
    "salud": ["#salud", "#health", "#bienestar", "#wellness", "#medicina",
              "#vidasana", "#cuidadopersonal", "#saludmental", "#auto-cuidado",
              "#saludybienestar", "#healthy", "#saludable", "#medico"],
    "educacion": ["#educacion", "#education", "#aprendizaje", "#estudiar",
                  "#escuela", "#universidad", "#cursos", "#formacion",
                  "#aprender", "#estudia", "#educaciondigital", "#aprendizaje"],
    "default": ["#contenido", "#post", "#instagood", "#follow", "#like4like",
                "#instadaily", "#photooftheday", "#picoftheday", "#love",
                "#instamood"],
}

# Platform-specific hashtag limits
PLATFORM_HASHTAG_LIMITS = {
    Platform.INSTAGRAM: 30,
    Platform.LINKEDIN: 5,
    Platform.TWITTER: 3,
    Platform.TIKTOK: 6,
    Platform.FACEBOOK: 5,
    Platform.YOUTUBE: 15,
    Platform.BLOG: 10,
}


def _slugify(text: str) -> str:
    """Convert text to hashtag-friendly slug."""
    # Remove accents
    import unicodedata
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    # Lowercase, replace spaces with nothing (hashtag pattern)
    text = re.sub(r"[^\w\s]", "", text.lower())
    text = re.sub(r"\s+", "", text)
    return text


def generate_hashtags(topic: str, niche: str, platform: Platform, count: int = 15) -> list[str]:
    """Generate hashtags combining niche pool + topic-derived + trending-style."""
    # Get niche hashtags
    niche_pool = NICHE_HASHTAGS.get(niche.lower(), NICHE_HASHTAGS["default"])

    # Topic-derived
    words = re.findall(r"\w+", topic.lower())
    topic_hashtags = []
    for word in words:
        if len(word) >= 4:
            topic_hashtags.append(f"#{word}")
    # Also a single combined
    slug = _slugify(topic)
    if slug and len(slug) <= 30:
        topic_hashtags.insert(0, f"#{slug}")

    # Platform-specific (mix niche + topic + branded)
    platform_limit = PLATFORM_HASHTAG_LIMITS.get(platform, 10)
    final_count = min(count, platform_limit)

    # Combine and dedupe
    combined = []
    seen = set()
    for tag in topic_hashtags + niche_pool:
        if tag.lower() not in seen:
            combined.append(tag)
            seen.add(tag.lower())
        if len(combined) >= final_count:
            break

    return combined[:final_count]
