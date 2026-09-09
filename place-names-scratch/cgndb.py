import sqlite3, json, urllib.request, urllib.parse, time, re, sys, os, math
c=sqlite3.connect('file:db/history/history.sqlite?mode=ro',uri=True); c.row_factory=sqlite3.Row
pages=c.execute("select slug,body from pages where topic='place-names'").fetchall()
names=set()
for p in pages:
    for m in re.finditer(r'\[\[place:([^\]|]+)(\|[^\]]*)?\]\]', p['body']):
        names.add(m.group(1).strip())
# also every place row of the topic
for r in c.execute("select name from places where topic='place-names'"): names.add(r['name'])
rows={}
for n in sorted(names):
    r=c.execute("select * from places where name=?",(n,)).fetchone()
    rows[n]=dict(r) if r else None
cache='place-names-scratch/cgndb-cache.json'
data=json.load(open(cache)) if os.path.exists(cache) else {}
def q(url):
    if url in data: return data[url]
    req=urllib.request.Request(url, headers={'User-Agent':'arctic-history review (rec3141, U Manitoba)'})
    for attempt in range(3):
        try:
            j=json.loads(urllib.request.urlopen(req,timeout=40).read().decode('utf-8'))
            data[url]=j; json.dump(data,open(cache,'w')); time.sleep(0.7); return j
        except Exception as e:
            time.sleep(3)
            err=str(e)
    data[url]={'error':err}; json.dump(data,open(cache,'w')); return data[url]
out={}
for n in sorted(names):
    url='https://geogratis.gc.ca/services/geoname/en/geonames.json?q=%s&num=20'%urllib.parse.quote(n)
    j=q(url)
    items=j.get('items',[]) if isinstance(j,dict) else []
    out[n]={'row':rows[n],'items':[{k:it.get(k) for k in ('id','name','latitude','longitude','decision','status','concise','province','feature')} for it in items]}
json.dump(out,open('place-names-scratch/cgndb-results.json','w'),indent=1)
print('done',len(out))
