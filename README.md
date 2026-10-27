# Ember &amp; Spice — restaurant website concept

A premium, single-page restaurant website for a **fictional** modern Bihari live-fire restaurant in Purnea, Bihar. Built as a presentation piece for restaurant owners: dark editorial art direction, real photography, restrained motion, a genuine Three.js ember field and a working set of front-end interactions. The menu is built around litti chokha, sattu, mustard oil and Champaran mutton — no beef.

> **Demo content.** Ember &amp; Spice is not a real restaurant. The address, phone number, email, WhatsApp number, opening hours, chef, menu and prices are placeholders. The reservation button opens an explanatory panel and does **not** create a booking. The page is marked `noindex, nofollow`; remove that meta tag before any real launch.

## Run it locally

The site is plain HTML, CSS and JavaScript — no build step, no package manager, no dependencies to install.

From this folder:

```powershell
python -m http.server 8000
```

Then open **http://localhost:8000**.

You can use any static server instead, for example:

```powershell
npx serve .
```

> Use a local server rather than double-clicking `index.html`. The hero ember effect is an ES module and the browser will block module imports from `file://`. The rest of the site still works without JavaScript.

To preview on a phone, run the server on your computer and open `http://<your-computer-ip>:8000` from a device on the same network.

## Publish on GitHub Pages

The repository includes a GitHub Actions workflow at `.github/workflows/pages.yml`. After pushing the site to a GitHub repository:

1. Open **Settings → Pages** in the repository and set **Build and deployment → Source** to **GitHub Actions**.
2. Push to the `main` or `master` branch, or run **Deploy static website to GitHub Pages** from the **Actions** tab.
3. When the workflow succeeds, GitHub shows the live address under **Settings → Pages**. Project sites are usually available at `https://<username>.github.io/<repository>/`.

The workflow publishes only `index.html`, `favicon.svg` and `assets/`; the working folders and source notes are not included in the live site. The page remains labelled as a fictional concept demo and is marked `noindex`.

## What is included

- **Hero** — split-screen food photography (rohu in terracotta), editorial type, a genuine Three.js ember particle field, pointer parallax and a scroll cue.
- **Our Story** — layered image composition, Purnea sattu mills and litti copy, founder signature and restaurant statistics.
- **Six Signature Dishes** — litti chokha, Champaran mutton, Bihari fish curry, mutton kebab, mutton pulao and malpua in an asymmetric editorial grid with hover states and rupee pricing.
- **Menu** — cream "printed menu" interlude with five accessible tab panels (Bihari starters, fire, garden, desserts and coolers), dietary keys, INR pricing and changing category imagery.
- **Gallery** — eight-image mosaic with a keyboard-navigable lightbox (arrow keys, Escape, focus restoration).
- **Experience** — full-bleed parallax dining-room image with a three-part evening sequence.
- **Contact** — hours, placeholder Purnea contact details, map link, reservation notice and demo disclosure.
- **Footer** — navigation, hours, social links and demo credits.
- **Reservation dialog** — native `<dialog>` that explicitly says nothing has been booked or sent, with call/WhatsApp placeholders.
- **Mobile navigation** — full-screen native dialog with focus management and scroll lock.

## Structure

```
.
├─ index.html                     # all markup, metadata and JSON-LD
├─ favicon.svg
├─ assets/
│  ├─ css/style.css               # design system + responsive layout
│  ├─ js/
│  │  ├─ main.js                  # navigation, reveals, tabs, dialogs, lightbox, 3D tilt
│  │  ├─ embers.js                # lazy Three.js hero + global ember fields
│  │  └─ vendor/three.module.min.js
│  ├─ fonts/                      # self-hosted Instrument Serif + Manrope
│  └─ img/                        # responsive WebP derivatives + OG image
├─ _parts/                        # source chunks used to assemble the page
├─ _final/                        # original photography and processing scripts
└─ _candidates*/                  # image-selection contact sheets (disposable)
```

The `_parts`, `_final` and `_candidates` folders are working files, not part of the deployed site. Only `index.html`, `favicon.svg` and `assets/` need to be uploaded.

