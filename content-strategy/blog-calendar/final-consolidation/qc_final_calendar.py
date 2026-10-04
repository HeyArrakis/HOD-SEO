"""Strict QC for FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv (prints results; writes nothing into the final folder)."""
import csv, os, re, json, hashlib, datetime as dt, collections, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
P = lambda *a: os.path.join(ROOT, *a)
FINAL_DIR = P('FINAL-BLOG-CALENDAR'); FINAL = P('FINAL-BLOG-CALENDAR', 'BLOG_CALENDAR_FINAL.csv')
rows = list(csv.DictReader(open(FINAL, encoding='utf-8')))
sched = [r for r in rows if r['status'] != 'UNUSED_SLOT']
new = [r for r in sched if r['locked_date_status'] == 'NEW_IN_OPEN_SLOT']
locked_src = [x for x in csv.DictReader(open(P('content-strategy/blog-calendar/blog_content_calendar.csv'))) if x['blog_id'].startswith('BC-')]
s15 = list(csv.DictReader(open(P('architecture/15_keyword_url_map.csv'))))
s15_owner = {x['keyword'].lower(): x['target_id'] for x in s15}
s15_disp = {x['keyword'].lower(): x['mapping_disposition'] for x in s15}
br = {x['keyword'].lower(): x for x in csv.DictReader(open(P('content-strategy/blog-calendar/blog_keyword_research.csv')))}
c1 = list(csv.DictReader(open(P('content-strategy/blog-calendar/final-consolidation/call1_processed.csv'))))
s19 = {x['target_page_id'] for x in csv.DictReader(open(P('content-strategy/19_brief_registry.csv')))}
results = []
def check(name, ok, detail=''):
    results.append((name, ok, detail)); print(('PASS ' if ok else 'FAIL ') + name + (f' :: {detail}' if detail else ''))

def kw_list(field):
    out = []
    for part in field.split(';'):
        k = part.split('(')[0].strip().strip('"').lower()
        if k and not k.startswith('s15 cluster') and not k.startswith('see ') and len(k) < 80: out.append(k)
    return out

# 1 single file
files = [f for f in os.listdir(FINAL_DIR) if not f.startswith('.')]
check('01 exactly one file in FINAL-BLOG-CALENDAR', files == ['BLOG_CALENDAR_FINAL.csv'], str(files))
# 2 no duplicate dates
c = collections.Counter(r['publish_date'] for r in rows)
check('02 no duplicate publish dates (scheduled or slot)', all(v == 1 for v in c.values()), str([k for k, v in c.items() if v > 1]))
# 3 locked future dates preserved
carry = {'BC-001', 'BC-018', 'BC-003'}
byid = {r['content_id']: r for r in sched}
bad = [x['blog_id'] for x in locked_src if x['blog_id'] not in carry and byid.get(x['blog_id'], {}).get('publish_date') != x['planned_publish_date']]
check('03 all 25 future locked dates preserved exactly', not bad and len(locked_src) == 28, str(bad))
# 4 carried-forward items
okc = all(byid[i]['original_planned_date'] < '2026-10-04' <= byid[i]['publish_date'] and byid[i]['status'] == 'LOCKED_CARRIED_FORWARD' for i in carry)
check('04 past-dated locked posts carried forward with original date preserved', okc, str({i: (byid[i]['original_planned_date'], byid[i]['publish_date']) for i in carry}))
# 5 seasonal/festive dates not moved
sf = [x for x in locked_src if x['content_type'] in ('SEASONAL', 'FESTIVAL') and x['blog_id'] not in carry]
check('05 no confirmed seasonal/festival date moved', all(byid[x['blog_id']]['publish_date'] == x['planned_publish_date'] for x in sf), f'{len(sf)} seasonal/festival rows checked')
# 6 ownership: new rows' keywords vs Stage 15 owners
viol = []
for r in new:
    owner_id = r['target_owner'].split(' ')[0]
    for k in [r['primary_keyword']] + kw_list(r['secondary_keywords']):
        o = s15_owner.get(k)
        if o and o != owner_id:
            viol.append(f"{r['content_id']}: '{k}' owned by {o}")
check('06 no Stage 15 ownership violated by new rows (primary + secondaries)', not viol, '; '.join(viol))
# 7 duplicate primary keywords
pk = collections.Counter(r['primary_keyword'].lower() for r in sched if r['content_id'] != 'BC-004-DEC-REFRESH')
check('07 no duplicate primary keyword (BC-004 December refresh is the same URL)', all(v == 1 for v in pk.values()), str([k for k, v in pk.items() if v > 1]))
# 8 new primaries not used by locked rows (primary or secondary)
locked_kws = set()
for x in locked_src:
    locked_kws.add(x['primary_keyword'].lower()); locked_kws.update(kw_list(x['secondary_keywords']))
