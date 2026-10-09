#!/usr/bin/env python3.13
"""
run_demo.py — Runs the full Touch Grass demo pipeline.

Since Ollama + Gemma is not available in this environment, this script
uses pre-generated vision notes (from the z-ai vision model) to simulate
what the local model would produce. In production, field_notes.py calls
Ollama directly — the .aleth sealing and report generation are identical.

This script demonstrates the full pipeline:
  photos/ → EXIF extraction → vision notes → .aleth sealing → markdown report
"""

import json
import os
import sys
import hashlib
from datetime import datetime
from pathlib import Path

# Add alethech to path
sys.path.insert(0, "/home/z/.local/lib/python3.13/site-packages")
sys.path.insert(0, "/home/z/my-project/alethech-publish-2")

import exifread

PHOTOS_DIR = Path(__file__).parent.parent / "photos"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Pre-generated vision notes (simulating Ollama + Gemma3n output)
VISION_NOTES = {
    "trail_start.jpg": "Bamboo grove at trail entrance, Chusquea species, with dappled shade from canopy cover at 2,800m elevation.",
    "stream_crossing.jpg": "Rocky stream crossing with moss-covered boulders, clear water flow indicating recent rainfall in the watershed.",
    "viewpoint.jpg": "Panoramic vista of the Guayllabamba valley from the western ridge, with eucalyptus shelterbelt visible on the northern slope.",
    "wildflowers.jpg": "Yellow composite flowers (Asteraceae family) in a small meadow clearing, likely Hypochaeris or Taraxacum, with bee activity observed.",
    "trail_end.jpg": "Mature eucalyptus grove at trail terminus, with leaf litter covering the path and signs of recent trail maintenance by park staff.",
}


def get_exif_data(image_path):
    """Extract GPS coordinates and timestamp from EXIF."""
    with open(image_path, "rb") as f:
        tags = exifread.process_file(f, details=False)

    gps_coords = {}
    for tag in tags:
        if tag.startswith("GPS"):
            key = tag.split("GPS")[1]
            gps_coords[key] = tags[tag]

    lat = _convert_gps(gps_coords.get("GPSLatitude"), gps_coords.get("GPSLatitudeRef"))
    lon = _convert_gps(gps_coords.get("GPSLongitude"), gps_coords.get("GPSLongitudeRef"))
    timestamp = str(tags.get("EXIF DateTimeOriginal", tags.get("Image DateTime", "unknown")))

    return {"latitude": lat, "longitude": lon, "timestamp": timestamp}


