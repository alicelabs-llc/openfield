import json, urllib.request, ssl, time, sys

TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
BASE = "https://gitlab.com/api/v4"
HEADERS = {
    "PRIVATE-TOKEN": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
}
CTX = ssl.create_default_context()

def api_post(path, payload, delay=30, retries=4):
    last_err = None
    for attempt in range(retries):
        time.sleep(delay)
        url = BASE + path
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=40) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            last_err = (e.code, body)
            if e.code in (403, 429, 500, 502, 503) and attempt < retries - 1:
                delay = delay * 2
                continue
            print(f"HTTP {e.code} for {path}: {body[:800]}", file=sys.stderr)
            raise
    raise RuntimeError(f"failed after retries: {last_err}")

if __name__ == "__main__":
    # args: fork_project_id source_branch target_branch target_project_id title description
    fork_pid = int(sys.argv[1])
    source_branch = sys.argv[2]
    target_branch = sys.argv[3]
    target_pid = int(sys.argv[4])
    title = sys.argv[5]
    description = sys.argv[6]
    payload = {
        "source_branch": source_branch,
        "target_branch": target_branch,
        "target_project_id": target_pid,
        "title": title,
        "description": description,
        "remove_source_branch": False,
    }
    r = api_post(f"/projects/{fork_pid}/merge_requests", payload, delay=30)
    print("MR web_url:", r.get("web_url"))
    print("MR iid:", r.get("iid"), "state:", r.get("state"))
    print("MR id:", r.get("id"))
