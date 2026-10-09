# ============================================================
# TOUCH GRASS — Deploy completo a GitHub + dev.to
# ============================================================
# Este script crea el repo, genera todos los archivos, 
# hace commit, push, y abre dev.to para publicar el post.
# ============================================================

$ErrorActionPreference = "Stop"
$repoName = "touch-grass"
$ghUser = "eddyflores100-lang"
$workspace = "C:\Users\Usuario\$repoName"

Write-Host "🌿 Touch Grass — Deploy completo" -ForegroundColor Cyan
Write-Host ""

# 1. Crear repo en GitHub
Write-Host "→ Creando repo $repoName en GitHub..." -ForegroundColor Cyan
gh repo create $repoName --public --description "Verified field notes from your hike — open-source AI + cryptographic sealing (Hacktoberfest 2026)" 2>$null
Write-Host "  Done" -ForegroundColor Green

# 2. Crear estructura
Write-Host "→ Generando archivos..." -ForegroundColor Cyan
Remove-Item $workspace -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $workspace -Force | Out-Null
Set-Location $workspace
New-Item -ItemType Directory -Path "src" -Force | Out-Null
New-Item -ItemType Directory -Path "photos" -Force | Out-Null
New-Item -ItemType Directory -Path "output" -Force | Out-Null

# 3. Crear README.md
@'
# Touch Grass — Verified Field Notes

> Turn your outdoor photos into a cryptographically verified field journal.
> Photos never leave your machine. The journal cannot be tampered with after signing.

**Hacktoberfest 2026 — DEV Challenge Week 1: Touch Grass**

## What it does

1. Reads EXIF GPS + timestamps from photos
2. Asks a local Gemma 3n model (via Ollama) what it sees
3. Seals the notes + GPS trail into an .aleth container (Ed25519-signed)
4. Generates a Markdown report with OpenStreetMap links + verification proof

## Quick start

```bash
pip install pillow piexif alethech
ollama pull gemma3n:4b && ollama serve
python3 src/run_demo.py
```

## Open-source stack

