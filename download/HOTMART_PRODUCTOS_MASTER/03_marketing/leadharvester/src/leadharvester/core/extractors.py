"""LeadHarvester — Utilities for extracting contact info from bio text."""
from __future__ import annotations
import re

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
# Phone: optional +country code, then 7-15 digits with optional separators
PHONE_RE = re.compile(r"(\+?\d{1,3}[\s\-\.\)]?)?\(?\s*(\d[\d\s\-\.\(\)]{6,}\d)")
URL_RE = re.compile(r"https?://[^\s]+")

# Patterns often used to obfuscate emails in bios
EMAIL_OBFUSCATIONS = [
    (r"\s*\[?at\]?\s*", "@"),
    (r"\s*\[?dot\]?\s*", "."),
    (r"\s*\[?ar\]?\s*", "@"),
    (r"\s*\[?punto\]?\s*", "."),
]


def extract_email(text: str) -> str:
    """Extract email from text, handling common obfuscations."""
    if not text:
        return ""
    cleaned = text
    for pattern, replacement in EMAIL_OBFUSCATIONS:
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
    m = EMAIL_RE.search(cleaned)
    return m.group(0) if m else ""


def extract_phone(text: str) -> str:
    """Extract phone number from text."""
    if not text:
        return ""
    m = PHONE_RE.search(text)
    if not m:
        return ""
    # Concatenate all matched groups
    raw = "".join(g for g in m.groups() if g)
    if not raw:
        return ""
    # Extract only digits and the leading +
    digits = re.sub(r"[^\d+]", "", raw)
    if not digits.startswith("+"):
        digits = "+" + digits.lstrip("+")
    # Require at least 8 chars (+CC + number)
    if len(digits) < 8:
        return ""
    return digits


def extract_website(text: str) -> str:
    """Extract website URL from text."""
    if not text:
        return ""
    for m in URL_RE.finditer(text):
        url = m.group(0)
        if any(s in url for s in ("instagram.com", "facebook.com", "twitter.com", "tiktok.com", "youtube.com")):
            continue
        return url
    return ""


def is_business_bio(bio: str) -> bool:
    """Heuristic: does the bio suggest a business?"""
    if not bio:
        return False
    # Normalize for token matching (add spaces around)
    bio_lower = " " + bio.lower() + " "
    business_signals = [
        "venta", "compra", "servicio", "empresa", "tienda", "shop", "store",
        "oficial", "negocio", "delivery", "envío", "envio", "precio", "promotion",
        "consultoría", "consultoria", "asesoría", "asesoria", "freelance",
        "whatsapp", "wa.me", "contacto", "contact",
        " dm ",  # "DM for orders"
    ]
    return any(sig in bio_lower for sig in business_signals)


def extract_category(bio: str) -> str:
    """Best-effort category extraction."""
    if not bio:
        return ""
    bio_lower = bio.lower()
    categories = {
        "restaurante": ["restaurante", "comida", "restaurant", "café", "cafe", "food", "cocina"],
        "moda": ["moda", "fashion", "ropa", "clothing", "boutique", "store"],
        "fitness": ["fitness", "gym", "entrenamiento", "workout", "yoga"],
        "belleza": ["belleza", "beauty", "maquillaje", "makeup", "spa", "peluquería"],
        "tecnología": ["tech", "software", "developer", "programador", "sistemas"],
        "marketing": ["marketing", "agencia", "social media", "publicidad"],
        "inmobiliaria": ["inmobiliaria", "real estate", "propiedad", "inmueble"],
        "salud": ["salud", "health", "médico", "medico", "clínica", "clinica", "doctor"],
        "educación": ["educación", "educacion", "academia", "curso", "teacher", "profesor"],
    }
    for cat, keywords in categories.items():
        if any(kw in bio_lower for kw in keywords):
            return cat
    return ""
