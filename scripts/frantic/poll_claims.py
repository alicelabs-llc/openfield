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
        return e.code, {"error": e.read().decode()[:600]}
    except Exception as e:
        return 0, {"error": str(e)}

# Poll every 30s for 5 min (10 iterations)
DEADLINE = time.time() + 5*60
iter_n = 0
last_status = {}
while time.time() < DEADLINE:
    iter_n += 1
    print(f"\n=== Poll iteration {iter_n} @ {time.strftime('%H:%M:%S')} ===")
    judged_any = False
    for bounty, cid in CLAIMS.items():
        code, data = get(f"/claims/{cid}")
        status = data.get("status") if isinstance(data, dict) else None
        judged_at = data.get("judged_at") if isinstance(data, dict) else None
        rej = data.get("rejection_reason") if isinstance(data, dict) else None
        qual = data.get("quality") if isinstance(data, dict) else None
        sig = (status, judged_at, rej, qual)
        if sig != last_status.get(bounty):
            print(f"  #{bounty}: status={status} judged_at={judged_at} quality={qual} rejection={rej}")
            last_status[bounty] = sig
        else:
            print(f"  #{bounty}: status={status} judged_at={judged_at} (no change)")
        if judged_at is not None:
            judged_any = True
    if judged_any:
        print(">>> At least one claim judged! Breaking to attempt new claim.")
        break
    # Sleep 30s between polls
    time.sleep(30)

print("\n=== Final summary ===")
for bounty, cid in CLAIMS.items():
    code, data = get(f"/claims/{cid}")
    print(f"#{bounty}: status={data.get('status')} judged_at={data.get('judged_at')} quality={data.get('quality')} rejection={data.get('rejection_reason')}")