clash = [r['content_id'] + ':' + r['primary_keyword'] for r in new if r['content_id'] != 'BC-004-DEC-REFRESH' and r['primary_keyword'].lower() in locked_kws]
check('08 no new primary keyword collides with a locked blog primary/secondary', not clash, str(clash))
clash2 = [f"{r['content_id']}:{k}" for r in new if r['content_id'] != 'BC-004-DEC-REFRESH' for k in kw_list(r['secondary_keywords']) if k in locked_kws]
check('09 no new secondary keyword collides with a locked blog keyword', not clash2, str(clash2))
# 10 cannibalization vs all 1,936 master keywords (owner must match or be unowned/held)
held_bad = [f"{r['content_id']}:{k}={s15_disp[k]}" for r in new for k in [r['primary_keyword']] + kw_list(r['secondary_keywords'])
            if k in s15_disp and s15_disp[k] in ('EXCLUDE_COMMERCIAL', 'CONDITIONAL_NOT_MAPPED', 'DEFERRED_NOT_MAPPED', 'EXCLUDE_COMPETITOR_BRAND') ]
check('10 no new row targets a Stage 15 excluded-commercial/held/deferred/competitor keyword (1,936-keyword map)', not held_bad, str(held_bad))
# 11 Stage 19 briefs: Education owners consistent
edu_ids = [r['content_id'] for r in sched if r['content_id'].startswith('EDU-') and r['content_id'] in s19]
check('11 every Stage 19 Education target is scheduled at most once and with its own owner id', len(edu_ids) == len(set(edu_ids)) and all(byid[i]['target_owner'].startswith(i) for i in edu_ids), f'{len(edu_ids)} Stage 19 targets scheduled')
# 12 sources present
check('12 all new rows have a source', all(r['source_stage'] for r in new))
# 13 intent validation for new rows
nv = [r['content_id'] for r in new if not re.search(r'validated|\(S8|\(S18\.5|C2|BC-004', r['search_intent'])]
check('13 all new rows carry SERP intent validation (S8 / S18.5 / final call 2)', not nv, str(nv))
# 14 KD + volume + AIO + PAA present
miss = [r['content_id'] for r in sched if not (r['keyword_difficulty'] and r['primary_search_volume'] and r['ai_overview'] and r['paa_present'])]
check('14 KD, volume, AIO and PAA present on every scheduled row', not miss, str(miss))
# 15 Education stays Education / Blog stays Blog
e_bad = [r['content_id'] for r in sched if (r['target_owner'].startswith('EDU-') or 'Education page' in r['target_owner']) != (r['education_or_blog'] == 'EDUCATION')]
check('15 Education-owned topics scheduled as EDUCATION and Blog topics as BLOG', not e_bad, str(e_bad))
# 16 no commercial head converted into content
comm = {k for k, x in br.items() if x['disposition'] in ('RESERVED_COMMERCIAL_PAGE', 'COMMERCIAL_PROMO_NOT_BLOG', 'REJECTED_SERP_INTENT')}
cb = [r['content_id'] + ':' + r['primary_keyword'] for r in sched if r['primary_keyword'].lower() in comm]
check('16 no scheduled primary is a reserved commercial / promo / rejected head', not cb, str(cb))
# 17 seasonal & festive timing
late = [r['content_id'] for r in sched if r['content_type'] in ('SEASONAL', 'FESTIVE', 'OCCASION') and r['lead_time_days'] != '' and int(r['lead_time_days']) < 14]
check('17 seasonal/festive/occasion items published >= 14 days before their event', not late, str(late))
xmas = [r['content_id'] for r in sched if r['content_category'] == 'CHRISTMAS' and r['status'] != 'SCHEDULED_REFRESH_BLOCKED_BUSINESS_FACT' and r['lead_time_days'] and int(r['lead_time_days']) < 45]
check('18 Christmas gift content >= 45 days ahead (refresh excepted)', not xmas, str(xmas))
# 19 Education lead time to December peak: all new Dec-peak Education pages before Dec 1
decp = [r['content_id'] for r in new if '2026-12 (' in r['event_date'] and r['education_or_blog'] == 'EDUCATION' and r['publish_date'] > '2026-12-01' and 'REFRESH' not in r['status']]
check('19 new Education pages with a December peak are published before December', not decp, str(decp))
# 20 no invented offers / guarantees
txt_fields = ['working_title', 'CTA_direction', 'ae_o_answer_format', 'why_scheduled', 'notes']
bad_claims = []
for r in sched:
    t = ' '.join(r[f] for f in txt_fields).lower()
    if re.search(r'\d+\s?% off|\bdiscount code\b|free shipping|guaranteed delivery|black friday deal|limited time offer', t): bad_claims.append(r['content_id'])
    for m in re.finditer(r'guarantee', t):
        ctx = t[max(0, m.start() - 40): m.end() + 5]
        if not re.search(r'never|not|no |without', ctx): bad_claims.append(r['content_id'] + ':guarantee')
