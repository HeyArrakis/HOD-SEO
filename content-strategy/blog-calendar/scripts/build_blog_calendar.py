"""Blog Content Calendar - HARD REVISION build (29 Sep - 31 Dec 2026).

Replaces the original 34-blog build (archived in scripts/archive/). Hand-authored topic decisions
(approved by the user after Round 2, 2026-09-29) plus generators. Local files only; no API call.

Inputs
  architecture/15_keyword_url_map.csv                          Stage 15 ownership + EXISTING_DATA
  content-strategy/blog-calendar/working/call1_processed.csv   NEW_RESEARCH R0 (keyword_overview, 292 kw)
  content-strategy/blog-calendar/revision/round1_merged_raw_keywords.csv  NEW_RESEARCH R1 (discovery)
  content-strategy/blog-calendar/revision/round3_processed.csv NEW_RESEARCH R3 (keyword_overview, 145 kw)
  content-strategy/blog-calendar/revision/round2_serp_analysis.csv  (SERP/PAA/AIO, 72 SERPs)
Output
  content-strategy/blog-calendar/blog_content_calendar.csv (single source of truth, updated in place)
  content-strategy/blog-calendar/blog_calendar_revision_log.csv (original 34 -> revised mapping)
Run: python3 content-strategy/blog-calendar/scripts/build_blog_calendar.py
"""
import csv, json, datetime as dt, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'content-strategy', 'blog-calendar')
P = lambda *a: os.path.join(ROOT, *a)

S15 = {r['normalized_keyword']: r for r in csv.DictReader(open(P('architecture/15_keyword_url_map.csv')))}
R0 = {r['keyword']: r for r in csv.DictReader(open(P('content-strategy/blog-calendar/working/call1_processed.csv')))}
R1 = {r['keyword']: r for r in csv.DictReader(open(P('content-strategy/blog-calendar/revision/round1_merged_raw_keywords.csv')))}
R3 = {r['keyword']: r for r in csv.DictReader(open(P('content-strategy/blog-calendar/revision/round3_processed.csv')))}
SERP = {r['keyword']: r for r in csv.DictReader(open(P('content-strategy/blog-calendar/revision/round2_serp_analysis.csv')))}

def _int(x):
    try: return int(float(x))
    except (TypeError, ValueError): return None

def vol(k):
    for s in (R0, R1, R3):
        if k in s and _int(s[k].get('search_volume')) is not None: return _int(s[k]['search_volume'])
    if k in S15: return _int(S15[k]['search_volume'])
    return None

def src(k):
    if k in S15: return 'EXISTING_DATA'
    if k in R0: return 'NEW_RESEARCH_R0' if R0[k]['search_volume'] != 'NOT_IN_DATAFORSEO_DB' else 'NEW_RESEARCH_R0_NO_DATA'
    if k in R1: return 'NEW_RESEARCH_R1'
    if k in R3: return 'NEW_RESEARCH_R3' if _int(R3[k].get('search_volume')) is not None else 'NEW_RESEARCH_R3_NO_DATA'
    return 'UNMEASURED'

def peak(k):
    if k in R0 and R0[k].get('peak_month_last12'):
        r = R0[k]; return f"{r['peak_month_last12']} (Nov idx {r['nov_index']}, Dec idx {r['dec_index']}, Feb idx {r['feb_index']})"
    if k in R1 and R1[k].get('peak_month'):
        r = R1[k]; return f"{r['peak_month']} (Nov idx {r['nov_idx']}, Dec idx {r['dec_idx']}, Feb idx {r['feb_idx']})"
    if k in R3: return f"Dec idx {R3[k].get('dec_index')}, Feb idx {R3[k].get('feb_index')}"
    return 'n/a'

def kd(k):
    for s, f in ((R0, 'keyword_difficulty'), (R1, 'kd'), (R3, 'keyword_difficulty')):
        if k in s and s[k].get(f) not in ('', None, 'None'): return s[k][f]
    return S15.get(k, {}).get('keyword_difficulty', '')

START, END = dt.date(2026, 9, 29), dt.date(2026, 12, 31)
SLOT_WEEKDAYS = (0, 1, 3, 4)
def week_of(d):
    monday = d - dt.timedelta(days=d.weekday()); first = START - dt.timedelta(days=START.weekday())
    return f"W{(monday - first).days // 7 + 1:02d} ({monday:%b %d}-{min(monday + dt.timedelta(days=6), END):%b %d})"
ALL_SLOTS = [START + dt.timedelta(days=i) for i in range((END - START).days + 1) if (START + dt.timedelta(days=i)).weekday() in SLOT_WEEKDAYS]

EV = {'Christmas': '2026-12-25', 'Hanukkah': '2026-12-04 (to 12-12)', 'Thanksgiving': '2026-11-26', 'Black Friday': '2026-11-27',
      'Cyber Monday': '2026-11-30', "New Year's Eve": '2026-12-31', "Valentine's Day": '2027-02-14', 'Diwali': '2026-11-08 (Dhanteras 11-06)',
      'Engagement season': "2026-11-26 to 2027-02-14 (Thanksgiving to Valentine's)"}
