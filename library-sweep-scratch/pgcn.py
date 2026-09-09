import sys,re,subprocess,urllib.parse
q=sys.argv[1]
url="https://publications.gc.ca/site/eng/search/search.html?"+urllib.parse.urlencode({'cnst':q})
h=subprocess.run(['curl','-sL','-m','60',url],capture_output=True,text=True).stdout
for u,t in re.findall(r'href="(/site/eng/[0-9.]+/publication\.html)"[^>]*>(.*?)</a>',h,re.S)[:15]:
    t=re.sub(r'<[^>]+>','',t); t=re.sub(r'\s+',' ',t).strip()
    print('  https://publications.gc.ca'+u,'|',t[:120])
