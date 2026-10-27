from PIL import Image, ImageDraw, ImageFont
import os, math
files = sorted(f for f in os.listdir('_final') if f.endswith('.jpg'))
font = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 22)
cols, rows, cw, ch = 4, 4, 360, 300
per = cols*rows
for s in range(math.ceil(len(files)/per)):
    batch = files[s*per:(s+1)*per]
    sheet = Image.new('RGB', (cols*cw, rows*ch), '#111')
    d = ImageDraw.Draw(sheet)
    for k, fn in enumerate(batch):
        im = Image.open('_final/'+fn).convert('RGB')
        im.thumbnail((cw-10, ch-36))
        x = (k%cols)*cw; y=(k//cols)*ch
        sheet.paste(im, (x + (cw-im.width)//2, y+4))
        d.rectangle([x,y+ch-30,x+cw,y+ch], fill='#000')
        d.text((x+8,y+ch-27), fn[:-4], font=font, fill='#fff')
    sheet.save(f'_final/final{s+1}.jpg', quality=85)
    print('final', s+1, len(batch))
