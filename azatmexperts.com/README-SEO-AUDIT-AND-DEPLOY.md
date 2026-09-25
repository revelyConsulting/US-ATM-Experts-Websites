# Arizona ATM Experts — Redesign, SEO Audit & Deployment Guide

Prepared September 10, 2026 for www.azatmexperts.com.

## 1. What was wrong with the old site (audit findings)

The existing site is a three-page Bootstrap build (Home, Equipment, Contact) plus eight product pages and a privacy page. It looks dated, and more importantly it gives Google very little to rank. The specific problems found:

| Issue | Impact | Fixed in new build |
|---|---|---|
| Nine `<h1>` tags on the homepage (every carousel slide and section header was an H1) | Google can't tell what the page is about | One H1 per page, keyword-led |
| Meta description was a copy of the title | Poor click-through from search results | Unique 120–160 char descriptions on every page |
| No canonical tags | Duplicate-content risk between www/non-www and http/https | Canonical on every page + `.htaccess` 301 to https://www |
| No structured data | No rich results, no local-business signals | LocalBusiness, Service, FAQPage, Product, BreadcrumbList, ItemList JSON-LD |
| ~25 customer logos with empty `alt` | Accessibility + image SEO | Logo gallery removed at your request; all remaining images have descriptive alt text |
| No dedicated service pages — placement and processing buried on the homepage | Site cannot rank for "free ATM placement Phoenix" separately; competitors (Fort Yuma ATM, Prineta) each have 1,200–2,500-word pages per service | Three service pages + home, 400–950 words each |
| `/events.html` is indexed by Google but returns 404 | Wasted authority, bad user experience | 301-redirected to `atm-placement.html` in `.htaccess` (event ATMs are no longer offered) |
| No sitemap.xml or robots.txt | Slower/incomplete indexing | Both included |
| Weak page titles ("Arizona ATM Experts \| ATM Sales & Rentals") | No location or service keywords near the front | Rewritten, e.g. "Free ATM Placement in Phoenix & Arizona \| $0 Install & Cash Loading" |
| No city/region signals beyond "Arizona" | Misses Phoenix, Scottsdale, Tempe, Tucson, etc. searches | Service-area section and `areaServed` schema listing 20 cities |
| No Open Graph / Twitter cards | Ugly shares on Facebook/LinkedIn | Added on every page |

## 2. Keyword map (what each page targets)

| Page | Primary keyword | Secondary |
|---|---|---|
| `index.html` | Arizona ATM company | free ATM placement Arizona, ATM sales Phoenix, ATM company near me |
| `atm-placement.html` | free ATM placement Phoenix | ATM for my business, ATM placement program, ATM revenue share Arizona |
| `dispensaries.html` | dispensary ATM Arizona | cannabis ATM, compliant dispensary ATM, ATM for dispensary Phoenix |
| `locations/*.html` (16 pages) | free ATM placement [city] AZ | ATM company [city], ATM for my business [city] |
| `atm-processing.html` | ATM processing Arizona | free ATM processing, ATM daily deposits |
| `equipment.html` | buy ATM machine Arizona | Hyosung ATM for sale, Genmega ATM for sale, lease an ATM |
| `product_pages/*` | [brand + model] ATM for sale | model price, specs |

## 3. What's in the package

```
site/
  index.html               Home
  atm-placement.html       NEW – Free ATM placement (primary landing page)
  dispensaries.html        NEW – Dispensary ATMs (compliance-focused)
  locations/*.html         NEW – 16 city landing pages (Phoenix, Scottsdale, Tempe, Mesa, Chandler, Gilbert, Glendale, Peoria, Surprise, Goodyear, Queen Creek, Casa Grande, Tucson, Prescott, Sedona, Flagstaff)
  atm-processing.html      NEW – ATM processing
  equipment.html           Rebuilt – ATM sales & leasing
  product_pages/*.html     Rebuilt – 9 product pages (7 original file names + new gm_nova.html and idm_origin.html; inhand_i22_dual.html retired and 301-redirected)
  privacy.html             Rebuilt
  404.html                 NEW – custom not-found page
  css/styles.css           All styling (no Bootstrap dependency)
  js/main.js               Mobile menu + footer year (tiny)
  sitemap.xml, robots.txt  NEW
  .htaccess                https + www redirect, 301s for the old /events.html, /contact.html, and /product_pages/inhand_i22_dual.html, custom 404, caching (Apache only)
```

