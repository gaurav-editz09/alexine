import urllib.request, re
for url in ['https://www.pexels.com/search/fine%20dining/','https://www.pexels.com/search/dark%20food%20photography/']:
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36'})
        html = urllib.request.urlopen(req, timeout=40).read().decode('utf-8','ignore')
        print(url, len(html))
        ids = re.findall(r'images\.pexels\.com/photos/(\d+)/', html)
        print('ids', len(ids), list(dict.fromkeys(ids))[:20])
    except Exception as e: print('ERR', e)
