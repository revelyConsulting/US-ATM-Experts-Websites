#!/usr/bin/env python3
"""Static site generator for the redesigned azatmexperts.com.
Run:  python3 build.py   -> writes finished site into ./site/
"""
import os, json, html, datetime, sys, re, shutil, colorsys

CFG = json.load(open(sys.argv[1]))
PAL = CFG["palette"]
STATE = CFG["name"]; ABBR = CFG["abbr"]; DOMAIN = f"{ABBR.lower()}atmexperts.com"
METRO = CFG["metro_city"]; METRO_PHRASE = CFG["metro_phrase"]; SPAN = CFG["span_phrase"]; SEASONAL = CFG["seasonal_phrase"]
CANNABIS = CFG["cannabis"]
OUT = sys.argv[2]
BASE = f"https://www.{DOMAIN}"
PHONE_DISPLAY = "833.843.3331"
PHONE_TEL = "+18338433331"
EMAIL = "info@usatmexperts.com"
ASSETS = "https://www.azatmexperts.com/_assets"   # shared product photos, PDFs and logos live on the Arizona host
LOGO_FILE = f"{ABBR.lower()}-puck-logo.png"
LOGO_LOCAL = os.path.exists(os.path.join("site/_assets/_images/_state_logo", LOGO_FILE))
LOGO = (f"{BASE}" if LOGO_LOCAL else ASSETS) + f"/_images/_state_logo/{LOGO_FILE}"
TODAY = datetime.date.today().isoformat()
SRC_ASSETS = "site/_assets"   # anything present here is shipped inside the state folder and referenced locally; otherwise it's loaded from the Arizona host
def _have(sub, fname): return os.path.exists(os.path.join(SRC_ASSETS, sub, fname))
def img_url(fname, r): return f"{r}_assets/_images/_atm_images/{fname}" if _have("_images/_atm_images", fname) else f"{ASSETS}/_images/_atm_images/{fname}"
def img_abs(fname): return f"{BASE}/_assets/_images/_atm_images/{fname}" if _have("_images/_atm_images", fname) else f"{ASSETS}/_images/_atm_images/{fname}"
def img_fallback(fname, r): return ""
SHIP_PDFS = False   # brochures stay on the Arizona host for now (they are large); flip to True to ship them in every state folder
def pdf_url(fname, r): return f"{r}_assets/_pdf/{fname}" if SHIP_PDFS and _have("_pdf", fname) else f"{ASSETS}/_pdf/{fname}"
BRAND = f"{STATE} ATM Experts"

