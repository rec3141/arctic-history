import sys, re, urllib.parse, subprocess
q=sys.argv[1]; field=sys.argv[2] if len(sys.argv)>2 else 'ti'
url="https://www.canadiana.ca/search?"+urllib.parse.urlencode({'q1.0':q,'f1.0':field,'so':'score'})
h=subprocess.run(['curl','-sL','-m','60',url],capture_output=True,text=True).stdout
m=re.search(r'([\d,]+) results? for',h)
print('URL',url); print('hits:', m.group(1) if m else '?')
for blk in re.findall(r'<h3[^>]*>.*?</h3>', h, re.S)[:15]:
    t=re.sub(r'<[^>]+>','',blk); t=re.sub(r'\s+',' ',t).strip()
    print(' -',t[:140])
for a in re.findall(r'href="(/view/[^"]+)"', h)[:15]:
    print('   view:',a)
