#!/usr/bin/env python3
"""
field_notes.py — Touch Grass: verified field notes from your outdoor photos.

Turns a folder of hike/walk photos into a verified field-notes journal:
  1. Reads EXIF GPS + timestamps from each photo
  2. Asks a local vision model (Ollama + Gemma 3n) what it sees
  3. Seals the notes + GPS trail into a .aleth container (Ed25519-signed)
  4. Generates a Markdown report with map links + verification proof

Why open matters: photos with GPS coordinates never leave your machine.
The vision model runs locally via Ollama. The .aleth container proves the
journal wasn't tampered with after signing.

Usage:
    python3 field_notes.py ./photos/ --output ./journal.md

Requirements:
    pip install pillow exifread alethech
    ollama pull gemma3n:4b    # or any open-weight vision model
    ollama serve              # must be running on localhost:11434
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import exifread
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

# alethech for cryptographic verification
try:
    from alethech import AlethContainer, AlethKey
    from alethech.canonical import canonical_json
    ALETHECH_AVAILABLE = True
except ImportError:
    ALETHECH_AVAILABLE = False


def get_exif_data(image_path):
    """Extract GPS coordinates and timestamp from a photo's EXIF data."""
    with open(image_path, "rb") as f:
        tags = exifread.process_file(f, details=False)

    # Extract GPS
    gps_coords = {}
    for tag in tags:
        if tag.startswith("GPS"):
            key = tag.split("GPS")[1]
            gps_coords[key] = tags[tag]

    lat = _convert_gps(gps_coords.get("GPSLatitude"), gps_coords.get("GPSLatitudeRef"))
    lon = _convert_gps(gps_coords.get("GPSLongitude"), gps_coords.get("GPSLongitudeRef"))

    # Extract timestamp
    timestamp = str(tags.get("EXIF DateTimeOriginal", tags.get("Image DateTime", "unknown")))

    return {
        "latitude": lat,
        "longitude": lon,
        "timestamp": timestamp,
    }


def _convert_gps(value, ref):
    """Convert EXIF GPS rational to decimal degrees."""
    if not value:
        return None
    try:
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)
        decimal = d + m / 60 + s / 3600
        if ref and ref.values == "S":
            decimal = -decimal
        if ref and ref.values == "W":
            decimal = -decimal
        return round(decimal, 6)
    except (IndexError, AttributeError, ZeroDivisionError):
        return None


def ask_vision_model(image_path, prompt="What do you see? Describe in one sentence."):
    """
    Ask a local vision model (via Ollama) to describe the photo.
    Falls back to a placeholder if Ollama is not running.

    In production: ollama.generate(model='gemma3n:4b', images=[image_bytes])
    """
    try:
        import urllib.request
        import base64

        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()

        payload = json.dumps({
            "model": "gemma3n:4b",
            "prompt": prompt,
            "images": [image_b64],
            "stream": False,
            "options": {"temperature": 0.3, "num_predict": 60},
        }).encode()

        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            return result.get("response", "").strip()

    except Exception as e:
        return f"[vision model unavailable: {e}]"


def create_field_notes_entry(photo_path, exif_data, vision_note):
    """Create a single field-notes entry dict."""
    return {
        "photo": os.path.basename(photo_path),
        "timestamp": exif_data.get("timestamp", "unknown"),
        "gps": {
            "lat": exif_data.get("latitude"),
            "lon": exif_data.get("longitude"),
        },
        "note": vision_note,
        "hash": _sha256_file(photo_path),
    }


def _sha256_file(path):
    """Compute SHA-256 of a file."""
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def seal_in_aleth(entries, output_path, passphrase="touch-grass-demo"):
    """
    Seal the field-notes journal into a .aleth container.

    The .aleth format is an Ed25519-signed, scrypt-encrypted, hash-linked DAG.
    Once sealed, the journal cannot be modified without invalidating the
    signature — proving the field notes were not altered after the hike.
    """
    if not ALETHECH_AVAILABLE:
        return None, "alethech not installed"

    try:
        # Initialize a new alethech identity
        key = AlethKey.generate()

        # Create container
        container = AlethContainer.new(
            identity=key,
            passphrase=passphrase,
            recovery_passphrase=passphrase,
        )

        # Commit the field notes as a memory entry
        memory_data = {
            "type": "field_notes_journal",
            "created": datetime.utcnow().isoformat() + "Z",
            "entries": entries,
            "entry_count": len(entries),
        }

        container.commit(
            data=canonical_json(memory_data),
            evidence={"source": "field_notes.py", "version": "1.0.0"},
        )

        # Export to .aleth file
        container.export(output_path, passphrase=passphrase)

        verification = container.verify()
        return {
            "file": output_path,
            "container_id": container.container_id[:16],
            "verified": verification.is_valid,
            "key_fingerprint": key.fingerprint()[:16],
        }, None

    except Exception as e:
        return None, str(e)


