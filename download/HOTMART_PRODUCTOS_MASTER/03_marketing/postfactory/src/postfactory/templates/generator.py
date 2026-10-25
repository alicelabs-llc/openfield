"""PostFactory — Template-based post generator (free, no AI)."""
from __future__ import annotations
from datetime import datetime, timedelta
from postfactory.core.models import Post, PostRequest, Platform, ContentType
from postfactory.core.hashtags import generate_hashtags


# Template structures per content_type
TEMPLATES = {
    ContentType.EDUCATIONAL: [
        "¿Sabías que {topic}? 🤔\n\n{point1}\n{point2}\n{point3}\n\n{cta}\n\n{hashtags}",
        "Hoy te enseñamos sobre {topic} 👇\n\n1️⃣ {point1}\n2️⃣ {point2}\n3️⃣ {point3}\n\n{cta}\n\n{hashtags}",
        "💡 Tip sobre {topic}:\n\n{point1}\n\nSi esto te sirvió, compártelo con alguien que lo necesite 🙌\n\n{hashtags}",
    ],
    ContentType.PROMOTIONAL: [
        "🔥 ¡{brand} presenta {topic}!\n\n{point1}\n{point2}\n{point3}\n\n{cta}\n\n{hashtags}",
        "✨ Novedad en {brand}: {topic}\n\n{point1}\n{point2}\n\n{cta}\n\n{hashtags}",
        "¿Buscas {topic}? En {brand} lo tenemos para ti 🎯\n\n{point1}\n{point2}\n\n{cta}\n\n{hashtags}",
    ],
    ContentType.ENGAGEMENT: [
        "Pregunta para ti: ¿{topic}? 👀\n\nCuéntanos en los comentarios 👇\n\n{hashtags}",
        "Vota por tu favorito: {topic}\n\nA) {point1}\nB) {point2}\nC) {point3}\n\n¡Escribe tu opción en comentarios! 🗳️\n\n{hashtags}",
        "Esto dividirá opiniones: ¿{topic}?\n\nYo digo que sí. ¿Tú qué opinas? 👇\n\n{hashtags}",
    ],
    ContentType.STORYTELLING: [
        "Hace tiempo, aprendí algo importante sobre {topic}.\n\n{point1}\n\nY eso cambió mi forma de ver las cosas.\n\n{cta}\n\n{hashtags}",
        "La historia de hoy: {topic}.\n\nTodo empezó cuando {point1}.\nLuego {point2}.\nY finalmente {point3}.\n\nEl aprendizaje: {cta}\n\n{hashtags}",
        "Te cuento algo sobre {topic} que quizás no sabías 👇\n\n{point1}\n{point2}\n\n{cta}\n\n{hashtags}",
    ],
    ContentType.INSPIRATIONAL: [
        "✨ Sobre {topic}:\n\n{point1}\n\n{cta}\n\n{hashtags}",
        "Hoy recordé por qué empecé esto.\n\n{topic} no es solo un tema. Es una pasión.\n\n{point1}\n\n{cta}\n\n{hashtags}",
        "Cada día es una nueva oportunidad.\n\nY {topic} es lo que me motiva.\n\n{point1}\n\n{cta}\n\n{hashtags}",
    ],
    ContentType.LISTICLE: [
        "3 cosas sobre {topic} que quizás no sabías 👇\n\n1. {point1}\n2. {point2}\n3. {point3}\n\n¿Cuál te sorprendió más?\n\n{hashtags}",
        "Top 5 sobre {topic}:\n\n1️⃣ {point1}\n2️⃣ {point2}\n3️⃣ {point3}\n4️⃣ Bonus: {point4}\n5️⃣ Bonus: {point5}\n\n{cta}\n\n{hashtags}",
        "Lista rápida sobre {topic}:\n\n• {point1}\n• {point2}\n• {point3}\n\nGuarda este post para después 🔖\n\n{hashtags}",
    ],
    ContentType.HOW_TO: [
        "Cómo hacer {topic} paso a paso 👇\n\n1. {point1}\n2. {point2}\n3. {point3}\n\n{cta}\n\n{hashtags}",
        "Tutorial: {topic} en 3 pasos\n\nPaso 1: {point1}\nPaso 2: {point2}\nPaso 3: {point3}\n\n{cta}\n\n{hashtags}",
        "Aprende {topic} hoy mismo 🚀\n\nEmpezamos por {point1}.\nLuego {point2}.\nY por último {point3}.\n\n{cta}\n\n{hashtags}",
    ],
    ContentType.BEHIND_SCENES: [
        "Detrás de {topic} en {brand} 🔍\n\n{point1}\n{point2}\n\nEsto no se ve todos los días 😊\n\n{hashtags}",
        "Behind the scenes de {topic} 📸\n\n{point1}\n\nLa magia ocurre cuando {point2}.\n\n{cta}\n\n{hashtags}",
        "Lo que nadie ve sobre {topic}:\n\n{point1}\n{point2}\n\nY así es como lo hacemos 👷\n\n{hashtags}",
    ],
    ContentType.USER_GENERATED: [
        "Nuestros clientes hablan sobre {topic} 💬\n\n{point1}\n\nGracias por compartir tu experiencia. {cta}\n\n{hashtags}",
        "Historia real de alguien que probó {topic}:\n\n{point1}\n{point2}\n\n¿Tú ya lo probaste? {cta}\n\n{hashtags}",
        "Reseñas de nuestros clientes sobre {topic} ⭐\n\n{point1}\n{point2}\n{point3}\n\nGracias por confiar en {brand} 🙏\n\n{hashtags}",
    ],
    ContentType.NEWS: [
        "📰 Última hora sobre {topic}:\n\n{point1}\n{point2}\n\n¿Qué opinas? Comenta abajo 👇\n\n{hashtags}",
        "Noticia importante sobre {topic} ⚡\n\n{point1}\n\nLee más en {cta}\n\n{hashtags}",
        "Lo que debes saber sobre {topic} hoy:\n\n{point1}\n{point2}\n\nComparte para que más personas lo sepan 📢\n\n{hashtags}",
    ],
}

