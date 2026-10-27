import urllib.request
picks = {
 'porkbelly':'1568600891621-50f697b9a1c7',
 'samosa':'1601050690597-df0568f70950',
 'biryani':'1589302168068-964664d93dc0',
 'naan':'1567337710282-00832b415979',
 'dining_dark':'1590846406792-0adc7f938f1d',
 'dumpling':'1563245372-f21724e3856d',
 'butterchicken':'1603894584373-5ac82b2ae398',
 'prawn':'1563379926898-05f4575a45d8',
 'shortrib':'1529692236671-f1f6cf9683ba',
 'ribs':'1529193591184-b1d58069ecdd',
 'squash':'1567188040759-fb8a883dc6d8',
 'cocktail':'1514362545857-3bc16c4c7d1b',
 'chef':'1551218808-94e220e084d2',
 'spices':'1532336414038-cf19250c5757',
 'dessert':'1551024506-0bccd828d307',
 'steak':'1558030006-450675393462',
 'carpaccio':'1504674900247-0877df9cc836'
}
for name,pid in picks.items():
    url=f'https://images.unsplash.com/photo-{pid}?w=1800&q=88&fm=jpg'
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        open(f'_final/hi_{name}.jpg','wb').write(urllib.request.urlopen(req,timeout=60).read())
        print(name,'ok')
    except Exception as e: print(name,'ERR',e)
