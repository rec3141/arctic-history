#!/usr/bin/env python3
"""Rewrite artifacts through the CLI, carrying every existing field forward and
applying named overrides, so nothing is blanked by omission."""
import json, sqlite3, subprocess, sys

DB = "db/history/history.sqlite"
TOOL = ["/usr/bin/python3", "tools/history-db.py"]

FIELDS = {  # column -> cli flag
    "type": "--type", "title": "--title", "date_text": "--date",
    "creator": "--creator", "description": "--description",
    "lat": "--lat", "lon": "--lon", "source_url": "--source-url",
    "download_url": "--download-url", "local_file": "--local-file",
    "licence": "--licence", "credit": "--credit", "bibkey": "--bibkey",
    "pages": "--pages", "language": "--language", "view_file": "--view-file",
    "routing": "--routing",
}


def edit(aid, **over):
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    r = c.execute("SELECT * FROM artifacts WHERE id=?", (aid,)).fetchone()
    if not r:
        sys.exit(f"no artifact {aid}")
    d = dict(r)
    d.update(over)
    cmd = list(TOOL) + (["track"] if d["type"] == "track" else ["artifact"])
    cmd += ["--id", aid, "--topic", d["topic"]]
    for col, flag in FIELDS.items():
        if d["type"] == "track" and col == "type":
            continue
        v = d.get(col)
        if v is None or v == "":
            continue
        cmd += [flag, str(v)]
    ppl = d.get("people")
    if isinstance(ppl, str):
        ppl = json.loads(ppl or "[]")
    if ppl:
        cmd += ["--people", ";".join(ppl)]
    tags = d.get("tags")
    if isinstance(tags, str):
        tags = json.loads(tags or "[]")
    if tags:
        cmd += ["--tags", ",".join(tags)]
    for col, flag in (("geometry", "--geometry"), ("waypoints", "--waypoints")):
        v = d.get(col)
        if v:
            cmd += [flag, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)]
    c.close()
    p = subprocess.run(cmd, capture_output=True, text=True)
    print(aid, p.returncode, (p.stdout or "").strip()[:160], (p.stderr or "").strip()[:400])
    return p.returncode
