"""Blog Content Calendar - HARD REVISION QC (28 checks, matching the revision brief's Final Hard QA list).
Run: python3 content-strategy/blog-calendar/blog_calendar_qc.py      Exit code 0 = all checks pass.
"""
import csv, json, os, re, sys, hashlib, datetime as dt, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
P = lambda *a: os.path.join(ROOT, *a)
H = lambda *a: os.path.join(HERE, *a)

RAW_TEXT = open(H('blog_content_calendar.csv'), encoding='utf-8').read()
ALL = list(csv.DictReader(open(H('blog_content_calendar.csv'), encoding='utf-8')))
CAL = [r for r in ALL if r['content_status'] != 'UNUSED_SLOT']
SLOTS = [r for r in ALL if r['content_status'] == 'UNUSED_SLOT']
BACK = list(csv.DictReader(open(H('blog_topic_backlog.csv'))))
KWR = list(csv.DictReader(open(H('blog_keyword_research.csv'))))
REVLOG = list(csv.DictReader(open(H('blog_calendar_revision_log.csv'))))
OPP = list(csv.DictReader(open(H('revision', 'blog_high_volume_opportunity_table.csv'))))
OVERLAP = list(csv.DictReader(open(H('revision', 'round2_serp_overlap.csv'))))
R1 = {r['keyword']: r for r in csv.DictReader(open(H('revision', 'round1_merged_raw_keywords.csv')))}
S15 = {r['normalized_keyword']: r for r in csv.DictReader(open(P('architecture/15_keyword_url_map.csv')))}
TARGETS = {r['target_id'] for r in csv.DictReader(open(P('architecture/15_target_page_registry.csv')))}
PAGES16 = {r['page_id'] for r in csv.DictReader(open(P('architecture/16_page_link_requirements.csv')))}
B19 = list(csv.DictReader(open(P('content-strategy/19_content_boundaries.csv'))))

START, END = dt.date(2026, 9, 29), dt.date(2026, 12, 31)
CHRISTMAS, BLACK_FRIDAY, VDAY = dt.date(2026, 12, 25), dt.date(2026, 11, 27), dt.date(2027, 2, 14)
INTENTS = {'INFORMATIONAL', 'COMMERCIAL_RESEARCH', 'TRANSACTIONAL', 'NAVIGATIONAL', 'MIXED'}
ORIGINAL_34 = [f'BC-{i:03d}' for i in range(1, 35)]
NEW_IDS = ['BC-035', 'BC-036', 'BC-037', 'BC-038', 'BC-039']
REMOVED_OR_MERGED = ['BC-002', 'BC-010', 'BC-012', 'BC-013', 'BC-020', 'BC-026', 'BC-027', 'BC-028', 'BC-029', 'BC-030', 'BC-033']
TEMPLATE_REQUIRED = {'BLOG-GIFTS': ['BLOG-HUB', 'COM-FJ-BRACELETS', 'COM-FJ-EARRINGS', 'COM-FJ-NECKLACES'], 'BLOG-CRAFT': ['BLOG-HUB', 'COM-BESPOKE'],
                     'BLOG-STYLE': ['BLOG-HUB'], 'BLOG-INDUSTRY': ['BLOG-HUB', 'EDU-LG-00', 'EDU-LG-05'], 'BLOG-LAUNCH': ['BLOG-HUB', 'COM-ER', 'COM-FJ', 'COM-PDP']}

