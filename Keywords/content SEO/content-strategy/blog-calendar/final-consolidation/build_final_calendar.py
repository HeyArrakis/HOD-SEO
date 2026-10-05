"""Build FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv (2026-10-03).

Inputs (read-only): the locked revised calendar (content-strategy/blog-calendar/blog_content_calendar.csv),
new_items.py (rows added around the locked dates), Stage 15 map, Stage 19 registry, call1/call2 outputs.
Output: exactly one file in FINAL-BLOG-CALENDAR/. QC runs at the end (qc_final_calendar.py).
"""
import csv, os, re, sys, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
from new_items import NEW

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
LOCKED_CSV = os.path.join(ROOT, 'content-strategy/blog-calendar/blog_content_calendar.csv')
OUT_DIR = os.path.join(ROOT, 'FINAL-BLOG-CALENDAR')
OUT = os.path.join(OUT_DIR, 'BLOG_CALENDAR_FINAL.csv')
START, END = dt.date(2026, 10, 4), dt.date(2027, 3, 31)
WEEK1 = dt.date(2026, 9, 28)  # same week numbering as the revised calendar (W01 = Sep 28 - Oct 4)

COLS = ['content_id', 'publish_date', 'day', 'week', 'sequence', 'locked_date_status', 'original_planned_date',
        'content_type', 'content_category', 'status', 'working_title', 'primary_keyword', 'primary_search_volume',
        'secondary_keywords', 'secondary_search_volume', 'keyword_priority', 'search_intent', 'commercial_intent',
        'keyword_difficulty', 'serp_competition', 'serp_page_type', 'serp_features', 'ai_overview', 'paa_present',
        'paa_questions_count', 'ae_o_answer_format', 'season', 'festival', 'occasion', 'event_date', 'lead_time_days',
        'source_stage', 'source_cluster', 'existing_or_new', 'HOD_relevance', 'product_category', 'target_audience',
        'funnel_stage', 'target_url_type', 'target_owner', 'education_or_blog', 'internal_link_targets', 'CTA_direction',
        'cannibalization_status', 'why_scheduled', 'priority_reason', 'notes']

# Locked rows: final content_type / content_category labels (decided per article; the dates are untouched)
LOCKED_TYPE = {
 'BC-001': ('HIGH_INTENT', 'BESPOKE'), 'BC-018': ('OCCASION', 'ANNIVERSARY'), 'BC-003': ('OCCASION', 'GIFTING'),
 'BC-004': ('FESTIVE', 'CHRISTMAS'), 'BC-035': ('OCCASION', 'ANNIVERSARY'), 'BC-036': ('INFORMATIONAL', 'RING_CULTURE'),
 'BC-006': ('BLOG', 'STYLE'), 'BC-008': ('FESTIVE', 'CHRISTMAS'), 'BC-009': ('FESTIVE', 'CHRISTMAS'),
 'BC-007': ('BLOG', 'WEDDING'), 'BC-011': ('INFORMATIONAL', 'RING_CULTURE'), 'BC-037': ('INFORMATIONAL', 'RING_CULTURE'),
 'BC-014': ('OCCASION', 'PROPOSAL'), 'BC-015': ('BLOG', 'INDUSTRY'), 'BC-024': ('HIGH_INTENT', 'BUYING_RESEARCH'),
 'BC-016': ('SEASONAL', 'PROPOSAL'), 'BC-017': ('FESTIVE', 'PROPOSAL'), 'BC-005': ('BLOG', 'CRAFT'),
 'BC-019': ('HIGH_INTENT', 'BLACK_FRIDAY'), 'BC-021': ('INFORMATIONAL', 'STYLE'), 'BC-039': ('INFORMATIONAL', 'RING_CULTURE'),
 'BC-022': ('BLOG', 'STYLE'), 'BC-038': ('BLOG', 'RING_CULTURE'), 'BC-023': ('INFORMATIONAL', 'ANNIVERSARY'),
 'BC-025': ('INFORMATIONAL', 'STYLE'), 'BC-031': ('SEASONAL', 'TRENDS'), 'BC-032': ('SEASONAL', 'TRENDS'),
 'BC-034': ('FESTIVE', 'VALENTINES'),
}
# Past-dated locked posts (not published; status PLANNED_NOT_BRIEFED): carried forward by user decision 2026-10-03
CARRY = {'BC-001': '2026-10-04', 'BC-018': '2026-10-07', 'BC-003': '2026-10-14'}
# Final gap-research notes attached to locked rows (keywords/dates NOT changed)
GAP_NOTES = {
 'BC-021': 'Final gap research (2026-10-03): "bracelet stacking" (14,800; Dec 2.2x; C2 AIO "How to Build a Bracelet Stack") and "how to tell if tennis bracelet is real" (1,300; BR) fit here as sections via the existing secondary "how to stack bracelets"; NOT given a separate post to avoid cannibalising this locked article. Bracelet sizing now lives in EDU-RJG-BR (Nov 13).',
 'BC-014': 'Final gap research: "how to propose to your girlfriend" (1,300; C1) and "beach proposal ideas" (1,300; C1) fit as sections here; no separate post.',
 'BC-006': 'Final gap research: necklace sizing now has its own Education owner (EDU-RJG-NL, Nov 12) - link to it for lengths instead of re-explaining.',
 'BC-007': 'Final gap research: wedding-band buying decisions now live in EDU-WB-GUIDE (Jan 11); this post keeps wearing order and "should engagement ring and wedding band match".',
 'BC-037': 'Final gap research: wedding-band style catalogue now lives in BLOG-WR-TYPES (Dec 4); this post keeps "wedding ring vs wedding band".',
 'BC-022': 'Final gap research: "ear stacking ideas" (1,300) rejected (piercing-led SERP, no AIO); wedding-band styles moved to BLOG-WR-TYPES.',
 'BC-036': 'Final gap research: BLOG-WR-HISTORY (Feb 1) answers the left-hand history question in one line and links here.',
 'BC-024': 'Final gap research: wedding-band cost questions go to BLOG-WB-BUYS (Jan 14), not here; insurance budget PAA links here from EDU-INS.',
 'BC-016': 'Final gap research: BLOG-NPD (Feb 16) links here for "most popular day to propose".',
 'BC-004': 'December refresh scheduled separately as BC-004-DEC-REFRESH (Dec 7), blocked on shipping cut-off facts.',
}

