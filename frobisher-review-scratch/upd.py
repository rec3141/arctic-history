#!/usr/bin/env python3
"""Re-run `history-db.py artifact` for one artifact, keeping every stored field
except the ones named on the command line."""
import json, sqlite3, subprocess, sys

DB = '/data/dev/arctic-history/db/history/history.sqlite'
PY = '/usr/bin/python3'
TOOL = 'tools/history-db.py'

FLAGS = [
    ('type', '--type'), ('title', '--title'), ('date_text', '--date'),
    ('date_end', '--date-end'), ('creator', '--creator'),
    ('description', '--description'), ('lat', '--lat'), ('lon', '--lon'),
    ('geometry', '--geometry'), ('waypoints', '--waypoints'),
    ('source_url', '--source-url'), ('download_url', '--download-url'),
    ('local_file', '--local-file'), ('licence', '--licence'),
    ('pages', '--pages'), ('language', '--language'),
    ('view_file', '--view-file'), ('routing', '--routing'),
    ('credit', '--credit'), ('bibkey', '--bibkey'),
]


def update(aid, **over):
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    r = c.execute("SELECT * FROM artifacts WHERE id=?", (aid,)).fetchone()
    c.close()
    if r is None:
        raise SystemExit('no such artifact: ' + aid)
    d = dict(r)
    d.update(over)
    cmd = [PY, TOOL, 'artifact', '--id', aid, '--topic', d['topic']]
    for col, flag in FLAGS:
        v = d.get(col)
        if v in (None, ''):
            continue
        cmd += [flag, str(v)]
    for col, flag in (('people', '--people'), ('tags', '--tags')):
        v = d.get(col)
        if not v:
            continue
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except Exception:
                v = [v]
        sep = ';' if col == 'people' else ','
        joined = sep.join(str(x) for x in v)
        if joined:
            cmd += [flag, joined]
    p = subprocess.run(cmd, capture_output=True, text=True,
                       cwd='/data/dev/arctic-history')
    print(aid, p.returncode, (p.stdout + p.stderr).strip()[:200])
    return p.returncode