# Reviewed near-match pairs (blog keyword ~ Stage 15 owned keyword). Row must also say BOUNDARY.
DOCUMENTED_BOUNDARIES = {
    ('how diamonds are cut', 'can you cut diamonds'): 'Cutting PROCESS vs EDU-GEN-01 hardness.',
    ('how diamonds are cut', 'can water cut diamonds'): 'Same boundary (EDU-GEN-01).',
    ('how diamonds are cut', 'will lab grown diamonds cut glass'): 'Same boundary (EDU-GEN-01).',
    ('where are lab grown diamonds made', 'lab grown diamonds made'): 'WHERE vs EDU-LG-00 HOW.',
    ('how is a diamond ring made', 'how diamond made'): 'Jewellery manufacture (BC-001) vs EDU-NAT-00 natural formation.',
    ('where are lab grown diamonds made', 'how are diamonds made'): 'Geography vs EDU-NAT-00 formation.',
    ('where are lab grown diamonds made', 'what are diamonds made of'): 'Geography vs EDU-GEN-01 composition.',
}
# Intentional blog-to-blog pairs (similar wording, different SERPs: <3 shared top-10 URLs in Round 2).
DOCUMENTED_BLOG_PAIRS = {
    frozenset({'BC-036', 'BC-039'}): 'Wedding-ring finger vs promise-ring finger: separate SERPs.',
    frozenset({'BC-036', 'BC-038'}): 'Which finger (wedding) vs what each finger means: separate SERPs.',
    frozenset({'BC-038', 'BC-039'}): 'General finger meanings vs promise-ring placement.',
    frozenset({'BC-011', 'BC-039'}): 'Promise ring meaning vs promise ring finger: <2 shared URLs.',
    frozenset({'BC-007', 'BC-036'}): 'Wear ORDER vs which finger/hand: <2 shared URLs.',
    frozenset({'BC-018', 'BC-035'}): 'By-year hub vs 10th spoke: <2 shared URLs.',
    frozenset({'BC-031', 'BC-032'}): 'Engagement ring trends vs fine jewellery trends.',
    frozenset({'BC-014', 'BC-017'}): 'Proposal hub vs holiday spoke.', frozenset({'BC-014', 'BC-034'}): "Proposal hub vs Valentine's spoke.",
    frozenset({'BC-017', 'BC-034'}): 'Different events.', frozenset({'BC-007', 'BC-037'}): 'Wear order vs difference between ring types.',
    frozenset({'BC-036', 'BC-037'}): 'Which finger vs difference between rings.',
}
STOP = {'a', 'an', 'the', 'is', 'are', 'of', 'to', 'for', 'and', 'on', 'in', 'do', 'does', 'how', 'what', 'vs', 'your', 'can', 'you', 'it', 'be', 'i', 'my', 'her', 'go', 'which'}
GENERIC = {'lab', 'grown', 'diamond', 'diamonds', 'created', 'jewelry', 'jewellery', 'ring', 'rings', 'engagement'}
def toks(s): return {t for t in re.findall(r'[a-z0-9]+', s.lower()) if t not in STOP}
def jacc(a, b):
    A, B = toks(a), toks(b); return len(A & B) / len(A | B) if A and B else 0
def near(a, b):
    A, B = toks(a), toks(b)
    if not A or not B or not (A & B) - GENERIC: return False
    small, big = (A, B) if len(A) <= len(B) else (B, A)
    return jacc(a, b) >= 0.75 or (len(small) >= 2 and small <= big and bool(small - GENERIC))
def kws(r):
    return [r['primary_keyword']] + [m.strip() for m in re.findall(r'(?:^|; )([^;()]+?) \([^)]*\)', r['secondary_keywords'])]
def n(x):
    try: return int(float(x))
    except (TypeError, ValueError): return None

results = []
def check(i, name, ok, detail=''): results.append((i, name, bool(ok), detail))
ids = {r['blog_id'] for r in CAL}
by_id = {r['blog_id']: r for r in CAL}

# 1
prim = [r['primary_keyword'] for r in CAL]
check(1, 'No duplicate primary keywords', len(prim) == len(set(prim)), f'{len(prim)} primaries')

# 2 duplicate intent disguised by wording: same DataForSEO demand group, or >=3 shared top-10 URLs between scheduled primaries
grp = {}
dup_grp = []
for r in CAL:
    g = R1.get(r['primary_keyword'], {}).get('demand_group')
    if g:
        if g in grp: dup_grp.append((grp[g], r['blog_id']))
        grp[g] = r['blog_id']
pk2id = {r['primary_keyword']: r['blog_id'] for r in CAL}
dup_serp = [(o['keyword_a'], o['keyword_b'], o['shared_top10_urls']) for o in OVERLAP
            if o['keyword_a'] in pk2id and o['keyword_b'] in pk2id and int(o['shared_top10_urls']) >= 3]
