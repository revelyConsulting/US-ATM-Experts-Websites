"""Derive build_us.py (usatmexperts.com hub) from build_state.py."""
import re
s = open('build_state.py').read()
fails = []
def rep(old, new, count=1):
    global s
    if old not in s: fails.append(old[:90]); return
    s = s.replace(old, new, count)

# ---------- config: no JSON needed
rep('CFG = json.load(open(sys.argv[1]))\nPAL = CFG["palette"]',
    'CFG = {"name":"the United States","abbr":"US","metro_city":"America","metro_phrase":"every major metro","span_phrase":"from coast to coast","seasonal_phrase":"tourist seasons, sports schedules, and regional holidays","cities":[],"cannabis":True,"palette":{"primary":"#002868","accent":"#bf0a30","highlight":"#f4f4f4"}}\nPAL = CFG["palette"]')
rep('OUT = sys.argv[2]', 'OUT = sys.argv[1] if len(sys.argv)>1 else "multistate/usatmexperts.com"')
rep('BRAND = f"{STATE} ATM Experts"', 'BRAND = "US ATM Experts"')

# ---------- nav: add Partners
rep(']+([("Dispensaries","dispensaries.html")] if CANNABIS else [])+[',
    ']+([("Dispensaries","dispensaries.html")] if CANNABIS else [])+[("Partners","partners.html")]+[')

# ---------- national phrasing
rep('<div class="social">Serving all of {STATE}</div>', '<div class="social">Serving all 50 states</div>')
rep('<small>Serving all of {STATE}</small>', '<small>Serving all 50 states</small>')
rep('<p>{BRAND} is part of the US ATM Experts network, providing free ATM placement, ATM processing, and equipment sales for {STATE} businesses.</p>',
    '<p>{BRAND} is the national ATM company behind the ATM Experts network in all 50 states: free ATM placement, ATM processing, equipment sales, and a vaulting partner program for independent operators.</p>')
rep('<li>Serving all of {STATE}</li>', '<li>Serving all 50 states</li>')
rep('<span class="eyebrow">Part of US ATM Experts · Serving all of {STATE}</span>', '<span class="eyebrow">National ATM company · Serving all 50 states</span>')
rep("<h1>{STATE}'s ATM company for free ATM placement and ATM sales</h1>", "<h1>America's ATM company for free ATM placement and ATM sales</h1>")
rep('<span>Serving all of {STATE}</span><span>Genmega & Hyosung authorized dealer</span><span>Trusted by {STATE} hospitality &amp; ret',
    '<span>Serving all 50 states</span><span>Genmega & Hyosung authorized dealer</span><span>Trusted by hospitality &amp; ret')
rep('(f"How do I find a reliable ATM company near me in {STATE}?", f"<p>Look for a company that owns its routes, loads its own cash, and answers the phone. {BRAND} is part of the US ATM Experts network, places and services ATMs across {STATE}, and is an authorized Genmega and Nautilus Hyosung dealer. Call {PHONE_DISPLAY} and you\'ll reach our team.</p>"),',
    '("How do I find a reliable ATM company near me?", f"<p>Look for a company that owns its routes, loads its own cash, and answers the phone. {BRAND} places and services ATMs in all 50 states through local ATM Experts teams and vaulting partners, and is an authorized Genmega and Nautilus Hyosung dealer. Call {PHONE_DISPLAY} and you\'ll reach our team.</p>"),')
rep('(f"What areas of {STATE} do you serve?", f"<p>All of it. We serve {METRO_PHRASE} and communities {SPAN}, including {\', \'.join(AREAS[:-1])}, and {AREAS[-1]}.</p>"),',
    '("What areas do you serve?", "<p>All 50 states. Each state has its own ATM Experts site and local service routes; find yours on the <a href=\\"states.html\\">state directory</a>.</p>"),')
rep('"title":f"{STATE} ATM Company | Free ATM Placement & Sales | {METRO}",', '"title":"US ATM Experts | Free ATM Placement, Processing & ATM Sales Nationwide",')
rep('<p>{BRAND} is trusted across {STATE} by business owners', '<p>{BRAND} is trusted in all 50 states by business owners')
rep('<a href="atm-placement.html">free ATM placement</a> in {METRO}, {DISP_LINK_HOME}', '<a href="atm-placement.html">free ATM placement</a> anywhere in the country, {DISP_LINK_HOME}')
rep('for your business, one {STATE} team handles it.</p>', 'for your business, one national team handles it.</p>')
rep('alt="{STATE} ATM service areas including {", ".join(AREAS[:6])}"', 'alt="US ATM Experts service area: all 50 states"')
rep('f"<p>At setup we analyze your location to determine the best surcharge and maximum withdrawal amount for your customers. Most {STATE} locations run between $3.50 and $4.00.</p>"',
    '"<p>At setup we analyze your location to determine the best surcharge and maximum withdrawal amount for your customers. Most locations run between $3.50 and $4.00.</p>"')
