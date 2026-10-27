import os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000/"
OUT = os.path.join(os.path.dirname(__file__), "shots")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1).new_page()
    page.goto(BASE, wait_until="networkidle")
    page.wait_for_timeout(800)

    for sel, name in [
        ("#story", "story"),
        ("#dishes", "dishes"),
        ("#menu", "menu"),
        ("#gallery", "gallery"),
        ("#experience", "experience"),
        ("#contact", "contact"),
        (".site-footer", "footer"),
    ]:
        page.locator(sel).scroll_into_view_if_needed()
        page.wait_for_timeout(700)
        page.locator(sel).screenshot(path=os.path.join(OUT, f"section-{name}.png"))

    # Reserve dialog
    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(300)
    page.locator(".hero [data-open-reserve]").click()
    page.wait_for_timeout(500)
    page.locator("#reserve-dialog").screenshot(path=os.path.join(OUT, "dialog-reserve.png"))
    page.locator("[data-close-reserve]").first.click()
    page.wait_for_timeout(300)

    # Menu tabs
    page.locator("#menu").scroll_into_view_if_needed()
    page.locator("#tab-fire").click()
    page.wait_for_timeout(700)
    page.locator("#menu").screenshot(path=os.path.join(OUT, "menu-fire-tab.png"))

    # Gallery lightbox
    page.locator("#gallery").scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    page.locator("[data-gallery]").nth(2).click()
    page.wait_for_timeout(700)
    page.screenshot(path=os.path.join(OUT, "lightbox.png"))
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(500)
    page.screenshot(path=os.path.join(OUT, "lightbox-next.png"))
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    # Mobile nav + reserve at 390
    mobile = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1).new_page()
    mobile.goto(BASE, wait_until="networkidle")
    mobile.wait_for_timeout(800)
    mobile.locator(".menu-toggle").click()
    mobile.wait_for_timeout(500)
    mobile.screenshot(path=os.path.join(OUT, "mobile-nav.png"))
    mobile.locator("#mobile-nav [data-open-reserve]").click()
    mobile.wait_for_timeout(500)
    mobile.screenshot(path=os.path.join(OUT, "mobile-reserve.png"))

    browser.close()
print("done")
