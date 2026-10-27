import json, urllib.request, ssl, time

GL_TOKEN = "glpat-VTdIPfmOYCLcAQHp0IdlyWM6MQpvOjEKdTpranZqbQ8.01.17073yv2r"
GL_HEADERS = {"PRIVATE-TOKEN": GL_TOKEN, "User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CTX = ssl.create_default_context()

def fetch(url, delay=20):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=GL_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}

# Known GitLab repos with hacktoberfest activity
TARGETS = [
    # (name, pid, lang, avoid?)
    ("inkscape/inkscape", 3472737, "C++", True),  # already touched
    ("Calamares/calamares", None, "C++", False),
    ("GNOME/gitlab", None, "C", False),
    ("KDE/invent", None, "C++", False),
    ("libreoffice/core", None, "C++", False),
    ("vlc/vlc", None, "C", False),
    ("Bitcoin/Core", None, "C++", False),
    ("qemu-project/qemu", None, "C", False),
    ("gstreamer/gstreamer", None, "C", False),
    ("xorg/xserver", None, "C", False),
    ("kernel/linux", None, "C", False),
    ("gitlab-org/gitlab", None, "Ruby", False),
    ("freedesktop/wlroots", None, "C", False),
    (" dbus/dbus", None, "C", False),
    ("systemd/systemd", None, "C", False),
    ("ffmpeg/ffmpeg", None, "C", False),
    ("vmware/open-vmdk", None, "Shell", False),
    ("emacs/emacs", None, "C", False),
    ("godotengine/godot", None, "C++", False),
    ("AdguardSoftware/AdGuardFilters", None, "Text", False),
    ("theforeman/foreman", None, "Ruby", False),
    ("opencraft/opencraft", None, "Python", False),
    ("obsproject/obs-studio", None, "C++", False),
    ("wireshark/wireshark", None, "C", False),
    ("blender/blender", None, "C++", False),
]

print("Searching GitLab repos for hacktoberfest issues...")
gl_candidates = []
seen = set()

for name, pid, lang, avoid in TARGETS:
    if avoid:
        continue
    if name in seen:
        continue
    seen.add(name)
    
    # Try to find project ID first
    if pid is None:
        encoded = name.strip().replace("/", "%2F")
        code, d = fetch(f"https://gitlab.com/api/v4/projects/{encoded}", delay=8)
        if code != 200:
            continue
        pid = d.get("id")
    
    # Get issues with hacktoberfest label
    code, d = fetch(f"https://gitlab.com/api/v4/projects/{pid}/issues?labels=hacktoberfest&state=opened&per_page=5&sort=desc&order_by=created_at", delay=10)
    if code == 200 and isinstance(d, list) and len(d) > 0:
        print(f"\n  *** {name} (pid={pid}) — {len(d)} hacktoberfest issues ***")
        for it in d[:3]:
            if it.get("assignees"):
                continue
            title = it.get("title","")[:70]
            iid = it.get("iid")
            labels = it.get("labels",[])
            created = (it.get("created_at","?"))[:10]
            url = it.get("web_url","")
            print(f"    !{iid} ({created}): {title}")
            gl_candidates.append({
                "repo": name,
                "iid": iid,
                "title": title,
                "labels": labels[:5],
                "created": created,
                "url": url,
                "lang": lang,
            })
    
    if len(gl_candidates) >= 10:
        break

print(f"\n{'='*60}")
print(f"GitLab hacktoberfest candidates: {len(gl_candidates)}")
for i, c in enumerate(gl_candidates[:10], 1):
    print(f"  {i}. {c['repo']}!{c['iid']} ({c['lang']}, {c['created']})")
    print(f"     title: {c['title']}")
    print(f"     url: {c['url']}")