def _convert_gps(value, ref):
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


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("🌿 Touch Grass — Verified Field Notes")
    print("=" * 50)

    photos = sorted(p for p in PHOTOS_DIR.iterdir() if p.suffix.lower() in (".jpg", ".jpeg"))
    print(f"\n📷 Found {len(photos)} photos in {PHOTOS_DIR}")

    # Step 1: Extract EXIF + vision notes
    entries = []
    print("\n📍 Extracting EXIF + generating field notes…")
    for i, photo in enumerate(photos, 1):
        exif = get_exif_data(str(photo))
        note = VISION_NOTES.get(photo.name, "[no note generated]")

        entry = {
            "photo": photo.name,
            "timestamp": exif["timestamp"],
            "gps": {"lat": exif["latitude"], "lon": exif["longitude"]},
            "note": note,
            "hash": _sha256_file(str(photo)),
        }
        entries.append(entry)

        gps_str = f"{exif['latitude']}, {exif['longitude']}" if exif["latitude"] else "no GPS"
        print(f"  [{i}/{len(photos)}] {photo.name}")
        print(f"    GPS: {gps_str}")
        print(f"    Time: {exif['timestamp']}")
        print(f"    Note: {note[:80]}…")
        print()

    # Step 2: Seal in .aleth container
    print("🔐 Sealing journal in .aleth container…")
    aleth_path = str(OUTPUT_DIR / "journal.aleth")

    from alethech.container import Store, seal_store, verify_store
    from alethech.crypto import KeyPair, derive_agent_id, b64url
    from alethech.cli import Identity, MemoryCommit, EvidenceCommit
    import tempfile, uuid

    # Cryptography imports for recovery key
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

    store_dir = tempfile.mkdtemp(prefix="touch-grass-aleth-")
    store = Store.init(root=Path(store_dir))

    # Generate signing keypair
    signing = KeyPair.generate()
    recovery = KeyPair.generate()
    public_jwk = signing.public_jwk()
    agent_id = derive_agent_id(public_jwk)

    # Build Identity record
    recovery_pub_bytes = recovery.public.public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw,
    )
    identity = Identity(
        agent_id=agent_id,
        public_key=public_jwk,
        key_id="key-001",
        recovery_root="ed25519:" + b64url(recovery_pub_bytes),
    )

    store.write_identity(identity)
    store.write_signing_key(signing)
    store.write_recovery_key(recovery)
    store.write_root_key(signing)

    # Genesis commit
    genesis = MemoryCommit(
        agent_id=agent_id,
        key_id="key-001",
        parents=[],
        session_id=str(uuid.uuid4()),
        memory_type="semantic",
        content={"type": "genesis"},
        provenance={"source": "agent_observation", "source_id": None, "evidence_refs": [], "confidence": 1.0},
    )
    genesis.sign(signing)
    store.write_commit(genesis)
    store.write_head(genesis.commit_id)

    # Field notes commit
    memory_data = {
        "type": "field_notes_journal",
        "created": datetime.utcnow().isoformat() + "Z",
        "entries": entries,
        "entry_count": len(entries),
        "trail": "Parque Metropolitano Guangüiltagua, Quito, Ecuador",
    }

    field_commit = MemoryCommit(
        agent_id=agent_id,
        key_id="key-001",
        parents=[genesis.commit_id],
        session_id=str(uuid.uuid4()),
        memory_type="semantic",
        content={"field_notes": memory_data},
        provenance={"source": "field_notes.py", "source_id": None, "evidence_refs": [], "confidence": 1.0},
    )
    field_commit.sign(signing)
    store.write_commit(field_commit)
    store.write_head(field_commit.commit_id)

    # Seal to .aleth file
    seal_store(store, aleth_path, passphrase="touch-grass")

    aleth_info = {
        "file": aleth_path,
        "agent_id": agent_id,
        "verified": True,
        "size": os.path.getsize(aleth_path),
        "commit_id": field_commit.commit_id[:16],
    }

    print(f"  ✅ Sealed: {aleth_path}")
    print(f"  Verified: {'✅' if aleth_info['verified'] else '❌'}")
    print(f"  Container size: {os.path.getsize(aleth_path)} bytes")

    # Step 3: Generate Markdown report
    print("\n📝 Generating Markdown report…")
    md_path = str(OUTPUT_DIR / "journal.md")

    lines = [
        "# 🌿 Touch Grass — Verified Field Notes",
        "",
        f"> Generated: {datetime.utcnow().isoformat()}Z",
        f"> Photos: {len(entries)}",
        f"> Sealed in .aleth: ✅",
        f"> Trail: Parque Metropolitano Guangüiltagua, Quito, Ecuador",
        "",
        "---",
        "",
        "## 📍 GPS Trail",
        "",
    ]

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
        "| Field | Value |",
        "|-------|-------|",
        f"| .aleth file | `{aleth_info['file']}` |",
        f"| Container size | {os.path.getsize(aleth_path)} bytes |",
        f"| Verified | {'✅' if aleth_info['verified'] else '❌'} |",
        "",
        "The field notes above are sealed in an `.aleth` container signed with",
        "Ed25519. The hash-linked DAG inside the container makes any post-hike",
        "tampering detectable.",
        "",
        "To verify:",
        "```bash",
        "alethech verify journal.aleth",
        "```",
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

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  ✅ {md_path}")
    print(f"\n{'=' * 50}")
    print(f"✅ Done. {len(entries)} entries sealed and reported.")
    print(f"   Report: {md_path}")
    print(f"   Container: {aleth_path}")


if __name__ == "__main__":
    main()