rep('(f"Do you offer ATM placement near me in {STATE}?", f"<p>If your business is in {STATE}, almost certainly yes. We run regular routes through {\', \'.join(AREAS[:-1])}, and {AREAS[-1]}. See our " + TOP_LINKS + " pages, or call and ask about your city.</p>"),',
    '("Do you offer ATM placement near me?", "<p>Almost certainly yes. We place ATMs in all 50 states through local ATM Experts teams and vaulting partners. Find your state on the <a href=\\"states.html\\">state directory</a>, or call and ask about your city.</p>"),')
rep('"title":f"Free ATM Placement in {METRO} & {STATE} | {BRAND}",', '"title":"Free ATM Placement Nationwide | US ATM Experts",')
rep('"desc":f"Get a free ATM at your {STATE} bar, restaurant, hotel, or store. We install, load the cash, and monitor it at no cost — you earn a monthly surcharge share. {METRO} & statewide.",',
    '"desc":"Get a free ATM at your bar, restaurant, hotel, or store anywhere in the United States. We install, load the cash, and monitor it at no cost — you earn a monthly surcharge share.",')
rep('f"Turnkey ATM placement program for {STATE} businesses at no cost', 'f"Turnkey ATM placement program for businesses in all 50 states at no cost')
rep('sub_hero(pl,f"Free ATM placement in {STATE}",f"Free ATM placement for {METRO} and {STATE} businesses — installed, stocked, and monitored by us"',
    'sub_hero(pl,"Free ATM placement nationwide","Free ATM placement for businesses in all 50 states — installed, stocked, and monitored by us"')
rep("<p>We've placed machines everywhere from {METRO} bars to small-town city halls.", "<p>We've placed machines everywhere from big-city bars to small-town city halls.")
rep('<div class="card"><h3>Local cash routes, not a call center</h3><p>We run our own cash and service routes across {STATE}, {SPAN}. When a machine needs attention, a technician who covers your area handles it — backed by the resources of the US ATM Experts network.</p></div>',
    '<div class="card"><h3>Local cash routes, not a call center</h3><p>We run cash and service routes in every state through our local ATM Experts teams and vetted vaulting partners. When a machine needs attention, a technician who covers your area handles it — backed by a national company.</p></div>')
rep('<div class="card"><h3>Built for {STATE} traffic patterns</h3><p>{SEASONAL[0].upper()+SEASONAL[1:]} all change',
    '<div class="card"><h3>Built for local traffic patterns</h3><p>Tourist seasons, sports schedules, and regional holidays all change')
rep('{areas_block(heading=f"Free ATM placement across {STATE}")}', '{states_block(heading="Free ATM placement in every state")}')
rep('(f"Do you serve dispensaries outside {METRO}?", f"<p>Yes. We place and service dispensary ATMs across {STATE}, including {\', \'.join(AREAS[1:6])}, and {METRO_PHRASE}.</p>"),',
    '("Which states do you serve dispensaries in?", "<p>Every state with legal cannabis retail — recreational or medical. Each of those states has a dispensary page on its ATM Experts site; find yours on the <a href=\\"states.html\\">state directory</a>.</p>"),')
rep('{areas_block(heading=f"Dispensary ATMs across {STATE}")}', '{states_block(heading="Dispensary ATMs in every legal state")}')
rep('"title":f"ATM Machines for Sale in {STATE} | Genmega & Hyosung Dealer",', '"title":"ATM Machines for Sale | Genmega & Hyosung Dealer | US ATM Experts",')
rep('"desc":f"ATM machines for sale in {METRO} and across {STATE}: Genmega', '"desc":f"ATM machines for sale nationwide: Genmega')
rep('sub_hero(eq,f"ATM sales in {STATE}",f"Buy an ATM in {STATE} and keep 100% of the surcharge",f"{BRAND} is an authorized Genmega and Nautilus Hyosung dealer serving {METRO} and all of {STATE}.',
    'sub_hero(eq,"ATM sales nationwide","Buy an ATM and keep 100% of the surcharge",f"{BRAND} is an authorized Genmega and Nautilus Hyosung dealer shipping to all 50 states.')