# Default points if user didn't provide
DEFAULT_POINTS = {
    "fitness": ["rinde mejor cuando descansas 1 día entre sesiones", "la constancia supera a la intensidad", "la nutrición es el 70% del resultado"],
    "marketing": ["tu contenido necesita un CTA claro", "la audiencia se construye con valor, no con spam", "el storytelling vende más que las features"],
    "tecnologia": ["la documentación es tan importante como el código", "automatizar tareas repetitivas multiplica tu tiempo", "los tests salvan vidas (de desarrolladores)"],
    "comida": ["la frescura de los ingredientes marca la diferencia", "menos es más: respeta el sabor natural", "la técnica es más importante que la receta"],
    "default": ["esto funciona cuando lo aplicas con consistencia", "el detalle está en la ejecución", "los pequeños hábitos crean grandes resultados"],
}


# Best posting times per platform
BEST_TIMES = {
    Platform.INSTAGRAM: ["07:00-09:00", "12:00-14:00", "18:00-20:00"],
    Platform.LINKEDIN: ["08:00-10:00", "12:00-13:00", "17:00-18:00"],
    Platform.TWITTER: ["08:00-10:00", "13:00-15:00", "17:00-19:00"],
    Platform.TIKTOK: ["06:00-10:00", "19:00-23:00"],
    Platform.FACEBOOK: ["09:00-11:00", "13:00-15:00"],
    Platform.YOUTUBE: ["14:00-16:00", "19:00-21:00"],
    Platform.BLOG: ["any morning"],
}


def generate_posts(req: PostRequest) -> list[Post]:
    """Generate post variations using templates."""
    templates = TEMPLATES.get(req.content_type, TEMPLATES[ContentType.EDUCATIONAL])

    # Use user points or defaults
    if req.key_points:
        points = list(req.key_points) + [""] * 5
    else:
        # Use postfactory settings if available, else default pool
        try:
            from postfactory.core.config import get_settings
            s = get_settings()
            niche = s.brand_niche
        except Exception:
            niche = "default"
        default_pool = DEFAULT_POINTS.get(niche.lower(), DEFAULT_POINTS["default"])
        points = default_pool + [""] * 5

    point1, point2, point3, point4, point5 = points[:5]

    cta = req.call_to_action or _default_cta(req.platform, req.content_type)
    brand = req.brand_name or ""

    try:
        from postfactory.core.config import get_settings
        s = get_settings()
        niche = s.brand_niche
    except Exception:
        niche = "marketing"
    hashtags_list = generate_hashtags(req.topic, niche, req.platform)
    hashtags = " ".join(hashtags_list[:5]) if req.include_hashtags else ""

    variations = min(req.variations, len(templates))
    posts = []
    for i in range(variations):
        template = templates[i % len(templates)]
        text = template.format(
            topic=req.topic,
            brand=brand,
            point1=point1,
            point2=point2,
            point3=point3,
            point4=point4,
            point5=point5,
            cta=cta,
            hashtags=hashtags,
        )
        if not req.include_emojis:
            text = _strip_emojis(text)

        post = Post(
            text=text,
            platform=req.platform,
            content_type=req.content_type,
            hashtags=hashtags_list if req.include_hashtags else [],
            emoji_count=_count_emojis(text) if req.include_emojis else 0,
            word_count=len(text.split()),
            char_count=len(text),
            suggested_image_prompt=_image_prompt(req.topic, req.content_type),
            best_posting_time=BEST_TIMES.get(req.platform, ["flexible"])[0],
        )
        posts.append(post)
    return posts


def _default_cta(platform: Platform, content_type: ContentType) -> str:
    if platform == Platform.LINKEDIN:
        return "¿Qué opinas? Cuéntame en los comentarios."
    if platform == Platform.TWITTER:
        return "RT si te sirvió ↓"
    if platform == Platform.TIKTOK:
        return "Sígueme para más tips 🚀"
    if content_type == ContentType.PROMOTIONAL:
        return "Link en bio 🔗"
    return "¿Te sirvió? Compártelo 🙌"


def _strip_emojis(text: str) -> str:
    import unicodedata
    result = []
    for char in text:
        try:
            if unicodedata.category(char).startswith("So") or ord(char) > 0x1F000:
                continue
        except Exception:
            pass
        result.append(char)
    return "".join(result)


def _count_emojis(text: str) -> int:
    import unicodedata
    return sum(1 for c in text if unicodedata.category(c).startswith("So") or ord(c) > 0x1F000)


def _image_prompt(topic: str, content_type: ContentType) -> str:
    return f"Imagen para post de {content_type.value} sobre {topic}. Estilo limpio, alta calidad, paleta moderna."
