import re,sys
path=sys.argv[1]; pat=sys.argv[2]
raw=open(path,encoding='utf-8',errors='replace').read()
# build collapsed text with map back to raw offsets
out=[];idx=[]
prev_space=False
for i,ch in enumerate(raw):
    if ch.isspace():
        if not prev_space:
            out.append(' ');idx.append(i)
        prev_space=True
    else:
        out.append(ch);idx.append(i);prev_space=False
flat=''.join(out)
ctx=int(sys.argv[3]) if len(sys.argv)>3 else 300
for m in re.finditer(pat,flat,re.I):
    s=max(0,m.start()-ctx);e=min(len(flat),m.end()+ctx)
    # line number in raw
    ln=raw.count('\n',0,idx[m.start()])+1
    print(f"--- line {ln} ---")
    print(flat[s:e])
    print()
