"""LicitAlert — JSON-backed store for tenders and alert rules."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from licitalert.core.config import get_settings
from licitalert.core.models import Tender, AlertRule, Country, TenderStatus


class AlertStore:
    """JSON-based persistence."""

    def __init__(self):
        self.s = get_settings()

    @property
    def base_path(self) -> Path:
        return self.s.data_path

    def _file(self, name: str) -> Path:
        p = self.base_path / f"{name}.json"
        if not p.exists():
            p.write_text("[]", encoding="utf-8")
        return p

    def _load(self, name: str) -> list[dict]:
        return json.loads(self._file(name).read_text(encoding="utf-8"))

    def _save(self, name: str, data: list[dict]):
        self._file(name).write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

    # Alert rules
    def list_rules(self) -> list[AlertRule]:
        rules = []
        for r in self._load("rules"):
            r["countries"] = [Country(c) for c in r.get("countries", [])]
            rules.append(AlertRule(**r))
        return rules

    def save_rule(self, rule: AlertRule) -> AlertRule:
        rules = self._load("rules")
        rules = [r for r in rules if r["id"] != rule.id]
        d = rule.model_dump()
        d["countries"] = [c.value for c in rule.countries]
        rules.append(d)
        self._save("rules", rules)
        return rule

    def delete_rule(self, rule_id: str) -> bool:
        rules = self._load("rules")
        before = len(rules)
        rules = [r for r in rules if r["id"] != rule_id]
        if len(rules) < before:
            self._save("rules", rules)
            return True
        return False

    # Tenders cache
    def list_tenders(self, country: str = None, limit: int = 100) -> list[Tender]:
        tenders = []
        for t in self._load("tenders"):
            t["country"] = Country(t.get("country", "ec"))
            t["status"] = TenderStatus(t.get("status", "unknown"))
            if t.get("budget"):
                from decimal import Decimal
                t["budget"] = Decimal(str(t["budget"]))
            if t.get("published_at") and isinstance(t["published_at"], str):
                t["published_at"] = datetime.fromisoformat(t["published_at"])
            if t.get("deadline") and isinstance(t["deadline"], str):
                t["deadline"] = datetime.fromisoformat(t["deadline"])
            tenders.append(Tender(**t))
        if country:
            tenders = [t for t in tenders if t.country.value == country]
        return tenders[:limit]

    def save_tender(self, tender: Tender) -> Tender:
        tenders = self._load("tenders")
        # Avoid duplicates
        if any(t["id"] == tender.id and t.get("country") == tender.country.value for t in tenders):
            return tender
        d = tender.model_dump()
        d["country"] = tender.country.value
        d["status"] = tender.status.value
        if tender.budget:
            d["budget"] = str(tender.budget)
        if tender.published_at:
            d["published_at"] = tender.published_at.isoformat()
        if tender.deadline:
            d["deadline"] = tender.deadline.isoformat()
        tenders.append(d)
        # Cap to last 1000
        if len(tenders) > 1000:
            tenders = tenders[-1000:]
        self._save("tenders", tenders)
        return tender

    def is_seen(self, tender_id: str, country: str) -> bool:
        return any(t["id"] == tender_id and t.get("country") == country for t in self._load("tenders"))
