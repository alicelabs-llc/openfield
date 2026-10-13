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

body = """Hi @NovaCode37 — following up on your offer on #530. If #446 is still up for grabs, I'd like to take it.

Quick plan, roughly mirroring the spec above:

1. Add `tests/test_scan_endpoints.py` using `TestClient` (copying the setup from `tests/test_cors_order.py`).
2. Seed a finished scan via a small fixture dict shaped like `start_scan`'s output, written under `_SCANS_DIR` pointed at `tmp_path`.
3. For each of the 6 endpoints: 200 + correct content-type for a known id; 404 for an unknown but valid id; 400 for a malformed id rejected by `validate_scan_id`.
4. Access-control test: a scan owned by principal A must 404 for principal B (covers `_scan_visible_to`).
5. Skip `/report/pdf` cleanly if `xhtml2pdf` import fails (CI installs it, local devs may not).

Will aim to keep the file under ~150 lines and runnable in <5s offline. If anything in the plan above doesn't match what you had in mind, happy to adjust before opening the PR.

Could you assign me so it doesn't get picked up twice?"""

code, d = api("POST", "https://api.github.com/repos/NovaCode37/Prism-platform/issues/446/comments", {"body": body})
print(f"HTTP {code}")
if code == 201:
    print(f"Comment id: {d.get('id')}")
    print(f"URL: {d.get('html_url')}")
else:
    print(d)