rep('{areas_block()}', '{states_block()}')

# ---------- footer: replace city column with popular states
rep('''def footer_cities(r):
    out=[]; cs=CITIES[:12]
    for i in range(0,len(cs),3):
        out.append("<li>"+" · ".join(f'<a href="{r}locations/{c["slug"]}.html">{c["name"]}</a>' for c in cs[i:i+3])+"</li>")
    return "\\n   ".join(out)''',
'''POPULAR = ["CA","TX","FL","NY","AZ","IL","PA","OH","GA","NC","MI","WA"]
def footer_cities(r):
    out=[]
    for i in range(0,len(POPULAR),3):
        out.append("<li>"+" · ".join(f'<a href="https://www.{ab.lower()}atmexperts.com/">{STATE_NAMES[ab]}</a>' for ab in POPULAR[i:i+3])+"</li>")
    out.append(f'<li><a href="{r}states.html">All 50 states →</a></li>')
    return "\\n   ".join(out)''')
rep('<div><h4>Service areas</h4><ul>', '<div><h4>State sites</h4><ul>')
# footer_cities uses STATE_NAMES defined later; move STATE_NAMES up by defining early
m = re.search(r'\nSTATE_NAMES = \{.*?\}\n', s, re.S)
names_line = m.group(0)
s = s.replace(names_line, '\n', 1)
rep('CITIES = CFG["cities"]', names_line.strip() + '\nCITIES = CFG["cities"]')

# ---------- states_block replaces areas_block
rep('def areas_block(depth=0, heading=None):',
'''def states_block(depth=0, heading=None):
    heading = heading or "Serving businesses in all 50 states"
    r = rel(depth)
    chips = "".join(f'<a href="https://www.{ab.lower()}atmexperts.com/" style="text-decoration:none"><span>{n}</span></a>' for ab,n in sorted(STATE_NAMES.items(), key=lambda x:x[1]))
    return f"""<section class="alt"><div class="wrap"><div class="section-head"><span class="eyebrow">Service area</span><h2>{heading}</h2><p class="lead">Every state has its own ATM Experts team and website. Pick yours for local service areas, city pages, and state-specific programs.</p></div><div class="areas">{chips}</div></div></section>"""
def areas_block(depth=0, heading=None):''')

# ---------- schema: country-wide
rep('"areaServed":[{"@type":"State","name":STATE}]+[{"@type":"City","name":a} for a in AREAS],', '"areaServed":[{"@type":"Country","name":"United States"}],')
rep('"@id":BASE+"/#business","parentOrganization":{"@type":"Organization","name":"US ATM Experts","url":"https://www.usatmexperts.com/"},', '"@id":BASE+"/#business",')

# ---------- no city pages
rep('for c in CITIES: PAGES.append(city_page(c))', 'pass  # no city pages on the national hub')

# ---------- SVG localization: use big cities on the bank-statement graphic
rep('c2=AREAS[1] if len(AREAS)>1 else METRO; c3=AREAS[2] if len(AREAS)>2 else METRO; c4=AREAS[3] if len(AREAS)>3 else METRO',
    'METRO="Denver"; ABBR_SVG="CO"; c2="Austin"; c3="Chicago"; c4="Seattle"')
rep('.replace("Phoenix, AZ 85004",f"{METRO}, {ABBR}").replace("PHOENIX AZ 85004",f"{METRO.upper()} {ABBR}").replace("PHOENIX, AZ 85004",f"{METRO.upper()}, {ABBR}").replace("Phoenix AZ",f"{METRO} {ABBR}").replace("PHOENIX AZ",f"{METRO.upper()} {ABBR}")',
    '.replace("Phoenix, AZ 85004",f"{METRO}, {ABBR_SVG}").replace("PHOENIX AZ 85004",f"{METRO.upper()} {ABBR_SVG}").replace("PHOENIX, AZ 85004",f"{METRO.upper()}, {ABBR_SVG}").replace("Phoenix AZ",f"{METRO} {ABBR_SVG}").replace("PHOENIX AZ",f"{METRO.upper()} {ABBR_SVG}")')
rep('.replace("Tempe AZ",f"{c2} {ABBR}").replace("Mesa AZ",f"{c3} {ABBR}").replace("Scottsdale AZ",f"{c4} {ABBR}").replace("Phoenix",METRO)',
    '.replace("Tempe AZ",f"{c2} TX").replace("Mesa AZ",f"{c3} IL").replace("Scottsdale AZ",f"{c4} WA").replace("Phoenix",METRO)')
