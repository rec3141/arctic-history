#!/usr/bin/env python3
"""Re-issue an artifact row through history-db.py, preserving every field
except the ones given as overrides."""
import sqlite3, subprocess, json, sys

DB = 'db/history/history.sqlite'

FIELDS = [
    ('type', '--type'), ('title', '--title'), ('date_start', '--date'),
    ('date_end', '--date-end'), ('creator', '--creator'),
    ('description', '--description'), ('lat', '--lat'), ('lon', '--lon'),
    ('geometry', '--geometry'), ('waypoints', '--waypoints'),
    ('source_url', '--source-url'), ('download_url', '--download-url'),
    ('local_file', '--local-file'), ('licence', '--licence'),
    ('credit', '--credit'), ('bibkey', '--bibkey'), ('pages', '--pages'),
    ('language', '--language'), ('view_file', '--view-file'),
    ('routing', '--routing'),
]
LISTY = {'people': '--people', 'tags': '--tags'}


def patch(aid, **over):
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    r = c.execute('select * from artifacts where id=?', (aid,)).fetchone()
    if r is None:
        raise SystemExit('no such artifact: ' + aid)
    d = dict(r)
    d.update(over)
    cmd = ['/usr/bin/python3', 'tools/history-db.py', 'artifact',
           '--id', aid, '--topic', d['topic']]
    for col, flag in FIELDS:
        v = d.get(col)
        if v in (None, ''):
            continue
        cmd += [flag, str(v)]
    for col, flag in LISTY.items():
        v = d.get(col)
        if not v:
            continue
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except Exception:
                v = [x.strip() for x in v.split(';')]
        if v:
            cmd += [flag, ';'.join(v)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    print(aid, p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1:] or '')
    if p.returncode:
        raise SystemExit(1)
