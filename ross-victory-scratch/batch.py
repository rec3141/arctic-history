import re,sqlite3,sys
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from verify import best,flat,FILES
c=sqlite3.connect('/data/dev/arctic-history/db/history/history.sqlite')
c.row_factory=sqlite3.Row
def cands(text):
    out=[]
    for m in re.finditer(r"'([^']{40,})'",text): out.append(m.group(1))
    for m in re.finditer(r'"([^"]{40,})"',text): out.append(m.group(1))
    return out
rows=list(c.execute("select id,bibkey,description,title from artifacts where topic='ross-victory' order by id"))
for r in rows:
    d=r['description'] or ''
    for q in cands(d):
        q2=q.replace('...',' ')
        bib=r['bibkey'] if r['bibkey'] in FILES else 'ross1835narrative'
        # split on ellipsis into parts
        parts=[p.strip() for p in re.split(r'\.\.\.',q) if len(p.strip())>25]
        for p in parts:
            score,seg=best(flat(FILES[bib]),p)
            if score<0.985:
                print(f"[{r['id']}] {bib} score={score:.3f}")
                print("  DB  :",p[:220])
                print("  TEXT:",seg[:260])
                print()
