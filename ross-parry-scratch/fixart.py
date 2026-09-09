#!/usr/bin/env python3
"""Re-run history-db.py artifact for a row, preserving every existing field
and applying only the named edits.

Usage: fixart.py <edits.json>
  edits.json: {"<artifact id>": {"title": "...", "pages": "...", ...}, ...}
Keys are artifact column names; values replace. A value of null clears.
"""
import json
import sqlite3
import subprocess
import sys

DB = "/data/dev/arctic-history/db/history/history.sqlite"
TOOL = ["/usr/bin/python3", "tools/history-db.py", "artifact"]

# artifact column -> command-line flag
FLAGS = [
    ("id", "--id"), ("topic", "--topic"), ("type", "--type"), ("title", "--title"),
    ("date_text", "--date"), ("creator", "--creator"), ("description", "--description"),
    ("lat", "--lat"), ("lon", "--lon"), ("source_url", "--source-url"),
    ("download_url", "--download-url"), ("local_file", "--local-file"),
    ("licence", "--licence"), ("credit", "--credit"), ("bibkey", "--bibkey"),
    ("pages", "--pages"), ("language", "--language"), ("view_file", "--view-file"),
]


def listish(v):
    """people/tags are stored as JSON lists; the CLI wants delimited strings."""
    if not v:
        return None
    if isinstance(v, (list, tuple)):
        return [str(x).strip() for x in v if str(x).strip()]
    try:
        parsed = json.loads(v)
        if isinstance(parsed, list):
            return parsed
    except (ValueError, TypeError):
        pass
    return [x.strip() for x in str(v).replace(";", ",").split(",") if x.strip()]


def main():
    edits = json.load(open(sys.argv[1]))
    con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    con.row_factory = sqlite3.Row
    for aid, changes in edits.items():
        row = con.execute("select * from artifacts where id=?", (aid,)).fetchone()
        if row is None:
            print("MISSING", aid)
            continue
        data = dict(row)
        data.update(changes)

        cmd = list(TOOL)
        for col, flag in FLAGS:
            val = data.get(col)
            if val is None or val == "":
                continue
            cmd += [flag, str(val)]
        people = listish(data.get("people"))
        if people:
            cmd += ["--people", ";".join(people)]
        tags = listish(data.get("tags"))
        if tags:
            cmd += ["--tags", ",".join(tags)]
        # date_end is stored separately only for ranges expressed in date_text
        if data.get("date_end") and "/" not in str(data.get("date_text") or ""):
            cmd += ["--date-end", str(data["date_end"])]

        res = subprocess.run(cmd, capture_output=True, text=True,
                             cwd="/data/dev/arctic-history")
        status = "ok " if res.returncode == 0 else "FAIL"
        print(status, aid, (res.stdout or res.stderr).strip()[:140])


if __name__ == "__main__":
    main()
