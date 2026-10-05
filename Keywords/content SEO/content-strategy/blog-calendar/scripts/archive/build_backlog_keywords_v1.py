"""Blog Content Calendar Stage - backlog + keyword research outputs.
Run after build_blog_calendar.py. Local files only; no API call.
"""
import csv, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'content-strategy', 'blog-calendar')
P = lambda *a: os.path.join(ROOT, *a)

S15 = {r['normalized_keyword']: r for r in csv.DictReader(open(P('architecture/15_keyword_url_map.csv')))}
NEW = list(csv.DictReader(open(P('content-strategy/blog-calendar/working/call1_processed.csv'))))
CAL = [r for r in csv.DictReader(open(os.path.join(OUT, 'blog_content_calendar.csv'))) if r['content_status'] != 'UNUSED_SLOT']

use = {}
for r in CAL:
    use[r['primary_keyword']] = ('PRIMARY', r['blog_id'], r)
    for k in re.findall(r'(?:^|; )([^;()]+?) \([^)]*\)', r['secondary_keywords']):
        use.setdefault(k.strip(), ('SECONDARY', r['blog_id'], r))

# ------------------------------------------------ disposition rules for keywords NOT used by a scheduled blog
RULES = [  # (regex, code, reason, owner/target)
 (r'^(black friday|cyber monday|small business saturday)', 'COMMERCIAL_PROMO_NOT_BLOG',
  'Deal/sale query. All measured Black Friday/Cyber Monday terms with SERP data have product-led SERP features (Black Friday ~9-11x in Nov; Cyber Monday 5-8x in early Dec); a blog cannot credibly rank for "deals". Belongs to a seasonal offer page, if HOD runs a promotion.', 'Seasonal offer landing page (business decision; Stage 12 curated collection, INDEXABLE_CONDITIONAL)'),
 (r'halloween|spooky|october birthstone|christmas earrings|christmas necklace|jewelry advent calendar|galentine|^christmas jewelry$',
  'NOT_HOD_FIT', 'Costume, novelty or gemstone-birthstone intent. HOD sells fine diamond jewellery; gemstone categories are NOT_PROPOSED (Stage 12 D-16).', 'none'),
 (r'sweetest day', 'LEAD_TIME_INSUFFICIENT_2026', 'Sweetest Day is Oct 17, 2026; under 3 weeks of lead time from the calendar start. Product-led SERP.', 'none; plan for 2027 (publish by early Sep 2027)'),
 (r'fall jewelry|autumn jewelry', 'WEAK_FIT_OR_TIMING', 'Product-led SERP; fall trend demand peaks in September (already passed) and is small.', 'none'),
 (r'thanksgiving gifts|friendsgiving|thanksgiving jewelry', 'NOT_HOD_FIT', 'Hostess/novelty gift intent, not fine jewellery. Thanksgiving is handled as the start of engagement season (BC-016).', 'none'),
 (r'diwali|dhanteras', 'FUTURE_BUSINESS_DECISION', 'Generic Diwali gift intent (product SERPs). HOD\'s Surat/Diwali angle is covered by BC-015. A Diwali jewellery gift guide depends on a business decision to target the Indian-American gifting audience.', 'none'),
 (r'engagement ring budget|how much to spend on an engagement ring|how much should an engagement ring cost', 'EDUCATION_OWNER_DEFERRED',
  'Budget ADVICE is an Education buying-guide intent (Stage 13 section 3). Owner topic EDU-RJG-04 is DEFERRED (Stage 14). High demand, so it needs an Education decision. BC-024 covers only the dated statistic.', 'EDU-RJG-04 (DEFERRED)'),
 (r'how to choose an engagement ring|how to pick an engagement ring|how to buy an engagement ring|engagement ring buying guide|what to know before buying an engagement ring|should i propose with a lab grown diamond',
  'EXISTING_PAGE_OWNER', 'Engagement-ring buying guide intent. The existing article /blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online (EXIST-BLOG-ER-ONLINE, Stage 13 DEFER) and EDU-LG-10 already cover this; EDU-RJG-04 is the deferred Education owner. Update the existing article instead of creating a new one.', 'EXIST-BLOG-ER-ONLINE / EDU-LG-10 / EDU-RJG-04 (DEFERRED)'),
 (r'engagement ring insurance|insure an engagement ring', 'EDUCATION_GAP', 'Evergreen practical-ownership question (Education test, Stage 13 section 4). No Stage 14/15 owner exists.', 'Proposed Education candidate under Ring & Jewellery Guides (not created)'),
 (r'how to clean engagement ring|engagement ring care', 'EXISTING_PAGE_OWNER', 'Care and cleaning belong to Education (Stage 13 framework).', 'EDU-RJG-03 (CONDITIONAL)'),
 (r'necklace length|bracelet size|measure bracelet size', 'EDUCATION_GAP', 'Practical sizing tool/guide (Stage 13 framework: sizing belongs to Education). Dec peak (~1.6-1.9x): high gift-season value, but no Stage 14/15 owner.', 'Proposed Education candidate under Ring & Jewellery Guides (not created)'),
 (r'stud size|stud earring size|what size diamond studs|choose diamond stud earrings', 'EXISTING_PAGE_OWNER', 'Carat-for-earrings questions are owned by EDU-4C-07 (Stage 15: "is 1/2 carat diamond good for earrings"). Stud shopping belongs to COM-FJ-EARRINGS.', 'EDU-4C-07; COM-FJ-EARRINGS'),
 (r'ring size secretly|ring size without asking|surprise proposal engagement ring size', 'EXISTING_PAGE_OWNER', 'Ring sizing is owned by EDU-RJG-02. Recommend adding a "finding her size secretly" section there (Stage 19 update candidate); proposal posts link to it.', 'EDU-RJG-02'),
 (r'getting cheaper|lab grown diamond price trend|lab grown diamond prices', 'EXISTING_PAGE_OWNER', 'Same intent as Stage 15 "will lab-grown diamonds get cheaper" (EDU-LG-05). BC-002 links there and does not target it.', 'EDU-LG-05'),
 (r'hip hop|iced out|cuban link|mens diamond jewelry', 'BUSINESS_DEPENDENCY', '/hiphop is a "Coming Soon" placeholder (Stage 1). A launch post needs a live collection. Shopping heads belong to the collection page.', 'Hip Hop collection (placeholder)'),
 (r'^t bar|t bar necklace', 'BUSINESS_DEPENDENCY', 'T-bar is a live merchandising collection, but its category form is undecided (Stage 12). A collection story (BLOG-LAUNCH) waits for that decision; "t bar necklace" is a shopping head.', 'COM-CURATED-TBAR (undecided)'),
 (r'redesign|heirloom|reset diamond|turn old ring', 'BUSINESS_DEPENDENCY', 'Remodel/redesign service is not confirmed (Stage 15 REVIEW row "can you turn diamond earring into ring"). Good future Craft post if HOD offers it.', 'COM-BESPOKE (if the service exists)'),
 (r'lariat', 'BACKLOG_LOW_PRIORITY', 'Only one lariat product; "what is a lariat necklace" is 390/month. Not worth a slot this quarter; mention in BC-006.', 'COM-FJ-NECKLACES'),
 (r'wedding band trends|wedding ring trends', 'FUTURE_WINDOW', 'Peaks in August (wedding season), not in Q4. Publish in spring 2027.', 'none'),
 (r'shopping together|shop for engagement rings together|ask her father', 'BACKLOG_LOW_PRIORITY', 'Low demand (0-210) and weak product link.', 'none'),
 (r'^gifts for (wife|girlfriend)$|^christmas gifts for her$|^christmas gift ideas for her$|holiday gift guide for her|gifts for her under 500|jewelry gifts under 1000|meaningful jewelry gifts|sentimental jewelry gifts|diamond gift ideas|how to buy jewelry for a woman|what jewelry to get my wife|how to choose jewelry for a gift|how to buy earrings for someone|secret santa|8 nights of hanukkah|hanukkah gifts$',
  'CONTEXT_ONLY', 'Broad non-jewellery gift head or very low/no demand. Covered inside the gift series as context; not a target for a jewellery blog.', 'BC-004 series (context)'),
 (r'.*', 'RESERVED_COMMERCIAL_PAGE', 'Shopping/product head (product-led SERP). Stage 13 section 3: the Blog never targets category or product queries; a blog post links to the category instead.', None),
]
# no-data keywords that still carry a substantive routing decision keep their rule-based disposition
RULES_NODATA_KEEP = r'getting cheaper|lab grown diamond prices|redesign|reset diamond|turn old ring|should i propose with a lab grown diamond|ring size secretly|surprise proposal|insure an engagement ring|hip hop|what is a t bar|half eternity'
COMMERCIAL_OWNER = [
 (r'tennis bracelet', 'COM-FJ-BRACELETS (tennis subcategory conditional)'),
 (r'stud|huggie|hoop|earring', 'COM-FJ-EARRINGS'),
 (r'necklace|pendant|solitaire necklace', 'COM-FJ-NECKLACES'),
 (r'eternity|anniversary band|anniversary ring|wedding|bridal', 'COM-WB'),
 (r'custom|bespoke|design your own|handmade', 'COM-BESPOKE'),
 (r'engagement ring|toi et moi|east west|bezel|three stone|two stone|hidden halo|elongated|promise ring|proposal ring', 'COM-ER (style subcategories conditional)'),
 (r'lab grown diamonds india', 'COM-LG-HUB (conditional)'),
 (r'.*', 'COM-FJ'),
]
EVENT = {'HALLOWEEN_FALL': ('Halloween / fall / Sweetest Day', '2026-10-31 / 2026-10-17'), 'DIWALI_SURAT': ('Diwali / craft', '2026-11-08'),
         'THANKSGIVING': ('Thanksgiving', '2026-11-26'), 'BLACK_FRIDAY_CYBER': ('Black Friday / Cyber Monday', '2026-11-27 / 2026-11-30'),
         'CHRISTMAS_HOLIDAY_GIFTS': ('Christmas / holiday gifting', '2026-12-25'), 'HANUKKAH': ('Hanukkah', '2026-12-04'),
         'PROPOSAL_ENGAGEMENT_SEASON': ('Engagement season', '2026-11-26 to 2027-02-14'), 'TRENDS': ('New-year trends', '2027-01'),
         'STYLE_EVERGREEN': ('Evergreen style', 'n/a'), 'OCCASIONS_EVERGREEN_AND_VDAY': ("Occasions / Valentine's", "2027-02-14 (Valentine's) / n/a"),
         'CUSTOM_BESPOKE': ('Bespoke (evergreen)', 'n/a')}

