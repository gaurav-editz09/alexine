import os, json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000/"
OUT = os.path.join(os.path.dirname(__file__), "shots3")
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = ctx.new_page()
    errs = []
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    page.goto(BASE, wait_until="networkidle")
    page.wait_for_timeout(1200)
    h = page.evaluate("document.body.scrollHeight")
    for y in range(0, h, 700):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(70)
    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(800)

    for sec in ["dishes", "gallery"]:
        el = page.query_selector("#" + sec)
        el.scroll_into_view_if_needed()
        page.wait_for_timeout(800)
        el.screenshot(path=os.path.join(OUT, f"{sec}.png"))

    menu = page.query_selector("#menu")
    menu.scroll_into_view_if_needed()
    page.wait_for_timeout(700)
    for tab in ["fire", "desserts"]:
        page.click(f"#tab-{tab}")
        page.wait_for_timeout(600)
        menu.screenshot(path=os.path.join(OUT, f"menu-{tab}.png"))

    print(json.dumps({"errors": errs, "gallery_count": page.eval_on_selector_all("[data-gallery]", "els => els.length"), "lightbox": page.inner_text(".lightbox__count")}, ensure_ascii=False))
    browser.close()
