import urllib.request, os
picks = {
 'hero_a':'1558030006-450675393462',
 'hero_b':'1529692236671-f1f6cf9683ba',
 'hero_c':'1555939594-58d7cb561ad1',
 'shortrib':'1529193591184-b1d58069ecdd',
 'butterchicken':'1603894584373-5ac82b2ae398',
 'prawnpasta':'1563379926898-05f4575a45d8',
 'skewers':'1555939594-58d7cb561ad1',
 'porkbelly':'1590846406792-0adc7f938f1d',
 'dessert':'1551024506-0bccd828d307',
 'samosa':'1596797038530-2c107229654b',
 'dumpling':'1563245372-f21724e3856d',
 'squash':'1567188040759-fb8a883dc6d8',
 'pie':'1519915028121-7d3463d20b13',
 'cocktail':'1514362545857-3bc16c4c7d1b',
 'spices':'1532336414038-cf19250c5757',
 'chef':'1551218808-94e220e084d2',
 'dining1':'1414235077428-338989a2e8c0',
 'dining2':'1552566626-52f8b828add9',
 'dining3':'1592861956120-e524fc739696',
 'bar':'1514933651103-005eec06c04b',
 'bar2':'1560624052-449f5ddf0c31',
 'woman':'1495521821757-a1efb6729352',
 'table':'1543352634-a1c51d9f1fa7',
 'curry':'1603360946369-dc9bb6258143',
 'salmon':'1502301103665-0b95cc738daf',
 'biryani':'1601050690597-df0568f70950',
 'ribs':'1529193591184-b1d58069ecdd',
 'carpaccio':'1504674900247-0877df9cc836'
}
os.makedirs('_final', exist_ok=True)
for name,pid in picks.items():
    url=f'https://images.unsplash.com/photo-{pid}?w=1400&q=80&fm=jpg'
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        open(f'_final/{name}.jpg','wb').write(urllib.request.urlopen(req,timeout=40).read())
        print(name,'ok')
    except Exception as e: print(name,'ERR',e)
