#!/usr/bin/env python3
"""Stage 18.5 QC — targeted SERP validation supplement. Read-only; exits non-zero on failure."""
import csv
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
P = lambda *a: os.path.join(BASE, *a)
RAW = P('dataforseo', 'raw', '18_5_stage_serp')
rd = lambda p: list(csv.DictReader(open(P(p), newline='', encoding='utf-8')))

APPROVED = ['what are lab grown diamonds', 'do lab grown diamonds hold their value', 'are lab grown diamonds ethical',
            'do lab grown diamonds get cloudy', 'how are diamonds formed', '4cs of diamonds', 'diamond color chart',
            'diamond carat size chart', 'diamond cut', 'diamond shapes', 'diamond certificate', '14k vs 18k gold',
            'white gold vs platinum', 'engagement ring settings', 'ring size chart', 'how to measure ring size',
            'what are diamonds made of']
APPROVED_MAX = 0.0102
SNAP = json.load(open(P('scripts', '18_5_upstream_checksums.json')))
LOGS = {'progress.md', 'cost-log.csv', 'decision-log.md'}
OUTS = [P('serp', 'analysis', f) for f in ('18_5_targeted_serp_validation.csv', '18_5_stage18_change_log.csv',
                                           '18_5_semantic_supplement.md', '18_5_stage_summary.md')]
VAL = rd('serp/analysis/18_5_targeted_serp_validation.csv')
CH = rd('serp/analysis/18_5_stage18_change_log.csv')
MAN = rd('dataforseo/raw/18_5_stage_serp/manifest.csv')
POST = json.load(open(os.path.join(RAW, '00_task_post_response.json'), encoding='utf-8'))
BAL = json.load(open(os.path.join(RAW, '_account_balance_check.json')))
REG18 = {r['gap_id']: r for r in rd('content-strategy/18_semantic_gap_register.csv')}
REG15 = {r['target_id'] for r in rd('architecture/15_target_page_registry.csv')}
CL11 = {r['cluster_id'] for r in rd('clusters/11_cluster_registry.csv')}


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


GET = {}
for f in glob.glob(os.path.join(RAW, '09242103-*.json')):
    d = json.load(open(f, encoding='utf-8'))
    GET[d['tasks'][0]['id']] = d
KW_TEXT = {d['tasks'][0]['result'][0]['keyword']: ' \n'.join(strings(d['tasks'][0]['result'][0])).lower() for d in GET.values()}

R = []


def check(n, name, ok, detail=''):
    R.append((n, name, bool(ok), detail))


def sha(p):
    return hashlib.sha256(open(P(p), 'rb').read()).hexdigest()


changed = [p for p, h in SNAP.items() if p not in LOGS and (not os.path.exists(P(p)) or sha(p) != h)]
post_tasks = POST['tasks']
post_ids = [t['id'] for t in post_tasks]

check(1, 'Exactly 17 queries were executed', POST['tasks_count'] == 17 and len(post_tasks) == 17
      and sorted(t['data']['keyword'] for t in post_tasks) == sorted(APPROVED) and len(GET) == 17)
cl = rd('cost-log.csv')
s185 = [r for r in cl if 'Stage 18.5' in r['stage']]
other_post = [f for f in glob.glob(P('dataforseo', 'raw', '**', '*.json'), recursive=True)
              if '18_5_stage_serp' not in f and 'hod_stage18_5' in open(f, encoding='utf-8', errors='ignore').read()]
check(2, 'No extra paid queries were executed', len(s185) == 1 and s185[0]['number_of_requests'].startswith('1') and not other_post
      and abs(BAL['difference_usd'] - 0.0102) < 1e-9, f'cost-log rows {len(s185)}; stray {other_post[:2]}')
check(3, 'Every task has a task_id', all(r['task_id'] for r in MAN) and len(MAN) == 17 and set(r['task_id'] for r in MAN) == set(post_ids))
check(4, 'Every task has a raw response', set(GET) == set(post_ids)
      and all(GET[i]['tasks'][0]['status_code'] == 20000 and GET[i]['tasks'][0]['result_count'] == 1 for i in GET))
