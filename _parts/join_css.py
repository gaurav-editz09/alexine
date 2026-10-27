import os
parts = [f'_parts/style{i}.css' for i in range(1,5)]
out = ''.join(open(p, encoding='utf-8').read() for p in parts)
open('assets/css/style.css','w',encoding='utf-8',newline='\n').write(out)
print('style.css', len(out), 'chars')
print('braces', out.count('{'), out.count('}'))
