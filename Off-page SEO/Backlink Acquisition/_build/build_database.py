"""Build 01-HOD-BACKLINK-ACQUISITION-DATABASE.csv from curated rows + saved evidence.

Inputs (read-only): _raw/dataforseo/C2..C6, _raw/page-checks/*.json
Output: 01-HOD-BACKLINK-ACQUISITION-DATABASE.csv (overwritten by each run; nothing else is touched).
Competitor target URLs, link attributes and first/last-seen dates for gap rows are looked up from the
saved provider/live-check files, not typed by hand. Priority is computed from the documented formula
(see 05-METHODOLOGY-AND-DATA-LIMITATIONS.md section 7)."""
import csv, json, os, re
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, '_raw')
DATE = '2026-10-10'
HP = 'https://www.houseofdiams.com/'
BESPOKE = 'https://www.houseofdiams.com/bespoke'
ER = 'https://www.houseofdiams.com/engagement-rings'
A_REAL = 'https://www.houseofdiams.com/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide'
A_LGVN = 'https://www.houseofdiams.com/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams'
A_CVD = 'https://www.houseofdiams.com/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams'
A_ONLINE = 'https://www.houseofdiams.com/blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-of-diams'
A_SHAPES = 'https://www.houseofdiams.com/blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of-diams'
A_SIZE = 'https://www.houseofdiams.com/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams'
A_GOLD = 'https://www.houseofdiams.com/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams'
EARRINGS = 'https://www.houseofdiams.com/fine-jewellery/earrings'
WB_HER = 'https://www.houseofdiams.com/wedding-bands/for-her'

G0 = ('Global readiness gate G0 (see 05 §8): /shipping placeholder text and empty /returns must be fixed (F-A1, F-A2), '
      'public contact details (F-C2) and company identity / named spokesperson (F-C1) confirmed, and unverified claims '
      '(IGI/GIA, lifetime warranty, overnight shipping) removed before any outreach.')
AWS = 'Link targets must be re-checked after the AWS cut-over (URL stability UNKNOWN).'

# ---------- evidence loaders ----------
def norm(u):
    return re.sub(r'^https?://(www\.)?', '', u).rstrip('/')

prov = {}   # url_from -> list of provider link rows
for fn, call in [('C2_processed.csv', 'C2'), ('C3_processed.csv', 'C3')]:
    for r in csv.DictReader(open(os.path.join(RAW, 'dataforseo', fn), encoding='utf-8')):
        prov.setdefault(r['url_from'], []).append(r)
broken = {}
for r in csv.DictReader(open(os.path.join(RAW, 'dataforseo', 'C5_processed.csv'), encoding='utf-8')):
    broken.setdefault(r['url_from'], []).append(r)
live = {}
for fn in ['gap_pages_2026-10-10.json', 'extra_pages_2026-10-10.json']:
    for x in json.load(open(os.path.join(RAW, 'page-checks', fn))):
        live[x['url']] = x
ranks = {i['target']: i['rank'] for i in json.load(open(os.path.join(RAW, 'dataforseo', 'C6_bulk_ranks_2026-10-10.json')))['items']}
c4 = {r['referring_domain']: r for r in csv.DictReader(open(os.path.join(RAW, 'dataforseo', 'C4_processed.csv'), encoding='utf-8'))}
_c1 = json.load(open(os.path.join(RAW, 'dataforseo', 'C1_hod_backlinks_one_per_domain_2026-10-10.json')))
HOD_REF = {i['domain_from'].replace('www.', '') for i in _c1['tasks'][0]['result'][0]['items']}
titles = {}
for fn in ['routes_2026-10-10.json', 'routes_subpages_2026-10-10.json', 'gap_pages_2026-10-10.json', 'extra_pages_2026-10-10.json']:
    for x in json.load(open(os.path.join(RAW, 'page-checks', fn))):
        if x.get('title') and x.get('status') == 200:
            titles[norm(x['url'])] = x['title']
for k, v in broken.items():
    if v and v[0]['page_from_title']:
        titles.setdefault(norm(k), v[0]['page_from_title'].strip())

def norm(u):
    return re.sub(r'^https?://(www\.)?', '', u).rstrip('/')

def provider_rows(url, table):
    n = norm(url)
    out = []
    for k, v in table.items():
        if norm(k) == n:
            out += v
    return out

def gap_evidence(url):
    """Return (competitor domains, competitor target URLs, attributes text, evidence class, first/last seen, title)."""
    pr = provider_rows(url, prov)
    lv = live.get(url) or next((v for k, v in live.items() if norm(k) == norm(url)), None)
    comps, targets, attrs = OrderedDict(), [], []
    seen_txt = ''
    for r in pr:
        d = r['competitor_target']
        comps[d] = 1
        if len(targets) < 4 and r['url_to'] not in targets:
            targets.append(r['url_to'])
        attrs.append(f"{d}: provider dofollow={r['dofollow']}{(' attrs=' + r['attributes']) if r['attributes'] else ''}")
    if pr:
        fs = min(r['first_seen'] for r in pr if r['first_seen']); ls = max(r['last_seen'] for r in pr if r['last_seen'])
        seen_txt = f'provider first_seen {fs}, last_seen {ls}'
    live_ok = bool(lv and lv.get('status') == 200 and lv.get('competitor_links'))
    if lv and lv.get('competitor_links'):
        rel = OrderedDict()
        for c in lv['competitor_links']:
            rel.setdefault(c['domain'], set()).add(c['rel'] or 'no rel')
        attrs.append('LIVE ' + DATE + ': ' + '; '.join(f"{d} rel={'/'.join(sorted(v))}" for d, v in list(rel.items())[:6]))
        for d in rel:
            comps[d] = 1
    if pr and live_ok:
        ev = 'PROVIDER_AND_LIVE_VERIFIED'
    elif pr:
        ev = 'PROVIDER_VERIFIED_LIVE_' + (f"BLOCKED_HTTP_{lv.get('status')}" if lv else 'NOT_CHECKED')
    elif live_ok:
        ev = 'LIVE_PAGE_VERIFIED'
    else:
        ev = 'NOT_VERIFIED'
    if not targets and lv:
        for c in lv.get('competitor_links', []):
            if c['href'] not in targets and len(targets) < 4:
                targets.append(c['href'])
    title = (lv or {}).get('title') or (pr[0]['page_from_title'] if pr else '')
    return list(comps), targets, ' | '.join(attrs[:8]), ev, seen_txt, title, lv

COLS = ['Opportunity ID', 'Prospect domain', 'Prospect URL / source-page URL', 'Source-page title', 'Opportunity category',
        'Domain relevance', 'Target audience relevance', 'Authority metric', 'Authority metric provider', 'Authority metric type',
        'Competitor linking?', 'Competitor domain(s)', 'Verified competitor backlink URL', 'Existing HOD backlink?',
        'Link type / acquisition route', 'Link attributes, where verifiable', 'Potential HOD target page',
        'Potential anchor text or citation wording', 'Outreach angle', 'Contact name, if verified',
        'Public contact email or contact-page URL', 'Contact/source evidence URL', 'Acquisition feasibility', 'Priority',
        'Priority rationale', 'Outreach status', 'Next action', 'Research source / provider', 'Date researched',
        'Verification notes', 'Limitations / dependencies',
        # helper columns
        'Evidence class', 'Score R (relevance 0-3)', 'Score Q (source quality 0-3)', 'Score P (pathway 0-3)',
        'Score G (gap evidence 0-2)', 'Score F (feasibility 0-3)', 'Score V (business value 0-3)', 'Priority score (0-17)',
        'DataForSEO call ref', 'Queue rank']

ROWS = []

