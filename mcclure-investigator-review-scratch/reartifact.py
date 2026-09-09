#!/usr/bin/env python3
"""Re-run `history-db.py artifact` for an existing row, preserving every field
except the ones named on the command line as key=value overrides.

    reartifact.py <id> description="new text" title="new title"
"""
import json, sqlite3, subprocess, sys, pathlib

DB = '/data/dev/arctic-history/db/history/history.sqlite'
ROOT = '/data/dev/arctic-history'


def rerun(aid, **over):
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    r = c.execute('select * from artifacts where id=?', (aid,)).fetchone()
    if not r:
        raise SystemExit(f'no artifact {aid}')
    d = dict(r)
    d.update(over)
    cmd = ['/usr/bin/python3', 'tools/history-db.py', 'artifact',
           '--id', d['id'], '--topic', d['topic'], '--type', d['type'],
           '--title', d['title'], '--bibkey', d['bibkey'], '--credit', d['credit']]

    def opt(flag, val):
        if val not in (None, ''):
            cmd.extend([flag, str(val)])

    opt('--date', d['date_text'])
    # date_end is only passed when it is not already implied by date_text
    if d['date_end'] and '/' not in (d['date_text'] or '') and d['date_end'] != d['date_start']:
        opt('--date-end', d['date_end'])
    opt('--creator', d['creator'])
    opt('--description', d['description'])
    opt('--licence', d['licence'])
    opt('--pages', d['pages'])
    opt('--language', d['language'])
    opt('--source-url', d['source_url'])
    opt('--download-url', d['download_url'])
    opt('--local-file', d['local_file'])
    opt('--view-file', d['view_file'])
    opt('--routing', d['routing'])
    if d['lat'] is not None:
        opt('--lat', d['lat'])
        opt('--lon', d['lon'])
    if d['geometry']:
        opt('--geometry', d['geometry'])
    if d['waypoints']:
        opt('--waypoints', d['waypoints'])
    for flag, col, sep in (('--people', 'people', ';'), ('--tags', 'tags', ',')):
        v = d[col]
        if v:
            try:
                items = json.loads(v) if isinstance(v, str) else v
            except Exception:
                items = [v]
            if items:
                opt(flag, sep.join(items))
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if p.returncode:
        print('FAIL', aid, p.stderr.strip()[:400])
    else:
        print('ok  ', aid, p.stdout.strip())
    return p.returncode


if __name__ == '__main__':
    aid = sys.argv[1]
    over = {}
    for arg in sys.argv[2:]:
        k, _, v = arg.partition('=')
        over[k] = v
    rerun(aid, **over)
