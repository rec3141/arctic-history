import sqlite3, re, sys, unicodedata, os, glob
BASE='/data/dev/arctic-history/db/history/'
FILES={
 'white1910placenames':['place-names/files/place-names-gbc1910-ninth-report.txt'],
 'foxe1635northwest':['davis-baffin-hudson/files/davis-baffin-hudson-christy1894-foxe-james-v1.txt','davis-baffin-hudson/files/davis-baffin-hudson-christy1894-foxe-james-v2.txt'],
 'boas1888central':['inuit-oral-history/files/inuit-oral-history-boas-central-eskimo.txt'],
 'parry1821journal':['_staging/txt/journalofvoyagef00inparr.txt'],
 'belcher1855last':['franklin-search/files/franklin-search-belcher-v1.txt','franklin-search/files/franklin-search-belcher-v2.txt'],
 'sverdrup1904newland':['sverdrup-bernier-peary/files/sverdrup-bernier-peary-sverdrup-newland-v1.txt','sverdrup-bernier-peary/files/sverdrup-bernier-peary-sverdrup-newland-v2.txt'],
 'osborn1852stray':['franklin-search/files/franklin-search-osborn-strayleaves.txt'],
 'greely1886three':['nares-greely/files/nares-greely-threeyearsofarct01gree.txt','nares-greely/files/nares-greely-threeyearsofarct02gree.txt'],
 'dunbar1955review':['place-names/files/place-names-dunbar1955-taylor-review.txt'],
 'gst2020greenland':['place-names/files/place-names-greenlandpilot-placenames.txt'],
}
def norm(s):
    s=unicodedata.normalize('NFKD',s)
    s=s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"')
    s=s.replace('—',' ').replace('–',' ').replace('-',' ')
    s=s.lower()
    s=re.sub(r'[^a-z0-9 ]',' ',s)
    s=re.sub(r'\s+',' ',s)
    return s.strip()
CACHE={}
def text(p):
    if p not in CACHE:
        try: CACHE[p]=norm(open(BASE+p,errors='replace').read())
        except Exception as e: CACHE[p]='';print('  !! cannot read',p,e)
    return CACHE[p]
ALL=None
def allfiles():
    global ALL
    if ALL is None:
        ALL=[p[len(BASE):] for p in glob.glob(BASE+'*/files/*.txt')+glob.glob(BASE+'_staging/*.txt')+glob.glob(BASE+'_staging/txt/*.txt')+glob.glob(BASE+'_staging/khp/*.txt')]
    return ALL
def find(frag,bibkey):
    f=norm(frag)
    if len(f)<15: return None,'(too short)'
    hits=[]
    for p in FILES.get(bibkey,[]):
        if f in text(p): hits.append(p)
    if hits: return True,hits
    # partial: try progressively shorter head
    for p in FILES.get(bibkey,[]):
        t=text(p)
        for cut in (0.75,0.5,0.35):
            sub=' '.join(f.split()[:max(4,int(len(f.split())*cut))])
            if sub in t: return 'PARTIAL',[p,'matched first %d%% : %r'%(cut*100,sub)]
    other=[p for p in allfiles() if f in text(p)]
    if other: return 'ELSEWHERE',other
    return False,[]
if __name__=='__main__':
    pass