# Business-fact wording rule (confirmed_business_facts.md): bespoke timing must read "typically", never as a promise.
CTA_FIX = {
 'BC-017': ('typical bespoke 3-4 weeks', 'bespoke typically ~3-4 weeks, stone-dependent, never guaranteed'),
 'BC-034': ('typical 3-4 weeks', 'bespoke typically ~3-4 weeks, stone-dependent, never guaranteed'),
}

def week_label(d):
    n = (d - WEEK1).days // 7 + 1
    s = WEEK1 + dt.timedelta(days=7 * (n - 1)); e = s + dt.timedelta(days=6)
    return f"W{n:02d} ({s.strftime('%b %d')}-{e.strftime('%b %d')})"

def kd_band(kd):
    try: k = float(kd)
    except: return 'n/a'
    return 'LOW' if k < 15 else ('MEDIUM' if k <= 35 else 'HIGH')

def first_date(s):
    m = re.search(r'(\d{4}-\d{2}-\d{2})', s or '')
    return dt.date.fromisoformat(m.group(1)) if m else None

def lead(pub, ev):
    if not ev: return ''
    d = (ev - pub).days
    return str(d) if d >= 0 else ''

# SUPERSEDED (2026-10-03): BLOG_CALENDAR_FINAL.csv is now the single source of truth and is edited in place
# (finalize_in_place.py). Refuse to regenerate it.
if os.path.exists(OUT) and 'publishing_priority' in open(OUT, encoding='utf-8').readline():
    sys.exit('BLOG_CALENDAR_FINAL.csv is finalized; edit it in place instead of rebuilding.')