rep('pins=CITIES[:8]; pos=', 'pins=[{"name":n} for n in ["Seattle","Denver","Chicago","New York","Los Angeles","Dallas","Atlanta","Miami"]]; pos=')
rep('<title id="t">{esc(STATE)} ATM service areas</title>', '<title id="t">US ATM Experts service area: all 50 states</title>')

open('build_us.py','w').write(s)
print("unmatched:", len(fails)); [print("  -", f) for f in fails]

# ---------- second pass: remaining phrases
s = open('build_us.py').read(); fails = []
rep('"alternateName":f"{ABBR} ATM Experts"', '"alternateName":"United States ATM Experts"')
rep('"description":f"Free ATM placement, ATM processing, and ATM sales for businesses across {STATE}. Part of the US ATM Experts network.",', '"description":"Free ATM placement, ATM processing, ATM sales, and a vaulting partner program for independent operators — in all 50 states.",')
rep('"slogan":f"Free ATM placement, processing, and sales across {STATE}",', '"slogan":"Free ATM placement, processing, and sales in all 50 states",')
rep('"areaServed":f"US-{ABBR}"', '"areaServed":"US"')
rep('"desc":f"{BRAND} offers free ATM placement, ATM processing, and Genmega & Hyosung ATM sales across {STATE}. Part of the US ATM Experts network. Call {PHONE_DISPLAY}.",', '"desc":f"{BRAND} offers free ATM placement, ATM processing, and Genmega & Hyosung ATM sales in all 50 states, plus a vaulting partner program for ATM operators. Call {PHONE_DISPLAY}.",')
rep('<h2>ATM solutions for {STATE} businesses</h2>', '<h2>ATM solutions for businesses in every state</h2>')
rep('<h2>The best {STATE} locations for a placed ATM</h2>', '<h2>The best locations for a placed ATM</h2>')
rep('<span class="eyebrow">Local expertise</span><h2>Why {STATE} businesses choose {BRAND}</h2>', '<span class="eyebrow">National reach, local service</span><h2>Why businesses choose {BRAND}</h2>')
rep('"title":f"Dispensary ATMs in {STATE} | Compliant Cannabis ATM Placement",', '"title":"Dispensary ATMs Nationwide | Compliant Cannabis ATM Placement",')
rep('"desc":f"100% compliant ATMs for {STATE} dispensaries.', '"desc":"100% compliant ATMs for dispensaries in every legal state.')
rep('for cannabis dispensaries in {STATE}, with', 'for cannabis dispensaries nationwide, with')
rep('f"100% compliant ATMs for {STATE} dispensaries"', '"100% compliant ATMs for dispensaries nationwide"')
rep('"title":f"ATM Processing for {STATE} ATM Owners | {BRAND}",', '"title":"ATM Processing for ATM Owners Nationwide | US ATM Experts",')
rep('included with every ATM we sell or place in {STATE}.', 'included with every ATM we sell or place, in all 50 states.')
rep('for ATM owners in {STATE}."', 'for ATM owners in all 50 states."')
rep('f"{STATE} ATM processing with daily vault cash deposits and real-time reporting"', '"ATM processing with daily vault cash deposits and real-time reporting"')
rep('>All of {esc(STATE)}</text>', '>All 50 states</text>')
rep('>Local {esc(STATE)} service</text>', '>Local teams + vaulting partners</text>')
rep('<text x="904" y="596" fill="#5b6172" font-family="Inter,Arial" font-size="12" font-weight="700" letter-spacing="1.5">PART OF</text>', '<text x="904" y="596" fill="#5b6172" font-family="Inter,Arial" font-size="12" font-weight="700" letter-spacing="1.5">NATIONAL HQ</text>')

