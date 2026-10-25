"""ReviewReply AI — Template-based fallback generator (no AI needed)."""
from __future__ import annotations
from reviewreply.core.models import ReviewRequest, ReplySuggestion, Sentiment
from reviewreply.core.sentiment import detect_sentiment


# Template library by sentiment
TEMPLATES = {
    Sentiment.POSITIVE: {
        "corto": "¡Gracias {name}! 🙌 Nos alegra mucho que hayas tenido una excelente experiencia. ¡Te esperamos pronto!",
        "medio": "¡Hola {name}! Muchísimas gracias por tomarte el tiempo de compartir tu experiencia. Nos llena de alegría saber que disfrutaste {topic}. Trabajamos duro cada día para ofrecer exactamente eso. Te esperamos nuevamente pronto. 🙌",
        "detallado": "¡Hola {name}! Gracias por tus amables palabras y por confiar en nosotros. Nos emociona saber que destacaste {topic}, ya que es algo en lo que ponemos especial cuidado. Tu feedback nos motiva a seguir mejorando. Si alguna vez necesitas algo adicional, no dudes en contactarnos directamente. ¡Volverás a recibir el mismo excelente trato! Te esperamos pronto. Un abrazo.",
    },
    Sentiment.NEGATIVE: {
        "corto": "Hola {name}. Lamentamos tu experiencia. Escríbenos a contacto@negocio.com para solucionarlo.",
        "medio": "Hola {name}. Lamentamos mucho que tu experiencia con {topic} no haya sido la esperada. Nos gustaría conocer más detalles para solucionarlo. Por favor escríbenos a contacto@negocio.com con tu número de orden y te contactaremos de inmediato.",
        "detallado": "Hola {name}. Leímos tu reseña y sentimos mucho que no hayas tenido la experiencia que esperabas respecto a {topic}. Tomamos muy en serio este tipo de comentarios y queremos solucionarlo cuanto antes. Te invitamos a escribirnos directamente a contacto@negocio.com con los detalles de tu visita (fecha y hora aproximada) para que nuestro equipo pueda investigar y tomar las medidas correspondientes. Agradecemos tu feedback porque nos ayuda a mejorar. Esperamos tener la oportunidad de cambiar tu próxima experiencia. — Equipo {business}",
    },
    Sentiment.NEUTRAL: {
        "corto": "¡Gracias {name} por tu reseña! Esperamos verte de nuevo pronto.",
        "medio": "Hola {name}. Gracias por tomarte el tiempo de compartir tu experiencia. Trabajamos para mejorar y nos gustaría que en tu próxima visita tengas una mejor opinión sobre {topic}. ¡Te esperamos!",
        "detallado": "Hola {name}. Agradecemos mucho tu comentario. Entendemos que tu experiencia con {topic} pudo haber sido neutral y queremos aprovechar la oportunidad para mejorar. Estamos trabajando en optimizar ese aspecto específicamente. Te invitamos a visitarnos nuevamente pronto y contarnos cómo fue tu experiencia. Tu opinión es clave para nosotros. ¡Te esperamos! — Equipo {business}",
    },
    Sentiment.MIXED: {
        "corto": "Hola {name}. Gracias por tu feedback mixto. Trabajaremos en {topic} para mejorar.",
        "medio": "Hola {name}. Apreciamos tu reseña. Nos alegra lo positivo y tomamos nota de lo que mencionas sobre {topic}. Te invitamos a volver y contarnos cómo fue esta vez.",
        "detallado": "Hola {name}. Gracias por compartir tu experiencia. Valoramos mucho que resaltes lo positivo y también tomamos muy en serio tus comentarios sobre {topic}. Estamos implementando mejoras concretas en ese aspecto y nos encantaría que vuelvas a visitarnos pronto para que percibas el cambio. Si deseas hablar más a fondo, no dudes en escribirnos a contacto@negocio.com. — Equipo {business}",
    },
}


def template_reply(req: ReviewRequest, business_name: str = "") -> list[ReplySuggestion]:
    """Generate 3 template-based replies (no AI required, free)."""
    sentiment = detect_sentiment(req.text, req.rating)
    name = req.author_name or "amig@"
    topics = __import__("reviewreply.core.sentiment", fromlist=["extract_topics"]).extract_topics(req.text)
    topic_str = topics[0] if topics else "nuestra atención"

    templates = TEMPLATES.get(sentiment, TEMPLATES[Sentiment.NEUTRAL])
    suggestions = []
    for length_label, template in templates.items():
        text = template.format(name=name, topic=topic_str, business=business_name or "el equipo")
        suggestions.append(ReplySuggestion(
            text=text,
            tone=length_label,
            sentiment_addressed=sentiment,
            word_count=len(text.split()),
        ))
    return suggestions
