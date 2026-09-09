import sqlite3,re,sys
sys.path.insert(0,'place-names-scratch')
from quotecheck import find, norm
c=sqlite3.connect('file:db/history/history.sqlite?mode=ro',uri=True); c.row_factory=sqlite3.Row
rows=c.execute("select * from artifacts where topic='place-names' and type='quote' order by id").fetchall()
for r in rows:
    d=r['description'] or ''
    frags=re.findall(r"'([^']{25,})'", d)+re.findall(r'"([^"]{25,})"', d)
    print('###',r['id'],r['bibkey'],r['pages'])
    if not frags: print('   no fragment found in description')
    for f in frags:
        for part in re.split(r'\s*\.\.\.\s*', f):
            st,info=find(part,r['bibkey'])
            print('   %-9s %r' % (st,part[:90]))
            if st in ('PARTIAL','ELSEWHERE'): print('        ',info)