The new pages reference your **existing** image folder (`_assets/_images/...`) and PDF brochures (`_assets/_pdf/...`) by the same paths, so those don't need re-uploading. New asset files included in the zip that must be uploaded (all in `_assets/_images/`): `hero-storefronts.svg`, `hero-desert.svg`, `hero-processing.svg`, `hero-equipment.svg`, `hero-flag.svg`, `dispensary-hero.svg` (page hero backgrounds); `arizona-service-map.svg`, `placement-locations.svg`, `daily-vault-cash-deposits.svg`, `real-time-reporting.svg`, `dispensary-bank-statement.svg` (in-page illustrations); `_assets/_images/_atm_images/genmega-nova.jpg` (Nova product photo), and `_assets/_pdf/Genmega_Nova_Brochure.pdf` (Nova spec sheet). The IDM Origin router photo is loaded directly from IDM Wireless (https://idmwireless.com/wp-content/uploads/origin-1-510x382.jpg). If you'd rather self-host it, save that file as `_assets/_images/_atm_images/idm-origin-router.jpg` — the pages already fall back to that path automatically if IDM's copy ever disappears. All existing URLs are preserved. The one exception is the retired `/events.html`, which `.htaccess` redirects to the placement page; if your host isn't Apache, add that 301 in the host's dashboard.

## 3b. Processing page: portfolio section + floating quote form

The processing page now leads with a *Current ATM operators* section (aggressive interchange, no processing fees with daily deposits, painless conversion) and has a floating **Get a quote** button that opens a slide-in form (business name, name, address, number of terminals, monthly transactions). The form posts to Formspree: create a free form at https://formspree.io pointed at your inbox and replace `YOUR_FORM_ID` in `atm-processing.html`. Every "free processing" mention on that page carries an asterisk with the cannabis $0.05 processing-fee footnote.

## 4. How to deploy (plain HTML host: cPanel, GoDaddy, FTP, etc.)

1. **Back up** the current site (download the whole web root).
2. Upload everything inside `site/` to your web root (usually `public_html/`), overwriting the old `index.html`, `equipment.html`, `privacy.html`, and `product_pages/`. Delete the old `contact.html` (it is 301-redirected to the homepage in `.htaccess`). Do **not** delete `_assets/`.
3. Delete the old CSS/JS folders if you had any (`_assets/_css`, Bootstrap files, etc.) only after confirming the new pages render — they're no longer referenced.
4. If your host is not Apache (e.g. Netlify, Cloudflare Pages), delete `.htaccess` and set up the https/www redirect and `404.html` in the host's dashboard instead.
5. Visit the site and click through every nav item on desktop and phone.

Contact note: the contact page and form were removed at your request in favor of a floating call-to-action button. Until that button is added, the phone number and email in the header and footer are the only contact paths.

## 5. Post-launch checklist (do these the same week)

1. **Google Search Console** — add the property if you haven't, submit `https://www.azatmexperts.com/sitemap.xml`, and request indexing for `atm-placement.html`, `dispensaries.html`, and `atm-processing.html`.
2. **Google Business Profile** — this is the single biggest local-ranking factor. Create/claim it, search the category list for "ATM" and pick the closest business-service match Google offers (avoid bank/financial-institution categories), add the phone, hours, service area (all Arizona cities you serve), photos of installed machines, and start collecting reviews from existing placement locations such as bars, hotels, and city facilities. Once you have a street address (or a service-area business with hidden address), add it to the `address` block in the LocalBusiness schema on `index.html` and the footer.
3. **Google Ads conversion** — the existing tag (AW-16638075010) is carried over. With no form page, track conversions on phone-number clicks (a `tel:` click event) or on the floating CTA once it's added.
4. **Google Analytics 4** — if you have a GA4 property, paste its snippet below the Ads tag in `build.py`'s `head()` (or in each page's `<head>`).
5. **Rich results test** — run `https://search.google.com/test/rich-results` on the home, placement, and one product page to confirm the schema is picked up.
6. **PageSpeed** — run `https://pagespeed.web.dev/`. All hero backgrounds and section illustrations are now lightweight SVGs (2–7 KB each), so image weight is no longer a concern. The old `_slider_images` and stock JPGs are no longer referenced and can be deleted from the server once the new site is live.
7. **Links** — get the business listed on the Nautilus Hyosung and Genmega dealer locators, Arizona chambers of commerce, and the US ATM Experts site (a link from usatmexperts.com to the placement page helps).

