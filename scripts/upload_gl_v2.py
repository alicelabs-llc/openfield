import json, ssl, time, base64, urllib.request, urllib.error

TOKEN = "glpat-PfWyLHoeZpLOyyQSzyDX72M6MQpvOjEKdTpranZqbQ8.01.1715hm5mn"
FORK_PID = 87979492
UPSTREAM_PID = 8551643
BRANCH = "fix/migrate-deprecated-openssl-apis"
CTX = ssl.create_default_context()
headers = {"PRIVATE-TOKEN": TOKEN, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

# Read the file
with open("/home/z/my-project/contrib-libvmod/fork/src/vmod_crypto.c", "rb") as f:
    content = base64.b64encode(f.read()).decode()

# File already exists — need PUT instead of POST to update it
print("=== Upload file via Contents API (PUT to update) ===")
payload = {
    "branch": BRANCH,
    "content": content,
    "commit_message": "fix: migrate from deprecated OpenSSL RSA APIs to EVP_PKEY_fromdata",
    "encoding": "base64",
}
data = json.dumps(payload).encode()

for attempt in range(5):
    try:
        req = urllib.request.Request(
            f"https://gitlab.com/api/v4/projects/{FORK_PID}/repository/files/src%2Fvmod_crypto.c",
            data=data,
            headers={**headers, "Content-Type": "application/json"},
            method="PUT"
        )
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            d = json.loads(resp.read().decode())
            print(f"  ✅ File updated: {d.get('file_path')}")
            print(f"  branch: {d.get('branch')}")
            break
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  Attempt {attempt+1}: HTTP {e.code}: {body[:200]}")
        time.sleep(15)
    except Exception as e:
        print(f"  Attempt {attempt+1}: {e}")
        time.sleep(15)
else:
    print("  ❌ Failed to update file")
    exit(1)

# Create MR
print("\n=== Create MR ===")
time.sleep(10)
mr_payload = {
    "title": "fix: migrate from deprecated OpenSSL RSA APIs to EVP_PKEY_fromdata",
    "source_branch": BRANCH,
    "target_branch": "master",
    "target_project_id": UPSTREAM_PID,
    "description": "Closes !5.\n\nOpenSSL 3.0 deprecated RSA_new, RSA_set0_key, EVP_PKEY_assign_RSA, RSA_free. Replaced with EVP_PKEY_fromdata API using OSSL_PARAM. Uses #if OPENSSL_VERSION_NUMBER guards for backward compat.",
}
data = json.dumps(mr_payload).encode()

for attempt in range(5):
    try:
        req = urllib.request.Request(
            f"https://gitlab.com/api/v4/projects/{FORK_PID}/merge_requests",
            data=data,
            headers={**headers, "Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            d = json.loads(resp.read().decode())
            print(f"  ✅ MR !{d['iid']}: {d['web_url']}")
            break
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  Attempt {attempt+1}: HTTP {e.code}: {body[:200]}")
        time.sleep(15)
    except Exception as e:
        print(f"  Attempt {attempt+1}: {e}")
        time.sleep(15)
