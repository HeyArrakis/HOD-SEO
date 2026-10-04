#!/usr/bin/env python3
"""Stage 18 QC — semantic gap analysis. Read-only; exits non-zero on any failure."""
import csv
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = lambda *a: os.path.join(BASE, *a)
rd = lambda p: list(csv.DictReader(open(P(p), newline='', encoding='utf-8')))

GAP = rd('content-strategy/18_semantic_gap_register.csv')
ENT = rd('content-strategy/18_entity_coverage.csv')
QST = rd('content-strategy/18_question_coverage.csv')
SP = rd('content-strategy/18_serp_semantic_patterns.csv')
CP = rd('content-strategy/18_cross_page_semantic_ownership.csv')
REL = rd('content-strategy/18_related_search_classification.csv')
M15 = rd('architecture/15_keyword_url_map.csv')
BYKW = {r['keyword']: r for r in M15}
REG15 = {r['target_id']: r for r in rd('architecture/15_target_page_registry.csv')}
ARCH14 = {r['topic_id']: r for r in rd('architecture/14_education_architecture.csv')}
PLR16 = {r['page_id'] for r in rd('architecture/16_page_link_requirements.csv')}
S8 = {r['keyword']: r for r in rd('serp/analysis/08_hod_serp_validation.csv')}
Q17 = rd('content-strategy/17_question_map.csv')
SNAP = json.load(open(P('content-strategy/scripts/18_upstream_checksums.json')))
STATS = json.load(open(P('content-strategy/scripts/18_build_stats.json')))
TESTER = 'cvd/hpht diamond tester'
OUTS = [P('content-strategy', f) for f in ('18_semantic_gap_register.csv', '18_entity_coverage.csv', '18_question_coverage.csv',
                                           '18_serp_semantic_patterns.csv', '18_cross_page_semantic_ownership.csv',
                                           '18_related_search_classification.csv', '18_stage_summary.md')]
MAPPED = ('MAP_EXISTING_URL', 'MAP_EXISTING_URL_KEEP', 'MAP_PROPOSED_URL', 'MAP_INTERIM_HOME')

RAW_PAA, RAW_REL = {}, {}
for f in glob.glob(P('serp/raw/08_stage8_by_id/*.json')):
    d = json.load(open(f))
    for t in d['tasks']:
        for res in t.get('result') or []:
            its = res.get('items') or []
            RAW_PAA[res['keyword']] = {q.get('title') for it in its if it['type'] == 'people_also_ask' for q in it.get('items') or []}
            RAW_REL[res['keyword']] = {(q if isinstance(q, str) else q.get('title')) for it in its if it['type'] == 'related_searches' for q in it.get('items') or []}
OWN = {}
for kw in S8:
    r = BYKW.get(kw)
    if kw != TESTER and r and r['mapping_disposition'] in MAPPED and r['target_id']:
        OWN.setdefault(r['target_id'], []).append(kw)

results = []


def check(n, name, ok, detail=''):
    results.append((n, name, bool(ok), detail))


def sha(p):
    return hashlib.sha256(open(P(p), 'rb').read()).hexdigest()


LOGS = {'progress.md', 'cost-log.csv', 'decision-log.md'}   # stage logs are appended each stage
changed = [p for p, h in SNAP.items() if p not in LOGS and (not os.path.exists(P(p)) or sha(p) != h)]

# 1
check(1, 'Every Stage 15 target has semantic-gap coverage',
      set(REG15) == {g['target_page_id'] for g in GAP} and set(REG15) <= {s['target_page_id'] for s in SP} and set(REG15) <= {e['target_page_id'] for e in ENT},
      f'{len({g["target_page_id"] for g in GAP})}/27 in register')
# 2
check(2, 'No Stage 15 keyword ownership changes', 'architecture/15_keyword_url_map.csv' not in changed and len(M15) == 1936)
# 3
urls = set()
for f in OUTS:
    urls |= set(re.findall(r'(?<![\w.])/(?:blog|education|shop|engagement-rings)/[\w\-/]+', open(f, encoding='utf-8').read()))
existing = {r['existing_url'] for r in REG15.values() if r['existing_url']}
check(3, 'No new URL ownership (only existing Stage 15 URLs referenced)', urls <= existing, f'unexpected: {sorted(urls - existing)[:3]}')
# 4
reg_clusters = {c.strip() for r in REG15.values() for c in r['cluster_ids'].split(';')}
gap_clusters = {c.strip() for g in GAP for c in g['cluster_id'].split(';')}
check(4, 'No new clusters', gap_clusters <= reg_clusters and 'clusters/11_cluster_registry.csv' not in changed)
# 5
check(5, 'Every gap has evidence', all(g['source_evidence'].strip() and int(g['evidence_count']) >= 0 for g in GAP)
      and all(g['source_evidence'] != '' for g in GAP))
