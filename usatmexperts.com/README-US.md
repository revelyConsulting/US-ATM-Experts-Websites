# US ATM Experts — www.usatmexperts.com

Generated September 15, 2026. The national hub of the ATM Experts network, built on the same generator, design, and SEO structure as the Arizona rebuild and the 49 state sites.

## What's different from a state site

- **Brand & scope**: "US ATM Experts", national ATM company, "Serving all 50 states". No city pages; instead a **State directory** (`states.html`) with a card for every state linking to that state's site (home, free placement, buy an ATM, and dispensaries where legal). Every service page ends with a 50-state chip grid linking to the state sites.
- **Partners page** (`partners.html`, in the nav): the vaulting partner program for established independent ATM operators — how it works, four steps, tools partners get, partner requirements, FAQ. US ATM Experts signs and holds the location agreement; the partner provides the machine, the vault cash, and repairs (parts available at a discounted rate). Compensation is described as a monthly surcharge share with "reach out for current partner rates" (no numbers). A partner promo band also appears on the home page.
- **Colors**: US flag — navy `#002868`, red `#bf0a30`, white — applied to CSS and every SVG graphic.
- **Logo**: your `us-puck-logo.png`, shipped in `_assets/_images/_state_logo/`.
- **Event / mobile ATM content** from the old site is dropped, as on the state sites.
- **Schema**: LocalBusiness with `areaServed: United States` (no parentOrganization — this *is* the parent), Service, FAQPage, Product, BreadcrumbList, and an ItemList of all 50 state sites on the directory page.
- **Contact**: 833.843.3331 · info@usatmexperts.com (the old partners page listed an azatmexperts.com email; that's gone).

## Files

```
index.html               Home
atm-placement.html       Free ATM placement (national)
dispensaries.html        Dispensary ATMs (national)
atm-processing.html      ATM processing
equipment.html           ATM sales
partners.html            NEW — Vaulting partner program
states.html              NEW — State directory (all 50 state sites)
product_pages/*.html     9 product pages
privacy.html, 404.html
css/styles.css, js/main.js, sitemap.xml, robots.txt, .htaccess
_assets/_images/*.svg    Graphics in US colors; _atm_images/ product photos; _state_logo/us-puck-logo.png
```

`.htaccess` 301-redirects the old `/contact.html` to the home page. All images are served from this domain. Same two exceptions as the state sites: the Hyosung MX 2800T photo and the PDF spec sheets still load from azatmexperts.com.

## Apply Now floating button (partners page only) — one thing to set up

A red "Apply now" button floats at the bottom-right of `partners.html` and opens a slide-in application panel (the hero and closing-banner buttons open the same panel; Esc, the × button, or clicking outside closes it). The form posts to Formspree. Create a free form at https://formspree.io (send-to address: info@usatmexperts.com), copy its form ID, and replace `YOUR_FORM_ID` in `partners.html` (one occurrence: `action="https://formspree.io/f/YOUR_FORM_ID"`), or in `make_build_us.py` and rebuild. Until that's done, submitting the form shows a Formspree error page. Fields sent: business_name, contact_name, address, phone, email, service_zip, service_radius (5 / 15 / 25 / 50 / 100 / 150+ miles, or The entire state). A hidden honeypot field (`_gotcha`) blocks most spam bots, and Formspree can add a redirect to a thank-you page from its dashboard if you want one.

## Deploy

Upload everything in this folder to the web root of www.usatmexperts.com, replacing the old `index.html`, `equipment.html`, `partners.html`, and `contact.html`. If the host isn't Apache, delete `.htaccess` and set up the https + www redirect and custom 404 in the host dashboard.

## After launch

1. Google Search Console: add the property, submit `sitemap.xml`, request indexing for the home, placement, and partners pages.
2. Google Business Profile for US ATM Experts with the 833 number.
3. This site is the hub the 50 state sites all link to; the state directory page returns the favor. Once the state sites are live, that reciprocal linking is what tells Google the network is one legitimate organization.

## Please verify

- Partner program details were written from your answers (existing operators only; US ATM Experts holds the location agreement; the partner provides the machine, the vault cash, and repairs, with parts at a discounted rate; surcharge share paid monthly by the 10th; not a franchise) plus reasonable requirements (insurance, background check, 24-hour response, smartphone). Adjust anything that doesn't match how you actually run the program.
- "Equipment discounts" and "competitive interchange" for partners were carried over from your current partners page.
- Hours in the schema are Mon–Fri 8:00–17:00.

## Editing later

`python3 build_us.py` regenerates the site (it derives from `build_state.py`; the copy changes live in `make_build_us.py`).