def fnum(x):
    try: return float(x)
    except (TypeError, ValueError): return None

def assessed_intent(r):
    if r['search_volume'] == 'NOT_IN_DATAFORSEO_DB': return 'UNMEASURED'
    prod, aio, forum = r['serp_product_led'] == 'True', r['serp_has_ai_overview'] == 'True', r['serp_has_forums'] == 'True'
    dfs = r['dfs_main_intent']
    if prod and not aio and not forum: return 'TRANSACTIONAL' if dfs == 'transactional' else 'COMMERCIAL'
    if prod and (aio or forum): return 'MIXED'
    if dfs in ('transactional', 'commercial') and not (aio or forum): return 'COMMERCIAL'
    return 'INFORMATIONAL'

rows = []
for r in NEW:
    k = r['keyword']
    idx = [fnum(r.get(c)) for c in ('oct_index', 'nov_index', 'dec_index', 'feb_index')]
    mx = max([i for i in idx if i is not None], default=None)
    season = 'NO_DATA' if mx is None else ('SEASONAL (peak ' + r['peak_month_last12'] + ')' if mx >= 2.0 else 'EVERGREEN')
    ev, evd = EVENT[r['candidate_group']]
    if k in use:
        role, bid, c = use[k]
        disp, reason, owner = role, f'Used by {bid} ({c["blog_category"]}).', c['target_category']
        pub, lead, hod, com = c['planned_publish_date'], c['seo_lead_time'], c['HOD_relevance'], c['commercial_relevance']
    elif r['search_volume'] == 'NOT_IN_DATAFORSEO_DB' and not re.search(RULES_NODATA_KEEP, k):
        disp, reason, owner = 'NO_DATA', 'Not in the DataForSEO database (not returned, not charged). No demand evidence, so not targeted.', 'none'
        bid, pub, lead, hod, com = '', '', '', 'n/a', 'n/a'
    elif k in ('diamond jewelry trends', 'thanksgiving engagement'):
        disp, reason, owner = 'MERGED_LOW_DEMAND', 'Demand of 10/month; covered as context in ' + ('BC-032' if 'trends' in k else 'BC-016') + '.', 'BC-032' if 'trends' in k else 'BC-016'
        bid, pub, lead, hod, com = '', '', '', 'MEDIUM', 'INDIRECT'
    else:
        for rx, code, why, own in RULES:
            if re.search(rx, k):
                disp, reason, owner = code, why, own
                if own is None:
                    owner = next(o for rx2, o in COMMERCIAL_OWNER if re.search(rx2, k))
                break
        bid, pub, lead = '', '', ''
        hod = {'NOT_HOD_FIT': 'LOW', 'COMMERCIAL_PROMO_NOT_BLOG': 'HIGH (commercial, not blog)'}.get(disp, 'MEDIUM-HIGH')
        com = 'HIGH (commercial page)' if disp in ('RESERVED_COMMERCIAL_PAGE', 'COMMERCIAL_PROMO_NOT_BLOG') else ('NO_DIRECT_COMMERCIAL_CONNECTION' if disp == 'NOT_HOD_FIT' else 'INDIRECT')
    rows.append({
        'data_source': 'NEW_RESEARCH', 'keyword': k, 'candidate_group': r['candidate_group'],
        'search_volume': r['search_volume'], 'avg_monthly_last12': r.get('avg_last12', ''),
        'oct_2025': r.get('oct_2025', ''), 'nov_2025': r.get('nov_2025', ''), 'dec_2025': r.get('dec_2025', ''), 'jan_2026': r.get('jan_2026', ''), 'feb_2026': r.get('feb_2026', ''),
        'oct_index': r.get('oct_index', ''), 'nov_index': r.get('nov_index', ''), 'dec_index': r.get('dec_index', ''), 'feb_index': r.get('feb_index', ''),
        'peak_month_last12': r.get('peak_month_last12', ''), 'keyword_difficulty': r.get('keyword_difficulty', ''), 'cpc': r.get('cpc', ''),
        'paid_competition': r.get('paid_competition', ''), 'dfs_main_intent': r.get('dfs_main_intent', ''), 'assessed_search_intent': assessed_intent(r),
        'serp_item_types': r.get('serp_item_types', ''), 'season_or_event': ev, 'event_date': evd, 'evergreen_or_seasonal': season,
        'recommended_publish_date': pub, 'seo_lead_time': lead, 'HOD_relevance': hod, 'commercial_relevance': com,
        'target_page_or_category': owner, 'disposition': disp, 'used_in_blog_id': bid, 'disposition_reason': reason,
        'source_endpoint': r['source_endpoint'], 'stage15_status': 'NOT_IN_STAGE15 (new keyword)'})