def add(oid, domain, url, cat, drel, arel, route, target, anchor, angle, contact, contact_ev, R, Q, P, F, V,
        next_action, notes='', limits='', cname='', title='', gap=True, comp_override=None, status=None,
        disq=False, source='', call='', ev_override=None, G_override=None, queue=''):
    comps, targets, attrs, ev, seen, ltitle, lv = gap_evidence(url) if gap else ([], [], '', 'PUBLIC_SOURCE_PROSPECT', '', '', None)
    if comp_override is not None:
        comps, targets, attrs, ev = comp_override
    if ev_override:
        ev = ev_override
    G = G_override if G_override is not None else (2 if ev == 'PROVIDER_AND_LIVE_VERIFIED' else 1 if ev.startswith('PROVIDER') or ev == 'LIVE_PAGE_VERIFIED' or ev == 'PROVIDER_DOMAIN_LEVEL' else 0)
    score = R + Q + P + G + F + V
    if disq:
        pri, st = 'NONE', 'DISQUALIFIED'
    else:
        pri = 'P1' if (score >= 14 and F >= 2 and P >= 2 and R >= 3) else 'P2' if score >= 10 else 'P3'
        st = status or ('PRIORITIZED' if pri == 'P1' else 'VERIFIED_PROSPECT')
    feas = 'HIGH' if F == 3 else 'MEDIUM' if F == 2 else 'LOW'
    reason = (f"Score {score}/17 (R{R} Q{Q} P{P} G{G} F{F} V{V}). " +
              ('Disqualified: ' + notes.split('DISQ:')[1].split('|')[0].strip() if disq and 'DISQ:' in notes else
               'P1 requires score >=14 with R=3, F>=2 and P>=2. ' if pri == 'P1' else
               'P2 = score 10-13 or a P1-level score that misses a P1 gate. ' if pri == 'P2' else
               'P3 = score <=9: longer-term, lower-confidence or resource-intensive. ' if pri == 'P3' else ''))
    comp_flag = 'Yes' if comps else ('Unknown' if not gap else 'No')
    ROWS.append({
        'Opportunity ID': oid, 'Prospect domain': domain, 'Prospect URL / source-page URL': url,
        'Source-page title': title or ltitle or titles.get(norm(url), 'NOT CAPTURED (no HTTP 200 to scripted fetch on 2026-10-10)'), 'Opportunity category': cat, 'Domain relevance': drel,
        'Target audience relevance': arel,
        'Authority metric': ranks.get(domain.replace('www.', ''), ''),
        'Authority metric provider': 'DataForSEO Backlinks API (bulk_ranks)' if domain.replace('www.', '') in ranks else 'NOT COLLECTED',
        'Authority metric type': 'DataForSEO domain Rank, 0-1000 scale, collected 2026-10-10 (third-party estimate; not a Google metric)' if domain.replace('www.', '') in ranks else '',
        'Competitor linking?': comp_flag, 'Competitor domain(s)': '; '.join(comps),
        'Verified competitor backlink URL': '; '.join(targets) if targets else ('Domain-level only (C4 domain_intersection); no source-page URL retrieved' if ev == 'PROVIDER_DOMAIN_LEVEL' else ''),
        'Existing HOD backlink?': ('Yes (C1 — spam-pattern link)' if domain.replace('www.', '') in HOD_REF else 'No (domain absent from C1 HOD referring domains, 2026-10-10)'),
        'Link type / acquisition route': route,
        'Link attributes, where verifiable': attrs or 'Not verifiable until a link exists',
        'Potential HOD target page': target, 'Potential anchor text or citation wording': anchor,
        'Outreach angle': angle, 'Contact name, if verified': cname,
        'Public contact email or contact-page URL': contact, 'Contact/source evidence URL': contact_ev,
        'Acquisition feasibility': feas, 'Priority': pri, 'Priority rationale': reason + (notes.split('WHY:')[1].split('|')[0].strip() if 'WHY:' in notes else ''),
        'Outreach status': st, 'Next action': next_action,
        'Research source / provider': source or ('DataForSEO Backlinks API ' + call + ' + live curl/browser page check' if gap else 'Public web (live curl page check + web search)'),
        'Date researched': DATE,
        'Verification notes': ('; '.join(x for x in [seen, re.sub(r'(DISQ|WHY):[^|]*\|?', '', notes).strip()] if x)),
        'Limitations / dependencies': limits,
        'Evidence class': ev, 'Score R (relevance 0-3)': R, 'Score Q (source quality 0-3)': Q, 'Score P (pathway 0-3)': P,
        'Score G (gap evidence 0-2)': G, 'Score F (feasibility 0-3)': F, 'Score V (business value 0-3)': V,
        'Priority score (0-17)': score, 'DataForSEO call ref': call, 'Queue rank': queue})

# =====================================================================================
# A. COMPETITOR BACKLINK GAP — verified pages linking to competitors, not to HOD
# =====================================================================================
add('GAP-001', 'loveyoutomorrow.com', 'https://loveyoutomorrow.com/best-online-custom-engagement-ring-designers/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'EDITORIAL_ROUNDUP_INCLUSION', BESPOKE, 'House of Diams (brand name); descriptive: "custom engagement rings from House of Diams"',
    'Roundup of online custom-ring designers, updated 2026-09-25. Offer HOD for evaluation as an online bespoke option, with the confirmed process facts only: design typically 2–3 weeks to make plus about 6–9 days delivery, stone-dependent, never guaranteed.',
    'https://loveyoutomorrow.com/contact-us/', 'https://loveyoutomorrow.com/ (homepage nav "Contact Us")', 3, 2, 2, 2, 3,
    'After G0: send a short evaluation offer to the contact page, referencing the article by name and offering product/process facts and images; do not ask for a link or offer payment.',
    notes='Browser check: byline Kelly Warner, modified 2026-09-25, affiliate disclosure, competitor links rel=noopener. Contact page returned Cloudflare 403 to scripted fetch (route exists in site nav). WHY: Closest topical match to HOD bespoke in the whole dataset; article recently updated.',
    limits=G0 + ' Site is affiliate-funded; inclusion may depend on an affiliate program HOD does not have (UNKNOWN). ' + AWS,
    cname='Kelly Warner (article byline)', call='C2')
add('GAP-002', 'bridalmusings.com', 'https://bridalmusings.com/156203/where-to-buy-wedding-engagement-rings/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'EDITORIAL_ROUNDUP_INCLUSION', ER, 'House of Diams',
    'Annual "where to buy engagement rings online" roundup. Offer HOD as an online engagement-ring and bespoke option with verified product facts.',
    'info@bridalmusings.com', 'https://bridalmusings.com/start', 3, 3, 3, 2, 3,
    'After G0: email info@bridalmusings.com with a brief, fact-checked brand note for the 2027 update of the roundup.',
    notes='WHY: Wedding publication, roundup updated for 2026, public email route verified on its contact page.',
    limits=G0 + ' Competitor links carry rel=noopener / noreferrer (affiliate tracking may be involved; UNKNOWN). ' + AWS, call='C3')
add('GAP-003', 'bridalmusings.com', 'https://bridalmusings.com/185996/best-places-to-buy-wedding-bands-online/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'EDITORIAL_ROUNDUP_INCLUSION', WB_HER, 'House of Diams',
    'Wedding-band roundup; pitch only the women\'s wedding-band range that exists today.',
    'info@bridalmusings.com', 'https://bridalmusings.com/start', 3, 3, 3, 1, 2,
    'Bundle with GAP-002 as one email once the men\'s range question (F-E3) is answered.',
    limits=G0 + ' Men\'s wedding bands are empty / unconfirmed (F-E3); pitch would be women\'s bands only. ' + AWS, call='C2')
add('GAP-004', 'theplunge.com', 'https://theplunge.com/engagement-rings/buying-diamond-engagement-ring-online-or-physical-store',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'EDITORIAL_PITCH', A_ONLINE, 'descriptive: "how to choose a lab-grown engagement ring online" (House of Diams guide)',
    'Men\'s engagement-advice site comparing online vs in-store ring buying. Offer HOD\'s existing online-buying guide as a resource, or HOD as an online example.',
    'http://theplunge.com/aboutus', 'https://www.theplunge.com/ (footer About / Press / Advertise)', 3, 2, 2, 2, 3,
    'After G0 and a fact-check refresh of the HOD guide: contact via the About page; offer the guide as a supporting resource.',
    notes='Competitor links on page have no rel attribute (followed) per live check. No public email found.',
    limits=G0 + ' No named editor or email verified. ' + AWS, call='C2')
add('GAP-005', 'theplunge.com', 'https://www.theplunge.com/engagement-rings/radiant-cut-diamond-engagement-ring-buyers-guide',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'EDITORIAL_ROUNDUP_INCLUSION', ER, 'House of Diams',
    'Shape buyer\'s guide that features retailer ring examples; HOD sells radiant-cut designs.',
    'http://theplunge.com/aboutus', 'https://www.theplunge.com/', 3, 2, 2, 2, 2,
    'Combine with GAP-004 in one contact; propose radiant-cut product examples.', limits=G0 + ' ' + AWS, call='C2')
add('GAP-006', 'theplunge.com', 'https://www.theplunge.com/engagement-rings/heart-shape-diamond-engagement-ring-buyers-guide',
    'BROKEN_LINK_OPPORTUNITY', 'HIGH', 'HIGH', 'BROKEN_LINK_REPLACEMENT', 'https://www.houseofdiams.com/shop/elowen-heart-halo-engagement-ring',
    'House of Diams heart halo engagement ring (product name)',
    'Page links to a Brilliant Earth product URL that DataForSEO reports as 404. Offer a live heart-shape example as a replacement.',
    'http://theplunge.com/aboutus', 'https://www.theplunge.com/', 3, 2, 2, 1, 2,
    'Re-confirm the dead Brilliant Earth link in a browser, then mention it in the GAP-004 contact.',
    notes='Broken target is a Brilliant Earth product URL (purchase_review) seen as 404 by DataForSEO; not browser-confirmed.',
    limits=G0 + ' Product URLs are the least stable link targets (AWS / catalog changes). ', call='C5',
    comp_override=(['brilliantearth.com'], ['https://www.brilliantearth.com/rings/cyorings/purchase_review/?did=5977752& (404 per DataForSEO)'], 'provider dofollow=True (C5)', 'PROVIDER_VERIFIED_BROKEN'), G_override=1)
