#!/bin/bash
# usage: sheet.sh <ia-id>
ID=$1
mkdir -p sheets
ls thumbs/$ID/*.jpg | sort -t n -k2 -n > /tmp/list_$ID.txt
/usr/bin/python3 - "$ID" <<'PY'
import sys,os,re,subprocess
ID=sys.argv[1]
fs=sorted(os.listdir(f'thumbs/{ID}'), key=lambda x:int(re.search(r'n(\d+)',x).group(1)))
per=110
for i in range(0,len(fs),per):
    chunk=fs[i:i+per]
    labels=[]
    args=[]
    for f in chunk:
        n=int(re.search(r'n(\d+)',f).group(1))
        args+=['-label',str(n),f'thumbs/{ID}/{f}']
    out=f'sheets/{ID}-{i//per}.jpg'
    subprocess.run(['montage']+args+['-tile','11x10','-geometry','150x+2+2','-background','white','-pointsize','16',out],check=True)
    print(out)
PY