# EXISTING_DATA keywords used by the calendar
for k, (role, bid, c) in sorted(use.items()):
    if k in S15 and not any(x['keyword'] == k for x in rows):
        s = S15[k]
        rows.append({'data_source': 'EXISTING_DATA', 'keyword': k, 'candidate_group': 'STAGE7_MASTER',
                     'search_volume': s['search_volume'], 'keyword_difficulty': s['keyword_difficulty'], 'cpc': s['cpc'], 'paid_competition': s['competition'],
                     'dfs_main_intent': s['keyword_intent'], 'assessed_search_intent': s['serp_intent'] or 'not SERP-validated',
                     'season_or_event': c['event_or_season'], 'event_date': c['event_date'], 'evergreen_or_seasonal': 'EVERGREEN (Stage 4/6 monthly data flat)',
                     'recommended_publish_date': c['planned_publish_date'], 'seo_lead_time': c['seo_lead_time'], 'HOD_relevance': c['HOD_relevance'], 'commercial_relevance': c['commercial_relevance'],
                     'target_page_or_category': c['target_category'], 'disposition': role, 'used_in_blog_id': bid,
                     'disposition_reason': f"Stage 15 {s['mapping_disposition']} / {s['cluster_id']}: {s['reason'][:160]}",
                     'source_endpoint': 'Stage 7 master (Stage 4/6 DataForSEO Labs, 2026-09-17)', 'stage15_status': s['mapping_disposition']})

