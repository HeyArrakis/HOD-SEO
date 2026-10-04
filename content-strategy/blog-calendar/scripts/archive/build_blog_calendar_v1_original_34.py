"""Blog Content Calendar Stage (29 Sep - 31 Dec 2026) - build script.

Hand-authored topic selections plus generators. Reads only local files:
  - architecture/15_keyword_url_map.csv            (Stage 15 ownership, EXISTING_DATA metrics)
  - dataforseo/raw/04_*.json, 06_*.json             (EXISTING_DATA monthly searches)
  - content-strategy/blog-calendar/working/call1_processed.csv  (NEW_RESEARCH, keyword_overview 2026-09-29)
Writes the calendar, backlog and keyword-research CSVs into content-strategy/blog-calendar/.
No API call is made here. Re-run: python3 content-strategy/blog-calendar/scripts/build_blog_calendar.py
"""
import csv, json, datetime as dt, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'content-strategy', 'blog-calendar')
P = lambda *a: os.path.join(ROOT, *a)

# ---------------------------------------------------------------- data sources
S15 = {r['normalized_keyword']: r for r in csv.DictReader(open(P('architecture/15_keyword_url_map.csv')))}
NEW = {r['keyword']: r for r in csv.DictReader(open(P('content-strategy/blog-calendar/working/call1_processed.csv')))}

EXIST_MS = {}
for f in ['dataforseo/raw/04_hod_keywords_for_site_raw.json', 'dataforseo/raw/06_hod_keyword_ideas_raw.json']:
    d = json.load(open(P(f)))
    for it in d['tasks'][0]['result'][0]['items']:
        kw = it.get('keyword') or (it.get('keyword_data') or {}).get('keyword')
        ki = it.get('keyword_info') or (it.get('keyword_data') or {}).get('keyword_info')
        if kw and ki and ki.get('monthly_searches'):
            EXIST_MS.setdefault(kw.lower().strip(), {(m['year'], m['month']): m['search_volume'] for m in ki['monthly_searches'] if m.get('search_volume') is not None})

def kw_source(k):
    if k in NEW:
        return 'NEW_RESEARCH' if NEW[k]['search_volume'] != 'NOT_IN_DATAFORSEO_DB' else 'NEW_RESEARCH_NO_DATA'
    if k in S15:
        return 'EXISTING_DATA'
    return 'UNMEASURED'

def vol(k):
    if k in NEW:
        v = NEW[k]['search_volume']
        return int(v) if v not in ('', 'NOT_IN_DATAFORSEO_DB', 'None') else None
    if k in S15:
        v = S15[k]['search_volume']
        try: return int(float(v))
        except ValueError: return None
    return None

def fmt_kw(k):
    v = vol(k)
    return f"{k} ({v if v is not None else 'n/a'}; {kw_source(k)})"

# ---------------------------------------------------------------- calendar frame
START, END = dt.date(2026, 9, 29), dt.date(2026, 12, 31)
SLOT_WEEKDAYS = (0, 1, 3, 4)  # Mon, Tue, Thu, Fri = 4 planned slots per week

def week_of(d):
    monday = d - dt.timedelta(days=d.weekday())
    first = START - dt.timedelta(days=START.weekday())
    n = (monday - first).days // 7 + 1
    sun = monday + dt.timedelta(days=6)
    return f"W{n:02d} ({monday:%b %d}-{min(sun, END):%b %d})"

ALL_SLOTS = [START + dt.timedelta(days=i) for i in range((END - START).days + 1)
             if (START + dt.timedelta(days=i)).weekday() in SLOT_WEEKDAYS]

EVENTS = {  # verified dates (see summary for sources)
    'Christmas': '2026-12-25', 'Christmas Eve': '2026-12-24', 'Hanukkah': '2026-12-04 (to 12-12)',
    'Thanksgiving': '2026-11-26', 'Black Friday': '2026-11-27', 'Cyber Monday': '2026-11-30',
    "New Year's Eve": '2026-12-31', "Valentine's Day": '2027-02-14', 'Diwali': '2026-11-08 (Dhanteras 11-06)',
    'Engagement season': '2026-11-26 to 2027-02-14 (Thanksgiving to Valentine\'s)',
}

