import json, sqlite3, subprocess
DB='/data/dev/arctic-history/db/history/history.sqlite'
def evupd(eid, **over):
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    r=dict(c.execute("select * from events where id=?", (eid,)).fetchone())
    r.update(over)
    def lst(v):
        if not v: return []
        if isinstance(v,str):
            try: return json.loads(v)
            except Exception: return [x.strip() for x in v.split(';') if x.strip()]
        return list(v)
    a=['/usr/bin/python3','tools/history-db.py','event','--topic',r['topic'],
       '--date',r['date_text'],'--title',r['title']]
    def add(f,v):
        if v not in (None,''): a.extend([f,str(v)])
    add('--date-end',r['date_end']); add('--detail',r['detail'])
    add('--lat',r['lat']); add('--lon',r['lon']); add('--place',r['place'])
    add('--bibkey',r['bibkey'])
    p=lst(r['people']); t=lst(r['tags'])
    if p: add('--people','; '.join(p))
    if t: add('--tags',','.join(t))
    q=subprocess.run(a,cwd='/data/dev/arctic-history',capture_output=True,text=True)
    print(('ok ' if not q.returncode else 'FAIL ')+str(eid), q.stderr[-300:] if q.returncode else '')
