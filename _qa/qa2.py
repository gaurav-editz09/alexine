import json, os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000/"
OUT = os.path.join(os.path.dirname(__file__), "shots2")
os.makedirs(OUT, exist_ok=True)
report = {}

with sync_playwright() as p:
    browser = p.chromium.launch()

    # ---------- desktop pass ----------
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = ctx.new_page()
    errors, pageerrors, failed = [], [], []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: pageerrors.append(str(e)))
    page.on("requestfailed", lambda r: failed.append(r.url + " :: " + (r.failure or "")))
    page.goto(BASE, wait_until="networkidle")
    page.wait_for_timeout(1500)

    # broken images
    broken = page.evaluate("""() => [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.currentSrc || i.src)""")

    # scroll through whole page to trigger lazy load / reveals
    h = page.evaluate("document.body.scrollHeight")
    for y in range(0, h, 600):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(80)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(900)
    broken2 = page.evaluate("""() => [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.currentSrc || i.src)""")

    # sections
    for sec in ["story", "dishes", "gallery", "experience", "contact"]:
        el = page.query_selector("#" + sec)
        if el:
            el.scroll_into_view_if_needed()
            page.wait_for_timeout(700)
            el.screenshot(path=os.path.join(OUT, f"desk-{sec}.png"))

    # menu tabs
    menu = page.query_selector("#menu")
    menu.scroll_into_view_if_needed()
    page.wait_for_timeout(800)
    for tab in ["starters", "fire", "garden", "desserts", "cellar"]:
        page.click(f"#tab-{tab}")
        page.wait_for_timeout(650)
        menu.screenshot(path=os.path.join(OUT, f"menu-{tab}.png"))

    # reserve dialog
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(400)
    page.click(".hero [data-open-reserve]")
    page.wait_for_timeout(500)
    page.screenshot(path=os.path.join(OUT, "reserve-dialog.png"))
    dlg_open = page.evaluate("document.getElementById('reserve-dialog').open")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    # lightbox
    gal = page.query_selector("#gallery")
    gal.scroll_into_view_if_needed()
    page.wait_for_timeout(600)
    page.click("[data-gallery]")
    page.wait_for_timeout(600)
    page.screenshot(path=os.path.join(OUT, "lightbox.png"))
    lb_open = page.evaluate("document.getElementById('lightbox').open")
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(300)
    lb_caption = page.inner_text("#lightbox-caption")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    # tab keyboard test
    page.focus("#tab-starters")
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(250)
    focused = page.evaluate("document.activeElement.id")
    selected = page.evaluate("document.querySelector('[role=tab][aria-selected=true]').id")

    report["desktop"] = {
        "console_errors": errors,
        "page_errors": pageerrors,
        "failed_requests": failed,
        "broken_images": sorted(set(broken + broken2)),
        "reserve_open": dlg_open,
        "lightbox_open": lb_open,
        "lightbox_caption_after_arrow": lb_caption,
        "tab_arrow_focus": focused,
        "tab_arrow_selected": selected,
        "scrollWidth": page.evaluate("document.documentElement.scrollWidth"),
    }
    print(json.dumps(report["desktop"], indent=2, ensure_ascii=False), flush=True)
    ctx.close()

    # ---------- mobile pass ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
    page = ctx.new_page()
    merrors = []
    page.on("console", lambda m: merrors.append(m.text) if m.type == "error" else None)
    page.goto(BASE, wait_until="networkidle")
    page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(OUT, "mobile-hero.png"))
    # open nav
    page.click(".menu-toggle")
    page.wait_for_timeout(500)
    page.screenshot(path=os.path.join(OUT, "mobile-nav.png"))
    nav_open = page.evaluate("document.getElementById('mobile-nav').open")
    page.click("[data-close-nav]")
    page.wait_for_timeout(400)
    # menu on mobile
    page.query_selector("#menu").scroll_into_view_if_needed()
    page.wait_for_timeout(700)
    page.screenshot(path=os.path.join(OUT, "mobile-menu.png"))
    page.click("#tab-desserts")
    page.wait_for_timeout(500)
    page.screenshot(path=os.path.join(OUT, "mobile-desserts.png"))
    report["mobile"] = {
        "console_errors": merrors,
        "nav_open": nav_open,
        "scrollWidth": page.evaluate("document.documentElement.scrollWidth"),
        "innerWidth": page.evaluate("innerWidth"),
    }
    ctx.close()
    browser.close()

print(json.dumps(report, indent=2, ensure_ascii=False))