src = json.load(open(os.path.join(RAW, '_raw_sources.json')))
check(5, 'Every raw response is preserved (verbatim, parseable, provenance recorded)', all(i in src for i in post_ids) and 'task_post' in src
      and all(os.path.getsize(os.path.join(RAW, f'{i}.json')) > 5000 for i in post_ids))
check(6, 'Actual cost is recorded', s185 and float(s185[0]['actual_cost_usd']) == 0.0102 and POST['cost'] == 0.0102
      and all(float(r['cost']) == 0.0006 for r in MAN))
check(7, 'Actual cost does not exceed approved maximum', POST['cost'] <= APPROVED_MAX + 1e-12 and BAL['difference_usd'] <= APPROVED_MAX + 1e-12)
datas = [t['data'] for t in post_tasks] + [d['tasks'][0]['data'] for d in GET.values()]
check(8, 'Location = 2840', all(d['location_code'] == 2840 for d in datas))
check(9, 'Language = en', all(d['language_code'] == 'en' for d in datas))
check(10, 'Depth = 10', all(d['depth'] == 10 for d in datas))
check(11, 'Desktop configuration (normal priority)', all(d['device'] == 'desktop' and d['priority'] == 1 for d in datas))
check(12, 'Clickstream = false (no clickstream or extra paid parameter requested)',
      all(not any(re.search(r'clickstream|calculate_rectangles|load_async_ai_overview|people_also_ask_click_depth|search_param|target', k) for k in d) for d in datas))
for n, tag, label in [(13, '15_', 'Stage 15'), (14, '14_', 'Stage 14'), (15, '16_', 'Stage 16'), (16, '17_', 'Stage 17'), (17, '18_', 'Stage 18')]:
    stage_files = [p for p in SNAP if os.path.basename(p).startswith(tag) or ('scripts/' in p and re.search(rf'(build|qc)_{tag[:-1]}\.py$', p))]
    check(n, f'No {label} files changed', stage_files and not [p for p in changed if p in stage_files], f'{len(stage_files)} files checked')
check(18, 'No keyword ownership changed', 'architecture/15_keyword_url_map.csv' not in changed
      and all(r['affected_target_id'] in REG15 for r in CH))
urls = set()
for f in OUTS:
    urls |= set(re.findall(r'houseofdiams\.com/[\w\-/]*', open(f, encoding='utf-8').read()))
check(19, 'No new URL ownership created', not urls and not any('url' in c.lower() for c in list(VAL[0].keys()) + list(CH[0].keys())))
cls = set()
for f in OUTS:
    cls |= set(re.findall(r'\bCL-\d{3}\b', open(f, encoding='utf-8').read()))
check(20, 'No new clusters created', cls <= CL11, str(cls - CL11))
bad21 = [f for f in OUTS if re.search(r'\b(create|build|add|launch|recommend)\w*\s+(a\s+|an\s+)?(new\s+)?(page|url)\b|\bnew page\b', open(f, encoding='utf-8').read(), re.I)
         and not re.search(r'creates no page', open(f, encoding='utf-8').read())]
check(21, 'No page was recommended/created from SERP evidence', not [f for f in OUTS if re.search(r'\bnew page\b|\bcreate (a|an) (new )?page\b|\brecommend(ed)? (a|an) (new )?page\b', open(f, encoding='utf-8').read(), re.I)])
ev_bad = []
for r in CH:
    toks = re.findall(r'\[ev:"(.+?)"\]', r['notes'])
    if not r['new_evidence'].strip() or not toks or r['keyword'] not in KW_TEXT:
        ev_bad.append(r['affected_gap_id'])
        continue
    if any(t.lower() not in KW_TEXT[r['keyword']] for t in toks):
        ev_bad.append(('token', r['keyword'], toks))
    g = r['affected_gap_id']
    if g.startswith('G18-') and (g not in REG18 or REG18[g]['target_page_id'] != r['affected_target_id']):
        ev_bad.append(('gap', g))
