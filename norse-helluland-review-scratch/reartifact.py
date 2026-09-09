#!/usr/bin/env python3
"""Re-run tools/history-db.py artifact for an existing artifact, preserving every
stored field and overriding only what is named. Writes go through the tool."""
import json
import sqlite3
import subprocess
import sys

DB = "db/history/history.sqlite"
FLAGS = {
    "type": "--type", "title": "--title", "date_text": "--date", "creator": "--creator",
    "lat": "--lat", "lon": "--lon", "source_url": "--source-url",
    "download_url": "--download-url", "local_file": "--local-file", "licence": "--licence",
    "credit": "--credit", "bibkey": "--bibkey", "pages": "--pages", "language": "--language",
    "people": "--people", "tags": "--tags", "view_file": "--view-file",
    "geometry": "--geometry", "waypoints": "--waypoints", "routing": "--routing",
}


def reartifact(aid, description=None, **overrides):
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    r = c.execute("SELECT * FROM artifacts WHERE id=?", (aid,)).fetchone()
    if not r:
        raise SystemExit(f"no artifact {aid}")
    row = dict(r)
    row.update(overrides)
    cmd = ["/usr/bin/python3", "tools/history-db.py", "artifact",
           "--id", aid, "--topic", row["topic"]]
    if row.get("date_end") and row["date_end"] != row["date_start"] \
            and "/" not in str(row.get("date_text") or ""):
        cmd += ["--date-end", row["date_end"]]
    for col, flag in FLAGS.items():
        v = row.get(col)
        if v in (None, ""):
            continue
        cmd += [flag, str(v)]
    desc = description if description is not None else row.get("description")
    if desc:
        cmd += ["--description", desc]
    p = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    if p.returncode:
        sys.stderr.write(p.stderr)
        raise SystemExit(f"FAILED {aid}")
    return p.stdout.strip()


if __name__ == "__main__":
    aid = sys.argv[1]
    desc = None
    if len(sys.argv) > 2:
        desc = open(sys.argv[2], encoding="utf-8").read().strip()
    ov = {}
    for kv in sys.argv[3:]:
        k, _, v = kv.partition("=")
        ov[k] = v
    reartifact(aid, desc, **ov)