check(2, 'No duplicate search intent disguised by wording (same demand group or >=3 shared top-10 URLs between primaries)', not dup_grp and not dup_serp, f'{dup_grp} {dup_serp}')

# 3 Stage 15 ownership
conf = []
for r in CAL:
    for k in kws(r):
        s = S15.get(k)
        if not s: continue
        if s['target_id']: conf.append((r['blog_id'], k, 'owned by ' + s['target_id']))
        elif s['mapping_disposition'].startswith('EXCLUDE'): conf.append((r['blog_id'], k, s['mapping_disposition']))
        elif s['mapping_disposition'] in ('DEFERRED_NOT_MAPPED', 'CONDITIONAL_NOT_MAPPED', 'REVIEW_REQUIRED') and 'Blog' not in s['reason']:
            conf.append((r['blog_id'], k, s['mapping_disposition'] + ' (not assigned to Blog)'))
check(3, 'No Stage 15 ownership conflict (exact match against all 1,936 keywords)', not conf, str(conf[:5]))

# 4 Stage 19 boundaries
avoid = [b['concept'].lower() for b in B19 if b['ownership_status'] == 'EXCLUDED_AVOID']
b19 = [(r['blog_id'], k) for r in CAL for k in kws(r) if 'tester' in k or any(k in c for c in avoid)]
check(4, 'No Stage 19 boundary conflict (EXCLUDED_AVOID concepts, cvd/hpht tester)', not b19, str(b19))

# 5 blog-to-blog cannibalization
seen, dup_kw = {}, []
for r in CAL:
    for k in kws(r):
        if k in seen and seen[k] != r['blog_id']: dup_kw.append((k, seen[k], r['blog_id']))
        seen.setdefault(k, r['blog_id'])
pp = [(a['blog_id'], b['blog_id']) for i, a in enumerate(CAL) for b in CAL[i + 1:]
      if near(a['primary_keyword'], b['primary_keyword']) and frozenset({a['blog_id'], b['blog_id']}) not in DOCUMENTED_BLOG_PAIRS]
check(5, 'No blog-to-blog cannibalization (no keyword in two blogs; near-match primaries only where SERP-documented)', not dup_kw and not pp, f'{dup_kw[:4]} {pp[:4]}')

# 6 blog vs Education
owned = [k for k, s in S15.items() if s['target_id']]
undoc = []
for r in CAL:
    for k in kws(r):
        for o in owned:
            if near(k, o) and (k, o) not in DOCUMENTED_BOUNDARIES: undoc.append((r['blog_id'], k, o, S15[o]['target_id']))
            if (k, o) in DOCUMENTED_BOUNDARIES and 'BOUNDARY' not in r['cannibalization_check']: undoc.append((r['blog_id'], k, o, 'BOUNDARY missing'))
bc24 = by_id.get('BC-024', {})
check(6, 'No blog-vs-Education cannibalization (near-matches documented; BC-024 user decision recorded; EDU-RJG-04 unchanged)',
      not undoc and 'USER DECISION' in bc24.get('cannibalization_check', '') and 'UNCHANGED' in bc24.get('cannibalization_check', ''), str(undoc[:4]))

# 7 evidence
noev = [r['blog_id'] for r in CAL if n(r['primary_search_volume']) is None or r['serp_intent'] == 'NOT_SERP_CHECKED']
check(7, 'Every primary keyword has evidence (measured volume AND a Round 2 SERP)', not noev, str(noev))

# 8 low-volume justification
lowv = [r['blog_id'] for r in CAL if (n(r['primary_search_volume']) or 0) < 300 and len(r['low_volume_justification']) < 60]
check(8, 'Low-volume primaries (<300/mo) carry a documented justification', not lowv, f"{sum(1 for r in CAL if (n(r['primary_search_volume']) or 0) < 300)} low-volume; missing {lowv}")

