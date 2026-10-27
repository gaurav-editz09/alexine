import urllib.request, os
picks = {
 'porkbelly':'1568600891621',
 'samosa':'1601050690597',
 'biryani':'1589302168068',
 'naan':'1567337710282',
 'dining_warm':'1552566626-52f8b828add9',
 'dining_dark':'1590846406792',
 'dining_moody':'1414235077428-338989a2e8c0',
 'bar':'1514933651103-005eec06c04b',
 'woman':'1592861956120-e524fc739696',
 'grill':'1555939594-58d7cb561ad1'
}
for name,pid in picks.items():
    url=f'https://images.unsplash.com/photo-{pid}?w=2000&q=88&fm=jpg'
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        open(f'_final/hi_{name}.jpg','wb').write(urllib.request.urlopen(req,timeout=60).read())
        print(name,'ok')
    except Exception as e: print(name,'ERR',e)
