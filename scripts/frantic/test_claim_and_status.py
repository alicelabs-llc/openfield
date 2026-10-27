import json, urllib.request, ssl, sys

AGENT_TOKEN = "fr_agent_e6c0b469a385ff32b00d44fafa0a39d8c9a273bce5a8cbf0"
BASE = "https://gofrantic.com/v1"
UA = "MarketNow-UTA-Trust-Agent/1.0"
CTX = ssl.create_default_context()

def req(method, path, body=None):
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body else None
    headers = {
        "Authorization": f"Bearer {AGENT_TOKEN}",
        "User-Agent": UA,
        "Accept": "application/json",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error_body": e.read().decode()[:800]}
    except Exception as e:
        return 0, {"error": str(e)}

print("=== Agent status ===")
code, data = req("GET", "/agents/agent-408707/status")
print(f"HTTP {code}")
print(json.dumps(data, indent=2)[:1500])

# Attempt to claim bounty #141 as a probe (won't lose anything — we expect rejection if limit is enforced)
print("\n=== Probe: POST /v1/claims  bounty=141 ===")
code, data = req("POST", "/claims", {"bounty":141,"agent_kid":"agent-408707"})
print(f"HTTP {code}")
print(json.dumps(data, indent=2)[:1500])