add('GAP-007', 'buzzfeed.com', 'https://www.buzzfeed.com/emmamcanaw/best-places-to-buy-custom-engagement-rings-online',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'AFFILIATE_PROGRAM_DEPENDENT', BESPOKE, 'House of Diams',
    'Shopping roundup of custom-ring retailers. All competitor links are rel="sponsored" (commerce/affiliate), so inclusion passes no ranking credit; value is referral traffic and brand visibility.',
    'NOT VERIFIED', 'https://www.buzzfeed.com/emmamcanaw/best-places-to-buy-custom-engagement-rings-online', 3, 3, 1, 2, 3,
    'Do not pitch until HOD decides whether to run an affiliate program; then route via BuzzFeed\'s shopping team (contact route to be verified).',
    notes='Live check: all competitor links rel=sponsored.',
    limits=G0 + ' Requires an affiliate program (business decision, not an SEO action). Sponsored links do not pass ranking credit.', call='C2')
add('GAP-008', 'buzzfeed.com', 'https://www.buzzfeed.com/francinehendrickson/conflict-free-engagement-rings-youll-absolutely-fawn-over',
    'BROKEN_LINK_OPPORTUNITY', 'HIGH', 'HIGH', 'AFFILIATE_PROGRAM_DEPENDENT', ER, 'House of Diams',
    'Shopping list with a dead Brilliant Earth product link (per DataForSEO). Same affiliate dependency as GAP-007.',
    'NOT VERIFIED', 'https://www.buzzfeed.com/', 2, 3, 1, 1, 1,
    'Revisit together with GAP-007 if an affiliate program exists.', limits='Affiliate dependency; sponsored links.', call='C5',
    comp_override=(['brilliantearth.com', 'bluenile.com', 'catbirdnyc.com'], ['https://www.brilliantearth.com/Versailles-Diamond-Ring-(1/2-ct.-tw.)-White-... (404 per DataForSEO)'], 'LIVE: competitor links rel=sponsored', 'PROVIDER_AND_LIVE_VERIFIED'),
    status='REVISIT_LATER')
add('GAP-009', 'reviewed.com', 'https://reviewed.com/style/features/best-places-to-buy-engagement-rings-online',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'EDITORIAL_ROUNDUP_INCLUSION', ER, 'House of Diams',
    'USA Today network shopping guide (15 online ring retailers; states editors choose independently). Offer HOD for evaluation.',
    'NOT VERIFIED', 'https://reviewed.com/style/features/best-places-to-buy-engagement-rings-online', 3, 3, 1, 1, 3,
    'Find the guide author\'s public contact or Reviewed\'s editorial contact page and verify before outreach.',
    notes='Found via public web search; live page verified 38 competitor links. Not in the C2/C3 intersections (so gap = live-page evidence only).',
    limits=G0 + ' Contact route unverified. ' + AWS, source='Web search + live curl page check', call='')
add('GAP-010', 'askmen.com', 'https://www.askmen.com/dating/relationship_advice/how-to-find-unique-engagement-rings-online.html',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'EDITORIAL_PITCH', BESPOKE, 'House of Diams',
    'Men\'s lifestyle guide to unique rings online; HOD bespoke and unusual-cut designs (toi-et-moi, east-west) fit.',
    'NOT VERIFIED', 'https://www.askmen.com/', 3, 3, 1, 2, 2,
    'Verify the AskMen editorial contact; pitch unique-design examples after G0.', notes='Competitor links rel=nofollow (live).',
    limits=G0 + ' Contact route unverified.', call='C2')
add('GAP-011', 'bestlifeonline.com', 'https://bestlifeonline.com/engagement-rings/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'EDITORIAL_ROUNDUP_INCLUSION', ER, 'House of Diams',
    'Engagement rings "for every budget" roundup; offer HOD designs with real price points.',
    'NOT VERIFIED', 'https://bestlifeonline.com/engagement-rings/', 3, 2, 1, 2, 2,
    'Verify editorial contact (site blocks scripted access).', limits=G0 + ' Homepage returned 403 to scripted fetch; route unverified.', call='C2')
add('GAP-012', 'munaluchibridal.com', 'https://www.munaluchibridal.com/munabling-10-unconventional-engagement-rings-for-the-daring-bride/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'EDITORIAL_PITCH', ER, 'House of Diams',
    'US multicultural bridal publication; "unconventional rings" feature. Pitch distinctive designs (toi-et-moi, east-west marquise).',
    'https://www.munaluchibridal.com/contact/', 'https://www.munaluchibridal.com/ (nav Contact / Submissions)', 3, 3, 2, 2, 2,
    'After G0: send a design-led pitch via the contact page; check the submissions page for product-feature rules.',
    limits=G0 + ' ' + AWS, call='C2')
add('GAP-013', 'rings.com', 'https://rings.com/pages/jewelry-buyer-protection-scores',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'REVIEW_REQUEST', HP, 'House of Diams',
    'Study scoring 20 retailers on published buyer-protection policies (deposit, cancellation, returns, warranty, shipping insurance, certification). HOD would only score well once its policies are published.',
    'rodney@rings.com (named on the study page for questions); info@rings.com', 'https://rings.com/pages/jewelry-buyer-protection-scores ; https://rings.com/pages/contact-us', 3, 2, 2, 1, 2,
    'Do NOT contact until /shipping and /returns carry real terms; then ask whether new retailers can be scored.',
    notes='Study page states no compensation for inclusion and no retailer editorial control; scored from public policy pages (collected 2026-05-25). WHY: High relevance, but outcome depends entirely on HOD publishing policies.',
    limits=G0 + ' Scoring would expose missing policies (current /shipping and /returns defects) — reputational risk if pitched early.', call='C2')
add('GAP-014', 'caratbrands.com', 'https://caratbrands.com/reviews/ritani/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'REVIEW_REQUEST', HP, 'House of Diams',
    'Independent retailer-review site ("no retailer has editorial input"). HOD could be reviewed; it cannot be influenced.',
    'editor@caratbrands.com', 'https://caratbrands.com/about/', 3, 2, 2, 1, 2,
    'After G0, optionally notify the editor that HOD exists; accept that the review is independent and may be critical.',
    notes='Competitor links rel=sponsored nofollow (live). About page lists editor@ for errors/outdated info; no review-request process stated.',
    limits=G0 + ' Independent reviewers will assess the same policy gaps.', call='C2')
add('GAP-015', 'labdiamondsreviews.com', 'https://labdiamondsreviews.com/news/choosing-the-right-place-to-buy-a-lab-diamond-engagement-ring/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'REVIEW_REQUEST', ER, 'House of Diams',
    'Lab-diamond specialist blog (Tom Thornbridge) recommending where to buy lab diamond rings. Offer HOD for review.',
    'https://labdiamondsreviews.com/contact/', 'https://labdiamondsreviews.com/about/', 3, 2, 2, 2, 2,
    'After G0: brief note via the contact page with factual brand information.',
    notes='Second linking page: /news/buying-lab-diamonds-online/ (also verified). Author states he is affiliated with major vendors.',
    limits=G0 + ' Affiliate-led site; inclusion may depend on affiliate terms (UNKNOWN).', cname='Tom Thornbridge (site owner, About page)', call='C2')
add('GAP-016', 'clothedup.com', 'https://clothedup.com/best-places-to-buy-lab-grown-diamonds/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'MEDIUM', 'EDITORIAL_ROUNDUP_INCLUSION', ER, 'House of Diams',
    'Lab-grown retailer roundup on a fashion blog.', 'NOT VERIFIED', 'https://clothedup.com/', 3, 1, 1, 2, 1,
    'Low priority; verify a contact route only if capacity allows.', limits='Contact unverified; likely affiliate-led.', call='C2')
add('GAP-017', 'teachjewelry.com', 'https://teachjewelry.com/diamonds/princess-vs-asscher-cut/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'MEDIUM', 'RESOURCE_PAGE_SUGGESTION', A_SHAPES, 'descriptive: "diamond shapes guide" (House of Diams)',
    'Jewelry education site with editorial guidelines; competitor links are nofollow. Possible correction/resource contact only where HOD content adds something.',
    'jacob.clarke@teachjewelry.com (listed on editorial guidelines page for errors)', 'https://teachjewelry.com/about/editorial-guidelines/', 3, 2, 2, 2, 1,
    'Hold; revisit after the shapes guide refresh (EDU-SHP-00, 2026-11-13) is live.', notes='Second page: /diamonds/how-testers-work/.',
    limits='Email is for error reports, not pitches; nofollow links.', cname='Jacob Clarke (founder, per editorial guidelines)', call='C2', status='REVISIT_LATER')