# 9 high-volume reviewed
unrev = [o['keyword'] for o in OPP if o['recommended_action'] == 'DISCOVERED_NOT_PRIORITISED']
kw_unrev = [r['keyword'] for r in KWR if r['disposition'] == 'DISCOVERED_NOT_PRIORITISED' and (n(r['search_volume']) or 0) >= 5000
            and not any(o['keyword'] == r['keyword'] or o['demand_group'] == r['candidate_group'].split(' / ')[0] for o in OPP)]
check(9, 'High-volume opportunities reviewed (every relevant demand group >=5,000/mo has a written decision)', len(OPP) > 0 and not unrev and not kw_unrev, f'{len(OPP)} rows; {unrev[:3]} {kw_unrev[:3]}')

# 10 PAA
nopaa = [r['blog_id'] for r in CAL if r['paa_present'] != 'YES' or r['paa_questions'].count('[') < 3]
check(10, 'PAA captured for every scheduled blog (>=3 questions, each with a placement)', not nopaa, str(nopaa))

# 11 AIO
noaio = [r['blog_id'] for r in CAL if r['ai_overview'] not in ('PRESENT', 'ABSENT') or (r['ai_overview'] == 'PRESENT' and not r['aio_structure']) or len(r['aeo_answer_format']) < 30]
check(11, 'AI Overview captured (present/absent + structure) and an AEO answer format for every blog', not noaio, f"{sum(r['ai_overview'] == 'PRESENT' for r in CAL)}/{len(CAL)} AIO; {noaio}")

# 12 intent verified
badi = [r['blog_id'] for r in CAL if r['search_intent'] not in INTENTS or r['serp_intent'] in ('', 'NOT_SERP_CHECKED')]
check(12, 'Search intent stated and verified against the live SERP', not badi, str(badi))

# 13 SERP type verified; product-led primaries only with an explicit commercial-lean flag
badt = [r['blog_id'] for r in CAL if not r['serp_page_types']]
trans = [r['blog_id'] for r in CAL if r['serp_intent'].startswith('TRANSACTIONAL') and 'commercial-lean' not in r['revision_status']]
check(13, 'SERP page types recorded; no product-led primary without an explicit commercial-lean flag', not badt and not trans, f'{badt} {trans}')

# 14 seasonal timing
bad14 = []
for r in CAL:
    if r['content_type'] in ('SEASONAL', 'FESTIVAL'):
        if not r['event_or_season'] or r['event_date'] in ('', 'n/a'): bad14.append((r['blog_id'], 'no event')); continue
        d = dt.date.fromisoformat(r['planned_publish_date'])
        try: pb = dt.date.fromisoformat(r['publish_by_date'][:10])
        except ValueError: bad14.append((r['blog_id'], 'no publish_by')); continue
        if d > pb: bad14.append((r['blog_id'], 'after publish_by'))
        m = re.match(r'(\d{4}-\d{2}-\d{2})', r['event_date'])
        if m and dt.date.fromisoformat(m.group(1)) <= d: bad14.append((r['blog_id'], 'on/after event'))
check(14, 'Seasonal/festival timing valid (event recorded; planned before publish_by and before the event)', not bad14, str(bad14))

# 15 lead time + cadence
dates = [dt.date.fromisoformat(r['planned_publish_date']) for r in CAL]
pw = {}
for r in CAL: pw[r['week'][:3]] = pw.get(r['week'][:3], 0) + 1
check(15, 'Lead time recorded for every blog; all dates in window; cadence <= 4/week; unused slots explained',
      all(len(r['seo_lead_time']) > 10 for r in CAL) and all(START <= d <= END for d in dates) and max(pw.values()) <= 4 and all(s['priority_reason'] for s in SLOTS),
      f'{len(CAL)} scheduled, {len(SLOTS)} unused, max/week {max(pw.values())}')

# 16 Christmas
bad16 = []
for r in CAL:
    if 'Christmas' in r['festival_relevance'] and r['content_type'] in ('SEASONAL', 'FESTIVAL'):
        gap = (CHRISTMAS - dt.date.fromisoformat(r['planned_publish_date'])).days
        need = 45 if r['blog_category'] == 'BLOG-GIFTS' else 28
        if gap < need: bad16.append((r['blog_id'], gap, need))
