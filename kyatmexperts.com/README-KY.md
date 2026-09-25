# Kentucky ATM Experts — www.kyatmexperts.com

Generated September 17, 2026 as part of the US ATM Experts 49-state rollout. Same structure, copy, SEO work, and design as the Arizona rebuild (www.azatmexperts.com), localized for Kentucky.

## What's localized for Kentucky

- **Brand**: "Kentucky ATM Experts", positioned as *part of US ATM Experts* (no local-office or founding-year claim).
- **Contact**: 833.843.3331 · info@usatmexperts.com on every page, header, footer, and in the LocalBusiness schema.
- **Colors**: the Kentucky state-flag palette — primary `#002868`, accent `#b8862b`, highlight `#ffd700` — applied to the CSS and every SVG graphic.
- **Logo**: your existing Kentucky flag puck, shipped in this folder at `_assets/_images/_state_logo/ky-puck-logo.png` (header, footer, favicon, Open Graph image, and schema).
- **City pages** (10): Louisville, Lexington, Bowling Green, Owensboro, Covington, Frankfort, Elizabethtown, Richmond, Paducah, Pikeville. Each has unique local copy, neighborhoods/districts, nearby-city links, city-specific FAQs, and Service + FAQ + Breadcrumb schema.
- **Service-area map**: `_assets/_images/service-map.svg` (generic map with pins for the first eight cities).
- `dispensaries.html` — Dispensary ATMs (100% compliant, real name/address on customers' bank statements, largest cannabis ATM company in the country, 14 years, 99%+ uptime, cash-load prediction)
- **Processing page**: leads with a *Current ATM operators* section (bring your portfolio over: aggressive interchange rates with no numbers stated, no processing fees with daily deposits, painless conversion) plus a floating **Get a quote** button that opens a slide-in form (business name, name, address, number of terminals, monthly transactions). The form posts to Formspree — create a free form at https://formspree.io and replace `YOUR_FORM_ID` in `atm-processing.html` (submissions arrive with the subject "Portfolio processing inquiry (Kentucky ATM Experts)", so one Formspree form can serve every state). Also: every "free processing" mention carries an asterisk with the footnote "Due to additional required compliance, cannabis transactions are subject to a $0.05 processing fee."

## Files

```
index.html               Home
atm-placement.html       Free ATM placement (primary landing page)
dispensaries.html        Dispensary ATMs
atm-processing.html      ATM processing
equipment.html           ATM sales
product_pages/*.html     9 product pages (Genmega G2500, Onyx, Onyx-W, Nova; Hyosung Halo II, MX2800SE, MX2800T; InHand I-22 modem; IDM Origin router)
locations/*.html         10 city landing pages
privacy.html, 404.html
css/styles.css, js/main.js
sitemap.xml, robots.txt, .htaccess
_assets/_images/*.svg    Hero backgrounds and illustrations, recolored for Kentucky
_assets/_images/_atm_images/*.jpg   Product photos (G2500, Onyx, Onyx-W, Nova, Halo II, MX 2800SE, I-22, Origin), shipped in this folder
_assets/_images/_state_logo/ky-puck-logo.png   State flag puck logo
```

**Every image is served from this site's own domain** — nothing loads from azatmexperts.com or any other site. Two exceptions remain: the Hyosung MX 2800T product photo (no copy was in your Images folder, so it still loads from `https://www.azatmexperts.com/_assets/_images/_atm_images/nautilus-hyosung-mx2800T.jpg` — send me that photo and I'll ship it locally too), and the PDF spec-sheet links, which point at the brochures on the Arizona server to keep each state folder small (the new Nova brochure is in the package's `_shared-upload-to-azatmexperts.com/` folder and needs uploading there once).

## Deploy (plain HTML host)

1. Upload everything in this folder to the web root of www.kyatmexperts.com (usually `public_html/`).
2. If the host isn't Apache, delete `.htaccess` and set up the https + www redirect and the custom `404.html` in the host dashboard.
3. Click through every nav item on desktop and phone. The floating call-to-action button you're adding is the only contact path besides the phone number and email in the header/footer.

## After launch (same week)

1. **Google Search Console** — add `https://www.kyatmexperts.com`, submit `sitemap.xml`, request indexing for `index.html`, `atm-placement.html`, `dispensaries.html`, and the top three city pages.
2. **Google Business Profile** — the biggest local-ranking factor. A service-area profile for Kentucky with the 833 number, hours, and photos of installs. Reviews from placed locations matter more than anything on the page.
3. **Citations** — same name / phone / URL on Yelp, BBB, Bing Places, Apple Maps, the Genmega and Hyosung dealer locators, and the Kentucky chamber of commerce.
4. **Backlinks** — link this site from usatmexperts.com and from the other state sites' footers if you want a network signal.
5. **Rich results test** on the home, placement, and one product page (https://search.google.com/test/rich-results).

## Please verify before publishing

- The **hours** in the LocalBusiness schema are Mon–Fri 8:00–17:00 (carried from Arizona). Adjust in `build_state.py` if the 833 line runs different hours.
- Nationwide claims used verbatim from the Arizona site: "largest cannabis ATM company in the country" and "14 years placing ATMs in dispensaries" (cannabis states only), "Genmega & Hyosung authorized dealer", "free processing on every machine", "2-year manufacturer's warranty", "free shipping and handling (within the lower 48 states)", modem pricing ($129 I-22, $99 Origin, +$4.95/mo airtime). All other prices say "Reach out for current pricing."
- City copy was written from general knowledge of each city; a local read-through for street/district names is worthwhile.
- The "Trusted by Kentucky hospitality & retail businesses" trust bar line assumes you already have (or will have) customers in the state.

## Editing later

`build_state.py` + `states/KY.json` (city data) + `states/palettes.json` (colors) generate every page: `python3 build_all.py KY`. The generated HTML is plain and can also be edited directly — keep one `<h1>` per page and update `sitemap.xml` when adding pages.
