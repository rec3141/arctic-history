import re,unicodedata,difflib,os
BASE='/data/dev/arctic-history/db/history/'
FILES=[
 'place-names/files/place-names-gbc1910-ninth-report.txt',
 'davis-baffin-hudson/files/davis-baffin-hudson-christy1894-foxe-james-v1.txt',
 'davis-baffin-hudson/files/davis-baffin-hudson-christy1894-foxe-james-v2.txt',
 'davis-baffin-hudson/files/davis-baffin-hudson-markham1880-davis.txt',
 'davis-baffin-hudson/files/davis-baffin-hudson-markham1881-baffin.txt',
 'inuit-oral-history/files/inuit-oral-history-boas-central-eskimo.txt',
 'inuit-oral-history/files/inuit-oral-history-ross1835-narrative.txt',
 '_staging/txt/journalofvoyagef00inparr.txt',
 '_staging/journalofsecondv00parr.txt',
 'franklin-search/files/franklin-search-belcher-v1.txt',
 'franklin-search/files/franklin-search-belcher-v2.txt',
 'franklin-search/files/franklin-search-osborn-strayleaves.txt',
 'franklin-search/files/franklin-search-sutherland-v1.txt',
 'franklin-search/files/franklin-search-sutherland-v2.txt',
 'mcclure-investigator/files/mcclure-investigator-mcdougall1857.txt',
 'sverdrup-bernier-peary/files/sverdrup-bernier-peary-sverdrup-newland-v1.txt',
 'sverdrup-bernier-peary/files/sverdrup-bernier-peary-sverdrup-newland-v2.txt',
 'sverdrup-bernier-peary/files/sverdrup-bernier-peary-bernier-report-1909.txt',
 'sverdrup-bernier-peary/files/sverdrup-bernier-peary-bernier-report-1910.txt',
 'nares-greely/files/nares-greely-threeyearsofarct01gree.txt',
 'nares-greely/files/nares-greely-threeyearsofarct02gree.txt',
 'nares-greely/files/nares-greely-narrativeofvoyag01nare.txt',
 'nares-greely/files/nares-greely-narrativeofvoyag02nare.txt',
 'greenland-inughuit/files/greenland-inughuit-peary1898-v1.txt',
 'greenland-inughuit/files/greenland-inughuit-peary1898-v2.txt',
 'greenland-inughuit/files/greenland-inughuit-peary1907-nearest.txt',
 'greenland-inughuit/files/greenland-inughuit-macmillan1918-fouryears.txt',
 'crocker-land-1913/files/crocker-land-1913-macmillan1918-fouryears.txt',
 'karluk-cae/files/karluk-cae-stefansson1921-friendly-arctic.txt',
 'qei-from-the-air-1947/files/qei-from-the-air-1947-dunbar1956-arctic-canada-from-the-air.txt',
 'whaling/files/whaling-low1906-neptune.txt',
 'whaling/files/whaling-mdonald1841-eenoolooapik.txt',
 'posts-rcmp-missions/files/posts-rcmp-missions-grant2002-arctic-justice-chapters.txt',
 'place-names/files/place-names-greenlandpilot-placenames.txt',
 'place-names/files/place-names-dunbar1955-taylor-review.txt',
 'place-names/notes/iht-grise-fiord-resolute-place-names.md',
 'place-names/notes/boas1888-names.md',
 'place-names/notes/white1910-northern-gazetteer-extract.md',
 'place-names/notes/grant2002-inuit-names.md',
 'place-names/notes/low1906-whaler-names.md',
 'place-names/notes/qtc-community-names.md',
 'place-names/notes/parry1824-names.md',
 'place-names/notes/ross1835-names.md',
]
def norm(s):
    s=unicodedata.normalize('NFKD',s)
    for a,b in [('’',"'"),('‘',"'"),('“','"'),('”','"'),('—',' '),('–',' '),('-',' ')]:
        s=s.replace(a,b)
    s=re.sub(r'[^A-Za-z0-9 ]',' ',s.lower())
    return re.sub(r'\s+',' ',s).strip()
T={}
def load():
    for p in FILES:
        try: T[p]=norm(open(BASE+p,errors='replace').read())
        except Exception: T[p]=''
def check(frag):
    f=norm(frag)
    w=f.split()
    if len(w)<5: return ('SHORT',0,'','')
    for p,t in T.items():
        if f in t: return ('OK',1.0,p,f)
    # anchor on any 5-token window
    best=None
    for p,t in T.items():
        for st in range(0,len(w)-4):
            anc=' '.join(w[st:st+5])
            i=t.find(anc)
            if i>=0:
                lo=max(0,i-st*8-20); win=t[lo:lo+len(f)+120]
                r=difflib.SequenceMatcher(None,f,win[:len(f)+40]).ratio()
                # refine: sliding
                best2=max((difflib.SequenceMatcher(None,f,win[k:k+len(f)+10]).ratio(),win[k:k+len(f)+10]) for k in range(0,min(60,max(1,len(win)-len(f)))))
                if best is None or best2[0]>best[1]: best=(p,best2[0],best2[1])
                break
    if best: return ('FUZZ',best[1],best[0],best[2])
    return ('MISS',0,'','')
