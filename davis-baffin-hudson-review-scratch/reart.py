#!/usr/bin/env python3
"""Re-issue an existing artifact through history-db.py with field overrides.

Usage: reart.py <id> key=value [key=value ...]
Values starting with @ are read from the named file.
"""
import json, sqlite3, subprocess, sys

DB = 'db/history/history.sqlite'
FIELDS = [
    ('title', '--title'), ('type', '--type'), ('bibkey', '--bibkey'),
    ('credit', '--credit'), ('date_text', '--date'), ('creator', '--creator'),
    ('description', '--description'), ('lat', '--lat'), ('lon', '--lon'),
    ('source_url', '--source-url'), ('download_url', '--download-url'),
    ('local_file', '--local-file'), ('licence', '--licence'), ('pages', '--pages'),
    ('language', '--language'), ('people', '--people'), ('tags', '--tags'),
    ('view_file', '--view-file'), ('routing', '--routing'),
]

def main():
    aid = sys.argv[1]
    over = {}
    for a in sys.argv[2:]:
        k, v = a.split('=', 1)
        if v.startswith('@'):
            v = open(v[1:], encoding='utf-8').read().strip()
        over[k] = v
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    r = db.execute("select * from artifacts where id=?", (aid,)).fetchone()
    if r is None:
        sys.exit('no such artifact: ' + aid)
    cmd = ['/usr/bin/python3', 'tools/history-db.py', 'artifact',
           '--id', aid, '--topic', r['topic']]
    for col, flag in FIELDS:
        val = over.get(col, r[col])
        if col in ('people', 'tags') and val and val.startswith('['):
            val = ';'.join(json.loads(val)) if col == 'people' else ','.join(json.loads(val))
        if val is None or val == '':
            continue
        cmd += [flag, str(val)]
    print(' '.join(repr(c) for c in cmd[:8]), '...')
    subprocess.run(cmd, check=True)

main()
