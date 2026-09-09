"""Rewrite an artifact through tools/history-db.py, preserving every field
not explicitly overridden."""
import json, sqlite3, subprocess, sys
DB='/data/dev/arctic-history/db/history/history.sqlite'
TOOL=['/usr/bin/python3','tools/history-db.py']
def get(aid):
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    r=c.execute("select * from artifacts where id=?",(aid,)).fetchone()
    if not r: raise SystemExit('no artifact '+aid)
    return dict(r)
def upd(aid, **over):
    r=get(aid); r.update(over)
    args=TOOL+['artifact','--id',r['id'],'--topic',r['topic'],'--type',r['type'],
               '--title',r['title'],'--bibkey',r['bibkey'],'--credit',r['credit']]
    def add(flag,val):
        if val not in (None,''): args.extend([flag,str(val)])
    add('--date',r['date_text']); add('--date-end',r['date_end'] if r['date_text'] and '/' in str(r['date_text']) else None)
    add('--creator',r['creator']); add('--description',r['description'])
    add('--lat',r['lat']); add('--lon',r['lon'])
    add('--source-url',r['source_url']); add('--download-url',r['download_url'])
    add('--local-file',r['local_file']); add('--licence',r['licence'])
    add('--pages',r['pages']); add('--language',r['language'])
    add('--view-file',r['view_file'])
    if r['routing']: add('--routing',r['routing'])
    if r['geometry']: add('--geometry',r['geometry'])
    if r['waypoints']: add('--waypoints',r['waypoints'])
    def lst(v):
        if v is None: return []
        if isinstance(v,str):
            v=v.strip()
            if not v: return []
            try: return json.loads(v)
            except Exception: return [x.strip() for x in v.split(';') if x.strip()]
        return list(v)
    ppl=lst(r['people']); tgs=lst(r['tags'])
    if ppl: add('--people','; '.join(ppl))
    if tgs: add('--tags',','.join(tgs))
    p=subprocess.run(args,cwd='/data/dev/arctic-history',capture_output=True,text=True)
    if p.returncode: print('FAIL',aid,p.stderr[-500:]); return False
    print('ok',aid); return True
