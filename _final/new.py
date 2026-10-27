from PIL import Image, ImageDraw, ImageFont
import os
files=['hi_porkbelly.jpg','hi_samosa.jpg','hi_biryani.jpg','hi_naan.jpg','hi_dining_dark.jpg']
font=ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf',22)
cw,ch=420,400
sheet=Image.new('RGB',(cw*3,ch*2),'#111'); d=ImageDraw.Draw(sheet)
for k,fn in enumerate(files):
    im=Image.open('_final/'+fn).convert('RGB'); im.thumbnail((cw-8,ch-34))
    x=(k%3)*cw; y=(k//3)*ch
    sheet.paste(im,(x+(cw-im.width)//2,y+2))
    d.rectangle([x,y+ch-30,x+cw,y+ch],fill='#000'); d.text((x+6,y+ch-27),fn[3:-4],font=font,fill='#fff')
sheet.save('_final/new.jpg',quality=85)