add('GAP-018', 'engagementringbible.com', 'https://www.engagementringbible.com/where-to-buy-an-engagement-ring-online/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'MEDIUM', 'EDITORIAL_ROUNDUP_INCLUSION', ER, 'House of Diams',
    'Small niche guide listing online ring retailers.', 'NOT VERIFIED', 'https://www.engagementringbible.com/', 3, 1, 0, 2, 1,
    'Verify ownership/contact before any action.', limits='No contact route found.', call='C2')
add('GAP-019', 'blufashion.com', 'https://blufashion.com/apparel/jewelry/best-online-jewelry-stores-for-engagement-rings/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'MEDIUM', 'EDITORIAL_ROUNDUP_INCLUSION', ER, 'House of Diams',
    'Fashion blog roundup of online engagement-ring stores (2026).', 'NOT VERIFIED', 'https://blufashion.com/', 3, 1, 0, 2, 1,
    'Verify contact route; low priority.', limits='Contact unverified; likely affiliate.', call='C2')
add('GAP-020', 'everafterguide.net', 'https://www.everafterguide.net/unique-engagement-rings.html',
    'COMPETITOR_BACKLINK_GAP', 'MEDIUM', 'MEDIUM', 'EDITORIAL_ROUNDUP_INCLUSION', ER, 'House of Diams',
    'Wedding-ideas site listing unique rings.', 'NOT VERIFIED', 'https://www.everafterguide.net/', 2, 1, 0, 2, 1,
    'Low priority.', limits='No contact route found.', call='C2')
add('GAP-021', 'howtomoney.com', 'https://www.howtomoney.com/save-money-engagement-ring/',
    'COMPETITOR_BACKLINK_GAP', 'MEDIUM', 'MEDIUM', 'EDITORIAL_PITCH', A_LGVN, 'descriptive: "lab-grown vs natural diamonds comparison"',
    'Personal-finance article on saving on a ring; lab-grown cost angle (no invented price data).', 'NOT VERIFIED', 'https://www.howtomoney.com/', 2, 2, 0, 2, 1,
    'Low priority.', limits='Contact unverified.', call='C2')
add('GAP-022', 'thekrazycouponlady.com', 'https://thekrazycouponlady.com/tips/money/best-places-to-buy-an-engagement-ring',
    'COMPETITOR_BACKLINK_GAP', 'MEDIUM', 'MEDIUM', 'AFFILIATE_PROGRAM_DEPENDENT', ER, 'House of Diams',
    'Deals site; competitor links nofollow noindex — requires deals/affiliate program.', 'NOT VERIFIED', 'https://thekrazycouponlady.com/', 2, 2, 0, 2, 0,
    'Revisit only if HOD runs a deals/affiliate program.', limits='Deal/affiliate dependent.', call='C2', status='REVISIT_LATER')
add('GAP-023', 'ringreel.com', 'https://www.ringreel.com/best-engagement-rings/lab-grown-diamond-stores/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'REVIEW_REQUEST', ER, 'House of Diams',
    'Comparison site with a "how we research" method; competitor links sponsored/nofollow.', 'https://www.ringreel.com/contact-us/', 'https://www.ringreel.com/about/', 3, 1, 2, 2, 1,
    'After G0: optional factual brand note via the contact page.', notes='Second page: /best-engagement-rings/stores/ (also verified).',
    limits='Sponsored/affiliate links; no ranking credit.', call='C3')
add('GAP-024', 'mymillennialguide.com', 'https://www.mymillennialguide.com/best-place-to-buy-engagement-ring/',
    'COMPETITOR_BACKLINK_GAP', 'MEDIUM', 'MEDIUM', 'AFFILIATE_PROGRAM_DEPENDENT', ER, 'House of Diams',
    'Personal-finance roundup; competitor links nofollow.', 'https://www.mymillennialguide.com/contact-us/', 'https://www.mymillennialguide.com/contact-us/', 2, 1, 2, 2, 1,
    'Low priority.', notes='Email on the contact page is labelled for the media kit (advertising), so it is not used as an editorial contact.',
    limits='Advertising-oriented route; avoid paid placement.', call='C3')
add('GAP-025', 'thezoereport.com', 'https://www.thezoereport.com/p/demystifying-lab-grown-diamonds-2-experts-on-the-essential-facts-common-myths-49025282',
    'EXPERT_CONTRIBUTION', 'HIGH', 'HIGH', 'EXPERT_COMMENTARY', A_CVD, 'House of Diams (expert source attribution)',
    'Fashion publication ran an expert Q&A on lab-grown diamonds. Offer a named HOD spokesperson for future lab-grown explainers (CVD vs HPHT, how lab-grown diamonds are graded).',
    'NOT VERIFIED', 'https://www.thezoereport.com/', 3, 3, 1, 2, 3,
    'After F-C1 names a spokesperson: monitor journalist-request platforms (DPR-001/002) for TZR / Bustle Digital Group queries.',
    notes='Competitor links nofollow (live).', limits=G0 + ' Needs a named, verifiable expert; never invent credentials.', call='C3')
add('GAP-026', 'bustle.com', 'https://www.bustle.com/style/engagement-ring-trends-2025',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'EXPERT_COMMENTARY', HP, 'House of Diams',
    'Annual ring-trends story with retailer examples. HOD\'s planned 2027 trends article (BC-031, 2026-12-01) is the hook.',
    'NOT VERIFIED', 'https://www.bustle.com/', 3, 3, 1, 2, 2,
    'Conditional: pitch trend commentary only after BC-031 is published and fact-checked.',
    notes='Competitor links nofollow (live).', limits=G0 + ' Depends on unpublished BC-031. Contact unverified.', call='C5', status='REVISIT_LATER')
add('GAP-027', 'purewow.com', 'https://www.purewow.com/fashion/lab-grown-diamonds-vs-real-diamonds',
    'BROKEN_LINK_OPPORTUNITY', 'HIGH', 'HIGH', 'BROKEN_LINK_REPLACEMENT', A_REAL, 'descriptive: "lab-grown diamonds vs simulants such as moissanite"',
    'Article links to Brilliant Earth\'s moissanite-vs-diamond page, which a browser check confirmed is a 404. HOD\'s live "Are lab-grown diamonds real?" guide covers lab-grown vs simulants (moissanite, CZ) — a partial, honest replacement.',
    'NOT VERIFIED (PureWow editorial-policy page lists only a reprints address)', 'https://www.purewow.com/page/editorial-policy', 3, 3, 1, 2, 1,
    'Find the article author\'s public contact; offer the replacement only after the EDU-LG-01 refresh (2026-12-02) improves the simulant section.',
    notes='Browser confirmed the BE target 404 on 2026-10-10. Other competitor links on the page rel=sponsored.',
    limits='HOD page covers moissanite in one paragraph only; replacement fit is partial. Large publishers rarely swap links for brand content.',
    call='C5', comp_override=(['brilliantearth.com', 'bluenile.com', 'vrai.com', 'cleanorigin.com'], ['https://www.brilliantearth.com/news/moissanite-vs-diamond/ (404, browser-confirmed)'], 'BE link: provider dofollow=False; LIVE rel=noopener nofollow; others rel=sponsored', 'PROVIDER_AND_LIVE_VERIFIED'),
    status='REVISIT_LATER')
add('GAP-028', 'nearlywed.com', 'https://nearlywed.com/fashion-beauty/what-are-lab-created-diamonds/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'EDITORIAL_PITCH', A_REAL, 'descriptive: "are lab-grown diamonds real" guide',
    'Wedding site explainer on lab-created diamonds linking retailers. Offer HOD as an example or its guide as a resource.',
    'NOT VERIFIED', 'https://nearlywed.com/', 3, 2, 0, 2, 1, 'Verify contact route.', limits='Contact unverified.', call='C5')
add('GAP-029', 'popsugar.com', 'https://www.popsugar.com/love/engagement-rings-decade-46398642',
    'COMPETITOR_BACKLINK_GAP', 'MEDIUM', 'HIGH', 'EDITORIAL_PITCH', HP, 'House of Diams',
    'Evergreen ring-style feature; ad-hoc product inclusion only.', 'NOT VERIFIED', 'https://www.popsugar.com/', 2, 3, 0, 2, 1,
    'Long-term: commerce pitch if an affiliate program exists.', limits='Older article; contact unverified.', call='C2')
add('GAP-030', 'elitedaily.com', 'https://www.elitedaily.com/p/the-best-engagement-ring-style-for-you-based-on-your-zodiac-sign-8088837',
    'COMPETITOR_BACKLINK_GAP', 'MEDIUM', 'HIGH', 'EDITORIAL_PITCH', HP, 'House of Diams',
    'Lifestyle ring-style piece; low feasibility.', 'NOT VERIFIED', 'https://www.elitedaily.com/', 2, 3, 0, 2, 0, 'Low priority.', limits='Contact unverified.', call='C2')
