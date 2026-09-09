#!/usr/bin/env python3
"""Update fields on an existing artifact row without losing the rest of it.

    upd.py <artifact-id> field=value [field=value ...]
    upd.py --file changes.json          # {"id": {"field": "value", ...}, ...}

Reads the row, overlays the changes, and re-issues history-db.py artifact with
every field, because the writer replaces the whole row.
"""
import json
import sqlite3
import subprocess
import sys

DB = '/data/dev/arctic-history/db/history/history.sqlite'
TOOL = ['/usr/bin/python3', 'tools/history-db.py', 'artifact']
CWD = '/data/dev/arctic-history'

FLAGS = {
    'type': '--type', 'title': '--title', 'date_text': '--date', 'date_end': '--date-end',
    'creator': '--creator', 'description': '--description', 'lat': '--lat', 'lon': '--lon',
    'geometry': '--geometry', 'waypoints': '--waypoints', 'source_url': '--source-url',
    'download_url': '--download-url', 'local_file': '--local-file', 'licence': '--licence',
    'credit': '--credit', 'bibkey': '--bibkey', 'pages': '--pages', 'language': '--language',
    'view_file': '--view-file', 'routing': '--routing',
}


def update(aid, changes):
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    row = c.execute('select * from artifacts where id=?', (aid,)).fetchone()
    if row is None:
        raise SystemExit(f'no such artifact: {aid}')
    r = dict(row)
    r.update(changes)
    cmd = TOOL + ['--id', aid, '--topic', r['topic']]
    for col, flag in FLAGS.items():
        v = r.get(col)
        if v in (None, ''):
            continue
        cmd += [flag, str(v)]
    # people and tags are stored as JSON lists, given as semicolon/comma strings
    people = json.loads(r['people'] or '[]')
    if people:
        cmd += ['--people', ';'.join(people)]
    tags = json.loads(r['tags'] or '[]')
    if tags:
        cmd += ['--tags', ','.join(tags)]
    out = subprocess.run(cmd, cwd=CWD, capture_output=True, text=True)
    if out.returncode:
        raise SystemExit(f'{aid}: {out.stderr.strip()}')
    return out.stdout.strip()


if __name__ == '__main__':
    if sys.argv[1] == '--file':
        spec = json.load(open(sys.argv[2]))
        for aid, ch in spec.items():
            print(update(aid, ch))
    else:
        aid = sys.argv[1]
        ch = dict(kv.split('=', 1) for kv in sys.argv[2:])
        print(update(aid, ch))
