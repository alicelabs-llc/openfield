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
    # args: project_id branch start_branch commit_message action_spec_file
    project_id = int(sys.argv[1])
    branch = sys.argv[2]
    start_branch = sys.argv[3]
    commit_message = sys.argv[4]
    spec_file = sys.argv[5]
    # spec_file is JSON: list of {file_path, content_path}
    with open(spec_file) as f:
        specs = json.load(f)
    actions = []
    for s in specs:
        with open(s["content_path"]) as f:
            content = f.read()
        actions.append({"action": "update", "file_path": s["file_path"], "content": content})
    payload = {"branch": branch, "commit_message": commit_message, "start_branch": start_branch, "actions": actions}
    r = api_post(f"/projects/{project_id}/repository/commits", payload, delay=30)
    print("commit sha:", r.get("id"), "short:", r.get("short_id"), "branch:", branch)
