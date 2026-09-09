import re
RAW=open('/data/dev/arctic-history/db/history/place-names/files/place-names-gbc1910-ninth-report.txt',errors='replace').read()
# page headers: a standalone number line adjacent to a running head
marks=[]
for m in re.finditer(r'\n\s*(\d{1,3})\s*\n', RAW):
    n=int(m.group(1))
    ctx=RAW[max(0,m.start()-300):m.end()+300]
    if 'SESSIONAL' in ctx.upper() or 'PLACE-NAMES' in ctx.upper() or 'GEOGRAPHIC BOARD' in ctx.upper() or 'EDWARD VII' in ctx.upper() or 'GEORGE  V' in ctx.upper():
        marks.append((m.start(),n))
marks.sort()
def page(idx):
    p=None
    for off,n in marks:
        if off<=idx: p=n
        else: break
    return p
def findpage(pattern):
    m=re.search(pattern,RAW,re.I|re.S)
    return (page(m.start()) if m else None), (m.start() if m else None)
