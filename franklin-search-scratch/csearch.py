import sys,json,time,urllib.parse,urllib.request
UA="arctic-history-research/1.0 (CCGS Amundsen history layer; UManitoba; hawkwing3141@gmail.com)"
def api(params):
    u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(params)
    r=urllib.request.Request(u,headers={"User-Agent":UA})
    return json.load(urllib.request.urlopen(r,timeout=60))
for i,q in enumerate(sys.argv[1:]):
    if i: time.sleep(12)
    try:
        d=api(dict(action="query",format="json",list="search",srnamespace=6,srlimit=15,srsearch=q))
        print("=== "+q)
        for x in d["query"]["search"]: print("   "+x["title"])
    except Exception as e:
        print("=== "+q+"  ERR "+str(e))
