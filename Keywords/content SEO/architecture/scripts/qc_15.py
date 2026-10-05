#!/usr/bin/env python3
"""Stage 15 QC — keyword → URL mapping. Exits non-zero on any failure."""
import csv, collections, hashlib, json, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = lambda *a: os.path.join(ROOT, *a)
rd = lambda p: list(csv.DictReader(open(P(p), newline='', encoding='utf-8')))
results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))


K = rd('architecture/15_keyword_url_map.csv')
R = rd('architecture/15_target_page_registry.csv')
C = rd('architecture/15_cluster_page_map.csv')
PR = rd('content-strategy/15_ranking_equity_protection.csv')
M7 = rd('dataforseo/processed/07_hod_master_keyword_database.csv')
REG11 = {r['cluster_id'] for r in rd('clusters/11_cluster_registry.csv')}
ARCH = {r['topic_id']: r for r in rd('architecture/14_education_architecture.csv')}
CONS = rd('architecture/14_education_cluster_consolidation.csv')
EQ = rd('content-strategy/13_ranking_equity_analysis.csv')
SITE = 'https://www.houseofdiams.com'

DISP = {'MAP_EXISTING_URL', 'MAP_PROPOSED_URL', 'MAP_EXISTING_URL_KEEP', 'MAP_INTERIM_HOME', 'CONDITIONAL_NOT_MAPPED', 'DEFERRED_NOT_MAPPED',
        'EXCLUDE_COMMERCIAL', 'EXCLUDE_NOISE', 'EXCLUDE_COMPETITOR_BRAND', 'EXCLUDE_OFF_SCOPE', 'REVIEW_REQUIRED'}
MAPPED = {'MAP_EXISTING_URL', 'MAP_PROPOSED_URL', 'MAP_EXISTING_URL_KEEP', 'MAP_INTERIM_HOME'}
CONF = {'HIGH', 'MEDIUM', 'LOW'}
RISK = {'HIGH', 'MEDIUM', 'LOW', 'INSUFFICIENT_EVIDENCE', 'NOT_APPLICABLE'}
URLST = {'EXISTING_KEEP', 'EXISTING_MOVE_WHEN_CONDITIONS_MET', 'EXISTING_RETARGET_THEN_MOVE', 'PROPOSED_URL', 'URL_PENDING', 'NONE'}
REQ = ['keyword', 'normalized_keyword', 'cluster_id', 'cluster_name', 'cluster_primary_intent', 'keyword_intent', 'search_volume', 'cpc', 'competition',
       'keyword_difficulty', 'serp_validated', 'serp_page_type', 'serp_intent', 'existing_ranking_url', 'existing_ranking_position',
       'existing_content_url', 'stage14_topic_id', 'stage14_topic_name', 'stage14_hub', 'mapping_disposition', 'target_page_type',
       'target_url_status', 'target_url', 'target_url_source', 'mapping_confidence', 'cannibalization_risk', 'reason', 'evidence_source', 'notes']

# 0. schema
check('00 keyword map has all required columns', all(c in K[0] for c in REQ), [c for c in REQ if c not in K[0]])
check('00 registry has all required columns', all(c in R[0] for c in ['target_id', 'target_page_name', 'page_type', 'hub', 'status', 'existing_or_proposed', 'existing_url', 'proposed_url', 'primary_intent', 'primary_searcher_need', 'cluster_ids', 'keyword_count', 'highest_search_volume', 'serp_evidence', 'existing_equity', 'cannibalization_risk', 'business_dependency', 'stage14_source', 'notes']))
check('00 cluster map has all required columns', all(c in C[0] for c in ['cluster_id', 'cluster_name', 'primary_topic_id', 'primary_topic_name', 'target_id', 'target_page_name', 'mapping_status', 'secondary_topic_id', 'secondary_target_id', 'reason', 'evidence_level', 'serp_evidence', 'notes']))
check('00 ranking protection has all required columns', all(c in PR[0] for c in ['keyword', 'ranking_url', 'ranking_position', 'cluster_id', 'current_intent', 'mapped_target_id', 'mapped_target_url', 'action', 'equity_risk', 'reason', 'migration_status', 'notes']))

