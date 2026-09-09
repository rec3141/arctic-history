"""Re-write an artifact through tools/history-db.py, preserving every field, applying changes."""
import sqlite3, subprocess, sys, json, os
DB='db/history/history.sqlite'
FIELDS=[('type','--type'),('title','--title'),('bibkey','--bibkey'),('credit','--credit'),
        ('date_text','--date'),('date_end','--date-end'),('creator','--creator'),
        ('description','--description'),('lat','--lat'),('lon','--lon'),
        ('source_url','--source-url'),('download_url','--download-url'),('local_file','--local-file'),
        ('licence','--licence'),('pages','--pages'),('language','--language'),
        ('view_file','--view-file'),('routing','--routing'),('geometry','--geometry'),('waypoints','--waypoints')]
def edit(aid, **changes):
    c=sqlite3.connect('file:%s?mode=ro'%DB,uri=True); c.row_factory=sqlite3.Row
    r=c.execute("select * from artifacts where id=?",(aid,)).fetchone()
    if not r: raise SystemExit('no artifact '+aid)
    row=dict(r)
    row.update(changes)
    cmd=['/usr/bin/python3','tools/history-db.py','artifact','--id',aid,'--topic',row['topic']]
    for f,flag in FIELDS:
        v=row.get(f)
        if v in (None,''): continue
        cmd += [flag, str(v)]
    for f,flag in (('people','--people'),('tags','--tags')):
        v=row.get(f)
        if not v: continue
        if isinstance(v,str):
            try: v=json.loads(v)
            except Exception: v=[v]
        if isinstance(v,list):
            if f=='people': v=';'.join(v)
            else: v=','.join(v)
        if v: cmd += [flag, v]
    p=subprocess.run(cmd,capture_output=True,text=True)
    print(aid, p.returncode, (p.stdout or '').strip()[:120], (p.stderr or '').strip()[:300])