## Design and technical notes

- **Type:** Instrument Serif for display and Manrope for interface/body copy, self-hosted as `woff2` with `font-display: swap`. Rupee amounts use the Manrope stack so the `₹` glyph renders consistently on every platform.
- **Colour:** charcoal `#0B0A09`, warm cream `#F3EADB`, copper `#C98A56`, with a cream menu interlude for contrast.
- **Motion:** CSS transitions plus `IntersectionObserver` reveals; all non-essential motion is disabled under `prefers-reduced-motion: reduce`.
- **3D:** Three.js r0.169 is vendored locally and imported dynamically. A fixed WebGL ember field sits behind the dark sections with a scroll-driven camera and pointer parallax; the hero adds its own denser field. Image cards use CSS 3D tilt and depth entrances. The scene runs only on screens at least 900px wide with a fine pointer and no reduced-motion preference, pauses when the cream menu covers the viewport or the tab is hidden, caps device pixel ratio at 1.75 and fails silently if WebGL is unavailable.
- **No fake 3D food:** no licensed photorealistic 3D dish model was available, so the hero uses real photography with depth and motion rather than pretending a photograph is a 3D render. The 3D layer is atmospheric — embers, depth and parallax — never a simulated dish.
- **Localisation:** `lang="en-IN"`, Purnea/Bihar address, `+91` phone and WhatsApp placeholders, Indian rupee (`₹`) pricing and a 10% discretionary service charge.
- **Accessibility:** skip link, landmarks, visible focus styles, labelled dialogs, tablist keyboard controls, alt text, sufficient contrast and reduced-motion support.
- **Performance:** responsive `srcset`/`sizes` images, WebP, lazy loading below the fold, preloaded hero image and fonts, deferred JavaScript, locally hosted assets.

## Before a real launch

1. Replace every placeholder business detail: address, phone, email, WhatsApp, Instagram, opening hours, chef and menu.
2. Connect the reserve buttons to a real booking provider (SevenRooms, OpenTable, Dineout) or an email enquiry form with server-side validation.
3. Replace the demo reservation panel copy and remove the demo bar, chips and notes.
4. Remove `<meta name="robots" content="noindex, nofollow">` and update the canonical URL, Open Graph URL and JSON-LD to the live domain.
5. Replace the stock and Wikimedia Commons photography with the restaurant's own shoot. If any Commons image is kept, retain the author and licence attribution shown below (CC BY / CC BY-SA require it).
6. Run a fresh Lighthouse audit against the production host and test on real iOS/Android devices.

## Credits

- **Interior and atmosphere photography:** [Unsplash](https://unsplash.com) — used under the Unsplash License for this concept. Images are illustrative and do not depict the fictional restaurant.
- **Bihari dish photography:** [Wikimedia Commons](https://commons.wikimedia.org), resized, cropped and colour-graded for this demo:
  - Litti — *Litti Chokha-MB49* by Rajeeb Dutta, CC BY-SA 4.0.
  - Champaran mutton — *Mutton Curry (44786)* by Gaurav Dhwaj Khadka, CC BY-SA 3.0, and *Champaran meat* by YN Food Affair, CC BY 3.0.
  - Rohu curry — *Rohu fish curry* by Dolon Prova, CC BY-SA 4.0.
  - Malpua — *Malpua sweet in Kolkata, India* by Ravi Dwivedi, CC BY-SA 4.0.
  - Sattu paratha — *Sattu Ke Parathe* by Neha Sonal, CC BY-SA 4.0.
- **Typefaces:** [Instrument Serif](https://fonts.google.com/specimen/Instrument+Serif) and [Manrope](https://fonts.google.com/specimen/Manrope), both licensed under the SIL Open Font License.
- **3D:** [Three.js](https://threejs.org), MIT License, vendored locally.

## Known limitations

- No backend, booking engine, payments, analytics or form submission.
- Phone, WhatsApp, Instagram and Maps links are placeholders or generic destinations.
- The ember canvas requires WebGL and a desktop-class pointer; on mobile and reduced-motion settings it is intentionally disabled.
- The page is a design concept, not a production restaurant site.