check('20 no invented offers, discounts, shipping promises or guarantees', not bad_claims, str(bad_claims))
# 21 bespoke fact wording hedged
bf = [r['content_id'] for r in sched for f in txt_fields if re.search(r'3-4 weeks|2-3 weeks', r[f]) and not re.search(r'typically|usually|generally', r[f])]
check('21 bespoke timeline always hedged ("typically"/"usually")', not bf, str(bf))
# 22 low-volume justification
lv = [r['content_id'] for r in new if r['primary_search_volume'].isdigit() and int(r['primary_search_volume']) < 1000 and 'REFRESH' not in r['status']
      and not re.search(r'LOW-VOLUME JUSTIFICATION|S15 primary|Stage 15 primary|approved Stage 19 brief|Stage 19 brief', r['notes'] + r['priority_reason'] + r['existing_or_new'] + r['secondary_keywords'])]
lv += [r['content_id'] for r in sched if r['locked_date_status'] != 'NEW_IN_OPEN_SLOT' and int(r['primary_search_volume']) < 300 and 'Low-volume justification' not in r['notes']]
check('22 every low-volume primary has an explicit reason', not lv, str(lv))
# 23 ranking equity: Stage 3 ranking keywords not targeted by another page
rk = {x['keyword'].lower(): x['target_id'] for x in s15 if x['existing_ranking_url']}
re_bad = [f"{r['content_id']}:{k}" for r in sched for k in [r['primary_keyword']] + kw_list(r['secondary_keywords'])
          if k in rk and rk[k] and not r['target_owner'].startswith(rk[k])]
check('23 Stage 3 ranking keywords only appear on their protected owner', not re_bad, str(re_bad))
ref_ok = all(re.search(r'no (url change|move)|same url', (r['existing_or_new'] + r['notes'] + r['url_type'] if 'url_type' in r else r['existing_or_new'] + r['notes'] + r['target_url_type']).lower()) for r in sched if 'REFRESH' in r['status'])
check('24 every refresh row states same URL / no move', ref_ok)
# 25 operational start
check('25 schedule starts operationally on 2026-10-04', min(r['publish_date'] for r in sched) == '2026-10-04' and min(r['publish_date'] for r in rows) == '2026-10-04')
# 26 practicality
wk = collections.Counter(r['week'] for r in sched)
check('26 practical cadence: max 5 items per week, max 1 per day', max(wk.values()) <= 5, str(wk.most_common(3)))
# 27 required columns
req = ['publish_date', 'day', 'week', 'sequence', 'content_type', 'content_category', 'status', 'working_title', 'primary_keyword', 'primary_search_volume', 'secondary_keywords', 'secondary_search_volume', 'keyword_priority', 'search_intent', 'commercial_intent', 'keyword_difficulty', 'serp_competition', 'serp_page_type', 'serp_features', 'ai_overview', 'paa_present', 'paa_questions_count', 'ae_o_answer_format', 'season', 'festival', 'occasion', 'event_date', 'lead_time_days', 'source_stage', 'source_cluster', 'existing_or_new', 'HOD_relevance', 'product_category', 'target_audience', 'funnel_stage', 'target_url_type', 'target_owner', 'education_or_blog', 'internal_link_targets', 'CTA_direction', 'cannibalization_status', 'why_scheduled', 'priority_reason', 'notes']
check('27 all recommended columns present', all(c in rows[0] for c in req))
labels = {'EDUCATION', 'BLOG', 'INFORMATIONAL', 'HIGH_INTENT', 'SEASONAL', 'FESTIVE', 'OCCASION', 'COMMERCIAL_SUPPORT'}
check('28 content_type uses only the standard labels', all(r['content_type'] in labels for r in sched))
check('29 every unused slot carries a reason', all(r['notes'] for r in rows if r['status'] == 'UNUSED_SLOT'))
# 30 upstream Stage 1-19 files unchanged (sha256 snapshot from the blog-calendar stage)
snap = json.load(open(P('content-strategy/blog-calendar/scripts/upstream_checksums.json')))
items = snap.items() if isinstance(snap, dict) and not snap.get('files') else snap['files'].items()
changed = []
for rel, h in items:
    h = h if isinstance(h, str) else h.get('sha256')
    fp = P(rel)
    if os.path.exists(fp) and hashlib.sha256(open(fp, 'rb').read()).hexdigest() != h: changed.append(rel)
