"""Tests for template-based post generator."""
import pytest
from postfactory.core.models import PostRequest, Platform, ContentType
from postfactory.templates import generate_posts, TEMPLATES, BEST_TIMES


class TestGeneratePosts:
    def test_educational_returns_variations(self):
        req = PostRequest(
            topic="marketing digital",
            platform=Platform.INSTAGRAM,
            content_type=ContentType.EDUCATIONAL,
            variations=3,
        )
        posts = generate_posts(req)
        assert len(posts) == 3
        for p in posts:
            assert p.text
            assert p.word_count > 5
            assert p.platform == Platform.INSTAGRAM
            assert p.content_type == ContentType.EDUCATIONAL

    def test_includes_hashtags_when_requested(self):
        req = PostRequest(topic="test topic", include_hashtags=True, variations=1)
        posts = generate_posts(req)
        assert len(posts[0].hashtags) > 0

    def test_excludes_hashtags_when_requested(self):
        req = PostRequest(topic="test topic", include_hashtags=False, variations=1)
        posts = generate_posts(req)
        assert posts[0].hashtags == []

    def test_strip_emojis_when_disabled(self):
        req = PostRequest(topic="test topic", include_emojis=False, variations=1)
        posts = generate_posts(req)
        assert posts[0].emoji_count == 0

    def test_uses_user_key_points(self):
        req = PostRequest(
            topic="productivity tips",
            key_points=["tip 1 custom", "tip 2 custom", "tip 3 custom"],
            variations=1,
        )
        posts = generate_posts(req)
        # At least one of the custom points should appear in the text
        assert "tip 1 custom" in posts[0].text

    def test_best_posting_time_set(self):
        req = PostRequest(topic="test topic", platform=Platform.LINKEDIN, variations=1)
        posts = generate_posts(req)
        assert posts[0].best_posting_time  # not empty

    def test_image_prompt_set(self):
        req = PostRequest(topic="AI tools", variations=1)
        posts = generate_posts(req)
        assert "AI tools" in posts[0].suggested_image_prompt

    def test_all_content_types_have_templates(self):
        for ct in ContentType:
            assert ct in TEMPLATES, f"Missing templates for {ct}"
            assert len(TEMPLATES[ct]) >= 2

    def test_all_platforms_have_best_times(self):
        for p in Platform:
            assert p in BEST_TIMES