# ---------- Partners + States pages, inserted before the render loop
NEW_PAGES = r'''
# ================= STATE DIRECTORY =================
_regions = {
 "West": ["AK","AZ","CA","CO","HI","ID","MT","NV","NM","OR","UT","WA","WY"],
 "Midwest": ["IL","IN","IA","KS","MI","MN","MO","NE","ND","OH","SD","WI"],
 "South": ["AL","AR","DE","FL","GA","KY","LA","MD","MS","NC","OK","SC","TN","TX","VA","WV"],
 "Northeast": ["CT","ME","MA","NH","NJ","NY","PA","RI","VT"],
}
_cannabis_states = {"CA","CO","WA","OR","NV","NM","MI","IL","MA","ME","VT","NJ","NY","CT","RI","DE","MD","VA","MO","OH","MN","MT","AK","HI","OK","AR","FL","PA","LA","MS","WV","KY","UT","ND","SD","NH","AZ"}
def _state_cards(abbrs):
    out=[]
    for ab in sorted(abbrs, key=lambda a: STATE_NAMES[a]):
        n=STATE_NAMES[ab]; u=f"https://www.{ab.lower()}atmexperts.com/"
        disp = f' · <a href="{u}dispensaries.html">Dispensaries</a>' if ab in _cannabis_states else ""
        out.append(f'<div class="card"><span class="eyebrow" style="margin-bottom:.2rem">{ab}</span><h3><a href="{u}" style="text-decoration:none;color:inherit">{n} ATM Experts</a></h3><p style="margin:0;font-size:.95rem"><a href="{u}atm-placement.html">Free placement</a> · <a href="{u}equipment.html">Buy an ATM</a>{disp}</p></div>')
    return "".join(out)
_region_sections = "".join(f'<h2 style="margin-top:2.5rem">{reg}</h2><div class="grid grid-4">{_state_cards(abs_)}</div>' for reg,abs_ in _regions.items())
st = {
 "path":"states.html",
 "title":"ATM Experts by State | Free ATM Placement in All 50 States",
 "desc":"Find your state's ATM Experts team. Free ATM placement, ATM processing, ATM sales, and compliant dispensary ATMs in all 50 states, backed by US ATM Experts.",
 "ld":[crumbs_ld([("Home","index.html"),("State directory","states.html")]),
       {"@context":"https://schema.org","@type":"ItemList","name":"ATM Experts state sites","itemListElement":[{"@type":"ListItem","position":i+1,"name":f"{STATE_NAMES[ab]} ATM Experts","url":f"https://www.{ab.lower()}atmexperts.com/"} for i,ab in enumerate(sorted(STATE_NAMES, key=lambda a: STATE_NAMES[a]))]}],
}
st["body"] = sub_hero(st,"State directory","ATM Experts in all 50 states","Every state has its own ATM Experts team, website, city service pages, and local cash routes. Pick your state to get started, or call the national line and we'll connect you.","hero-skyline.svg",crumbs=[("State directory",None)]) + f"""
<section><div class="wrap">
 <div class="section-head"><span class="eyebrow">Find your state</span><h2>One company, fifty local teams</h2><p class="lead">The same free placement program, free processing, Genmega and Hyosung equipment, and dispensary compliance in every state — with local technicians and vaulting partners who know your area.</p></div>
 {_region_sections}
</div></section>
{cta_band(h="Not sure which team to call?", p="Call the national line. We'll route you to the right state team the same day.")}
"""
PAGES.append(st)

# ================= PARTNERS =================
PA_FAQ = [
 ("Is this a franchise?", "<p>No. There are no franchise fees, territory purchases, or royalties. You keep operating your own business; we hand you locations to vault under the US ATM Experts name and share the surcharge with you.</p>"),
 ("Do I need to already operate ATMs?", "<p>Yes. The program is built for established independent ATM operators who already run a route, carry their own vault cash, and have the insurance and processes that go with it.</p>"),
 ("Who supplies the vault cash?", "<p>You do. You fund the cassettes on the locations assigned to you, and your cash is returned to your bank account through daily vault-cash deposits as customers withdraw it.</p>"),
 ("How am I paid?", "<p>You earn a share of the surcharge on every withdrawal at the locations you vault, paid monthly with a full transaction report. Reach out for current partner rates.</p>"),
 ("Who owns the machine and the location agreement?", "<p>US ATM Experts holds the location agreement. You provide and install the ATM, and you vault it. Repairs are your responsibility. If a repair calls for parts, we can supply them at a discounted rate.</p>"),
 ("How many locations will I get?", "<p>It depends on your market and capacity. Most partners start with a handful of locations near their existing route and grow from there as our placement team signs new sites in their area.</p>"),
 ("What if a machine breaks?", "<p>Repairs are your responsibility, the same as the machines already on your route. We can supply any parts you need at a discounted rate, and our national team and your dedicated account rep back you on technical support and processing issues.</p>"),
 ("How quickly do I get started?", "<p>Once you're approved, onboarding is a matter of days: we set you up on our reporting platform, assign your first locations, and schedule the cash loads.</p>"),
]
pa = {
 "path":"partners.html",
 "title":"ATM Vaulting Partner Program | US ATM Experts",
 "desc":"Independent ATM operators: add revenue by vaulting US ATM Experts locations in your area. We sign the locations; you place your machine, supply and load the cash, and earn a surcharge share. Not a franchise.",
 "ld":[service_ld("ATM vaulting partner program", BASE+"/partners.html","Revenue-share program for independent ATM operators who vault and service US ATM Experts placement locations in their market."), faq_ld(PA_FAQ), crumbs_ld([("Home","index.html"),("Partners","partners.html")])],
}
pa["body"] = sub_hero(pa,"Vaulting partner program","Add revenue to your ATM route by vaulting our locations","US ATM Experts is looking for established independent ATM operators in every state. We sign the locations. You place your own machine, supply and load the cash, and keep it running — and earn a share of every surcharge. No franchise fees, no royalties.","hero-storefronts.svg",crumbs=[("Partners",None)]) + f"""
<div class="trust"><div class="wrap"><span>Not a franchise</span><span>Locations handed to you</span><span>Free processing</span><span>Monthly surcharge share</span><span>Real-time reporting</span></div></div>

<section><div class="wrap"><div class="split">
 <div>
  <span class="eyebrow">How it works</span>
  <h2>More locations on your route, without the sales work</h2>
  <p>You already have the hard part figured out: the cash, the vehicle, the route, the discipline to keep machines full. What limits most independent operators is finding and signing new locations. That's what we do all day, in all 50 states.</p>
  <p>As a vaulting partner, you take on locations US ATM Experts has signed near your existing route. You install one of your own machines, fund and load the cash, and handle service and repairs. We handle the location agreement, processing, reporting, and support. You're paid a share of the surcharge on every withdrawal.</p>
  <ul class="checks">
   <li><strong>You keep your business.</strong> No franchise fees, territory purchases, or royalties.</li>
   <li><strong>Locations come to you.</strong> Our placement team signs the sites; you install your machine and vault it.</li>
   <li><strong>Your cash comes back daily.</strong> Vault cash is deposited to your account as it's withdrawn.</li>
   <li><strong>You're paid monthly.</strong> Surcharge share plus a full transaction report.</li>
   <li><strong>Discounted parts.</strong> Repairs are on you, but parts come at our dealer-discounted rate.</li>
  </ul>
 </div>
 <img src="_assets/_images/daily-vault-cash-deposits.svg" alt="Cash loaded by a vaulting partner is returned through daily vault deposits" width="1200" height="900" loading="lazy">
</div></div></section>

<section class="alt"><div class="wrap">
 <div class="section-head"><span class="eyebrow">Step by step</span><h2>From application to first payout</h2></div>
 <div class="steps">
  <div class="step"><h3>Apply</h3><p>Call {PHONE_DISPLAY} or email us. We'll ask about your current route, your market, how much cash you can put to work, and your capacity for additional stops.</p></div>
  <div class="step"><h3>Onboarding</h3><p>Once approved, we set you up on our real-time reporting platform and cash-load prediction tools, and introduce you to your dedicated account rep.</p></div>
  <div class="step"><h3>Assigned locations</h3><p>We hand you signed locations near your route. You install your machine, fund the cassette, and schedule the first load; we handle the location relationship and processing.</p></div>
  <div class="step"><h3>Load, service, get paid</h3><p>Keep the machines full and running, with discounted parts from us when a repair calls for them. Vault cash comes back daily, and your surcharge share is paid each month by the 10th of the following month.</p></div>
 </div>
</div></section>

<section><div class="wrap"><div class="split">
 <img src="_assets/_images/real-time-reporting.svg" alt="Real-time reporting dashboard showing cash remaining and surcharge revenue" width="1200" height="900" loading="lazy">
 <div>
  <span class="eyebrow">What you get</span>
  <h2>The tools of a national operator, on your route</h2>
  <ul class="checks">
   <li><strong>Signed locations</strong> — agreements in place and ready for your machine, handed to you as they come online in your area.</li>
   <li><strong>Free processing</strong> on every partner location, with competitive interchange.</li>
   <li><strong>Daily vault cash deposits</strong> so your money isn't sitting in a cassette longer than it has to.</li>
   <li><strong>Real-time online reporting</strong> — cash remaining, withdrawals, and surcharge revenue on every machine, from your phone.</li>
   <li><strong>Low-cash alerts and cash-load prediction</strong> that learn each location's pattern so you're not making unnecessary trips.</li>
   <li><strong>A dedicated account rep</strong> and national technical support behind you.</li>
   <li><strong>Equipment and parts discounts</strong> on Genmega and Hyosung machines, wireless modems, and any repair parts you need for partner locations.</li>
   <li><strong>Name recognition</strong> — locations see a national brand with a track record, which makes every renewal easier.</li>
  </ul>
 </div>
</div></div></section>

<section class="alt"><div class="wrap">
 <div class="section-head"><span class="eyebrow">Who we're looking for</span><h2>Partner requirements</h2><p class="lead">This program works best for operators who already run a tight route. Here's what we look for:</p></div>
 <div class="grid grid-3">
  <div class="card"><h3>An established ATM route</h3><p>You currently own and vault ATMs, have machines available to deploy, and know what it takes to keep one at 99%+ uptime.</p></div>
  <div class="card"><h3>Your own vault cash</h3><p>You can fund the cassettes on the locations assigned to you and keep them stocked through weekends and busy seasons.</p></div>
  <div class="card"><h3>Reliable loading and repair capacity</h3><p>A vehicle, a schedule, and the ability to respond to a low-cash alert or a service call within 24 hours. You handle repairs; we discount the parts.</p></div>
  <div class="card"><h3>Insurance and good standing</h3><p>Appropriate business insurance for cash handling, a clean background check, and a business entity in good standing in your state.</p></div>
  <div class="card"><h3>Basic tech</h3><p>A smartphone or computer for our reporting platform and alerts. We'll train you on everything else.</p></div>
  <div class="card"><h3>A service mindset</h3><p>Our locations expect the machine to work. Partners who treat every site like their own best account do very well in this program.</p></div>
 </div>
</div></section>

{faq_block(PA_FAQ, title="Vaulting partner FAQ")}
{cta_band(h="Ready to add locations to your route?", p=f"Call {PHONE_DISPLAY} or email {EMAIL} with your market and a little about your current route. We'll tell you what's available in your area.")}
"""
PAGES.append(pa)

'''
rep('for p in PAGES:', NEW_PAGES + '\nfor p in PAGES:')
open('build_us.py','w').write(s)
print("pass2 unmatched:", len(fails)); [print("  -", f) for f in fails]

