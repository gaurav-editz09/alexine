from PIL import Image, ImageEnhance, ImageFilter
import os, random

SRC = '_final'
OUT = 'assets/img'
os.makedirs(OUT, exist_ok=True)

def crop_to(im, ratio, fx=0.5, fy=0.5):
    w, h = im.size
    target = ratio
    if w / h > target:
        nw = int(h * target)
        x = int((w - nw) * fx)
        box = (x, 0, x + nw, h)
    else:
        nh = int(w / target)
        y = int((h - nh) * fy)
        box = (0, y, w, y + nh)
    return im.crop(box)

def save(im, name, widths, quality=78, grade=None):
    for w in widths:
        h = round(w * im.height / im.width)
        r = im.resize((w, h), Image.LANCZOS)
        if grade:
            r = grade(r)
        p = f'{OUT}/{name}-{w}.webp'
        r.save(p, 'WEBP', quality=quality, method=6)
        print(p, round(os.path.getsize(p)/1024), 'KB', r.size)

def grade_warm_dark(im):
    im = ImageEnhance.Brightness(im).enhance(0.94)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im = ImageEnhance.Color(im).enhance(1.03)
    return im

def grade_deep(im):
    im = ImageEnhance.Brightness(im).enhance(0.96)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    return im

def load(n): return Image.open(f'{SRC}/hi_{n}.jpg').convert('RGB')

# HERO
steak = load('steak')
desk = crop_to(steak, 16/10, 0.5, 0.5)
save(desk, 'hero', [1200, 1800], 76)
mob = crop_to(steak, 4/5, 0.5, 0.55)
save(mob, 'hero-mobile', [700, 1000], 76)
og = crop_to(steak, 1200/630, 0.5, 0.5).resize((1200,630), Image.LANCZOS)
og = grade_deep(og)
og.save(f'{OUT}/og.jpg', 'JPEG', quality=86)
print('og.jpg', round(os.path.getsize(f'{OUT}/og.jpg')/1024), 'KB')

# SIGNATURES 4:5
sigs = {
 'dish-shortrib': ('shortrib', 0.5, 0.5, grade_deep),
 'dish-butterchicken': ('butterchicken', 0.5, 0.5, grade_warm_dark),
 'dish-prawn': ('prawn', 0.5, 0.5, grade_deep),
 'dish-grill': ('grill', 0.5, 0.5, grade_deep),
 'dish-biryani': ('biryani', 0.5, 0.45, grade_warm_dark),
 'dish-dessert': ('dessert', 0.5, 0.55, None),
}
for name,(src,fx,fy,grade) in sigs.items():
    save(crop_to(load(src), 4/5, fx, fy), name, [600, 900], 78, grade)

# STORY
save(crop_to(load('chef'), 4/5, 0.5, 0.5), 'story-chef', [600, 900], 78, grade_warm_dark)
save(crop_to(load('spices'), 3/4, 0.5, 0.6), 'story-spices', [500, 800], 78, grade_warm_dark)

# MENU 4:5
menu = {
 'menu-starters': ('dumpling', 0.5, 0.55, grade_deep),
 'menu-fire': ('ribs', 0.5, 0.5, grade_deep),
 'menu-garden': ('squash', 0.5, 0.5, grade_warm_dark),
 'menu-desserts': ('dessert', 0.5, 0.55, None),
 'menu-cellar': ('cocktail', 0.5, 0.5, grade_deep),
}
for name,(src,fx,fy,grade) in menu.items():
    save(crop_to(load(src), 4/5, fx, fy), name, [500, 800], 78, grade)

# GALLERY
gal = {
 'gallery-room': ('dining_moody', 3/2, 0.5, 0.5, grade_deep),
 'gallery-bar': ('bar', 4/5, 0.5, 0.5, grade_warm_dark),
 'gallery-spice': ('spices', 3/2, 0.5, 0.55, grade_warm_dark),
 'gallery-cocktail': ('cocktail', 4/5, 0.5, 0.5, grade_deep),
 'gallery-warm': ('dining_warm', 3/2, 0.5, 0.5, grade_warm_dark),
 'gallery-woman': ('woman', 4/5, 0.58, 0.5, grade_warm_dark),
 'gallery-grill': ('grill', 1, 0.5, 0.5, grade_deep),
 'gallery-chef': ('chef', 4/5, 0.5, 0.5, grade_warm_dark),
}
for name,(src,ratio,fx,fy,grade) in gal.items():
    widths = [700, 1000] if ratio <= 1 else [800, 1200]
    save(crop_to(load(src), ratio, fx, fy), name, widths, 76, grade)

# EXPERIENCE 16:9
save(crop_to(load('dining_dark'), 16/9, 0.5, 0.5), 'experience', [1200, 1800], 74, grade_deep)
# CONTACT 4:5
save(crop_to(load('dining_warm'), 4/5, 0.5, 0.5), 'contact', [600, 900], 78, grade_warm_dark)

# NOISE
random.seed(7)
n = Image.new('L', (180,180))
px = n.load()
for y in range(180):
    for x in range(180):
        px[x,y] = random.randint(95,160)
n = n.convert('RGBA')
a = n.split()[0].point(lambda v: 22)
n.putalpha(a)
n.save(f'{OUT}/noise.png')
print('noise.png', round(os.path.getsize(f'{OUT}/noise.png')/1024), 'KB')