rows = []
# ---------------- locked rows
locked = [x for x in csv.DictReader(open(LOCKED_CSV)) if x['blog_id'].startswith('BC-')]
assert len(locked) == 28, len(locked)
for x in locked:
    bid = x['blog_id']; orig = x['planned_publish_date']
    pub = CARRY.get(bid, orig)
    ctype, ccat = LOCKED_TYPE[bid]
    paa_n = len([q for q in x['paa_questions'].split(' | ') if q.strip()]) if x['paa_questions'] else 0
    kd = x['keyword_difficulty']
    ev = first_date(x['event_date'])
    notes = '; '.join(v for v in [
        f"Revision status: {x['revision_status']}" + (f" (merged from {x['merged_from']})" if x['merged_from'] else ''),
        f"Low-volume justification: {x['low_volume_justification']}" if x['low_volume_justification'] else '',
        f"Business facts: {x['business_facts_required']}" if x['business_facts_required'] else '',
        f"Promote-to-Education flag: {x['promote_to_education_flag']}" if x['promote_to_education_flag'] else '',
        f"Refresh cycle: {x['refresh_cycle']}" if x['refresh_cycle'] else '',
        GAP_NOTES.get(bid, ''),
        ('CTA wording normalised to the confirmed-fact rule ("typically", never guaranteed); meaning unchanged.' if bid in CTA_FIX else ''),
        (f"CARRIED FORWARD: original locked date {orig} passed before publication (status PLANNED_NOT_BRIEFED); moved to the first open slot from 2026-10-04 by user decision (2026-10-03). No future locked date moved." if bid in CARRY else ''),
    ] if v)
    rows.append({
     'content_id': bid, 'publish_date': pub,
     'locked_date_status': 'LOCKED_CARRIED_FORWARD' if bid in CARRY else 'LOCKED_CONFIRMED',
     'original_planned_date': orig,
     'content_type': ctype, 'content_category': ccat,
     'status': 'LOCKED_CARRIED_FORWARD' if bid in CARRY else 'LOCKED_CONFIRMED',
     'working_title': x['blog_title_working'], 'primary_keyword': x['primary_keyword'],
     'primary_search_volume': x['primary_search_volume'], 'secondary_keywords': x['secondary_keywords'],
     'secondary_search_volume': x['secondary_search_volume'], 'keyword_priority': x['priority'],
     'search_intent': f"{x['search_intent']} (SERP-verified: {x['serp_intent']})",
     'commercial_intent': x['commercial_relevance'], 'keyword_difficulty': kd,
     'serp_competition': f"{kd_band(kd)} - KD {kd}; top domains: {x['serp_top5_domains']}",
     'serp_page_type': x['serp_page_types'],
     'serp_features': f"AIO {x['ai_overview']}; PAA {x['paa_present']}; AIO structure: {x['aio_structure']}",
     'ai_overview': x['ai_overview'], 'paa_present': x['paa_present'], 'paa_questions_count': str(paa_n),
     'ae_o_answer_format': x['aeo_answer_format'], 'season': x['event_or_season'], 'festival': x['festival_relevance'],
     'occasion': x['seasonal_relevance'], 'event_date': x['event_date'],
     'lead_time_days': lead(dt.date.fromisoformat(pub), ev),
     'source_stage': f"Revised Blog Calendar (hard SEO revision, 2026-10-03); keyword source: {x['keyword_source']}",
     'source_cluster': x['cluster_id'], 'existing_or_new': 'EXISTING_PLAN (locked revised calendar)',
     'HOD_relevance': x['HOD_relevance'], 'product_category': x['target_category'] + (f" / {x['target_product']}" if x['target_product'] not in ('', 'n/a') else ''),
     'target_audience': x['target_audience'], 'funnel_stage': x['funnel_stage'],
     'target_url_type': 'BLOG_POST (/blog)', 'target_owner': f"{bid} (Blog-owned; {x['blog_category']})",
     'education_or_blog': 'BLOG', 'internal_link_targets': x['internal_link_targets'],
     'CTA_direction': x['CTA_direction'].replace(*CTA_FIX[bid]) if bid in CTA_FIX else x['CTA_direction'],
     'cannibalization_status': x['cannibalization_check'],
     'why_scheduled': f"LOCKED date from the revised calendar. Lead-time logic: {x['seo_lead_time']}",
     'priority_reason': x['priority_reason'], 'notes': notes,
    })

# ---------------- new rows
for n in NEW:
    pub = dt.date.fromisoformat(n['date'])
    ev = dt.date.fromisoformat(n['event']) if n['event'] else None
    rows.append({
     'content_id': n['id'], 'publish_date': n['date'], 'locked_date_status': 'NEW_IN_OPEN_SLOT', 'original_planned_date': '',
     'content_type': n['content_type'], 'content_category': n['content_category'], 'status': n['status'],
     'working_title': n['title'], 'primary_keyword': n['pk'], 'primary_search_volume': str(n['pv']),
     'secondary_keywords': n['sk'], 'secondary_search_volume': (f"{n['sv']} ({n['sv_note']})" if n['sv'] != '' else ''),
     'keyword_priority': n['prio'], 'search_intent': n['intent'], 'commercial_intent': n['comm'], 'keyword_difficulty': n['kd'],
     'serp_competition': n['comp'], 'serp_page_type': n['page_type'], 'serp_features': n['feats'], 'ai_overview': n['aio'],
     'paa_present': n['paa'], 'paa_questions_count': n['paa_n'], 'ae_o_answer_format': n['aeo'], 'season': n['season'],
     'festival': n['festival'], 'occasion': n['occasion'], 'event_date': n['event_label'], 'lead_time_days': lead(pub, ev),
     'source_stage': n['src'], 'source_cluster': n['cluster'], 'existing_or_new': n['eon'], 'HOD_relevance': n['hod'],
     'product_category': n['product'], 'target_audience': n['audience'], 'funnel_stage': n['funnel'],
     'target_url_type': n['url_type'], 'target_owner': n['owner'], 'education_or_blog': n['eob'],
     'internal_link_targets': n['links'], 'CTA_direction': n['cta'], 'cannibalization_status': n['cann'],
     'why_scheduled': n['why'], 'priority_reason': n['prio_reason'], 'notes': n['notes'],
    })