add('GAP-031', 'glamour.com', 'https://www.glamour.com/story/lauren-conrads-engagement-ring',
    'COMPETITOR_BACKLINK_GAP', 'MEDIUM', 'HIGH', 'EDITORIAL_PITCH', HP, 'House of Diams',
    'Celebrity-inspired ring roundup; links nofollow.', 'NOT VERIFIED', 'https://www.glamour.com/', 2, 3, 0, 2, 0, 'Low priority.', limits='Contact unverified; celebrity news-led.', call='C2')
add('GAP-032', 'brit.co', 'https://www.brit.co/engagement-ring-trends-by-country/',
    'COMPETITOR_BACKLINK_GAP', 'MEDIUM', 'HIGH', 'EDITORIAL_PITCH', HP, 'House of Diams',
    'Engagement-trends feature; Brit + Co lists an editorial email.', 'edit@brit.co', 'https://www.brit.co/contact/', 2, 3, 2, 2, 1,
    'Conditional on BC-031 (trends) being published.', limits='Depends on unpublished BC-031.', call='C5', status='REVISIT_LATER')
add('GAP-033', 'foxnews.com', 'https://www.foxnews.com/deals/proposal-engagement-rings',
    'BROKEN_LINK_OPPORTUNITY', 'MEDIUM', 'HIGH', 'AFFILIATE_PROGRAM_DEPENDENT', ER, 'House of Diams',
    'Deals page with a dead Brilliant Earth product link (DataForSEO 404); commerce links rel=sponsored.', 'NOT VERIFIED', 'https://www.foxnews.com/deals/proposal-engagement-rings', 2, 3, 0, 2, 0,
    'Revisit only with an affiliate program.', limits='Affiliate dependent; sponsored links.', call='C5',
    comp_override=(['brilliantearth.com', 'withclarity.com', 'kay.com', 'zales.com'], ['https://www.brilliantearth.com/rings/cyorings/purchase_review/?did=5977754 (404 per DataForSEO)'], 'LIVE: competitor links rel=sponsored noopener / none', 'PROVIDER_AND_LIVE_VERIFIED'), status='REVISIT_LATER')
add('GAP-034', 'platinumjewelry.com', 'https://platinumjewelry.com/platinum-pulse/holiday-gift-guide/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'EDITORIAL_ROUNDUP_INCLUSION', HP, 'House of Diams',
    'Platinum Guild International gift guides link to retailers selling platinum pieces (second page: /platinum-pulse/wedding-day-jewelry-gift-ideas/).',
    'https://platinumjewelry.com/contact/', 'https://platinumjewelry.com/', 3, 3, 2, 0, 2,
    'Revisit only if HOD confirms platinum products (F-E4).', limits='Platinum availability UNCONFIRMED (F-E4); live catalog lists 10K/14K gold.', call='C2', status='REVISIT_LATER')
add('GAP-035', 'growndiamond.com', 'https://growndiamond.com/compare/best-lab-diamond-retailers-2026',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'MEDIUM', 'AFFILIATE_PROGRAM_DEPENDENT', ER, 'House of Diams',
    'Affiliate comparison page (competitor links nofollow sponsored).', 'NOT VERIFIED', 'https://growndiamond.com/', 3, 1, 0, 2, 0,
    'No action.', limits='Affiliate dependent; DataForSEO Rank 0.', call='C3', status='REVISIT_LATER')
add('GAP-036', 'wedgenerator.com', 'https://wedgenerator.com/brands/',
    'RELEVANT_DIRECTORY', 'MEDIUM', 'MEDIUM', 'BRAND_DIRECTORY_SUBMISSION', ER, 'House of Diams',
    'Small free wedding-tools site with a 50-brand finder (rings category). Inclusion process not stated.', 'tosom@wedgenerator.com', 'https://wedgenerator.com/about/', 2, 1, 2, 2, 1,
    'Low priority: ask whether ring brands can be suggested.', limits='Very low authority (Rank 28); nofollow links.', call='C3')
add('GAP-037', 'newswatchtv.com', 'https://newswatchtv.com/2025/10/24/5-best-online-diamond-retailers-reviewed-for-2025/',
    'COMPETITOR_BACKLINK_GAP', 'MEDIUM', 'MEDIUM', 'NONE', '', '',
    'Not pursued.', '', '', 2, 1, 0, 2, 0, 'Verify whether this is a paid/sponsored segment before any consideration.',
    notes='Review-style "best retailers" page on a TV-segment site; editorial vs paid status could not be determined. DISQ: commercial/sponsored nature unverified; paid placements that pass ranking credit are out of scope |',
    limits='Treat as paid until shown otherwise.', call='C2', disq=True)
add('GAP-038', 'indexall.io', 'https://indexall.io/jewelry/wedding/',
    'COMPETITOR_BACKLINK_GAP', 'LOW', 'LOW', 'NONE', '', '', 'Not pursued.', '', '', 1, 0, 0, 2, 0, 'None.',
    notes='DISQ: generic link directory with no editorial selection — low value |', call='C2', disq=True)
add('GAP-039', 'diamonds.pro', 'https://www.diamonds.pro/guides/most-popular-engagement-ring-shapes-by-state/',
    'COMPETITOR_BACKLINK_GAP', 'HIGH', 'HIGH', 'REVIEW_REQUEST', ER, 'House of Diams',
    'Affiliate review site for diamond retailers (competitor links carry utm tags).', 'NOT VERIFIED', 'https://www.diamonds.pro/', 3, 2, 0, 2, 0,
    'No action now.', limits='Affiliate-led; site blocks scripted access; route unverified.', call='C5', status='REVISIT_LATER')
add('GAP-040', 'destinationido.com', 'https://destinationido.com/planning-and-advice/discover-your-engagement-ring-style/',
    'BROKEN_LINK_OPPORTUNITY', 'HIGH', 'HIGH', 'EDITORIAL_PITCH', A_REAL, 'descriptive: "lab-grown diamonds vs simulants"',
    'Wedding magazine ring-style guide; one link points to Brilliant Earth\'s dead moissanite page (browser-confirmed 404). Partial replacement fit as GAP-027.',
    'https://destinationido.com/about-us/#contact', 'https://destinationido.com/about-us/', 3, 2, 2, 2, 1,
    'Revisit after the EDU-LG-01 refresh.', limits='Partial content fit (moissanite).', call='C5',
    comp_override=(['brilliantearth.com'], ['https://www.brilliantearth.com/news/moissanite-vs-diamond/ (404, browser-confirmed)'], 'provider dofollow=True; LIVE rel=noopener', 'PROVIDER_AND_LIVE_VERIFIED'), status='REVISIT_LATER')

# Broken-link candidates examined and rejected
add('GAP-041', 'premierbridewisconsin.com', 'https://premierbridewisconsin.com/2022/09/23/jefferson-county-wedding-at-bennett-barn/',
    'BROKEN_LINK_OPPORTUNITY', 'MEDIUM', 'LOW', 'NONE', '', '', 'Not pursued.', '', '', 2, 2, 0, 1, 0, 'None.',
    notes='Linked BE men\'s ring-styles page confirmed 404, but the source page itself now returns 404. DISQ: source page no longer exists; HOD has no men\'s range (F-E3) |',
    call='C5', disq=True, comp_override=(['brilliantearth.com'], ['https://www.brilliantearth.com/wedding-ring-guide/mens-wedding-ring-styles/ (404, browser-confirmed)'], 'provider dofollow=True', 'PROVIDER_VERIFIED_SOURCE_GONE'), G_override=1)
add('GAP-042', 'dhgate.com', 'https://fashion.dhgate.com/rings/wedding-band-rings-need-size-and-material-proof-first/',
    'BROKEN_LINK_OPPORTUNITY', 'LOW', 'LOW', 'NONE', '', '', 'Not pursued.', '', '', 1, 0, 0, 1, 0, 'None.',
    notes='Links to BE ring-size page (browser-confirmed 404), nofollow. DISQ: marketplace content blog; low editorial quality |', call='C5', disq=True,
    comp_override=(['brilliantearth.com'], ['https://www.brilliantearth.com/news/how-to-measure-ring-size/ (404, browser-confirmed)'], 'provider dofollow=False', 'PROVIDER_VERIFIED_BROKEN'), G_override=1)
add('GAP-043', 'articlesfactory.com', 'https://www.articlesfactory.com/articles/dating-advice/my-least-favorite-diamond-shapes-for-engagement-rings.html',
    'BROKEN_LINK_OPPORTUNITY', 'LOW', 'LOW', 'NONE', '', '', 'Not pursued.', '', '', 1, 0, 0, 1, 0, 'None.',
    notes='Links to BE diamond-shapes page (browser-confirmed 404), nofollow. Source URL truncated in provider data (verify full path). DISQ: open article directory — a manipulative-link risk category |', call='C5', disq=True,
    comp_override=(['brilliantearth.com'], ['https://www.brilliantearth.com/diamond-education/diamond-shapes/ (404, browser-confirmed)'], 'provider dofollow=False', 'PROVIDER_VERIFIED_BROKEN'), G_override=1)
