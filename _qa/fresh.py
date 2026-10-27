import os, json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000/"
OUT = os.path.join(os.path.dirname(__file__), "shots")
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = ctx.new_page()
    errs = []
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    page.goto(BASE, wait_until="networkidle")
    page.wait_for_timeout(1800)
    page.screenshot(path=os.path.join(OUT, "fresh-hero.png"))
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1200)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(800)
    page.screenshot(path=os.path.join(OUT, "fresh-full.png"), full_page=True)
    # menu section
    el = page.query_selector("#menu")
    if el:
        el.scroll_into_view_if_needed()
        page.wait_for_timeout(900)
        el.screenshot(path=os.path.join(OUT, "fresh-menu.png"))
    print(json.dumps({"errors": errs, "title": page.title()}, ensure_ascii=False))
    browser.close()