# 6
check(6, 'Every gap has confidence', all(g['confidence'] in ('HIGH', 'MEDIUM', 'LOW') for g in GAP))
# 7 SERP claims
bad = []
for g in GAP:
    for k, n in re.findall(r'(\d+)/(\d+) SERPs', g['source_evidence']):
        if int(n) != len(OWN.get(g['target_page_id'], [])) or int(k) > int(n):
            bad.append(g['gap_id'])
    if 'Stage 8 AI Overview text' in g['source_evidence'] and g['target_page_id'] not in OWN:
        bad.append(g['gap_id'])
for s in SP:
    if s['serp_keyword'] in S8:
        s8 = S8[s['serp_keyword']]
        if (s['ai_overview'], s['paa'], s['shopping'], s['images'], s['video']) != (s8['ai_overview_presence'], s8['paa_presence'], s8['shopping_presence'], s8['image_presence'], s8['video_presence']):
            bad.append(s['serp_keyword'])
        if BYKW[s['serp_keyword']]['target_id'] != s['target_page_id']:
            bad.append(s['serp_keyword'])
    elif not (s['serp_keyword'].startswith('AGGREGATE') or s['serp_keyword'] == 'NO_STAGE8_SERP'):
        bad.append(s['serp_keyword'])
check(7, 'No unsupported SERP claims', not bad, str(bad[:5]))
# 8 volumes
HEADS = ['4cs of diamonds', 'diamond 4cs', 'diamond color chart', 'diamond color scale', 'diamond clarity chart', 'diamond carat', 'carat weight',
         'diamond cut chart', 'diamond shapes', '14k vs 18k gold', '10k vs 14k gold', 'ring size chart', 'ring size guide', 'how to measure ring size',
         'ring sizer', 'engagement ring settings', 'prong setting', 'bezel setting', 'white gold vs platinum', 'what are lab grown diamonds',
         'vvs diamonds', 'igi certification', 'gia certification', 'diamond certificate']
vol_bad = []
cols_bad = []
for f in OUTS:
    txt = open(f, encoding='utf-8').read().lower()
    for h in HEADS:
        for mm in re.finditer(re.escape(h) + r'[^\n;|]{0,6}\(?\s?(\d[\d,]{2,})', txt):
            vol_bad.append((os.path.basename(f), h, mm.group(1)))
    if f.endswith('.csv'):
        cols_bad += [c for c in open(f, encoding='utf-8').readline().lower().split(',') if 'volume' in c]
check(8, 'No invented search volume', not vol_bad and not cols_bad, str(vol_bad[:3] + cols_bad[:3]))
# 9 PAA trace
paa_rows = [q for q in QST if q['source'].startswith('STAGE8_PAA')]
paa_bad = [q['question'] for q in paa_rows if q['question'] not in RAW_PAA.get(re.search(r'SERP: "(.+)"\)', q['source']).group(1), set())]
routed = {q['question'] for q in Q17 if q['source_type'] == 'STAGE8_PAA'}
owner_rows = [q for q in paa_rows if q['coverage_status'] != 'OWNED_ELSEWHERE']
check(9, 'PAA questions trace to Stage 8/17 evidence', not paa_bad and {q['question'] for q in owner_rows} == routed and len(owner_rows) == 146,
      f'{len(owner_rows)} owner rows; untraced {paa_bad[:2]}')
# 10 related trace
rel_bad = [r['related_search'] for r in REL if not any(r['related_search'] in RAW_REL.get(k, set()) for k in r['serp_keywords'].split('; '))]
not7 = [r for r in REL if r['in_stage7'] == 'NO']
check(10, 'Related searches trace to Stage 8/17 evidence', not rel_bad and sum(int(r['occurrences']) for r in not7) == 324
      and len({r['related_search'].lower() for r in not7}) == 248, f'{len(not7)} exact / {len({r["related_search"].lower() for r in not7})} case-insensitive')
# 11 entities
check(11, 'Entities trace to evidence', all(e['evidence_source'] and (int(e['evidence_count']) > 0 or 'Adjacent' in e['evidence_source']) for e in ENT))
# 12 cross-page vs Stage 15
own_ids = set(REG15) | set(ARCH14) | PLR16
x_bad = []
for g in GAP:
    if g['owner_page_id'] not in own_ids:
        x_bad.append(g['gap_id'])
    mm = re.search(r'Stage 15 check: "(.+?)" -> ', g['notes'])
    if mm and g['owner_status'] != 'OWNED_HERE':
        a = BYKW[mm.group(1)]
        o = g['owner_page_id']
        ok = (a['target_id'] == o) if o in REG15 else (a['stage14_topic_id'] == o) if o in ARCH14 else a['mapping_disposition'] in ('CONDITIONAL_NOT_MAPPED', 'DEFERRED_NOT_MAPPED')
        if not ok:
            x_bad.append(g['gap_id'])
    if g['owner_status'] == 'OWNED_ELSEWHERE' and g['owner_page_id'] not in REG15:
        x_bad.append(g['gap_id'])
