import urllib.request, re, os
queries = {
 'finedining':'fine-dining',
 'plated':'gourmet-food-dark',
 'fire':'chef-fire-cooking',
 'luxrest':'luxury-restaurant-interior-dark',
 'dessert':'plated-dessert-fine-dining',
 'grill':'grilled-meat-dark',
 'cocktail':'craft-cocktail-dark-bar',
 'chef':'chef-plating'
}
for name,q in queries.items():
    url = f'https://unsplash.com/s/photos/{q}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36'})
        html = urllib.request.urlopen(req, timeout=40).read().decode('utf-8','ignore')
        ids = re.findall(r'images\.unsplash\.com/photo-([a-zA-Z0-9_-]+)', html)
        seen=[]
        for i in ids:
            if i not in seen: seen.append(i)
        print(name, len(html), len(seen))
        with open(f'_candidates/q_{name}.txt','w') as f: f.write('\n'.join(seen))
        print('  ', ' '.join(seen[:12]))
    except Exception as e:
        print(name, 'ERR', e)