check(16, 'Christmas timing valid (gift posts >=45 days, others >=28 days before Dec 25)', not bad16, str(bad16))

# 17 Valentine
vd = [r for r in CAL if r['event_date'].startswith('2027-02-14')]
check(17, "Valentine's timing valid (1-2 posts, Dec 1 or later, >=6 weeks before Feb 14)",
      1 <= len(vd) <= 2 and all(dt.date(2026, 12, 1) <= dt.date.fromisoformat(r['planned_publish_date']) <= VDAY - dt.timedelta(days=42) for r in vd), f'{len(vd)} post(s)')

# 18 Black Friday
bf = [r for r in CAL if 'Black Friday' in r['event_or_season'] or 'Black Friday' in r['festival_relevance']]
check(18, 'Black Friday timing valid (>=21 days before Nov 27)', bf and all((BLACK_FRIDAY - dt.date.fromisoformat(r['planned_publish_date'])).days >= 21 for r in bf), f'{len(bf)} post(s)')

# 19 internal links
bad19 = []
for r in CAL:
    links = [x.strip() for x in r['internal_link_targets'].split(';') if x.strip()]
    for l in links:
        if l not in PAGES16 and l not in ids: bad19.append((r['blog_id'], 'unknown ' + l))
    for req in TEMPLATE_REQUIRED[r['blog_category']]:
        if req not in links: bad19.append((r['blog_id'], 'missing ' + req))
    for x in r['related_articles'].split(';'):
        if x.strip() and x.strip() not in ids: bad19.append((r['blog_id'], 'related ' + x.strip()))
    if r['related_target_page_id'] and r['related_target_page_id'] not in TARGETS: bad19.append((r['blog_id'], r['related_target_page_id']))
check(19, 'Internal links valid (Stage 16 page IDs or scheduled blogs; template-REQUIRED links; related IDs exist)', not bad19, str(bad19[:6]))

# 20-22
check(20, 'CTA direction exists for every blog', all(len(r['CTA_direction']) > 5 for r in CAL))
check(21, 'HOD relevance stated and not LOW', all(r['HOD_relevance'] and not r['HOD_relevance'].upper().startswith('LOW') for r in CAL))
check(22, 'Commercial connection: commercial relevance + target category (or NO_DIRECT_COMMERCIAL_CONNECTION)',
      all(r['commercial_relevance'] and (r['target_category'] or 'NO_DIRECT_COMMERCIAL_CONNECTION' in r['commercial_relevance']) for r in CAL))

# 23 new research separated
bad23 = []
for r in KWR:
    if r['data_source'] == 'NEW_RESEARCH' and r['keyword'] in S15 and r['research_round'] != 'R0_seasonal_keyword_overview': bad23.append(('NEW in master', r['keyword']))
    if r['data_source'] == 'EXISTING_DATA' and r['keyword'] not in S15: bad23.append(('EXISTING not in master', r['keyword']))
    if not r['research_round']: bad23.append(('no round', r['keyword']))
for r in CAL:
    for k in kws(r):
        exp = 'EXISTING_DATA' if k in S15 else 'NEW_RESEARCH'
        if exp not in r['keyword_source']: bad23.append(('calendar source', r['blog_id'], k))
check(23, 'New research clearly separated (data_source + research_round; calendar sources consistent)', not bad23, str(bad23[:5]))

# 24 credentials
leak = []
for dp, dn, fn in os.walk(HERE):
    for f in fn:
        if f.endswith(('.csv', '.md', '.py', '.json')):
            if re.search(r'(?i)(password|api[_-]?key|authorization: basic)\s*[:=]', open(os.path.join(dp, f), errors='ignore').read()): leak.append(f)
check(24, 'No credentials leaked in stage outputs', not leak, str(leak))

