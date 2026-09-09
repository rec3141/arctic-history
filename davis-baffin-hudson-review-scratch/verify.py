import re, sys, unicodedata
D='db/history/davis-baffin-hudson/files/'
FILES={
 'davis':D+'davis-baffin-hudson-markham1880-davis.txt',
 'baffin':D+'davis-baffin-hudson-markham1881-baffin.txt',
 'hudson':D+'davis-baffin-hudson-asher1860-hudson.txt',
 'munk':D+'davis-baffin-hudson-gosch1897-munk-bookii.txt',
 'foxe1':D+'davis-baffin-hudson-christy1894-foxe-james-v1.txt',
 'foxe2':D+'davis-baffin-hudson-christy1894-foxe-james-v2.txt',
}
def norm(s, dehyph=False):
    s=unicodedata.normalize('NFKD',s)
    for a,b in [('’',"'"),('‘',"'"),('“','"'),('”','"'),('—','-'),('–','-')]:
        s=s.replace(a,b)
    if dehyph:
        s=re.sub(r'-\s*\n\s*','',s)   # join hyphenated line breaks
    s=re.sub(r'[^a-z0-9]+',' ',s.lower())
    return ' '.join(s.split())
NORM={k:norm(open(v,encoding='utf-8',errors='replace').read(),dehyph=True) for k,v in FILES.items()}

def ctx(k,i,n):
    return NORM[k][max(0,i-60):i+n+60]

for block in sys.stdin.read().split('\n@@\n'):
    block=block.strip()
    if not block: continue
    label,q=block.split('||',1)
    nq=norm(q)
    hits=[(k,NORM[k].find(nq)) for k in FILES if NORM[k].find(nq)>=0]
    if hits:
        print('OK  ',label,'->',[h[0] for h in hits])
        continue
    # fallback: longest matching prefix, report where it breaks
    words=nq.split()
    best=(0,None,None)
    for k in FILES:
        lo,hi=0,len(words)
        while lo<hi:
            mid=(lo+hi+1)//2
            if NORM[k].find(' '.join(words[:mid]))>=0: lo=mid
            else: hi=mid-1
        if lo>best[0]: best=(lo,k,NORM[k].find(' '.join(words[:lo])))
    n,k,i=best
    print('MISS',label,' matched first',n,'/',len(words),'words in',k)
    if k and n>=4:
        print('     TEXT:',ctx(k,i,len(' '.join(words[:n]))+80))
        print('     WANT:',nq[:220])
