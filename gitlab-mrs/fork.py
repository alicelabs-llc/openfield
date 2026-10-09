import json, urllib.request, ssl, time, sys

TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
BASE = "https://gitlab.com/api/v4"
HEADERS = {
    "PRIVATE-TOKEN": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
}
CTX = ssl.create_default_context()

def api_post(path, payload, delay=30, retries=3):
    for attempt in range(retries):
        time.sleep(delay)
        url = BASE + path
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if e.code in (403, 429) and attempt < retries - 1:
                delay = delay * 2
                continue
            print(f"HTTP {e.code} for {path}: {body[:500]}", file=sys.stderr)
            raise

def api_get(path, delay=0, retries=3):
    for attempt in range(retries):
        time.sleep(delay)
        url = BASE + path
        req = urllib.request.Request(url, headers=HEADERS, method="GET")
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if e.code in (403, 429) and attempt < retries - 1:
                delay = max(delay, 30) * 2
                continue
            print(f"HTTP {e.code} for {path}: {body[:300]}", file=sys.stderr)
            raise

def fork_project(project_id):
    # First check if fork already exists
    try:
        forks = api_get(f"/projects/{project_id}/forks", delay=0)
        for f in forks:
            if f.get("namespace", {}).get("full_path") == "eddyflores100":
                print(f"Fork already exists: id={f['id']} path={f['path_with_namespace']}", flush=True)
                return f
    except Exception as e:
        print(f"check forks: {e}", file=sys.stderr)
    # Create fork
    try:
        r = api_post(f"/projects/{project_id}/fork", {"namespace": "eddyflores100"}, delay=30)
        print(f"Fork created: id={r.get('id')} path={r.get('path_with_namespace')}", flush=True)
        return r
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        # If already exists / taken
        if "has already been taken" in body or e.code == 409:
            forks = api_get(f"/projects/{project_id}/forks", delay=5)
            for f in forks:
                if f.get("namespace", {}).get("full_path") == "eddyflores100":
                    print(f"Fork already exists (taken): id={f['id']} path={f['path_with_namespace']}", flush=True)
                    return f
        print(f"Fork failed: {body[:400]}", file=sys.stderr)
        raise

if __name__ == "__main__":
    pid = sys.argv[1]
    f = fork_project(int(pid))
    # wait for fork to be ready (import_status)
    fork_id = f["id"]
    for i in range(40):
        time.sleep(5)
        try:
            info = api_get(f"/projects/{fork_id}", delay=0)
            status = info.get("import_status")
            print(f"  fork import_status={status}", flush=True)
            if status == "finished":
                break
            if status == "failed":
                print("Fork import failed!", file=sys.stderr)
                break
        except Exception as e:
            print(f"  poll error: {e}", file=sys.stderr)
    print("Fork ready:", f.get("path_with_namespace"), "id=", fork_id, flush=True)