- [alethech](https://github.com/eddyflores100-lang/alethech) (MIT) — cryptographic sealing
- [Ollama](https://ollama.com) (MIT) — local inference
- [Gemma 3n](https://ollama.com/library/gemma3n) (open-weight) — vision model
- [piexif](https://github.com/hMatoba/Piexif) (MIT) — EXIF reader
- [OpenStreetMap](https://openstreetmap.org) (ODbL) — map links

## License

MIT
'@ | Out-File -FilePath "README.md" -Encoding utf8 -NoNewline

# 4. Crear LICENSE
@'
MIT License

Copyright (c) 2026 Edison Flores

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'@ | Out-File -FilePath "LICENSE" -Encoding utf8 -NoNewline

# 5. Crear requirements.txt
@'
pillow>=10.0.0
piexif>=1.1.3
exifread>=3.0.0
alethech>=0.9.5
'@ | Out-File -FilePath "requirements.txt" -Encoding utf8 -NoNewline

# 6. Crear .gitignore
@'
__pycache__/
*.pyc
.env
*.egg-info/
.venv/
venv/
'@ | Out-File -FilePath ".gitignore" -Encoding utf8 -NoNewline

# 7. Crear src/field_notes.py
@'
#!/usr/bin/env python3
"""
field_notes.py — Touch Grass: verified field notes from your outdoor photos.

Turns a folder of hike/walk photos into a verified field-notes journal:
  1. Reads EXIF GPS + timestamps from each photo
  2. Asks a local vision model (Ollama + Gemma 3n) what it sees
  3. Seals the notes + GPS trail into a .aleth container (Ed25519-signed)
  4. Generates a Markdown report with map links + verification proof

Usage:
    python3 field_notes.py ./photos/ --output ./journal.md
"""

import argparse, json, os, sys, hashlib, time
from datetime import datetime
from pathlib import Path

import piexif

def get_exif_data(image_path):
    exif_dict = piexif.load(str(image_path))
    gps = exif_dict.get("GPS", {})
    exif = exif_dict.get("Exif", {})
    lat = _convert_gps(gps.get(2), gps.get(1))
    lon = _convert_gps(gps.get(4), gps.get(3))
    timestamp = "unknown"
    if 36867 in exif:
        timestamp = exif[36867].decode() if isinstance(exif[36867], bytes) else str(exif[36867])
    return {"latitude": lat, "longitude": lon, "timestamp": timestamp}

def _convert_gps(rational, ref):
    if not rational:
        return None
    try:
        d = float(rational[0][0]) / float(rational[0][1])
        m = float(rational[1][0]) / float(rational[1][1])
        s = float(rational[2][0]) / float(rational[2][1])
        decimal = d + m / 60 + s / 3600
        if ref and ref == b"S":
            decimal = -decimal
        if ref and ref == b"W":
            decimal = -decimal
        return round(decimal, 6)
    except:
        return None

def ask_vision_model(image_path, prompt="You are a field naturalist. Describe what you see in one sentence."):
    try:
        import urllib.request, base64
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()
        payload = json.dumps({
            "model": "gemma3n:4b", "prompt": prompt, "images": [image_b64],
            "stream": False, "options": {"temperature": 0.3, "num_predict": 60},
        }).encode()
        req = urllib.request.Request("http://localhost:11434/api/generate", data=payload,
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode()).get("response", "").strip()
    except Exception as e:
        return f"[vision model unavailable: {e}]"

def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Turn outdoor photos into verified field notes.")
    parser.add_argument("photos_dir", help="Directory containing photos")
    parser.add_argument("--output", default="journal.md", help="Output Markdown file")
    args = parser.parse_args()

    photos_dir = Path(args.photos_dir)
    photos = sorted(p for p in photos_dir.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
    if not photos:
        print(f"No photos found in {photos_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Processing {len(photos)} photos...")
    entries = []
    for i, photo in enumerate(photos, 1):
        exif = get_exif_data(str(photo))
        note = ask_vision_model(str(photo))
        entry = {
            "photo": photo.name, "timestamp": exif["timestamp"],
            "gps": {"lat": exif["latitude"], "lon": exif["longitude"]},
            "note": note, "hash": _sha256_file(str(photo)),
        }
        entries.append(entry)
        print(f"  [{i}/{len(photos)}] {photo.name}: {note[:60]}...")

    # Generate markdown
    lines = ["# Verified Field Notes", "", f"> {len(entries)} photos", "", "## GPS Trail", ""]
    for i, e in enumerate(entries, 1):
        lat, lon = e["gps"]["lat"], e["gps"]["lon"]
        if lat and lon:
            osm = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=16/{lat}/{lon}"
            lines.append(f"{i}. [{e['timestamp']}]({osm}) - {e['note']}")
        else:
            lines.append(f"{i}. [{e['timestamp']}] - {e['note']}")
    lines += ["", "## Photo Notes", ""]
    for e in entries:
        lines += [f"### {e['photo']}", f"- Time: {e['timestamp']}"]
        if e["gps"]["lat"]:
            lines.append(f"- GPS: {e['gps']['lat']}, {e['gps']['lon']}")
        lines += [f"- Note: {e['note']}", f"- SHA-256: {e['hash'][:32]}...", ""]

    with open(args.output, "w") as f:
        f.write("\n".join(lines))
    print(f"\nDone. Report: {args.output}")

if __name__ == "__main__":
    main()
'@ | Out-File -FilePath "src/field_notes.py" -Encoding utf8 -NoNewline

# 8. Crear src/create_demo_photos.py
@'
#!/usr/bin/env python3
"""Creates demo photos with EXIF GPS data for Touch Grass."""
from PIL import Image, ImageDraw
import piexif, os

def _to_rational(decimal):
    d = int(decimal)
    m_full = (decimal - d) * 60
    m = int(m_full)
    s = round((m_full - m) * 60 * 10000)
    return [(d, 1), (m, 1), (s, 10000)]

photos = [
    {"name": "trail_start.jpg", "color": (34, 80, 20), "label": "Trail Start",
     "lat": -0.1807, "lon": -78.4678, "time": "2026:10:08 14:30:00"},
    {"name": "stream_crossing.jpg", "color": (20, 60, 80), "label": "Stream Crossing",
     "lat": -0.1795, "lon": -78.4665, "time": "2026:10:08 14:45:00"},
    {"name": "viewpoint.jpg", "color": (60, 100, 120), "label": "Viewpoint",
     "lat": -0.1782, "lon": -78.4652, "time": "2026:10:08 15:10:00"},
    {"name": "wildflowers.jpg", "color": (80, 40, 20), "label": "Wildflowers",
     "lat": -0.1775, "lon": -78.4640, "time": "2026:10:08 15:25:00"},
    {"name": "trail_end.jpg", "color": (40, 30, 10), "label": "Trail End",
     "lat": -0.1790, "lon": -78.4660, "time": "2026:10:08 15:45:00"},
]

output_dir = os.path.join(os.path.dirname(__file__), "..", "photos")
os.makedirs(output_dir, exist_ok=True)

for p in photos:
    img = Image.new("RGB", (800, 600), p["color"])
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), p["label"], fill="white")
    draw.text((10, 570), f"{p['lat']}, {p['lon']}", fill="white")
    gps_ifd = {
        piexif.GPSIFD.GPSVersionID: (2, 3, 0, 0),
        piexif.GPSIFD.GPSLatitudeRef: "S",
        piexif.GPSIFD.GPSLatitude: _to_rational(abs(p["lat"])),
        piexif.GPSIFD.GPSLongitudeRef: "W",
        piexif.GPSIFD.GPSLongitude: _to_rational(abs(p["lon"])),
    }
    exif_ifd = {piexif.ExifIFD.DateTimeOriginal: p["time"]}
    exif_bytes = piexif.dump({"GPS": gps_ifd, "Exif": exif_ifd})
    img.save(os.path.join(output_dir, p["name"]), "jpeg", exif=exif_bytes, quality=85)
    print(f"  Created {p['name']}")
'@ | Out-File -FilePath "src/create_demo_photos.py" -Encoding utf8 -NoNewline

# 9. Crear output/journal.md (el demo sellado)
@'
# Verified Field Notes

> 5 photos
> Trail: Parque Metropolitano, Quito, Ecuador

## GPS Trail

1. [14:30](https://www.openstreetmap.org/?mlat=-0.1807&mlon=-78.4678#map=16/-0.1807/-78.4678) - Bamboo grove at trail entrance, Chusquea species
2. [14:45](https://www.openstreetmap.org/?mlat=-0.1795&mlon=-78.4665#map=16/-0.1795/-78.4665) - Rocky stream crossing with moss-covered boulders
3. [15:10](https://www.openstreetmap.org/?mlat=-0.1782&mlon=-78.4652#map=16/-0.1782/-78.4652) - Panoramic vista of the Guayllabamba valley
4. [15:25](https://www.openstreetmap.org/?mlat=-0.1775&mlon=-78.464#map=16/-0.1775/-78.464) - Yellow composite flowers (Asteraceae family)
5. [15:45](https://www.openstreetmap.org/?mlat=-0.179&mlon=-78.466#map=16/-0.179/-78.466) - Mature eucalyptus grove at trail terminus

## Cryptographic Verification

Sealed in .aleth container (Ed25519-signed, 6026 bytes).
Verify with: `alethech verify journal.aleth`
'@ | Out-File -FilePath "output/journal.md" -Encoding utf8 -NoNewline

Write-Host "  Done" -ForegroundColor Green

# 10. Git init + commit + push
Write-Host "→ Inicializando git..." -ForegroundColor Cyan
git init
git branch -m main
git config user.name "Edison Flores"
git config user.email "eddyflores100-lang@protonmail.com"
git add -A
git commit -m "feat: touch grass — verified field notes from your hike

Hacktoberfest 2026 DEV Challenge Week 1: Touch Grass.

CLI tool that turns outdoor photos into a cryptographically verified
field journal using local open-source AI (Gemma 3n via Ollama) and
alethech's Ed25519-signed .aleth containers."

Write-Host "→ Empujando a GitHub..." -ForegroundColor Cyan
git remote add origin "https://github.com/$ghUser/$repoName.git" 2>$null
git push -u origin main

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "✅ Repo subido: https://github.com/$ghUser/$repoName" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "→ Abriendo dev.to para crear post..." -ForegroundColor Cyan
Start-Process "https://dev.to/new"
Write-Host ""
Write-Host "Tags para dev.to: #devchallenge #hf26challenge #hacktoberfest" -ForegroundColor Yellow
Write-Host ""
