import re,sys,unicodedata
FILES={
 'v1':'db/history/amundsen-gjoa/files/amundsen-gjoa-northwest-passage-v1.txt',
 'v1b':'db/history/amundsen-gjoa/files/northwestpassage01amunuoft.txt',
 'v2':'db/history/amundsen-gjoa/files/amundsen-gjoa-northwest-passage-v2.txt',
 'v2b':'db/history/amundsen-gjoa/files/northwestpassage02amun.txt',
}
def norm(s):
    s=unicodedata.normalize('NFKD',s)
    s=s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"')
    s=re.sub(r'[^a-z0-9]+',' ',s.lower())
    return ' '.join(s.split())
TXT={k:norm(open(v,encoding='utf-8',errors='replace').read()) for k,v in FILES.items()}
RAW={k:open(v,encoding='utf-8',errors='replace').read() for k,v in FILES.items()}
def find(q,ctx=120):
    n=norm(q)
    out=[]
    for k,t in TXT.items():
        i=t.find(n)
        if i>=0:
            out.append((k,i,t[max(0,i-ctx):i+len(n)+ctx]))
    return out
if __name__=='__main__':
    q=sys.argv[1]
    r=find(q)
    if not r: print("NOT FOUND:",q[:90])
    for k,i,c in r: print(f"[{k}@{i}] ...{c}...")