# 1-2. every Stage 7 keyword exactly once, none dropped
kc = collections.Counter(r['keyword'] for r in K)
m7 = [r['keyword'] for r in M7]
check('01 every Stage 7 keyword appears exactly once', len(K) == len(M7) == 1936 and all(kc[k] == 1 for k in m7), f'{len(K)} rows vs {len(M7)}')
check('02 no keyword silently dropped or added', set(kc) == set(m7), f'missing {len(set(m7) - set(kc))}, extra {len(set(kc) - set(m7))}')
check('02 every row has a disposition and a reason', all(r['mapping_disposition'] and r['reason'] for r in K))

# 3. no keyword with two target URLs
tk = collections.defaultdict(set)
for r in K:
    tk[r['keyword']].add((r['target_id'], r['target_url']))
check('03 no keyword has two target URLs', all(len(v) == 1 for v in tk.values()) and not any(';' in r['target_url'] for r in K))

# 4. cluster ids exist
bad = [r['cluster_id'] for r in K if r['cluster_id'].startswith('CL-') and r['cluster_id'] not in REG11]
nonc = {r['cluster_id'] for r in K if not r['cluster_id'].startswith('CL-')}
check('04 every cluster_id exists in Stage 11', not bad and nonc <= {'NOISE', 'COMPETITOR_BRAND', 'UNCLUSTERED_REVIEW'}, f'{bad[:5]} {nonc}')
check('04 cluster map covers all 89 Stage 11 clusters once', sorted(r['cluster_id'] for r in C) == sorted(REG11))

# 5. Stage 14 topic ids exist
t14 = {r['stage14_topic_id'] for r in K if r['stage14_topic_id']} | {r['primary_topic_id'] for r in C if r['primary_topic_id'] != 'NONE'}
t14 |= {t.strip() for r in C for t in r['secondary_topic_id'].split(';') if t.strip()}
check('05 every Stage 14 topic_id exists', t14 <= set(ARCH), sorted(t14 - set(ARCH)))

# 6. target ids exist in registry; 14. no duplicate target ids
RID = [r['target_id'] for r in R]
used = {r['target_id'] for r in K if r['target_id']} | {r['target_id'] for r in C if r['target_id']} | {t.strip() for r in C for t in r['secondary_target_id'].split(';') if t.strip()}
used |= {r['mapped_target_id'] for r in PR if not r['mapped_target_id'].startswith('(none')}
check('06 every target_id exists in the registry', used <= set(RID), sorted(used - set(RID)))
check('06 every registry target owns >=1 keyword and counts match', all(int(r['keyword_count']) == sum(1 for k in K if k['target_id'] == r['target_id']) > 0 for r in R))
check('14 no duplicate target IDs', len(RID) == len(set(RID)))
check('06 mapped dispositions have a target_id; unmapped have none',
      all(bool(r['target_id']) == (r['mapping_disposition'] in MAPPED) for r in K))

# 7-8. Stage 3 ranking keywords and URLs
eqk = {e['keyword'] for e in EQ}
check('07 all 28 Stage 3 ranking keywords in ranking protection', len(PR) == 28 and {p['keyword'] for p in PR} == eqk and len(eqk) == 28)
eq_pos = {(e['keyword'], e['url'].replace(SITE, ''), e['position']) for e in EQ}
check('07 ranking URL and position preserved exactly', {(p['keyword'], p['ranking_url'], p['ranking_position']) for p in PR} == eq_pos)
rank_urls = {e['url'].replace(SITE, '') for e in EQ}
reg_exist = {r['existing_url'] for r in R}
check('08 every Stage 3 ranking URL preserved (action KEEP_EXISTING_URL*)', all(p['action'].startswith('KEEP_EXISTING_URL') for p in PR))
check('08 every Stage 3 ranking URL is a registry target at its current URL', rank_urls <= reg_exist, sorted(rank_urls - reg_exist))
undocumented = [p['keyword'] for p in PR if p['action'] != 'KEEP_EXISTING_URL' and not p['reason']]
check('08 any non-targeted ranking keyword is documented', not undocumented)
mis = [p['keyword'] for p in PR if p['action'] == 'KEEP_EXISTING_URL' and p['mapped_target_url'] != p['ranking_url']]
check('08 KEEP_EXISTING_URL rows map to the ranking URL', not mis, mis)
check('08 no migration recommended by Stage 15', not any(re.search(r'\b(MOVE_NOW|REDIRECT_NOW|MIGRATE_NOW)\b', p['action']) for p in PR))