# EXISTING_DATA keywords considered and routed to backlog (no Stage 15 change)
for k, reason in [('can you return an engagement ring', 'EDU-RJG-04 DEFERRED (CL-122).'), ('do men get engagement rings too', 'EDU-RJG-04 DEFERRED (CL-122).'),
                  ('do engagement rings have to be diamond', 'EDU-RJG-04 DEFERRED (CL-122).'), ('do you wear engagement ring everyday', 'EDU-RJG-03 CONDITIONAL (CL-115).'),
                  ('lab diamond studs', 'Commercial studs subcategory CONDITIONAL (CL-125).'), ('will lab-grown diamonds get cheaper', 'Owned by EDU-LG-05.'),
                  ('mixed metal rings', 'Commercial DEFERRED (CL-123).'), ('conflict free diamonds', 'EDU-NAT-02 CONDITIONAL (CL-073); Dec spike 4.5x noted.')]:
    s = S15[k]
    rows.append({'data_source': 'EXISTING_DATA', 'keyword': k, 'candidate_group': 'STAGE7_MASTER', 'search_volume': s['search_volume'],
                 'keyword_difficulty': s['keyword_difficulty'], 'dfs_main_intent': s['keyword_intent'], 'assessed_search_intent': s['serp_intent'] or 'not SERP-validated',
                 'target_page_or_category': s['target_id'] or s['stage14_topic_id'] or 'none', 'disposition': 'EXISTING_PAGE_OWNER' if s['target_id'] else 'BACKLOG_EXISTING_OWNER_HELD',
                 'disposition_reason': reason, 'source_endpoint': 'Stage 7 master (2026-09-17)', 'stage15_status': s['mapping_disposition']})