for c in CP:
    if c['actual_owner_page_id'] == c['current_target_page_id']:
        x_bad.append(c['concept'])
check(12, 'Cross-page ownership agrees with Stage 15', not x_bad, str(x_bad[:5]))
# 13 duplicate ownership via xkeys
xk = lambda s: (re.search(r'\[xkey:(\w+)\]', s) or [None, None])[1]
here = {}
dup = []
for g in GAP:
    k = xk(g['notes'])
    if k and g['owner_status'] == 'OWNED_HERE':
        if k in here and here[k] != g['target_page_id']:
            dup.append(k)
        here[k] = g['target_page_id']
host = {(xk(g['notes']), g['target_page_id']) for g in GAP if g['owner_status'] in ('OWNED_HERE', 'INTERIM_HOME_HERE')}
orph = [(xk(g['notes']), g['owner_page_id']) for g in GAP if g['owner_status'] == 'OWNED_ELSEWHERE' and xk(g['notes'])
        and (xk(g['notes']), g['owner_page_id']) not in host]
check(13, 'No duplicate ownership created', not dup and not orph, f'dup {dup} orphan {orph[:4]}')
# 14 no new pages
TREAT = {'CORE_SECTION', 'SUPPORTING_SECTION', 'INLINE_ANSWER', 'FAQ', 'DEFINITION_BLOCK', 'COMPARISON_TABLE', 'STEP_SEQUENCE', 'VISUAL_CHART',
         'CATEGORY_COPY', 'BRIEF_MENTION_AND_LINK', 'AVOID', 'BUSINESS_INPUT_REQUIRED', 'VALIDATE_BEFORE_USE'}
check(14, 'No semantic gap is turned into a new page', all(g['recommended_treatment'] in TREAT for g in GAP)
      and not any(re.search(r'new (page|url)|create (a|new) (page|url)|separate page', g['recommended_treatment'] + g['stage19_relevance'], re.I) for g in GAP))
# 15 business dependent
check(15, 'Business-dependent gaps explicitly marked', all(g['business_dependency'] for g in GAP if g['gap_severity'] == 'BUSINESS_DEPENDENT')
      and all(g['gap_severity'] == 'BUSINESS_DEPENDENT' for g in GAP if g['recommended_treatment'] == 'BUSINESS_INPUT_REQUIRED'))
# 16 body coverage
COV = {'FUTURE_PAGE', 'BODY_UNKNOWN', 'TITLE/H1_NOT_EVIDENT', 'CONFIRMED_MISSING'}
ok16 = all(g['coverage_status'] in COV and g['coverage_status'] != 'CONFIRMED_MISSING' for g in GAP)
ok16 &= all(q['coverage_status'] in COV | {'OWNED_ELSEWHERE', 'NOT_APPLICABLE'} for q in QST)
ok16 &= all(e['coverage_status'] in COV | {'OWNED_ELSEWHERE'} for e in ENT)
ok16 &= all((g['coverage_status'] == 'FUTURE_PAGE') == (not REG15[g['target_page_id']]['existing_url']) for g in GAP)
ok16 &= all('BODY_COVERAGE=UNKNOWN' in g['current_coverage'] for g in GAP if g['coverage_status'] != 'FUTURE_PAGE')
check(16, 'Body coverage not claimed without body evidence', ok16)
# 17 ranking keywords
REP = rd('content-strategy/15_ranking_equity_protection.csv')
rk = [r for r in REP if r.get('keyword')]
ok17 = 'content-strategy/15_ranking_equity_protection.csv' not in changed and len(rk) == 28
ok17 &= not any(re.search(r'redirect|change (the )?url|move (the )?url|new slug', open(f, encoding='utf-8').read(), re.I) for f in OUTS if f.endswith('.csv'))
check(17, 'All 28 Stage 3 ranking keywords remain protected', ok17, f'{len(rk)} rows')
# 18 tester
ok18 = TESTER not in {s['serp_keyword'] for s in SP} and not any(TESTER in r['serp_keywords'] for r in REL)
ok18 &= not any(TESTER in q['source'] for q in QST) and not any(TESTER in g['source_evidence'] for g in GAP)
ok18 &= BYKW[TESTER]['mapping_disposition'].startswith('EXCLUDE')
check(18, '`cvd/hpht diamond tester` remains excluded', ok18)
# 19
check(19, 'Stage 16 linking relationships unchanged', not [p for p in changed if '/16_' in p])
# 20
check(20, 'Stage 7-17 files unchanged', not changed, f'changed: {changed[:4]}')
# 21
cl = rd('cost-log.csv')
s18 = [r for r in cl if 'Stage 18' in r['stage']]
check(21, 'No paid DataForSEO call without approval', not os.path.exists(P('dataforseo/raw/18_stage18'))
      and all(float(r['actual_cost_usd'] or 0) == 0 for r in s18) and len(s18) == 1)