check(22, 'All changed assumptions have evidence (verbatim tokens found in raw SERP; gap IDs match Stage 18)', not ev_bad, str(ev_bad[:3]))
vol_bad = []
for f in OUTS:
    t = open(f, encoding='utf-8').read()
    vol_bad += re.findall(r'(search volume|monthly searches|volume)[^\n|]{0,20}\b\d[\d,]{2,}', t, re.I)
    vol_bad += [c for c in (open(f, encoding='utf-8').readline().lower().split(',') if f.endswith('.csv') else []) if 'volume' in c]
check(23, 'No unsupported search-volume claims', not vol_bad, str(vol_bad[:3]))
g_bad = []
for f in OUTS:
    t = open(f, encoding='utf-8').read()
    for m in re.finditer(r'guarantee', t, re.I):
        pre = t[max(0, m.start() - 40):m.start()].lower()
        if not re.search(r'\bno\b|\bnot\b|nothing|never|without', pre):
            g_bad.append(t[max(0, m.start() - 40):m.end() + 10])
    g_bad += re.findall(r'(will|ensures?|secures?) (appear|rank|feature)[^.\n]{0,40}ai overview', t, re.I)
check(24, 'No AI Overview guarantee claims', not g_bad, str(g_bad[:2]))
briefs = glob.glob(P('**', '19_*'), recursive=True)
brief_bad = [f for f in OUTS if re.search(r'^\s*(title|h1|meta description|word count|outline)\s*:', open(f, encoding='utf-8').read(), re.I | re.M)]
check(25, 'No content brief was created', not briefs and not brief_bad, str(briefs[:2] + brief_bad))
# extra integrity
check(26, 'Validation rows: 17, Stage 8 vocabulary for intent/page type, features match raw item types',
      len(VAL) == 17 and all(v['validated_intent'] in {'INFORMATIONAL', 'COMMERCIAL_RESEARCH', 'TRANSACTIONAL', 'NAVIGATIONAL', 'MIXED', 'UNCLEAR'} for v in VAL)
      and all(v['dominant_page_type'] in {'EDITORIAL_GUIDE', 'COMPARISON', 'CATEGORY', 'PRODUCT', 'EDUCATIONAL', 'BRAND', 'MARKETPLACE', 'MIXED', 'OTHER', 'UNCLEAR'} for v in VAL)
      and all((v['ai_overview'] == 'YES') == ('ai_overview' in GET[v['task_id']]['tasks'][0]['result'][0]['item_types'])
              and (v['paa'] == 'YES') == ('people_also_ask' in GET[v['task_id']]['tasks'][0]['result'][0]['item_types'])
              and (v['local_pack'] == 'YES') == ('local_pack' in GET[v['task_id']]['tasks'][0]['result'][0]['item_types']) for v in VAL))
check(27, 'Change-type vocabulary valid', all(r['change_type'] in {'CONFIRMED', 'STRENGTHENED', 'WEAKENED', 'CHANGED', 'INVALIDATED', 'NEW_EVIDENCE', 'CONFLICT', 'UNCHANGED'} for r in CH))
check(28, 'Stage 8 raw SERP files untouched', not [p for p in changed if p.startswith('serp/raw/')])
q18 = subprocess.run([sys.executable, P('content-strategy', 'scripts', 'qc_18.py')], capture_output=True, text=True).stdout
f18 = [l for l in q18.splitlines() if l.startswith('[FAIL]')]
s18_only = [r for r in cl if 'Stage 18 ' in r['stage'] and 'Stage 18.5' not in r['stage']]
check(29, 'qc_18 only fails its point-in-time checks (21: sees the approved Stage 18.5 cost row; 29: qc_17 sees Stage 18/18.5 files); Stage 18 itself stays $0',
      all((' 29.' in l) or (' 21.' in l) for l in f18) and len(s18_only) == 1 and float(s18_only[0]['actual_cost_usd']) == 0
      and not os.path.exists(P('dataforseo', 'raw', '18_stage18')), '; '.join(f18)[:200])

npass = sum(r[2] for r in R)
for n, name, ok, d in R:
    print(f'[{"PASS" if ok else "FAIL"}] {n:>2}. {name}' + (f'  ({d})' if d and not ok else ''))
print(f'\n{npass}/{len(R)} PASS')
sys.exit(0 if npass == len(R) else 1)