s = open('build_us.py').read(); fails = []
rep('"areaServed":{"@type":"State","name":STATE}}', '"areaServed":{"@type":"Country","name":"United States"}}')
rep('all from one {STATE} team you can reach by phone', 'all from one national team you can reach by phone')
open('build_us.py','w').write(s)
print("pass3 unmatched:", len(fails)); [print("  -", f) for f in fails]

s = open('build_us.py').read(); fails = []
rep('{states_block()}', '''<section class="dark"><div class="wrap"><div class="split">
 <div>
  <span class="eyebrow">Vaulting partners</span>
  <h2>Independent ATM operator? Vault our locations and add revenue to your route.</h2>
  <p>We sign the locations. You place your own machine, supply and load the cash on the sites near your route, and earn a share of every surcharge. Not a franchise — no fees, no royalties.</p>
  <div class="btn-row"><a class="btn btn-light" href="partners.html">See the partner program →</a></div>
 </div>
 <img src="_assets/_images/daily-vault-cash-deposits.svg" alt="Vault cash returned to a partner through daily deposits" width="1200" height="900" loading="lazy" style="border-radius:var(--radius)">
</div></div></section>
{states_block()}''')
open('build_us.py','w').write(s)
print("pass4 unmatched:", len(fails))

# ---------- Apply Now form on the partners page
s = open('build_us.py').read(); fails = []
FORM = r"""
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
.apply-panel .close{position:absolute;top:.9rem;right:.9rem;background:var(--sand);border:0;width:38px;height:38px;border-radius:50%;font-size:1.3rem;cursor:pointer;color:var(--navy)}
@media(max-width:480px){.apply-panel form.quote{grid-template-columns:1fr}.fab span{display:none}.fab{padding:.9rem}}
</style>
<button class="fab" type="button" id="apply" aria-controls="apply-panel" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg><span>Apply now</span></button>
<div class="apply-overlay" data-close></div>
<aside class="apply-panel" id="apply-panel" role="dialog" aria-modal="true" aria-labelledby="apply-title" aria-hidden="true">
 <button class="close" type="button" aria-label="Close" data-close>&times;</button>
 <span class="eyebrow">Apply now</span>
 <h2 id="apply-title" style="margin-bottom:.4rem;font-size:1.6rem">Tell us about your route</h2>
 <p style="color:var(--muted);margin-bottom:1.25rem">Takes two minutes. We'll review your market and reach out with what's available in your area.</p>
 <form class="quote" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
  <input type="hidden" name="_subject" value="New vaulting partner application">
  <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
  <div class="full"><label for="ap-business">Business name</label><input id="ap-business" name="business_name" type="text" required autocomplete="organization"></div>
  <div class="full"><label for="ap-contact">Contact name</label><input id="ap-contact" name="contact_name" type="text" required autocomplete="name"></div>
  <div class="full"><label for="ap-address">Address</label><input id="ap-address" name="address" type="text" required autocomplete="street-address" placeholder="Street, city, state, ZIP"></div>
  <div><label for="ap-phone">Phone number</label><input id="ap-phone" name="phone" type="tel" required autocomplete="tel"></div>
  <div><label for="ap-email">Email address</label><input id="ap-email" name="email" type="email" required autocomplete="email"></div>
  <div><label for="ap-zip">Service ZIP code</label><input id="ap-zip" name="service_zip" type="text" inputmode="numeric" pattern="[0-9]{5}(-[0-9]{4})?" required placeholder="Center of your route"></div>
  <div><label for="ap-radius">Service radius</label><select id="ap-radius" name="service_radius" required>
   <option value="" disabled selected>Select a radius</option>
   <option>5 miles</option><option>15 miles</option><option>25 miles</option><option>50 miles</option><option>100 miles</option><option>150+ miles</option><option>The entire state</option>
  </select></div>
  <div class="full"><button class="btn btn-primary" type="submit" style="width:100%">Submit application</button></div>
  <p class="full" style="margin:0;font-size:.82rem;color:var(--muted)">By submitting, you agree to be contacted by US ATM Experts about the vaulting partner program. We don't share your information.</p>
 </form>
 <p style="margin:1.25rem 0 0;font-size:.9rem;color:var(--muted)">Prefer to talk? Call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</aside>
<script>
(function(){var b=document.body,fab=document.getElementById('apply'),panel=document.getElementById('apply-panel');
function open(){b.classList.add('apply-open');fab.setAttribute('aria-expanded','true');panel.setAttribute('aria-hidden','false');setTimeout(function(){document.getElementById('ap-business').focus()},250);}
function close(){b.classList.remove('apply-open');fab.setAttribute('aria-expanded','false');panel.setAttribute('aria-hidden','true');}
fab.addEventListener('click',open);
document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',close)});
document.querySelectorAll('a[href="#apply"]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();open();})});
document.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
if(location.hash==='#apply'){open();}
})();
</script>
"""
rep('PAGES.append(pa)', 'pa["body"] += FORM.replace("{PHONE_TEL}",PHONE_TEL).replace("{PHONE_DISPLAY}",PHONE_DISPLAY).replace("{EMAIL}",EMAIL)\nPAGES.append(pa)')
rep('PAGES = []', 'FORM = r\"\"\"' + FORM + '\"\"\"\nPAGES = []')
# hero + CTA buttons point to the form
rep('"hero-storefronts.svg",crumbs=[("Partners",None)]) + f"""', '"hero-storefronts.svg",crumbs=[("Partners",None)],extra=\'<div class="btn-row"><a class="btn btn-light" href="#apply">Apply now</a></div>\') + f"""')
rep('{cta_band(h="Ready to add locations to your route?", p=f"Call {PHONE_DISPLAY} or email {EMAIL} with your market and a little about your current route. We\'ll tell you what\'s available in your area.")}',
    '<section class="cta-band"><div class="wrap"><h2>Ready to add locations to your route?</h2><p>Tap Apply now, or call {PHONE_DISPLAY} with your market and a little about your current route. We\'ll tell you what\'s available in your area.</p><div class="btn-row" style="justify-content:center"><a class="btn btn-outline" href="#apply">Apply now</a><a class="btn btn-outline" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div></div></section>')
rep('<div class="btn-row"><a class="btn btn-light" href="partners.html">See the partner program →</a></div>', '<div class="btn-row"><a class="btn btn-light" href="partners.html">See the partner program →</a><a class="btn btn-outline" style="border-color:#fff;color:#fff" href="partners.html#apply">Apply now</a></div>')
open('build_us.py','w').write(s)
print("pass5 unmatched:", len(fails)); [print("  -", f) for f in fails]