def _hex(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def _mix(h, t, white=True):
    r,g,b=_hex(h); tr,tg,tb=(255,255,255) if white else (0,0,0)
    return '#%02x%02x%02x'%(round(r+(tr-r)*t),round(g+(tg-g)*t),round(b+(tb-b)*t))
def _lum(h):
    r,g,b=_hex(h); return (0.2126*r+0.7152*g+0.0722*b)/255
P,A,H = PAL["primary"],PAL["accent"],PAL["highlight"]
COLOR_MAP = {"#0f1f4b":P,"#182d66":_mix(P,.10),"#1c2f66":_mix(P,.12),"#1f2d5c":_mix(P,.10),"#16265a":_mix(P,.06),"#2b3f7a":_mix(P,.22),
 "#3a4c85":_mix(P,.30),"#243466":_mix(P,.16),"#1b2a5b":_mix(P,.06),"#141a33":_mix(P,.25,False),"#0b1638":_mix(P,.30,False),"#2e4a8a":_mix(P,.28),"#1f3f7a":_mix(P,.2),
 "#d9552b":A,"#b8431d":_mix(A,.18,False),"#e8763a":_mix(A,.18),"#f2b134":H,"#b87333":_mix(H,.25,False)}
def recolor(text):
    for k,v in COLOR_MAP.items(): text=text.replace(k,v).replace(k.upper(),v)
    return text

# ------------------------------------------------------------------ CSS
CSS = r"""
:root{
  --navy:#0f1f4b; --navy-2:#182d66; --ink:#1b1f2a; --muted:#5b6172;
  --copper:#d9552b; --copper-2:#b8431d; --gold:#f2b134;
  --sand:#f7f4ee; --line:#e6e1d8; --white:#fff;
  --radius:14px; --shadow:0 10px 30px rgba(15,31,75,.10);
  --max:1180px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;font-family:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);background:var(--white);line-height:1.6;font-size:17px}
img{max-width:100%;height:auto;display:block}
a{color:var(--copper-2)}
h1,h2,h3,h4{font-family:"Manrope","Inter",system-ui,sans-serif;line-height:1.15;margin:0 0 .5em;color:var(--navy);letter-spacing:-.01em}
h1{font-size:clamp(2rem,4.2vw,3.25rem);font-weight:800}
h2{font-size:clamp(1.6rem,3vw,2.25rem);font-weight:800}
h3{font-size:1.25rem;font-weight:700}
p{margin:0 0 1em}
.wrap{max-width:var(--max);margin:0 auto;padding:0 20px}
.eyebrow{display:inline-block;font-size:.8rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--copper);margin-bottom:.75rem}
.lead{font-size:1.15rem;color:var(--muted)}
.btn{display:inline-block;padding:.85rem 1.5rem;border-radius:999px;font-weight:700;text-decoration:none;border:2px solid transparent;transition:.2s;line-height:1.2}
.btn-primary{background:var(--copper);color:#fff}
.btn-primary:hover{background:var(--copper-2)}
.btn-outline{border-color:var(--navy);color:var(--navy);background:transparent}
.btn-outline:hover{background:var(--navy);color:#fff}
.btn-light{background:#fff;color:var(--navy)}
.btn-light:hover{background:var(--sand)}
.btn-row{display:flex;gap:.75rem;flex-wrap:wrap;align-items:center}
.skip{position:absolute;left:-999px;top:0;background:var(--navy);color:#fff;padding:.5rem 1rem;z-index:99}
.skip:focus{left:8px;top:8px}

/* top bar + header */
.topbar{background:var(--navy);color:#fff;font-size:.9rem}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;gap:1rem;min-height:38px}
.topbar a{color:#fff;text-decoration:none;font-weight:600}
.topbar .social a{margin-left:.9rem;opacity:.85}
.topbar .social a:hover{opacity:1}
header.site{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
header.site .wrap{display:flex;align-items:center;justify-content:space-between;gap:1rem;min-height:84px}
.brand{display:flex;align-items:center;gap:.75rem;text-decoration:none;color:var(--navy)}
.brand img{width:58px;height:58px;border-radius:50%}
.brand strong{font-family:"Manrope",sans-serif;font-size:1.15rem;line-height:1.1;display:block}
.brand small{display:block;white-space:nowrap;color:var(--muted);font-size:.78rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase}
nav.main ul{list-style:none;margin:0;padding:0;display:flex;gap:.25rem;align-items:center}
nav.main a{display:block;white-space:nowrap;padding:.6rem .8rem;text-decoration:none;color:var(--ink);font-weight:600;border-radius:8px}
nav.main a:hover,nav.main a[aria-current=page]{background:var(--sand);color:var(--navy)}
nav.main .cta a{background:var(--copper);color:#fff;border-radius:999px;padding:.65rem 1.2rem;margin-left:.5rem}
nav.main .cta a:hover{background:var(--copper-2)}
.nav-toggle{display:none;background:none;border:2px solid var(--navy);border-radius:8px;padding:.4rem .6rem;font-weight:700;color:var(--navy);cursor:pointer}
@media(max-width:1400px){.brand small{display:none}}
@media(max-width:900px){
  .nav-toggle{display:block}
  nav.main{display:none;position:absolute;left:0;right:0;top:100%;background:#fff;border-bottom:1px solid var(--line);box-shadow:var(--shadow)}
  nav.main.open{display:block}
  nav.main ul{flex-direction:column;align-items:stretch;padding:.75rem 20px 1rem}
  nav.main .cta a{margin:.5rem 0 0;text-align:center}
  .topbar .social{display:none}
}

/* hero */
.hero{position:relative;color:#fff;background:var(--navy);overflow:hidden}
.hero .bg{position:absolute;inset:0;background-size:cover;background-position:center;opacity:.35}
.hero .wrap{position:relative;padding:clamp(3.5rem,9vw,7rem) 20px;max-width:var(--max)}
.hero h1{color:#fff;max-width:14ch}
.hero .lead{color:rgba(255,255,255,.85);max-width:52ch;font-size:1.2rem}
.hero .eyebrow{color:var(--gold)}
.hero-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:3rem;align-items:center}
.hero-card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:var(--radius);padding:1.5rem;backdrop-filter:blur(6px)}
.hero-card h3{color:#fff;margin-bottom:.75rem}
.hero-card ul{margin:0;padding:0;list-style:none}
.hero-card li{padding:.4rem 0 .4rem 1.8rem;position:relative;color:rgba(255,255,255,.92)}
.hero-card li::before{content:"";position:absolute;left:0;top:.75rem;width:1.1rem;height:1.1rem;border-radius:50%;background:var(--gold);mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z' fill='%23000'/%3E%3C/svg%3E") center/contain no-repeat;-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z' fill='%23000'/%3E%3C/svg%3E") center/contain no-repeat}
@media(max-width:900px){.hero-grid{grid-template-columns:1fr}}
.hero.sub .wrap{padding:clamp(3rem,7vw,5rem) 20px}
.crumbs{font-size:.85rem;margin-bottom:1rem;color:rgba(255,255,255,.75)}
.crumbs a{color:#fff;text-decoration:none}
.crumbs span{margin:0 .4rem}

/* trust strip */
.trust{background:var(--sand);border-bottom:1px solid var(--line)}
.trust .wrap{display:flex;flex-wrap:wrap;gap:1rem 2.5rem;justify-content:center;padding:1rem 20px;font-weight:600;color:var(--navy);font-size:.95rem}
.trust span::before{content:"✓";color:var(--copper);margin-right:.45rem;font-weight:800}

/* sections */
section{padding:clamp(3rem,7vw,5.5rem) 0}
section.alt{background:var(--sand)}
section.dark{background:var(--navy);color:#fff}
section.dark h2,section.dark h3{color:#fff}
section.dark .lead{color:rgba(255,255,255,.8)}
.section-head{max-width:70ch;margin-bottom:2.5rem}
.center{text-align:center;margin-left:auto;margin-right:auto}
.grid{display:grid;gap:1.5rem}
.grid-2{grid-template-columns:repeat(2,minmax(0,1fr))}
.grid-3{grid-template-columns:repeat(3,minmax(0,1fr))}
.grid-4{grid-template-columns:repeat(4,minmax(0,1fr))}
.grid-5{grid-template-columns:minmax(0,1.4fr) repeat(4,minmax(0,1fr))}
@media(max-width:900px){.grid-3,.grid-4,.grid-5{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.grid-2,.grid-3,.grid-4,.grid-5{grid-template-columns:1fr}}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:1.6rem;box-shadow:0 2px 0 rgba(15,31,75,.03);display:flex;flex-direction:column}
.card.link{transition:.2s;text-decoration:none;color:inherit}
.card.link:hover{transform:translateY(-3px);box-shadow:var(--shadow);border-color:#d8d2c6}
.card .icon{width:48px;height:48px;border-radius:12px;background:var(--sand);display:grid;place-items:center;margin-bottom:1rem;color:var(--copper)}
.card .icon svg{width:26px;height:26px}
.card h3{margin-bottom:.4rem}
.card p{color:var(--muted);margin-bottom:.75rem}
.card .more{margin-top:auto;font-weight:700;color:var(--copper-2);text-decoration:none}
.card.feature{border-top:4px solid var(--copper)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:center}
@media(max-width:900px){.split{grid-template-columns:1fr}}
.split img{border-radius:var(--radius);box-shadow:var(--shadow);width:100%;object-fit:cover;aspect-ratio:4/3}
.checks{list-style:none;padding:0;margin:0 0 1.5rem}
.checks li{padding:.45rem 0 .45rem 2rem;position:relative}
.checks li::before{content:"✓";position:absolute;left:0;top:.4rem;width:1.4rem;height:1.4rem;border-radius:50%;background:var(--copper);color:#fff;font-size:.8rem;font-weight:800;display:grid;place-items:center}
.checks strong{color:var(--navy)}
.steps{counter-reset:s;display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem}
@media(max-width:900px){.steps{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.steps{grid-template-columns:1fr}}
.step{counter-increment:s;background:#fff;border-radius:var(--radius);padding:1.5rem;border:1px solid var(--line)}
.step::before{content:counter(s,decimal-leading-zero);font-family:"Manrope",sans-serif;font-weight:800;font-size:2rem;color:var(--copper);display:block;line-height:1;margin-bottom:.75rem}
.step h3{font-size:1.1rem}
.step p{color:var(--muted);margin:0;font-size:.97rem}

/* earnings table */
.table-wrap{overflow-x:auto;border-radius:var(--radius);border:1px solid var(--line);background:#fff}
table{border-collapse:collapse;width:100%;min-width:560px;font-size:.98rem}
th,td{padding:.9rem 1rem;text-align:left;border-bottom:1px solid var(--line)}
th{background:var(--sand);color:var(--navy);font-family:"Manrope",sans-serif;font-size:.85rem;text-transform:uppercase;letter-spacing:.06em}
tbody tr:last-child td{border-bottom:0}
td strong{color:var(--navy)}
.note{font-size:.88rem;color:var(--muted)}
.stat{background:#fff;border-radius:var(--radius);padding:1.5rem;border:1px solid var(--line);text-align:center}
.stat b{display:block;font-family:"Manrope",sans-serif;font-size:2.2rem;color:var(--copper);line-height:1.1}
.stat span{color:var(--muted);font-size:.95rem}
section.dark .stat{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.15)}
section.dark .stat b{color:var(--gold)}
section.dark .stat span{color:rgba(255,255,255,.8)}

/* faq */
.faq details{background:#fff;border:1px solid var(--line);border-radius:12px;padding:0 1.25rem;margin-bottom:.75rem}
.faq summary{cursor:pointer;font-weight:700;color:var(--navy);padding:1rem 0;list-style:none;display:flex;justify-content:space-between;gap:1rem;font-family:"Manrope",sans-serif}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-size:1.4rem;color:var(--copper);line-height:1}
.faq details[open] summary::after{content:"–"}
.faq .a{padding:0 0 1.1rem;color:var(--muted)}
.faq .a p:last-child{margin-bottom:0}

/* logos */
.logos{display:grid;grid-template-columns:repeat(6,1fr);gap:1rem}
@media(max-width:900px){.logos{grid-template-columns:repeat(3,1fr)}}
@media(max-width:500px){.logos{grid-template-columns:repeat(2,1fr)}}
.logos div{background:#fff;border:1px solid var(--line);border-radius:12px;padding:1rem;display:grid;place-items:center;min-height:86px}
.logos img{max-height:46px;width:auto;filter:grayscale(1);opacity:.75;transition:.2s}
.logos div:hover img{filter:none;opacity:1}

/* areas */
.areas{display:flex;flex-wrap:wrap;gap:.5rem}
.areas span{background:#fff;border:1px solid var(--line);border-radius:999px;padding:.35rem .9rem;font-size:.92rem;font-weight:600;color:var(--navy)}

/* products */
.product{display:flex;flex-direction:column}
.product img{aspect-ratio:1;object-fit:contain;background:var(--sand);border-radius:12px;padding:.5rem;margin-bottom:1rem}
.product .price{font-family:"Manrope",sans-serif;font-weight:800;color:var(--navy);font-size:1.15rem}
.product .price small{display:block;font-weight:500;color:var(--muted);font-size:.8rem}
.spec{display:grid;grid-template-columns:1fr 1fr;gap:.5rem 1.5rem;margin:0}
.spec div{padding:.6rem 0;border-bottom:1px solid var(--line)}
.spec dt{font-weight:700;color:var(--navy);font-size:.85rem;text-transform:uppercase;letter-spacing:.05em}
.spec dd{margin:0;color:var(--muted)}
@media(max-width:600px){.spec{grid-template-columns:1fr}}

/* cta band */
.cta-band{background:linear-gradient(135deg,var(--copper) 0%,#e8763a 100%);color:#fff;text-align:center}
.cta-band h2{color:#fff}
.cta-band p{color:rgba(255,255,255,.92);max-width:60ch;margin:0 auto 1.5rem}
.cta-band .btn-light{color:var(--copper-2)}
.cta-band .btn-outline{border-color:#fff;color:#fff}
.cta-band .btn-outline:hover{background:#fff;color:var(--copper-2)}

/* forms */
form.quote{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
form.quote .full{grid-column:1/-1}
@media(max-width:600px){form.quote{grid-template-columns:1fr}}
label{display:block;font-weight:600;font-size:.9rem;margin-bottom:.35rem;color:var(--navy)}
input,select,textarea{width:100%;padding:.8rem .95rem;border:1px solid #cfc9be;border-radius:10px;font:inherit;background:#fff}
input:focus,select:focus,textarea:focus{outline:2px solid var(--copper);outline-offset:1px;border-color:var(--copper)}
textarea{min-height:130px;resize:vertical}
.consent{font-size:.82rem;color:var(--muted)}
.consent label{font-weight:500;display:flex;gap:.6rem;align-items:flex-start;color:var(--muted)}
.consent input{width:auto;margin-top:.3rem}
.contact-side .card{margin-bottom:1rem}
.contact-grid{grid-template-columns:1.4fr .8fr;align-items:start}
@media(max-width:900px){.contact-grid{grid-template-columns:1fr}}
.contact-side a{font-weight:700;text-decoration:none;color:var(--navy);font-size:1.15rem}

/* footer */
footer{background:#0b1638;color:rgba(255,255,255,.8);padding:3.5rem 0 2rem;font-size:.95rem}
footer .grid{gap:2.5rem}
footer h4{color:#fff;font-size:.9rem;text-transform:uppercase;letter-spacing:.1em;margin-bottom:1rem}
footer ul{list-style:none;padding:0;margin:0}
footer li{margin-bottom:.5rem}
footer a{color:rgba(255,255,255,.85);text-decoration:none}
footer a:hover{color:#fff;text-decoration:underline}
footer .brand{color:#fff;margin-bottom:1rem}
footer .brand small{color:rgba(255,255,255,.6)}
footer .network{border-top:1px solid rgba(255,255,255,.12);margin-top:2.5rem;padding-top:1.75rem}
footer .network p{font-size:.85rem;color:rgba(255,255,255,.6);margin-bottom:.75rem}
footer .network-links{display:flex;flex-wrap:wrap;gap:.35rem .9rem;font-size:.8rem}
footer .network-links a{color:rgba(255,255,255,.7)}
footer .network-links span{color:#fff;font-weight:700}
footer .bottom{border-top:1px solid rgba(255,255,255,.12);margin-top:2.5rem;padding-top:1.5rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:1rem;font-size:.85rem;color:rgba(255,255,255,.6)}
.prose{max-width:75ch}
.prose h2{margin-top:2rem}
.prose ul{padding-left:1.2rem}
"""

JS = r"""
document.addEventListener('DOMContentLoaded',function(){
  var t=document.querySelector('.nav-toggle'),n=document.querySelector('nav.main');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});}
  var y=document.getElementById('year');if(y){y.textContent=new Date().getFullYear();}
});
"""

# ------------------------------------------------------------------ icons
ICONS = {
 "place": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
 "event": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9h18M8 3v4M16 3v4"/><rect x="3" y="5" width="18" height="16" rx="2"/><path d="m9 15 2 2 4-4"/></svg>',
 "process": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m7 15 4-5 3 3 6-7"/></svg>',
 "sales": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="2" width="12" height="20" rx="2"/><rect x="9" y="5" width="6" height="4"/><path d="M9 13h6M9 16h6"/></svg>',
 "cash": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M6 12h.01M18 12h.01"/></svg>',
 "support": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14a8 8 0 0 1 16 0"/><rect x="2" y="13" width="5" height="7" rx="1.5"/><rect x="17" y="13" width="5" height="7" rx="1.5"/><path d="M19 20a4 4 0 0 1-4 2h-2"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></svg>',
 "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 3h15v13H1zM16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
 "wifi": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14.08 0M1.42 9a16 16 0 0 1 21.16 0M8.53 16.11a6 6 0 0 1 6.95 0"/><circle cx="12" cy="20" r="1"/></svg>',
 "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
}

SOCIAL = [
 ("Facebook","https://www.facebook.com/azatmexperts"),
 ("Instagram","https://www.instagram.com/azatmexperts/"),
 ("LinkedIn","https://www.linkedin.com/company/az-atm-expert/"),
 ("X / Twitter","https://twitter.com/azatmexperts"),
]

NAV = [
 ("ATM Placement","atm-placement.html"),
]+([("Dispensaries","dispensaries.html")] if CANNABIS else [])+[
 ("Processing","atm-processing.html"),
 ("Equipment","equipment.html"),
]

CUSTOMERS = [
 ("holiday-inn-express-logo.png","Holiday Inn Express"),
 ("arizona-cardinals-logo.png","Arizona Cardinals"),
 ("milwaukee-brewers-logo.png","Milwaukee Brewers"),
 ("san-diego-padres-logo.png","San Diego Padres"),
 ("tx-rangers-logo.png","Texas Rangers"),
 ("cactus-league-logo.png","Cactus League"),
 ("phoenix-rising-logo.png","Phoenix Rising FC"),
 ("findlay-toyota-center-logo.png","Findlay Toyota Center"),
 ("city-of-chandler-logo.png","City of Chandler"),
 ("city-of-surprise-logo.png","City of Surprise"),
 ("city-of-casa-grande-logo.png","City of Casa Grande"),
 ("town-of-queen-creek.png","Town of Queen Creek"),
 ("bottled-blonde-logo.png","Bottled Blonde"),
 ("buffalo-chip-logo.png","Buffalo Chip Saloon"),
 ("dame-of-the-west-logo.png","Dame of the West"),
 ("deirks-bentleys-logo.png","Dierks Bentley's Whiskey Row"),
 ("fifth-estate-tattoo-logo.png","Fifth Estate Tattoo"),
 ("lookout-tavern-logo.png","Lookout Tavern"),
 ("out-west-general-logo.png","Out West General"),
 ("sandbar-logo.png","Sandbar Mexican Grill"),
 ("sedona-arts-festival-logo.png","Sedona Arts Festival"),
 ("shave-fade-barber-logo.png","Shave & Fade Barber"),
 ("super8-logo.png","Super 8"),
 ("tavern-grill-logo.png","Tavern Grill"),
]

CITIES = CFG["cities"]
CITY_BY_SLUG = {c["slug"]:c for c in CITIES}
AREAS = [c["name"] for c in CITIES]
TOP = [c["name"] for c in CITIES[:3]]

# ------------------------------------------------------------------ helpers
def esc(s): return html.escape(s, quote=True)

def rel(depth): return "../"*depth

def head(p, depth=0):
    r = rel(depth)
    LOGO_R = f"{r}_assets/_images/_state_logo/{LOGO_FILE}" if LOGO_LOCAL else LOGO
    canonical = f"{BASE}/{p['path']}" if p['path']!="index.html" else f"{BASE}/"
    og_img = LOGO
    ld = json.dumps(p.get("ld", []), ensure_ascii=False, indent=1)
    nav_items = "".join('<li><a href="%s%s"%s>%s</a></li>' % (r, h, ' aria-current="page"' if p["path"]==h else "", t) for t,h in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(p['title'])}</title>
<meta name="description" content="{esc(p['desc'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(p['title'])}">
<meta property="og:description" content="{esc(p['desc'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f1f4b">
<link rel="icon" href="{LOGO_R}">
<link rel="apple-touch-icon" href="{LOGO_R}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}css/styles.css">
<script type="application/ld+json">{ld}</script>
<!-- Google Ads tag (carried over from the current site) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-16638075010"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','AW-16638075010');</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <div><a href="tel:{PHONE_TEL}">📞 {PHONE_DISPLAY}</a> &nbsp;·&nbsp; <a href="mailto:{EMAIL}">{EMAIL}</a></div>
  <div class="social">Serving all of {STATE}</div>
</div></div>
<header class="site"><div class="wrap">
  <a class="brand" href="{r}index.html"><img src="{LOGO_R}" alt="{BRAND} logo" width="58" height="58"><span><strong>{BRAND}</strong><small>ATM placement · processing · sales</small></span></a>
  <button class="nav-toggle" aria-expanded="false" aria-controls="mainnav">Menu</button>
  <nav class="main" id="mainnav" aria-label="Main"><ul>
    {nav_items}
  </ul></nav>
</div></header>
<main id="main">
"""

DISP_LI = lambda r: ('<li><a href="%sdispensaries.html">Dispensary ATMs</a></li>' % r) if CANNABIS else ""
DISP_LINK_HOME = ('a <a href="dispensaries.html">compliant dispensary ATM</a> in ' + (CFG["cities"][1]["name"] if len(CFG["cities"])>1 else CFG["metro_city"]) + ', ') if CANNABIS else ""
DISP_LINK_PL = '<a href="dispensaries.html">compliant dispensary ATMs</a>, ' if CANNABIS else ""
DISP_WORD = "dispensaries, " if CANNABIS else ""
DOMAIN_RE = DOMAIN.replace(".", "\\.")
TOP_LINKS = ", ".join('<a href="locations/%s.html">%s</a>' % (c["slug"],c["name"]) for c in CFG["cities"][:3])

def footer_cities(r):
    out=[]; cs=CITIES[:12]
    for i in range(0,len(cs),3):
        out.append("<li>"+" · ".join(f'<a href="{r}locations/{c["slug"]}.html">{c["name"]}</a>' for c in cs[i:i+3])+"</li>")
    return "\n   ".join(out)


STATE_NAMES = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"}
def network_block(current_abbr):
    links = "".join(
        (f'<span aria-current="true">{n}</span>' if ab == current_abbr else f'<a href="https://www.{ab.lower()}atmexperts.com/">{n}</a>')
        for ab, n in sorted(STATE_NAMES.items(), key=lambda x: x[1]))
    return f''' <div class="network">
  <h4>The US ATM Experts network</h4>
  <p>Free ATM placement, processing, and sales in every state. Visit <a href="https://www.usatmexperts.com/">US ATM Experts</a> or your state site:</p>
  <div class="network-links">{links}</div>
 </div>
'''

def foot(depth=0):
    LOGO_R = f"{rel(depth)}_assets/_images/_state_logo/{LOGO_FILE}" if LOGO_LOCAL else LOGO
    r = rel(depth)
    return f"""</main>
<footer><div class="wrap">
 <div class="grid grid-5">
  <div>
   <a class="brand" href="{r}index.html"><img src="{LOGO_R}" alt="" width="58" height="58" loading="lazy"><span><strong>{BRAND}</strong><small>Serving all of {STATE}</small></span></a>
   <p>{BRAND} is part of the US ATM Experts network, providing free ATM placement, ATM processing, and equipment sales for {STATE} businesses.</p>
  </div>
  <div><h4>Services</h4><ul>
   <li><a href="{r}atm-placement.html">Free ATM Placement</a></li>
   {DISP_LI(r)}
   <li><a href="{r}atm-processing.html">ATM Processing</a></li>
   <li><a href="{r}equipment.html">Buy an ATM</a></li>
  </ul></div>
  <div><h4>Equipment</h4><ul>
   <li><a href="{r}product_pages/gm_g2500.html">Genmega G2500</a></li>
   <li><a href="{r}product_pages/gm_onyx.html">Genmega Onyx</a></li>
   <li><a href="{r}product_pages/gm_onyx_w.html">Genmega Onyx-W</a></li>
   <li><a href="{r}product_pages/gm_nova.html">Genmega Nova</a></li>
   <li><a href="{r}product_pages/idm_origin.html">IDM Wireless Modems</a></li>
  </ul></div>
  <div><h4>Service areas</h4><ul>
   {footer_cities(r)}
  </ul></div>
  <div><h4>Contact</h4><ul>
   <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
   <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
   <li>Serving all of {STATE}</li>
  </ul></div>
 </div>
{network_block(ABBR)}
 <div class="bottom">
  <div>© <span id="year">2026</span> {BRAND}. All rights reserved. Part of <a href="https://www.usatmexperts.com" target="_blank" rel="noopener">US ATM Experts</a>.</div>
  <div><a href="{r}privacy.html">Privacy Policy</a> · <a href="{r}sitemap.xml">Sitemap</a></div>
 </div>
</div></footer>
<script src="{r}js/main.js" defer></script>
</body>
</html>
"""

def cta_band(depth=0, h="Ready to add an ATM to your business?", p="Call us or send a few details about your location. We'll tell you the same day whether it qualifies for free placement and what you can expect to earn."):
    r = rel(depth)
    return f"""<section class="cta-band"><div class="wrap">
  <h2>{h}</h2><p>{p}</p>
  <div class="btn-row" style="justify-content:center"><a class="btn btn-outline" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div>
</div></section>"""

def faq_block(items, title="Frequently asked questions", intro=None, depth=0):
    body = "".join(f'<details><summary>{esc(q)}</summary><div class="a">{a}</div></details>' for q,a in items)
    return f"""<section class="alt" id="faq"><div class="wrap"><div class="section-head"><span class="eyebrow">FAQ</span><h2>{title}</h2>{f'<p class="lead">{intro}</p>' if intro else ''}</div><div class="faq" style="max-width:820px">{body}</div></div></section>"""

def faq_ld(items):
    import re
    def strip(s): return re.sub("<[^>]+>","",s).strip()
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q,a in items]}

def logos_block(depth=0):
    r = rel(depth)
    tiles = "".join(f'<div><img src="{r}_assets/_images/_customer_logos/{f}" alt="{esc(n)} logo" loading="lazy" width="300" height="75"></div>' for f,n in CUSTOMERS)
    return f"""<section><div class="wrap"><div class="section-head center"><span class="eyebrow">Trusted across Arizona</span><h2>Who we work with</h2><p class="lead">From MLB spring training ballparks and city governments to neighborhood bars, hotels, and barbershops.</p></div><div class="logos">{tiles}</div></div></section>"""

CITY_SLUGS = {c["name"]:c["slug"] for c in CITIES}
def areas_block(depth=0, heading=None):
    heading = heading or f"Serving businesses across {STATE}"
    r = rel(depth)
    chips = "".join((f'<a href="{r}locations/{CITY_SLUGS[a]}.html" style="text-decoration:none"><span>{a}</span></a>' if a in CITY_SLUGS else f"<span>{a}</span>") for a in AREAS)
    return f"""<section class="alt"><div class="wrap"><div class="section-head"><span class="eyebrow">Service area</span><h2>{heading}</h2><p class="lead">We place, service, and cash-load ATMs across {STATE}, {SPAN}. If your business is in {STATE}, we can help.</p></div><div class="areas">{chips}</div></div></section>"""

def sub_hero(p, eyebrow, h1, lead, bg, depth=0, crumbs=None, extra=""):
    r = rel(depth)
    c = ""
    if crumbs:
        c = '<div class="crumbs"><a href="'+r+'index.html">Home</a>' + "".join('<span>/</span>' + ('<a href="%s%s">%s</a>' % (r,u,t) if u else t) for t,u in crumbs) + "</div>"
    bgurl = f"{r}_assets/_images/{bg}" if bg.endswith('.svg') else f"{r}_assets/_images/_slider_images/{bg}"
    op = ";opacity:.5" if bg.endswith('.svg') else ""
    return f"""<div class="hero sub"><div class="bg" style="background-image:url('{bgurl}'){op}"></div><div class="wrap">{c}<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lead">{lead}</p>{extra}</div></div>"""

ORG = {
 "@context":"https://schema.org","@type":"LocalBusiness","@id":BASE+"/#business","parentOrganization":{"@type":"Organization","name":"US ATM Experts","url":"https://www.usatmexperts.com/"},
 "name":BRAND,"alternateName":f"{ABBR} ATM Experts","url":BASE+"/",
 "logo":LOGO,
 "image":LOGO,
 "telephone":PHONE_TEL,"email":EMAIL,
 "description":f"Free ATM placement, ATM processing, and ATM sales for businesses across {STATE}. Part of the US ATM Experts network.",
 "address":{"@type":"PostalAddress","addressRegion":ABBR,"addressCountry":"US"},
 "areaServed":[{"@type":"State","name":STATE}]+[{"@type":"City","name":a} for a in AREAS],
 "parentOrganization":{"@type":"Organization","name":"US ATM Experts","url":"https://www.usatmexperts.com"},
 "slogan":f"Free ATM placement, processing, and sales across {STATE}",
 "knowsAbout":["ATM placement","ATM processing","ATM sales","Genmega ATMs","Nautilus Hyosung ATMs","dispensary ATMs","cannabis ATM compliance","wireless ATM routers"],
 "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"17:00"}],
 "contactPoint":{"@type":"ContactPoint","telephone":PHONE_TEL,"contactType":"sales","areaServed":f"US-{ABBR}","availableLanguage":"English"},
 "brand":[{"@type":"Brand","name":"Genmega"},{"@type":"Brand","name":"Nautilus Hyosung"},{"@type":"Brand","name":"IDM Wireless"}],
 "hasOfferCatalog":{"@type":"OfferCatalog","name":"ATM services","itemListElement":[
   {"@type":"Offer","itemOffered":{"@type":"Service","name":"Free ATM placement","url":BASE+"/atm-placement.html"}},
   ]+([{"@type":"Offer","itemOffered":{"@type":"Service","name":"Dispensary ATM placement","url":BASE+"/dispensaries.html"}}] if CANNABIS else [])+[
   {"@type":"Offer","itemOffered":{"@type":"Service","name":"ATM processing","url":BASE+"/atm-processing.html"}},
   {"@type":"Offer","itemOffered":{"@type":"Service","name":"ATM sales","url":BASE+"/equipment.html"}}]}
}

def service_ld(name, url, desc, stype="Service"):
    return {"@context":"https://schema.org","@type":stype,"name":name,"url":url,"description":desc,
            "provider":{"@id":BASE+"/#business"},"areaServed":{"@type":"State","name":STATE}}

def crumbs_ld(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":BASE+"/"+u} for i,(n,u) in enumerate(items)]}


# ---------------- floating quote panel (processing page) ----------------
FLOAT_CSS = r"""
<style>
.fab{position:fixed;right:20px;bottom:20px;z-index:60;display:inline-flex;align-items:center;gap:.6rem;background:var(--copper);color:#fff;font-weight:700;padding:.9rem 1.4rem;border-radius:999px;border:0;box-shadow:0 12px 30px rgba(0,0,0,.25);cursor:pointer;font:inherit;font-weight:700}
.fab:hover{background:var(--copper-2)}
.fab svg{width:20px;height:20px}
.apply-overlay{position:fixed;inset:0;background:rgba(15,31,75,.45);z-index:70;opacity:0;pointer-events:none;transition:.2s}
.apply-panel{position:fixed;top:0;right:0;height:100%;width:min(480px,100%);background:#fff;z-index:80;transform:translateX(100%);transition:.25s;overflow-y:auto;padding:1.5rem 1.5rem 2rem;box-shadow:-10px 0 40px rgba(0,0,0,.2)}
body.apply-open .apply-overlay{opacity:1;pointer-events:auto}
body.apply-open .apply-panel{transform:none}
body.apply-open{overflow:hidden}
.apply-panel form.quote{grid-template-columns:1fr 1fr}
.apply-panel form.quote>div{display:flex;flex-direction:column;justify-content:flex-end}
.apply-panel .close{position:absolute;top:.9rem;right:.9rem;background:var(--sand);border:0;width:38px;height:38px;border-radius:50%;font-size:1.3rem;cursor:pointer;color:var(--navy)}
@media(max-width:480px){.apply-panel form.quote{grid-template-columns:1fr}.fab span{display:none}.fab{padding:.9rem}}
</style>
"""
FLOAT_JS = r"""
<script>
(function(){var b=document.body,fab=document.getElementById('apply'),panel=document.getElementById('apply-panel');
function open(){b.classList.add('apply-open');fab.setAttribute('aria-expanded','true');panel.setAttribute('aria-hidden','false');setTimeout(function(){panel.querySelector('input:not([type=hidden])').focus()},250);}
function close(){b.classList.remove('apply-open');fab.setAttribute('aria-expanded','false');panel.setAttribute('aria-hidden','true');}
fab.addEventListener('click',open);
document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',close)});
document.querySelectorAll('a[href="#apply"]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();open();})});
document.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
if(location.hash==='#apply'){open();}
})();
</script>
"""
def float_panel(label, eyebrow, title, intro, subject, fields, submit, consent):
    FULL = ' class="full"'
    req_mark = ' <span style="color:#c0392b">*</span>'
    rows = "".join(f'<div{FULL if full else ""}><label for="{fid}">{lab}{req_mark if "required" in inp else ""}</label>{inp}</div>' for fid,lab,inp,full in fields)
    return FLOAT_CSS + f"""
<button class="fab" type="button" id="apply" aria-controls="apply-panel" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg><span>{label}</span></button>
<div class="apply-overlay" data-close></div>
<aside class="apply-panel" id="apply-panel" role="dialog" aria-modal="true" aria-labelledby="apply-title" aria-hidden="true">
 <button class="close" type="button" aria-label="Close" data-close>&times;</button>
 <span class="eyebrow">{eyebrow}</span>
 <h2 id="apply-title" style="margin-bottom:.4rem;font-size:1.6rem">{title}</h2>
 <p style="color:var(--muted);margin-bottom:1.25rem">{intro}</p>
 <form class="quote" action="https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8&orgId=00Dfn00000Io6pR" method="POST">
  <input type="hidden" name="oid" value="00Dfn00000Io6pR">
  <input type="hidden" name="retURL" value="https://usatmexperts.com/thankyou.html">
  <input type="hidden" name="lead_source" value="Web">
  <input type="hidden" name="url" value="{BASE}">
  {rows}
  <div class="full"><button class="btn btn-primary" type="submit" style="width:100%">{submit}</button></div>
  <p class="full" style="margin:0;font-size:.82rem;color:var(--muted)">{consent}</p>
 </form>
 <p style="margin:1.25rem 0 0;font-size:.9rem;color:var(--muted)">Prefer to talk? Call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</aside>
""" + FLOAT_JS

PORTFOLIO_FORM = float_panel("Get a quote","Move your portfolio","Tell us about your terminals","We'll come back with interchange and processing terms for your portfolio, usually within two business days.",f"Portfolio processing inquiry ({BRAND})",[
 ("pf-business","Business name",'<input id="pf-business" name="company" type="text" required autocomplete="organization">',True),
 ("pf-first","First name",'<input id="pf-first" name="first_name" type="text" required autocomplete="given-name">',False),
 ("pf-last","Last name",'<input id="pf-last" name="last_name" type="text" required autocomplete="family-name">',False),
 ("pf-email","Email",'<input id="pf-email" name="email" type="email" required autocomplete="email">',False),
 ("pf-phone","Phone",'<input id="pf-phone" name="phone" type="tel" required autocomplete="tel">',False),
 ("pf-street","Street address",'<input id="pf-street" name="street" type="text" required autocomplete="street-address">',True),
 ("pf-city","City",'<input id="pf-city" name="city" type="text" required autocomplete="address-level2">',False),
 ("pf-state","State",f'<select id="pf-state" name="state" required autocomplete="address-level1"><option value="{ABBR}" selected>{ABBR}</option></select>',False),
 ("pf-zip","ZIP",'<input id="pf-zip" name="zip" type="text" required autocomplete="postal-code" inputmode="numeric">',False),
 ("pf-terminals","Number of terminals",'<input id="pf-terminals" name="00NbV0000045QUD" type="number" min="1" step="1" required inputmode="numeric">',False),
 ("pf-tx","Monthly transactions",'<input id="pf-tx" name="00NbV0000045QcH" type="number" min="0" step="1" required inputmode="numeric" placeholder="Average">',False),
 ("pf-description","Anything else we should know?",'<textarea id="pf-description" name="description" placeholder="Current processor, contract end date, etc."></textarea>',True),
],"Request processing terms",f"By submitting, you agree to be contacted by {BRAND} about ATM processing. We don't share your information.")

PORTFOLIO = f"""
<section class="dark" id="portfolio"><div class="wrap">
 <div class="section-head"><span class="eyebrow">Current ATM operators</span><h2>Already running a portfolio? Bring it to us.</h2><p class="lead">If you operate your own ATMs and you're paying too much for processing, or waiting too long for your money, we'll move your terminals over and put more of every transaction in your pocket.</p></div>
 <div class="grid grid-3">
  <div class="card" style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.15);color:#fff"><h3>Aggressive interchange rates</h3><p style="color:rgba(255,255,255,.8)">Our volume as part of a national operator gets us interchange terms most independents never see, and we pass them through. The more terminals and transactions you bring, the better the rate. Reach out for a quote on your portfolio.</p></div>
  <div class="card" style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.15);color:#fff"><h3>No processing fees, daily deposits</h3><p style="color:rgba(255,255,255,.8)">No monthly processing or statement fees. Vault cash and surcharge are deposited daily as customers withdraw, settled through the Federal Reserve, so your cash isn't tied up in someone else's float.</p></div>
  <div class="card" style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.15);color:#fff"><h3>Painless conversion</h3><p style="color:rgba(255,255,255,.8)">We handle the terminal reprogramming and network paperwork, convert on your schedule so no machine goes dark, and give you real-time reporting on every terminal from day one. You keep 100% of your surcharge.</p></div>
 </div>
 <div class="btn-row" style="margin-top:2rem;justify-content:center"><a class="btn btn-light" href="#apply">Get a processing quote</a><a class="btn btn-outline" style="border-color:#fff;color:#fff" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div>
</div></section>
"""

PAGES = []

# ================================================================== HOME
HOME_FAQ = [
 ("How much does free ATM placement cost my business?", "<p>Nothing. With our free placement program we supply the machine, install it, load and manage the cash, and monitor it 24/7. All you need to provide is a standard power outlet.</p>"),
 ("How much can my location earn from an ATM?", "<p>It depends on foot traffic and the surcharge. A typical bar, restaurant, or convenience store doing 100–300 withdrawals a month earns roughly $50–$300 per month in surcharge share, or $1,800–$10,800 over a three-year agreement, based on our actual locations. See the <a href=\"atm-placement.html#earnings\">earnings estimates</a>.</p>"),
 ("Which brands of ATM do you sell?", "<p>We're an authorized dealer for Genmega (G2500, Onyx, Onyx-W, Nova) and Nautilus Hyosung (Halo II, MX 2800SE Force, MX 2800T), plus InHand wireless modems. Every machine we sell includes free processing and support.</p>"),
 (f"How do I find a reliable ATM company near me in {STATE}?", f"<p>Look for a company that owns its routes, loads its own cash, and answers the phone. {BRAND} is part of the US ATM Experts network, places and services ATMs across {STATE}, and is an authorized Genmega and Nautilus Hyosung dealer. Call {PHONE_DISPLAY} and you'll reach our team.</p>"),
 (f"What areas of {STATE} do you serve?", f"<p>All of it. We serve {METRO_PHRASE} and communities {SPAN}, including {', '.join(AREAS[:-1])}, and {AREAS[-1]}.</p>"),
]
home = {
 "path":"index.html",
 "title":f"{STATE} ATM Company | Free ATM Placement & Sales | {METRO}",
 "desc":f"{BRAND} offers free ATM placement, ATM processing, and Genmega & Hyosung ATM sales across {STATE}. Part of the US ATM Experts network. Call {PHONE_DISPLAY}.",
 "ld":[ORG, {"@context":"https://schema.org","@type":"WebSite","url":BASE+"/","name":BRAND,"publisher":{"@id":BASE+"/#business"}}, faq_ld(HOME_FAQ)],
}
home["body"] = f"""
<div class="hero"><div class="bg" style="background-image:url('_assets/_images/hero-storefronts.svg');opacity:.5"></div><div class="wrap"><div class="hero-grid">
 <div>
  <span class="eyebrow">Part of US ATM Experts · Serving all of {STATE}</span>
  <h1>{STATE}'s ATM company for free ATM placement and ATM sales</h1>
  <p class="lead">We install, stock, and monitor a top-of-the-line ATM at your business for $0 — and offer you revenue share options. Or, you buy your own machine and keep 100% of the surcharge revenue.</p>
  <div class="btn-row"><a class="btn btn-light" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div>
 </div>
 <div class="hero-card"><h3>The no-cost ATM program includes</h3><ul>
  <li>Free installation</li><li>We supply and load the cash</li><li>24/7/365 monitoring</li><li>Revenue share options</li></ul></div>
</div></div></div>
<div class="trust"><div class="wrap"><span>Serving all of {STATE}</span><span>Genmega & Hyosung authorized dealer</span><span>Trusted by {STATE} hospitality &amp; retail businesses</span><span>Free processing on every machine</span></div></div>

<section><div class="wrap">
 <div class="section-head"><span class="eyebrow">What we do</span><h2>ATM solutions for {STATE} businesses</h2><p class="lead">Whether you want a machine placed for free or want to own your own ATM and keep 100% of the surcharge, we handle every part of the operation.</p></div>
 <div class="grid grid-3">
  <a class="card link feature" href="atm-placement.html"><div class="icon">{ICONS['place']}</div><h3>Free ATM Placement</h3><p>A turnkey ATM at your dispensary, bar, restaurant, hotel, retail store, or venue at zero cost. We do everything and provide you with fair revenue share options.</p><span class="more">Learn about placement →</span></a>
  <a class="card link" href="atm-processing.html"><div class="icon">{ICONS['process']}</div><h3>ATM Processing</h3><p>Daily deposits and real-time online reporting, included free with every ATM we sell or process.</p><span class="more">Processing details →</span></a>
  <a class="card link" href="equipment.html"><div class="icon">{ICONS['sales']}</div><h3>ATM Sales</h3><p>Genmega and Nautilus Hyosung machines with free shipping, free processing, and 100% of the surcharge revenue.</p><span class="more">Browse equipment →</span></a>
 </div>
</div></section>

<section class="alt"><div class="wrap"><div class="split">
 <div>
  <span class="eyebrow">Why {BRAND}</span>
  <h2>Reliable machines, backed by second-to-none service</h2>
  <p>{BRAND} is trusted across {STATE} by business owners who need an ATM that simply works. We've placed machines in {DISP_WORD}restaurants, bars, hotels, tattoo shops, barbershops, and city facilities, and we back every one with best in class support.</p>
  <p>Whether you need <a href="atm-placement.html">free ATM placement</a> in {METRO}, {DISP_LINK_HOME}<a href="atm-processing.html">ATM processing</a> for a machine you already own, or a <a href="equipment.html">new Genmega or Hyosung ATM</a> for your business, one {STATE} team handles it.</p>
  <ul class="checks">
   <li><strong>Free processing</strong> and daily cash deposits</li>
   <li><strong>Support</strong> with dedicated account reps</li>
   <li><strong>Free shipping &amp; handling</strong> on every machine we sell</li>
   <li><strong>State-of-the-art ATMs</strong> from Genmega and Hyosung</li>
   <li><strong>Flexible revenue-sharing</strong> options to fit your location</li>
  </ul>
  
 </div>
 <img src="_assets/_images/service-map.svg" alt="{STATE} ATM service areas including {", ".join(AREAS[:6])}" width="1200" height="900" loading="lazy">
</div></div></section>

<section class="dark"><div class="wrap">
 <div class="section-head"><span class="eyebrow">Why an ATM pays off</span><h2>Cash still drives sales</h2><p class="lead">Industry data on North American ATM use, and what it means for your register.</p></div>
 <div class="grid grid-4">
  <div class="stat"><b>10B+</b><span>ATM transactions per year in North America</span></div>
  <div class="stat"><b>20–25%</b><span>more spent by a typical ATM user vs. a non-user</span></div>
  <div class="stat"><b>2–3%</b><span>saved on every cash sale vs. credit card processing fees</span></div>
  <div class="stat"><b>$0</b><span>to get started with free placement</span></div>
 </div>
</div></section>

<section><div class="wrap">
 <div class="section-head"><span class="eyebrow">How it works</span><h2>From first call to first payout in four steps</h2></div>
 <div class="steps">
  <div class="step"><h3>Tell us about your location</h3><p>Give us a call or reach out through the contact button on this page. We'll ask about foot traffic, hours, and space.</p></div>
  <div class="step"><h3>Site analysis</h3><p>We recommend the right machine, surcharge, and withdrawal limit for your customers.</p></div>
  <div class="step"><h3>Free install &amp; cash load</h3><p>We deliver, install, and stock the ATM. You supply a standard 110v outlet.</p></div>
  <div class="step"><h3>Get paid monthly</h3><p>If you opt for a revenue share, you receive your split each month by the 10th of the following month.</p></div>
 </div>
</div></section>

{areas_block()}
{faq_block(HOME_FAQ)}
{cta_band()}
"""
PAGES.append(home)

# ================================================================== PLACEMENT
PL_FAQ = [
 ("I already have a Visa/Mastercard terminal. How does an ATM help my bottom line?", "<p>Industry reports on North American ATM activity show more than 10 billion transactions a year with over half a trillion dollars dispensed, half of all adults using ATMs regularly, and a typical ATM user spending 20–25% more than a non-user. Customers who pay with cash instead of a debit card also save you credit-card processing fees.</p>"),
 ("My register already accepts ATM cards. What does an ATM add?", "<p>Customers who aren't sure of their balance often avoid making a purchase rather than risk a declined card. At our ATM they can check checking, savings, and credit balances for free, and in most cases transfer funds from savings, then withdraw cash and spend it at your establishment. It also ends cash-back at the register, where you pay processing fees on the full amount and tie up your own drawer cash.</p>"),
 ("How much does it cost to get started?", "<p>With free placement, nothing. We pay for the install, setup, cash loading, and monitoring. All you do is take advantage of the benefits an ATM brings.</p>"),
 ("How much will the surcharge be?", f"<p>At setup we analyze your location to determine the best surcharge and maximum withdrawal amount for your customers. Most {STATE} locations run between $3.50 and $4.00.</p>"),
 ("When do I receive my surcharge payout?", "<p>Free-placement locations are paid at the end of each month, along with a printout of every transaction for that period.</p>"),
 ("What are my ongoing expenses?", "<p>With a free placement you have none. The ATM needs a data port (or wireless modem) and a standard electrical outlet. One roll of receipt paper is included and typically lasts five to six months; additional rolls cost less than $10.</p>"),
 (f"Do you offer ATM placement near me in {STATE}?", f"<p>If your business is in {STATE}, almost certainly yes. We run regular routes through {', '.join(AREAS[:-1])}, and {AREAS[-1]}. See our " + TOP_LINKS + " pages, or call and ask about your city.</p>"),
 ("What kinds of businesses qualify?", "<p>Bars, restaurants, nightclubs, hotels and motels, convenience stores, smoke and vape shops, tattoo shops, barbershops and salons, laundromats, entertainment venues, and city or county facilities. If you have steady foot traffic and cash-friendly customers, you're a strong candidate.</p>"),
]
pl = {
 "path":"atm-placement.html",
 "title":f"Free ATM Placement in {METRO} & {STATE} | {BRAND}",
 "desc":f"Get a free ATM at your {STATE} bar, restaurant, hotel, or store. We install, load the cash, and monitor it at no cost — you earn a monthly surcharge share. {METRO} & statewide.",
 "ld":[service_ld("Free ATM placement", BASE+"/atm-placement.html",f"Turnkey ATM placement program for {STATE} businesses at no cost: installation, cash loading, monitoring, and a surcharge revenue share."), faq_ld(PL_FAQ), crumbs_ld([("Home","index.html"),("Free ATM Placement","atm-placement.html")])],
}
pl["body"] = sub_hero(pl,f"Free ATM placement in {STATE}",f"Free ATM placement for {METRO} and {STATE} businesses — installed, stocked, and monitored by us","Are you a business owner interested in a turnkey ATM solution placed free of charge at your place of business? Our no-cost, full-service program means we take on every expense and every task. You collect a share of the surcharge every month.","hero-skyline.svg",crumbs=[("Free ATM Placement",None)],extra=f'<div class="btn-row"><a class="btn btn-light" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div>') + f"""
<div class="trust"><div class="wrap"><span>$0 install &amp; upgrades</span><span>We supply all the cash</span><span>24/7/365 monitoring</span><span>Monthly surcharge payout</span></div></div>

<section><div class="wrap">
 <div class="section-head"><span class="eyebrow">What's included</span><h2>Our no-cost, full-service ATM program</h2><p class="lead">Everything an ATM needs to run, handled by {BRAND}.</p></div>
 <div class="grid grid-4">
  <div class="card"><div class="icon">{ICONS['truck']}</div><h3>Free installation and upgrades</h3><p>We do not charge to install your ATM or to perform upgrades over the life of the agreement.</p></div>
  <div class="card"><div class="icon">{ICONS['cash']}</div><h3>Cash loading services</h3><p>We provide all the capital and keep the machine stocked so your customers always find cash on hand.</p></div>
  <div class="card"><div class="icon">{ICONS['support']}</div><h3>Monitoring and maintenance</h3><p>We monitor your machine 24 hours a day, 365 days a year to ensure continuous operation, and fix problems fast.</p></div>
  <div class="card"><div class="icon">{ICONS['process']}</div><h3>Aggressive revenue share</h3><p>A generous share of every surcharge, paid monthly, so the ATM becomes a steady new income line for your business.</p></div>
 </div>
</div></section>

<section class="alt" id="earnings"><div class="wrap">
 <div class="section-head"><span class="eyebrow">Earnings estimates</span><h2>What a free ATM placement can pay your location</h2><p class="lead">Estimates are based on actual US ATM Experts locations. Your numbers will vary with foot traffic and the surcharge we set together.</p></div>
 <div class="table-wrap"><table>
  <thead><tr><th>Scenario</th><th>Surcharge</th><th>Your share</th><th>Withdrawals / month</th><th>Monthly</th><th>3-year total</th></tr></thead>
  <tbody>
   <tr><td><strong>Average surcharge, low volume</strong></td><td>$3.50</td><td>$0.50</td><td>100</td><td><strong>$50</strong></td><td><strong>$1,800</strong></td></tr>
   <tr><td><strong>Average surcharge, high volume</strong></td><td>$3.50</td><td>$0.50</td><td>300</td><td><strong>$150</strong></td><td><strong>$5,400</strong></td></tr>
   <tr><td><strong>High surcharge, low volume</strong></td><td>$4.00</td><td>$1.00</td><td>100</td><td><strong>$100</strong></td><td><strong>$3,600</strong></td></tr>
   <tr><td><strong>High surcharge, high volume</strong></td><td>$4.00</td><td>$1.00</td><td>300</td><td><strong>$300</strong></td><td><strong>$10,800</strong></td></tr>
  </tbody></table></div>
 <p class="note" style="margin-top:.75rem">Plus the indirect lift: ATM users spend 20–25% more in-store than non-users, and every cash sale avoids card processing fees.</p>
</div></section>

<section><div class="wrap"><div class="split">
 <img src="_assets/_images/placement-locations.svg" alt="Illustrated business types that qualify for free ATM placement: dispensary, bar and grill, hotel, convenience store, tattoo and barber, city facility" width="1200" height="900" loading="lazy">
 <div>
  <span class="eyebrow">Who it's for</span>
  <h2>The best {STATE} locations for a placed ATM</h2>
  <p>We've placed machines everywhere from {METRO} bars to small-town city halls. The common thread is steady foot traffic and customers who like to pay cash. Strong candidates include:</p>
  <ul class="checks">
   <li>Bars, nightclubs, breweries, and restaurants</li>
   <li>Hotels, motels, and resorts</li>
   <li>Convenience stores, smoke shops, and liquor stores</li>
   <li>Tattoo shops, barbershops, and salons</li>
   <li>Nightlife districts and entertainment venues</li>
   <li>City, town, and county facilities</li>
  </ul>
  
 </div>
</div></div></section>

<section class="alt"><div class="wrap">
 <div class="section-head"><span class="eyebrow">How it works</span><h2>Placement in four steps</h2></div>
 <div class="steps">
  <div class="step"><h3>Quick qualification</h3><p>Tell us your business type, hours, and rough foot traffic. Most locations hear back the same day.</p></div>
  <div class="step"><h3>Site analysis</h3><p>We pick the machine, surcharge, and withdrawal limit that best fit your customers.</p></div>
  <div class="step"><h3>Install &amp; cash load</h3><p>We deliver and install the ATM and stock it with our cash. You provide an outlet and a data connection.</p></div>
  <div class="step"><h3>Monthly payout</h3><p>Your surcharge share arrives at the end of each month with a full transaction report.</p></div>
 </div>
</div></section>

<section><div class="wrap"><div class="section-head"><span class="eyebrow">Placement vs. ownership</span><h2>Should you take a free placement or buy your own ATM?</h2></div>
 <div class="grid grid-2">
  <div class="card feature"><h3>Free placement</h3><p>Best if you want zero upfront cost and zero responsibility. We own the machine, supply the cash, and handle service. You earn a per-transaction share, paid monthly.</p></div>
  <div class="card"><h3>Buy your own</h3><p>Best if you have the capital and want to keep 100% of the surcharge. Every machine we sell includes free processing, free shipping, support, and next-day deposits.</p><a class="more" href="equipment.html">See our ATMs →</a></div>
 </div>
</div></section>

<section><div class="wrap"><div class="section-head"><span class="eyebrow">Local expertise</span><h2>Why {STATE} businesses choose {BRAND}</h2></div>
 <div class="grid grid-3">
  <div class="card"><h3>Local cash routes, not a call center</h3><p>We run our own cash and service routes across {STATE}, {SPAN}. When a machine needs attention, a technician who covers your area handles it — backed by the resources of the US ATM Experts network.</p></div>
  <div class="card"><h3>Built for {STATE} traffic patterns</h3><p>{SEASONAL[0].upper()+SEASONAL[1:]} all change how much cash a location needs. Our cash load prediction software learns each location's pattern so the machine is stocked for the rush and not over-loaded in the lull.</p></div>
  <div class="card"><h3>One company for every ATM need</h3><p>Free placement, {DISP_LINK_PL}<a href="atm-processing.html">ATM processing</a>, and <a href="equipment.html">Genmega and Hyosung machines for sale</a> — all from one {STATE} team you can reach by phone.</p></div>
 </div>
</div></section>

<section class="alt"><div class="wrap"><div class="split">
 <div>
  <span class="eyebrow">Install day</span>
  <h2>What to expect when we install your ATM</h2>
  <p>Once your location is approved, we schedule a delivery window that works around your business hours. Our technician positions the machine where it will get the most use, usually near the entrance or the register, and connects it to power. Connectivity is handled by a wireless router, so there's no phone line or ethernet run to arrange.</p>
  <p>The machine is loaded with our cash, tested with live transactions, and monitored from the moment it comes online. You'll receive a login for real-time reporting and a direct line to your account representative. Most installs are finished in under an hour.</p>
  <ul class="checks"><li>Scheduled around your hours</li><li>Placed where it earns the most</li><li>Wireless connectivity included</li><li>Tested live before we leave</li></ul>
 </div>
 <img src="_assets/_images/daily-vault-cash-deposits.svg" alt="Illustration of an ATM being stocked and its surcharge revenue deposited to the location owner" width="1200" height="900" loading="lazy">
</div></div></section>

{areas_block(heading=f"Free ATM placement across {STATE}")}
{faq_block(PL_FAQ, title="Free ATM placement FAQs")}
{cta_band(h="Find out if your location qualifies", p="Send a few details about your business and we'll respond with a recommendation and an earnings estimate — no obligation.")}
"""
PAGES.append(pl)


# ================================================================== DISPENSARIES
DI_FAQ = [
 ("Are your dispensary ATMs compliant?", "<p>Yes. Our dispensary ATMs are 100% compliant. Every transaction is processed transparently under your dispensary's real business name and address, so that is exactly what appears on your customers' bank statements — no disguised merchant descriptors, no shell company names, and no workarounds that put your license or your banking relationships at risk.</p>"),
 ("What shows up on the customer's bank statement?", "<p>Your dispensary's actual name and street address. The withdrawal is recorded on the cardholder's bank statement exactly where it happened, the same way it would be for any other retail business.</p>"),
 ("Does it cost my dispensary anything?", "<p>Not with free placement. We supply the machine, install it, load and manage the cash, and monitor it around the clock. You provide a standard 110v outlet, and we provide you with fair revenue share options.</p>"),
 ("How much cash can the ATM hold?", "<p>It depends on the model and your volume. Our Genmega machines support up to four 2,000-note cassettes, and we size the cash load and refill schedule to your traffic so the machine stays stocked through your busiest days.</p>"),
 (f"Do you serve dispensaries outside {METRO}?", f"<p>Yes. We place and service dispensary ATMs across {STATE}, including {', '.join(AREAS[1:6])}, and {METRO_PHRASE}.</p>"),
]
di = {
 "path":"dispensaries.html",
 "title":f"Dispensary ATMs in {STATE} | Compliant Cannabis ATM Placement",
 "desc":f"100% compliant ATMs for {STATE} dispensaries. Customer bank statements show your dispensary's real name and address. Free placement, cash loading, and monitoring from the largest cannabis ATM company in the country.",
 "ld":[service_ld("Dispensary ATM placement", BASE+"/dispensaries.html",f"Compliant ATM placement, cash management, and processing for cannabis dispensaries in {STATE}, with the dispensary's real name and address on every customer bank statement."), faq_ld(DI_FAQ), crumbs_ld([("Home","index.html"),("Dispensary ATMs","dispensaries.html")])],
}
di["body"] = sub_hero(di,"Dispensary ATMs",f"100% compliant ATMs for {STATE} dispensaries","Cash is still king in cannabis. We're the largest cannabis ATM company in the country, and every machine we place runs fully compliant — with your dispensary's real name and address showing on your customers' bank statements.","dispensary-hero.svg",crumbs=[("Dispensary ATMs",None)],extra=f'<div class="btn-row"><a class="btn btn-light" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div>') + f"""
<div class="trust"><div class="wrap"><span>100% compliant</span><span>Real name &amp; address on bank statements</span><span>Largest cannabis ATM company in the country</span><span>Free placement available</span></div></div>

<section><div class="wrap"><div class="split">
 <div>
  <span class="eyebrow">Compliance first</span>
  <h2>Transparent transactions. Your real name and address on the bank statement.</h2>
  <p>Some ATM operators put machines in dispensaries under a different merchant name or a disguised address to hide what the business is. That exposes the dispensary and its customers, and it can cost you your banking relationships. We don't do that.</p>
  <p>Every ATM we place in a dispensary processes under your actual business name and street address. The line item on your customer's bank statement shows exactly where the withdrawal happened — the same way it would at any other retailer.</p>
  <ul class="checks">
   <li><strong>100% compliant</strong> ATM placement and processing</li>
   <li><strong>Real dispensary name and address</strong> on every customer bank statement</li>
   <li><strong>No disguised descriptors</strong>, shell names, or workarounds</li>
   <li><strong>Accurate statement records</strong> for you and your customers</li>
  </ul>
  
 </div>
 <img src="_assets/_images/dispensary-bank-statement.svg" alt="Illustration of a customer's mobile banking statement showing an ATM withdrawal listed under the dispensary's real name and street address" width="1200" height="900" loading="lazy">
</div></div></section>

<section class="dark"><div class="wrap">
 <div class="section-head"><span class="eyebrow">Why us</span><h2>The largest cannabis ATM company in the country</h2><p class="lead">Dispensaries are a specialty for us, not an afterthought. We understand the cash volume, the compliance expectations, and the service level a licensed dispensary needs.</p></div>
 <div class="grid grid-3">
  <div class="stat"><b>#1</b><span>largest cannabis ATM company in the country</span></div>
  <div class="stat"><b>100%</b><span>compliant transactions, with your real address on the bank statement</span></div>
  <div class="stat"><b>$0</b><span>to get started with free placement</span></div>
 </div>
</div></section>

<section class="alt"><div class="wrap">
 <div class="section-head"><span class="eyebrow">Built for dispensaries</span><h2>What your dispensary gets</h2></div>
 <div class="grid grid-4">
  <div class="card"><div class="icon">{ICONS['shield']}</div><h3>Compliant processing</h3><p>Transparent transactions under your real business name and address, so your ATM never becomes a compliance problem.</p></div>
  <div class="card"><div class="icon">{ICONS['cash']}</div><h3>Cash that keeps up</h3><p>We supply and load the cash, size the cassettes to your volume, and monitor levels so the machine doesn't run dry on a Friday night.</p></div>
  <div class="card"><div class="icon">{ICONS['process']}</div><h3>Real-time reporting</h3><p>See cash remaining, surcharge revenue, and every transaction from a web or mobile login.</p></div>
  <div class="card"><div class="icon">{ICONS['support']}</div><h3>Dedicated support</h3><p>A dedicated account representative who knows your machine and your location.</p></div>
 </div>
</div></section>

<section><div class="wrap">
 <div class="section-head"><span class="eyebrow">Aggressive revenue shares</span><h2>Dispensary ATMs earn more, so we share more</h2><p class="lead">Dispensaries run cash-only, which makes an on-site ATM one of the highest-volume machines we place. That volume lets us offer dispensaries some of the most aggressive revenue share options in the industry.</p></div>
 <div class="grid grid-3">
  <div class="card feature"><div class="icon">{ICONS['cash']}</div><h3>Options sized to your volume</h3><p>We analyze your foot traffic and transaction counts and build a revenue share around them. Higher volume means a stronger split for your dispensary.</p></div>
  <div class="card"><div class="icon">{ICONS['process']}</div><h3>Paid monthly, on time</h3><p>Your split is deposited each month by the 10th of the following month, backed by a full transaction report you can verify against your online reporting login.</p></div>
  <div class="card"><div class="icon">{ICONS['shield']}</div><h3>Nothing out of pocket</h3><p>We supply the machine, the cash, the installation, and the monitoring. Your dispensary provides a standard 110v outlet and collects a share of every surcharge.</p></div>
 </div>
 <div class="btn-row" style="margin-top:2rem"><a class="btn btn-outline" href="atm-placement.html#earnings">See earnings estimates</a></div>
</div></section>


<section class="alt"><div class="wrap"><div class="split">
 <div>
  <span class="eyebrow">Dispensary ATM experts</span>
  <h2>We've been doing this a long time, and it shows</h2>
  <p>Dispensary ATMs are not a side business for us. We've been placing and servicing ATMs in dispensaries for 14 years, and we've built our operation around the two things a dispensary can't afford: downtime and an empty machine.</p>
  <ul class="checks">
   <li><strong>Over 99% uptime</strong> across our dispensary ATMs, so your customers always have a working machine when they walk in</li>
   <li><strong>Cash load prediction software</strong> that forecasts each location's withdrawals and schedules refills before the cash runs low, so our ATMs never run empty</li>
   <li><strong>14 years of experience</strong> with the cash volume, compliance expectations, and service level licensed dispensaries require</li>
   <li><strong>Real-time monitoring</strong> that flags cash levels and machine errors the moment they happen</li>
  </ul>
  
 </div>
 <div class="grid" style="grid-template-columns:1fr 1fr;gap:1rem">
  <div class="stat"><b>99%+</b><span>uptime on our dispensary ATMs</span></div>
  <div class="stat"><b>0</b><span>empty machines — cash loads are predicted, not guessed</span></div>
  <div class="stat"><b>#1</b><span>largest cannabis ATM company in the country</span></div>
  <div class="stat"><b>14</b><span>years in the ATM business</span></div>
 </div>
</div></div></section>

{areas_block(heading=f"Dispensary ATMs across {STATE}")}
{faq_block(DI_FAQ, title="Dispensary ATM FAQs")}
{cta_band(h="Put a compliant ATM in your dispensary", p="Tell us about your location and volume. We'll recommend the right machine, cash plan, and revenue share for your dispensary.")}
"""
di["body"] = di["body"].replace("_assets/_images/_slider_images/../dispensary-hero.svg')\"","_assets/_images/dispensary-hero.svg');opacity:.5\"",1)
if CANNABIS: PAGES.append(di)

# ================================================================== PROCESSING
PR_FAQ = [
 ("When do I receive my vault money?", "<p>Funds from Monday's transactions are available Tuesday, Tuesday's on Wednesday, and Thursday's on Friday. Transactions from Friday, Saturday, and Sunday are deposited the following Monday via the Federal Reserve.</p>"),
 ("I already operate ATMs with another processor. Can I switch?", "<p>Yes. We convert existing portfolios all the time. Tell us your terminal count and average monthly transactions and we'll quote interchange and processing terms; if you move, we handle the reprogramming and network paperwork and convert on your schedule so no machine goes dark.</p>"),
 ("Is processing really free?", "<p>Yes. Free ATM processing is included with every ATM we sell and with every free placement. There are no monthly processing or statement fees.</p>"),
 ("How do I see my ATM's activity?", "<p>You receive your own personal login to monitor your ATM on the web or a mobile app: see how much cash remains in the machine, your surcharge revenue, and transaction history in real time.</p>"),
 ("Can you take over processing for an ATM I already own?", "<p>In most cases, yes. Call us with the make and model of your machine and we'll walk you through switching.</p>"),
]
pr = {
 "path":"atm-processing.html",
 "title":f"ATM Processing for {STATE} ATM Owners | {BRAND}",
 "desc":f"Free ATM processing with daily deposits and real-time online reporting, included with every ATM we sell or place in {STATE}. Keep 100% of the surcharge on owned machines.",
 "ld":[service_ld("ATM processing", BASE+"/atm-processing.html",f"ATM transaction processing with daily deposits and real-time online reporting for ATM owners in {STATE}."), faq_ld(PR_FAQ), crumbs_ld([("Home","index.html"),("ATM Processing","atm-processing.html")])],
}
pr["body"] = sub_hero(pr,"ATM processing",f"{STATE} ATM processing with aggressive interchange and daily deposits",f"{BRAND} provides free ATM processing with each ATM we sell, and aggressive interchange for operators who bring their portfolio to us. No more waiting days for your vault cash funds, and no more guessing how much money is remaining in your ATM.","hero-processing.svg",crumbs=[("ATM Processing",None)],extra='<div class="btn-row"><a class="btn btn-light" href="#apply">Get a processing quote</a></div>') + f"""
<div class="trust"><div class="wrap"><span>Aggressive interchange</span><span>No processing fees</span><span>Daily deposits</span><span>Real-time reporting</span><span>Dedicated account rep</span></div></div>
{PORTFOLIO}

<section><div class="wrap"><div class="split">
 <img src="_assets/_images/daily-vault-cash-deposits.svg" alt="Illustration of cash withdrawn from an ATM being deposited to your bank the next business day" width="1200" height="900" loading="lazy">
 <div>
  <span class="eyebrow">Daily cash deposits</span>
  <h2>Your money, back in your account daily</h2>
  <p>No more waiting days for your funds to be deposited back into your account. {BRAND} makes sure your funds are deposited daily as cash is withdrawn from your ATM, settled through the Federal Reserve.</p>
  <ul class="checks"><li>Monday's transactions available Tuesday</li><li>Weekend transactions deposited Monday</li><li>Access to online statements</li><li>Surcharge deposits can be daily or monthly</li></ul>
 </div>
</div></div></section>

<section class="alt"><div class="wrap"><div class="split">
 <div>
  <span class="eyebrow">Online real-time reporting</span>
  <h2>Know exactly what your ATM is doing</h2>
  <p>You'll receive your own personal login so you can monitor your ATM via the web or a mobile app. See how much money remains in your machine, your surcharge revenue to date, and every transaction as it happens. This service is included with every machine we sell.</p>
  
 </div>
 <img src="_assets/_images/real-time-reporting.svg" alt="Illustration of a real-time ATM reporting dashboard showing cash remaining, surcharge revenue, and recent withdrawals" width="1200" height="900" loading="lazy">
</div></div></section>

<section><div class="wrap">
 <div class="section-head"><span class="eyebrow">Included with every ATM</span><h2>What our processing service includes</h2></div>
 <div class="grid grid-3">
  <div class="card"><div class="icon">{ICONS['cash']}</div><h3>Free processing</h3><p>No monthly processing fees. On ATMs you own, you keep 100% of the surcharge.</p></div>
  <div class="card"><div class="icon">{ICONS['support']}</div><h3>Dedicated support</h3><p>A dedicated account representative who knows your machine.</p></div>
  <div class="card"><div class="icon">{ICONS['shield']}</div><h3>Compliance handled</h3><p>EMV-compliant equipment and processing that keeps you current with network rules.</p></div>
 </div>
</div></section>

{faq_block(PR_FAQ, title="ATM processing FAQs")}
{cta_band(h="Own an ATM or thinking about it?", p="Compare buying and free placement with a quick call. We'll show you the numbers for your location.")}
"""
FOOTNOTE = '<section style="padding:1.5rem 0"><div class="wrap"><p id="cannabis-fee" style="margin:0;font-size:.9rem;color:var(--muted)">* Due to additional required compliance, cannabis transactions are subject to a $0.05 processing fee.</p></div></section>'
if CANNABIS:   # footnote only where cannabis retail is legal
    pr["body"] = re.sub(r"([Ff]ree (?:ATM )?processing)(?![*\w])", r"\1*", pr["body"])
    pr["body"] = pr["body"].replace('<section class="cta-band">', FOOTNOTE + '<section class="cta-band">', 1)
pr["body"] += PORTFOLIO_FORM
PAGES.append(pr)

# ================================================================== EQUIPMENT
PRODUCTS = [
 {"slug":"nh_halo_ii","brand":"Nautilus Hyosung","name":"Halo II","img":"nautilus-hyosung-halo-ii.jpg","price":None,"pdf":"Halo_II_Brochure.pdf",
  "short":"Sleek retail ATM with a 10.1\" screen, customizable LED keypad lighting, and Hyosung's industry-leading reliability.",
  "desc":"The HALO II offers a unique, sleek design perfect for locations ranging from small convenience stores to high-end retail ATM locations. Eye-catching, customizable color LED lighting around the keypad attracts more users to drive additional transactions and revenue to your bottom line. The intuitive Hyosung interface is presented on a vivid 10.1-inch LCD screen, and all user touch points — screen, keypad, and cash exit — are positioned for optimal visibility and access.",
  "sections":[("Reliability","Nautilus Hyosung continues to lead the industry in reliability and ease of service. The HALO II uses proven cash-dispensing technology engineered for maximum uptime, widely regarded as the best in the industry."),("Environmentally friendly","Energy-saving features reduce power consumption and operating cost without sacrificing performance."),("New technology","Optional cardless withdrawals via NFC let customers use their phone at the ATM.")],
  "specs":[("Platform","Microsoft Windows CE 6.0"),("Display","10.1\" color TFT LCD"),("Card reader","DIP, EMV-compliant"),("Cash cassette","1,000 or 2,000 notes"),("Dimensions","54.2\"H × 15.7\"W × 23.4\"D"),("Weight","265 lbs"),("Power","AC 110/220V ±10%, 50/60 Hz, 145W"),("Operating range","0–40°C, 20–85% humidity")]},
 {"slug":"nh_mx2800se","brand":"Nautilus Hyosung","name":"MX 2800SE (Force)","img":"nautilus-hyosung-mx2800se.jpg","price":None,"pdf":"MX2800SE_Brochure.pdf",
  "short":"12.1\" capacitive-touch display, dimmable topper, and up to 6,000-note capacity for high-volume locations.",
  "desc":"The brilliant 12.1-inch color display has capacitive-touch function keys and an elegant user interface. The integrated topper has a brightness control (high, medium, low) so the FORCE can be customized to any environment, from bright convenience stores to dark nightclubs. Arrows at the card and receipt slots light up to direct the user, and the vault holds up to 6,000 notes.",
  "sections":[("Serviceability","Vault lighting makes cash loading and service easier, and the design offers maximum installation versatility."),("Security","An optional camera photographs users during transactions and can display an on-screen awareness notification."),("Connectivity","Includes a wireless-modem mounting bracket and two additional power outlets, one for a wireless modem and one for any other device.")],
  "specs":[("Platform","Microsoft Windows CE 6.0"),("Display","12.1\" wide color TFT LCD, capacitive touch keys"),("Card reader","EMV Level 1–2 compliant"),("Cash capacity","Up to 6,000 notes (three 2,000-note cassettes)"),("Dimensions","56.4\"H × 15.7\"W × 23.0\"D"),("Weight","286.6 lbs"),("Power","AC 110/240V ±10%, 50/60 Hz, 145W"),("Operating range","0–40°C (32–104°F)")]},
 {"slug":"nh_mx2800T","brand":"Nautilus Hyosung","name":"MX 2800T","img":"nautilus-hyosung-mx2800T.jpg","price":None,"pdf":"2800T_Brochure.pdf",
  "short":"Through-the-wall ATM with an adjustable throat up to 10\", 12.1\" display, and multi-language interface.",
  "desc":"Based on customer feedback, the 2800T now comes standard with an adjustable throat servicing walls up to 10 inches. It showcases an elegant user interface on a brilliant 12.1-inch color display with capacitive-touch function keys, and the integrated topper's brightness control lets it fit any environment, from bright C-stores to dark nightclubs.",
  "sections":[("Serviceability","Vault lighting for cash loading and maximum installation versatility."),("Security","Optional camera photographs users during transactions and can display an on-screen awareness notification."),("Connectivity","Wireless mounting bracket and two additional power outlets: one for your wireless modem and another for any other device.")],
  "specs":[("Platform","Microsoft Windows CE 6.0"),("Display","12.1\" customer screen (800×480); 8\" operator panel"),("Card reader","EMV DIP type, magnetic stripe compatible"),("Cash dispenser","2,000-note removable cassette, upgradable to three"),("Printer","80 mm thermal receipt"),("Dimensions","72.0\"H × 15.7\"W × 26.3–33.3\"D"),("Weight","330.7 lbs"),("Languages","English, Spanish, French, Japanese, Chinese, Korean")]},
 {"slug":"gm_g2500","brand":"Genmega","name":"G2500","img":"genmega-g2500.jpg","price":None,"pdf":"Genmega_G2500_Brochure.pdf",
  "short":"The workhorse retail ATM: configurable hardware, 8\" screen (10.2\" touch optional), and dispensers up to 4×2,000 notes.",
  "desc":"Genmega's G2500 series is designed for retail and off-premise locations. It comes loaded with all the features you expect and adds hardware configuration choices that let you custom-fit each machine to the needs of your location. Standard features include an 8-inch high-resolution LCD (upgradeable to a 10.2-inch touchscreen), a standard receipt printer (upgradeable to 3-inch graphics-capable), and optional energy-efficient LED toppers.",
  "sections":[("Flexible dispensers","Accepts cash dispensers from Genmega and other suppliers, from a 1,000-note removable cassette up to four 2,000-note cassettes."),("Security","UL 291 business-hours vault with electronic lock; PCI/Interac-certified PIN pad.")],
  "specs":[("Display","8\" 32-bit color TFT LCD, 800×480 (10.2\" touch optional)"),("Printer","56 mm standard; 80 mm graphics-capable optional"),("PIN pad","16-key alphanumeric, PCI/Interac certified"),("CPU","Cortex-A8 800 MHz, 256 MB DDR2, 512 MB flash"),("Card reader","DIP type, EMV optional"),("Cash dispenser","1,000-note cassette up to 4×2,000 notes"),("Dimensions","56.3\"H × 15.8\"W × 22.3\"D"),("Weight / power","222 lbs · AC 110/220V, 50/60 Hz, 145W")]},
 {"slug":"gm_onyx","brand":"Genmega","name":"Onyx","img":"genmega-onyx.jpg","price":None,"pdf":"Genmega_Onyx_Brochure.pdf",
  "short":"Modern, upscale design with a 10.2\" wide display, lighted function keys, and a reflective front bezel.",
  "desc":"A new, modern, upscale design containing a set of standard features that are sure to impress, the Onyx provides the latest in ATM technology for any market. It features a 10.2-inch wide LED-LCD display (optional 12.1-inch touchscreen), a reflective front bezel, and lighted function keys. An optional 3-inch receipt printer supports graphics. Fully compliant with EMV, PCI-EPP, and ADA standards.",
  "sections":[("Dispenser options","Supports multiple dispenser configurations inside a UL 291 vault with electronic lock."),("Low power","Runs on just 85.5 watts, keeping operating costs down.")],
  "specs":[("Display","10.2\" wide 32-bit color TFT LCD, 1280×800"),("Printer","56 mm (2\") standard; 80 mm (3\") optional, graphics capable"),("CPU","Cortex-A8 800 MHz, 256 MB DDR2, 512 MB flash"),("Compliance","EMV, PCI-EPP, ADA"),("Dimensions","56.4\"H × 15.8\"W × 22.3\"D"),("Weight","223 lbs"),("Power","AC 110/220V ±10%, 50/60 Hz, 85.5W")]},
 {"slug":"gm_onyx_w","brand":"Genmega","name":"Onyx-W","img":"genmega-onyx-w.jpg","price":None,"pdf":"Genmega_OnyxW_Brochure.pdf",
  "short":"Wall-mount or countertop ATM with a 10.1\" display and 1,000-note cassette — ideal where floor space is tight.",
  "desc":"Featuring a high-resolution 10.1-inch LED screen and light-up touch function keys along with a 2-inch receipt printer, the Onyx-W uses the same modules, software, and functions found in existing Genmega ATMs. It installs as a wall-mounted or countertop unit, and a 1,000-note removable cassette with internal vault and electronic lock secures the cash.",
  "sections":[("Compact footprint","At just over 10 inches deep, the Onyx-W fits bars, salons, and shops where a full-size ATM won't."),("Security","Electronic, A-series, or Cencon lock options.")],
  "specs":[("Display","10.1\" TFT, 1280×800, 8 lighted-touch function keys"),("Printer","56 mm (2\")"),("CPU","Cortex-A8 800 MHz, 256 MB SRAM, 512 MB flash, Windows CE 6.0"),("Card reader","EMV, DIP type"),("Cassette","1,000 or 2,000 notes"),("Dimensions","19.7\"H × 26.8\"W × 10.4\"D"),("Weight","121 lbs"),("Power","110/220V, 50/60 Hz, 145W")]},
 {"slug":"gm_nova","brand":"Genmega","name":"Nova","img":"genmega-nova.jpg","price":None,"pdf":"Genmega_Nova_Brochure.pdf",
  "short":"The future of retail ATMs: a 17\" vertical touchscreen that runs full-motion video up top and the ATM program below, with edge lighting and up to 4×2,000-note capacity.",
  "desc":"With a world of new services, new functions, and new revenue-generating opportunities, the NOVA stands ready to redefine the retail ATM. Its high-definition 17-inch touchscreen allows full-motion video on the top half of the screen while running the ATM program on the bottom half, creating a new generation of retail ATMs — and a new advertising revenue line without the need for a digital topper.",
  "sections":[("Proven components","Created with tried and tested components from existing Genmega retail ATMs, the NOVA does not require you to stock additional parts. It uses the same UL-291 certified vault as the G2500 and Onyx, with the same security features Genmega ATMs have offered for years."),("Designed for what's next","Edge lighting around the cash dispenser and encrypted PIN pad draws customers in, and the platform is built with an eye on Near Field Communications, recyclers, and future components."),("Security","UL 291 business-hours vault with electronic lock; UL 291 Level 1 vault available; PCI 5.0 certified encrypted PIN pad.")],
  "specs":[("Display","17\" vertical capacitive touchscreen (HD, full-motion video)"),("Cash dispenser","Up to 4 × 2,000-note removable cassettes"),("Vault","UL 291 business-hours vault; UL 291 Level 1 available"),("Card reader","EMV MCR"),("Printer","3\" receipt printer"),("PIN pad","Encrypted, PCI 5.0 certified"),("Lighting","Edge lighting around CDU and EPP")]},
 {"slug":"inhand_i22","brand":"InHand","name":"I-22 Wireless Modem (IP-only)","img":"inhand-i22-iponly.jpg","price":"$129","airtime":"+$4.95/mo for airtime","pdf":None,
  "short":"4G LTE modem on Verizon or AT&T with two ethernet ports and a 5-year advanced-replacement warranty.",
  "desc":"The InHand I-22 brings the same reliability and affordability as the previous I-4100 with more capability: a lower price, a second ethernet port, and a choice of Verizon 4G LTE or AT&T 4G LTE service. Choose the IP-only model when you need one carrier.",
  "sections":[("Includes","Two 3G/4G antennas, power supply, mounting bracket, ATM programming guide, and a 5-year warranty with advanced replacement program.")],
  "specs":[("Carrier","Verizon 4G LTE or AT&T 4G LTE"),("Ethernet","2 ports"),("Antennas","Two receptacles, two antennas included"),("Warranty","5 years, advanced replacement")]},
 {"slug":"idm_origin","brand":"IDM Wireless","name":"Origin Wireless Router","img":"idm-origin-router.jpg","price":"$99","airtime":"+$4.95/mo for airtime","pdf":None,
  "short":"Compact Cat 4 LTE router built for retail ATMs, certified on AT&T, T-Mobile, and Verizon, with dual-SIM failover and built-in security.",
  "desc":"The IDM Wireless Origin delivers reliable wireless connectivity for retail-level ATM machines, featuring dual SIM failover and built-in security. It combines industrial-grade hardware with advanced network features to support your ATM connectivity needs, and flexible configuration options and centralized management tools make it an essential part of any deployment.",
  "sections":[("Features and capabilities","Fully integrated with the IDM monitoring portal (idmcontrol.com). Cat 4 data speeds up to 150 Mbps down and 50 Mbps up. Certified for AT&T, T-Mobile, and Verizon for nationwide coverage. Two 10/100 Mbps Ethernet ports support LAN or WAN configurations."),("Built for the field","A metal IP30 casing resists extreme temperatures (-20°C to 70°C) and electromagnetic interference, in a compact 3.2\" × 0.96\" × 3.66\" footprint with a DC 12V power supply.")],
  "specs":[("Carriers","AT&T, T-Mobile, Verizon (single or dual-carrier failover)"),("LTE category","Cat 4 — up to 150 Mbps down / 50 Mbps up"),("Ethernet","Two 10/100 Mbps ports, LAN or WAN"),("Management","IDM Control monitoring portal"),("Casing","Metal, IP30"),("Operating temperature","-20°C to 70°C"),("Dimensions","3.2\" × 0.96\" × 3.66\""),("Power","DC 12V")]},
]

def product_card(p, depth=0):
    r = rel(depth)
    return f"""<a class="card link product" href="{r}product_pages/{p['slug']}.html"><img src="{img_url(p['img'],r)}"{img_fallback(p['img'],r)} alt="{esc(p['brand']+' '+p['name'])}{'' if p['brand'] in ('InHand','IDM Wireless') else ' ATM'}" width="500" height="500" loading="lazy"><span class="eyebrow" style="margin-bottom:.2rem">{p['brand']}</span><h3>{p['name']}</h3><p>{p['short']}</p><span class="price">{p["price"] if p.get("price") else "Reach out for current pricing"}<small>{("USD · "+p["airtime"]) if p.get("airtime") else ("USD" if p.get("price") else "")}</small></span><span class="more" style="margin-top:.75rem">View details →</span></a>"""

EQ_FAQ = [
 ("What's included when I buy an ATM?", "<p>Free processing, programming, an Origin Wireless Router, free shipping and handling (within the lower 48 states), real-time online reporting, a 2 year manufacturer's warranty, and 100% of the surcharge revenue.</p>"),
 ("What does an owned ATM need at my location?", "<p>A standard electrical outlet. Your ATM package comes with a modem for connectivity as well as a roll of receipt paper, which typically lasts six to twelve months. Rolls of receipt paper can be purchased through us or other online retailers.</p>"),
]
eq = {
 "path":"equipment.html",
 "title":f"ATM Machines for Sale in {STATE} | Genmega & Hyosung Dealer",
 "desc":f"ATM machines for sale in {METRO} and across {STATE}: Genmega and Nautilus Hyosung ATMs from {BRAND}. Every machine includes free processing, free shipping, and 100% of the surcharge.",
 "ld":[crumbs_ld([("Home","index.html"),("Buy an ATM","equipment.html")]), faq_ld(EQ_FAQ),
       {"@context":"https://schema.org","@type":"ItemList","name":"ATMs for sale","itemListElement":[{"@type":"ListItem","position":i+1,"name":f"{p['brand']} {p['name']}","url":f"{BASE}/product_pages/{p['slug']}.html"} for i,p in enumerate(PRODUCTS)]}],
}
eq["body"] = sub_hero(eq,f"ATM sales in {STATE}",f"Buy an ATM in {STATE} and keep 100% of the surcharge",f"{BRAND} is an authorized Genmega and Nautilus Hyosung dealer serving {METRO} and all of {STATE}. We'll walk you through the entire process, from choosing a model to your first deposit.","hero-equipment.svg",crumbs=[("Buy an ATM",None)]) + f"""
<div class="trust"><div class="wrap"><span>Free processing</span><span>Free shipping &amp; handling</span><span>Real-time online stats</span><span>Manufacturer's warranty</span><span>100% surcharge revenue</span></div></div>

<section><div class="wrap"><div class="section-head"><span class="eyebrow">Genmega</span><h2>Genmega ATMs</h2><p class="lead">The industry benchmark for reliability and uptime.</p></div><div class="grid grid-4">{''.join(product_card(p) for p in PRODUCTS if p['brand']=='Genmega')}</div></div></section>
<section class="alt"><div class="wrap"><div class="section-head"><span class="eyebrow">Nautilus Hyosung</span><h2>Nautilus Hyosung ATMs</h2></div><div class="grid grid-3">{''.join(product_card(p) for p in PRODUCTS if p['brand']=='Nautilus Hyosung')}</div></div></section>
<section><div class="wrap"><div class="section-head"><span class="eyebrow">Connectivity</span><h2>Wireless modems</h2><p class="lead">Skip the phone line. Run your ATM on 4G LTE.</p></div><div class="grid grid-3">{''.join(product_card(p) for p in PRODUCTS if p['brand'] in ('InHand','IDM Wireless'))}</div></div></section>


{faq_block(EQ_FAQ, title="ATM purchase FAQs")}
{cta_band(h="Reach out for current pricing", p="Pricing depends on cassette, screen, and topper options. Call us with your location details and we'll quote the exact build.")}
"""
PAGES.append(eq)

# ---- product pages
for p in PRODUCTS:
    full = f"{p['brand']} {p['name']}"
    url = f"{BASE}/product_pages/{p['slug']}.html"
    prod_ld = {"@context":"https://schema.org","@type":"Product","name":full+(" Wireless Modem" if p['brand']=='InHand' else "" if p['brand']=='IDM Wireless' else " ATM"),"image":img_abs(p['img']),"description":p['desc'],"brand":{"@type":"Brand","name":p['brand']},
               "offers":{"@type":"Offer","availability":"https://schema.org/InStock","seller":{"@id":BASE+"/#business"},"url":url,**({"price":p["price"].replace("$",""),"priceCurrency":"USD"} if p.get("price") else {})}}
    pg = {"path":f"product_pages/{p['slug']}.html","depth":1,
          "title":f"{full}{'' if p['brand'] in ('InHand','IDM Wireless') else ' ATM'} for Sale | {BRAND}",
          "desc":(p['short']+(" $"+p["price"].strip("$")+" from "+BRAND+"." if p.get("price") else " Free processing and shipping in "+STATE+". Reach out for current pricing."))[:158],
          "ld":[prod_ld, crumbs_ld([("Home","index.html"),("Buy an ATM","equipment.html"),(full,f"product_pages/{p['slug']}.html")])]}
    secs = "".join(f"<h2>{esc(t)}</h2><p>{esc(b)}</p>" for t,b in p['sections'])
    specs = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k,v in p['specs'])
    pdf = f'<a class="btn btn-outline" href="{pdf_url(p["pdf"],"../")}" target="_blank" rel="noopener">PDF spec sheet</a>' if p['pdf'] else ""
    price_html = (p["price"]+' <span style="font-size:1rem;font-weight:500;color:var(--muted)">USD'+((" · "+p["airtime"]) if p.get("airtime") else "")+'</span>') if p.get("price") else "Reach out for current pricing"
    pg["body"] = f"""
<div class="hero sub"><div class="bg" style="background-image:url('../_assets/_images/hero-equipment.svg');opacity:.5"></div><div class="wrap">
 <div class="crumbs"><a href="../index.html">Home</a><span>/</span><a href="../equipment.html">Equipment</a><span>/</span>{esc(full)}</div>
 <span class="eyebrow">{esc(p['brand'])}</span><h1>{esc(full)}{'' if p['brand'] in ('InHand','IDM Wireless') else ' ATM'}</h1><p class="lead">{esc(p['short'])}</p></div></div>
<section><div class="wrap"><div class="split" style="align-items:start">
 <img src="{img_url(p['img'],"../")}"{img_fallback(p['img'],"../")} alt="{esc(full)}" width="500" height="500" style="aspect-ratio:1;object-fit:contain;background:var(--sand);padding:1rem">
 <div class="prose">
  <p class="price" style="font-family:Manrope,sans-serif;font-size:1.6rem;font-weight:800;color:var(--navy);margin-bottom:.2rem">{price_html}</p>
  <p class="note">Includes free processing, free shipping &amp; handling (within the lower 48 states), real-time online stats, 2-year manufacturer's warranty, and 100% of the surcharge revenue.</p>
  <div class="btn-row" style="margin:1rem 0 1.5rem"><a class="btn btn-outline" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>{pdf}</div>
  <h2 style="margin-top:0">Product description</h2><p>{esc(p['desc'])}</p>{secs}
 </div>
</div></div></section>
<section class="alt"><div class="wrap"><h2>Specifications</h2><dl class="spec">{specs}</dl></div></section>
<section><div class="wrap"><div class="section-head"><h2>Other equipment</h2></div><div class="grid grid-4">{''.join(product_card(q,1) for q in PRODUCTS if q['slug']!=p['slug'] and q['brand']!='InHand')[:0]}{''.join(product_card(q,1) for q in [x for x in PRODUCTS if x['slug']!=p['slug']][:4])}</div></div></section>
{cta_band(1, h=f"Interested in the {esc(p['name'])}?", p="Tell us about your location and we'll quote the exact configuration, delivery, and setup.")}
"""
    PAGES.append(pg)


# ================================================================== CITY PAGES


def city_page(c):
    name=c["name"]; slug=c["slug"]; url=f"{BASE}/locations/{slug}.html"
    faq=[
     (f"Do you offer free ATM placement in {name}?", f"<p>Yes. Our free ATM placement program is available to qualifying businesses in {name} and throughout {c['region']}. We supply the machine, install it, load and manage the cash, and monitor it around the clock. You provide a standard 110v outlet, and we provide you with fair revenue share options.</p>"),
     (f"How quickly can you install an ATM in {name}?", f"<p>Most {name} installations are scheduled within days of approval. Tell us about your location and foot traffic, and we'll recommend the right machine and get it on the calendar.</p>"),
     (f"Can I buy an ATM for my {name} business instead?", f"<p>Yes. We sell Genmega and Nautilus Hyosung ATMs with free processing, programming, an Origin Wireless Router, free shipping and handling within the lower 48 states, real-time online reporting, a 2 year manufacturer's warranty, and 100% of the surcharge revenue. See our <a href=\"../equipment.html\">equipment page</a>.</p>"),
    ]+([(f"Do you service dispensaries in {name}?", f"<p>Yes. We're the largest cannabis ATM company in the country, and our dispensary ATMs are 100% compliant, with the dispensary's real name and address on customer bank statements. Learn more on our <a href=\"../dispensaries.html\">dispensary ATM page</a>.</p>")] if CANNABIS else [])
    nearby=" · ".join(f'<a href="{n}.html">{CITY_BY_SLUG[n]["name"]}</a>' for n in c["nearby"] if n in CITY_BY_SLUG)
    chips="".join(f"<span>{a}</span>" for a in c["areas"])
    pg={"path":f"locations/{slug}.html","depth":1,
        "title":f"Free ATM Placement in {name}, {ABBR} | {BRAND}",
        "desc":f"Free ATM placement and ATM sales in {name}, {STATE}. {BRAND} installs, cash-loads, and monitors ATMs in {name} bars, restaurants, hotels, {DISP_WORD}and retail at no cost. Call {PHONE_DISPLAY}.",
        "ld":[
          {"@context":"https://schema.org","@type":"Service","name":f"ATM placement in {name}, {ABBR}","serviceType":"ATM placement and ATM sales","url":url,
           "provider":{"@id":BASE+"/#business"},"areaServed":{"@type":"City","name":name,"containedInPlace":{"@type":"State","name":STATE}},
           "description":f"Free ATM placement, cash loading, monitoring, processing, and ATM sales for businesses in {name}, {STATE}."},
          faq_ld(faq),
          crumbs_ld([("Home","index.html"),("Free ATM Placement","atm-placement.html"),(f"{name}, {ABBR}",f"locations/{slug}.html")]),
        ]}
    pg["body"]=f"""
<div class="hero sub"><div class="bg" style="background-image:url('../_assets/_images/hero-skyline.svg');opacity:.5"></div><div class="wrap">
 <div class="crumbs"><a href="../index.html">Home</a><span>/</span><a href="../atm-placement.html">Free ATM Placement</a><span>/</span>{esc(name)}, {ABBR}</div>
 <span class="eyebrow">ATM placement · {esc(name)}, {STATE}</span><h1>Free ATM placement in {esc(name)}, {ABBR}</h1>
 <p class="lead">{BRAND} places, cash-loads, and services ATMs for businesses in {esc(name)} at no cost, and sells Genmega and Hyosung machines to owners who want to keep 100% of the surcharge. Part of the US ATM Experts network.</p>
 <div class="btn-row"><a class="btn btn-light" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div></div></div>
<div class="trust"><div class="wrap"><span>$0 install &amp; cash loading</span><span>Revenue share options</span><span>Local {esc(name)} service routes</span><span>Genmega &amp; Hyosung dealer</span></div></div>

<section><div class="wrap"><div class="split">
 <div>
  <span class="eyebrow">Serving {esc(name)}</span>
  <h2>An ATM company that knows {esc(name)}</h2>
  <p>{c['blurb']}</p>
  <p>Every {esc(name)} placement includes free installation, all the cash the machine needs, 24/7/365 monitoring, and a revenue share paid each month by the 10th of the following month. If you'd rather own your ATM, every machine we sell includes free processing, programming, and an Origin Wireless Router.</p>
  <ul class="checks">
   <li><strong>Free placement</strong> for bars, restaurants, hotels, {DISP_WORD}C-stores, salons, and more</li>
   <li><strong>Cash load prediction</strong> so {esc(name)} machines never run empty</li>
   <li><strong>Over 99% uptime</strong> with dedicated account support</li>
   <li><strong>ATM sales</strong> with 100% of the surcharge to you</li>
  </ul>
 </div>
 <img src="../_assets/_images/placement-locations.svg" alt="Business types that qualify for free ATM placement in {esc(name)}, {STATE}" width="1200" height="900" loading="lazy">
</div></div></section>

<section class="alt"><div class="wrap">
 <div class="section-head"><span class="eyebrow">Neighborhoods &amp; districts</span><h2>Where we place ATMs in {esc(name)}</h2><p class="lead">We serve all of {esc(name)}, including these areas.</p></div>
 <div class="areas">{chips}</div>
 <p class="note" style="margin-top:1.5rem">Nearby service areas: {nearby}</p>
</div></section>

<section><div class="wrap">
 <div class="section-head"><span class="eyebrow">How it works</span><h2>Free ATM placement in {esc(name)} in four steps</h2></div>
 <div class="steps">
  <div class="step"><h3>Tell us about your location</h3><p>Give us a call or reach out through the contact button on this page. We'll ask about foot traffic, hours, and space.</p></div>
  <div class="step"><h3>Site analysis</h3><p>We recommend the right machine, surcharge, and withdrawal limit for your {esc(name)} customers.</p></div>
  <div class="step"><h3>Free install &amp; cash load</h3><p>We deliver, install, and stock the ATM. You supply a standard 110v outlet.</p></div>
  <div class="step"><h3>Get paid monthly</h3><p>If you opt for a revenue share, you receive your split each month by the 10th of the following month.</p></div>
 </div>
 <p style="margin-top:1.5rem">See our <a href="../atm-placement.html#earnings">earnings estimates</a>, learn about <a href="../atm-processing.html">ATM processing</a>, or browse <a href="../equipment.html">ATMs for sale</a>.</p>
</div></section>

{faq_block(faq, title=f"{esc(name)} ATM FAQs")}
{cta_band(1, h=f"Get an ATM for your {esc(name)} business", p="Call us with your location details and we'll tell you whether it qualifies for free placement and what you can expect to earn.")}
"""
    return pg
for c in CITIES: PAGES.append(city_page(c))

# ================================================================== PRIVACY
pv = {"path":"privacy.html","title":f"Privacy Policy | {BRAND}","desc":f"How {BRAND} collects, uses, and protects information submitted through {DOMAIN}.","ld":[]}
pv["body"] = f"""<section><div class="wrap prose">
<span class="eyebrow">Legal</span><h1>Privacy Policy</h1><p class="note">Effective date: July 12, 2018 · Last reviewed: {TODAY}</p>
<p>{BRAND} ("us", "we", or "our") operates the www.{DOMAIN} website (the "Service"). This page informs you of our policies regarding the collection, use, and disclosure of personal data when you use our Service and the choices you have associated with that data.</p>
<h2>Information we collect</h2>
<p>When you contact us we may ask you to provide personally identifiable information that can be used to contact or identify you, including your email address, first and last name, phone number, and business address or location details. We also collect usage data such as your IP address, browser type and version, the pages you visit, the time and date of your visit, and other diagnostic data, through cookies and similar technologies.</p>
<h2>How we use your information</h2>
<ul><li>To provide and maintain the Service</li><li>To respond to your inquiry and provide a quote</li><li>To notify you about changes to our Service</li><li>To allow you to participate in interactive features of our Service</li><li>To provide customer support and gather analysis so we can improve the Service</li><li>To monitor the usage of the Service and detect, prevent, and address technical issues</li></ul>
<h2>SMS communications</h2>
<p>If you consent to receive SMS messages, we may text you about your inquiry. Message and data rates may apply and message frequency will vary. Reply STOP to opt out at any time. <strong>No mobile information will be shared with third parties or affiliates for marketing or promotional purposes.</strong></p>
<h2>Security of data</h2>
<p>The security of your data is important to us, but remember that no method of transmission over the Internet or method of electronic storage is 100% secure. While we strive to use commercially acceptable means to protect your personal data, we cannot guarantee its absolute security.</p>
<h2>Service providers and analytics</h2>
<p>We use third-party services to operate the Service, including form handling and Google Analytics / Google Ads, which may collect usage data. You can opt out of Google Analytics by installing the Google Analytics opt-out browser add-on.</p>
<h2>Transfer of data</h2>
<p>Your information may be transferred to and maintained on computers located in the United States. We will take all steps reasonably necessary to ensure that your data is treated securely and that adequate controls are in place, including the security of your data.</p>
<h2>Children's privacy</h2>
<p>Our Service does not address anyone under the age of 18, and we do not knowingly collect personally identifiable information from anyone under 18.</p>
<h2>Changes to this policy</h2>
<p>We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and, where appropriate, via email or a prominent notice on our Service prior to the change becoming effective.</p>
<h2>Contact us</h2>
<p>Questions about this Privacy Policy? Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
</div></section>"""
PAGES.append(pv)

# ================================================================== 404
nf = {"path":"404.html","title":f"Page Not Found | {BRAND}","desc":f"That page doesn't exist. Find ATM placement, processing, and equipment from {BRAND}.","ld":[],"noindex":True}
nf["body"] = """<section><div class="wrap center" style="max-width:640px;padding:4rem 20px"><span class="eyebrow">404</span><h1>We couldn't find that page</h1><p class="lead">It may have moved. Try one of these instead.</p><div class="btn-row" style="justify-content:center;margin-top:1.5rem"><a class="btn btn-primary" href="/atm-placement.html">Free ATM placement</a><a class="btn btn-outline" href="/atm-processing.html">ATM processing</a><a class="btn btn-outline" href="/equipment.html">Equipment</a></div></div></section>"""
PAGES.append(nf)

# ================================================================== WRITE
os.makedirs(os.path.join(OUT,"css"),exist_ok=True)
os.makedirs(os.path.join(OUT,"js"),exist_ok=True)
os.makedirs(os.path.join(OUT,"product_pages"),exist_ok=True)
os.makedirs(os.path.join(OUT,"locations"),exist_ok=True)
open(os.path.join(OUT,"css","styles.css"),"w").write(recolor(CSS.strip())+"\n")
open(os.path.join(OUT,"js","main.js"),"w").write(JS.strip()+"\n")
for p in PAGES:
    d = p.get("depth",0)
    h = head(p,d)
    if p.get("noindex"): h = h.replace('content="index, follow, max-image-preview:large"','content="noindex, follow"')
    open(os.path.join(OUT,p["path"]),"w").write(h+p["body"]+foot(d))

urls = [p for p in PAGES if not p.get("noindex")]
def prio(path):
    return "1.0" if path=="index.html" else "0.9" if path in ("atm-placement.html","dispensaries.html") else "0.8" if path in ("equipment.html","atm-processing.html",) else "0.7" if path.startswith("locations") else "0.6" if path.startswith("product_pages") else "0.3"
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{BASE}/{'' if p['path']=='index.html' else p['path']}</loc><lastmod>{TODAY}</lastmod><priority>{prio(p['path'])}</priority></url>\n" for p in urls) + "</urlset>\n"
open(os.path.join(OUT,"sitemap.xml"),"w").write(sm)
open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
open(os.path.join(OUT,".htaccess"),"w").write(f"""# {BRAND} — Apache config (safe to delete if your host isn't Apache)
RewriteEngine On
# Force https + www
RewriteCond %{{HTTPS}} off [OR]
RewriteCond %{{HTTP_HOST}} ^{DOMAIN_RE}$ [NC]
RewriteRule ^(.*)$ https://www.{DOMAIN}/$1 [R=301,L]
# Retired pages
Redirect 301 /events.html /atm-placement.html
Redirect 301 /product_pages/inhand_i22_dual.html /product_pages/idm_origin.html
Redirect 301 /contact.html /
Redirect 301 /thank-you.html /
# Custom 404
ErrorDocument 404 /404.html
# Cache static assets
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
</IfModule>
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml
</IfModule>
""")
# ---- assets: copy shared illustrations, recolor, and localize text
SRC=os.path.join(os.path.dirname(os.path.abspath(__file__)),"site","_assets","_images")
DST=os.path.join(OUT,"_assets","_images"); os.makedirs(DST,exist_ok=True)
want=["hero-storefronts.svg","hero-skyline.svg","hero-processing.svg","hero-equipment.svg","placement-locations.svg","daily-vault-cash-deposits.svg","real-time-reporting.svg"]+(["dispensary-hero.svg","dispensary-bank-statement.svg"] if CANNABIS else [])
c2=AREAS[1] if len(AREAS)>1 else METRO; c3=AREAS[2] if len(AREAS)>2 else METRO; c4=AREAS[3] if len(AREAS)>3 else METRO
for n in want:
    t=open(os.path.join(SRC,n)).read()
    t=recolor(t)
    t=t.replace("Arizona ATM Experts",BRAND).replace("1234 N Central Ave","1234 Main St").replace("1234 N CENTRAL AVE","1234 MAIN ST")
    t=t.replace("Phoenix, AZ 85004",f"{METRO}, {ABBR}").replace("PHOENIX AZ 85004",f"{METRO.upper()} {ABBR}").replace("PHOENIX, AZ 85004",f"{METRO.upper()}, {ABBR}").replace("Phoenix AZ",f"{METRO} {ABBR}").replace("PHOENIX AZ",f"{METRO.upper()} {ABBR}")
    t=t.replace("Tempe AZ",f"{c2} {ABBR}").replace("Mesa AZ",f"{c3} {ABBR}").replace("Scottsdale AZ",f"{c4} {ABBR}").replace("Phoenix",METRO)
    if n=="placement-locations.svg" and not CANNABIS: t=t.replace(">DISPENSARY<",">SMOKE SHOP<").replace('fill="#6fae6b"','fill="'+_mix(P,.22)+'"')
    open(os.path.join(DST,n),"w").write(t)
# service map (generic, per state)
pins=CITIES[:8]; pos=[(560,300),(700,380),(480,440),(640,520),(760,250),(420,330),(700,600),(520,600)]
pinsvg="".join(f'<use href="#pin" transform="translate({x},{y})"/><text x="{x+20}" y="{y-28}">{esc(c["name"])}</text>' for c,(x,y) in zip(pins,pos))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" role="img" aria-labelledby="t"><title id="t">{esc(STATE)} ATM service areas</title>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f7f4ee"/><stop offset="1" stop-color="#ece6da"/></linearGradient><filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="{P}" flood-opacity=".18"/></filter>
<g id="pin"><path d="M0 0 C-16 -22 -22 -32 -22 -44 A22 22 0 1 1 22 -44 C22 -32 16 -22 0 0Z" fill="{A}"/><circle cx="0" cy="-44" r="9" fill="#fff"/></g></defs>
<rect width="1200" height="900" fill="url(#bg)"/><circle cx="1020" cy="150" r="130" fill="{H}" opacity=".18"/>
<g filter="url(#sh)"><path d="M340 160 C 520 90, 760 110, 880 200 C 960 270, 940 420, 900 540 C 860 660, 720 740, 560 720 C 400 700, 300 600, 320 460 C 335 360, 300 250, 340 160 Z" fill="{P}"/><path d="M360 180 C 530 120, 745 135, 858 215 C 930 275, 915 415, 878 530 C 840 645, 712 718, 566 700 C 415 682, 322 590, 340 462 C 354 366, 322 262, 360 180 Z" fill="{_mix(P,.10)}"/></g>
<g fill="#ffffff" font-family="Inter,Arial" font-size="15" font-weight="600">{pinsvg}</g>
<g filter="url(#sh)"><rect x="70" y="620" width="330" height="140" rx="18" fill="#fff"/><text x="94" y="656" fill="#5b6172" font-family="Inter,Arial" font-size="12" font-weight="700" letter-spacing="1.5">SERVICE AREA</text><text x="94" y="694" fill="{P}" font-family="Inter,Arial" font-size="24" font-weight="800">All of {esc(STATE)}</text><text x="94" y="724" fill="#5b6172" font-family="Inter,Arial" font-size="14">Placed, cash-loaded, and serviced</text></g>
<g filter="url(#sh)"><rect x="880" y="560" width="250" height="200" rx="18" fill="#fff"/><text x="904" y="596" fill="#5b6172" font-family="Inter,Arial" font-size="12" font-weight="700" letter-spacing="1.5">PART OF</text><text x="904" y="640" fill="{A}" font-family="Inter,Arial" font-size="26" font-weight="800">US ATM Experts</text><text x="904" y="676" fill="{P}" font-family="Inter,Arial" font-size="15" font-weight="700">Nationwide network</text><text x="904" y="700" fill="#5b6172" font-family="Inter,Arial" font-size="14">Local {esc(STATE)} service</text></g>
</svg>'''
open(os.path.join(DST,"service-map.svg"),"w").write(svg)
print(f"Built {len(PAGES)} pages into {OUT}")



# ---- ship shared assets locally (everything present in site/_assets/_images/_atm_images, _pdf, and this state's puck) ----
for sub in (("_images/_atm_images","_pdf") if SHIP_PDFS else ("_images/_atm_images",)):
    sd=os.path.join(SRC_ASSETS,sub)
    if os.path.isdir(sd):
        dd=os.path.join(OUT,"_assets",sub); os.makedirs(dd,exist_ok=True)
        for f in os.listdir(sd): shutil.copy(os.path.join(sd,f),os.path.join(dd,f))
if LOGO_LOCAL:
    dd=os.path.join(OUT,"_assets","_images","_state_logo"); os.makedirs(dd,exist_ok=True)
    shutil.copy(os.path.join("site/_assets/_images/_state_logo",LOGO_FILE),os.path.join(dd,LOGO_FILE))
