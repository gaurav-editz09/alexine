import os
parts = [f'_parts/{i:02d}.html' for i in range(1,6)]
out = ''.join(open(p, encoding='utf-8').read() for p in parts)
open('index.html','w',encoding='utf-8',newline='\n').write(out)
print('index.html', len(out), 'chars')