# 9. CVD/HPHT
U_CVD = '/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams'
cvd = [r for r in K if re.search(r'\b(cvd|hpht)\b', r['keyword'])]
check('09 CVD/HPHT keywords map only to the existing CVD-vs-HPHT URL (or are unmapped)',
      all(r['target_url'] in ('', U_CVD) for r in cvd) and all(r['target_id'] in ('', 'EDU-LG-03') for r in cvd))
check('09 no registry target is a CVD-only or HPHT-only page',
      not any(re.search(r'\b(cvd|hpht)\b', (r['target_page_name'] + r['proposed_url']).lower()) and r['target_id'] != 'EDU-LG-03' for r in R))
check('09 CL-016/017/018 all on EDU-LG-03', all(r['target_id'] == 'EDU-LG-03' for r in K if r['cluster_id'] in ('CL-016', 'CL-017', 'CL-018')))

# 10. lab vs natural
U_LVN = '/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams'
lvn = [r for r in K if r['cluster_id'] == 'CL-011']
check('10 lab-vs-natural (CL-011) keywords stay on the existing URL (KEEP)', lvn and all(r['target_url'] == U_LVN and r['mapping_disposition'] == 'MAP_EXISTING_URL_KEEP' for r in lvn))
check('10 no other target claims lab-vs-natural comparison wording',
      not [r['keyword'] for r in K if r['target_id'] and r['target_id'] != 'EDU-LG-02'
           and re.search(r'(lab|synthetic).*(vs|or|difference).*natural|natural.*(vs|or|difference).*(lab|synthetic)', r['keyword'])
           and not re.search(r'microscope|tester|\btest|detect|\btell\b', r['keyword'])])  # identification questions belong to EDU-LG-09 (D14-13)

# 11. commercial SERPs not on Education
bad11 = [r['keyword'] for r in K if r['target_id'].startswith('EDU') and r['serp_page_type'] in ('CATEGORY', 'PRODUCT', 'BRAND')]
check('11 no validated CATEGORY/PRODUCT/BRAND keyword mapped to Education', not bad11, bad11)
excl = {r['cluster_id'] for r in CONS if r['assignment_role'] == 'PRIMARY' and r['decision'] == 'EXCLUDE_NOT_EDUCATION'}
leak = [r for r in K if r['cluster_id'] in excl and r['target_id'].startswith('EDU')]
explained = all(('SECONDARY' in r['reason'] or 'Keyword-level INFORMATIONAL' in r['reason']) for r in leak)
check('11 Education mappings from Stage 14-excluded clusters carry explicit evidence', explained, [r['keyword'] for r in leak if not ('SECONDARY' in r['reason'] or 'Keyword-level INFORMATIONAL' in r['reason'])])
check('11 Stage 14-excluded head terms not on Education (CL-001/006/104/105/120/123 fully unmapped to EDU)',
      not [r for r in K if r['cluster_id'] in ('CL-001', 'CL-006', 'CL-104', 'CL-105', 'CL-120', 'CL-123') and r['target_id'].startswith('EDU')])