## 6. Content ideas for the next 90 days

Each of these becomes a new page that can rank on its own and links to `atm-placement.html`:

- "Free ATM Placement in Scottsdale" / Tempe / Mesa / Tucson (city pages, ~600 words each, using the placement template)
- "How Much Does an ATM Make for a Bar?" (uses the earnings table)
- Case study: how a Whiskey Row bar increased cash sales with a placed ATM

## 7. Things I couldn't verify — please check

- **Pricing**: all prices were removed at your request; every product shows "Reach out for current pricing."
- **Business address & hours**: not on the old site, so schema uses only "Phoenix, AZ". Add the real address if you're comfortable publishing it.
- **Founding year**: footer and schema say 2012 per your instruction.
- **SMS consent language**: I kept your existing wording and added "Reply STOP to opt out," which carriers require. Have whoever handles your 10DLC registration confirm it matches.

## 8. Editing the site later

`build.py` (in this package) generates every page from one template, so nav, footer, and schema stay consistent. Edit text there and run `python3 build.py`. If you'd rather not use Python, the generated HTML files are plain and can be edited directly — just keep one `<h1>` per page and update `sitemap.xml` when adding pages.

## 8. SEO strategy — what's been done and what still needs you

### On-page (done in this build)
- **One target per page.** Home = "Arizona ATM company"; placement = "free ATM placement Phoenix/Arizona"; dispensaries = "dispensary ATM Arizona"; equipment = "ATM machines for sale Arizona"; each city page = "free ATM placement [city] AZ". Titles are ≤60 characters with the keyword first, and every H1 names the service and the geography.
- **16 city landing pages** under `/locations/` with unique local copy (districts, landmarks, municipal customers), city-specific FAQs, and Service + FAQ + Breadcrumb schema scoped to that city. These are what let you show up for "[city] ATM placement" searches, which the old site could never rank for.
- **Internal linking.** Every service-area chip and the new footer "Service areas" column link to the city pages; city pages link to each other, to placement, processing, equipment, and dispensaries; the home about section and placement page cross-link every service. Google follows these to understand the site's structure.
- **Content depth.** The placement page is now ~1,300 words (competitors run 1,200–2,500), with local-expertise and install-day sections; the dispensary page is ~950.
- **Structured data.** LocalBusiness (with areaServed for 32 cities, hours, brands, contact point, founding date), Service per page, FAQPage on every service and city page, Product on every machine, BreadcrumbList sitewide.
- **Technical.** One H1 per page, canonical tags, sitemap with 31 indexable URLs, robots.txt, 301s for retired URLs, lightweight SVG graphics, descriptive alt text on every image, mobile-clean layouts.

### Off-page (this is what decides #1 — none of it can be done from inside the website)
1. **Google Business Profile** is the single biggest factor for "ATM company near me" and map-pack results. Claim it, verify it, fill every field, add photos of real installs weekly for the first two months, and post updates monthly.
2. **Reviews.** Ask every happy location for a Google review with a direct link. Ten reviews with replies will outrank a competitor with zero. Never buy or fabricate reviews.
3. **Citations.** Get the exact same name/phone/website listed on Yelp, BBB, Bing Places, Apple Maps, Nextdoor, the Arizona Chamber, local chambers (Phoenix, Scottsdale, Tempe, Tucson), and the Genmega and Hyosung dealer locators.
4. **Backlinks.** A link from usatmexperts.com to the placement page; supplier/partner pages (IDM Wireless, Genmega dealer listings); local news or trade coverage of the dispensary compliance angle — that story is unusual and quotable.
5. **Search Console.** Submit the sitemap, request indexing on the placement, dispensary, and top city pages, and watch the "Performance" report monthly for queries you're ranking 5–15 for; those are the ones a little more content or a link will push to page one.

### Honest expectation
On-page work is now stronger than the competitors I reviewed (Fort Yuma ATM, Prineta, General ATMs). The site is positioned to compete for every Arizona ATM query. But "very top" is earned over months, mostly through the Google Business Profile, reviews, and links above. Expect movement within 4–8 weeks of launch and meaningful rankings in 3–6 months if the off-page list is worked consistently.