TEMPLATE_REQUIRED = {'BLOG-GIFTS': ['BLOG-HUB', 'COM-FJ-BRACELETS', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES'], 'BLOG-CRAFT': ['BLOG-HUB', 'COM-BESPOKE'],
                     'BLOG-STYLE': ['BLOG-HUB'], 'BLOG-INDUSTRY': ['BLOG-HUB', 'EDU-LG-00', 'EDU-LG-05'], 'BLOG-LAUNCH': ['BLOG-HUB', 'COM-ER', 'COM-FJ', 'COM-PDP']}
GIFT_LINKS = ['COM-FJ-EARRINGS', 'COM-FJ-NECKLACES', 'COM-FJ-BRACELETS']

T = []
def topic(**k): T.append(k)

# ============================ SCHEDULED TOPICS (28) ============================
topic(id='BC-001', status='KEPT (absorbs BC-010)', merged='BC-010', date='2026-09-29', template='BLOG-CRAFT', ctype='SEASONAL',
  event='Christmas / NYE / Valentine proposals (bespoke order lead time)', event_date=EV['Christmas'], publish_by='2026-10-09',
  lead='~12 weeks before Christmas. Confirmed HOD fact: bespoke typically takes 2-3 weeks to make plus ~6-9 days delivery (generally ~3-4 weeks, stone-dependent), so holiday enquiries need to arrive well before December.',
  title='How long does a custom engagement ring take? The bespoke process from design to delivery (and ordering in time for the holidays)',
  primary='how long does a custom engagement ring take', secondary=['custom engagement ring process', 'how to design your own engagement ring', 'custom ring cost', 'how is jewelry made', 'how are rings made', 'how is a diamond ring made'],
  cluster='NEW:BESPOKE_PROCESS (+ merged NEW:JEWELLERY_MAKING)', intent='INFORMATIONAL', funnel='CONSIDERATION', hub='COM-BESPOKE', spoke='Craft spoke: bespoke timeline + making stages', parent='Bespoke / craftsmanship', related='BC-017; BC-005',
  audience='Couples planning a holiday proposal who want a one-off ring', need='How long custom takes, each stage (consultation, CAD, casting, setting, finishing), and when to order',
  seasonal='HIGH (holiday order timing)', festival="Christmas; NYE; Valentine's (indirect)", hod='HIGH: HOD bespoke service with Surat manufacturing', commercial='HIGH: bespoke enquiry',
  category='COM-BESPOKE', product='n/a (bespoke service)', edu='EDU-RJG-01; EDU-SHP-00', target_id='', links=['BLOG-HUB', 'COM-BESPOKE', 'BRAND-ABOUT', 'EDU-RJG-01', 'EDU-SHP-00', 'COM-ER', 'EDU-MET-00'],
  cta='Book a bespoke consultation (COM-BESPOKE); order-by guidance stated as "typically"',
  paa='How long does it take to make a custom ring? [answer-first block: "typically 3-4 weeks at HOD, stone-dependent"] | What are the stages of making a custom ring? [numbered steps: consultation, CAD, casting, setting, polishing, delivery] | How is a ring made? [H2 - absorbed from BC-010] | Budget PAA (how much to spend) [link BC-024; not answered here]',
  aeo='Answer-first sentence with the typical timeline + stage-by-stage table (stage, typical time) + numbered process steps + "order-by for Christmas" callout (planning guidance, not a promise).',
  cann='BOUNDARY: commercial heads (custom engagement ring 40,500; design your own 5,400) stay with COM-BESPOKE. EDU-NAT-00 owns "how are diamonds made" (formation); the making section covers jewellery manufacture only. Budget PAA routed to BC-024.',
  facts='CONFIRMED: typical 2-3 weeks production + ~6-9 days delivery (generally ~3-4 weeks; stone-dependent; never guaranteed). Still needed: holiday cut-off decision.',
  lowjust="210/mo primary. Kept: strongest bespoke commercial assist in the calendar, a confirmed differentiating business fact (HOD typically ~3-4 weeks vs the AIO's generic 4-8 weeks), holiday timing, and first-hand craft (Stage 13's largest Blog gap). Absorbs BC-010's making-process demand (~370).",
  priority='P1_TIME_CRITICAL', why="Timing: must precede holiday bespoke orders. SERP MIXED, led by retailer process guides; AIO gives a stage-by-stage timeline. HOD's confirmed typical timeline is a differentiator. Direct bespoke lead-in.", promote='NO', refresh='Annually before October')

topic(id='BC-018', status='UPGRADED (re-scoped to by-year hub)', merged='', date='2026-10-01', template='BLOG-GIFTS', ctype='EVERGREEN',
  event='Anniversaries (year-round)', event_date='n/a', publish_by='n/a (evergreen)', lead='Evergreen; flat demand (Sep peak), so earliest publication maximises accumulation.',
  title='Anniversary gifts by year: the traditional and modern list (and where diamonds fit)',
  primary='anniversary gifts by year', secondary=['traditional anniversary gifts', 'modern anniversary gifts by year', 'what anniversary is diamond', 'diamond anniversary', '60th anniversary diamond', 'what is the 50th anniversary gift', 'what is the 60th anniversary gift', 'anniversary jewelry'],
  cluster='NEW:OCCASION_ANNIVERSARY_BY_YEAR', intent='INFORMATIONAL', funnel='AWARENESS', hub='BLOG-GIFTS -> COM-WB / COM-FJ', spoke='Anniversary hub; spoke BC-035 (10th)', parent='Gifts & occasions', related='BC-035; BC-023; BC-003',
  audience='Spouses marking anniversaries', need='The traditional and modern gift for each year, and which years suit jewellery',
  seasonal='LOW', festival='none', hod='HIGH: diamond (10th modern, 60th, 75th), gold (50th) and eternity bands', commercial='HIGH: eternity/anniversary bands; fine jewellery',
  category='COM-WB; COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS', product='Eternity and half-eternity bands; tennis bracelets; pendants (verify live)', edu='EDU-RJG-02', target_id='',
  links=['BLOG-HUB', 'COM-WB'] + GIFT_LINKS + ['BC-035', 'BC-023'], cta='Shop anniversary bands and fine jewellery',
  paa='What is the anniversary for each year? [year-by-year table: year | traditional | modern | jewellery idea] | What are normal anniversary gifts? [short answer] | What is 5 years of marriage called? [table row] | What anniversary is diamond? [answer block: 60th (and 75th); diamond is the modern 10th] | Is 10 years a diamond anniversary? [answer block + link BC-035]',
  aeo='Answer-first definition + full by-year table (traditional, modern) as the core asset + short answer blocks for diamond, gold and platinum years + link to the 10th-anniversary spoke.',
  cann='PASS: no Stage 15 owner. Distinct SERP from BC-035 (10 year; <2 shared URLs) and BC-023. "anniversary gifts diamond" (5,400, product SERP) and "anniversary gifts for her" (product/listicle SERP) are not targeted.',
  facts='Platinum availability (20th) - mention only if HOD sells platinum', lowjust='',
  priority='P2_HIGH', why='74,000/mo informational (by-year guides, The Knot, NYT, Wikipedia, Jared and Helzberg guides rank). AIO: early years + milestones. Replaces the weak "diamond anniversary" primary (SERP: cards, cakes, Kay products).', promote='NO', refresh='Yearly')

topic(id='BC-003', status='UPGRADED (primary)', merged='', date='2026-10-02', template='BLOG-GIFTS', ctype='EVERGREEN',
  event='Year-round occasion (new parents)', event_date='n/a', publish_by='n/a (evergreen)', lead='Evergreen; flat demand.',
  title='Push presents: what they are, when to give one, and jewellery ideas she will keep',
  primary='push present', secondary=['what is a push present', 'push present ideas', 'push present meaning', 'when do you give a push present', 'when did push presents become a thing'],
  cluster='NEW:OCCASION_PUSH_PRESENT', intent='INFORMATIONAL', funnel='AWARENESS', hub='BLOG-GIFTS -> COM-FJ', spoke='Occasion guide', parent='Gifts & occasions', related='BC-018; BC-023',
  audience='Partners of expecting parents', need='What a push present is, when to give it, typical budgets and jewellery ideas',
  seasonal='LOW', festival='none', hod='HIGH: studs, pendants and eternity bands are the typical push presents', commercial='HIGH',
  category='COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS; COM-WB', product='Solitaire studs; solitaire/heart pendants; half-eternity bands (verify live)', edu='EDU-RJG-02; EDU-4C-07', target_id='',
  links=['BLOG-HUB'] + GIFT_LINKS + ['COM-WB', 'EDU-RJG-02', 'COM-BESPOKE'], cta='Shop earrings / pendants / bands; bespoke for a personalised piece',
  paa='What is a push present? [answer-first definition] | What is a typical push present? [H2 list of jewellery ideas] | What is the average cost of a push present? [short answer, no invented statistics] | How soon after birth should you give a push gift? [short answer] | How common is a push present? [FAQ]',
  aeo='Definition-first opener + ideas list by jewellery type + short "when to give it" answer + FAQ.', cann='PASS: no Stage 15 owner; Stage 13 assigns occasions to the Blog.',
  facts='none', lowjust='', priority='P2_HIGH',
  why='Upgraded primary from 5,400 to 18,100. Both SERPs informational with jewellery retailers ranking (Ice Carats, Robinsons, Blue Nile); AIO definition-first then gift ideas.', promote='NO', refresh='Yearly')

topic(id='BC-004', status='KEPT (absorbs BC-012, BC-013, BC-020, BC-028 as sections)', merged='BC-012; BC-013; BC-020; BC-028', date='2026-10-05', template='BLOG-GIFTS', ctype='FESTIVAL',
  event='Christmas / Hanukkah / holiday gifting', event_date=EV['Christmas'], publish_by='2026-11-01',
  lead='11.5 weeks before Christmas and ~8.5 weeks before Hanukkah (Dec 4). Gift searches rise in November and peak in December. Refresh in early December with ready-to-ship guidance (same URL).',
  title='Holiday jewelry gift guide: diamond gifts by budget, recipient and style (Christmas and Hanukkah)',
  primary='christmas jewelry gifts', secondary=['holiday jewelry gift guide', 'jewelry gift guide', 'jewelry gift ideas', 'best jewelry gifts', 'jewelry gifts for mom', 'hanukkah jewelry', 'last minute jewelry gifts', 'jewelry stocking stuffers', 'christmas jewelry gifts for her'],
  cluster='NEW:HOLIDAY_JEWELRY_GIFTS', intent='COMMERCIAL_RESEARCH', funnel='CONSIDERATION', hub='BLOG-GIFTS hub -> COM-FJ', spoke='Seasonal gift hub; recipient spokes BC-008, BC-009', parent='Holiday gifting', related='BC-008; BC-009; BC-003',
  audience='US holiday shoppers buying diamond jewellery', need='Which jewellery makes a good gift at each budget and for each recipient (incl. mom), Hanukkah timing, and what still arrives in time',
  seasonal='HIGH', festival='Christmas; Hanukkah', hod='HIGH', commercial='HIGH',
  category='COM-FJ; COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS', product='Stud earrings; tennis bracelets; solitaire and heart pendants (verify live)', edu='EDU-RJG-02; EDU-4C-00; EDU-LG-02', target_id='',
  links=['BLOG-HUB', 'COM-FJ'] + GIFT_LINKS + ['COM-BESPOKE', 'EDU-RJG-02', 'EDU-4C-00', 'BC-008', 'BC-009'], cta='Shop by category; returns and shipping policy; bespoke for one-offs',
  paa='What is the best jewelry to give as a Christmas gift? [answer-first + H2 list] | What is the 2:1:1 rule in jewelry? [FAQ one-liner; 70/mo] | What is the hottest jewelry right now? [short answer, link BC-032] | What is the 5 gift rule for Christmas? [not answered - not jewellery]',
  aeo='Answer-first "best jewellery gifts" summary + budget-tier table + recipient sections (wife -> BC-008, girlfriend -> BC-009, mom, luxury) + Hanukkah timing box + ready-to-ship section refreshed in December.',
  cann='SERIES: hub owns generic holiday jewellery gift intent; BC-008/BC-009 keep recipient primaries (their SERPs share 2 URLs with each other, not with the hub). Removed posts (mom, luxury, Hanukkah, last minute) become sections, not URLs. Broad non-jewellery heads (christmas gifts for her/wife/mom) are not targeted.',
  facts='Holiday shipping cut-offs and returns window (needed for the December refresh)', lowjust='',
  priority='P1_TIME_CRITICAL', why='Timing: indexed before the November rise. SERP MIXED; retailer holiday gift guides rank alongside category pages. Consolidates four weak/failed posts into one hub.', promote='NO', refresh='Annually by October + December refresh (same URL)')

topic(id='BC-035', status='NEW (NEW-01)', merged='', date='2026-10-06', template='BLOG-GIFTS', ctype='EVERGREEN',
  event='Anniversaries (year-round)', event_date='n/a', publish_by='n/a (evergreen)', lead='Evergreen; flat demand.',
  title='10 year anniversary gift ideas: tin, aluminium and the modern diamond tradition',
  primary='10 year anniversary gift', secondary=['10 year anniversary gift traditional and modern', '10 year anniversary gift for wife', 'anniversary gift 10th', '10 year anniversary gift modern', '10 year anniversary gift for couple'],
  cluster='NEW:OCCASION_ANNIVERSARY_10TH', intent='COMMERCIAL_RESEARCH', funnel='CONSIDERATION', hub='BC-018 anniversary hub -> COM-WB', spoke='Anniversary spoke (10th)', parent='Gifts & occasions', related='BC-018; BC-023',
  audience='Couples reaching 10 years of marriage', need='The traditional (tin/aluminium) and modern (diamond) 10th-anniversary gift, with ideas',
  seasonal='LOW', festival='none', hod='HIGH: diamond jewellery is the modern 10th-anniversary gift', commercial='HIGH',
  category='COM-WB; COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS', product='Eternity bands; diamond studs; tennis bracelets (verify live)', edu='EDU-4C-00', target_id='',
  links=['BLOG-HUB', 'COM-WB'] + GIFT_LINKS + ['BC-018', 'BC-023'], cta='Shop diamond anniversary gifts',
  paa='What is a traditional gift for a 10 year anniversary? [answer-first: tin/aluminium] | What represents 10 years of marriage? [short answer] | What stone is 10 years of marriage? [answer block: diamond (modern)] | Is a 10 year anniversary a big deal? [FAQ]',
  aeo='Answer-first (traditional tin/aluminium; modern diamond) + ideas grouped Traditional / Modern diamond / Sentimental (mirrors the AIO sections) + FAQ.',
  cann='PASS: no Stage 15 owner; separate SERP from BC-018 (<2 shared URLs); male-recipient variants (for him/husband) are not targeted.', facts='none', lowjust='',
  priority='P2_HIGH', why='33,100/mo. SERP MIXED (Amazon/Etsy + "Tin, Diamond" guides); the AIO has a dedicated "Modern Diamond Ideas" section, a direct HOD fit.', promote='NO', refresh='Yearly')

topic(id='BC-036', status='NEW (NEW-02)', merged='', date='2026-10-08', template='BLOG-STYLE', ctype='EVERGREEN',
  event='Engagement season (evergreen)', event_date=EV['Engagement season'], publish_by='2026-11-15', lead='Evergreen; publish before engagement season.',
  title='What finger does a wedding ring go on? (And which hand for the engagement ring)',
  primary='what finger does a wedding ring go on', secondary=['wedding ring finger', 'what hand does engagement ring go on', 'which hand is the ring finger', 'what finger does a ring go on', 'why is the wedding ring on the left hand', 'which hand does engagement ring go on', 'what hand does a wedding ring go on in america'],
  cluster='NEW:RING_TRADITION_FINGER_HAND', intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-WB / COM-ER', spoke='Ring traditions spoke', parent='Ring traditions', related='BC-007; BC-037; BC-038; BC-039',
  audience='Newly engaged and married people; gift buyers', need='Which finger and hand, why the left hand, and cultural differences',
  seasonal='MEDIUM', festival='Engagement season', hod='HIGH', commercial='MEDIUM-HIGH: wedding bands, bridal sets',
  category='COM-WB; COM-ER', product='Bridal sets; wedding bands (verify live)', edu='EDU-RJG-02', target_id='', links=['BLOG-HUB', 'COM-WB', 'COM-ER', 'EDU-RJG-02', 'BC-007', 'BC-038'],
  cta='Shop wedding bands and bridal sets; ring size guide',
  paa='Is the wedding ring on the left or right finger? [answer-first] | Where do married men wear their rings? [H3] | Why do you wear a wedding ring on your right hand? [H2 regional/cultural table] | Which finger do you propose on? [short answer] | Which finger ring means single? [link BC-038]',
  aeo='Answer-first sentence (fourth finger, left hand, in the US) + country/culture table (left vs right) + "why the left hand" history + one line on stacking order linking to BC-007.',
  cann='BOUNDARY: shares 2 top-10 URLs with the "what hand does engagement ring go on" SERP (one article). BC-007 owns ORDER/stacking etiquette (<2 shared URLs). BC-038 owns meanings of other fingers. EDU-RJG-02 owns ring SIZE.',
  facts='none', lowjust='', priority='P2_HIGH', why='27,100 + wedding ring finger 18,100 + what hand 6,600 + variants. Informational (retailer guides, Wikipedia, Reddit); AIO: left fourth finger, regional differences, why left, stacking.', promote='CANDIDATE (Ring traditions hub)', refresh='Yearly')

topic(id='BC-006', status='UPGRADED (primary)', merged='', date='2026-10-09', template='BLOG-STYLE', ctype='EVERGREEN',
  event='Style (Nov peak)', event_date='n/a', publish_by='n/a (evergreen)', lead='Evergreen; necklace layering peaks in November (1.56x).',
  title='Necklace layering: how to layer necklaces by length, weight and pendant (without tangling)',
  primary='necklace layering', secondary=['how to layer necklaces', 'layering necklaces', 'how to keep layered necklaces from tangling', 'popular layered necklaces', 'necklace layering lengths'],
  cluster='NEW:STYLE_NECKLACE_LAYERING', intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-FJ-NECKLACES', spoke='Style spoke: necklaces', parent='Styling', related='BC-021; BC-025',
  audience='Women buying or styling fine necklaces', need='Length rules, combinations, tangle prevention',
  seasonal='LOW', festival='none', hod='HIGH: solitaire, pendant, station, lariat and T-bar pieces', commercial='HIGH',
  category='COM-FJ-NECKLACES', product='Solitaire pendants; station necklace; lariat; T-bar (verify live)', edu='EDU-MET-00', target_id='', links=['BLOG-HUB', 'COM-FJ-NECKLACES', 'COM-FJ', 'EDU-MET-00', 'COM-PDP'],
  cta='Shop necklaces & pendants',
  paa='What is the rule for layering necklaces? [answer-first: ~2-inch length difference] | What is the trick for layering necklaces? [numbered steps] | How do you keep layered necklaces from tangling? [H2 tips] | Is layering necklaces in style in 2026? [short answer, link BC-032] | What is the 2:1:1 rule in jewelry? [FAQ one-liner]',
  aeo='Answer-first rule + length chart (14", 16", 18", 20"+) + step-by-step build + anti-tangle tips.',
  cann='PASS: the two phrasings share 4 top-10 URLs (one intent). Product-led layered-necklace sets are not targeted. The necklace length chart remains a future Education gap (backlog).',
  facts='none', lowjust='', priority='P2_HIGH', why='Upgraded to 14,800 (+ "layering necklaces" 14,800, same demand group; "how to layer necklaces" 2,400). Guide-led SERP (David Yurman, Catbird, Mejuri, Brilliant Earth); AIO: 2-inch rule + tangle prevention.', promote='CANDIDATE (styling hub)', refresh='Yearly')

topic(id='BC-008', status='KEPT (P3, commercial-lean flag)', merged='', date='2026-10-12', template='BLOG-GIFTS', ctype='SEASONAL',
  event='Christmas / anniversaries', event_date=EV['Christmas'], publish_by='2026-11-01', lead='~10.5 weeks before Christmas; wife-gift searches ~4x in December.',
  title='Jewelry gifts for your wife: meaningful diamond pieces she will actually wear',
  primary='jewelry gifts for wife', secondary=['best jewelry gifts for wife', 'meaningful jewelry for wife', 'christmas gifts for wife jewelry', 'gifts for wife who has everything'],
  cluster='NEW:GIFTS_RECIPIENT_WIFE', intent='COMMERCIAL_RESEARCH', funnel='CONSIDERATION', hub='BC-004 gift hub -> COM-FJ', spoke='Recipient spoke: wife', parent='Holiday gifting', related='BC-004; BC-018',
  audience='Husbands/partners', need='Jewellery ideas matched to her style, with safe-sizing advice', seasonal='HIGH', festival='Christmas; anniversaries', hod='HIGH', commercial='HIGH',
  category='COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS; COM-WB', product='Tennis bracelets; eternity bands; drop earrings (verify live)', edu='EDU-RJG-02', target_id='',
  links=['BLOG-HUB'] + GIFT_LINKS + ['COM-WB', 'BC-004'], cta='Shop gifts by category',
  paa='What is the best jewelry to gift my wife? [answer-first] | What are some good jewelry gift ideas for my wife? [H2 list] | What to get your wife if she has everything? [H2] | What is the 2:1:1 rule for jewelry? [FAQ one-liner]',
  aeo='Answer-first pick (studs / pendant / tennis bracelet) + ideas grouped by style + "no ring-size risk" tip + FAQ.',
  cann='SERIES: shares 2 URLs with BC-009 (related, distinct recipients). Broad "christmas gifts for wife" (27,100; generic non-jewellery SERP) is not targeted.', facts='Returns window; shipping cut-off', lowjust='',
  priority='P3_MEDIUM', why='Commercial-leaning SERP (Jared, Kay, Tiffany, Helzberg categories) with editorial listicles from The Knot and Byrdie. December peak. FLAG: a commercial "gifts for her/wife" collection may be the stronger owner later.', promote='NO', refresh='Annually by October')

topic(id='BC-009', status='KEPT (P3, commercial-lean flag)', merged='', date='2026-10-13', template='BLOG-GIFTS', ctype='SEASONAL',
  event='Christmas / first holidays together', event_date=EV['Christmas'], publish_by='2026-11-01', lead='~10.5 weeks before Christmas.',
  title='Jewelry gifts for your girlfriend: first-Christmas and meaningful diamond ideas',
  primary='jewelry gifts for girlfriend', secondary=['first christmas gift for girlfriend', 'first christmas together gift', 'necklaces for girlfriend birthday', 'meaningful necklaces for girlfriend'],
  cluster='NEW:GIFTS_RECIPIENT_GIRLFRIEND', intent='COMMERCIAL_RESEARCH', funnel='CONSIDERATION', hub='BC-004 gift hub -> COM-FJ', spoke='Recipient spoke: girlfriend', parent='Holiday gifting', related='BC-004; BC-011',
  audience="Partners buying a girlfriend's first major jewellery gift", need='Meaningful gifts that do not imply a proposal; no ring-size risk', seasonal='HIGH', festival='Christmas', hod='HIGH', commercial='HIGH',
  category='COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-FJ-BRACELETS', product='Heart pendants; huggies; stud earrings (verify live)', edu='EDU-RJG-02', target_id='',
  links=['BLOG-HUB'] + GIFT_LINKS + ['BC-004', 'BC-011'], cta='Shop pendants and earrings',
  paa='What is the best jewelry to gift to my girlfriend? [answer-first] | What is a good jewelry gift for my girlfriend? [H2 list] | What is the 5 gift rule for girlfriends? [not answered - not jewellery] | What is the 3 month rule for rings? [link BC-024]',
  aeo='Answer-first + ideas by relationship stage + promise-ring link + FAQ.', cann='SERIES: see BC-008. Promise rings are linked (BC-011), not covered.', facts='Returns window; shipping cut-off', lowjust='',
  priority='P3_MEDIUM', why='Same pattern as BC-008 (category-led with The Knot and Swarovski guides ranking). December peak.', promote='NO', refresh='Annually by October')

topic(id='BC-007', status='KEPT (boundary with BC-036)', merged='', date='2026-10-15', template='BLOG-STYLE', ctype='EVERGREEN',
  event='Engagement season (evergreen)', event_date=EV['Engagement season'], publish_by='2026-11-15', lead='Evergreen; publish before engagement season.',
  title='How to wear your engagement ring and wedding band: order, wedding-day etiquette and soldering',
  primary='how to wear engagement ring and wedding band', secondary=['which ring goes on first wedding or engagement', 'do you wear your engagement ring on your wedding day', 'does the wedding band go on first', 'correct way proper way to wear wedding ring set', 'should engagement ring and wedding band match'],
  cluster='NEW:STYLE_BRIDAL_WEAR', intent='INFORMATIONAL', funnel='RETENTION', hub='COM-WB / COM-ER', spoke='Style spoke: bridal wear order', parent='Ring traditions', related='BC-036; BC-022; BC-037',
  audience='Engaged and newly married couples', need='Which ring goes first, what to do on the wedding day, soldering vs separate', seasonal='MEDIUM', festival='Engagement season', hod='HIGH: bridal sets and bands', commercial='HIGH',
  category='COM-WB; COM-ER', product='Bridal ring sets (verify live)', edu='EDU-RJG-02; EDU-MET-00', target_id='', links=['BLOG-HUB', 'COM-WB', 'COM-ER', 'EDU-RJG-02', 'EDU-MET-00', 'BC-036'],
  cta='Shop wedding bands / bridal sets',
  paa='Which goes on first, the engagement or wedding ring? [answer-first: band first, closest to the heart] | Why do you not wear your engagement ring on your wedding day? [H2] | Are you supposed to wear a wedding band and an engagement ring together? [H2] | Do you wear an engagement ring and a wedding band all the time? [FAQ]',
  aeo='Answer-first order + wedding-day switch steps (numbered) + alternatives list + soldering pros/cons table.',
  cann='BOUNDARY: <2 shared URLs with the finger/hand SERP; "which hand" secondaries moved to BC-036. BC-022 covers multi-ring stacking design.', facts='Whether HOD offers ring soldering', lowjust='',
  priority='P2_HIGH', why='3,600 + wedding-day 1,000 + order variants. Informational (retailer guides, Vogue, forums); AIO: traditional order, wedding day, alternatives, soldering.', promote='CANDIDATE (Ring traditions hub)', refresh='Yearly')

topic(id='BC-011', status='KEPT (finger topic split to BC-039)', merged='', date='2026-10-16', template='BLOG-GIFTS', ctype='EVERGREEN',
  event='Holiday gifting / engagement season (Dec peak)', event_date=EV['Christmas'], publish_by='2026-11-15', lead='Evergreen with a December peak (1.38x).',
  title='What is a promise ring? Meaning, who gives one, and how it differs from an engagement ring',
  primary='what is a promise ring', secondary=['promise ring vs engagement ring', 'what does a promise ring mean from a boyfriend'],
  cluster='NEW:OCCASION_PROMISE_RING', intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-FJ', spoke='Ring traditions spoke', parent='Ring traditions', related='BC-039; BC-009; BC-037',
  audience='Young couples; gift buyers not ready to propose', need='What it means, when to give one, how it differs from an engagement ring', seasonal='MEDIUM', festival='Christmas', hod='MEDIUM-HIGH: diamond fashion rings and bands', commercial='MEDIUM',
  category='COM-FJ (Rings, conditional)', product='Diamond fashion rings; half-eternity bands (verify live)', edu='EDU-RJG-02', target_id='', links=['BLOG-HUB', 'COM-FJ'] + GIFT_LINKS + ['EDU-RJG-02', 'COM-ER', 'BC-039'],
  cta='Shop fine-jewellery rings; see engagement rings when ready',
  paa='How serious is a promise ring? [answer block] | When should a girl receive a promise ring? [H3] | Can I give my boyfriend a promise ring? [H3] | Do I kneel for a promise ring? [FAQ] | What finger is for a promise ring? [one line + link BC-039]',
  aeo='Definition-first + meanings list + comparison table (promise vs engagement ring) + FAQ.', cann='SPLIT: the finger question lives in BC-039 (separate SERP, <2 shared URLs). "promise rings" (301,000) is a shopping head, not targeted.', facts='none', lowjust='',
  priority='P2_HIGH', why='22,200/mo. MIXED but retailer-guide led; AIO: meanings, look, how to wear.', promote='CANDIDATE (Ring traditions hub)', refresh='Yearly')

topic(id='BC-037', status='NEW (NEW-03)', merged='', date='2026-10-19', template='BLOG-STYLE', ctype='EVERGREEN',
  event='Engagement season (evergreen)', event_date=EV['Engagement season'], publish_by='2026-11-15', lead='Evergreen; flat demand (Dec 1.05x). Published mid-October so it is indexed before engagement season.',
  title='Engagement ring vs wedding ring: what is the difference (and do you need both)?',
  primary='engagement ring vs wedding ring', secondary=['wedding ring vs engagement ring vs wedding band', 'wedding ring vs wedding band', 'engagement ring and wedding band rules', 'engagement ring vs wedding ring price'],
  cluster='NEW:RING_TRADITION_COMPARISON', intent='INFORMATIONAL', funnel='CONSIDERATION', hub='COM-ER / COM-WB', spoke='Ring traditions spoke', parent='Ring traditions', related='BC-036; BC-007; BC-011',
  audience='Couples planning engagement and wedding purchases', need='The difference, whether you need both, and how they pair', seasonal='MEDIUM', festival='Engagement season', hod='HIGH', commercial='HIGH: engagement rings, bands, bridal sets',
  category='COM-ER; COM-WB', product='Bridal sets (verify live)', edu='EDU-LG-10', target_id='', links=['BLOG-HUB', 'COM-ER', 'COM-WB', 'BC-036', 'BC-007', 'BC-024'],
  cta='Shop bridal sets; engagement rings; wedding bands',
  paa='Can I use my engagement ring as a wedding ring? [H2] | Is it normal to wear an engagement ring and a wedding ring? [short answer, link BC-007] | Should your engagement ring be different than your wedding ring? [H3] | Is it okay if my wedding band is thicker than my engagement ring? [FAQ] | What is the three month ring rule? [link BC-024]',
  aeo='Answer-first difference + side-by-side comparison table (purpose, when given, design, cost) + FAQ.', cann='PASS: no Stage 15 owner; <2 shared URLs with BC-036 and BC-007.', facts='none', lowjust='',
  priority='P2_HIGH', why='18,100 (+ the "vs wedding band" group 18,100). 6 of 7 top results are retailer comparison guides; AIO gives side-by-side definitions.', promote='CANDIDATE (Ring traditions hub)', refresh='Yearly')

topic(id='BC-014', status='KEPT', merged='', date='2026-10-20', template='BLOG-GIFTS', ctype='EVERGREEN',
  event='Engagement season (evergreen)', event_date=EV['Engagement season'], publish_by='2026-11-15', lead='Evergreen; Dec index 1.27.',
  title='Proposal ideas: how to plan a proposal she will remember (with the ring at the centre)',
  primary='proposal ideas', secondary=['how to propose', 'how to plan a proposal', 'proposal ideas at home', 'romantic proposal ideas', 'which knee do you propose on'],
  cluster='NEW:PROPOSAL_PLANNING', intent='INFORMATIONAL', funnel='CONSIDERATION', hub='COM-ER', spoke='Proposal series hub; seasonal spokes BC-017, BC-034', parent='Proposal & engagement', related='BC-017; BC-034; BC-016',
  audience='People planning to propose', need='Ideas, planning steps and etiquette, with the ring as the centre', seasonal='MEDIUM', festival='Engagement season', hod='MEDIUM-HIGH (ring moment; wedding planning excluded)', commercial='HIGH: engagement rings; ring size',
  category='COM-ER', product='Engagement rings (verify live)', edu='EDU-RJG-02; EDU-LG-10', target_id='EDU-RJG-02', links=['BLOG-HUB', 'COM-ER', 'EDU-RJG-02', 'EDU-LG-10', 'COM-BESPOKE'] + GIFT_LINKS,
  cta='Choose the ring (engagement rings / bespoke); get her size right (EDU-RJG-02)',
  paa="How do you propose in a unique way? [H2 idea groups: intimate / outdoor / creative] | Do and don'ts of proposing? [H2 two-column list] | Which knee do I propose on? [answer block: left knee traditionally] | What is quiet proposing? [FAQ] | What should I say when proposing? [H3]",
  aeo="Answer-first principle + idea groups mirroring the AIO (intimate, outdoor, creative) + planning checklist (numbered) + dos/don'ts list + FAQ.",
  cann='PASS. "how to propose" has its own SERP but a shared PAA set; kept as a section so proposal content stays ring-centred (D-BC-06). Ring-size-in-secret stays on EDU-RJG-02.', facts='none', lowjust='',
  priority='P2_HIGH', why='14,800 (KD 9) + how to propose 3,600 + romantic 2,900 + knee 1,300. Informational (lists, social, forums).', promote='NO', refresh='Yearly')

topic(id='BC-015', status='KEPT (absorbs BC-002)', merged='BC-002', date='2026-10-22', template='BLOG-INDUSTRY', ctype='FESTIVAL',
  event='Diwali (Surat) / lab-grown industry note', event_date=EV['Diwali'], publish_by='2026-10-30', lead='~2.5 weeks before Diwali (Nov 8; later than 2025). Industry context is time-bound (dated).',
  title='Where are lab-grown diamonds made? Surat, India, China and the 2026 lab-grown market (dated industry note)',
  primary='where are lab grown diamonds made', secondary=['surat diamonds', 'surat diamond industry', 'lab grown diamond market', 'lab grown diamond news', 'lab grown diamond trends', 'future of lab grown diamonds', 'lab grown diamonds industry'],
  cluster='NEW:INDUSTRY_GEOGRAPHY + CL-014 (Blog primary) + CL-026', intent='INFORMATIONAL', funnel='AWARENESS', hub='EDU-LG-00 / BRAND-ABOUT', spoke='Industry Notes spoke', parent='Lab-grown diamonds; craftsmanship', related='BC-005; BC-001',
  audience="Lab-grown buyers asking about origin; readers of HOD's Surat heritage", need="Which countries grow and cut lab-grown diamonds, Surat's role, and what changed in the market this year",
  seasonal='LOW', festival='Diwali (Surat context)', hod="HIGH: HOD's Surat manufacturing link", commercial='MEDIUM: trust -> lab-grown collection',
  category='COM-ER; COM-FJ', product='n/a', edu='EDU-LG-00; EDU-LG-03; EDU-LG-05; EDU-LG-07', target_id='EDU-LG-00',
  links=['BLOG-HUB', 'EDU-LG-00', 'EDU-LG-05', 'EDU-LG-03', 'EDU-LG-07', 'BRAND-ABOUT', 'COM-BESPOKE'], cta='Read how lab-grown diamonds are grown (EDU-LG-00/LG-03); meet the HOD workshop (About)',
  paa='Where are most lab-grown diamonds produced? [answer-first: India and China lead] | Why is Surat famous for diamonds? [H2: cuts ~9 of 10 diamonds (per AIO; cite a primary source)] | Are lab-grown diamond prices falling? [one line + link EDU-LG-05] | What is the downside to lab-grown diamonds? [link EDU-LG-02]',
  aeo='Answer-first geography sentence + country table (growing vs cutting) + Surat section + dated 2026 market facts with sources.',
  cann='BOUNDARY: EDU-LG-00 owns HOW lab-grown diamonds are made; EDU-LG-03 owns CVD/HPHT; EDU-LG-05 owns price/value ("getting cheaper" not targeted); EDU-NAT-00 owns natural formation; EDU-GEN-01 owns composition. EDU-LG-02 owns lab-grown popularity questions ("when did lab grown diamonds become popular" removed as a secondary - near-match to an LG-02 keyword). This note owns WHERE + dated market context.',
  facts='HOD sourcing geography; any ethics claim wording (Stage 19 BLOCKING for claims); dated market sources',
  lowjust='210/mo primary (combined ~1,000 with market/news/Surat). Kept: unique HOD Surat angle, Stage 13/14 assign CL-014 market notes to the Blog, informational SERP (AIO names India and China), Diwali timing; absorbs weak BC-002 so the market topic has no thin post of its own.',
  priority='P2_HIGH', why='Merged industry piece (geography + Surat + market). SERP MIXED informational (ABC, VRAI, Brilliant Earth, Wikipedia, Forbes).', promote='NO', refresh='Every 6-12 months (dated)')

topic(id='BC-024', status='UPGRADED (combined cost + budget article, user-approved)', merged='', date='2026-10-23', template='BLOG-INDUSTRY', ctype='SEASONAL',
  event='Engagement season (cost research peaks Dec-Jan)', event_date=EV['Engagement season'], publish_by='2026-11-20', lead='Before the December/January peak ("how much to spend" Dec 1.34x; "average cost" peaks in January).',
  title='How much should an engagement ring cost? Average prices, budget rules and how much to spend',
  primary='how much should an engagement ring cost', secondary=['average engagement ring cost', 'how much to spend on an engagement ring', 'engagement ring budget', 'engagement ring cost', 'how much to spend on an engagement ring calculator', '3 month salary rule engagement ring'],
  cluster='NEW:ENGAGEMENT_RING_COST_AND_BUDGET', intent='INFORMATIONAL', funnel='CONSIDERATION', hub='COM-ER; EDU-LG-05', spoke='Buying-decision spoke (dated averages + budget guidance)', parent='Buying decisions', related='BC-019; BC-037; BC-016',
  audience='Ring buyers setting a budget', need='What people actually spend (dated, sourced), how much to spend, and how lab-grown changes what the budget buys',
  seasonal='MEDIUM-HIGH', festival='Engagement season', hod='HIGH', commercial='HIGH',
  category='COM-ER', product='n/a', edu='EDU-LG-05; EDU-LG-02; EDU-LG-00; EDU-4C-07', target_id='EDU-LG-05', links=['BLOG-HUB', 'EDU-LG-00', 'EDU-LG-05', 'EDU-LG-02', 'COM-ER', 'EDU-4C-07'],
  cta='See how lab-grown changes value (EDU-LG-05); browse engagement rings by budget',
  paa='How much should a man spend on an engagement ring? [answer-first: no fixed rule + dated averages] | How much should I spend on an engagement ring if I make $100,000 a year? [H2 with an illustrative table; not personalised financial advice] | What is the 3 month rule for ring? [H3: origin of the salary rule and why it is outdated] | Is $5,000 / $10,000 a lot for an engagement ring? [table of what budgets buy, lab vs natural] | How big is a $5000 engagement ring? [link EDU-4C-07]',
  aeo='Answer-first "no fixed rule; US average ~$X (dated source)" + budget-by-income illustrative table + lab-grown vs natural budget table + FAQ. All figures dated and sourced; no personalised financial advice.',
  cann='USER DECISION (2026-09-29): one comprehensive Blog article owns the average-cost + budget intent (AIO text identical across these SERPs; PAA overlap). No second budget article. None of these keywords is in the Stage 15 map; EDU-RJG-04 ownership of CL-122 is UNCHANGED and, if built, it links here for budget rather than duplicating it. EDU-LG-05 keeps lab-grown price/value questions.',
  facts='Named, dated survey sources for averages; no HOD price claims', lowjust='',
  priority='P2_HIGH', why='Combined demand ~34,000/mo (6,600 + average 8,100 + how much to spend 4,400 + budget 12,100 + variants). Editorial SERP (Reddit, retailer guides, Vogue, Amex); budget PAA recurs on 7 SERPs.', promote='NO (user decision: Blog)', refresh='Annually when new survey data is published')

topic(id='BC-016', status='KEPT', merged='', date='2026-10-26', template='BLOG-INDUSTRY', ctype='SEASONAL',
  event='Engagement season starts (Thanksgiving)', event_date=EV['Thanksgiving'], publish_by='2026-10-30', lead='~4 weeks before Thanksgiving; peaks in November (1.88x).',
  title="When is engagement season? Why so many proposals happen between Thanksgiving and Valentine's Day",
  primary='when is engagement season', secondary=['engagement season', 'most popular day to get engaged', 'most popular month to get engaged', 'thanksgiving proposal ideas', 'thanksgiving proposal'],
  cluster='NEW:ENGAGEMENT_SEASON', intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-ER', spoke='Proposal series: seasonality & data', parent='Proposal & engagement', related='BC-014; BC-017; BC-019',
  audience='Couples expecting or planning a proposal', need='When engagement season is, the data behind it, and planning ahead', seasonal='HIGH', festival="Thanksgiving; Christmas; NYE; Valentine's", hod='HIGH', commercial='MEDIUM-HIGH',
  category='COM-ER', product='n/a', edu='EDU-LG-10', target_id='', links=['BLOG-HUB', 'COM-ER', 'EDU-LG-02', 'EDU-LG-05', 'EDU-LG-00', 'BC-001', 'BC-014'], cta='Plan ahead: engagement rings; bespoke timeline (BC-001)',
  paa='What month do most engagements happen? [answer-first: December (dated source)] | What is the luckiest day to get engaged? [FAQ; no astrology claims] | Is 7 months too early to propose? [not answered - relationship advice, out of scope]',
  aeo='Answer-first date range (late November to mid-February) + ranked list of top proposal days (dated The Knot data) + planning timeline.', cann='PASS: no Stage 15 owner.', facts='Cite The Knot survey with year',
  lowjust='170/mo (peak ~320). Kept: informational SERP (The Knot, Brides, jewellers), AIO confirms the season, highly qualified pre-Thanksgiving audience, and it anchors the proposal series.',
  priority='P1_TIME_CRITICAL', why='Must be live before Thanksgiving opens the season.', promote='NO', refresh='Yearly (update survey year)')

topic(id='BC-017', status='KEPT (absorbs BC-029; "christmas proposal" dropped)', merged='BC-029', date='2026-10-27', template='BLOG-GIFTS', ctype='FESTIVAL',
  event="Christmas, Christmas Eve and New Year's Eve proposals", event_date=EV['Christmas'] + ' / ' + EV["New Year's Eve"], publish_by='2026-11-09',
  lead='~8.5 weeks before Christmas; Christmas proposal searches Nov 2.9x, Dec 5.3x; NYE proposal Dec 6-7x.',
  title="Christmas and New Year's Eve proposal ideas: festive ways to propose (plus a ring-timing checklist)",
  primary='christmas proposal ideas', secondary=['christmas engagement', 'christmas eve proposal', 'how to propose on christmas', 'holiday proposal ideas', 'winter proposal ideas', 'new years eve proposal ideas', 'new years proposal', 'new years eve proposal'],
  cluster='NEW:PROPOSAL_HOLIDAY', intent='INFORMATIONAL', funnel='CONSIDERATION', hub='BC-014 proposal hub -> COM-ER', spoke='Seasonal proposal spoke: Christmas + NYE', parent='Proposal & engagement', related='BC-014; BC-016; BC-001',
  audience='People planning a holiday proposal', need='Festive proposal ideas and ring timing', seasonal='HIGH', festival="Christmas; Christmas Eve; New Year's Eve", hod='HIGH', commercial='HIGH',
  category='COM-ER', product='Engagement rings (verify live)', edu='EDU-RJG-02', target_id='EDU-RJG-02', links=['BLOG-HUB', 'COM-ER', 'EDU-RJG-02', 'BC-001', 'BC-014'] + GIFT_LINKS,
  cta='Order the ring in time (engagement rings / bespoke; typical bespoke 3-4 weeks)',
  paa='Do people get engaged at Christmas? [answer-first: Christmas Day and Eve are the top proposal days] | What are some creative ideas for a holiday proposal? [H2 lists: at-home, outdoor/public, NYE midnight] | Is 2026 a good year to get engaged? [not answered] | Do I put the ring on her finger when I propose? [FAQ, link BC-036]',
  aeo='Answer-first + idea lists mirroring the AIO (cozy at-home / scenic & public / NYE countdown) + ring-timing checklist.',
  cann='"christmas proposal" (590) REMOVED from secondaries: its SERP is the Hallmark / Prime Video movie. Winter and NYE merged here (NYE standalone was 90/mo). Generic ideas link to BC-014.',
  facts='Order-by dates for Dec 24/25/31 (uses the confirmed bespoke timeline)', lowjust='',
  priority='P1_TIME_CRITICAL', why='Christmas Day and Eve are the most popular proposal days. SERP MIXED informational (The Knot list, retailer idea lists).', promote='NO', refresh='Annually by October')

topic(id='BC-005', status='KEPT', merged='', date='2026-10-29', template='BLOG-CRAFT', ctype='EVERGREEN',
  event='Craft (evergreen)', event_date='n/a', publish_by='n/a (evergreen)', lead='Evergreen; flat demand. Scheduled after the Diwali/Surat industry note (BC-015) so the two craft/industry pieces link to each other.',
  title='How diamonds are cut and polished: the five steps inside a Surat cutting workshop',
  primary='how diamonds are cut', secondary=['diamond cutting process', 'diamond polishing'],
  cluster='NEW:DIAMOND_CUTTING_CRAFT', intent='INFORMATIONAL', funnel='AWARENESS', hub='BRAND-ABOUT / COM-BESPOKE', spoke='Craft spoke: stone cutting', parent='Craftsmanship (Surat)', related='BC-015; BC-001',
  audience='Buyers researching quality; curious readers', need='How rough becomes a polished diamond, and why cutting skill matters', seasonal='NONE', festival='none', hod='HIGH: Surat link', commercial='INDIRECT',
  category='COM-ER; COM-BESPOKE', product='n/a', edu='EDU-4C-06; EDU-NAT-00; EDU-SHP-00; EDU-GEN-01', target_id='EDU-4C-06', links=['BLOG-HUB', 'COM-BESPOKE', 'BRAND-ABOUT', 'EDU-4C-06', 'EDU-SHP-00', 'EDU-NAT-00', 'EDU-GEN-01'],
  cta='Learn cut grades (EDU-4C-06); see HOD craftsmanship (About)',
  paa='How does a jeweler cut a diamond? [numbered 5 steps: planning/scanning, cleaving/sawing, bruting, faceting, polishing] | How are diamonds cut if they are so hard? [one line + link EDU-GEN-01] | How were diamonds cut historically? [H3 short history] | What is the prettiest cut of a diamond? [link EDU-SHP-00]',
  aeo='Answer-first (lasers, diamond-tipped saws, polishing wheels) + 5-step process mirroring the AIO + first-hand workshop evidence.',
  cann='BOUNDARY: EDU-4C-06 owns cut GRADE; EDU-GEN-01 owns hardness ("can you cut diamonds"); EDU-NAT-00 S06 keeps its short mining/cutting summary. This post owns the first-hand cutting PROCESS.', facts='Whether HOD cuts/polishes in-house or via Surat partners; workshop photography', lowjust='',
  priority='P2_HIGH', why='1,900 + polishing 1,300. Informational/process SERP (Wikipedia, Reddit ELI5, Baunat, GIA, YouTube).', promote='NO (brand craft)', refresh='Keep as record')

topic(id='BC-019', status='KEPT', merged='', date='2026-10-30', template='BLOG-INDUSTRY', ctype='FESTIVAL',
  event='Black Friday / Cyber Monday', event_date=EV['Black Friday'] + ' / ' + EV['Cyber Monday'], publish_by='2026-11-06', lead='4 weeks before Black Friday; deal searches spike ~10x in November.',
  title='Is Black Friday a good time to buy an engagement ring? The best time of year to buy diamonds',
  primary='best time to buy an engagement ring', secondary=['best time to buy diamonds', 'best time of year to buy jewelry', 'is black friday a good time to buy an engagement ring'],
  cluster='NEW:BUYING_TIMING', intent='INFORMATIONAL', funnel='CONSIDERATION', hub='COM-ER; EDU-LG-10', spoke='Black Friday informational post (not a deals page)', parent='Buying decisions', related='BC-024; BC-016',
  audience='Ring buyers weighing sales against quality', need='Whether sales seasons are cheaper and how to check a discount is real', seasonal='HIGH', festival='Black Friday; Cyber Monday', hod='HIGH', commercial='HIGH',
  category='COM-ER', product='n/a', edu='EDU-LG-10; EDU-CERT-00; EDU-LG-05', target_id='EDU-LG-10', links=['BLOG-HUB', 'EDU-LG-00', 'EDU-LG-05', 'EDU-LG-10', 'EDU-CERT-00', 'COM-ER', 'BC-024'],
  cta='Compare with confidence (certification guide) -> engagement rings; any live HOD offer page',
  paa='What is the cheapest month to buy an engagement ring? [answer-first per AIO: Jan-early Mar, Aug-Sep] | Ideal timeline before proposing [H2 timeline] | Is Black Friday a good time? [H2: how to verify a discount] | Budget PAA [link BC-024]',
  aeo='Answer-first months + "times to avoid" + discount-verification checklist (certificate, 4Cs, price history).', cann='BOUNDARY: EDU-LG-10 owns how to choose; EDU-LG-05 owns price/value; BC-024 owns budget. "black friday * deals" not targeted (product SERPs).',
  facts='Whether HOD runs a Black Friday offer (never state discounts that do not exist)',
  lowjust='210/mo primary (Dec 1.7x). Kept: the only winnable Black Friday angle (all 14 measured deal SERPs are product-led), informational SERP (Reddit, jeweller guides), strong commercial assist, festival timing.',
  priority='P1_TIME_CRITICAL', why='Black Friday strategy post; must be indexed in early November.', promote='CANDIDATE (future EDU-RJG-04 timing section)', refresh='Annually by October')

topic(id='BC-021', status='KEPT', merged='', date='2026-11-02', template='BLOG-STYLE', ctype='EVERGREEN',
  event='Style (Dec gift peak)', event_date='n/a', publish_by='2026-11-20', lead='Evergreen; Dec 1.72x.',
  title='What is a tennis bracelet? Why it is called that, and how to wear one',
  primary='what is a tennis bracelet', secondary=['why is it called a tennis bracelet', 'chris evert tennis bracelet', 'how to wear a tennis bracelet', 'tennis bracelet stack', 'how to stack bracelets'],
  cluster='NEW:STYLE_TENNIS_BRACELET', intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-FJ-BRACELETS', spoke='Style spoke: bracelets', parent='Styling / jewellery types', related='BC-006; BC-025; BC-004',
  audience='Bracelet buyers and gift shoppers', need='Definition, the name story, and wearing tips', seasonal='MEDIUM', festival='Christmas (gift demand)', hod='HIGH: 6+ tennis bracelets', commercial='HIGH',
  category='COM-FJ-BRACELETS', product='Tennis bracelets (verify live)', edu='EDU-4C-00; EDU-MET-00', target_id='', links=['BLOG-HUB', 'COM-FJ-BRACELETS', 'COM-FJ', 'COM-PDP', 'EDU-4C-00'],
  cta='Shop tennis bracelets',
  paa='Why do they call it a tennis bracelet? [answer block: Chris Evert, 1978 US Open] | What is the difference between a regular bracelet and a tennis bracelet? [comparison table] | How much should you pay for a tennis bracelet? [short answer; link EDU-4C-00; no invented prices] | Does anyone wear tennis bracelets anymore? [FAQ, link BC-032]',
  aeo='Definition-first + name-history box + comparison table + styling list + FAQ.', cann='PASS: "tennis bracelet" (135,000) is a category head reserved for COM-FJ-BRACELETS.', facts='none', lowjust='',
  priority='P2_HIGH', why='3,600 + name 3,600 + Chris Evert 1,000. Informational retailer guides + Vogue.', promote='CANDIDATE (jewellery-types guide)', refresh='Yearly')

topic(id='BC-039', status='NEW (NEW-05, split from BC-011)', merged='', date='2026-11-03', template='BLOG-STYLE', ctype='EVERGREEN',
  event='Holiday gifting (Dec peak)', event_date=EV['Christmas'], publish_by='2026-11-30', lead='Evergreen; December peak 1.64x.',
  title='What finger does a promise ring go on? Placement, hand and meaning',
  primary='what finger does a promise ring go on', secondary=['what hand does a promise ring go on', 'promise ring finger', 'what finger to wear promise ring', 'is it bad luck to wear promise ring on ring finger', 'promise ring finger placement meaning'],
  cluster='NEW:RING_TRADITION_PROMISE_FINGER', intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-FJ', spoke='Ring traditions spoke', parent='Ring traditions', related='BC-011; BC-036; BC-038',
  audience='Promise ring givers and receivers', need='Which finger/hand, and what each placement signals', seasonal='MEDIUM', festival='Christmas', hod='MEDIUM-HIGH', commercial='MEDIUM',
  category='COM-FJ (Rings, conditional)', product='Diamond fashion rings (verify live)', edu='EDU-RJG-02', target_id='', links=['BLOG-HUB', 'COM-FJ', 'BC-011', 'BC-036', 'EDU-RJG-02'],
  cta='Shop fine-jewellery rings; read what a promise ring means (BC-011)',
  paa='What finger is a promise ring worn on? [answer-first: no official finger; common placements] | What hand does a promise ring go on? [H2] | What comes next after a promise ring? [FAQ, link BC-011] | When should a girl receive a promise ring? [link BC-011]',
  aeo='Answer-first + placement table (left ring finger, right ring finger, other fingers, on a chain) + FAQ.', cann='SPLIT from BC-011: separate SERP (<2 shared URLs). BC-011 owns meaning; BC-036 owns the wedding-ring finger; BC-038 owns general finger meanings.', facts='none', lowjust='',
  priority='P2_HIGH', why='12,100 + what hand 2,900 + promise ring finger 3,600. 5 dedicated retailer guides; AIO: no official finger + placements.', promote='CANDIDATE (Ring traditions hub)', refresh='Yearly')

topic(id='BC-022', status='KEPT (not upgraded to "ring stacking")', merged='', date='2026-11-05', template='BLOG-STYLE', ctype='EVERGREEN',
  event='Engagement season (Dec peak)', event_date=EV['Engagement season'], publish_by='2026-11-30', lead='Evergreen; stacking demand ~2x in Nov/Dec.',
  title='How to stack rings: engagement ring, wedding band and eternity band combinations',
  primary='how to stack rings', secondary=['wedding band stack', 'wedding ring stack', 'how to stack rings with engagement ring', 'wedding band stack ideas', 'how to stack wedding bands'],
  cluster='NEW:STYLE_RING_STACKING', intent='INFORMATIONAL', funnel='CONSIDERATION', hub='COM-WB', spoke='Style spoke: stacking design', parent='Styling', related='BC-007; BC-023; BC-036',
  audience='Engaged/married buyers adding bands', need='Which bands pair with which ring styles; balance and rules', seasonal='MEDIUM-HIGH', festival='Engagement season; Christmas', hod='HIGH', commercial='HIGH',
  category='COM-WB; COM-ER', product='Bridal sets; eternity and half-eternity bands (verify live)', edu='EDU-SHP-00; EDU-MET-00', target_id='', links=['BLOG-HUB', 'COM-WB', 'COM-ER', 'EDU-SHP-00', 'EDU-MET-00', 'COM-PDP', 'BC-007'],
  cta='Shop wedding bands and bridal sets',
  paa='What are the rules for stacking rings? [answer-first list] | How to build a good ring stack? [numbered steps: base ring, textures/widths, metals/stones, balance - mirrors AIO] | How to make stacked rings stay in place? [H3] | What is a wedding band stack? [answer block] | In what order do you stack your wedding rings? [one line + link BC-007]',
  aeo='Answer-first + build steps + pairing table (ring shape x band style) + FAQ.', cann='PASS: "ring stacking" (40,500) is TRANSACTIONAL (7 product pages, no AIO) and not targeted. EDU-MET-00 owns "do iridium bands stack". BC-007 owns wear ORDER.', facts='none', lowjust='',
  priority='P2_HIGH', why='590 primary + wedding band stack 9,900 + wedding ring stack 9,900 (MIXED; AIO "how to build a ring stack"). Guide-led primary SERP (Mejuri, Brilliant Earth, Lagos, GIA).', promote='NO', refresh='Yearly')

topic(id='BC-038', status='NEW (NEW-04; absorbs BC-027 meaning)', merged='BC-027', date='2026-11-06', template='BLOG-STYLE', ctype='EVERGREEN',
  event='Ring culture (evergreen)', event_date='n/a', publish_by='n/a (evergreen)', lead='Evergreen; flat demand.',
  title='Ring finger meaning: what a ring on each finger symbolises (thumb to pinky, left vs right)',
  primary='ring finger meaning', secondary=['what do rings on each finger mean', 'right ring finger meaning', 'what does a ring on the middle finger mean', 'what does a ring on the index finger mean', 'what does a ring on the pinky finger mean', 'left ring finger meaning', 'which finger ring means single', 'right hand ring'],
  cluster='NEW:RING_TRADITION_MEANINGS', intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-FJ', spoke='Ring traditions spoke', parent='Ring traditions', related='BC-036; BC-039; BC-011',
  audience='Ring wearers curious about symbolism; self-purchasers', need='What each finger and hand signals, including right-hand rings', seasonal='LOW', festival='none', hod='HIGH: fashion/statement rings, bands', commercial='MEDIUM-HIGH',
  category='COM-FJ (Rings, conditional); COM-WB', product='Statement and fashion rings (verify live)', edu='EDU-RJG-02', target_id='', links=['BLOG-HUB', 'COM-FJ', 'COM-WB', 'BC-036', 'BC-039', 'COM-PDP'],
  cta='Shop fine-jewellery rings',
  paa='What does a ring mean on each finger? [answer-first + per-finger H2s: thumb, index, middle, ring, pinky - mirrors AIO] | Which finger ring means single? [answer block with a cultural caveat] | What does a ring on the right hand mean? [H2: right-hand rings and self-purchase - absorbed from BC-027] | Which finger is forbidden to wear a ring? [FAQ, cultural context, no claims]',
  aeo='Answer-first + finger-by-finger table (left vs right) + right-hand ring section + cultural-caveat note.', cann='PASS: the two meaning SERPs share 3 top-10 URLs (one intent). BC-036 owns which finger the wedding ring goes on; BC-039 owns the promise-ring finger. "right hand ring" (product SERP) is a secondary only as a meaning section.', facts='none', lowjust='',
  priority='P2_HIGH', why='9,900 + right ring finger 2,400 + pinky 2,900 + middle 1,900 + index 880 + each-finger 1,600. Informational retailer guides; AIO structured per finger.', promote='CANDIDATE (Ring traditions hub)', refresh='Yearly')

topic(id='BC-023', status='KEPT', merged='', date='2026-11-09', template='BLOG-STYLE', ctype='EVERGREEN',
  event='Anniversary / push-present gifting (Dec peak)', event_date='n/a', publish_by='2026-11-30', lead='Evergreen; Dec 1.61x.',
  title='Eternity ring meaning: when to give one, which finger, and full vs half eternity',
  primary='eternity ring meaning', secondary=['what is an anniversary ring', 'half eternity band vs full eternity', 'half eternity ring meaning', 'eternity ring which finger', '7 stone eternity ring meaning'],
  cluster='NEW:STYLE_ETERNITY_MEANING', intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-WB', spoke='Ring traditions spoke', parent='Ring traditions', related='BC-018; BC-035; BC-022',
  audience='Spouses choosing a milestone ring', need='Symbolism, when it is given, full vs half, which finger', seasonal='MEDIUM', festival='Christmas; anniversaries', hod='HIGH', commercial='HIGH',
  category='COM-WB', product='Eternity and half-eternity bands (verify live)', edu='EDU-RJG-02', target_id='', links=['BLOG-HUB', 'COM-WB', 'COM-PDP', 'EDU-RJG-02', 'BC-018', 'BC-035'],
  cta='Shop eternity & anniversary bands',
  paa='When should a woman get an eternity ring? [answer block] | What are the rules for eternity rings? [H2 list] | Which finger is an eternity ring worn on? [short answer] | What are the four rings a woman should receive? [FAQ] | What ring do you get after 10 years of marriage? [link BC-035]',
  aeo='Definition-first + "when to give" list + full vs half comparison table + FAQ.', cann='PASS: "eternity ring" (12,100) is TRANSACTIONAL and reserved for COM-WB.', facts='Whether full eternity bands can be resized (HOD policy)', lowjust='',
  priority='P3_MEDIUM', why='590 + meaning variants. MIXED informational (Wikipedia, retailer explainers); AIO: meaning, when to give, full vs half.', promote='NO', refresh='Yearly')

topic(id='BC-025', status='UPGRADED (primary)', merged='', date='2026-11-10', template='BLOG-STYLE', ctype='EVERGREEN',
  event='Style (Dec gift peak)', event_date='n/a', publish_by='2026-11-30', lead='Evergreen; Dec 1.19x.',
  title='Different types of earrings: studs, huggies, hoops and drops (plus earring backs explained)',
  primary='different types of earrings', secondary=['what are huggie earrings', 'types of earring backs', 'different types of earrings studs', 'hoops vs huggies', 'types of earring backs for studs', 'types of earrings with names and pictures'],
  cluster='NEW:STYLE_EARRING_TYPES', intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-FJ-EARRINGS', spoke='Style spoke: earrings', parent='Styling / jewellery types', related='BC-021; BC-006; BC-004',
  audience='Earring buyers and gift shoppers', need='Earring types, names, backs, and which suits whom', seasonal='MEDIUM', festival='Christmas (gift demand)', hod='HIGH: studs, huggies, hoops, drops', commercial='HIGH',
  category='COM-FJ-EARRINGS', product='Solitaire studs; huggies; hoops; drops (verify live)', edu='EDU-4C-07; EDU-MET-00', target_id='', links=['BLOG-HUB', 'COM-FJ-EARRINGS', 'COM-PDP', 'EDU-MET-00', 'EDU-4C-07'],
  cta='Shop earrings by type',
  paa="What are the different types of earrings called? [answer-first list with pictures] | What's the difference between hoop and huggie earrings? [comparison table] | What are huggie earrings? [H2 definition] | What is the 2/3 earring rule? [FAQ one-liner] | Types of earring backs [H2 table: push, screw, lever, latch]",
  aeo='Answer-first named list + type-by-type sections with pictures + earring-back table + hoop vs huggie comparison.', cann='PASS: "huggie earrings" (22,200) and "diamond stud earrings" (49,500) are category heads. Carat-for-studs stays on EDU-4C-07.', facts='Which earring backs HOD uses', lowjust='',
  priority='P2_HIGH', why='Upgraded to the style-guide intent: 1,600 + earring backs 3,600 + huggies 1,300 + studs 1,600. "Different types" SERP = 8 retailer style guides; the huggies SERP leans product-led.', promote='CANDIDATE (jewellery-types guide)', refresh='Yearly')

topic(id='BC-031', status='KEPT', merged='', date='2026-12-01', template='BLOG-STYLE', ctype='SEASONAL',
  event='New-year trend searches (peak Jan-Feb)', event_date='2027-01 to 2027-02', publish_by='2026-12-15', lead='~6-10 weeks before the Jan-Feb peak ("engagement ring trends 2026" peaked Feb 2026 at 3.46x).',
  title='Engagement ring trends for 2027: toi et moi, east-west, bezel, three-stone and elongated shapes',
  primary='engagement ring trends', secondary=['engagement ring trends 2027', 'engagement ring trends 2026', 'popular engagement ring styles', 'most popular engagement ring styles', 'most popular engagement ring shape', 'engagement ring trends to avoid', 'three stone ring meaning'],
  cluster='NEW:TRENDS_ENGAGEMENT_RINGS', intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-ER', spoke='Trend spoke', parent='Trends', related='BC-032; BC-037',
  audience='Engagement-ring shoppers during proposal season', need='Which styles and shapes are trending', seasonal='HIGH', festival='Engagement season; New Year', hod='HIGH', commercial='HIGH',
  category='COM-ER; COM-ER-SIDESTONE', product='Toi et moi; east-west marquise; bezel solitaire; three-stone; hidden halo (verify live)', edu='EDU-SHP-00; EDU-RJG-01', target_id='EDU-SHP-00',
  links=['BLOG-HUB', 'COM-ER', 'COM-ER-SIDESTONE', 'EDU-SHP-00', 'EDU-RJG-01', 'COM-PDP'], cta='Shop engagement rings by style',
  paa='What are the trendy engagement ring styles for 2027? [answer-first list] | What is the Gen Z engagement ring trend? [H3] | What engagement rings are out of style? [H2 "trends to avoid"] | What is the newest trend in engagement rings? [short answer] | What does a three-stone ring mean? [H3 - absorbed from removed BC-026]',
  aeo='Answer-first trend list + one section per style with a picture + "trends to avoid" + links to EDU-SHP-00 for shape choice.',
  cann='BOUNDARY: EDU-SHP-00 owns shape choice; EDU-RJG-01 owns setting types; "engagement ring styles" (18,100) is routed to Education (not targeted). Style heads (toi et moi, bezel, east-west, three stone engagement ring) are reserved for conditional COM-ER style subcategories.', facts='none', lowjust='',
  priority='P1_TIME_CRITICAL', why='Must be indexed before the January-February peak. MIXED editorial SERP (Vogue, Elle, Brilliant Earth, VRAI, Jared).', promote='NO', refresh='Annually in December (same URL)')

topic(id='BC-032', status='KEPT', merged='', date='2026-12-03', template='BLOG-STYLE', ctype='SEASONAL',
  event='New-year trend searches (peak Jan)', event_date='2027-01', publish_by='2026-12-15', lead='~5-8 weeks before the January peak.',
  title='Fine jewelry trends for 2027: diamond earrings, bracelets and necklaces to watch',
  primary='jewelry trends', secondary=['jewelry trends 2027', 'jewelry trends 2026', 'bracelet trends', 'earring trends', 'necklace trends', 'women jewelry trends', 'jewelry trends for 2027'],
  cluster='NEW:TRENDS_FINE_JEWELRY', intent='INFORMATIONAL', funnel='AWARENESS', hub='COM-FJ', spoke='Trend spoke', parent='Trends', related='BC-031; BC-006; BC-021',
  audience='Fine-jewellery shoppers', need='What is trending for the coming year', seasonal='HIGH', festival='New Year', hod='HIGH', commercial='HIGH',
  category='COM-FJ; COM-FJ-EARRINGS; COM-FJ-BRACELETS; COM-FJ-NECKLACES', product='Tennis bracelets; triple-row hoops; heart and solitaire pendants (verify live)', edu='EDU-MET-00', target_id='',
  links=['BLOG-HUB', 'COM-FJ', 'COM-FJ-EARRINGS', 'COM-FJ-BRACELETS', 'COM-FJ-NECKLACES', 'EDU-MET-00'], cta='Shop fine jewellery',
  paa='What is the most trending jewelry right now? [answer-first] | What are the new trends in jewelry? [H2 per trend] | What jewelry is selling the most right now? [short answer, no invented sales data] | What are the hottest jewelry trends according to Vogue? [cite, do not copy]',
  aeo='Answer-first summary + one H2 per trend + "how to wear it" line per trend.', cann='PASS: no Stage 15 owner; distinct from BC-031 (engagement rings only).', facts='none', lowjust='',
  priority='P2_HIGH', why='2,900 + 2026/2027 variants. Informational editorial SERP (WhoWhatWear, Elle, Vogue, Brilliant Earth, National Jeweler).', promote='NO', refresh='Annually in December (same URL)')

topic(id='BC-034', status='UPGRADED (primary)', merged='', date='2026-12-08', template='BLOG-GIFTS', ctype='FESTIVAL',
  event="Valentine's Day 2027 proposals", event_date=EV["Valentine's Day"], publish_by='2026-12-31',
  lead="~9.5 weeks before Valentine's Day and ~4 weeks before the January surge ('valentines day proposal': Dec 210 -> Jan 2,900 -> Feb 4,400).",
  title="Valentine's Day proposal ideas: romantic ways to propose on February 14",
  primary='valentines day proposal', secondary=['valentines day proposal ideas', "valentine's day proposal ideas"],
  cluster='NEW:PROPOSAL_VALENTINES', intent='INFORMATIONAL', funnel='CONSIDERATION', hub='BC-014 proposal hub -> COM-ER', spoke="Seasonal proposal spoke: Valentine's", parent='Proposal & engagement', related='BC-014; BC-017',
  audience="People planning a Valentine's proposal", need="Valentine's proposal ideas and ring timing", seasonal='HIGH', festival="Valentine's Day", hod='HIGH', commercial='HIGH',
  category='COM-ER', product='Engagement rings (verify live)', edu='EDU-RJG-02', target_id='EDU-RJG-02', links=['BLOG-HUB', 'COM-ER', 'EDU-RJG-02', 'BC-014', 'BC-001'] + GIFT_LINKS,
  cta='Engagement rings / bespoke (typical 3-4 weeks; order by mid-January)',
  paa="Is it a good idea to propose on Valentine's Day? [answer-first: pros/cons] | What are 10 romantic proposal ideas? [H2 list: classic, unique, at-home] | Do and don'ts of proposing? [link BC-014] | What to do immediately after proposing? [FAQ]",
  aeo='Answer-first + idea lists (classic / unique / at-home) + planning tips + ring-timing box.', cann="Separate from BC-017 by date. Valentine's JEWELLERY gift intent (removed BC-033) is product-led and routed to a commercial collection.", facts='Order-by date for Feb 14 (confirmed bespoke timeline)', lowjust='',
  priority='P1_TIME_CRITICAL', why="Upgraded to 720 (+ ideas 390). Informational (The Knot, Vogue lists); AIO: romantic, unique, planning tips. The only Valentine's post in the window, published early for the January rise.", promote='NO', refresh='Annually by mid-December')

# ============================ REMOVED / MERGED (not scheduled) ============================
REMOVED = [
 ('BC-002', 'MERGED', 'BC-015', 'lab grown diamond market (70)', 'Too thin alone; market section folded into the BC-015 industry note.'),
 ('BC-010', 'MERGED', 'BC-001', 'how is jewelry made (210)', 'Incoherent SERP; making stages folded into the bespoke timeline post.'),
 ('BC-012', 'REMOVED', 'BC-004 (section); commercial gifts collection recommended', 'jewelry gifts for mom (1,000)', 'SERP: 7/10 product/category pages, no AIO.'),
 ('BC-013', 'REMOVED', 'BC-004 (luxury section)', 'luxury christmas gifts for her (260)', 'SERP: luxury fashion/beauty brands; HOD cannot satisfy.'),
 ('BC-020', 'REMOVED', 'BC-004 (Hanukkah section)', 'hanukkah jewelry (140)', 'SERP: Judaica/novelty marketplace; intent mismatch.'),
 ('BC-026', 'REMOVED', 'BC-031 (three-stone section); backlog', 'three stone ring meaning (110)', 'Weak demand.'),
 ('BC-027', 'REMOVED', 'BC-038 (right-hand meaning section)', 'right hand ring (2,900)', 'SERP: TRANSACTIONAL (4 product pages).'),
 ('BC-028', 'REMOVED', 'BC-004 (ready-to-ship section)', 'last minute christmas gifts for her (210)', 'SERP: generic non-jewellery listicles; no AIO.'),
 ('BC-029', 'MERGED', 'BC-017', 'new years eve proposal ideas (90)', 'Too thin alone.'),
 ('BC-030', 'REMOVED', 'none', 'new years eve jewelry (480)', 'SERP: product-leaning (Kay, Jared categories).'),
 ('BC-033', 'REMOVED', "Commercial Valentine's collection recommended", 'valentines day jewelry (2,900)', 'SERP: 10/10 product/category pages, no AIO.'),
]

# ============================ BUILD ============================
def fmt(k):
    v = vol(k); return f"{k} ({v if v is not None else 'n/a'}; {src(k)})"

assert len({t['date'] for t in T}) == len(T), 'duplicate dates'
T.sort(key=lambda t: t['date'])
cal = []
for t in T:
    d = dt.date.fromisoformat(t['date']); pk = t['primary']; s = SERP.get(pk, {})
    secv = [vol(k) or 0 for k in t['secondary']]
    cal.append({
      'blog_id': t['id'], 'revision_status': t['status'], 'merged_from': t['merged'],
      'planned_publish_date': t['date'], 'week': week_of(d), 'month': d.strftime('%B %Y'), 'event_or_season': t['event'],
      'content_type': t['ctype'], 'blog_category': t['template'], 'blog_title_working': t['title'],
      'primary_keyword': pk, 'primary_search_volume': vol(pk) if vol(pk) is not None else 'n/a', 'seasonal_peak': peak(pk), 'keyword_difficulty': kd(pk),
      'secondary_keywords': '; '.join(fmt(k) for k in t['secondary']), 'secondary_search_volume': sum(secv),
      'combined_keyword_volume': (vol(pk) or 0) + sum(secv),
      'keyword_source': ' + '.join(sorted({('EXISTING_DATA' if src(k) == 'EXISTING_DATA' else 'NEW_RESEARCH') for k in [pk] + t['secondary']})),
      'keyword_source_detail': '; '.join(f"{k}={src(k)}" for k in [pk] + t['secondary']),
      'cluster_id': t['cluster'], 'search_intent': t['intent'],
      'serp_intent': s.get('serp_intent_verified', 'NOT_SERP_CHECKED'), 'serp_page_types': s.get('top10_page_types', ''), 'serp_top5_domains': s.get('top5_domains', ''),
      'ai_overview': ('PRESENT' if s.get('ai_overview') == 'True' else 'ABSENT') if s else 'NOT_CHECKED', 'aio_structure': s.get('aio_section_headings', ''),
      'paa_present': ('YES' if s.get('paa_present') == 'True' else 'NO') if s else 'NOT_CHECKED', 'paa_questions': t['paa'], 'aeo_answer_format': t['aeo'],
      'related_searches': s.get('related_searches', ''),
      'funnel_stage': t['funnel'], 'hub': t['hub'], 'spoke': t['spoke'], 'parent_topic': t['parent'], 'related_articles': t['related'],
      'target_audience': t['audience'], 'searcher_need': t['need'], 'seasonal_relevance': t['seasonal'], 'festival_relevance': t['festival'],
      'event_date': t['event_date'], 'publish_by_date': t['publish_by'], 'seo_lead_time': t['lead'],
      'HOD_relevance': t['hod'], 'commercial_relevance': t['commercial'], 'target_category': t['category'], 'target_product': t['product'],
      'related_education_page': t['edu'], 'related_target_page_id': t['target_id'], 'internal_link_targets': '; '.join(t['links']),
      'CTA_direction': t['cta'], 'cannibalization_check': t['cann'], 'business_facts_required': t['facts'],
      'low_volume_justification': t['lowjust'], 'content_status': 'PLANNED_NOT_BRIEFED', 'priority': t['priority'], 'priority_reason': t['why'],
      'promote_to_education_flag': t['promote'], 'refresh_cycle': t['refresh']})

taken = {dt.date.fromisoformat(t['date']) for t in T}
REASON = {'W07': 'Capacity after the evergreen launch batch; no further topic passed the SERP/intent bar.',
          'W08': 'No qualifying new topic. Suggested use: drafting BC-004 sections (Hanukkah Dec 4, ready-to-ship).',
          'W09': 'Thanksgiving / Black Friday week. All Black Friday deal SERPs are product-led; no qualifying Blog topic.',
          'W10': 'Cyber Monday week; only the two January-peak trend posts qualify.',
          'W11': 'Too late for new Christmas content. Use for the BC-004 December refresh (shipping cut-offs, ready-to-ship).',
          'W12': "No qualifying topic (Valentine's jewellery SERP is product-led; routed to commercial).",
          'W13': 'Christmas week; no qualifying topic.', 'W14': 'Year-end; no qualifying topic.'}
cols = list(cal[0].keys())
rows = cal + [{**{c: '' for c in cols}, 'blog_id': f'SLOT-{s:%m%d}', 'planned_publish_date': s.isoformat(), 'week': week_of(s), 'month': s.strftime('%B %Y'),
               'content_status': 'UNUSED_SLOT', 'priority': 'n/a', 'priority_reason': REASON.get(week_of(s)[:3], 'No qualifying topic; weak topics were not invented.')}
              for s in ALL_SLOTS if s not in taken]
rows.sort(key=lambda r: r['planned_publish_date'])
with open(os.path.join(OUT, 'blog_content_calendar.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

with open(os.path.join(OUT, 'blog_calendar_revision_log.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['blog_id', 'revision_action', 'destination_or_revised_primary', 'original_primary', 'reason'])
    for t in T: w.writerow([t['id'], t['status'], f"{t['primary']} ({vol(t['primary'])})", '', t['why']])
    for r in REMOVED: w.writerow(list(r))

json.dump({'scheduled': len(cal), 'unused_slots': len(rows) - len(cal), 'total_slots': len(ALL_SLOTS),
           'by_type': {k: sum(1 for c in cal if c['content_type'] == k) for k in ('EVERGREEN', 'SEASONAL', 'FESTIVAL')},
           'by_priority': {k: sum(1 for c in cal if c['priority'] == k) for k in ('P1_TIME_CRITICAL', 'P2_HIGH', 'P3_MEDIUM', 'P4_LOW')},
           'by_category': {k: sum(1 for c in cal if c['blog_category'] == k) for k in TEMPLATE_REQUIRED},
           'by_week': {wk: sum(1 for c in cal if c['week'] == wk) for wk in sorted({week_of(s) for s in ALL_SLOTS})},
           'primary_demand_total': sum(v for v in (vol(t['primary']) for t in T) if v),
           'combined_demand_total': sum(c['combined_keyword_volume'] for c in cal)},
          open(os.path.join(OUT, 'scripts', 'build_stats.json'), 'w'), indent=1)
print('scheduled', len(cal), 'unused', len(rows) - len(cal))