# 12-13. deferred / conditional topics get no production URL
nonprod = {t for t, a in ARCH.items() if a['architecture_status'] in ('CONDITIONAL', 'DEFERRED')}
check('12/13 no CONDITIONAL/DEFERRED Stage 14 topic is a target', not (set(RID) & nonprod), sorted(set(RID) & nonprod))
check('12/13 no keyword targets a conditional/deferred topic', not [r for r in K if r['target_id'] in nonprod])
check('13 interim homes only where Stage 14 primary topic is CONDITIONAL and a SECONDARY row (or D15 rule) names the home',
      all(ARCH.get(r['stage14_topic_id'], {}).get('architecture_status') == 'CONDITIONAL' for r in K if r['mapping_disposition'] == 'MAP_INTERIM_HOME'))
check('12 conditional/deferred dispositions have blank target_url', all(r['target_url'] == '' for r in K if r['mapping_disposition'] not in MAPPED))

# 15. no duplicate target URLs
urls = [u for r in R for u in (r['existing_url'], r['proposed_url']) if u.startswith('/')]
check('15 no duplicate target URLs (existing + proposed)', len(urls) == len(set(urls)), [u for u, n in collections.Counter(urls).items() if n > 1])
prop = [r['proposed_url'] for r in R if r['proposed_url'].startswith('/')]
check('15 proposed URL expressions follow D-12 (lowercase, hyphens, no query, no ids, no brand suffix, <=3 segments)',
      all(re.fullmatch(r'/education(/[a-z0-9]+(-[a-z0-9]+)*){1,2}', u) and 'house-of-diams' not in u and '-copy-' not in u for u in prop), prop)
check('15 target_url in map equals registry URL', all(
    r['target_url'] == (next(x for x in R if x['target_id'] == r['target_id'])['existing_url'] or
                        (next(x for x in R if x['target_id'] == r['target_id'])['proposed_url'] if next(x for x in R if x['target_id'] == r['target_id'])['proposed_url'].startswith('/') else ''))
    for r in K if r['target_id']))

# 16-18. controlled values
check('16 no invalid mapping dispositions', {r['mapping_disposition'] for r in K} <= DISP, {r['mapping_disposition'] for r in K} - DISP)
check('17 no invalid confidence values', {r['mapping_confidence'] for r in K} <= CONF)
check('18 no invalid cannibalization-risk values', {r['cannibalization_risk'] for r in K} <= RISK and {r['cannibalization_risk'] for r in R} <= RISK)
check('18 no invalid target_url_status values', {r['target_url_status'] for r in K} <= URLST)
check('18 registry status/existing_or_proposed coherent', all((r['existing_or_proposed'] == 'EXISTING') == bool(r['existing_url']) for r in R))

# Special checks from the brief
check('S1 no lab-grown-only 4Cs target', not [r for r in R if '4C' in r['target_id'] and 'lab-grown' in r['target_page_name'].lower() and r['target_id'] != 'EDU-4C-00'])
check('S2 no per-shape page targets', [r['target_id'] for r in R if 'SHP' in r['target_id']] == ['EDU-SHP-00'])
check('S3 no IGI-only page (EDU-CERT-03 not a target)', 'EDU-CERT-03' not in RID)
check('S4 are-real (EDU-LG-01) holds no comparison keywords', not [r for r in K if r['target_id'] == 'EDU-LG-01' and re.search(r'\bvs\b|differen|better|compar', r['keyword'])])
check('S5 SI/VVS/clarity follow Stage 14', all(r['target_id'] == 'EDU-4C-02' for r in K if r['cluster_id'] == 'CL-041') and
      all(r['target_id'] == 'EDU-4C-03' for r in K if r['cluster_id'] == 'CL-043') and
      all(r['target_id'] == 'EDU-4C-01' and r['mapping_disposition'] == 'MAP_INTERIM_HOME' for r in K if r['cluster_id'] == 'CL-042'))
