import json, urllib.request, ssl

TOKEN = "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"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

def api(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

body = """Closes #446.

## Summary

Nothing in `tests/` previously called the endpoints that serve a finished scan — the API most users (and the browser extension) actually use. This adds `tests/test_scan_endpoints.py` covering all six GET endpoints:

```
GET /api/scan/{scan_id}                  web/app.py:879
GET /api/scan/{scan_id}/graph            web/app.py:893
GET /api/scan/{scan_id}/graph/export    web/app.py:903
GET /api/scan/{scan_id}/map              web/app.py:926
GET /api/scan/{scan_id}/report           web/app.py:1056
GET /api/scan/{scan_id}/report/pdf       web/app.py:1078
```

## Coverage

For each endpoint, four cases:

- **200 + correct content-type** for a known id owned by the calling principal.
- **404** for an unknown but well-formed (uuid-shaped) id (note: 404, not 400 — `validate_scan_id` accepts it, the lookup just returns None).
- **400** for a malformed id that `validate_scan_id` rejects (e.g. `not-a-uuid`).
- **404 for a known id owned by ANOTHER principal** — this is the access-control test the issue specifically asked for, covering `_scan_visible_to` in `web/app.py:249`, which until now had no test.

The `/graph/export` endpoint also gets:
- 200 + `application/graphml+xml` content-type for `fmt=graphml`
- 200 + `application/gexf+xml` content-type for `fmt=gexf`
- 400 for an unsupported format (e.g. `fmt=csv`)

The `/report/pdf` endpoint needs `xhtml2pdf` (a heavy dep that CI installs but a local checkout may not have). That test is skipped cleanly via `pytest.importorskip("xhtml2pdf")` rather than letting it error out, exactly as the issue spec asked.

## Fixture

Seeded directly into the in-memory `_scans` dict — no module runs, no network is hit. The fixture dict mirrors the shape that `start_scan` builds in `web/app.py:857` (around line 857), with `status="completed"` and a small `results` payload that includes a graph and a geoip entry so the `/graph` and `/map` endpoints have something to return. The `opsec_score` is shaped per `OpsecScorer.calculate()` in `modules/opsec_score.py`.

Two distinct API keys are configured via `API_KEYS`, so the access-control test gets two real, different `_principal_from_key()` hashes (one per principal).

## Run

```
$ pytest tests/test_scan_endpoints.py -q
27 passed in 1.98s
```

File is 27 tests, runs in <2s offline — matches the issue's "Done when the file runs offline in a few seconds and covers every row above."

## Notes

- I left a clarifying comment on the access-control test (`test_get_scan_returns_404_for_other_owners_scan`) explaining why the contract is 404 and not 403 — so a probing attacker cannot even learn whether a given scan_id exists.
- The `results` dict in the fixture does not include `report_path` (which the GET `/api/scan` endpoint strips out), so the strip is exercised implicitly by the 200 test.
- I deliberately did **not** add a `conftest.py` — `tests/test_cors_order.py` already establishes the pattern of loading `web.app` via `importlib.import_module` after wiping env vars per-test, and this file follows the same pattern for consistency.
"""

payload = {
    "title": "tests: cover scan-result endpoints (6 endpoints, access control)",
    "head": "eddyflores100-lang:fix/446-scan-endpoint-tests",
    "base": "main",
    "body": body,
}
code, d = api("POST", "https://api.github.com/repos/NovaCode37/Prism-platform/pulls", payload)
print(f"HTTP {code}")
if code in (200, 201):
    print(f"PR #{d['number']} created: {d['html_url']}")
    print(f"  state: {d['state']}  draft: {d.get('draft',False)}")
    print(f"  mergeable: {d.get('mergeable','?')}  mergeable_state: {d.get('mergeable_state','?')}")
else:
    print(f"message: {d.get('message','')}")
    if 'errors' in d:
        for e in d['errors']:
            print(f"  - {e.get('message','')}")
