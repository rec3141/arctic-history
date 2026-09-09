import re,sys
raw=open('/data/dev/arctic-history/db/history/ross-victory/files/ross-victory-narrative-1835.txt',encoding='utf-8',errors='replace').read()
flat=re.sub(r'\s+',' ',raw)
n=sys.argv[1]
pats=[rf'TO THE ARCTIC REGIONS\. {n}\b', rf'\b{n} SECOND VOYAGE']
for p in pats:
    for m in re.finditer(p,flat):
        print('---',p)
        print(flat[m.start():m.start()+int(sys.argv[2] if len(sys.argv)>2 else 700)])
        print()