check('30 no Stage 1-19 file modified (sha256 snapshot)', not changed, f'{len(list(items))} files checked; changed={changed}')
# 31 revised calendar itself untouched in this task
mt = dt.datetime.fromtimestamp(os.path.getmtime(P('content-strategy/blog-calendar/blog_content_calendar.csv')))
check('31 revised calendar file not modified by this task', mt < dt.datetime(2026, 10, 3, 16, 30), str(mt))
# 32-36 finalization pass
PP = {'MUST_PUBLISH', 'HIGH', 'NORMAL', 'FLEXIBLE'}; PS = {'READY_TO_WRITE', 'OWNERSHIP_CONFIRMATION', 'BUSINESS_FACT_REQUIRED', 'BACKLOG'}
check('32 every scheduled row has a valid publishing_priority and production_status',
      all(r['publishing_priority'] in PP and r['production_status'] in PS for r in sched))
check('33 unused slots remain unused (BACKLOG, no title/keyword)',
      all(r['production_status'] == 'BACKLOG' and not r['primary_keyword'] and r['working_title'] == '(no article scheduled)' for r in rows if r['status'] == 'UNUSED_SLOT'))
own_req = {'EDU-RJG-NL', 'EDU-RJG-BR', 'EDU-INS', 'EDU-WB-GUIDE', 'EDU-LG-09', 'EDU-RJG-03', 'BLOG-WR-TYPES'}
check('34 unresolved-ownership topics flagged OWNERSHIP_CONFIRMATION', all(byid[i]['production_status'] == 'OWNERSHIP_CONFIRMATION' for i in own_req))
check('35 shipping cut-off refresh flagged BUSINESS_FACT_REQUIRED', byid['BC-004-DEC-REFRESH']['production_status'] == 'BUSINESS_FACT_REQUIRED')
pre = os.environ.get('PRE_FINALIZE')
if pre and os.path.exists(pre):
    old = {r['content_id']: r for r in csv.DictReader(open(pre, encoding='utf-8'))}
    diffs = [f"{r['content_id']}.{c}" for r in rows for c in old[r['content_id']] if c != 'notes' and r[c] != old[r['content_id']][c]]
    diffs += [r['content_id'] + '.notes' for r in rows if not r['notes'].startswith(old[r['content_id']]['notes'])]
    check('36 finalization changed nothing except the two new columns and appended production notes', not diffs and set(old) == {r['content_id'] for r in rows}, str(diffs[:10]))
# stats
targeted = set()
for r in sched:
    targeted.add(r['primary_keyword'].lower()); targeted.update(kw_list(r['secondary_keywords']))
inuse = lambda k: k.lower() in targeted
measured = [x for x in c1 if x['search_volume'] not in ('NOT_IN_DATAFORSEO_DB', '', 'None')]
used = [x['keyword'] for x in measured if inuse(x['keyword'])]
hv_rej = [(x['keyword'], x['search_volume']) for x in measured if int(x['search_volume']) >= 5000 and not inuse(x['keyword'])]
print('measured but not targeted:', [(x['keyword'], x['search_volume']) for x in measured if not inuse(x['keyword']) and int(x['search_volume']) >= 1000])
print('\nSTATS scheduled', len(sched), 'unused', len(rows) - len(sched), 'new', len(new))
print('content_type', collections.Counter(r['content_type'] for r in sched))
print('education_or_blog', collections.Counter(r['education_or_blog'] for r in sched))
print('status', collections.Counter(r['status'] for r in sched))
print('publishing_priority', collections.Counter(r['publishing_priority'] for r in sched))
print('production_status', collections.Counter(r['production_status'] for r in rows))
print('call1 measured', len(measured), 'used in calendar', len(used))
print('high-volume (>=5,000) measured but not used:', hv_rej)
print('\nQC:', sum(1 for _, ok, _ in results if ok), '/', len(results), 'pass')
sys.exit(0 if all(ok for _, ok, _ in results) else 1)
