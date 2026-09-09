import re,sys,sqlite3,difflib,json,os
BASE='/data/dev/arctic-history/db/history/ross-victory/files/'
FILES={'ross1835narrative':BASE+'ross-victory-narrative-1835.txt',
       'huish1835last':BASE+'ross-victory-huish-1835.txt',
       'ross1835appendix':BASE+'ross-victory-appendix-1835.txt'}
cache={}
def flat(p):
    if p not in cache:
        t=open(p,encoding='utf-8',errors='replace').read()
        cache[p]=re.sub(r'\s+',' ',t)
    return cache[p]
def norm(s):
    s=s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"')
    s=s.replace('—',' ').replace('–','-')
    s=re.sub(r'\s+',' ',s)
    return s
def best(hay,needle):
    n=norm(needle); h=norm(hay)
    if n.lower() in h.lower(): return 1.0,'exact'
    # sliding window fuzzy
    sm=difflib.SequenceMatcher(None,None,None)
    words=n.split()
    # find anchor using a distinctive 4-word run
    bestr=0;bestseg=''
    for i in range(0,max(1,len(words)-3)):
        anchor=' '.join(words[i:i+4])
        for m in re.finditer(re.escape(anchor),h,re.I):
            s=max(0,m.start()-len(n)); e=min(len(h),m.start()+2*len(n))
            seg=h[s:e]
            r=difflib.SequenceMatcher(None,n.lower(),seg.lower()).find_longest_match(0,len(n),0,len(seg))
            # ratio via quick_ratio on best local window
            for off in range(0,max(1,len(seg)-len(n)),40):
                w=seg[off:off+len(n)+40]
                rr=difflib.SequenceMatcher(None,n.lower(),w.lower()).ratio()
                if rr>bestr: bestr=rr;bestseg=w
        if bestr>0.93: break
    return bestr,bestseg
if __name__=='__main__':
    bib=sys.argv[1]; phrase=sys.argv[2]
    r,seg=best(flat(FILES[bib]),phrase)
    print(round(r,3))
    if r<1.0: print('FOUND:',seg)
