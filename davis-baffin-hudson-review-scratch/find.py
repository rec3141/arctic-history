import re,sys,unicodedata
D='db/history/davis-baffin-hudson/files/'
FILES={'davis':'davis-baffin-hudson-markham1880-davis.txt','baffin':'davis-baffin-hudson-markham1881-baffin.txt',
 'hudson':'davis-baffin-hudson-asher1860-hudson.txt','munk':'davis-baffin-hudson-gosch1897-munk-bookii.txt',
 'foxe1':'davis-baffin-hudson-christy1894-foxe-james-v1.txt','foxe2':'davis-baffin-hudson-christy1894-foxe-james-v2.txt'}
def norm(s):
    s=unicodedata.normalize('NFKD',s)
    s=re.sub(r'-\s*\n\s*','',s)
    s=re.sub(r'[^a-z0-9]+',' ',s.lower())
    return ' '.join(s.split())
key=sys.argv[1]; q=norm(sys.argv[2]); w=int(sys.argv[3]) if len(sys.argv)>3 else 300
t=norm(open(D+FILES[key],encoding='utf-8',errors='replace').read())
i=0;n=0
while True:
    i=t.find(q,i)
    if i<0: break
    n+=1; print('---',i); print(t[max(0,i-w):i+len(q)+w]); i+=1
    if n>6: break
if n==0: print('NOT FOUND')