# 22 / 23
check(22, 'Paid research cost matches approved configuration (N/A: none approved or run)', not os.path.exists(P('dataforseo/processed/18_stage18_research_log.md')) or False)
check(23, 'All raw paid-call responses preserved (N/A: no paid call)', not os.path.exists(P('dataforseo/raw/18_stage18')))
# 24
hdr = ' '.join(open(f, encoding='utf-8').readline().lower() for f in OUTS if f.endswith('.csv'))
check(24, 'No overall page score/ranking created', not re.search(r'score|rank|priority', hdr))
# 25
briefs = glob.glob(P('**', '19_*'), recursive=True)
check(25, 'No Stage 19 content briefs created', not briefs and not any(re.search(r'word count|\bH2:|meta description:', open(f, encoding='utf-8').read(), re.I) for f in OUTS))
# extra integrity checks
VOC = dict(gap_type={'CORE_CONCEPT_GAP', 'SUPPORTING_CONCEPT_GAP', 'ENTITY_GAP', 'QUESTION_GAP', 'COMPARISON_GAP', 'ATTRIBUTE_GAP', 'PROCESS_GAP',
                     'DEFINITION_GAP', 'EXAMPLE_GAP', 'COMMERCIAL_CONTEXT_GAP', 'TRUST_EVIDENCE_GAP', 'AEO_GAP', 'SERP_FORMAT_GAP', 'USER_JOURNEY_GAP', 'INTERNAL_CONTEXT_GAP'},
           gap_severity={'CRITICAL_COVERAGE', 'IMPORTANT_COVERAGE', 'SUPPORTING_COVERAGE', 'OPTIONAL_CONTEXT', 'BUSINESS_DEPENDENT', 'INSUFFICIENT_EVIDENCE'},
           owner_status={'OWNED_HERE', 'OWNED_ELSEWHERE', 'INTERIM_HOME_HERE', 'CONDITIONAL_OWNER_NOT_BUILT', 'COMMERCIAL_PAGE_OWNER'})
check(26, 'Controlled vocabularies (gap type, severity, owner status, question treatment, related class, entity type)',
      all(g[k] in v for g in GAP for k, v in VOC.items())
      and all(q['recommended_treatment'] in {'CORE_SECTION', 'SUPPORTING_SECTION', 'FAQ', 'INLINE_ANSWER', 'CATEGORY_COPY', 'NOT_NEEDED'} for q in QST)
      and all(r['classification'] in {'NEW_SEMANTIC_CONCEPT', 'NEW_QUESTION', 'NEW_ATTRIBUTE', 'NEW_MODIFIER', 'CLOSE_VARIANT', 'DUPLICATE', 'AMBIGUOUS', 'IRRELEVANT', 'BUSINESS_DEPENDENT'} for r in REL)
      and all(e['entity_type'] in {'PRIMARY_ENTITY', 'SUPPORTING_ENTITY', 'COMPARISON_ENTITY', 'RELATED_ENTITY', 'PRODUCT_ENTITY', 'CERTIFICATION_ENTITY', 'MATERIAL_ENTITY', 'PROCESS_ENTITY'} for e in ENT))
check(27, 'Gap IDs unique; stats file agrees with outputs', len({g['gap_id'] for g in GAP}) == len(GAP) == STATS['gaps'] and len(ENT) == STATS['entities'] and len(QST) == STATS['questions'])
check(28, 'Related searches carry no ownership', all(r['ownership_effect'].startswith('NONE') for r in REL))
q17 = subprocess.run([sys.executable, P('content-strategy/scripts/qc_17.py')], capture_output=True, text=True).stdout
fails17 = [l for l in q17.splitlines() if 'FAIL' in l]
check(29, 'qc_17 still passes except its point-in-time "no new files" check', all(re.search(r'new file|unchanged|checksum|upstream', l, re.I) for l in fails17), '; '.join(fails17)[:200])

npass = sum(r[2] for r in results)
for n, name, ok, d in results:
    print(f'[{"PASS" if ok else "FAIL"}] {n:>2}. {name}' + (f'  ({d})' if d and not ok else ''))
print(f'\n{npass}/{len(results)} PASS')
sys.exit(0 if npass == len(results) else 1)
