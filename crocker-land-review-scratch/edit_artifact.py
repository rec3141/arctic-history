"""Re-issue tools/history-db.py artifact for an existing row, carrying every
current field forward and applying only the overrides given. Keeps the write
inside the tool (never touches the database directly)."""
import json
import sqlite3
import subprocess
import sys

DB = "db/history/history.sqlite"
FLAGS = {
    "type": "--type", "title": "--title", "date_text": "--date", "date_end": "--date-end",
    "creator": "--creator", "lat": "--lat", "lon": "--lon", "source_url": "--source-url",
    "download_url": "--download-url", "local_file": "--local-file", "licence": "--licence",
    "credit": "--credit", "bibkey": "--bibkey", "pages": "--pages", "language": "--language",
    "view_file": "--view-file", "routing": "--routing", "geometry": "--geometry",
    "waypoints": "--waypoints",
}


def edit(aid, **over):
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    r = db.execute("SELECT * FROM artifacts WHERE id=?", (aid,)).fetchone()
    if not r:
        raise SystemExit("no artifact " + aid)
    r = dict(r)
    db.close()
    cmd = ["/usr/bin/python3", "tools/history-db.py", "artifact",
           "--id", aid, "--topic", r["topic"]]
    desc = over.pop("description", r["description"] or "")
    for col, flag in FLAGS.items():
        v = over.pop(col, r.get(col))
        if v in (None, ""):
            continue
        cmd += [flag, str(v)]
    for col, flag in (("people", "--people"), ("tags", "--tags")):
        v = over.pop(col, None)
        if v is None:
            v = "; ".join(json.loads(r[col] or "[]")) if col == "people" else \
                ",".join(json.loads(r[col] or "[]"))
        if v:
            cmd += [flag, v]
    if over:
        raise SystemExit("unknown overrides: " + repr(over))
    open("crocker-land-review-scratch/_desc.txt", "w").write(desc)
    cmd += ["--description-file", "crocker-land-review-scratch/_desc.txt"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    print(aid, p.returncode, (p.stdout + p.stderr).strip()[:300])
    if p.returncode:
        raise SystemExit(1)


if __name__ == "__main__":
    print(sys.argv)
