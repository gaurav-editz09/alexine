import re
import shutil

path = "index.html"
shutil.copyfile(path, "_qa/index.before-localise.html")
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

replacements = [
    ('<html lang="en-GB" class="no-js">', '<html lang="en-IN" class="no-js">'),
    ('Live-Fire Indian Dining in London', 'Live-Fire Indian Dining in Purnea, Bihar'),
    ('fictional contemporary Indian restaurant in Shoreditch, London.', 'fictional contemporary Indian restaurant in Purnea, Bihar.'),
    ('fictional live-fire Indian restaurant in Shoreditch, London.', 'fictional live-fire Indian restaurant in Purnea, Bihar.'),
    ('fictional live-fire Indian restaurant in Shoreditch, London, built', 'fictional live-fire Indian restaurant in Purnea, Bihar, built'),
    ('<meta property="og:locale" content="en_GB">', '<meta property="og:locale" content="en_IN">'),
    ('"priceRange": "£££",', '"priceRange": "₹₹₹",\n    "currenciesAccepted": "INR",'),
    ('"telephone": "+44-20-0000-0000",', '"telephone": "+91-6454-000-000",'),
    ('"streetAddress": "14 Kestrel Lane",', '"streetAddress": "14 Kestrel Lane, off Station Road",'),
    ('"addressLocality": "London",', '"addressLocality": "Purnea",'),
    ('"addressRegion": "Shoreditch",', '"addressRegion": "Bihar",'),
    ('"postalCode": "E2 7DP",', '"postalCode": "854301",'),
    ('"addressCountry": "GB"', '"addressCountry": "IN"'),
    ('"opens": "17:30", "closes": "00:00"', '"opens": "17:30", "closes": "23:30"'),
    ('"opens": "12:00", "closes": "20:00"', '"opens": "12:00", "closes": "22:30"'),
    ('London · Est. 2019', 'Purnea · Est. 2019'),
    ('Shoreditch, London <span class="eyebrow__sep"', 'Purnea, Bihar <span class="eyebrow__sep"'),
    ('<span>Shoreditch</span>', '<span>Purnea</span>'),
    ('cook over English oak and Binchotan', 'cook over mango wood and Binchotan'),
    ('Opened in Shoreditch', 'Opened in Purnea'),
    ('English oak, black cardamom, burnt onion jus', 'Mango wood, black cardamom, burnt onion jus'),
    ('Whole spices, sourced along the Malabar coast', 'Whole spices, Malabar coast'),
    ('Prices in GBP · Demo menu', 'Prices in INR · Demo menu'),
    ('A discretionary 12.5% service charge is added.', 'A discretionary 10% service charge is added. Taxes as applicable.'),
    ('Tucked off a Shoreditch side street', 'Tucked off Station Road'),
    ('<address>14 Kestrel Lane<br>Shoreditch<br>London E2 7DP</address>', '<address>14 Kestrel Lane<br>off Station Road<br>Purnea, Bihar 854301</address>'),
    ('<div><dt>Fri–Sat</dt><dd>17:30–00:00</dd></div>', '<div><dt>Fri–Sat</dt><dd>17:30–23:30</dd></div>'),
    ('<div><dt>Sunday</dt><dd>12:00–20:00</dd></div>', '<div><dt>Sunday</dt><dd>12:00–22:30</dd></div>'),
    ('<p>14 Kestrel Lane<br>Shoreditch, London</p>', '<p>14 Kestrel Lane<br>Purnea, Bihar 854301</p>'),
    ('<p>14 Kestrel Lane, Shoreditch<br>Tue–Sun · from 17:30</p>', '<p>14 Kestrel Lane, Purnea<br>Tue–Sun · from 17:30</p>'),
    ('https://www.google.com/maps/search/?api=1&amp;query=Shoreditch+London', 'https://www.google.com/maps/search/?api=1&amp;query=Station+Road+Purnea+Bihar+854301'),
    ('https://wa.me/447000000000', 'https://wa.me/919000000000'),
    ('href="tel:+442000000000"', 'href="tel:+916454000000"'),
    ('+44 (0)20 0000 0000', '+91 6454 000 000'),
    ('SevenRooms, OpenTable or a simple email enquiry', 'SevenRooms, OpenTable, Dineout or a simple email enquiry'),
]

for old, new in replacements:
    count = html.count(old)
    if count == 0:
        print(f"WARN not found: {old[:80]}")
    html = html.replace(old, new)
    print(f"{count:2d}x {old[:70]}")

# Item-name-aware price replacement.
prices = {
    "12-Hour Short Rib": "₹1,150",
    "Ember Butter Chicken": "₹795",
    "Malabar Prawn Linguine": "₹895",
    "Tandoori Mixed Grill": "₹1,250",
    "Dum Biryani": "₹795",
    "Burnt Honey Sundae": "₹445",
    "Dahi Puri": "₹295",
    "Lamb Samosa": "₹345",
    "Beef Carpaccio": "₹495",
    "Smoked Duck Dumplings": "₹475",
    "Charred Oysters": "₹595",
    "Charcoal Ribeye": "₹1,450",
    "Burnt Orange Pork Belly": "₹995",
    "Charred Squash": "₹425",
    "Smoked Aubergine": "₹395",
    "House Naan": "₹175",
    "Kachumber": "₹245",
    "Saffron Rice": "₹225",
    "Cucumber Raita": "₹175",
    "Saffron &amp; Pistachio Kulfi": "₹345",
    "Dark Chocolate &amp; Chilli Tart": "₹375",
    "Mango &amp; Cardamom Pavlova": "₹345",
    "Cheese &amp; Chutney": "₹495",
    "Smoked Old Fashioned": "₹550",
    "Kokum Negroni": "₹495",
    "Rose &amp; Cardamom Spritz": "₹445",
    "Masala Chai": "₹195",
    "Salted Lime Soda": "₹175",
    "Sommelier’s Pairing": "₹1,750",
}

lines = html.splitlines(keepends=True)
counts = {name: 0 for name in prices}
for i, line in enumerate(lines):
    if "£" not in line:
        continue
    for name, price in prices.items():
        if name in line:
            new_line, n = re.subn(r"£\d[\d,]*", price, line, count=1)
            if n:
                lines[i] = new_line
                counts[name] += 1
                break

html = "".join(lines)

for name, count in counts.items():
    if count == 0:
        print(f"WARN no price replaced for {name}")
print("price replacements:", counts)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

remaining = {
    "£": html.count("£"),
    "GBP": html.count("GBP"),
    "London": html.count("London"),
    "Shoreditch": html.count("Shoreditch"),
    "en-GB": html.count("en-GB"),
    "en_GB": html.count("en_GB"),
    "+44": html.count("+44"),
    "447000000000": html.count("447000000000"),
    "E2 7DP": html.count("E2 7DP"),
}
print("remaining:", remaining)