def generate_markdown_report(entries, aleth_info, output_md):
    """Generate a Markdown report with field notes, map links, and verification proof."""
    lines = [
        "# 🌿 Touch Grass — Verified Field Notes",
        "",
        f"> Generated: {datetime.utcnow().isoformat()}Z",
        f"> Photos: {len(entries)}",
        f"> Sealed in .aleth: {'✅' if aleth_info else '❌'}",
        "",
        "---",
        "",
        "## 📍 GPS Trail",
        "",
    ]

    # OSM links for each photo
    for i, entry in enumerate(entries, 1):
        lat = entry["gps"]["lat"]
        lon = entry["gps"]["lon"]
        if lat and lon:
            osm_link = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=16/{lat}/{lon}"
            lines.append(f"{i}. [{entry['timestamp']}]({osm_link}) — {entry['note']}")
        else:
            lines.append(f"{i}. [{entry['timestamp']}] — {entry['note']} (no GPS)")

    lines.extend([
        "",
        "---",
        "",
        "## 🔐 Cryptographic Verification",
        "",
    ])

    if aleth_info:
        lines.extend([
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Container | `{aleth_info['container_id']}…` |",
            f"| Key fingerprint | `{aleth_info['key_fingerprint']}…` |",
            f"| Verified | {'✅' if aleth_info['verified'] else '❌'} |",
            f"| .aleth file | `{aleth_info['file']}` |",
            "",
            "The field notes above are sealed in an `.aleth` container signed with",
            "Ed25519. Anyone with the container file and the passphrase can verify",
            "that the notes were not modified after the hike — the hash-linked DAG",
            "in the container makes tampering detectable.",
            "",
            "To verify:",
            "```bash",
            "alethech verify journal.aleth",
            "```",
        ])
    else:
        lines.append("(alethech not available — notes are unsigned)")

    lines.extend([
        "",
        "---",
        "",
        "## 📸 Photo Notes",
        "",
    ])

    for entry in entries:
        lines.extend([
            f"### {entry['photo']}",
            f"- **Time:** {entry['timestamp']}",
        ])
        if entry["gps"]["lat"]:
            lines.append(f"- **GPS:** {entry['gps']['lat']}, {entry['gps']['lon']}")
        lines.extend([
            f"- **Note:** {entry['note']}",
            f"- **SHA-256:** `{entry['hash'][:32]}…`",
            "",
        ])

    with open(output_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return output_md


def main():
    parser = argparse.ArgumentParser(
        description="Turn outdoor photos into verified field notes."
    )
    parser.add_argument("photos_dir", help="Directory containing photos")
    parser.add_argument("--output", default="journal.md", help="Output Markdown file")
    parser.add_argument("--aleth", default="journal.aleth", help="Output .aleth container")
    parser.add_argument("--passphrase", default="touch-grass", help="Passphrase for .aleth container")
    parser.add_argument(
        "--prompt",
        default="You are a field naturalist. Describe what you see in this photo in one sentence. If you see plants, name them. If you see a landscape, describe it.",
        help="Prompt for the vision model",
    )
    args = parser.parse_args()

    photos_dir = Path(args.photos_dir)
    if not photos_dir.is_dir():
        print(f"Error: {photos_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Find all JPEG files
    photos = sorted(
        p for p in photos_dir.iterdir()
        if p.suffix.lower() in (".jpg", ".jpeg", ".png")
        and not p.name.startswith(".")
    )

    if not photos:
        print(f"No photos found in {photos_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"🌿 Processing {len(photos)} photos…")

    entries = []
    for i, photo in enumerate(photos, 1):
        print(f"  [{i}/{len(photos)}] {photo.name}…", end=" ", flush=True)

        # Step 1: Extract EXIF
        exif = get_exif_data(str(photo))
        print(f"GPS={'✓' if exif['latitude'] else '✗'}", end=" ")

        # Step 2: Ask vision model
        note = ask_vision_model(str(photo), args.prompt)
        print(f"vision={'✓' if not note.startswith('[') else '✗'}")

        # Step 3: Create entry
        entry = create_field_notes_entry(str(photo), exif, note)
        entries.append(entry)

    # Step 4: Seal in .aleth
    print(f"\n🔐 Sealing in .aleth container…")
    aleth_info, err = seal_in_aleth(entries, args.aleth, args.passphrase)
    if err:
        print(f"  ⚠️  {err}")
    else:
        print(f"  ✅ Sealed: {aleth_info['container_id']}…")

    # Step 5: Generate Markdown report
    print(f"\n📝 Generating report…")
    md_path = generate_markdown_report(entries, aleth_info, args.output)
    print(f"  ✅ {md_path}")

    print(f"\nDone. {len(entries)} entries sealed and reported.")


if __name__ == "__main__":
    main()
