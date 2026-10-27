import json
import os
import sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000/"
OUT = os.path.join(os.path.dirname(__file__), "shots")
os.makedirs(OUT, exist_ok=True)

VIEWPORTS = [
    ("desktop", 1440, 900),
    ("laptop", 1280, 800),
    ("tablet", 1024, 768),
    ("tablet-sm", 768, 1024),
    ("mobile", 390, 844),
    ("mobile-sm", 360, 780),
]

report = {}

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, width, height in VIEWPORTS:
        context = browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=1,
            reduced_motion="no-preference",
        )
        page = context.new_page()
        console_errors = []
        page_errors = []
        failed = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: page_errors.append(str(err)))
        page.on("requestfailed", lambda req: failed.append(req.url + " :: " + (req.failure or "")))
        page.goto(BASE, wait_until="networkidle")
        page.wait_for_timeout(1200)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(900)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(600)

        metrics = page.evaluate("""() => {
            const doc = document.documentElement;
            const vw = innerWidth;
            const offenders = [];
            document.querySelectorAll('body *').forEach(el => {
                const r = el.getBoundingClientRect();
                if (r.width > 0 && (r.right > vw + 2 || r.left < -2)) {
                    const cs = getComputedStyle(el);
                    if (cs.position === 'fixed' || cs.position === 'absolute') return;
                    offenders.push({tag: el.tagName, cls: el.className && String(el.className).slice(0,80), left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width)});
                }
            });
            return {
                innerWidth: vw,
                innerHeight: innerHeight,
                scrollWidth: doc.scrollWidth,
                scrollHeight: doc.scrollHeight,
                overflowX: doc.scrollWidth > vw + 1,
                offenders: offenders.slice(0, 20),
                heroH: document.querySelector('.hero').offsetHeight,
                embers: document.getElementById('embers').className,
                canvas: [document.getElementById('embers').width, document.getElementById('embers').height],
                fonts: document.fonts.status,
            };
        }""")

        page.screenshot(path=os.path.join(OUT, f"{name}-viewport.png"), full_page=False)
        page.screenshot(path=os.path.join(OUT, f"{name}-full.png"), full_page=True)

        report[name] = {
            "metrics": metrics,
            "console_errors": console_errors,
            "page_errors": page_errors,
            "failed_requests": failed,
        }
        context.close()
    browser.close()

with open(os.path.join(OUT, "report.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print(json.dumps(report, indent=2))
