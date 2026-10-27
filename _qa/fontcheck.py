import io, json, sys
from playwright.sync_api import sync_playwright

JS = r"""
() => {
  const price = document.querySelector('.dish__price');
  const mp = document.querySelector('.menu-item__price');
  const cs = price ? getComputedStyle(price) : null;
  const ms = mp ? getComputedStyle(mp) : null;
  const sample = document.createElement('canvas').getContext('2d');
  const measure = (font) => {
    sample.font = '40px ' + font;
    const a = sample.measureText('\u20b9').width;
    sample.font = '40px ' + font;
    const b = sample.measureText('\uFFFF').width;
    return { rupee: a, missing: b };
  };
  return {
    serifRupee: document.fonts.check('16px "Instrument Serif"', '\u20b9'),
    sansRupee: document.fonts.check('16px Manrope', '\u20b9'),
    serif: measure('"Instrument Serif"'),
    sans: measure('Manrope'),
    priceFont: cs && cs.fontFamily,
    menuPriceFont: ms && ms.fontFamily,
    priceText: price && price.textContent.trim(),
    menuPriceText: mp && mp.textContent.trim(),
    loaded: Array.from(document.fonts).map(f => f.family + ' ' + f.weight + ' ' + f.style + ' ' + f.status)
  };
}
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:8000/", wait_until="networkidle")
    page.wait_for_timeout(1500)
    result = page.evaluate(JS)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    browser.close()
