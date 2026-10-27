"""Tests for template-based reply generator (no AI needed)."""
import pytest
from reviewreply.core.models import ReviewRequest, Sentiment, Platform
from reviewreply.generators import template_reply
from reviewreply.generators.templates import TEMPLATES


class TestTemplateReply:
    def test_positive_review_returns_3_options(self):
        req = ReviewRequest(
            rating=5,
            text="Excelente servicio, muy amables. Recomiendo totalmente.",
            author_name="Juan",
        )
        suggestions = template_reply(req, business_name="Test Shop")
        assert len(suggestions) == 3
        for s in suggestions:
            assert s.text
            assert s.word_count > 5
        assert suggestions[0].tone == "corto"
        assert suggestions[1].tone == "medio"
        assert suggestions[2].tone == "detallado"

    def test_negative_review_uses_negative_templates(self):
        req = ReviewRequest(
            rating=1,
            text="Pésimo servicio, lento y caro. No recomiendo.",
            author_name="Pedro",
        )
        suggestions = template_reply(req, business_name="Test")
        assert len(suggestions) == 3
        # All suggestions should address negative sentiment
        for s in suggestions:
            assert s.sentiment_addressed.value == "negative"

    def test_template_includes_author_name(self):
        req = ReviewRequest(rating=5, text="Buen servicio", author_name="Maria")
        suggestions = template_reply(req, business_name="X")
        # At least one suggestion should mention Maria
        assert any("Maria" in s.text for s in suggestions)

    def test_template_without_author_uses_default_greeting(self):
        req = ReviewRequest(rating=5, text="Buen servicio")
        suggestions = template_reply(req)
        assert len(suggestions) == 3
        # Default greeting should be present
        assert any("amig@" in s.text for s in suggestions)

    def test_template_includes_business_name_in_detailed(self):
        req = ReviewRequest(rating=1, text="malo el servicio", author_name="X")
        suggestions = template_reply(req, business_name="Mi Empresa")
        # Detailed template should mention business
        detailed = [s for s in suggestions if s.tone == "detallado"][0]
        assert "Mi Empresa" in detailed.text or "el equipo" in detailed.text

    def test_all_sentiments_have_3_templates(self):
        """Verify TEMPLATES dict has all 4 sentiments × 3 lengths."""
        for sentiment in Sentiment:
            assert sentiment in TEMPLATES
            assert "corto" in TEMPLATES[sentiment]
            assert "medio" in TEMPLATES[sentiment]
            assert "detallado" in TEMPLATES[sentiment]
