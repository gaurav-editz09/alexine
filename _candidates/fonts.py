import urllib.request, re, os
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
css_url = 'https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Manrope:wght@200..800&display=swap'
req = urllib.request.Request(css_url, headers={'User-Agent':ua})
css = urllib.request.urlopen(req, timeout=40).read().decode()
open('_candidates/fonts.css','w').write(css)
# capture latin blocks
blocks = re.findall(r'/\* ([a-z0-9-]+) \*/\s*@font-face\s*\{([^}]+)\}', css)
for subset, body in blocks:
    if subset != 'latin': continue
    fam = re.search(r"font-family:\s*'([^']+)'", body).group(1)
    style = re.search(r"font-style:\s*(\w+)", body).group(1)
    weight = re.search(r"font-weight:\s*([\d ]+)", body).group(1).strip().replace(' ','-')
    url = re.search(r'url\((https://[^)]+)\)', body).group(1)
    fn = f"assets/fonts/{fam.replace(' ','')}-{weight}-{style}.woff2"
    r = urllib.request.Request(url, headers={'User-Agent':ua})
    open(fn,'wb').write(urllib.request.urlopen(r, timeout=40).read())
    print(fn, os.path.getsize(fn))
