"""Tests for hashtag generator."""
import pytest
from postfactory.core.hashtags import generate_hashtags, _slugify, NICHE_HASHTAGS, PLATFORM_HASHTAG_LIMITS
from postfactory.core.models import Platform


class TestSlugify:
    def test_basic(self):
        assert _slugify("Hola Mundo") == "holamundo"

    def test_accents(self):
        assert _slugify("Atención al Cliente") == "atencionalcliente"

    def test_special_chars(self):
        assert _slugify("Hello! World? #2026") == "helloworld2026"


class TestGenerateHashtags:
    def test_marketing_niche(self):
        tags = generate_hashtags("marketing digital", "marketing", Platform.INSTAGRAM)
        assert len(tags) > 0
        assert any("marketing" in t for t in tags)

    def test_topic_in_hashtags(self):
        tags = generate_hashtags("fitness motivation", "fitness", Platform.INSTAGRAM)
        assert any("fitness" in t for t in tags)

    def test_platform_limit(self):
        # LinkedIn max is 5
        tags = generate_hashtags("marketing", "marketing", Platform.LINKEDIN, count=20)
        assert len(tags) <= 5

    def test_twitter_limit(self):
        tags = generate_hashtags("tech news", "tecnologia", Platform.TWITTER, count=20)
        assert len(tags) <= 3

    def test_unknown_niche_uses_default(self):
        tags = generate_hashtags("random topic", "unknown_niche_xyz", Platform.INSTAGRAM)
        assert len(tags) > 0

    def test_all_niches_have_pool(self):
        for niche, pool in NICHE_HASHTAGS.items():
            assert len(pool) > 0, f"Empty pool for {niche}"

    def test_all_platforms_have_limit(self):
        for platform in Platform:
            assert platform in PLATFORM_HASHTAG_LIMITS

    def test_deduplication(self):
        tags = generate_hashtags("marketing marketing marketing", "marketing", Platform.INSTAGRAM)
        # No duplicates
        assert len(tags) == len(set(tags))