add('GAP-044', '6ixice.com', 'https://6ixice.com/blogs/news/10k-vs-14k-gold',
    'BROKEN_LINK_OPPORTUNITY', 'MEDIUM', 'MEDIUM', 'NONE', '', '', 'Not pursued.', '', '', 2, 1, 0, 0, 0, 'None.',
    notes='DataForSEO flagged the BE target as 404, but a browser check shows it now redirects to a live guide. DISQ: target no longer broken, and the source is a jewelry retailer (competitor) |', call='C5', disq=True,
    comp_override=(['brilliantearth.com'], ['https://www.brilliantearth.com/news/highest-karat-gold (now redirects; not broken)'], 'provider dofollow=True', 'PROVIDER_FLAG_STALE'), G_override=0)

# Domain-level competitor gap (C4 domain_intersection: links to all 5 competitors, not HOD)
def c4row(oid, domain, url, cat, drel, arel, route, target, anchor, angle, contact, cev, R, Q, P, F, V, nxt, notes='', limits='', cname='', status=None, disq=False, queue=''):
    r = c4.get(domain, {})
    bl = ', '.join(f"{k.replace('backlinks_to_', '')}={v}" for k, v in r.items() if k.startswith('backlinks_to_'))
    add(oid, domain, url, cat, drel, arel, route, target, anchor, angle, contact, cev, R, Q, P, F, V, nxt, notes=notes + (f' C4 backlink counts per competitor: {bl}.' if bl else ''),
        limits=limits, cname=cname, gap=False, status=status, disq=disq, call='C4', source='DataForSEO Backlinks API C4 (domain level) + live homepage check',
        comp_override=(['brilliantearth.com', 'bluenile.com', 'ritani.com', 'vrai.com', 'cleanorigin.com'], [], 'Not available at domain level', 'PROVIDER_DOMAIN_LEVEL'), queue=queue)
c4row('GAP-045', 'jckonline.com', 'https://www.jckonline.com/', 'EDITORIAL_PUBLICATION', 'HIGH', 'MEDIUM', 'PRESS_RELEASE_NEWS', HP, 'House of Diams',
      'US jewelry trade publication (JCK). Trade coverage builds entity credibility; consumer reach is limited. Pitch only genuine news (new collection, verified craft story once F-E6 is confirmed).',
      'https://www.jckonline.com/contact-us/', 'https://www.jckonline.com/ (footer Contact Us)', 3, 3, 2, 2, 2,
      'After G0: prepare a factual brand fact sheet; hold the pitch for real news.', notes='Contact page returned Cloudflare 403 to scripted fetch.', limits=G0)
c4row('GAP-046', 'stylemepretty.com', 'https://www.stylemepretty.com/submissions', 'WEDDING_PUBLICATION', 'MEDIUM', 'HIGH', 'SUBMISSION_FEATURE', HP, 'House of Diams (vendor credit)',
      'Real-wedding / styled-shoot submissions credit vendors. HOD could be credited only if its jewelry is genuinely worn in a submitted shoot (photographer-led).',
      'submissions-help@stylemepretty.com; https://www.stylemepretty.com/submissions', 'https://www.stylemepretty.com/contact/', 2, 3, 2, 1, 2,
      'Long-term: only via genuine photographer collaborations; never pay for placement.', notes='Vendor Guide / Little Black Book is a paid membership — excluded (see DIR-006).', limits='Requires real shoot collaboration.')
c4row('GAP-047', 'weddingchicks.com', 'https://www.weddingchicks.com/submit/', 'WEDDING_PUBLICATION', 'MEDIUM', 'HIGH', 'SUBMISSION_FEATURE', HP, 'House of Diams (vendor credit)',
      'Feature submissions credit vendors; same photographer-led route as GAP-046.', 'https://www.weddingchicks.com/submit/', 'https://www.weddingchicks.com/', 2, 2, 2, 1, 1,
      'Long-term; via genuine shoot collaborations only.', limits='Requires real shoot collaboration; vendor sign-up terms not reviewed.')
c4row('GAP-048', 'etonline.com', 'https://www.etonline.com/', 'LUXURY_PUBLICATION', 'LOW', 'HIGH', 'AFFILIATE_PROGRAM_DEPENDENT', HP, 'House of Diams',
      'Entertainment/shopping outlet linking jewelry retailers (commerce).', 'NOT VERIFIED', 'https://www.etonline.com/', 1, 3, 0, 0, 1, 'No action.', limits='Commerce/affiliate dependent.', status='REVISIT_LATER')
c4row('GAP-049', 'pricescope.com', 'https://www.pricescope.com/', 'OTHER', 'HIGH', 'HIGH', 'COMMUNITY_PARTICIPATION', '', '',
      'Long-running diamond forum (UGC). Not a link-building target: promotional posting violates community norms. Value = brand-reputation monitoring and, later, genuine expert answers by a disclosed HOD staff member.',
      'NOT VERIFIED', 'https://www.pricescope.com/', 3, 2, 1, 1, 1, 'Monitor for brand mentions only; no promotional links.',
      notes='C2 also shows PriceScope threads linking all three top competitors (UGC).', limits='UGC links; forum rules not reviewed.', status='REVISIT_LATER')
c4row('GAP-050', 'holrmagazine.com', 'https://holrmagazine.com/contact', 'LUXURY_PUBLICATION', 'LOW', 'MEDIUM', 'NONE', '', '', 'Not pursued.', '', 'https://holrmagazine.com/contact', 1, 1, 0, 0, 0, 'None.',
      notes='Contact page text includes "guest post" offers. DISQ: guest-post/sponsored-content signals; paid content that passes ranking credit is out of scope |', disq=True)
c4row('GAP-051', 'howigotengaged.com', 'https://www.howigotengaged.com/vendors', 'WEDDING_PUBLICATION', 'HIGH', 'HIGH', 'VENDOR_LISTING', HP, 'House of Diams',
      'Proposal-stories site with a "Proposal vendors" section; listing terms (free vs paid) not stated in the scan.', 'NOT VERIFIED', 'https://www.howigotengaged.com/vendors', 3, 1, 1, 1, 1,
      'Verify whether vendor listings are free and editorial; exclude if paid.', limits='Low authority (Rank 93); terms unverified.', status='VERIFICATION_REQUIRED')

# =====================================================================================
# B. STANDALONE PROSPECTS (public-source research; no competitor-link evidence collected)
# =====================================================================================
def sp(oid, domain, url, cat, drel, arel, route, target, anchor, angle, contact, cev, R, Q, P, F, V, nxt, notes='', limits='', cname='', status=None, disq=False, queue=''):
    add(oid, domain, url, cat, drel, arel, route, target, anchor, angle, contact, cev, R, Q, P, F, V, nxt, notes=notes, limits=limits,
        cname=cname, gap=False, status=status, disq=disq, queue=queue)
# Jewelry / diamond trade publications
sp('PUB-001', 'nationaljeweler.com', 'https://nationaljeweler.com/pages/contact-us', 'EDITORIAL_PUBLICATION', 'HIGH', 'MEDIUM', 'PRESS_RELEASE_NEWS', HP, 'House of Diams',
   'US trade magazine. Editorial staff and beats are listed publicly (fashion and gemstone associate editors). Pitch genuine news only: collection launches, a verified Surat craft story (F-E6), lab-grown design trends.',
   'Editorial staff emails listed on contact page', 'https://nationaljeweler.com/pages/contact-us', 3, 3, 3, 2, 2,
   'After G0: prepare a one-page brand fact sheet and a genuinely newsworthy hook; send to the fashion associate editor.',
   notes='Contact page lists: Michelle Graff (Editor-in-Chief), Lenore Fedow (Senior Editor, News), Natalie Francisco (Associate Editor, Fashion), Lauren McLemore (Associate Editor, Gemstones). No press-release submission process stated.',
   limits=G0 + ' Trade audience (retailers), not consumers; needs real news.', cname='Natalie Francisco (Associate Editor, Fashion) — listed on contact page')
sp('PUB-002', 'idexonline.com', 'https://www.idexonline.com/ContactUs', 'EDITORIAL_PUBLICATION', 'HIGH', 'LOW', 'PRESS_RELEASE_NEWS', HP, 'House of Diams',
   'Diamond trade news with Mumbai and USA contacts; regularly covers Surat lab-grown businesses. Possible trade-news route for a verified Surat story.',
   'usa@idexonline.com; mumbai@idexonline.com', 'https://www.idexonline.com/ContactUs', 3, 2, 2, 1, 1, 'Hold until F-E6 (Surat workshop facts) is confirmed.',
   limits='Trade audience; depends on F-E6.', status='REVISIT_LATER')
