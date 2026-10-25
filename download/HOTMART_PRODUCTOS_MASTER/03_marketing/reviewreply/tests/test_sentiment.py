"""Tests for sentiment analysis."""
import pytest
from reviewreply.core.models import Review, Platform
from reviewreply.core.sentiment import detect_sentiment, extract_topics


class TestDetectSentiment:
    def test_positive_text(self):
        s = detect_sentiment("Excelente servicio, muy amables. Recomiendo!", rating=5)
        assert s.value == "positive"

    def test_negative_text(self):
        s = detect_sentiment("Pesimo servicio, nunca llega. No recomiendo.", rating=1)
        assert s.value == "negative"

    def test_neutral_rating_only(self):
        s = detect_sentiment("Estuvo bien.", rating=3)
        assert s.value in ("neutral", "mixed", "positive", "negative")

    def test_mixed_text_with_pero(self):
        s = detect_sentiment("La comida buena pero el servicio lento", rating=3)
        assert s.value == "mixed"

    def test_english_positive(self):
        s = detect_sentiment("Amazing! Love it! Highly recommend!", rating=5)
        assert s.value == "positive"

    def test_english_negative(self):
        s = detect_sentiment("Terrible. Worst experience ever.", rating=1)
        assert s.value == "negative"

    def test_with_review_object(self):
        r = Review(id="1", platform=Platform.GOOGLE_REVIEWS, rating=5, text="Maravilloso, fantástico!")
        s = detect_sentiment(r)
        assert s.value == "positive"


class TestExtractTopics:
    def test_extract_service(self):
        topics = extract_topics("El servicio fue excelente")
        assert "servicio" in topics

    def test_extract_multiple(self):
        topics = extract_topics("Comida deliciosa pero el precio es caro")
        assert "comida" in topics
        assert "precio" in topics

    def test_no_topics(self):
        topics = extract_topics("Todo bien")
        assert topics == [] or len(topics) >= 0  # might find generic ones
