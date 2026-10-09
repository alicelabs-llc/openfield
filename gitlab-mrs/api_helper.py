import json, urllib.request, ssl, time, http.client

TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
BASE = "https://gitlab.com/api/v4"
HEADERS = {
    "PRIVATE-TOKEN": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "application/json",
}
CTX = ssl.create_default_context()

def raw_get(url, delay=0):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

if __name__ == "__main__":
    for path in ["inkscape%2Finkscape", "inkscape%2Fextensions", "fdroid%2Ffdroidclient"]:
        code, body = raw_get(f"{BASE}/projects/{path}")
        print(f"{path}: HTTP {code}, body[:200]={body[:200]}")