# ---------------------------------------------------------------- template link rules (Stage 16)
TEMPLATE_REQUIRED = {  # REQUIRED outgoing links per Stage 16 blog template
    'BLOG-GIFTS': ['BLOG-HUB', 'COM-FJ-BRACELETS', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES'],
    'BLOG-CRAFT': ['BLOG-HUB', 'COM-BESPOKE'],
    'BLOG-STYLE': ['BLOG-HUB'],
    'BLOG-INDUSTRY': ['BLOG-HUB', 'EDU-LG-00', 'EDU-LG-05'],
    'BLOG-LAUNCH': ['BLOG-HUB', 'COM-ER', 'COM-FJ', 'COM-PDP'],
}

# ---------------------------------------------------------------- hand-authored topics
# Every keyword below was checked against the Stage 15 map (see QC). Volumes are pulled, not typed.
T = []
def topic(**k): T.append(k)

topic(date='2026-09-29', template='BLOG-CRAFT', content_type='SEASONAL',
      event='Christmas (custom-order lead time); engagement season', event_date=EVENTS['Christmas'],
      publish_by='2026-10-09', lead='~12 weeks before Christmas; custom work needs production time before the gift date (HOD production time is a business fact).',
      title='How long a custom engagement ring takes: design to delivery, and ordering in time for the holidays',
      primary='how long does a custom engagement ring take',
      secondary=['custom engagement ring process', 'how to design your own engagement ring', 'custom ring cost'],
      cluster='NEW:BESPOKE_PROCESS (no Stage 11 cluster; Stage 11 has no bespoke keywords)',
      intent='INFORMATIONAL', funnel='CONSIDERATION', hub='COM-BESPOKE (commercial service hub)', spoke='Craft spoke: bespoke process and timeline',
      parent='Bespoke / custom jewellery', related='BC-010; BC-005',
      audience='Couples planning a holiday proposal who want a one-off ring', need='How long custom takes, what the steps are, and the latest date to order before a holiday proposal',
      seasonal='HIGH: order-by date for Christmas/NYE proposals', festival='Christmas, NYE proposals (indirect)',
      hod='HIGH: HOD offers bespoke (/bespoke) with Surat manufacturing', commercial='HIGH: direct path to the bespoke enquiry',
      category='COM-BESPOKE', product='n/a (bespoke service)', edu='EDU-RJG-01 (settings), EDU-SHP-00 (shapes)', target_id='',
      links=['BLOG-HUB', 'COM-BESPOKE', 'BRAND-ABOUT', 'EDU-RJG-01', 'EDU-SHP-00', 'COM-ER'],
      cta='Bespoke consultation / enquiry (COM-BESPOKE)',
      cann='PASS. Commercial head terms (custom engagement ring 40,500; design your own engagement ring 5,400) are left to COM-BESPOKE and not targeted here. Primary is a timeline question with an AIO + forum SERP.',
      facts='HOD bespoke production time; holiday order cut-off; price guidance policy',
      priority='P1_TIME_CRITICAL',
      why='Timing: must go live before holiday custom orders close. Demand: small (210) but informational AIO/forum SERP, KD 0. Commercial: strongest bespoke link in the dataset. Craft: first-hand evidence Stage 13 lists as the biggest Blog gap.',
      promote='NO', refresh='Annually before Oct (update order-by dates)')

topic(date='2026-10-01', template='BLOG-INDUSTRY', content_type='EVERGREEN',
      event='Industry note (lab-grown news peaks in October)', event_date='n/a',
      publish_by='2026-10-15', lead='Oct was the 12-month peak for lab grown diamond news (Oct index 2.28).',
      title='The lab-grown diamond market in 2026: prices, demand and what changed this year (dated industry note)',
      primary='lab grown diamond market',
      secondary=['lab grown diamond news', 'de beers lab grown', 'lab grown diamond trends', 'are more people buying lab grown diamonds', 'future of lab grown diamonds', 'are lab-grown diamonds the future'],
      cluster='CL-014 (Lab-Grown Diamond History & Market Trends; Stage 13/14: Blog primary)',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='EDU-LG-00 (Lab-Grown Education hub)', spoke='Industry Notes spoke: dated market commentary',
      parent='Lab-grown diamonds', related='BC-015',
      audience='Lab-grown buyers and researchers following price and market news', need='What is happening to lab-grown prices and demand right now, with dated sources',
      seasonal='MEDIUM: October news peak', festival='none',
      hod='HIGH: HOD core product is lab-grown', commercial='INDIRECT: Education-first, then the lab-grown collection',
      category='COM-ER / COM-FJ (COM-LG-HUB conditional)', product='n/a', edu='EDU-LG-00, EDU-LG-05, EDU-LG-02', target_id='EDU-LG-05',
      links=['BLOG-HUB', 'EDU-LG-00', 'EDU-LG-05', 'EDU-LG-02', 'EDU-LG-03', 'EDU-LG-07'],
      cta='Read the price/value guide (EDU-LG-05); then browse lab-grown engagement rings',
      cann='BOUNDARY: EDU-LG-05 owns price/value questions (incl. "will lab-grown diamonds get cheaper"). The note reports dated market facts only and links to LG-05 for "do they hold value/are they cheaper". The new term "are lab grown diamonds getting cheaper" is deliberately NOT targeted.',
      facts='Dated, sourced price references (Stage 19 LG-05 rule); no HOD pricing claims without data',
      priority='P2_HIGH',
      why='Topical authority for HOD\'s core category. Stage 13/14 assign CL-014 to Blog. Demand is small (70 + 260 news), but it is the one Industry Notes topic with evidence. Link dependency: EDU-LG-00/EDU-LG-05 are proposed pages; link LG-02 until they are live.',
      promote='NO', refresh='Every 6-12 months (dated)')

topic(date='2026-10-02', template='BLOG-GIFTS', content_type='EVERGREEN',
      event='Year-round occasion (new parents)', event_date='n/a',
      publish_by='n/a (evergreen)', lead='Evergreen; flat demand (Nov/Dec index ~1.0-1.25).',
      title='What is a push present? Meaning, etiquette and jewellery ideas',
      primary='what is a push present',
      secondary=['push present', 'push present ideas'],
      cluster='NEW:OCCASION_PUSH_PRESENT',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='BLOG-GIFTS (Gifts & Occasions) -> COM-FJ', spoke='Occasion guide',
      parent='Gifts & occasions', related='BC-018; BC-023',
      audience='Partners of expecting parents', need='What a push present is, whether it is expected, and what to give',
      seasonal='LOW', festival='none',
      hod='HIGH: studs, pendants and eternity bands are the typical push presents and are in the catalogue', commercial='HIGH: earrings, necklaces, eternity/anniversary bands',
      category='COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS; COM-WB', product='Solitaire stud earrings; solitaire pendants; half-eternity bands (verify live at publish)', edu='EDU-RJG-02 (ring size), EDU-4C-07 (carat for studs)', target_id='',
      links=['BLOG-HUB', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS', 'COM-WB', 'EDU-RJG-02', 'COM-BESPOKE'],
      cta='Shop earrings / pendants; bespoke engraving or birthstone-free custom piece via COM-BESPOKE',
      cann='PASS: no Stage 15 owner, no Education topic for occasions (Stage 13 assigns Gifts & Occasions to Blog).',
      facts='none blocking', priority='P2_HIGH',
      why='Largest evergreen occasion demand that fits HOD: push present 18,100 + ideas 8,100 + what is 5,400. KD 0; AIO + video SERP (informational). Year-round traffic balances the holiday-heavy calendar.',
      promote='NO', refresh='Annually')

topic(date='2026-10-05', template='BLOG-GIFTS', content_type='FESTIVAL',
      event='Christmas / holiday gifting', event_date=EVENTS['Christmas'],
      publish_by='2026-11-01', lead='11.5 weeks before Christmas; gift searches start rising in Nov (index 3.7) and peak in Dec (index 6.8). Needs indexing and internal links before the Nov rise.',
      title='Holiday jewelry gift guide: diamond gifts by budget, style and recipient (hub for the gift series)',
      primary='christmas jewelry gifts',
      secondary=['holiday jewelry gift guide', 'jewelry gift guide', 'jewelry gift ideas', 'best jewelry gifts', 'jewelry gifts under 500', 'christmas gifts under 500'],
      cluster='NEW:HOLIDAY_JEWELRY_GIFTS',
      intent='COMMERCIAL_RESEARCH', funnel='CONSIDERATION', hub='BLOG-GIFTS series hub -> COM-FJ', spoke='Seasonal hub; recipient spokes BC-008, BC-009, BC-012, BC-013, BC-020, BC-028',
      parent='Holiday gifting', related='BC-008; BC-009; BC-012; BC-013; BC-020; BC-028',
      audience='US holiday shoppers buying diamond jewellery as a gift', need='Which jewellery makes a good gift at each budget, and how to choose safely (size, returns)',
      seasonal='HIGH', festival='Christmas, Hanukkah, holiday season',
      hod='HIGH: full gifting catalogue (studs, hoops, tennis bracelets, pendants)', commercial='HIGH: category and product links',
      category='COM-FJ; COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS', product='Solenne/Celeste stud earrings; tennis bracelets; solitaire and heart pendants (verify live)', edu='EDU-RJG-02 (ring size), EDU-4C-00 (4Cs), EDU-LG-02 (lab vs natural)', target_id='',
      links=['BLOG-HUB', 'COM-FJ', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS', 'COM-BESPOKE', 'EDU-RJG-02', 'EDU-4C-00'],
      cta='Shop by category; returns/shipping policy link; bespoke for one-off gifts',
      cann='SERIES RISK (MEDIUM): recipient guides BC-008/009/012/013 must keep recipient-specific primaries; this hub owns the generic "christmas jewelry gifts / jewelry gift guide" intent. SERP overlap unvalidated (optional call 2).',
      facts='Holiday shipping cut-offs; returns/exchange window for gifts; price points (no fixed prices in copy)',
      priority='P1_TIME_CRITICAL',
      why='Timing: has to be indexed before the Nov rise. Demand: jewellery-specific gift terms ~1,500/month combined; SERPs product-led with AIO/forums, so a curated guide is a realistic format. Commercial: the strongest category-linking post in the calendar.',
      promote='NO', refresh='Annually by Oct (same URL; year in title only, Stage 13 section 7)')

topic(date='2026-10-06', template='BLOG-CRAFT', content_type='EVERGREEN',
      event='Craft (evergreen)', event_date='n/a', publish_by='n/a (evergreen)', lead='Evergreen.',
      title='How diamonds are cut and polished: inside a Surat cutting workshop',
      primary='how diamonds are cut',
      secondary=['diamond cutting process', 'diamond polishing'],
      cluster='NEW:DIAMOND_CUTTING_CRAFT',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='BRAND-ABOUT / COM-BESPOKE (craft evidence)', spoke='Craft spoke: stone cutting',
      parent='Craftsmanship (Surat)', related='BC-010; BC-015',
      audience='Curious buyers; people researching quality before buying', need='How rough becomes a polished diamond, step by step, and why cutting skill matters',
      seasonal='NONE', festival='none',
      hod='HIGH: Surat is the world\'s main cutting centre and HOD\'s manufacturing link', commercial='INDIRECT: trust -> cut guide -> engagement rings',
      category='COM-ER; COM-BESPOKE', product='n/a', edu='EDU-4C-06 (cut grade), EDU-NAT-00 (mine to jewellery summary), EDU-SHP-00', target_id='EDU-4C-06',
      links=['BLOG-HUB', 'COM-BESPOKE', 'BRAND-ABOUT', 'EDU-4C-06', 'EDU-SHP-00', 'EDU-NAT-00'],
      cta='Learn cut grades (EDU-4C-06); see HOD craftsmanship (About); commission a piece',
      cann='BOUNDARY (MEDIUM): EDU-4C-06 owns cut GRADE; EDU-GEN-01 owns "can you cut diamonds" (hardness); EDU-NAT-00 S06 summarises mining/cutting. This post owns the first-hand cutting PROCESS only. It must not grade cuts or answer the hardness questions; link out instead.',
      facts='Whether HOD cuts/polishes in-house or works with Surat partners (first-hand claims need confirmation); workshop photography',
      priority='P2_HIGH',
      why='Demand: 1,900 + 1,300 polishing, AIO/forum/video SERP (informational). KD 18. Only HOD can supply the first-hand evidence (Stage 13 section 8). It also fills the BLOG-CRAFT template.',
      promote='NO (brand/craft)', refresh='Keep as record; review yearly')

topic(date='2026-10-08', template='BLOG-STYLE', content_type='EVERGREEN',
      event='Style (evergreen; mild Nov peak)', event_date='n/a', publish_by='n/a (evergreen)', lead='Evergreen; necklace layering peaks Nov (index 1.56).',
      title='How to layer necklaces: lengths, pendants and diamond pieces that work together',
      primary='how to layer necklaces',
      secondary=['necklace layering'],
      cluster='NEW:STYLE_NECKLACE_LAYERING',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-FJ-NECKLACES', spoke='Style spoke: necklaces',
      parent='Styling', related='BC-021',
      audience='Women buying or styling fine necklaces', need='How to combine lengths and pendant styles without tangling or clashing',
      seasonal='LOW', festival='none',
      hod='HIGH: solitaire, pendant, station, lariat and T-bar pieces in catalogue', commercial='MEDIUM-HIGH: necklace category and products',
      category='COM-FJ-NECKLACES', product='Solitaire pendants; Celestine station necklace; lariat; T-bar pieces (verify live)', edu='EDU-MET-00 (mixing metals)', target_id='',
      links=['BLOG-HUB', 'COM-FJ-NECKLACES', 'COM-FJ', 'EDU-MET-00', 'COM-PDP'],
      cta='Shop necklaces & pendants',
      cann='PASS: no Stage 15 owner. "necklace length chart" (9,900) is NOT targeted; it is an Education-type sizing gap (backlog). This post links to it once it exists.',
      facts='none', priority='P2_HIGH',
      why='Demand: necklace layering 14,800 + how to layer 2,400. KD 0-1, AIO + forum + video SERP. Stage 13 puts styling in the Blog. Direct link to the necklace catalogue.',
      promote='CANDIDATE if Stage 14 adds a jewellery styling/ownership hub', refresh='Yearly')

topic(date='2026-10-09', template='BLOG-STYLE', content_type='EVERGREEN',
      event='Engagement season (evergreen with Dec peak)', event_date=EVENTS['Engagement season'], publish_by='2026-11-15', lead='Evergreen; "does the wedding band go on first" peaks Dec (1.58). Publish before engagement season.',
      title='How to wear an engagement ring and wedding band: order, hand and stacking etiquette',
      primary='how to wear engagement ring and wedding band',
      secondary=['which hand does engagement ring go on', 'does the wedding band go on first', 'should engagement ring and wedding band match'],
      cluster='NEW:STYLE_BRIDAL_WEAR',
      intent='INFORMATIONAL', funnel='RETENTION', hub='COM-WB / COM-ER', spoke='Style spoke: bridal wear',
      parent='Engagement & wedding rings', related='BC-022; BC-011',
      audience='Newly engaged and soon-to-be-married couples', need='Which hand, which order, and whether the band must match',
      seasonal='MEDIUM: engagement season', festival='Engagement season',
      hod='HIGH: bridal sets and bands in catalogue', commercial='HIGH: bridal sets, wedding bands',
      category='COM-WB; COM-ER', product='Bridal ring sets (Elaris, Solenne, Celestine) (verify live)', edu='EDU-RJG-02 (sizing), EDU-MET-00 (metal matching)', target_id='',
      links=['BLOG-HUB', 'COM-WB', 'COM-ER', 'EDU-RJG-02', 'EDU-MET-00', 'COM-PDP'],
      cta='Shop wedding bands / bridal sets',
      cann='PASS: no Stage 15 owner. "which hand" has KD 25 (secondary only). Kept distinct from BC-022 (stacking several rings/bands).',
      facts='none', priority='P2_HIGH',
      why='Demand: 3,600 + 1,300 + 880, KD 0. AIO/forum/video SERP (informational). Directly supports bridal sets and bands before engagement season.',
      promote='CANDIDATE (Ring & Jewellery Guides) if Stage 14 is revised', refresh='Yearly')

topic(date='2026-10-12', template='BLOG-GIFTS', content_type='SEASONAL',
      event='Christmas / holidays; anniversaries year-round', event_date=EVENTS['Christmas'], publish_by='2026-11-01', lead='~10.5 weeks before Christmas; "christmas gifts for wife" Nov index 2.3, Dec 9.2.',
      title='Jewelry gifts for your wife: diamond ideas she will actually wear',
      primary='jewelry gifts for wife',
      secondary=['christmas gifts for wife jewelry', 'gifts for wife who has everything', 'christmas gifts for wife'],
      cluster='NEW:GIFTS_RECIPIENT_WIFE',
      intent='COMMERCIAL_RESEARCH', funnel='CONSIDERATION', hub='BC-004 holiday gift hub -> COM-FJ', spoke='Recipient spoke: wife',
      parent='Holiday gifting', related='BC-004; BC-018',
      audience='Husbands/partners shopping for a wife', need='Jewellery ideas matched to her style, with safe-sizing advice',
      seasonal='HIGH', festival='Christmas; anniversaries',
      hod='HIGH', commercial='HIGH',
      category='COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS; COM-WB', product='Tennis bracelets; eternity bands; drop earrings (verify live)', edu='EDU-RJG-02', target_id='',
      links=['BLOG-HUB', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS', 'COM-WB', 'BC-004'],
      cta='Shop gifts by category', cann='SERIES RISK (MEDIUM): recipient-specific primary; generic "christmas gifts for wife" (27,100) is a stretch secondary on a broad non-jewellery SERP. Check SERP overlap with BC-004 (optional call 2).',
      facts='Returns window; shipping cut-off', priority='P2_HIGH',
      why='Recipient intent is distinct and high value. Jewellery-specific demand is 320 + 40 + 720; the broad head (27,100, KD 3) is upside. December peak, so publish by Nov 1.',
      promote='NO', refresh='Annually by Oct')

topic(date='2026-10-13', template='BLOG-GIFTS', content_type='SEASONAL',
      event='Christmas / first holidays together', event_date=EVENTS['Christmas'], publish_by='2026-11-01', lead='~10.5 weeks before Christmas; "christmas gifts for girlfriend" Nov 3.3, Dec 7.5.',
      title='Jewelry gifts for your girlfriend: first-Christmas and meaningful diamond ideas',
      primary='jewelry gifts for girlfriend',
      secondary=['first christmas gift for girlfriend', 'first christmas together gift', 'what jewelry to buy for girlfriend', 'christmas gifts for girlfriend'],
      cluster='NEW:GIFTS_RECIPIENT_GIRLFRIEND',
      intent='COMMERCIAL_RESEARCH', funnel='CONSIDERATION', hub='BC-004 holiday gift hub -> COM-FJ', spoke='Recipient spoke: girlfriend',
      parent='Holiday gifting', related='BC-004; BC-011',
      audience='Partners shopping for a girlfriend (often first big jewellery gift)', need='A gift that is meaningful without implying a proposal; safe choices (no ring-size risk)',
      seasonal='HIGH', festival='Christmas',
      hod='HIGH', commercial='HIGH',
      category='COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS', product='Heart pendants (Amora, Liora); huggies; stud earrings (verify live)', edu='EDU-RJG-02', target_id='',
      links=['BLOG-HUB', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS', 'BC-004', 'BC-011'],
      cta='Shop pendants and earrings', cann='SERIES RISK (MEDIUM): recipient-specific; links to promise-ring post BC-011 rather than covering promise rings.',
      facts='Returns window; shipping cut-off', priority='P2_HIGH',
      why='Distinct recipient intent. Jewellery demand 320 + 110 + 110; broad head 12,100 (KD 4, AIO/forum). December peak.',
      promote='NO', refresh='Annually by Oct')

topic(date='2026-10-15', template='BLOG-CRAFT', content_type='EVERGREEN',
      event='Craft (evergreen)', event_date='n/a', publish_by='n/a (evergreen)', lead='Evergreen.',
      title='How a diamond ring is made: from CAD design and casting to stone setting',
      primary='how is jewelry made',
      secondary=['how are rings made', 'how is a diamond ring made', 'jewelry manufacturing process', 'lab grown diamond factory'],
      cluster='NEW:JEWELLERY_MAKING (+ CL-026 lab-grown factory term, Stage 14 D14-12: Blog/brand)',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-BESPOKE / BRAND-ABOUT', spoke='Craft spoke: ring making',
      parent='Craftsmanship (Surat)', related='BC-001; BC-005',
      audience='Buyers comparing brands on quality; bespoke prospects', need='What happens between design and a finished ring, and where quality is won or lost',
      seasonal='NONE', festival='none',
      hod='HIGH: HOD manufactures (Surat)', commercial='MEDIUM: bespoke and engagement rings',
      category='COM-BESPOKE; COM-ER', product='n/a', edu='EDU-RJG-01 (settings), EDU-MET-00 (metals)', target_id='EDU-RJG-01',
      links=['BLOG-HUB', 'COM-BESPOKE', 'BRAND-ABOUT', 'EDU-RJG-01', 'EDU-MET-00', 'COM-PDP'],
      cta='See the bespoke process; browse engagement rings',
      cann='BOUNDARY: EDU-NAT-00 owns "how are diamonds made" (formation) and EDU-LG-00 owns "how are lab grown diamonds made". This post is about making the JEWELLERY (ring), never stone formation/growth. EDU-RJG-01 owns setting types; the post shows the setting craft and links there.',
      facts='HOD workshop steps and photos; whether HOD grows stones (only then use "lab grown diamond factory")',
      priority='P3_MEDIUM',
      why='Demand is small (210 + 140 + 20), but the SERP is informational (AIO/forum/video). First-hand craft proof supports trust and Bespoke (Stage 13 largest Blog gap).',
      promote='NO', refresh='Keep as record')

topic(date='2026-10-16', template='BLOG-GIFTS', content_type='EVERGREEN',
      event='Holiday gifting and engagement season (Dec peak)', event_date=EVENTS['Christmas'], publish_by='2026-11-15', lead='Evergreen with Dec peak ("what is a promise ring" Dec index 1.38).',
      title='What is a promise ring? Meaning, which finger, and how it differs from an engagement ring',
      primary='what is a promise ring',
      secondary=['promise ring vs engagement ring'],
      cluster='NEW:OCCASION_PROMISE_RING',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-FJ-RINGS (conditional) / COM-FJ', spoke='Occasion spoke: promise rings',
      parent='Ring traditions', related='BC-009; BC-007',
      audience='Young couples; gift buyers not ready to propose', need='What a promise ring means and how it differs from an engagement ring',
      seasonal='MEDIUM', festival='Christmas',
      hod='MEDIUM-HIGH: fine diamond rings and bands can serve as promise rings; no promise-ring category', commercial='MEDIUM: fine-jewellery rings',
      category='COM-FJ (Rings, conditional)', product='Diamond fashion rings; half-eternity bands (verify live)', edu='EDU-RJG-02', target_id='',
      links=['BLOG-HUB', 'COM-FJ', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS', 'EDU-RJG-02', 'COM-ER'],
      cta='Shop fine-jewellery rings; see engagement rings when ready',
      cann='PASS: "promise rings" (301,000, product SERP) is a shopping head and NOT targeted. Excluded Stage 15 "tungsten promise ring(s)" are not used.',
      facts='none', priority='P2_HIGH',
      why='Demand: 22,200 + 1,600, KD 0, AIO + forum SERP (informational). December peak. A natural gift-season question for HOD\'s ring range.',
      promote='CANDIDATE if a Ring traditions/Education hub is added', refresh='Yearly')

topic(date='2026-10-19', template='BLOG-GIFTS', content_type='SEASONAL',
      event='Christmas / holidays; Mother\'s Day (May)', event_date=EVENTS['Christmas'], publish_by='2026-11-01', lead='~9.5 weeks before Christmas; "christmas gifts for mom" Nov 3.0, Dec 8.1.',
      title='Jewelry gifts for mom: diamond pieces for every style (holiday and Mother\'s Day)',
      primary='jewelry gifts for mom',
      secondary=['gifts for mom jewelry', 'christmas gifts for mom'],
      cluster='NEW:GIFTS_RECIPIENT_MOM',
      intent='COMMERCIAL_RESEARCH', funnel='CONSIDERATION', hub='BC-004 holiday gift hub -> COM-FJ', spoke='Recipient spoke: mom',
      parent='Holiday gifting', related='BC-004; BC-018',
      audience='Adult children and partners buying for mothers', need='Classic, wearable jewellery gifts for a mother',
      seasonal='HIGH (Dec) + second window in May', festival='Christmas; Mother\'s Day 2027',
      hod='HIGH', commercial='HIGH',
      category='COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS', product='Stud earrings; pendants; tennis bracelets (verify live)', edu='EDU-4C-00', target_id='',
      links=['BLOG-HUB', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS', 'BC-004'],
      cta='Shop earrings / necklaces / bracelets', cann='SERIES RISK (MEDIUM): recipient-specific; the broad head "christmas gifts for mom" (49,500) is a stretch secondary only.',
      facts='Shipping cut-off', priority='P2_HIGH',
      why='Jewellery-specific demand 1,000 + 1,000 (the largest recipient-jewellery pair measured). December peak plus a second use in May.',
      promote='NO', refresh='Before Oct and before Apr')

topic(date='2026-10-20', template='BLOG-GIFTS', content_type='SEASONAL',
      event='Christmas / luxury gifting', event_date=EVENTS['Christmas'], publish_by='2026-11-01', lead='~9.5 weeks before Christmas; "luxury christmas gifts for her" Nov 3.9, Dec 5.0.',
      title='Luxury diamond gifts for her: statement pieces worth the splurge',
      primary='luxury christmas gifts for her',
      secondary=['diamond gifts', 'diamond gifts for her', 'luxury gifts for her', 'best jewelry gifts for her'],
      cluster='NEW:GIFTS_LUXURY_DIAMOND',
      intent='COMMERCIAL_RESEARCH', funnel='CONSIDERATION', hub='BC-004 holiday gift hub -> COM-FJ', spoke='Tier spoke: luxury/diamond',
      parent='Holiday gifting', related='BC-004; BC-008',
      audience='High-budget gift buyers', need='Statement diamond pieces and how to judge value (lab vs natural, 4Cs)',
      seasonal='HIGH', festival='Christmas',
      hod='HIGH: luxury diamond positioning', commercial='HIGH',
      category='COM-FJ-BRACELETS; COM-FJ-EARRINGS; COM-FJ-NECKLACES', product='Tennis bracelets; triple-row hoops; statement studs (verify live)', edu='EDU-LG-02, EDU-4C-00', target_id='EDU-LG-02',
      links=['BLOG-HUB', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS', 'EDU-LG-02', 'EDU-4C-00', 'COM-BESPOKE'],
      cta='Shop statement pieces; bespoke for one-offs',
      cann='SERIES RISK (MEDIUM-HIGH): "best jewelry gifts for her" could share a SERP with BC-004. Kept as secondary here; BC-004 owns the generic guide. Validate with optional call 2 before writing; if SERPs match, merge into BC-004 as a section.',
      facts='none', priority='P3_MEDIUM',
      why='Fits HOD\'s luxury positioning; December peak. Demand 260 + 210 + 1,900 (luxury gifts for her). Scheduled at MEDIUM because overlap with BC-004 is not yet validated.',
      promote='NO', refresh='Annually')

topic(date='2026-10-22', template='BLOG-GIFTS', content_type='EVERGREEN',
      event='Engagement season (evergreen, Dec peak)', event_date=EVENTS['Engagement season'], publish_by='2026-11-15', lead='Evergreen; proposal ideas Dec index 1.27; "proposal ideas at home" Dec 1.74.',
      title='Proposal ideas: how to plan a proposal she will remember (at home, outdoors, with family)',
      primary='proposal ideas',
      secondary=['how to propose', 'how to plan a proposal', 'proposal ideas at home'],
      cluster='NEW:PROPOSAL_PLANNING',
      intent='INFORMATIONAL', funnel='CONSIDERATION', hub='COM-ER (engagement rings)', spoke='Proposal series hub; seasonal spokes BC-017, BC-029, BC-034',
      parent='Proposal & engagement', related='BC-017; BC-029; BC-034; BC-016',
      audience='People planning to propose', need='Practical proposal ideas and planning steps, with the ring as the centre',
      seasonal='MEDIUM', festival='Engagement season',
      hod='MEDIUM-HIGH: proposal = engagement-ring moment (Stage 13 excludes general wedding planning; proposal content is kept to the ring moment)', commercial='HIGH: engagement rings; ring size',
      category='COM-ER', product='Engagement rings (verify live)', edu='EDU-RJG-02 (secret sizing), EDU-LG-10 (choosing a stone)', target_id='EDU-RJG-02',
      links=['BLOG-HUB', 'COM-ER', 'EDU-RJG-02', 'EDU-LG-10', 'COM-BESPOKE', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS'],
      cta='Choose the ring: engagement rings / bespoke; get her ring size right (EDU-RJG-02)',
      cann='PASS: no Stage 15 owner. Ring-size-in-secret stays on EDU-RJG-02 (link, do not answer). Seasonal proposal posts link back here and do not repeat generic ideas.',
      facts='none', priority='P2_HIGH',
      why='Demand: proposal ideas 14,800 (KD 9) + how to propose 3,600 + at home 720; AIO/video SERP. Direct lead-in to engagement rings in proposal season. Scope decision logged (D-BC-06).',
      promote='NO', refresh='Yearly')

topic(date='2026-10-23', template='BLOG-CRAFT', content_type='FESTIVAL',
      event='Diwali (Surat/India connection)', event_date=EVENTS['Diwali'], publish_by='2026-10-30', lead='~2 weeks before Diwali. Brand/industry piece: evergreen search value, with Diwali as the timely hook. Not a gift-deal post.',
      title='Where are lab-grown diamonds made? Inside Surat, the city that cuts most of the world\'s diamonds',
      primary='where are lab grown diamonds made',
      secondary=['surat diamonds', 'surat diamond industry', 'lab grown diamonds industry'],
      cluster='NEW:INDUSTRY_GEOGRAPHY (+ CL-026 industry term)',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='EDU-LG-00 / BRAND-ABOUT', spoke='Craft/Industry spoke: origin & Surat',
      parent='Lab-grown diamonds; craftsmanship', related='BC-005; BC-002',
      audience='Lab-grown buyers asking about origin; people researching HOD\'s Surat heritage', need='Which countries grow and cut lab-grown diamonds, and what Surat\'s role is',
      seasonal='LOW (Dec index 1.89)', festival='Diwali (Surat festival context; Indian-American audience)',
      hod='HIGH: HOD\'s Surat manufacturing link', commercial='MEDIUM: trust -> lab-grown collection',
      category='COM-ER; COM-FJ', product='n/a', edu='EDU-LG-00, EDU-LG-03 (CVD/HPHT growth), EDU-LG-07 (ethics)', target_id='EDU-LG-00',
      links=['BLOG-HUB', 'COM-BESPOKE', 'BRAND-ABOUT', 'EDU-LG-00', 'EDU-LG-03', 'EDU-LG-07'],
      cta='Read about how lab-grown diamonds are grown (EDU-LG-00/LG-03); meet the HOD workshop (About)',
      cann='BOUNDARY (MEDIUM): EDU-LG-00 owns "how are lab grown diamonds made" (process, interim home for LG-04); EDU-LG-03 owns CVD/HPHT. This post answers WHERE (geography, Surat industry), not HOW. Growth-method detail is a one-line summary plus a link. No natural-formation content (EDU-NAT-00 owns "how are diamonds made") and no composition content (EDU-GEN-01 owns "what are diamonds made of"). Ethics/sustainability claims link to EDU-LG-07 and need substantiation (Stage 19 BLOCKING fact).',
      facts='HOD sourcing geography; any ethics claim wording (Stage 19 BLOCKING for claims)', priority='P2_HIGH',
      why='Demand: 210 + 210 + 30. Informational AIO/forum/video SERPs, KD 30. Unique HOD angle (Surat) that competitors cannot copy. The Diwali timing gives a natural hook for the Indian-American audience.',
      promote='NO', refresh='Yearly (industry figures dated)')

topic(date='2026-10-26', template='BLOG-INDUSTRY', content_type='SEASONAL',
      event='Engagement season starts (Thanksgiving)', event_date=EVENTS['Thanksgiving'], publish_by='2026-10-30', lead='~4 weeks before Thanksgiving; "when is engagement season" peaks Nov (1.88).',
      title='When is engagement season? Why so many proposals happen between Thanksgiving and Valentine\'s Day',
      primary='when is engagement season',
      secondary=['engagement season', 'most popular day to get engaged', 'most popular month to get engaged', 'thanksgiving proposal ideas', 'thanksgiving proposal'],
      cluster='NEW:ENGAGEMENT_SEASON',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-ER', spoke='Proposal series spoke: seasonality & data',
      parent='Proposal & engagement', related='BC-014; BC-017; BC-019',
      audience='Couples expecting a proposal; people planning one', need='When engagement season is, the data behind it, and planning ahead',
      seasonal='HIGH', festival='Thanksgiving; Christmas; NYE; Valentine\'s',
      hod='HIGH', commercial='MEDIUM-HIGH: engagement rings; bespoke lead time',
      category='COM-ER', product='n/a', edu='EDU-LG-10', target_id='',
      links=['BLOG-HUB', 'COM-ER', 'EDU-LG-02', 'EDU-LG-05', 'EDU-LG-00', 'BC-001', 'BC-014'],
      cta='Plan ahead: engagement rings; bespoke timeline (BC-001)',
      cann='PASS: no Stage 15 owner. Thanksgiving proposal terms (70 total) are folded in here instead of a thin standalone post.',
      facts='Cite The Knot survey data with year (third-party, dated)', priority='P1_TIME_CRITICAL',
      why='Timing: must be live before Thanksgiving opens engagement season. Demand small (170 + 140 + 40 + 70) but tightly on-season, KD 0-10, AIO SERPs. It also anchors the proposal series.',
      promote='NO', refresh='Yearly (update survey year)')

topic(date='2026-10-27', template='BLOG-GIFTS', content_type='FESTIVAL',
      event='Christmas proposals (Christmas Day and Eve are the top proposal days)', event_date=EVENTS['Christmas'], publish_by='2026-11-09', lead='~8.5 weeks before Christmas; Nov index 2.9, Dec 5.3. Early publication allows indexing before the Nov rise.',
      title='Christmas proposal ideas: festive and winter ways to propose (plus ring-timing checklist)',
      primary='christmas proposal ideas',
      secondary=['christmas proposal', 'christmas engagement', 'christmas eve proposal', 'how to propose on christmas', 'holiday proposal ideas', 'winter proposal ideas', 'christmas engagement ring'],
      cluster='NEW:PROPOSAL_CHRISTMAS',
      intent='INFORMATIONAL', funnel='CONSIDERATION', hub='BC-014 proposal hub -> COM-ER', spoke='Seasonal proposal spoke: Christmas/winter',
      parent='Proposal & engagement', related='BC-014; BC-029; BC-016',
      audience='People planning a holiday proposal', need='Festive proposal ideas and when to buy the ring so it arrives in time',
      seasonal='HIGH', festival='Christmas; Christmas Eve; winter',
      hod='HIGH', commercial='HIGH: engagement rings; bespoke timeline',
      category='COM-ER', product='Engagement rings (verify live)', edu='EDU-RJG-02 (secret sizing)', target_id='EDU-RJG-02',
      links=['BLOG-HUB', 'COM-ER', 'EDU-RJG-02', 'BC-001', 'BC-014', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS'],
      cta='Order the ring in time: engagement rings / bespoke',
      cann='MERGE DECISION: winter + holiday proposal terms are secondaries here, not a separate post, to avoid two near-identical seasonal proposal articles. NYE (BC-029) stays separate (Dec 6-7x spike, different date). Validate SERP overlap (optional call 2).',
      facts='Order-by dates for Christmas delivery', priority='P1_TIME_CRITICAL',
      why='Christmas Day and Christmas Eve are the most popular proposal days (The Knot). Demand: 590 + 480 + 480 winter + 210 + smaller variants, KD 0-16, AIO SERPs. Strong ring purchase intent.',
      promote='NO', refresh='Annually by Oct')

topic(date='2026-10-29', template='BLOG-GIFTS', content_type='EVERGREEN',
      event='Anniversaries (year-round; Nov peak for anniversary jewellery)', event_date='n/a', publish_by='n/a (evergreen)', lead='Evergreen; anniversary jewelry peaks Nov (1.65); diamond anniversary peaks Feb (2.09).',
      title='Diamond anniversary: which anniversary is diamond, and diamond gifts by milestone year',
      primary='diamond anniversary',
      secondary=['60th anniversary diamond', 'anniversary jewelry', '10 year anniversary gift', 'anniversary gifts for her'],
      cluster='NEW:OCCASION_ANNIVERSARY',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='BLOG-GIFTS -> COM-WB / COM-FJ', spoke='Occasion spoke: anniversaries',
      parent='Gifts & occasions', related='BC-023; BC-008; BC-003',
      audience='Spouses marking milestone anniversaries', need='Which years are traditionally diamond, and which diamond gift suits each milestone',
      seasonal='LOW', festival='none (anniversaries)',
      hod='HIGH: eternity/anniversary bands and fine jewellery', commercial='HIGH',
      category='COM-WB; COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS', product='Eternity and half-eternity bands; tennis bracelets (verify live)', edu='EDU-RJG-02', target_id='',
      links=['BLOG-HUB', 'COM-WB', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS', 'BC-023'],
      cta='Shop anniversary bands / fine jewellery',
      cann='PASS: no Stage 15 owner. Kept distinct from BC-023 (eternity ring meaning): this post is milestone/occasion-led. Band shopping heads (anniversary band/ring) are left to COM-WB.',
      facts='none', priority='P2_HIGH',
      why='Demand: diamond anniversary 2,900 (AIO/video) + anniversary jewelry 1,600 + upside heads (10 year 33,100; for her 14,800). Evergreen with a direct band/jewellery link.',
      promote='NO', refresh='Yearly')

topic(date='2026-10-30', template='BLOG-INDUSTRY', content_type='FESTIVAL',
      event='Black Friday / Cyber Monday', event_date=EVENTS['Black Friday'] + ' / ' + EVENTS['Cyber Monday'], publish_by='2026-11-06', lead='4 weeks before Black Friday; Black Friday jewellery searches are ~10x in November, so the post must be indexed in early Nov.',
      title='Is Black Friday a good time to buy an engagement ring? The best time of year to buy diamonds and jewellery',
      primary='best time to buy an engagement ring',
      secondary=['best time to buy diamonds', 'best time of year to buy jewelry', 'is black friday a good time to buy an engagement ring'],
      cluster='NEW:BUYING_TIMING',
      intent='INFORMATIONAL', funnel='CONSIDERATION', hub='COM-ER; EDU-LG-10 (buying guide)', spoke='Black Friday strategy post (informational, not a deals page)',
      parent='Buying decisions', related='BC-016; BC-024',
      audience='Ring buyers weighing Black Friday sales against quality', need='Whether sales seasons are really cheaper, and what to check so a discount is real',
      seasonal='HIGH', festival='Black Friday; Cyber Monday; Christmas',
      hod='HIGH', commercial='HIGH: engagement rings; certification check',
      category='COM-ER', product='n/a', edu='EDU-LG-10, EDU-CERT-00, EDU-LG-05', target_id='EDU-LG-10',
      links=['BLOG-HUB', 'COM-ER', 'EDU-LG-10', 'EDU-CERT-00', 'EDU-LG-05', 'EDU-LG-00'],
      cta='Compare with confidence: certification guide -> engagement rings (and any live HOD offer page)',
      cann='BOUNDARY: EDU-LG-10 owns "how to choose a lab-grown diamond"; EDU-LG-05 owns price/value. This post covers TIMING only and links out. "black friday * deals" terms are NOT targeted (product-led SERPs; see backlog).',
      facts='Whether HOD runs a Black Friday offer (if yes, link the offer page; never state discounts that do not exist)', priority='P1_TIME_CRITICAL',
      why='Black Friday "deals" SERPs are product/retailer-led (all 14 measured deal terms with SERP data show product features), so a blog cannot credibly win them. The informational timing question (210 + 50 + 50, AIO/forum, KD 0, Dec peak 1.7) is winnable and helps buyers.',
      promote='CANDIDATE: merge the timing section into EDU-RJG-04 if that page is ever approved', refresh='Annually by Oct')

topic(date='2026-11-02', template='BLOG-GIFTS', content_type='FESTIVAL',
      event='Hanukkah', event_date=EVENTS['Hanukkah'], publish_by='2026-11-06', lead='~4.5 weeks before Hanukkah starts (Dec 4). "hanukkah jewelry" Nov 2.6, Dec 4.8.',
      title='Hanukkah jewelry gifts: diamond ideas for her across the eight nights',
      primary='hanukkah jewelry',
      secondary=['hanukkah gifts for her', 'hanukkah gift ideas'],
      cluster='NEW:GIFTS_HANUKKAH',
      intent='COMMERCIAL_RESEARCH', funnel='CONSIDERATION', hub='BC-004 holiday gift hub -> COM-FJ', spoke='Festival spoke: Hanukkah',
      parent='Holiday gifting', related='BC-004',
      audience='US shoppers buying Hanukkah gifts', need='Jewellery gift ideas that suit Hanukkah (no religious-symbol products unless HOD sells them)',
      seasonal='HIGH', festival='Hanukkah',
      hod='MEDIUM-HIGH: general fine jewellery; no Judaica', commercial='HIGH',
      category='COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS', product='Stud earrings; pendants (verify live)', edu='EDU-4C-00', target_id='',
      links=['BLOG-HUB', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS', 'BC-004'],
      cta='Shop earrings / necklaces / bracelets (shipping before Dec 4)', cann='PASS: festival-specific primary; the broad "hanukkah gifts" (5,400) is not targeted.',
      facts='Shipping cut-off for Dec 4 delivery', priority='P2_HIGH',
      why='Hanukkah starts Dec 4, three weeks before Christmas, so it needs its own earlier window. Demand: 140 + 30 + 720 (ideas, broader). Product-led SERP; medium winnability.',
      promote='NO', refresh='Annually (Hanukkah dates move)')

topic(date='2026-11-03', template='BLOG-STYLE', content_type='EVERGREEN',
      event='Style (Dec gift peak for tennis bracelets)', event_date='n/a', publish_by='2026-11-20', lead='Evergreen; "what is a tennis bracelet" Dec index 1.72.',
      title='What is a tennis bracelet? Why it is called that, and how to wear and stack one',
      primary='what is a tennis bracelet',
      secondary=['why is it called a tennis bracelet', 'how to wear a tennis bracelet', 'tennis bracelet stack', 'how to stack bracelets'],
      cluster='NEW:STYLE_TENNIS_BRACELET',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-FJ-BRACELETS', spoke='Style spoke: bracelets',
      parent='Styling', related='BC-006; BC-004',
      audience='Bracelet buyers and gift shoppers', need='What defines a tennis bracelet, where the name comes from, and how to wear it',
      seasonal='MEDIUM (gift peak)', festival='Christmas (gift demand)',
      hod='HIGH: 6+ tennis bracelets in catalogue', commercial='HIGH',
      category='COM-FJ-BRACELETS', product='Radiant Avenue, Crownline, Endless Orbit, Orbit Bezel tennis bracelets (verify live)', edu='EDU-4C-00; EDU-MET-00', target_id='',
      links=['BLOG-HUB', 'COM-FJ-BRACELETS', 'COM-FJ', 'COM-PDP', 'EDU-4C-00'],
      cta='Shop tennis bracelets',
      cann='PASS: "tennis bracelet" (135,000, product SERP) is a category head reserved for COM-FJ-BRACELETS (tennis subcategory is conditional) and is NOT targeted.',
      facts='none', priority='P2_HIGH',
      why='Demand: 3,600 + 3,600 + 1,000 + 590, KD 0, AIO/forum SERP. December gift peak. Strongest product link of the style posts. "How to measure bracelet size" is left to a future Education sizing page.',
      promote='CANDIDATE (jewellery-types guide) if Stage 14 is revised', refresh='Yearly')

topic(date='2026-11-05', template='BLOG-STYLE', content_type='EVERGREEN',
      event='Engagement season (Dec peak)', event_date=EVENTS['Engagement season'], publish_by='2026-11-30', lead='Evergreen; "ring stacking" Nov and Dec index 2.08.',
      title='How to stack rings: engagement ring, wedding band and eternity band combinations',
      primary='how to stack rings',
      secondary=['ring stacking', 'wedding band stack', 'how to stack wedding bands'],
      cluster='NEW:STYLE_RING_STACKING',
      intent='INFORMATIONAL', funnel='CONSIDERATION', hub='COM-WB', spoke='Style spoke: stacking',
      parent='Styling; engagement & wedding rings', related='BC-007; BC-023',
      audience='Engaged/married buyers adding bands', need='Which bands pair with which engagement ring styles and shapes',
      seasonal='MEDIUM-HIGH', festival='Engagement season; Christmas',
      hod='HIGH: bridal sets, eternity and half-eternity bands', commercial='HIGH',
      category='COM-WB; COM-ER', product='Bridal sets; eternity and half-eternity bands (verify live)', edu='EDU-SHP-00; EDU-MET-00', target_id='',
      links=['BLOG-HUB', 'COM-WB', 'COM-ER', 'EDU-SHP-00', 'EDU-MET-00', 'COM-PDP'],
      cta='Shop wedding bands and bridal sets',
      cann='PASS: no Stage 15 owner. EDU-MET-00 owns "do iridium bands stack" (metal question, excluded here). Distinct from BC-007 (order/hand etiquette).',
      facts='none', priority='P2_HIGH',
      why='Demand: ring stacking 40,500 (product SERP) + wedding band stack 9,900 + how to stack rings 590 (AIO/video, KD 0). December peak. Direct band sales link.',
      promote='NO', refresh='Yearly')

topic(date='2026-11-06', template='BLOG-STYLE', content_type='EVERGREEN',
      event='Anniversary / push-present gifting (Dec peak)', event_date='n/a', publish_by='2026-11-30', lead='Evergreen; "eternity ring meaning" Dec index 1.61.',
      title='Eternity ring meaning: when to give one, and eternity vs anniversary bands',
      primary='eternity ring meaning',
      secondary=['what is an anniversary ring', 'half eternity band vs full eternity'],
      cluster='NEW:STYLE_ETERNITY_MEANING',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-WB', spoke='Style spoke: band meanings',
      parent='Ring traditions', related='BC-018; BC-022; BC-003',
      audience='Spouses choosing an anniversary or milestone ring', need='What an eternity ring symbolises, when it is given, and full vs half',
      seasonal='MEDIUM', festival='Christmas; anniversaries',
      hod='HIGH: eternity and half-eternity bands', commercial='HIGH',
      category='COM-WB', product='Aurelia scalloped eternity ring; alternating pear eternity; half-eternity bands (verify live)', edu='EDU-RJG-02', target_id='',
      links=['BLOG-HUB', 'COM-WB', 'COM-PDP', 'EDU-RJG-02', 'BC-018'],
      cta='Shop eternity & anniversary bands',
      cann='PASS: heads "eternity ring/band" and "anniversary band/ring" (5,400-12,100, product SERPs) are left to COM-WB and not targeted. Resizing limits of full eternity bands link to EDU-RJG-02.',
      facts='Whether full eternity bands can be resized (HOD policy)', priority='P3_MEDIUM',
      why='Demand: 590 + 210 (+ product heads as upside), AIO SERP, KD 0. December peak. Direct band link.',
      promote='NO', refresh='Yearly')

topic(date='2026-11-09', template='BLOG-INDUSTRY', content_type='SEASONAL',
      event='Engagement season (ring-budget research peaks Oct-Jan)', event_date=EVENTS['Engagement season'], publish_by='2026-11-20', lead='Before the Dec/Jan peak ("average engagement ring cost" peaks Jan; "how much should an engagement ring cost" Dec 1.26).',
      title='Average engagement ring cost in 2026: what the latest survey data shows (dated industry note)',
      primary='average engagement ring cost',
      secondary=['engagement ring cost'],
      cluster='NEW:ENGAGEMENT_RING_COST_DATA',
      intent='INFORMATIONAL', funnel='CONSIDERATION', hub='COM-ER; EDU-LG-05', spoke='Industry note: dated cost data',
      parent='Buying decisions', related='BC-019; BC-016',
      audience='Ring buyers setting a budget', need='What people actually spend (dated, sourced), and how lab-grown changes the maths',
      seasonal='MEDIUM', festival='Engagement season',
      hod='HIGH', commercial='HIGH',
      category='COM-ER', product='n/a', edu='EDU-LG-05, EDU-LG-02, EDU-LG-00', target_id='EDU-LG-05',
      links=['BLOG-HUB', 'EDU-LG-00', 'EDU-LG-05', 'EDU-LG-02', 'COM-ER'],
      cta='See how lab-grown changes value (EDU-LG-05); browse engagement rings',
      cann='BOUNDARY (MEDIUM, FLAG FOR REVIEW): budgeting ADVICE ("engagement ring budget" 12,100; "how much to spend" 4,400; "how much should an engagement ring cost" 6,600) is an Education buying-guide intent (EDU-RJG-04, DEFERRED) and is NOT targeted. This note owns the dated survey-statistic intent only (Stage 13: dated market figures go in the Blog). EDU-LG-05 keeps lab-grown price questions.',
      facts='Named, dated third-party survey sources; no HOD price claims', priority='P2_HIGH',
      why='Demand: 8,100 + 2,900, KD 0-2, AIO/forum SERP. Dated statistics fit Stage 13\'s rule that time-bound figures live in the Blog. Clear lab-grown value angle for HOD.',
      promote='NO (dated by design)', refresh='Annually when new survey data is published')

topic(date='2026-11-10', template='BLOG-STYLE', content_type='EVERGREEN',
      event='Style (Dec gift peak)', event_date='n/a', publish_by='2026-11-30', lead='Evergreen; "huggie earrings" Dec index 1.69.',
      title='What are huggie earrings? Huggies vs hoops, and how to style them',
      primary='what are huggie earrings',
      secondary=['hoops vs huggies', 'how to style hoop earrings'],
      cluster='NEW:STYLE_HUGGIES',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-FJ-EARRINGS', spoke='Style spoke: earrings',
      parent='Styling', related='BC-004; BC-009',
      audience='Earring buyers and gift shoppers', need='What huggies are, how they differ from hoops, and how to wear them',
      seasonal='MEDIUM', festival='Christmas (gift demand)',
      hod='HIGH: huggies and hoops in catalogue', commercial='HIGH',
      category='COM-FJ-EARRINGS', product='Aurora triple-row huggies; Odette five-stone huggies; Trivessa huggies; hoops (verify live)', edu='EDU-MET-00', target_id='',
      links=['BLOG-HUB', 'COM-FJ-EARRINGS', 'COM-PDP', 'EDU-MET-00'],
      cta='Shop huggies and hoops',
      cann='PASS: "huggie earrings" (22,200, product SERP) is left to COM-FJ-EARRINGS (Hoops & Huggies subcategory, conditional) and not targeted.',
      facts='none', priority='P3_MEDIUM',
      why='Demand: 1,300 + 40 + 70, KD 0-10, AIO/video SERP. December gift peak. Catalogue depth in huggies/hoops.',
      promote='CANDIDATE (jewellery-types guide)', refresh='Yearly')

topic(date='2026-11-12', template='BLOG-STYLE', content_type='EVERGREEN',
      event='Style / trend', event_date='n/a', publish_by='n/a (evergreen)', lead='Evergreen.',
      title='Three-stone ring meaning: past, present and future (and the two-stone toi et moi alternative)',
      primary='three stone ring meaning',
      secondary=[],
      cluster='NEW:STYLE_THREE_STONE',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-ER (style subcategories conditional)', spoke='Style spoke: ring meanings',
      parent='Ring traditions', related='BC-031; BC-023',
      audience='Engagement and anniversary ring buyers', need='What a three-stone ring symbolises and how it compares with two-stone designs',
      seasonal='LOW', festival='none',
      hod='HIGH: Trinity oval three-stone, Trivelle three-stone, toi et moi two-stone in catalogue', commercial='HIGH',
      category='COM-ER', product='Trinity oval three-stone; Trivelle three-stone; Pear duo toi et moi (verify live)', edu='EDU-SHP-00; EDU-RJG-01', target_id='',
      links=['BLOG-HUB', 'COM-ER', 'COM-PDP', 'EDU-SHP-00', 'EDU-RJG-01'],
      cta='Shop three-stone and two-stone engagement rings',
      cann='PASS: "three stone engagement ring" (9,900) and "toi et moi ring" (27,100) are product-led style heads reserved for future COM-ER style subcategories and are NOT targeted; toi et moi is a comparison section only.',
      facts='none', priority='P4_LOW',
      why='Demand is small (110), but informational (AIO, KD 0) with direct products. LOW priority: it fills a slot only because it has a genuine product link; can be dropped if capacity is short.',
      promote='NO', refresh='Yearly')

topic(date='2026-11-13', template='BLOG-STYLE', content_type='EVERGREEN',
      event='Style / self-purchase (Dec peak)', event_date='n/a', publish_by='n/a (evergreen)', lead='Evergreen; Dec index 1.35.',
      title='What is a right-hand ring? The self-purchase diamond ring tradition',
      primary='right hand ring',
      secondary=['cocktail ring'],
      cluster='NEW:STYLE_RIGHT_HAND_RING',
      intent='MIXED', funnel='CONSIDERATION', hub='COM-FJ (Rings, conditional)', spoke='Style spoke: fashion rings',
      parent='Ring traditions', related='BC-011',
      audience='Women buying diamond rings for themselves', need='What a right-hand ring is and which styles suit it',
      seasonal='LOW', festival='New Year (treat-yourself) - weak',
      hod='HIGH: fashion/statement diamond rings in catalogue', commercial='HIGH',
      category='COM-FJ (Rings)', product='Asscher statement row ring; marquise cluster ring; Willow vine ring (verify live)', edu='EDU-SHP-00', target_id='',
      links=['BLOG-HUB', 'COM-FJ', 'COM-PDP', 'EDU-SHP-00'],
      cta='Shop fine-jewellery rings',
      cann='RISK (MEDIUM): the SERP is MIXED (AIO + products + forums; DataForSEO intent transactional). If the optional SERP check shows a product grid, retarget to the meaning angle or move to backlog. COM-FJ Rings subcategory is conditional (no owner conflict today).',
      facts='none', priority='P4_LOW',
      why='Demand 2,900 (+ cocktail ring 8,100), KD 0. Fits the fine-jewellery ring range, but intent is mixed. LOW priority pending SERP validation.',
      promote='NO', refresh='Yearly')

topic(date='2026-11-16', template='BLOG-GIFTS', content_type='FESTIVAL',
      event='Christmas (last-minute window Dec 14-24)', event_date=EVENTS['Christmas'], publish_by='2026-11-24', lead='~4 weeks before the last-minute surge (Dec index 11.5; Nov ~0). Must be indexed before mid-December.',
      title='Last-minute jewelry gifts: diamond pieces that still arrive before Christmas (and stocking stuffers)',
      primary='last minute christmas gifts for her',
      secondary=['last minute jewelry gifts', 'jewelry stocking stuffers', 'stocking stuffer jewelry'],
      cluster='NEW:GIFTS_LAST_MINUTE',
      intent='COMMERCIAL_RESEARCH', funnel='DECISION', hub='BC-004 holiday gift hub -> COM-FJ', spoke='Timing spoke: last minute',
      parent='Holiday gifting', related='BC-004',
      audience='Late holiday shoppers', need='Jewellery gifts that can still arrive in time, and gift-card/e-gift alternatives',
      seasonal='HIGH', festival='Christmas',
      hod='HIGH (conditional on shipping speed)', commercial='HIGH',
      category='COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS', product='In-stock ready-to-ship items (verify stock at publish)', edu='n/a', target_id='',
      links=['BLOG-HUB', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS', 'BC-004'],
      cta='Shop ready-to-ship pieces before the cut-off',
      cann='SERIES RISK (LOW): timing-specific primary, distinct from BC-004.',
      facts='BLOCKING: holiday shipping cut-off dates and which items ship fast (do not publish without them)', priority='P1_TIME_CRITICAL',
      why='The sharpest seasonal spike measured (Dec 11.5x). Must be indexed by early December. Demand 210 + 30 + 60, KD 0-11. Useful only if HOD can promise delivery, hence the blocking fact.',
      promote='NO', refresh='Annually by mid-Nov')

topic(date='2026-11-17', template='BLOG-GIFTS', content_type='FESTIVAL',
      event="New Year's Eve proposals", event_date=EVENTS["New Year's Eve"], publish_by='2026-12-01', lead='~6 weeks before NYE; Dec index 6-7x (NYE is a top-3 proposal day).',
      title="New Year's Eve proposal ideas: countdown proposals and ring timing",
      primary='new years eve proposal ideas',
      secondary=['new years proposal', 'new years eve proposal'],
      cluster='NEW:PROPOSAL_NYE',
      intent='INFORMATIONAL', funnel='CONSIDERATION', hub='BC-014 proposal hub -> COM-ER', spoke='Seasonal proposal spoke: NYE',
      parent='Proposal & engagement', related='BC-014; BC-017',
      audience='People planning a NYE proposal', need='NYE-specific proposal ideas and ordering the ring in time',
      seasonal='HIGH', festival="New Year's Eve",
      hod='HIGH', commercial='HIGH',
      category='COM-ER', product='Engagement rings (verify live)', edu='EDU-RJG-02', target_id='EDU-RJG-02',
      links=['BLOG-HUB', 'COM-ER', 'EDU-RJG-02', 'BC-014', 'BC-001', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS'],
      cta='Engagement rings / bespoke', cann='SEPARATE from BC-017 by date and intent (NYE spike is Dec-only, different ideas). Generic ideas link to BC-014.',
      facts='Delivery cut-off for Dec 31', priority='P3_MEDIUM',
      why='Small demand (90 + 70 + 40) but a 6-7x December spike and strong ring intent. KD 0.',
      promote='NO', refresh='Annually')

topic(date='2026-11-23', template='BLOG-STYLE', content_type='FESTIVAL',
      event="Holiday parties / New Year's Eve", event_date=EVENTS["New Year's Eve"], publish_by='2026-11-30', lead='~5 weeks before NYE; "new years eve jewelry" Dec index 1.93.',
      title="What jewelry to wear for New Year's Eve and holiday parties: diamond styling guide",
      primary='new years eve jewelry',
      secondary=['holiday party jewelry', 'holiday jewelry'],
      cluster='NEW:STYLE_HOLIDAY_PARTY',
      intent='MIXED', funnel='CONSIDERATION', hub='COM-FJ', spoke='Style spoke: occasion styling',
      parent='Styling', related='BC-006; BC-025',
      audience='Women dressing for holiday events', need='How to style statement diamond pieces for parties',
      seasonal='HIGH', festival="Holiday parties; New Year's Eve",
      hod='MEDIUM-HIGH: statement earrings and tennis bracelets', commercial='MEDIUM-HIGH',
      category='COM-FJ-EARRINGS; COM-FJ-BRACELETS; COM-FJ-NECKLACES', product='Drop earrings; statement hoops; tennis bracelets (verify live)', edu='n/a', target_id='',
      links=['BLOG-HUB', 'COM-FJ', 'COM-FJ-EARRINGS', 'COM-FJ-BRACELETS', 'COM-PDP'],
      cta='Shop statement earrings and bracelets',
      cann='RISK (MEDIUM): product-led SERPs (KD 14-17). A styling article is a secondary format there. PASS on ownership.',
      facts='none', priority='P4_LOW',
      why='Demand 480 + 880 + 40, but product-led SERPs. On-season and catalogue-relevant. LOW priority; drop first if capacity is short.',
      promote='NO', refresh='Annually')

topic(date='2026-12-01', template='BLOG-STYLE', content_type='SEASONAL',
      event='New year trend searches (peak Jan-Feb)', event_date='2027-01 to 2027-02', publish_by='2026-12-15', lead='~6-10 weeks before the Jan-Feb trend peak ("engagement ring trends 2026" peaked Feb 2026 at 3.46x).',
      title='Engagement ring trends for 2027: toi et moi, east-west, bezel and elongated shapes',
      primary='engagement ring trends',
      secondary=['engagement ring trends 2027', 'engagement ring trends 2026', 'popular engagement ring styles', 'most popular engagement ring styles', 'most popular engagement ring shape'],
      cluster='NEW:TRENDS_ENGAGEMENT_RINGS',
      intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-ER', spoke='Trend spoke; links to style/shape owners',
      parent='Trends', related='BC-026; BC-032',
      audience='Engagement-ring shoppers during proposal season', need='Which styles and shapes are trending now',
      seasonal='HIGH', festival='Engagement season; New Year',
      hod='HIGH: toi et moi, east-west, bezel, hidden halo, elongated shapes in catalogue', commercial='HIGH',
      category='COM-ER; COM-ER-SIDESTONE', product='Pear duo toi et moi; Solvienne east-west marquise; Cushion bezel solitaire; hidden-halo bridal sets (verify live)', edu='EDU-SHP-00; EDU-RJG-01', target_id='EDU-SHP-00',
      links=['BLOG-HUB', 'COM-ER', 'COM-ER-SIDESTONE', 'EDU-SHP-00', 'EDU-RJG-01', 'COM-PDP'],
      cta='Shop engagement rings by style',
      cann='BOUNDARY: EDU-SHP-00 owns shape choice (evergreen). This post owns the dated "what is trending" angle (Stage 13 framework: Blog for dated shape-trend pieces). Style heads (toi et moi 27,100; bezel 22,200; east west 4,400; hidden halo 8,100) are NOT targeted; they are reserved for conditional COM-ER style subcategories. One URL, refreshed yearly, year in title only.',
      facts='none', priority='P1_TIME_CRITICAL',
      why='Timing: must be indexed before the January-February trend peak. Demand 1,600 + 880 + variants, KD 0-22, AIO SERP. It also showcases trend styles that HOD stocks.',
      promote='NO', refresh='Annually in Dec (same URL)')

topic(date='2026-12-03', template='BLOG-STYLE', content_type='SEASONAL',
      event='New year trend searches (peak Jan)', event_date='2027-01', publish_by='2026-12-15', lead='~5-8 weeks before the January peak ("jewelry trends 2026" peaked Jan 2026).',
      title='Fine jewelry trends for 2027: diamond earrings, bracelets and necklaces to watch',
      primary='jewelry trends',
      secondary=['jewelry trends 2027', 'jewelry trends 2026', 'bracelet trends', 'earring trends', 'necklace trends'],
      cluster='NEW:TRENDS_FINE_JEWELRY',
      intent='COMMERCIAL_RESEARCH', funnel='AWARENESS', hub='COM-FJ', spoke='Trend spoke',
      parent='Trends', related='BC-031; BC-006; BC-021',
      audience='Fine-jewellery shoppers', need='What is trending in fine jewellery for the coming year',
      seasonal='HIGH', festival='New Year',
      hod='HIGH', commercial='HIGH',
      category='COM-FJ; COM-FJ-EARRINGS; COM-FJ-BRACELETS; COM-FJ-NECKLACES', product='Tennis bracelets; triple-row hoops; heart and solitaire pendants (verify live)', edu='EDU-MET-00', target_id='',
      links=['BLOG-HUB', 'COM-FJ', 'COM-FJ-EARRINGS', 'COM-FJ-BRACELETS', 'COM-FJ-NECKLACES', 'EDU-MET-00'],
      cta='Shop fine jewellery',
      cann='PASS: no Stage 15 owner. Kept distinct from BC-031 (engagement rings only). Fashion/costume trend angles are out of scope (fine diamond jewellery only).',
      facts='none', priority='P2_HIGH',
      why='Demand 2,900 + 2,400 + 1,000 bracelet trends, KD 0-34, AIO/forum SERPs. January peak, so publish early December. One URL, refreshed yearly.',
      promote='NO', refresh='Annually in Dec (same URL)')

topic(date='2026-12-15', template='BLOG-GIFTS', content_type='FESTIVAL',
      event="Valentine's Day 2027 (early SEO lead)", event_date=EVENTS["Valentine's Day"], publish_by='2026-12-31', lead="~8.5 weeks before Valentine's Day and ~3-4 weeks before the January surge ('valentines day jewelry': Dec 1,600 -> Jan 12,100 -> Feb 14,800).",
      title="Valentine's Day jewelry gift guide: diamond hearts, studs and pieces she will keep",
      primary='valentines day jewelry',
      secondary=['valentines day jewelry gifts', 'valentine gifts for her', 'valentines day gifts for her'],
      cluster='NEW:GIFTS_VALENTINES',
      intent='COMMERCIAL_RESEARCH', funnel='CONSIDERATION', hub='BLOG-GIFTS -> COM-FJ', spoke="Festival spoke: Valentine's",
      parent='Gifting', related='BC-034; BC-004',
      audience="Valentine's gift shoppers", need="Jewellery gifts for Valentine's Day, including heart pieces",
      seasonal='HIGH', festival="Valentine's Day",
      hod='HIGH: heart pendants, heart studs, clover necklaces', commercial='HIGH',
      category='COM-FJ-NECKLACES; COM-FJ-EARRINGS; COM-FJ-BRACELETS', product='Amora heart pendant; Amorette four-heart clover; Cherivelle heart studs; Heartlace tennis bracelet (verify live)', edu='EDU-4C-00', target_id='',
      links=['BLOG-HUB', 'COM-FJ-NECKLACES', 'COM-FJ-EARRINGS', 'COM-FJ-BRACELETS', 'COM-PDP'],
      cta="Shop Valentine's pieces",
      cann='PASS: festival-specific; broad heads (valentine gifts for her 22,200) are stretch secondaries on a non-jewellery SERP.',
      facts="Valentine's shipping cut-off (can be added in January)", priority='P1_TIME_CRITICAL',
      why="Research supports an early start. Measured demand rises ~8x from December to January, so the page must be indexed before January. Jewellery-specific demand 2,900 + 260; heads 22,200 + 8,100 as upside. Strong heart-jewellery catalogue.",
      promote='NO', refresh='Annually by mid-Dec')

topic(date='2026-12-22', template='BLOG-GIFTS', content_type='FESTIVAL',
      event="Valentine's Day 2027 proposals", event_date=EVENTS["Valentine's Day"], publish_by='2027-01-05', lead="~7.5 weeks before Valentine's Day; demand rises in January ('valentines day proposal': Dec 210 -> Jan 2,900 -> Feb 4,400).",
      title="Valentine's Day proposal ideas: romantic ways to propose on February 14",
      primary='valentines day proposal ideas',
      secondary=['valentines day proposal'],
      cluster='NEW:PROPOSAL_VALENTINES',
      intent='INFORMATIONAL', funnel='CONSIDERATION', hub='BC-014 proposal hub -> COM-ER', spoke="Seasonal proposal spoke: Valentine's",
      parent='Proposal & engagement', related='BC-014; BC-033',
      audience="People planning a Valentine's proposal", need="Valentine's proposal ideas and ordering the ring in time",
      seasonal='HIGH', festival="Valentine's Day",
      hod='HIGH', commercial='HIGH',
      category='COM-ER', product='Engagement rings (verify live)', edu='EDU-RJG-02', target_id='EDU-RJG-02',
      links=['BLOG-HUB', 'COM-ER', 'EDU-RJG-02', 'BC-014', 'BC-001', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS'],
      cta='Engagement rings / bespoke (order by late January)', cann='Separate from BC-017/BC-029 by date. Generic ideas link to BC-014.',
      facts="Order-by date for Feb 14 delivery", priority='P3_MEDIUM',
      why="Valentine's Day is the fifth most popular proposal day (The Knot). Demand 720 + 390 with a 6x February spike, KD 0-26. Publishing in late December gives it time to be indexed before the January rise.",
      promote='NO', refresh='Annually by mid-Dec')

# ---------------------------------------------------------------- build calendar rows
used_dates = {t['date'] for t in T}
assert len(used_dates) == len(T), 'two topics on one date'
T.sort(key=lambda t: t['date'])
cal = []
for i, t in enumerate(T, 1):
    d = dt.date.fromisoformat(t['date'])
    pk = t['primary']
    pv = vol(pk)
    np_ = NEW.get(pk, {})
    all_kws = [pk] + t['secondary']
    srcs = sorted({kw_source(k) for k in all_kws})
    combined = sum(v for v in (vol(k) for k in all_kws) if v)
    serp = ''
    if np_ and np_.get('serp_item_types'):
        flags = []
        if np_['serp_has_ai_overview'] == 'True': flags.append('AI_OVERVIEW')
        if np_['serp_product_led'] == 'True': flags.append('PRODUCT_FEATURES')
        if np_['serp_has_forums'] == 'True': flags.append('FORUMS')
        if np_['serp_has_video'] == 'True': flags.append('VIDEO')
        if np_['serp_has_paa'] == 'True': flags.append('PAA')
        serp = ' + '.join(flags) + ' (keyword_overview serp_item_types; top-10 URLs not validated)'
    elif pk in S15:
        serp = f"Stage 8 page type: {S15[pk]['serp_page_type'] or 'not validated'}"
    cal.append({
        'blog_id': f'BC-{i:03d}', 'planned_publish_date': t['date'], 'week': week_of(d), 'month': d.strftime('%B %Y'),
        'event_or_season': t['event'], 'content_type': t['content_type'], 'blog_category': t['template'],
        'blog_title_working': t['title'], 'primary_keyword': pk,
        'primary_keyword_volume': pv if pv is not None else 'n/a',
        'primary_keyword_peak': (np_.get('peak_month_last12') or '') + (f" (Nov idx {np_.get('nov_index')}, Dec idx {np_.get('dec_index')}, Feb idx {np_.get('feb_index')})" if np_ else ''),
        'primary_keyword_difficulty': np_.get('keyword_difficulty', '') if np_ else (S15.get(pk, {}).get('keyword_difficulty', '')),
        'secondary_keywords': '; '.join(fmt_kw(k) for k in t['secondary']),
        'combined_keyword_volume': combined,
        'keyword_source': ' + '.join(srcs), 'cluster_id': t['cluster'], 'search_intent': t['intent'], 'serp_signal': serp,
        'funnel_stage': t['funnel'], 'hub': t['hub'], 'spoke': t['spoke'], 'parent_topic': t['parent'], 'related_articles': t['related'],
        'target_audience': t['audience'], 'searcher_need': t['need'],
        'seasonal_relevance': t['seasonal'], 'festival_relevance': t['festival'], 'event_date': t['event_date'],
        'publish_by_date': t['publish_by'], 'seo_lead_time': t['lead'],
        'HOD_relevance': t['hod'], 'commercial_relevance': t['commercial'],
        'target_category': t['category'], 'target_product': t['product'], 'related_education_page': t['edu'],
        'related_target_page_id': t['target_id'], 'internal_link_targets': '; '.join(t['links']),
        'CTA_direction': t['cta'], 'cannibalization_check': t['cann'],
        'business_facts_required': t['facts'],
        'content_status': 'PLANNED_NOT_BRIEFED', 'priority': t['priority'], 'priority_reason': t['why'],
        'promote_to_education_flag': t['promote'], 'refresh_cycle': t['refresh'],
    })

# resolve BC-### placeholders written against the planned order (they were authored in date order)
# (IDs in related/link fields refer to the final sorted IDs; verified in QC)

# unused slots
unused = []
taken = {dt.date.fromisoformat(t['date']) for t in T}
reasons = {
    'W08': 'No further topic met the bar; Nov 19-20 left free for Black Friday week production of the gift series refresh (shipping cut-offs).',
    'W09': 'Thanksgiving / Black Friday week (Nov 26-27 holidays). All Black Friday demand measured is deal/product-led and not a Blog topic; no qualifying topic left.',
    'W10': 'Cyber Monday (Nov 30) and Dec 4: no further qualifying topic. Christmas content published now would be too late to rank for this season.',
    'W11': 'Too late for new Christmas content (under 3 weeks to Dec 25). Use this capacity to refresh BC-004/BC-028 cut-off dates and to produce Education owners (see summary).',
    'W12': 'Only the Valentine gift guide qualifies; other new topics would be weak.',
    'W13': 'Christmas week; only the Valentine proposal post qualifies.',
    'W14': 'Year-end; no qualifying topic. January-peak topics were already published in early December.',
}
for s in ALL_SLOTS:
    if s not in taken:
        wk = week_of(s)
        unused.append({'blog_id': f'SLOT-{s:%m%d}', 'planned_publish_date': s.isoformat(), 'week': wk, 'month': s.strftime('%B %Y'),
                       'content_status': 'UNUSED_SLOT', 'priority': 'n/a',
                       'priority_reason': reasons.get(wk[:3], 'No qualifying topic for this slot; weak topics were not invented.')})

cols = list(cal[0].keys())
with open(os.path.join(OUT, 'blog_content_calendar.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    rows = cal + [{**{c: '' for c in cols}, **u} for u in unused]
    rows.sort(key=lambda r: r['planned_publish_date'])
    w.writerows(rows)

json.dump({'scheduled': len(cal), 'unused_slots': len(unused), 'total_slots': len(ALL_SLOTS),
           'by_type': {k: sum(1 for c in cal if c['content_type'] == k) for k in ('EVERGREEN', 'SEASONAL', 'FESTIVAL')},
           'by_priority': {k: sum(1 for c in cal if c['priority'] == k) for k in ('P1_TIME_CRITICAL', 'P2_HIGH', 'P3_MEDIUM', 'P4_LOW')},
           'by_category': {k: sum(1 for c in cal if c['blog_category'] == k) for k in TEMPLATE_REQUIRED},
           'by_week': {wk: sum(1 for c in cal if c['week'] == wk) for wk in sorted({week_of(s) for s in ALL_SLOTS})}},
          open(os.path.join(OUT, 'scripts', 'build_stats.json'), 'w'), indent=1)
print('scheduled', len(cal), 'unused', len(unused))
