#!/usr/bin/python3
"""Re-run tools/history-db.py artifact for an existing row, with field overrides.

Reads the current row, applies overrides, and shells out to the tool so the
tool remains the only writer.
"""
import json
import sqlite3
import subprocess
import sys

DB = '/data/dev/arctic-history/db/history/history.sqlite'
TOOL = ['/usr/bin/python3', '/data/dev/arctic-history/tools/history-db.py']

FLAGS = {
    'title': '--title', 'bibkey': '--bibkey', 'credit': '--credit',
    'type': '--type', 'date_text': '--date', 'date_end': '--date-end',
    'creator': '--creator', 'description': '--description', 'lat': '--lat',
    'lon': '--lon', 'geometry': '--geometry', 'source_url': '--source-url',
    'download_url': '--download-url', 'local_file': '--local-file',
    'licence': '--licence', 'pages': '--pages', 'language': '--language',
    'view_file': '--view-file', 'routing': '--routing',
}


def listish(raw):
    if not raw:
        return ''
    try:
        v = json.loads(raw)
    except Exception:
        return raw
    if isinstance(v, list):
        return v
    return raw


def update(aid, **over):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    row = con.execute('select * from artifacts where id=?', (aid,)).fetchone()
    if row is None:
        raise SystemExit('no artifact %s' % aid)
    d = dict(row)
    d.update(over)
    cmd = TOOL + ['artifact', '--id', aid, '--topic', d['topic']]
    for col, flag in FLAGS.items():
        v = d.get(col)
        if v is None or v == '':
            continue
        cmd += [flag, str(v)]
    people = listish(d.get('people'))
    if isinstance(people, list) and people:
        cmd += ['--people', ';'.join(people)]
    elif isinstance(people, str) and people.strip():
        cmd += ['--people', people]
    tags = listish(d.get('tags'))
    if isinstance(tags, list) and tags:
        cmd += ['--tags', ','.join(tags)]
    elif isinstance(tags, str) and tags.strip():
        cmd += ['--tags', tags]
    wp = d.get('waypoints')
    if wp:
        cmd += ['--waypoints', wp if isinstance(wp, str) else json.dumps(wp)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(aid, r.returncode, (r.stdout + r.stderr).strip()[:300])


if __name__ == '__main__':
    print('import and call update()')
