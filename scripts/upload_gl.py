import json, ssl, time, base64, urllib.request, urllib.error

TOKEN = "glpat-PfWyLHoeZpLOyyQSzyDX72M6MQpvOjEKdTpranZqbQ8.01.1715hm5mn"
FORK_PID = 87979492
UPSTREAM_PID = 8551643
BRANCH = "fix/migrate-deprecated-openssl-apis"
CTX = ssl.create_default_context()

# Read the file
with open("/home/z/my-project/contrib-libvmod/fork/src/vmod_crypto.c", "rb") as f:
    content = base64.b64encode(f.read()).decode()

print(f"File size: {len(content)} chars (base64)")

# Step 1: Check if branch exists
print("\n=== Step 1: Check branch exists ===")
headers = {"PRIVATE-TOKEN": TOKEN, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
for attempt in range(3):
    try:
        req = urllib.request.Request(
            f"https://gitlab.com/api/v4/projects/{FORK_PID}/repository/branches/{BRANCH}",
            headers=headers, method="GET"
        )
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            d = json.loads(resp.read().decode())
            print(f"  ✅ Branch exists: {d['name']}")
            break
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:200]}")
        time.sleep(10)
    except Exception as e:
        print(f"  Attempt {attempt+1} failed: {e}")
        time.sleep(10)
else:
    print("  Creating branch...")
    time.sleep(15)
    data = json.dumps({"branch": BRANCH, "ref": "master"}).encode()
    req = urllib.request.Request(
        f"https://gitlab.com/api/v4/projects/{FORK_PID}/repository/branches",
        data=data, headers={**headers, "Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            d = json.loads(resp.read().decode())
            print(f"  ✅ Branch created: {d['name']}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "already exists" in body:
            print("  Branch already exists, continuing...")
        else:
            print(f"  HTTP {e.code}: {body[:200]}")
            exit(1)

# Step 2: Upload the file content
print("\n=== Step 2: Upload file via Contents API ===")
payload = {
    "branch": BRANCH,
    "content": content,
    "commit_message": "fix: migrate from deprecated OpenSSL RSA APIs to EVP_PKEY_fromdata\n\nCloses !5.\n\nOpenSSL 3.0 deprecated RSA_new, RSA_set0_key, EVP_PKEY_assign_RSA, RSA_free.\nReplaced with EVP_PKEY_fromdata API using OSSL_PARAM.\nUses #if OPENSSL_VERSION_NUMBER guards for backward compat with OpenSSL 1.1.",
    "encoding": "base64",
}
data = json.dumps(payload).encode()

for attempt in range(5):
    try:
        req = urllib.request.Request(
            f"https://gitlab.com/api/v4/projects/{FORK_PID}/repository/files/src%2Fvmod_crypto.c",
            data=data,
            headers={**headers, "Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            d = json.loads(resp.read().decode())
            print(f"  ✅ File uploaded: {d.get('file_path')}")
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
    print("  ❌ Failed to upload file after 5 attempts")
    exit(1)

# Step 3: Create the MR
print("\n=== Step 3: Create MR ===")
time.sleep(10)
mr_payload = {
    "title": "fix: migrate from deprecated OpenSSL RSA APIs to EVP_PKEY_fromdata",
    "source_branch": BRANCH,
    "target_branch": "master",
    "target_project_id": UPSTREAM_PID,
    "description": "Closes !5.\n\n## Summary\n\nOpenSSL 3.0 deprecated `RSA_new()`, `RSA_set0_key()`, `EVP_PKEY_assign_RSA()` and `RSA_free()`. These are now replaced with the provider-based `EVP_PKEY_fromdata()` API.\n\n## Approach\n\nUses `#if OPENSSL_VERSION_NUMBER` guards:\n- **OpenSSL >= 3.0**: uses `EVP_PKEY_CTX_new_from_name` + `EVP_PKEY_fromdata` with `OSSL_PARAM` for n/e/d. No RSA_* calls.\n- **OpenSSL < 3.0**: keeps the legacy `RSA_new`/`RSA_set0_key`/`EVP_PKEY_assign_RSA` path (still functional, just deprecated in 3.0).\n\nThe `err_rsa` label is also guarded so `RSA_free` is only called on the legacy path.\n\n## References\n\n- [EVP_PKEY_fromdata docs](https://www.openssl.org/docs/man3.0/man3/EVP_PKEY_fromdata.html)\n- [OpenSSL 3.0 migration guide](https://www.openssl.org/docs/man3.0/man7/migration_guide.html)",
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
            print(f"  ✅ MR !{d['iid']} created: {d['web_url']}")
            break
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  Attempt {attempt+1}: HTTP {e.code}: {body[:200]}")
        time.sleep(15)
    except Exception as e:
        print(f"  Attempt {attempt+1}: {e}")
        time.sleep(15)
else:
    print("  ❌ Failed to create MR after 5 attempts")
