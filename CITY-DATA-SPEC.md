Write one JSON file per state at /home/claude/azatm/states/<ABBR>.json (uppercase two-letter abbr), exactly this shape:

{
 "abbr": "TX",
 "name": "Texas",
 "metro_city": "Dallas",                      // the single city you'd name as the state's primary business hub
 "metro_phrase": "the Dallas–Fort Worth metroplex",   // how a local would refer to that metro area, lowercase article ok
 "span_phrase": "from Houston to El Paso",    // two far-apart well-known cities, used in "we serve businesses from X to Y"
 "seasonal_phrase": "rodeo season, football weekends, and summer tourism",  // 3 real, state-appropriate demand drivers that change how much cash a location needs
 "cities": [
   {
     "slug": "dallas",
     "name": "Dallas",
     "region": "North Texas",                 // regional phrase e.g. "the Bay Area", "the Front Range", "Southern Nevada"
     "blurb": "60-90 words. Factual, specific, present tense. Name 2-4 real, well-known districts/neighborhoods/landmarks and the kinds of businesses there (bars, restaurants, hotels, convenience stores, salons, entertainment venues; mention dispensaries ONLY if the state is in the CANNABIS_OK list). Do NOT invent customers, statistics, or claims like 'we've placed X machines'. Do NOT mention sports teams by trademarked name. Write as the company ('we place and service ATMs in...').",
     "areas": ["Deep Ellum", "Uptown", "Bishop Arts District", "Downtown Dallas", "Lower Greenville"],   // 4-6 real districts/neighborhoods
     "nearby": ["fort-worth", "plano", "arlington"]   // 3-4 slugs of OTHER cities in this same file
   }
 ]
}

Rules:
- 8 to 10 cities per state: the largest metros plus 2-3 regional hubs so the whole state is covered. Slugs are lowercase-hyphenated.
- Every "nearby" slug must exist in the same file.
- CANNABIS_OK (mention dispensaries allowed): CA, CO, WA, OR, NV, NM, MI, IL, MA, ME, VT, NJ, NY, CT, RI, DE, MD, VA, MO, OH, MN, MT, AK, HI, AZ, OK, AR, FL, PA, LA, MS, AL, WV, KY, UT, ND, SD, NH. All other states: do NOT mention dispensaries or cannabis.
- Valid JSON only (no comments in the actual file). Double-check it parses.