sp('PUB-003', 'rapaport.com', 'https://rapaport.com/contact-us/', 'EDITORIAL_PUBLICATION', 'MEDIUM', 'LOW', 'PRESS_RELEASE_NEWS', HP, 'House of Diams',
   'Diamond trade news (positions itself around the natural-diamond trade). Weak fit for a lab-grown jewelry brand.', 'news@rapaport.com', 'https://rapaport.com/contact-us/', 2, 3, 2, 1, 1,
   'Low priority.', limits='Positioning mismatch (natural-diamond focus).')
sp('PUB-004', 'instoremag.com', 'https://instoremag.com/news/press-releases/', 'EDITORIAL_PUBLICATION', 'MEDIUM', 'LOW', 'PRESS_RELEASE_NEWS', HP, 'House of Diams',
   'Trade magazine for US jewelry-store owners; publishes press releases. Audience is retailers, not HOD customers.', 'https://instoremag.com/news/press-releases/', 'https://instoremag.com/', 2, 2, 2, 1, 1, 'Low priority.',
   limits='Retailer audience; submission terms not reviewed (may be paid).')
# Industry associations
sp('ASSOC-001', 'labgrowndiamondcouncil.com', 'https://www.labgrowndiamondcouncil.com/', 'INDUSTRY_ASSOCIATION', 'HIGH', 'MEDIUM', 'MEMBERSHIP_DIRECTORY', HP, 'House of Diams (member listing)',
   'Lab-grown industry body with a Retailers membership category (per trade-press coverage). A member listing would be a relevant entity citation — if HOD qualifies and chooses to join.',
   'NOT VERIFIED (site returned HTTP 525 on 2026-10-10)', 'https://www.surveygizmo.com/s3/4997147/Lab-Grown-Diamond-Council-Application (from web search; not opened)', 3, 2, 1, 2, 2,
   'Re-check the LGDC site, current membership terms, fees and whether a public member directory with links exists; business decision for HOD.',
   notes='Membership tiers (Producers, Suppliers, Retailers, Associates) come from 2016–2019 trade-press coverage; current terms UNKNOWN. DataForSEO Rank 0 (site unreachable / no index data).',
   limits='Membership is a business decision and may cost money; HOD is not a member (do not imply otherwise).', status='VERIFICATION_REQUIRED')
sp('ASSOC-002', 'jewelers.org', 'https://www.jewelers.org/about/join-ja', 'INDUSTRY_ASSOCIATION', 'HIGH', 'HIGH', 'MEMBERSHIP_DIRECTORY', HP, 'House of Diams (member listing)',
   'Jewelers of America: US trade association with a Member Directory and consumer "Find a Jeweler". Relevance depends on HOD having a qualifying US business presence.',
   'https://www.jewelers.org/about/join-ja', 'https://www.jewelers.org/ (nav Join / Member Directory / Find a Jeweler)', 3, 3, 2, 1, 2,
   'Confirm eligibility (US presence — the "New York office" claim is unverified, F-C1) and fees before any decision.',
   limits='Eligibility UNKNOWN; membership is paid and a business decision; directory link attributes unknown.', status='VERIFICATION_REQUIRED')
sp('ASSOC-003', 'americangemsociety.org', 'https://www.americangemsociety.org/membership/', 'INDUSTRY_ASSOCIATION', 'HIGH', 'HIGH', 'MEMBERSHIP_DIRECTORY', HP, 'House of Diams (member listing)',
   'AGS business memberships (Retail, Partner, Emerging Designer) with a consumer "Find a Jeweler". Credentialing requirements are high; long-term.',
   'https://www.americangemsociety.org/contact/', 'https://www.americangemsociety.org/', 3, 3, 2, 0, 2, 'Long-term; review requirements only if HOD pursues credentials.',
   limits='Credential requirements; paid; Emerging Designer page returned 403 to scripted fetch.', status='REVISIT_LATER')
sp('ASSOC-004', 'responsiblejewellery.com', 'https://www.responsiblejewellery.com/membership/apply/', 'INDUSTRY_ASSOCIATION', 'HIGH', 'MEDIUM', 'MEMBERSHIP_DIRECTORY', HP, 'House of Diams (member listing)',
   'Responsible Jewellery Council certification with a "Find a Member" directory. Requires audited certification; substantial commitment.',
   'applications@responsiblejewellery.com', 'https://www.responsiblejewellery.com/membership/apply/', 3, 3, 2, 0, 1, 'Long-term business decision; not an SEO action.',
   limits='Audited certification; paid; must never be claimed before certified.', status='REVISIT_LATER')
sp('ASSOC-005', 'womensjewelryassociation.com', 'https://www.womensjewelryassociation.com/join-wja', 'INDUSTRY_ASSOCIATION', 'HIGH', 'MEDIUM', 'MEMBERSHIP_DIRECTORY', HP, 'House of Diams',
   'Women\'s Jewelry Association: professional/business/global memberships.', 'https://www.womensjewelryassociation.com/content.asp?contentid=321', 'https://www.womensjewelryassociation.com/', 2, 2, 2, 1, 1,
   'Low priority.', limits='Paid membership; directory link value unknown.')
sp('ASSOC-006', 'gjepc.org', 'https://www.gjepc.org/directory-landing.php', 'INDUSTRY_ASSOCIATION', 'HIGH', 'LOW', 'MEMBERSHIP_DIRECTORY', HP, 'House of Diams (member listing)',
   'India\'s Gem & Jewellery Export Promotion Council members directory; relevant to HOD\'s stated Surat base, not to US consumers.',
   'https://www.gjepc.org/contact-us.php', 'https://www.gjepc.org/registration.php', 3, 2, 2, 1, 1, 'Check whether HOD is already a GJEPC member (business question for HOD).',
   limits='Requires Indian exporter registration; HOD company details UNCONFIRMED (F-C1).', status='VERIFICATION_REQUIRED')
# Wedding publications (non-gap routes)
sp('WED-001', 'brides.com', 'https://www.brides.com/editorial-guidelines-5222899', 'WEDDING_PUBLICATION', 'HIGH', 'HIGH', 'EXPERT_COMMENTARY', A_ONLINE, 'House of Diams (expert source attribution)',
   'Brides regularly quotes jewelry experts in ring-shopping advice. A named HOD spokesperson could answer journalist queries (custom-ring timelines, lab-grown basics).',
   'https://www.brides.com/about-us-4777099#toc-contact-us', 'https://www.brides.com/about-us-4777099', 3, 3, 2, 2, 3,
   'After F-C1: route via journalist-request platforms (DPR-001/002) rather than cold pitching.', limits=G0 + ' Needs a named, verifiable expert.')
sp('WED-002', 'greenweddingshoes.com', 'https://greenweddingshoes.com/submissions/', 'WEDDING_PUBLICATION', 'MEDIUM', 'HIGH', 'SUBMISSION_FEATURE', HP, 'House of Diams (vendor credit)',
   'Feature submissions credit vendors (photographer-led).', 'submissions@greenweddingshoes.com', 'https://greenweddingshoes.com/submissions/', 2, 3, 2, 1, 1,
   'Long-term; genuine shoot collaborations only.', limits='Requires real shoot collaboration.')
sp('WED-003', 'zola.com', 'https://www.zola.com/expert-advice', 'WEDDING_PUBLICATION', 'HIGH', 'HIGH', 'EXPERT_COMMENTARY', HP, 'House of Diams',
   'Wedding-planning platform with a large expert-advice library (getting engaged, rings).', 'https://www.zola.com/contact-us', 'https://www.zola.com/expert-advice', 3, 3, 1, 1, 2,
   'Verify whether Zola sources outside experts; low priority until then.', limits='Editorial sourcing process unknown.', status='VERIFICATION_REQUIRED')
sp('WED-004', 'weddingforward.com', 'https://www.weddingforward.com/rings/ring-shopping-tips/', 'WEDDING_PUBLICATION', 'HIGH', 'HIGH', 'EDITORIAL_PITCH', HP, 'House of Diams',
   'Wedding blog with a ring-shopping-tips section.', 'NOT VERIFIED', 'https://www.weddingforward.com/about-us/', 3, 2, 0, 1, 1, 'Verify editorial contact.', limits='Contact unverified.')
sp('WED-005', 'junebugweddings.com', 'https://junebugweddings.com/wedding-blog/best-place-buy-engagement-rings-online/', 'WEDDING_PUBLICATION', 'HIGH', 'HIGH', 'EDITORIAL_ROUNDUP_INCLUSION', ER, 'House of Diams',
   'Roundup of online ring retailers (dated 2023); live page links Clean Origin and James Allen.', 'NOT VERIFIED', 'https://junebugweddings.com/', 3, 3, 0, 1, 1,
   'Check whether the roundup is still updated; vendor directory membership is paid and excluded.', limits='Older article; contact unverified.')
