"""Tests for the matching engine."""
import pytest
from decimal import Decimal
from datetime import datetime

from licitalert.core.models import Tender, AlertRule, Country, TenderStatus
from licitalert.core.matcher import matches_rule, find_matches


@pytest.fixture
def sample_tender():
    return Tender(
        id="TEST-001",
        country=Country.COLOMBIA,
        title="Desarrollo de software para entidad X",
        description="Sistema de gestión integral",
        entity="Ministerio de Tecnología",
        budget=Decimal("50000000"),
        currency="COP",
        category="servicios",
        status=TenderStatus.OPEN,
    )


@pytest.fixture
def sample_rule():
    return AlertRule(
        id="RULE-001",
        name="Test rule",
        countries=[Country.COLOMBIA],
        keywords=["software", "desarrollo"],
    )


class TestMatchesRule:
    def test_basic_match(self, sample_tender, sample_rule):
        matched, kws, score = matches_rule(sample_tender, sample_rule)
        assert matched is True
        assert "software" in kws
        assert "desarrollo" in kws
        assert score == 100

    def test_country_filter_no_match(self, sample_tender, sample_rule):
        sample_rule.countries = [Country.ECUADOR]
        matched, _, _ = matches_rule(sample_tender, sample_rule)
        assert matched is False

    def test_no_keywords_matches_all(self, sample_tender):
        rule = AlertRule(id="X", name="All", countries=[Country.COLOMBIA], keywords=[])
        matched, kws, score = matches_rule(sample_tender, rule)
        assert matched is True
        assert kws == []
        assert score >= 1

    def test_budget_min_filter(self, sample_tender, sample_rule):
        sample_rule.min_budget = Decimal("100000000")
        matched, _, _ = matches_rule(sample_tender, sample_rule)
        assert matched is False  # tender budget is 50M COP

    def test_budget_max_filter(self, sample_tender, sample_rule):
        sample_rule.max_budget = Decimal("10000000")
        matched, _, _ = matches_rule(sample_tender, sample_rule)
        assert matched is False

    def test_exclude_keywords(self, sample_tender, sample_rule):
        sample_rule.exclude_keywords = ["ministerio"]
        matched, _, _ = matches_rule(sample_tender, sample_rule)
        assert matched is False

    def test_no_keyword_match(self, sample_tender, sample_rule):
        sample_rule.keywords = ["construccion", "obra"]
        matched, kws, score = matches_rule(sample_tender, sample_rule)
        assert matched is False
        assert kws == []

    def test_partial_keyword_match(self, sample_tender):
        rule = AlertRule(id="X", name="X", keywords=["software", "construccion"])
        matched, kws, score = matches_rule(sample_tender, rule)
        assert matched is True
        assert "software" in kws
        assert "construccion" not in kws
        assert score == 50  # 1 out of 2 keywords


class TestFindMatches:
    def test_multiple_tenders_multiple_rules(self, sample_tender, sample_rule):
        tender2 = Tender(
            id="TEST-002",
            country=Country.ECUADOR,
            title="Construcción de puente",
            entity="Ministerio de Obras",
            budget=Decimal("500000"),
            currency="USD",
        )
        rule2 = AlertRule(id="R2", name="Construction", countries=[Country.ECUADOR], keywords=["construccion"])
        matches = find_matches([sample_tender, tender2], [sample_rule, rule2])
        # tender1 matches rule1, tender2 matches rule2
        assert len(matches) == 2

    def test_no_matches_returns_empty(self, sample_tender):
        rule = AlertRule(id="X", name="No match", keywords=["xyz123"])
        matches = find_matches([sample_tender], [rule])
        assert matches == []
