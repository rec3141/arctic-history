#!/usr/bin/env python3
"""Re-issue an artifact through the CLI with every existing field preserved,
changing only what is named in EDITS."""
import sqlite3, subprocess, json, sys

EDITS = json.load(open(sys.argv[1]))

c = sqlite3.connect('file:db/history/history.sqlite?mode=ro', uri=True)
c.row_factory = sqlite3.Row

for aid, changes in EDITS.items():
    r = c.execute("select * from artifacts where id=?", (aid,)).fetchone()
    if not r:
        print('MISSING', aid); continue
    d = dict(r)
    d.update(changes)
    cmd = ['/usr/bin/python3', 'tools/history-db.py', 'artifact',
           '--id', d['id'], '--topic', d['topic'], '--type', d['type'],
           '--title', d['title'], '--bibkey', d['bibkey'], '--credit', d['credit']]
    def add(flag, val):
        if val not in (None, ''):
            cmd.extend([flag, str(val)])
    add('--date', d['date_text'])
    add('--date-end', d['date_end'] if d['date_end'] and '/' not in (d['date_text'] or '') and d['date_end'] != d['date_start'] else None)
    add('--creator', d['creator'])
    add('--description', d['description'])
    add('--lat', d['lat']); add('--lon', d['lon'])
    if d['geometry']: cmd.extend(['--geometry', d['geometry']])
    if d['waypoints']: cmd.extend(['--waypoints', d['waypoints']])
    add('--source-url', d['source_url']); add('--download-url', d['download_url'])
    add('--local-file', d['local_file']); add('--licence', d['licence'])
    add('--pages', d['pages']); add('--language', d['language'])
    add('--view-file', d['view_file'])
    if d['routing']: cmd.extend(['--routing', d['routing']])
    ppl = json.loads(d['people'] or '[]'); tgs = json.loads(d['tags'] or '[]')
    if ppl: cmd.extend(['--people', ';'.join(ppl)])
    if tgs: cmd.extend(['--tags', ','.join(tgs)])
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(aid, '|', (res.stdout + res.stderr).strip()[:140])
