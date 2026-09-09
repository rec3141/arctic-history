import json,urllib.request,urllib.parse,sys,time
def q(name,num=15):
    url='https://geogratis.gc.ca/services/geoname/en/geonames.json?q=%s&num=%d'%(urllib.parse.quote(name),num)
    req=urllib.request.Request(url,headers={'User-Agent':'arctic-history review (U Manitoba)'})
    j=json.loads(urllib.request.urlopen(req,timeout=40).read().decode())
    return j.get('items',[])
for n in sys.argv[1:]:
    print('==',n)
    for it in q(n):
        st=it['status']['code'] if isinstance(it.get('status'),dict) else it.get('status')
        if it.get('province',{}).get('code') in ('62','61') or True:
            print('   %-32s %-18s %-8s %s %9.4f %9.4f prov=%s' % (it['name'][:32], st, it.get('decision'), (it.get('concise') or {}).get('code'), it.get('latitude') or 0, it.get('longitude') or 0, (it.get('province') or {}).get('code')))
    time.sleep(0.8)