# ---------------- unused standard slots (Mon/Tue/Thu/Fri cadence of the revised calendar)
used = {r['publish_date'] for r in rows}
old_slot_reason = {x['planned_publish_date']: x['priority_reason'] for x in csv.DictReader(open(LOCKED_CSV)) if x['blog_id'].startswith('SLOT')}
HOLIDAY = {'2026-11-26': 'Thanksgiving', '2026-11-27': 'Black Friday', '2026-12-24': 'Christmas Eve', '2026-12-25': 'Christmas Day',
           '2026-12-31': "New Year's Eve", '2027-01-01': "New Year's Day", '2027-01-18': 'Martin Luther King Jr. Day',
           '2027-02-15': "Presidents' Day"}
def unused_reason(d):
    s = d.isoformat()
    base = old_slot_reason.get(s, '')
    if s in HOLIDAY:
        return f"US holiday ({HOLIDAY[s]}): low publishing value. " + (f"Original calendar: {base}" if base else '')
    if d < dt.date(2026, 12, 1):
        return (f"Original calendar: {base} " if base else '') + 'Not needed: the week already carries the Education build-out; adding more would overload production.'
    if d <= dt.date(2026, 12, 31):
        return (f"Original calendar: {base} " if base else '') + 'Christmas / year-end week: no topic with useful timing; new evergreen content is better started in January.'
    if d < dt.date(2027, 2, 1):
        return ('January: no further topic passed the demand / SERP / ownership bar. Held candidates (not schedulable yet): '
                'EDU-4C-04 VS clarity (conditional; SERP unvalidated), EDU-LG-06 worth it (conditional), EDU-RJG-04 engagement ring buying guide (deferred, D-19), '
                'EDU-GEM-01 moissanite vs lab-grown (needs business decision), "what is gold vermeil" 12,100 (business dependency). Use for refreshes of high-traffic posts.')
    if d < dt.date(2027, 3, 1):
        return ("February: Valentine's content is already live (BC-034, Dec 8); Valentine's jewellery SERPs are product-led (routed to a commercial collection). "
                'No other validated topic. Suggested use: pre-Valentine refresh check of BC-034 and BC-017.')
    return ('March: no validated topic yet. Spring/summer wedding-band trends (BL-027) and graduation/Mother\'s Day (BL-030/BL-032) fall after this horizon or '
            'are commercial; measure them in Q1 2027 before scheduling Q2.')
d = START
while d <= END:
    if d.weekday() in (0, 1, 3, 4) and d.isoformat() not in used:
        rows.append({c: '' for c in COLS} | {
         'content_id': f"SLOT-{d.strftime('%Y%m%d')}", 'publish_date': d.isoformat(), 'locked_date_status': 'OPEN_SLOT',
         'status': 'UNUSED_SLOT', 'working_title': '(no article scheduled)', 'why_scheduled': 'Left unused deliberately (quality over filling).',
         'notes': unused_reason(d)})
    d += dt.timedelta(days=1)

# ---------------- order, day/week, sequence
rows.sort(key=lambda r: (r['publish_date'], 0 if r['status'] != 'UNUSED_SLOT' else 1, r['content_id']))
seq = 0
for r in rows:
    dd = dt.date.fromisoformat(r['publish_date'])
    r['day'] = dd.strftime('%A'); r['week'] = week_label(dd)
    if r['status'] != 'UNUSED_SLOT':
        seq += 1; r['sequence'] = str(seq)

os.makedirs(OUT_DIR, exist_ok=True)
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_MINIMAL); w.writeheader()
    for r in rows: w.writerow({c: r.get(c, '') for c in COLS})
print('written', OUT, 'rows', len(rows), 'scheduled', seq, 'unused', len(rows) - seq)
