"""LicitAlert — Matching engine (filter tenders by alert rules)."""
from __future__ import annotations
import unicodedata
from decimal import Decimal
from licitalert.core.models import Tender, AlertRule, TenderMatch


def _normalize(text: str) -> str:
    """Normalize text for matching: lowercase + strip accents."""
    text = text.lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return text


def matches_rule(tender: Tender, rule: AlertRule) -> tuple[bool, list[str], int]:
    """Check if a tender matches an alert rule. Returns (matches, matched_keywords, score)."""
    if not rule.active:
        return (False, [], 0)

    # Country filter
    if rule.countries and tender.country not in rule.countries:
        return (False, [], 0)

    # Budget range
    if rule.min_budget is not None and (tender.budget is None or tender.budget < rule.min_budget):
        return (False, [], 0)
    if rule.max_budget is not None and (tender.budget is None or tender.budget > rule.max_budget):
        return (False, [], 0)

    # Category filter
    if rule.categories and tender.category not in rule.categories:
        return (False, [], 0)

    # Normalize full text for matching
    full_text = _normalize(f"{tender.title} {tender.description} {tender.entity} {tender.category}")

    # Exclude keywords (normalize too)
    for excl in rule.exclude_keywords:
        if _normalize(excl) in full_text:
            return (False, [], 0)

    # Keyword matching (normalized)
    matched = []
    if not rule.keywords:
        # Empty keywords = match everything (with low score)
        return (True, [], 1)

    for kw in rule.keywords:
        if _normalize(kw) in full_text:
            matched.append(kw)

    if not matched:
        return (False, [], 0)

    # Calculate score: matched_keywords / total_keywords * 100
    score = int((len(matched) / len(rule.keywords)) * 100)
    # Bonus if budget matches
    if rule.min_budget or rule.max_budget:
        score = min(100, score + 10)

    return (True, matched, score)


def find_matches(tenders: list[Tender], rules: list[AlertRule]) -> list[TenderMatch]:
    """Find all tender-rule matches."""
    matches = []
    for tender in tenders:
        for rule in rules:
            matched, kws, score = matches_rule(tender, rule)
            if matched:
                matches.append(TenderMatch(
                    tender=tender,
                    rule_id=rule.id,
                    rule_name=rule.name,
                    matched_keywords=kws,
                    score=score,
                ))
    return matches
