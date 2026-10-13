# ============================================================
# HACKTOBERFEST SCRIPT 3 — Prism-platform #388 (md5 → sha256)
# ============================================================
# Repo: https://github.com/NovaCode37/Prism-platform
# Issue: #388 — Hash cache filenames with sha256 instead of MD5
# Fix: 1 archivo Python (web/app.py), 2 funciones cambiadas

$ErrorActionPreference = "Stop"
$workspace = "C:\Users\Usuario\hacktoberfest-prism"
New-Item -ItemType Directory -Path $workspace -Force | Out-Null
Set-Location $workspace

if (Test-Path Prism-platform) { Remove-Item Prism-platform -Recurse -Force }
gh repo clone NovaCode37/Prism-platform Prism-platform
Set-Location Prism-platform
git checkout -b fix/388-md5-to-sha256-cache-filenames

$pyPath = "web\app.py"
$bytes = [System.IO.File]::ReadAllBytes("$PWD\$pyPath")
$content = [System.Text.Encoding]::UTF8.GetString($bytes)

# Fix 1: _cache_key
$content = $content.Replace(
    'def _cache_key(module: str, target: str) -> str:
    import hashlib
    h = hashlib.md5(f"{module}:{target.lower().strip()}".encode()).hexdigest()
    return os.path.join(_CACHE_DIR, f"{module}_{h}.json")',
    'def _cache_key(module: str, target: str) -> str:
    import hashlib
    # Use sha256 for cache filenames: md5 is no longer considered
    # collision-resistant and some hardened environments (Fedora, FIPS mode)
    # outright block it. SHA-256 produces a longer hex digest (64 chars vs
    # 32) but filesystems handle that fine and it costs nothing. Old cache
    # files written with md5 will simply be re-generated on first request,
    # there is no migration to run.
    h = hashlib.sha256(f"{module}:{target.lower().strip()}".encode()).hexdigest()
    return os.path.join(_CACHE_DIR, f"{module}_{h}.json")')

# Fix 2: _geocode_place
$content = $content.Replace(
    'def _geocode_place(query: str) -> Optional[Dict]:
    import hashlib
    cache_path = os.path.join(_CACHE_DIR, "geocode_" + hashlib.md5(query.lower().encode()).hexdigest() + ".json")',
    'def _geocode_place(query: str) -> Optional[Dict]:
    import hashlib
    # See _cache_key(): switched from md5 to sha256 for collision-resistance
    # and FIPS-mode compatibility. Old geocode_<md5hex>.json files will be
    # re-fetched on first lookup since the new sha256-based filename will
    # not match any existing file.
    cache_path = os.path.join(_CACHE_DIR, "geocode_" + hashlib.sha256(query.lower().encode()).hexdigest() + ".json")')

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText("$PWD\$pyPath", $content, $utf8NoBom)

git diff --stat
git add $pyPath
git -c user.name="Edison Flores" -c user.email="eddyflores100-lang@protonmail.com" commit -m "cache: hash filenames with sha256 instead of md5" -m "Closes #388." -m "The two on-disk caches in web/app.py — _cache_key() for module results and _geocode_place() for geocoded coordinates — were keyed on hashlib.md5(...) of the request. MD5 is no longer considered collision-resistant and a number of hardened environments block it outright (Fedora 36+, FIPS mode, OpenSSL 3 in strict mode). Switch both to hashlib.sha256(...). SHA-256 is a drop-in replacement here because the digest is only used as a hex string in a filename — its 64-char length is well within filesystem limits and there is no parsing logic to update. Old cache files written with md5 will simply be re-generated on first request; there is no migration to run and no data loss. Per-issue request: do not change gravatar.py (gravatar API mandates md5) or any other usage that depends on md5 for an externally-defined protocol — only the local cache keys change here."

gh repo fork NovaCode37/Prism-platform --clone=false
git remote rename origin upstream 2>$null
git remote remove origin 2>$null
git remote add origin "https://github.com/eddyflores100-lang/Prism-platform.git"
git push -u origin fix/388-md5-to-sha256-cache-filenames

gh pr create --repo NovaCode37/Prism-platform --base main --head eddyflores100-lang:fix/388-md5-to-sha256-cache-filenames --title "cache: hash filenames with sha256 instead of md5" --body "Closes #388. Switch the two on-disk cache key functions (_cache_key and _geocode_place) from hashlib.md5 to hashlib.sha256. Drop-in replacement — digest is only used as a filename, no parsing logic to update. Old md5-based cache files will be regenerated on first request. Per-issue request, no changes to gravatar.py (gravatar API mandates md5)."
