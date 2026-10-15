import json, urllib.request, ssl

TOKEN = "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"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

body = """## Summary

The repo had **no automated tests, no CI, no requirements.txt, and could not be imported as a Python package** (no `__init__.py`). This PR fixes all four gaps and improves the README.

## What changed

### 1. `tests/` — 41 pytest tests (offline, <0.5s)

- `tests/test_enricher_core.py` (35 tests): `EnrichedCompany` dataclass (defaults, 37-field contract), `clean_email` (skip-list, length, regex, edge cases), `clean_phone` (US + international normalization), `extract_domain` (subdomain handling, malformed input), `is_valid_website`, `get_cache_key` (determinism, uniqueness), and `run_enrichment` (empty input, optional `progress_callback`, optional `stop_flag`).
- `tests/test_email_warmer.py` (2 tests): module imports cleanly, exposes usable symbols.
- `tests/test_imports.py` (4 tests): every top-level module imports without raising; `run_enrichment` and `EnrichedCompany` are callable.
- `tests/conftest.py`: adds repo root to `sys.path` so tests work from any CWD.

### 2. `.github/workflows/ci.yml` — GitHub Actions matrix

- Python 3.10, 3.11, 3.12 on ubuntu-latest
- Installs `requirements.txt` + pytest
- Runs the full suite + a smoke import test as a final gate
- Triggers on push to main and on PRs to main

### 3. `requirements.txt`

Pins the deps the README already mentioned but never committed:

```
customtkinter>=5.2.0
openpyxl>=3.1.0
requests>=2.31.0
beautifulsoup4>=4.12.0
aiohttp>=3.9.0
pandas>=2.0.0
brotli>=1.1.0
```

`brotli` was previously documented only in the old PR #1 description as "the missing dep required for aiohttp to decode search engine responses" — now it's explicit.

### 4. `__init__.py` — package-init

Makes the repo importable as a Python package. Exposes `EnrichedCompany` and `run_enrichment` as the public API:

```python
from nexuscold import EnrichedCompany, run_enrichment
```

### 5. `.gitignore`

Expanded to cover virtual envs (`.venv/`, `venv/`), IDE files (`.vscode/`, `.idea/`), build artifacts (`*.exe`, `*.spec`), credentials (`.env`, `.env.local`, `*.key`, `*.pem`), and OS noise (`Thumbs.db`, `.DS_Store`).

### 6. `README.md`

Rewritten with:

- Badges (Python version, license, CI status, test count)
- Install instructions for Linux/macOS (the old one was Windows-only) — including a `.venv` setup
- Usage examples for both the GUI (`python ALICELABS_EXTRACTOR_GUI.py`) and as a library (`from enricher_core import ...`)
- Tests section: `pytest tests/ -v`
- Architecture diagram of `enricher_core.py` (EnrichedCompany → Helpers → Cache → Rate-limiting → Sources → AI heuristic → Orchestration)
- Country-coverage table (USA/UK/EU/MX/BR/AU/IN/Latam with tax IDs and primary sources)
- Usage caveats: CAN-SPAM/GDPR/LGPD compliance, robots.txt respect, legitimate email warming only

## Verification

```
$ pip install -r requirements.txt
$ pip install pytest pytest-asyncio
$ pytest tests/ -v
============================== 41 passed in 0.46s ==============================

$ python -c "from enricher_core import EnrichedCompany, run_enrichment; print('OK')"
OK
```

## Files touched

- `tests/__init__.py`, `tests/conftest.py`, `tests/test_enricher_core.py`, `tests/test_email_warmer.py`, `tests/test_imports.py` — new (41 tests)
- `.github/workflows/ci.yml` — new
- `requirements.txt` — new
- `__init__.py` — new
- `.gitignore` — expanded
- `README.md` — rewritten

## Notes

- All tests are **offline** (no network calls) — they verify dataclass contracts, helper functions, and the empty-input path of `run_enrichment`. Adding integration tests against live search engines would require rate-limit handling and fixtures for HTML responses; that's a follow-up.
- I deliberately did **not** change any behavior in `enricher_core.py` or `email_warmer.py`. This PR is pure additive infrastructure (tests + CI + packaging). Behavioral changes / bug fixes should go in separate PRs so they can be reviewed on their own merits.
- The fork `eddyflores100-lang/NexusCold-1` was created fresh because the existing fork was tied to the older `eddyflores100-lang/NexusCold` repo (now archived as historical backup per its README banner).
"""

payload = {
    "title": "ci: add pytest suite, GitHub Actions, requirements.txt, package init",
    "head": "eddyflores100-lang:ci-tests-packaging",
    "base": "main",
    "body": body,
}
req = urllib.request.Request(
    "https://api.github.com/repos/alicelabs-llc/NexusCold/pulls",
    data=json.dumps(payload).encode(),
    headers=HEADERS,
    method="POST",
)
try:
    with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
        d = json.loads(resp.read().decode())
    print(f"HTTP {resp.status} - PR #{d.get('number')} created")
    print(f"  URL: {d.get('html_url')}")
    print(f"  state: {d.get('state')}  draft: {d.get('draft',False)}")
    print(f"  mergeable: {d.get('mergeable','?')}  mergeable_state: {d.get('mergeable_state','?')}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:500]}")
