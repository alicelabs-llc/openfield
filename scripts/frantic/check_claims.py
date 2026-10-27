import json, urllib.request, ssl, sys, time

AGENT_TOKEN = "fr_agent_e6c0b469a385ff32b00d44fafa0a39d8c9a273bce5a8cbf0"
BASE = "https://gofrantic.com/v1"
UA = "MarketNow-UTA-Trust-Agent/1.0"
CTX = ssl.create_default_context()

CLAIMS = {
    "140": "080363af-612e-435b-99f2-b4ba540766cf",
    "97":  "57bad783-abfa-4be6-96c3-2128de71cff3",
}

def get(path):
    url = f"{BASE}{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {AGENT_TOKEN}",
        "User-Agent": UA,
        "Accept": "application/json",
    }, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:600]
        return e.code, {"error": body}
    except Exception as e:
        return 0, {"error": str(e)}

for bounty, cid in CLAIMS.items():
    code, data = get(f"/claims/{cid}")
    print(f"=== Claim #{bounty} (id {cid}) ===")
    print(f"HTTP {code}")
    print(json.dumps(data, indent=2)[:2000])
    print()
