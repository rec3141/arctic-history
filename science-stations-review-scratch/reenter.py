#!/usr/bin/env python3
"""Re-issue an artifact through tools/history-db.py, preserving every field
already in the row and changing only what is passed on the command line."""
import json
import sqlite3
import subprocess
import sys

DB = "db/history/history.sqlite"


def reenter(aid, **changes):
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    r = c.execute("SELECT * FROM artifacts WHERE id=?", (aid,)).fetchone()
    if r is None:
        raise SystemExit("no artifact " + aid)
    d = dict(r)
    d.update(changes)
    cmd = ["/usr/bin/python3", "tools/history-db.py", "artifact",
           "--id", d["id"], "--topic", d["topic"], "--type", d["type"],
           "--title", d["title"], "--bibkey", d["bibkey"], "--credit", d["credit"]]

    def add(flag, val):
        if val not in (None, ""):
            cmd.extend([flag, str(val)])

    add("--date", d["date_text"])
    if d["date_end"] and "/" not in (d["date_text"] or ""):
        add("--date-end", d["date_end"])
    add("--creator", d["creator"])
    add("--description", d["description"])
    add("--lat", d["lat"])
    add("--lon", d["lon"])
    add("--geometry", d["geometry"])
    add("--waypoints", d["waypoints"])
    add("--source-url", d["source_url"])
    add("--download-url", d["download_url"])
    add("--local-file", d["local_file"])
    add("--licence", d["licence"])
    add("--pages", d["pages"])
    add("--language", d["language"])
    add("--view-file", d["view_file"])
    add("--routing", d["routing"])
    people = json.loads(d["people"] or "[]")
    if people:
        add("--people", ";".join(people))
    tags = json.loads(d["tags"] or "[]")
    if tags:
        add("--tags", ",".join(tags))
    out = subprocess.run(cmd, capture_output=True, text=True)
    print(aid, out.returncode, out.stdout.strip(), out.stderr.strip())


if __name__ == "__main__":
    aid = sys.argv[1]
    field = sys.argv[2]
    value = open(sys.argv[3]).read().strip() if sys.argv[3].startswith("@") is False and len(sys.argv) > 3 else None
    reenter(aid, **{field: value})
