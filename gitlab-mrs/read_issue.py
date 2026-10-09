import json, urllib.request, ssl, time

TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
HEADERS = {
    "PRIVATE-TOKEN": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
}
CTX = ssl.create_default_context()

def graphql(query, delay=30, retries=3):
    for attempt in range(retries):
        time.sleep(delay)
        data = json.dumps({"query": query}).encode('utf-8')
        req = urllib.request.Request("https://gitlab.com/api/graphql", data=data, headers=HEADERS, method="POST")
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if e.code == 403 and attempt < retries - 1:
                delay = delay * 2
                continue
            raise

def read_issue(project_path, iid):
    q = '{ project(fullPath: "%s") { issue(iid: "%s") { title description } } }' % (project_path, iid)
    return graphql(q, delay=30)

if __name__ == "__main__":
    import sys
    project = sys.argv[1]
    iid = sys.argv[2]
    try:
        r = read_issue(project, iid)
        proj = r.get("data", {}).get("project", {})
        issue = proj.get("issue", {}) if proj else {}
        print("TITLE:", issue.get("title"))
        print("---DESCRIPTION---")
        print(issue.get("description"))
    except Exception as e:
        print("ERROR:", e)
