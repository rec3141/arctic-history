#!/usr/bin/env python3
"""Patch amundsen-gjoa artifact rows: read the current row, apply a dict of
changes, and re-run tools/history-db.py artifact with the full field set."""
import json, sqlite3, subprocess, sys

DB = 'db/history/history.sqlite'
FIELDS = {
    'type': '--type', 'title': '--title', 'date_text': '--date', 'date_end': '--date-end',
    'creator': '--creator', 'description': '--description', 'lat': '--lat', 'lon': '--lon',
    'source_url': '--source-url', 'download_url': '--download-url', 'local_file': '--local-file',
    'licence': '--licence', 'credit': '--credit', 'bibkey': '--bibkey', 'pages': '--pages',
    'language': '--language', 'view_file': '--view-file',
}

def patch(aid, changes):
    db = sqlite3.connect(DB); db.row_factory = sqlite3.Row
    r = dict(db.execute("select * from artifacts where id=?", (aid,)).fetchone())
    db.close()
    if 'date' in changes:
        changes = dict(changes)
        changes['date_text'] = changes.pop('date')
    r.update(changes)
    cmd = ['/usr/bin/python3', 'tools/history-db.py', 'artifact', '--id', aid,
           '--topic', 'amundsen-gjoa']
    for col, flag in FIELDS.items():
        v = r.get(col)
        if v is None or v == '':
            continue
        cmd += [flag, str(v)]
    for col, flag in (('people', '--people'), ('tags', '--tags')):
        v = r.get(col)
        if not v:
            continue
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except Exception:
                v = [x.strip() for x in v.split(';' if col == 'people' else ',')]
        if v:
            cmd += [flag, (';' if col == 'people' else ',').join(v)]
    if r.get('geometry'):
        cmd += ['--geometry', r['geometry']]
    if r.get('waypoints'):
        cmd += ['--waypoints', r['waypoints']]
    if r.get('routing'):
        cmd += ['--routing', r['routing']]
    out = subprocess.run(cmd, capture_output=True, text=True)
    print(aid, out.returncode, (out.stdout + out.stderr).strip()[:200])

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1]))
    for aid, changes in spec.items():
        patch(aid, changes)
