#!/usr/bin/env python3
"""Re-run history-db.py artifact for an existing row, changing only named fields.
Required CLI args (topic/title/bibkey/credit/type) are read back from the row."""
import json, sqlite3, subprocess, sys, tempfile, os

DB = 'db/history/history.sqlite'
PY = '/usr/bin/python3'
TOOL = 'tools/history-db.py'


def edit(aid, **changes):
    c = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
    c.row_factory = sqlite3.Row
    r = c.execute('SELECT * FROM artifacts WHERE id=?', (aid,)).fetchone()
    if r is None:
        raise SystemExit(f'no such artifact {aid}')
    v = dict(r)
    v.update(changes)
    args = [PY, TOOL, 'artifact', '--id', aid,
            '--topic', v['topic'], '--title', v['title'],
            '--bibkey', v['bibkey'], '--credit', v['credit'],
            '--type', v['type']]
    tmp = None
    if 'description' in changes:
        fd, tmp = tempfile.mkstemp(suffix='.txt', dir='cook-review-scratch')
        os.write(fd, changes['description'].encode()); os.close(fd)
        args += ['--description-file', tmp]
    for k, flag in (('date', '--date'), ('date_end', '--date-end'),
                    ('pages', '--pages'), ('lat', '--lat'), ('lon', '--lon'),
                    ('tags', '--tags'), ('creator', '--creator'),
                    ('licence', '--licence'), ('local_file', '--local-file'),
                    ('view_file', '--view-file'), ('source_url', '--source-url')):
        if k in changes and changes[k] not in (None, ''):
            args += [flag, str(changes[k])]
    if 'date' not in changes and v.get('date_text'):
        args += ['--date', v['date_text']]
    if 'people' in changes:
        p = changes['people']
        args += ['--people', ';'.join(p) if isinstance(p, list) else p]
    elif v.get('people'):
        try:
            p = json.loads(v['people'])
            if p:
                args += ['--people', ';'.join(p)]
        except ValueError:
            pass
    if 'tags' not in changes and v.get('tags'):
        try:
            t = json.loads(v['tags'])
            t = ','.join(t) if isinstance(t, list) else str(t)
        except ValueError:
            t = v['tags']
        if t:
            args += ['--tags', t]
    out = subprocess.run(args, capture_output=True, text=True)
    if tmp:
        os.unlink(tmp)
    if out.returncode:
        print('FAIL', aid, out.stdout, out.stderr)
    else:
        print('ok  ', aid, out.stdout.strip())
    return out.returncode