# Digital PR / expert platforms
sp('DPR-001', 'qwoted.com', 'https://www.qwoted.com/for-media/', 'DIGITAL_PR', 'MEDIUM', 'HIGH', 'JOURNALIST_REQUEST_PLATFORM', HP, 'House of Diams (expert source attribution)',
   'Free expert-source platform where journalists post requests. Answer only jewelry/diamond/bridal queries where HOD has verified facts.',
   'https://app.qwoted.com/users/sign_up', 'https://www.qwoted.com/', 3, 3, 3, 2, 3,
   'After F-C1 names a spokesperson: create a free source profile (the user or HOD signs up; Claude does not create accounts).',
   notes='Homepage verified 200; "Join for FREE" route present. Paid tiers exist — free tier only.', limits=G0 + ' Requires a named, verifiable expert and fact-checked answers.')
sp('DPR-002', 'helpareporter.com', 'https://www.helpareporter.com/', 'DIGITAL_PR', 'MEDIUM', 'HIGH', 'JOURNALIST_REQUEST_PLATFORM', HP, 'House of Diams (expert source attribution)',
   'HARO was relaunched free by Featured.com in April 2025 (per press coverage). Daily journalist queries; answer only relevant ones.',
   'https://www.helpareporter.com/', 'https://www.globenewswire.com/fr/news-release/2026/05/26/3301366/0/en/Featured-com-Revives-Connectively-Launches-AI-Co-Pilot-for-PR.html', 3, 2, 2, 2, 3,
   'Verify the current sign-up flow in a browser (scripted fetch got a 429 security checkpoint); sign-up by HOD.',
   notes='Status from web search: Featured.com acquired HARO (Apr 2025) and announced reviving Connectively (May 2026).', limits=G0, status='VERIFICATION_REQUIRED')
sp('DPR-003', 'sourceofsources.com', 'https://sourceofsources.com/', 'DIGITAL_PR', 'MEDIUM', 'HIGH', 'JOURNALIST_REQUEST_PLATFORM', HP, 'House of Diams (expert source attribution)',
   'Free journalist-query digest started by HARO\'s original founder (per 2026 roundups).', 'NOT VERIFIED', 'https://sourceofsources.com/', 3, 2, 1, 2, 2,
   'Verify the official sign-up page (root returned 403 "Index file not found").', limits=G0, status='VERIFICATION_REQUIRED')
sp('DPR-004', 'featured.com', 'https://featured.com/', 'DIGITAL_PR', 'MEDIUM', 'MEDIUM', 'JOURNALIST_REQUEST_PLATFORM', HP, 'House of Diams (expert source attribution)',
   'Expert Q&A platform (owner of relaunched HARO). Free vs paid terms not reviewed.', 'https://featured.com/', 'https://featured.com/', 2, 2, 1, 1, 2,
   'Review terms; avoid pay-to-be-featured options.', limits='Possible paid tiers.', status='VERIFICATION_REQUIRED')
# Directories / review platforms
sp('DIR-001', 'dtcify.com', 'https://dtcify.com/submit', 'RELEVANT_DIRECTORY', 'MEDIUM', 'MEDIUM', 'BRAND_DIRECTORY_SUBMISSION', HP, 'House of Diams',
   'Curated DTC-brand directory with an Engagement & Wedding category that lists Ritani (C2 evidence). Submission requires login; pricing page exists.',
   'https://dtcify.com/submit', 'https://dtcify.com/about', 2, 1, 2, 2, 1, 'Low priority; confirm free submission and editorial review first.',
   notes='C2 shows dtcify.com/brand/ritani and /category/engagement-wedding linking competitors. DataForSEO Rank 0.',
   limits='Possibly paid/sponsored placements (labelled per About page); low authority.')
sp('DIR-002', 'trustpilot.com', 'https://www.trustpilot.com/review/houseofdiams.com', 'OTHER', 'MEDIUM', 'HIGH', 'NONE', HP, '',
   'Review profile for reputation/trust, not links. Only genuine, unincentivized reviews; HOD must not solicit fake or gated reviews.', 'NOT VERIFIED', 'https://www.trustpilot.com/review/houseofdiams.com', 2, 2, 1, 1, 1,
   'Check in a browser whether a profile already exists (scripted fetch blocked).', limits='Not an SEO link opportunity; review-platform policies apply.', status='VERIFICATION_REQUIRED')
sp('DIR-003', 'stonealgo.com', 'https://www.stonealgo.com/our-retailers/', 'DIAMOND_RESOURCE', 'HIGH', 'HIGH', 'VENDOR_LISTING', HP, 'House of Diams',
   'Diamond search engine with retailer partners ("Retailer? Join here"); its custom-ring article links competitors (nofollow). Partnership likely needs a loose-diamond inventory feed.',
   'management@stonealgo.com (labelled "Retailer? Join here")', 'https://www.stonealgo.com/', 3, 2, 2, 0, 1, 'Revisit only if HOD sells loose diamonds (F-E2).',
   notes='Gap evidence: https://www.stonealgo.com/blog/where-to-buy-a-custom-ring/ links BE, Blue Nile, Frank Darling, James Allen (live).',
   limits='HOD does not appear to sell loose stones (F-E2).', status='REVISIT_LATER')
sp('DIR-004', 'gia.edu', 'https://www.gia.edu/retailer-lookup', 'DIAMOND_RESOURCE', 'HIGH', 'HIGH', 'MEMBERSHIP_DIRECTORY', HP, 'House of Diams',
   'GIA Retailer Lookup lists retailers meeting GIA criteria (e.g. GIA-credentialed staff). Long-term only.', 'https://www.gia.edu/retailer-lookup', 'https://www.gia.edu/retailer-lookup', 3, 3, 1, 0, 1,
   'Long-term; eligibility criteria to be confirmed.', limits='Eligibility criteria not verified; HOD certification claims are unconfirmed (F-B1).', status='REVISIT_LATER')
sp('DIR-005', 'theknot.com', 'https://www.theknot.com/', 'WEDDING_PUBLICATION', 'HIGH', 'HIGH', 'VENDOR_LISTING', HP, 'House of Diams',
   'Largest US wedding marketplace (Jewelers vendor category exists). Listing terms and value unverified; site blocked scripted access.',
   'NOT VERIFIED', 'https://www.theknot.com/', 3, 3, 0, 0, 1, 'Verify in a browser whether online-only jewelers can list and whether listings are paid.',
   limits='Access denied to scripted fetch; vendor listings are typically local/paid (UNVERIFIED).', status='VERIFICATION_REQUIRED')
sp('DIR-006', 'stylemepretty.com', 'https://www.stylemepretty.com/vendor-guide', 'RELEVANT_DIRECTORY', 'MEDIUM', 'HIGH', 'NONE', '', '', 'Not pursued.', 'lbb@stylemepretty.com', 'https://www.stylemepretty.com/contact/', 2, 3, 0, 0, 0, 'None.',
   notes='DISQ: Vendor Guide / Little Black Book is a paid membership — a paid listing whose SEO value would depend on passing ranking credit |', disq=True)
sp('DIR-007', 'gemsociety.org', 'https://www.gemsociety.org/advertising/', 'DIAMOND_RESOURCE', 'HIGH', 'MEDIUM', 'NONE', '', '', 'Not pursued.', 'sponsorship@gemsociety.org', 'https://www.gemsociety.org/contact-us/', 3, 3, 0, 0, 0, 'None.',
   notes='Only commercial routes found (advertising/sponsorship). DISQ: paid sponsorship route only; no editorial route identified |', disq=True)

# Execution-queue order (03-OUTREACH-PRIORITY-QUEUE.md): P1 rows 1-5, then the strongest P2 rows 6-10.
QUEUE = {'GAP-002': 1, 'GAP-001': 2, 'DPR-001': 3, 'GAP-004': 4, 'GAP-012': 5,
         'WED-001': 6, 'PUB-001': 7, 'DPR-002': 8, 'ASSOC-001': 9, 'GAP-015': 10}
for r in ROWS:
    r['Queue rank'] = QUEUE.get(r['Opportunity ID'], '')
# =====================================================================================
with open(os.path.join(ROOT, '01-HOD-BACKLINK-ACQUISITION-DATABASE.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    for r in ROWS:
        w.writerow(r)
print('rows', len(ROWS))
from collections import Counter
print(Counter(r['Priority'] for r in ROWS))
print(Counter(r['Opportunity category'] for r in ROWS))
print(Counter(r['Outreach status'] for r in ROWS))
print(Counter(r['Evidence class'] for r in ROWS))
for r in ROWS:
    print(r['Opportunity ID'], r['Priority'], r['Priority score (0-17)'], r['Evidence class'], r['Competitor linking?'], '|', r['Source-page title'][:50])
