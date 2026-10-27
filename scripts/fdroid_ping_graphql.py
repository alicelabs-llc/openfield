import json, urllib.request, ssl, time

TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
HEADERS = {
    "PRIVATE-TOKEN": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
    "Accept": "application/json",
}
CTX = ssl.create_default_context()

body = """Friendly ping — the MR has been mergeable with no conflicts since the rebase on 2026-10-13 (commit 7fe864f9, pipeline #2940626084 green: `lint-and-test` on Python 3.10 and 3.11, `CodeQL`, `docker-build`, `frontend`, all success).

I think the open thread above (the comparison with !1721) is resolved: short version is that !1721 (Nardol) goes in the announcement direction and exposes the checkbox role and checked state on the whole item, while this MR suppresses the separate semantics of the purely-visual checkbox — the two changes are deliberately orthogonal and could land independently.

Happy to make further adjustments if anything still needs tweaking. Otherwise no rush, just flagging in case it slipped off the queue."""

# GraphQL mutation to create a note on a merge request
# Need: projectPath, iid
query = """
mutation {
  createNote(input: {
    noteableId: "gid://gitlab/MergeRequest/1786"
    body: %s
  }) {
    note {
      id
      body
      createdAt
      author { username }
    }
    errors
  }
}
""" % json.dumps(body)

# Actually, the noteableId needs the global ID which includes the project.
# Let me try the simpler REST approach with a fresh delay strategy.
# Or use GraphQL with the project namespace.

# Try createNoteMutation with the merge request global id
# First, get the merge request global id
print("=== Step 1: Get MR global ID via GraphQL ===")
time.sleep(15)
q1 = """{
  project(fullPath: "fdroid/fdroidclient") {
    mergeRequest(iid: "1786") {
      id
      title
      state
    }
  }
}"""
req = urllib.request.Request(
    "https://gitlab.com/api/graphql",
    data=json.dumps({"query": q1}).encode(),
    headers=HEADERS,
    method="POST",
)
try:
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        d = json.loads(resp.read().decode())
    if not d.get("data", {}).get("project"):
        print(f"  No project data: {d}")
        exit(1)
    mr = d["data"]["project"]["mergeRequest"]
    mr_global_id = mr["id"]
    print(f"  MR global id: {mr_global_id}")
    print(f"  title: {mr['title'][:80]}")
    print(f"  state: {mr['state']}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code}: {e.read().decode()[:300]}")
    exit(1)
except Exception as e:
    print(f"  ERR: {e}")
    exit(1)

# Step 2: Create the note via GraphQL
print("\n=== Step 2: Create note via GraphQL mutation ===")
time.sleep(20)
q2 = """
mutation CreateNote($input: CreateNoteInput!) {
  createNote(input: $input) {
    note {
      id
      body
      createdAt
      author { username }
    }
    errors
  }
}
"""
variables = {
    "input": {
        "noteableId": mr_global_id,
        "body": body,
    }
}
req = urllib.request.Request(
    "https://gitlab.com/api/graphql",
    data=json.dumps({"query": q2, "variables": variables}).encode(),
    headers=HEADERS,
    method="POST",
)
try:
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        d = json.loads(resp.read().decode())
    if d.get("errors"):
        print(f"  GraphQL errors: {d['errors']}")
    result = d.get("data", {}).get("createNote", {})
    if result.get("errors"):
        print(f"  Mutation errors: {result['errors']}")
    if result.get("note"):
        n = result["note"]
        print(f"  ✅ Note created!")
        print(f"  id: {n.get('id')}")
        print(f"  author: {n.get('author',{}).get('username')}")
        print(f"  createdAt: {n.get('createdAt')}")
        print(f"  body preview: {n.get('body','')[:200]}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code}: {e.read().decode()[:300]}")
except Exception as e:
    print(f"  ERR: {e}")