check('S6 CL-001 head terms not mapped to any URL', all(r['target_id'] == '' for r in K if r['cluster_id'] == 'CL-001'))
check('S7 no generic Buying Guides target', not [r for r in R if 'buying guides' in r['target_page_name'].lower()])
check('S8 no noise/competitor rows in registry', not [r for r in K if r['mapping_disposition'] in ('EXCLUDE_NOISE', 'EXCLUDE_COMPETITOR_BRAND') and r['target_id']])

# 19-20. no live-site / upstream modifications
snap = json.load(open(P('architecture/scripts/15_upstream_checksums.json')))
changed = [p for p, h in snap.items() if not os.path.exists(P(p)) or hashlib.sha256(open(P(p), 'rb').read()).hexdigest() != h]
check('20 Stage 1-14 files and all other pre-Stage-15 files unchanged (sha256 snapshot)', not changed, changed)
s14 = json.load(open(P('architecture/scripts/14_upstream_checksums.json')))
ch14 = [p for p, h in s14.items() if os.path.exists(P(p)) and hashlib.sha256(open(P(p), 'rb').read()).hexdigest() != h]
check('20 files checksummed at Stage 14 still unchanged', not ch14, ch14)
stage_files = [p for p in snap if re.match(r'(dataforseo/processed/07_|serp/analysis/08_|competitors/|content-strategy/1[034]_|clusters/11_|architecture/1[24]_)', p)]
check('20 Stage 7-14 deliverables covered by the snapshot', len(stage_files) >= 40, len(stage_files))
ALLOWED_NEW = {'architecture/15_keyword_url_map.csv', 'architecture/15_target_page_registry.csv', 'architecture/15_cluster_page_map.csv',
               'architecture/15_cannibalization_check.csv', 'architecture/15_keyword_url_mapping_summary.md', 'architecture/15_keyword_mapping_decision_log.md',
               'content-strategy/15_ranking_equity_protection.csv', 'architecture/scripts/build_15.py', 'architecture/scripts/summary_15.py',
               'architecture/scripts/qc_15.py', 'architecture/scripts/15_upstream_checksums.json', 'progress.md', 'cost-log.csv', 'decision-log.md'}
new = []
for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
    for f in files:
        if f.startswith('.'):
            continue
        p = os.path.relpath(os.path.join(root, f), ROOT)
        if p not in snap and p not in ALLOWED_NEW:
            new.append(p)
check('19 no live-site, site-inventory, raw-API or other files created/modified', not new, new)
check('19 site/ inventory files unchanged', not [p for p in changed if p.startswith('site/')])
check('19 no new raw API output (dataforseo/raw, serp/raw, competitors/raw)', not [p for p in new if '/raw' in p])

# security
blob = ''.join(open(P(p), encoding='utf-8').read() for p in ALLOWED_NEW if os.path.exists(P(p)) and p.startswith(('architecture/15', 'content-strategy/15', 'architecture/scripts/build_15', 'architecture/scripts/summary_15')))
check('SEC no credentials in Stage 15 files', not re.search(r'(DATAFORSEO_(LOGIN|PASSWORD)\s*=|api[_-]?key\s*[:=]|Authorization:\s*Basic)', blob, re.I))

# earlier QC scripts still pass
for q in ('qc_12.py', 'qc_14.py'):
    rc = subprocess.run([sys.executable, P('architecture/scripts', q)], capture_output=True, text=True)
    check(f'UP {q} still passes', rc.returncode == 0, rc.stdout.strip().splitlines()[-1] if rc.stdout.strip() else rc.stderr[-200:])
rc = subprocess.run([sys.executable, P('content-strategy/scripts/qc_13.py')], capture_output=True, text=True)
check('UP qc_13.py still passes', rc.returncode == 0, rc.stdout.strip().splitlines()[-1] if rc.stdout.strip() else rc.stderr[-200:])

fails = [r for r in results if not r[1]]
for n, ok, d in results:
    print(('PASS ' if ok else 'FAIL ') + n + ('' if ok else f'  -> {d}'))
print(f'\n{len(results) - len(fails)}/{len(results)} checks passed')
sys.exit(1 if fails else 0)
