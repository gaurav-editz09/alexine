from PIL import Image, ImageDraw, ImageFont
import os, math
files = sorted(f for f in os.listdir('_candidates') if f.endswith('.jpg'))
font = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 34)
cols, rows, cell = 4, 3, 320
per = cols*rows
for s in range(math.ceil(len(files)/per)):
    batch = files[s*per:(s+1)*per]
    sheet = Image.new('RGB', (cols*cell, rows*cell), '#111')
    d = ImageDraw.Draw(sheet)
    for k, fn in enumerate(batch):
        im = Image.open('_candidates/'+fn).convert('RGB')
        im.thumbnail((cell, cell))
        x = (k%cols)*cell; y=(k//cols)*cell
        sheet.paste(im, (x + (cell-im.width)//2, y + (cell-im.height)//2))
        label = fn[:2]
        d.rectangle([x+6,y+6,x+58,y+48], fill='#000')
        d.text((x+12,y+8), label, font=font, fill='#fff')
    sheet.save(f'_candidates/sheet{s+1}.jpg', quality=82)
    print('sheet', s+1, len(batch))
