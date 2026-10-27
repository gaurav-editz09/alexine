from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import os, math

SRC = '_bihari'
OUT = 'assets/img'
os.makedirs(OUT, exist_ok=True)

def crop_to(im, ratio, fx=0.5, fy=0.5):
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio)
        x = int((w - nw) * fx)
        box = (x, 0, x + nw, h)
    else:
        nh = int(w / ratio)
        y = int((h - nh) * fy)
        box = (0, y, w, y + nh)
    return im.crop(box)

def vignette(im, strength=0.55, power=1.7):
    w, h = im.size
    # small mask, then upscale for speed
    mw, mh = 320, max(1, round(320 * h / w))
    mask = Image.new('L', (mw, mh), 0)
    px = mask.load()
    cx, cy = (mw - 1) / 2, (mh - 1) / 2
    maxd = math.hypot(cx, cy)
    for y in range(mh):
        for x in range(mw):
            d = math.hypot(x - cx, y - cy) / maxd
            v = min(1.0, max(0.0, (d ** power)))
            px[x, y] = int(255 * v * strength)
    mask = mask.resize((w, h), Image.BICUBIC)
    dark = Image.new('RGB', (w, h), (8, 6, 5))
    return Image.composite(dark, im, mask)

def warm(im, amount=0.10):
    overlay = Image.new('RGB', im.size, (72, 34, 16))
    return Image.blend(im, overlay, amount)

def grain(im, amount=5):
    import random
    random.seed(11)
    w, h = im.size
    n = Image.new('L', (w // 2, h // 2))
    px = n.load()
    for y in range(n.height):
        for x in range(n.width):
            px[x, y] = 128 + random.randint(-amount, amount)
    n = n.resize((w, h), Image.BILINEAR).convert('RGB')
    return Image.blend(im, n, 0.045)

def grade(im, dark=0.86, contrast=1.12, color=0.94, vig=0.55):
    im = ImageEnhance.Brightness(im).enhance(dark)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Color(im).enhance(color)
    im = warm(im, 0.07)
    im = vignette(im, vig)
    im = grain(im, 6)
    return im

def save(im, name, widths, quality=80, g=None):
    for w in widths:
        h = round(w * im.height / im.width)
        r = im.resize((w, h), Image.LANCZOS)
        if g:
            r = g(r)
        p = f'{OUT}/{name}-{w}.webp'
        r.save(p, 'WEBP', quality=quality, method=6)
        print(p, round(os.path.getsize(p) / 1024), 'KB', r.size, flush=True)

def load(n):
    return Image.open(f'{SRC}/{n}.jpg').convert('RGB')

# ---------- HERO: rohu in terracotta ----------
hero = load('test_rohu')
desk = crop_to(hero, 16 / 10, 0.5, 0.48)
save(desk, 'hero', [1200, 1800], 78, lambda r: grade(r, dark=0.84, contrast=1.12))
mob = crop_to(hero, 4 / 5, 0.5, 0.48)
save(mob, 'hero-mobile', [700, 1000], 78, lambda r: grade(r, dark=0.84, contrast=1.12))

og = crop_to(hero, 1200 / 630, 0.5, 0.48).resize((1200, 630), Image.LANCZOS)
og = grade(og, dark=0.82, contrast=1.14, vig=0.6)
og.save(f'{OUT}/og.jpg', 'JPEG', quality=88, optimize=True, progressive=True)
print('og.jpg', round(os.path.getsize(f'{OUT}/og.jpg') / 1024), 'KB', flush=True)

# ---------- SIGNATURES (4:5) ----------
save(crop_to(load('litti2').crop((900, 500, 3700, 2900)), 4 / 5, 0.5, 0.5), 'dish-litti', [600, 900], 80,
     lambda r: grade(r, dark=0.84, contrast=1.18))
save(crop_to(load('mutton4'), 4 / 5, 0.5, 0.45), 'dish-champaran', [600, 900], 80,
     lambda r: grade(r, dark=0.86))
save(crop_to(load('rohu'), 4 / 5, 0.5, 0.5), 'dish-fish', [600, 900], 80,
     lambda r: grade(r, dark=0.84))
save(crop_to(load('malpua_l').crop((400, 150, 1000, 750)), 4 / 5, 0.5, 0.5), 'dish-malpua', [600, 900], 80,
     lambda r: grade(r, dark=0.86, contrast=1.18, vig=0.62))

# ---------- MENU (4:5) ----------
save(crop_to(load('sattu_thumb').crop((420, 210, 940, 730)), 4 / 5, 0.5, 0.5), 'menu-starters', [500, 800], 80,
     lambda r: grade(r, dark=0.88, contrast=1.14, vig=0.58))
save(crop_to(load('champaran'), 4 / 5, 0.5, 0.5), 'menu-fire', [500, 800], 80,
     lambda r: grade(r, dark=0.78, contrast=1.16, vig=0.7))

save(crop_to(load('malpua_l').crop((400, 150, 1000, 750)), 4 / 5, 0.42, 0.5), 'menu-desserts', [500, 800], 80,
     lambda r: grade(r, dark=0.84, contrast=1.16, vig=0.6))

