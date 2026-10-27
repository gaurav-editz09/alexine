import json
import os
from playwright.sync_api import sync_playwright
from PIL import Image

BASE = "http://127.0.0.1:8000/"
OUT = os.path.join(os.path.dirname(__file__), "shots")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1).new_page()
    page.goto(BASE, wait_until="networkidle")
    page.wait_for_timeout(1000)
    # reveal everything
    page.evaluate("document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-visible'))")
    page.wait_for_timeout(700)

    boxes = page.evaluate("""() => {
        const out = {};
        const ids = ['story','dishes','menu','gallery','experience','contact'];
        ids.forEach(id => { const r = document.getElementById(id).getBoundingClientRect(); out[id] = {x:0, y:r.top + scrollY, w:innerWidth, h:r.height}; });
        const f = document.querySelector('.site-footer').getBoundingClientRect();
        out.footer = {x:0, y:f.top + scrollY, w:innerWidth, h:f.height};
        return out;
    }""")
    page.add_style_tag(content=".demo-bar, .site-header, .scroll-progress, .grain { visibility: hidden !important; }")
    page.wait_for_timeout(200)
    full = os.path.join(OUT, "full-nohdr.png")
    page.screenshot(path=full, full_page=True)

    img = Image.open(full)
    print("full", img.size)
    for name, b in boxes.items():
        top = max(0, int(b["y"]))
        bottom = min(img.height, int(b["y"] + b["h"]))
        crop = img.crop((0, top, img.width, bottom))
        crop.save(os.path.join(OUT, f"crop-{name}.png"))
        print(name, crop.size)
    browser.close()
