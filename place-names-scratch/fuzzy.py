import re,unicodedata,glob,difflib,os
BASE='/data/dev/arctic-history/db/history/'
def norm(s):
    s=unicodedata.normalize('NFKD',s)
    for a,b in [('’',"'"),('‘',"'"),('“','"'),('”','"'),('—',' '),('–',' '),('-',' ')]:
        s=s.replace(a,b)
    s=re.sub(r'[^A-Za-z0-9 ]',' ',s.lower())
    return re.sub(r'\s+',' ',s).strip()
CACHE={}
def toks(p):
    if p not in CACHE:
        try: CACHE[p]=norm(open(BASE+p,errors='replace').read()).split()
        except Exception: CACHE[p]=[]
    return CACHE[p]
def best(frag,paths):
    ft=norm(frag).split()
    if len(ft)<4: return None
    out=[]
    for p in paths:
        T=toks(p)
        if not T: continue
        # anchor: find any 4-token window of frag in T
        idxs=[]
        for start in range(0,max(1,len(ft)-3)):
            key=ft[start:start+4]
            for i in range(len(T)-4):
                if T[i:i+4]==key:
                    idxs.append(i-start); break
            if idxs: break
        if not idxs: continue
        i=max(0,idxs[0]); w=T[i:i+len(ft)+8]
        r=difflib.SequenceMatcher(None,ft,w[:len(ft)+4]).ratio()
        out.append((r,p,' '.join(w[:len(ft)+4])))
    out.sort(reverse=True)
    return out[0] if out else None
def allfiles():
    return [p[len(BASE):] for p in glob.glob(BASE+'*/files/*.txt')+glob.glob(BASE+'_staging/*.txt')+glob.glob(BASE+'_staging/txt/*.txt')+glob.glob(BASE+'_staging/khp/*.txt')+glob.glob(BASE+'*/notes/*.md')]