# 25 upstream untouched
snap = json.load(open(H('scripts', 'upstream_checksums.json')))
changed = [p for p, v in snap.items() if not os.path.exists(P(p)) or hashlib.sha256(open(P(p), 'rb').read()).hexdigest() != v['sha256']]
check(25, 'Stage 1-19 files untouched (sha256 snapshot)', not changed, f'{len(snap)} files; changed {changed[:3]}')

# 26 costs
log = list(csv.DictReader(open(P('cost-log.csv'))))
def logged(stage_sub): return [r for r in log if stage_sub in r['stage']]
raw_cost = lambda f: json.load(open(P(f)))['cost']
r0 = raw_cost('dataforseo/raw/blog_calendar/01_keyword_overview_raw.json')
r1 = sum(json.load(open(f))['cost'] for f in glob.glob(P('dataforseo/raw/blog_calendar/revision/R1_*.json')))
r2 = json.load(open(P('dataforseo/raw/blog_calendar/revision/R2_serp/task_post_response.json')))['cost']
r3 = raw_cost('dataforseo/raw/blog_calendar/revision/R3_keyword_overview_raw.json')
logged_rev = sum(float(r['actual_cost_usd']) for r in logged('HARD REVISION'))
ok26 = (abs(r0 - 0.04404) < 1e-9 and len(logged('Round 1 discovery')) == 8 and abs(r1 - 0.54108) < 1e-6 and abs(r2 - 0.0972) < 1e-9 and abs(r3 - 0.02388) < 1e-9
        and abs(logged_rev - (r1 + r2 + r3)) < 1e-6 and logged_rev <= 4.0)
check(26, 'DataForSEO costs recorded correctly (raw responses = cost-log; revision total <= $4)', ok26, f'R0 {r0} | R1 {round(r1, 5)} | R2 {r2} | R3 {r3} | revision logged {round(logged_rev, 5)}')

# 27 calendar opens cleanly
hdr = ALL[0].keys() if ALL else []
ok27 = (RAW_TEXT.count('�') == 0 and len({r['blog_id'] for r in ALL}) == len(ALL) and all(len(r) == len(hdr) for r in ALL)
        and min(dt.date.fromisoformat(r['planned_publish_date']) for r in ALL) == START and max(dt.date.fromisoformat(r['planned_publish_date']) for r in ALL) == END
        and len({r['week'][:3] for r in ALL}) == 14 and not os.path.exists(H('blog_content_calendar_v2.csv')))
check(27, 'Final calendar opens cleanly (UTF-8, consistent columns, unique IDs, Sep 29-Dec 31, 14 weeks, no competing calendar file)', ok27, f'{len(ALL)} rows')

# 28 supporting files agree
stats = json.load(open(H('scripts', 'build_stats.json')))
summ = open(H('blog_calendar_summary.md')).read()
dlog = open(H('blog_calendar_decision_log.md')).read()
rev_ids = {r['blog_id'] for r in REVLOG}
kw_prim = {r['keyword'] for r in KWR if r['disposition'] == 'PRIMARY'}
back_removed = sum(1 for b in BACK if b['decision_code'] in ('REMOVED_IN_REVISION', 'ROUTE_TO_COMMERCIAL'))
ok28 = (set(ORIGINAL_34 + NEW_IDS) <= rev_ids and not (set(REMOVED_OR_MERGED) & ids) and set(NEW_IDS) <= ids
        and kw_prim == set(prim) and stats['scheduled'] == len(CAL) and back_removed >= 8
        and f"{len(CAL)} scheduled" in summ and 'HARD REVISION' in dlog)
check(28, 'Supporting files agree with the calendar (revision log, backlog, keyword research, stats, summary, decision log)', ok28,
      f'revlog {len(rev_ids)}; kw primaries {len(kw_prim)}; backlog removed rows {back_removed}')

fails = 0
for i, name, ok, detail in results:
    fails += not ok
    print(f"{i:>2}. {'PASS' if ok else 'FAIL'}  {name}" + (f'  [{detail}]' if detail and not ok else (f'  ({detail})' if detail else '')))
print(f"\n{len(results) - fails}/{len(results)} checks pass")
sys.exit(1 if fails else 0)
