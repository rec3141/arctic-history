import re,sqlite3,sys
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from verify import best,flat,FILES
c=sqlite3.connect('/data/dev/arctic-history/db/history/history.sqlite')
N=flat(FILES['ross1835narrative']); H=flat(FILES['huish1835last']); A=flat(FILES['ross1835appendix'])
for slug,body in c.execute("select slug,body from pages where topic='ross-victory'"):
    cands=[m.group(1) for m in re.finditer(r'"([^"]{30,})"',body)]
    for m in re.finditer(r'^> (.+(?:\n> .+)*)',body,re.M):
        cands.append(re.sub(r'\n> ',' ',m.group(1)))
    for q in cands:
        q=re.sub(r'\[\[[^\]|]*\|','',q).replace(']]','').replace('*','')
        for part in [p.strip() for p in q.split('...') if len(p.strip())>25]:
            s1,_=best(N,part); s2,_=best(H,part); s3,_=best(A,part)
            s=max(s1,s2,s3)
            if s<0.90:
                print(f"{slug}  {s:.2f}  {part[:150]}")