cols = list(rows[0].keys())
with open(os.path.join(OUT, 'blog_keyword_research.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows: w.writerow({c: r.get(c, '') for c in cols})

# ------------------------------------------------ topic backlog (hand-authored)
B = [
 # topic, keyword, reason, owner, future, window, code
 ('Black Friday / Cyber Monday jewellery deals', 'black friday jewelry deals (2,900); black friday jewelry sale (1,900); black friday ring deals (1,000); black friday engagement rings (880); cyber monday jewelry deals (590)',
  'Deal intent with product-led SERPs (all 14 measured deal terms with SERP data). A blog cannot credibly compete, and HOD has no confirmed promotion. BC-019 covers the winnable informational question.',
  'None today. Would be a seasonal offer landing page (Stage 12 curated collection, INDEXABLE_CONDITIONAL).', 'If HOD runs a Black Friday offer: build an offer page ~Nov 1 that reuses one URL each year; the blog links to it.', 'Nov 1-Dec 1', 'COMMERCIAL_PROMO_NOT_BLOG'),
 ('Engagement ring budget: how much to spend', 'engagement ring budget (12,100); how much should an engagement ring cost (6,600); how much to spend on an engagement ring (4,400)',
  'Evergreen buying-advice intent: Education by the Stage 13 tests. Owner EDU-RJG-04 is DEFERRED.', 'EDU-RJG-04 (DEFERRED)', 'Highest-demand unowned buying question found. Recommend an Education ownership decision; BC-024 links to it once it exists.', 'Oct-Jan peak', 'EDUCATION_OWNER_DEFERRED'),
 ('How to choose / buy an engagement ring', 'how to choose an engagement ring (1,000); how to pick an engagement ring (1,000); how to buy an engagement ring (720); engagement ring buying guide (170)',
  'Already covered by the existing deferred article and EDU-LG-10.', 'EXIST-BLOG-ER-ONLINE; EDU-LG-10; EDU-RJG-04 (DEFERRED)', 'Refresh the existing online-ring article before November instead of publishing a new one.', 'Year-round', 'EXISTING_PAGE_OWNER'),
 ('Necklace length chart / guide', 'necklace length chart (9,900); necklace length guide (1,900)', 'Practical sizing reference: Education type. No owner in Stage 14/15.',
  'none (Education gap)', 'Propose an Education page (Ring & Jewellery Guides). Dec peak 1.6-1.9x, and it supports BC-006.', 'Before Nov (gift season)', 'EDUCATION_GAP'),
 ('Bracelet size guide', 'how to measure bracelet size (1,900); bracelet size guide (480)', 'Practical sizing reference: Education type. No owner.', 'none (Education gap)', 'Education page candidate; supports BC-021 and tennis bracelet sales.', 'Before Nov', 'EDUCATION_GAP'),
 ('Engagement ring insurance', 'engagement ring insurance (8,100)', 'Evergreen ownership question: Education type. No owner. HOD does not sell insurance.', 'none (Education gap)', 'Education candidate; natural link from post-proposal content.', 'Dec-Jan (after proposals)', 'EDUCATION_GAP'),
 ('How to clean an engagement ring', 'how to clean engagement ring (1,900); engagement ring care (170)', 'Care belongs to Education.', 'EDU-RJG-03 (CONDITIONAL)', 'Activate EDU-RJG-03 with diamond-ring care (demand is proven here).', 'Year-round', 'EXISTING_PAGE_OWNER'),
 ('Finding her ring size secretly (proposal)', 'how to find out her ring size without asking (10)', 'Ring size is owned by EDU-RJG-02.', 'EDU-RJG-02', 'Add a section to EDU-RJG-02; proposal posts link to it.', 'Oct-Dec', 'EXISTING_PAGE_OWNER'),
 ('Diamond stud size / what carat studs', 'diamond stud size chart (110); what size diamond studs (20)', 'EDU-4C-07 owns carat-for-earrings questions.', 'EDU-4C-07', 'Ensure EDU-4C-07 has an earrings section (Stage 19 update candidate).', 'Dec peak', 'EXISTING_PAGE_OWNER'),
 ('Lab-grown vs natural for holiday gifts / proposals', 'lab grown vs natural diamonds (EXISTING_DATA; Dec index 1.68 for the cluster)', 'Owned by EDU-LG-02; a blog version would cannibalize a ranking page.',
  'EDU-LG-02', 'Refresh EDU-LG-02 before November (December peak measured from Stage 4/6 monthly data).', 'Nov-Dec', 'EXISTING_PAGE_OWNER'),
 ('Are lab-grown diamonds real? (gift-buyer worry)', 'are lab grown diamonds real (EXISTING_DATA; cluster Dec index 1.61)', 'Owned by EDU-LG-01.', 'EDU-LG-01', 'Refresh before November.', 'Nov-Dec', 'EXISTING_PAGE_OWNER'),
 ('4Cs quick guide for gift buyers', '4cs of diamonds (EXISTING_DATA; EDU-4C-00 cluster Dec index 1.52)', 'Owned by EDU-4C-00.', 'EDU-4C-00', 'Gift posts link to it; no blog duplicate.', 'Nov-Dec', 'EXISTING_PAGE_OWNER'),
 ('Will lab-grown diamonds get cheaper?', 'are lab grown diamonds getting cheaper (20); will lab-grown diamonds get cheaper (EXISTING_DATA)', 'Owned by EDU-LG-05.', 'EDU-LG-05', 'BC-002 links to it.', 'Year-round', 'EXISTING_PAGE_OWNER'),
 ('Engagement ring styles (toi et moi, east-west, bezel, hidden halo)', 'toi et moi ring (27,100); bezel engagement ring (22,200); hidden halo engagement ring (8,100); east west engagement ring (4,400); elongated hexagon engagement ring (2,400)',
  'Product-led style heads reserved for the conditional COM-ER style subcategories. BC-031 covers them as trend sections.', 'COM-ER style subcategories (CONDITIONAL, Stage 12 D-07)',
  'If the SERP check shows informational "meaning" intent for toi et moi, add a single meaning post in 2027.', 'Jan-Feb', 'RESERVED_COMMERCIAL_PAGE'),
 ('Tennis bracelet / stud earrings / huggies / pendants / eternity bands (category heads)', 'tennis bracelet (135,000); diamond stud earrings (49,500); heart necklace (27,100); huggie earrings (22,200); eternity ring (12,100); diamond pendant (8,100)',
  'Category/product heads (product-led SERPs). The Blog never targets them (Stage 13 section 10 rule 7). Blogs BC-021, BC-025, BC-023 link to them.', 'COM-FJ-BRACELETS; COM-FJ-EARRINGS; COM-FJ-NECKLACES; COM-WB', 'Evidence for the Stage 12 D-07 subcategory gate (tennis, studs, hoops & huggies).', 'Dec peak', 'RESERVED_COMMERCIAL_PAGE'),
 ('Custom engagement rings (commercial)', 'custom engagement ring (40,500); custom jewelry (40,500); design your own engagement ring (5,400); bespoke engagement ring (1,300)',
  'Commercial service intent owned by COM-BESPOKE. BC-001 takes only the timeline question.', 'COM-BESPOKE', 'Strong evidence for Bespoke sub-pages (Stage 12: CONDITIONAL).', 'Dec peak (2.5x)', 'RESERVED_COMMERCIAL_PAGE'),
 ('Heirloom ring redesign', 'heirloom ring redesign (90); redesign old jewelry (70)', 'Redesign/remodel service not confirmed.', 'COM-BESPOKE (if offered)', 'Craft post once the service is confirmed; a strong holiday angle.', 'Oct-Dec', 'BUSINESS_DEPENDENCY'),
 ('Hip hop / iced-out lab-diamond jewellery launch', 'hip hop jewelry (4,400); iced out chain (5,400); cuban link chain diamond (720); mens diamond jewelry (880)',
  '/hiphop is a Coming Soon placeholder (Stage 1).', 'Hip Hop collection (placeholder)', 'BLOG-LAUNCH post when the collection goes live.', 'Launch date', 'BUSINESS_DEPENDENCY'),
 ('T-bar collection story', 't bar necklace (2,400); t bar bracelet (170)', 'Collection form undecided (Stage 12). "t bar necklace" is a shopping head.', 'COM-CURATED-TBAR (undecided)', 'BLOG-LAUNCH/Craft story after the collection decision.', 'Any', 'BUSINESS_DEPENDENCY'),
 ('Sweetest Day jewellery gifts', 'sweetest day gifts (27,100); sweetest day gift ideas (590)', 'Oct 17, 2026 is under 3 weeks from the calendar start; product-led SERP; regional (Midwest) holiday.', 'none', 'Reconsider for 2027 (publish by early Sep 2027) only if HOD wants Midwest gifting.', 'Sep-Oct 2027', 'LEAD_TIME_INSUFFICIENT_2026'),
 ('Halloween / spooky jewellery', 'halloween jewelry (2,400); spooky jewelry (140)', 'Costume/novelty intent; no fine-diamond fit.', 'none', 'none', 'Oct', 'NOT_HOD_FIT'),
 ('October birthstone', 'october birthstone (246,000)', 'Opal/tourmaline; HOD does not sell gemstones (Stage 12 D-16: gemstone categories NOT_PROPOSED).', 'none', 'Only if a gemstone line launches.', 'Oct', 'NOT_HOD_FIT'),
 ('Thanksgiving gifts / Friendsgiving', 'thanksgiving gifts (3,600); friendsgiving gifts (720)', 'Hostess-gift intent, not fine jewellery. Thanksgiving is used only as the start of engagement season (BC-016).', 'none', 'none', 'Nov', 'NOT_HOD_FIT'),
 ('Thanksgiving proposal ideas (standalone)', 'thanksgiving proposal ideas (40); thanksgiving proposal (30)', 'Too small for its own post; folded into BC-016 as secondaries.', 'BC-016', 'none', 'Nov', 'MERGED'),
 ('Winter proposal ideas (standalone)', 'winter proposal ideas (480)', 'Likely SERP overlap with Christmas proposal ideas; merged into BC-017 to avoid near-duplicate seasonal posts.', 'BC-017', 'Split out only if SERP validation shows distinct results.', 'Nov-Dec', 'MERGED'),
 ('Diwali jewellery gift guide', 'diwali gifts (2,400); diwali gift ideas (1,300); diwali jewelry (70)', 'Generic gift intent (product SERPs); the target audience is a business decision. The Surat/Diwali brand angle is in BC-015.', 'none', 'Diwali 2027 is ~Oct 29: publish by early Oct 2027 if chosen.', 'Oct-Nov', 'FUTURE_BUSINESS_DECISION'),
 ('What is a lariat necklace', 'what is a lariat necklace (390); lariat necklace (18,100 head)', 'Only one lariat product; low informational demand.', 'COM-FJ-NECKLACES', 'Mention in BC-006; revisit if the lariat range grows.', 'Year-round', 'BACKLOG_LOW_PRIORITY'),
 ('Wedding band trends', 'wedding band trends (390); wedding ring trends (390)', 'Peaks in August, not Q4.', 'none', 'Spring 2027 Style post.', 'Apr-Aug 2027', 'FUTURE_WINDOW'),
 ('Just engaged: what to do next (insure, size, clean)', 'not measured (e.g. "just got engaged what to do")', 'Unmeasured; the practical parts are Education-owned (RJG-02, RJG-03, insurance gap).', 'EDU-RJG-02; EDU-RJG-03', 'Measure in a future keyword call; publish late Dec 2027 if demand exists.', 'Dec 26-Jan', 'UNMEASURED'),
 ('Do men get engagement rings? / must engagement rings be diamond?', 'do men get engagement rings too (260); do engagement rings have to be diamond (260); can you return an engagement ring (480) (EXISTING_DATA, CL-122)',
  'Stage 15 DEFERRED to EDU-RJG-04 (Education).', 'EDU-RJG-04 (DEFERRED)', 'Include in EDU-RJG-04 if approved.', 'Year-round', 'EXISTING_PAGE_OWNER'),
 ('Graduation / birthday jewellery gifts', 'graduation jewelry gift (1,000); birthday jewelry gifts (140)', 'Outside the Q4 window (graduation peaks in May) or product-led with low demand.', 'COM-FJ', 'Graduation guide by mid-April 2027.', 'Apr-May 2027', 'FUTURE_WINDOW'),
 ('Engagement ring shopping together', 'engagement ring shopping together (210)', 'Low demand; weak differentiation.', 'none', 'Possible section in BC-014.', 'Year-round', 'BACKLOG_LOW_PRIORITY'),
]
with open(os.path.join(OUT, 'blog_topic_backlog.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['backlog_id', 'topic', 'keyword', 'reason_not_scheduled', 'owner_page_if_existing', 'future_opportunity', 'seasonal_window', 'decision_code'])
    for i, b in enumerate(B, 1):
        w.writerow([f'BL-{i:03d}', *b[:6], b[6]])
import collections
print('keyword rows', len(rows), collections.Counter(r['disposition'] for r in rows))
print('backlog', len(B))
