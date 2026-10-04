#!/usr/bin/env python3
"""Stage 19 QC — content briefs. Read-only except for writing 19_output_checksums.json (check 28).
Exits non-zero on failure."""
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = lambda *a: os.path.join(BASE, *a)
rd = lambda p: list(csv.DictReader(open(P(p), newline='', encoding='utf-8')))
CS = 'content-strategy'

BR = rd(f'{CS}/19_content_briefs.csv')
RG = rd(f'{CS}/19_brief_registry.csv')
BD = rd(f'{CS}/19_content_boundaries.csv')
BF = rd(f'{CS}/19_business_fact_requirements.csv')
LK = rd(f'{CS}/19_internal_link_requirements.csv')
MD = {n: open(P(CS, n), encoding='utf-8').read() for n in ('19_stage_summary.md', '19_decision_log.md')}
OUTS = [f'{CS}/19_content_briefs.csv', f'{CS}/19_brief_registry.csv', f'{CS}/19_content_boundaries.csv',
        f'{CS}/19_business_fact_requirements.csv', f'{CS}/19_internal_link_requirements.csv', f'{CS}/19_stage_summary.md', f'{CS}/19_decision_log.md']
ALLOWED_NEW = set(OUTS) | {f'{CS}/scripts/{f}' for f in ('build_19.py', 'qc_19.py', '19_upstream_checksums.json', '19_upstream_qc_baseline.json',
                                                         '19_build_stats.json', '19_build_log.json', '19_output_checksums.json')}
LOGS = {'progress.md', 'cost-log.csv', 'decision-log.md'}

REG15 = rd('architecture/15_target_page_registry.csv')
T = [r['target_id'] for r in REG15]
KMAP = rd('architecture/15_keyword_url_map.csv')
L16 = rd('architecture/16_internal_link_map.csv')
EQ = rd(f'{CS}/15_ranking_equity_protection.csv')
GAPS = rd(f'{CS}/18_semantic_gap_register.csv')
GAP = {g['gap_id']: g for g in GAPS}
XOWN = rd(f'{CS}/18_cross_page_semantic_ownership.csv')
QC18 = rd(f'{CS}/18_question_coverage.csv')
QID = {f'Q18-{i:03d}': q for i, q in enumerate(QC18, 1)}
CH = rd('serp/analysis/18_5_stage18_change_log.csv')
CLID = {f'CL185-{i:03d}': r for i, r in enumerate(CH, 1)}
V185 = {r['keyword']: r for r in rd('serp/analysis/18_5_targeted_serp_validation.csv')}
CL11 = {r['cluster_id'] for r in rd('clusters/11_cluster_registry.csv')}
KNOWN = set(T) | {r['page_id'] for r in rd('architecture/16_page_link_requirements.csv')} | {r['topic_id'] for r in rd('architecture/14_education_architecture.csv')}
SNAP = json.load(open(P(CS, 'scripts', '19_upstream_checksums.json')))
BASEQ = json.load(open(P(CS, 'scripts', '19_upstream_qc_baseline.json')))

CONTENT = [r for r in BR if r['heading_level'] != 'CONTROL']
CONTROL = [r for r in BR if r['heading_level'] == 'CONTROL']
CONTEXTUAL = {'CONTEXTUAL', 'RELATED_CONTENT', 'EDITORIAL', 'EDUCATIONAL_CTA', 'COMMERCIAL_CTA', 'PRODUCT_RECOMMENDATION'}

R = []


def check(n, name, ok, detail=''):
    R.append((n, name, bool(ok), detail))


def sha(p):
    return hashlib.sha256(open(P(p), 'rb').read()).hexdigest()


def all_cells(rows):
    for r in rows:
        for k, v in r.items():
            yield k, v or ''


ALL_TEXT = [v for rows in (BR, RG, BD, BF, LK) for _, v in all_cells(rows)] + list(MD.values())

# effective severity recomputed independently from the 18.5 change log
WMAP = {'CRITICAL': 'CRITICAL_COVERAGE', 'IMPORTANT': 'IMPORTANT_COVERAGE', 'SUPPORTING': 'SUPPORTING_COVERAGE', 'OPTIONAL': 'OPTIONAL_CONTEXT'}
EFF = {g['gap_id']: g['gap_severity'] for g in GAPS}
for r in CH:
    m = re.search(r'Implied weight\s*([A-Z]*)\s*->\s*([A-Z]+)', r['notes'])
    if r['affected_gap_id'].startswith('G18-') and m and m.group(2) in WMAP:
        EFF[r['affected_gap_id']] = WMAP[m.group(2)]

ev_by_page_content = defaultdict(set)
ev_by_page_all = defaultdict(set)
for r in BR:
    ids = set(re.findall(r'G18-\d{4}', r['evidence_source']))
    ev_by_page_all[r['target_page_id']] |= ids
    if r['heading_level'] != 'CONTROL':
        ev_by_page_content[r['target_page_id']] |= ids

# 1-3
check(1, 'Exactly 27 Stage 15 target pages accounted for', len(T) == 27 and sorted(r['target_page_id'] for r in RG) == sorted(T)
      and {r['target_page_id'] for r in BR} == set(T))
bad2 = [r['target_page_id'] for rows in (BR, RG, BD, BF) for r in rows if r['target_page_id'] not in T]
bad2 += [r['owner_page_id'] for r in BD if r['owner_page_id'] not in KNOWN | {'EXCLUDED', 'OWNERSHIP_REVIEW_REQUIRED'}]
bad2 += [r['brief_page_id'] for r in LK if r['brief_page_id'] not in T]
check(2, 'No unauthorised new target page (all IDs are Stage 15 targets or existing Stage 14/15/16 pages)', not bad2, str(bad2[:5]))
req_cols = ['page_name', 'page_type', 'status', 'url', 'primary_intent', 'primary_keyword', 'searcher_need', 'journey_stages', 'content_depth',
            'serp_format', 'critical_requirements', 'ownership_review', 'existing_ranking_equity']
bad3 = [(r['target_page_id'], c) for r in RG for c in req_cols if not r[c].strip()]
bad3 += [r['target_page_id'] for r in RG if not r['searcher_need'].startswith('The user is trying to')]
bad3 += [r['target_page_id'] for r in RG if r['content_depth'] not in ('Essential', 'Moderate', 'Comprehensive')]
bad3 += [t for t in T if sum(1 for c in CONTROL if c['target_page_id'] == t) != 6]
check(3, 'Every target has one complete brief registry row (plus 6 control rows: MUST/SHOULD/DO NOT DUPLICATE/BUSINESS/INSUFFICIENT/NOT NEEDED)',
      len({r['target_page_id'] for r in RG}) == len(RG) == 27 and not bad3, str(bad3[:5]))

# 4 evidence traceability
bad4 = []
for r in BR:
    ev = r['evidence_source']
    if not re.search(r'G18-\d{4}|CL185-\d{3}|V185:|S18P:|Q18-\d{3}|\.csv|derived from section rows', ev):
        bad4.append(r['section_id'])
    for g in re.findall(r'G18-\d{4}', ev):
        if g not in GAP:
            bad4.append((r['section_id'], g))
    for c in re.findall(r'CL185-\d{3}', ev):
        if c not in CLID:
            bad4.append((r['section_id'], c))
    for q in re.findall(r'Q18-\d{3}', ev):
        if q not in QID or QID[q]['target_page_id'] != r['target_page_id']:
            bad4.append((r['section_id'], q))
    for v in re.findall(r'V185:([^;]+)', ev):
        if v.strip() not in V185:
            bad4.append((r['section_id'], v))
for r in CONTENT:
    for g in re.findall(r'G18-\d{4}', r['evidence_source']):
        if GAP[g]['target_page_id'] != r['target_page_id']:
            bad4.append((r['section_id'], g, 'other page'))
check(4, 'Every section traces to Stage 17/18/18.5 evidence (all cited G18/CL185/Q18/V185 IDs exist and belong to the page)', not bad4, str(bad4[:5]))

# 5-6 critical / important coverage
def owned_here(g):
    return g['owner_page_id'] == g['target_page_id'] or g['owner_status'] == 'INTERIM_HOME_HERE'


crit = [g['gap_id'] for g in GAPS if EFF[g['gap_id']] == 'CRITICAL_COVERAGE' and owned_here(g)]
miss5 = [g for g in crit if g not in ev_by_page_content[GAP[g]['target_page_id']]]
check(5, f'Critical gaps not silently omitted ({len(crit)} effective CRITICAL, owned here, all in content sections)', not miss5, str(miss5))
imp = [g['gap_id'] for g in GAPS if EFF[g['gap_id']] == 'IMPORTANT_COVERAGE']
miss6 = [g for g in imp if g not in ev_by_page_content[GAP[g]['target_page_id']]]
allg = [g for g in GAP if g not in ev_by_page_all[GAP[g]['target_page_id']]]
check(6, f'Important gaps represented ({len(imp)} effective IMPORTANT in content sections; all 304 gaps have a home)', not miss6 and not allg, str(miss6 + allg))

# 7 cross-page ownership preserved
bad7 = []
bkey = {(b['target_page_id'], b['concept'], b['owner_page_id'], b['ownership_status']) for b in BD}
for x in XOWN:
    if (x['current_target_page_id'], x['concept'], x['actual_owner_page_id'], x['relationship']) not in bkey:
        bad7.append(('boundary', x['concept'][:40]))
for g in GAPS:
    if g['owner_status'] in ('OWNED_ELSEWHERE', 'COMMERCIAL_PAGE_OWNER', 'CONDITIONAL_OWNER_NOT_BUILT'):
        rows = [r for r in BR if g['gap_id'] in r['evidence_source'] and r['target_page_id'] == g['target_page_id']]
        if not rows or not any(g['owner_page_id'] in r['cross_page_owner'] for r in rows):
            bad7.append(('section', g['gap_id']))
        for r in rows:
            if r['heading_level'] != 'CONTROL' and f"[BRIEF_MENTION -> {g['owner_page_id']}]" not in r['required_concepts']:
                bad7.append(('treatment', g['gap_id']))
check(7, 'Cross-page ownership preserved (66 Stage 18 boundaries carried; owned-elsewhere concepts are brief mentions naming the owner)', not bad7, str(bad7[:5]))

# 8 no second owner
owners = defaultdict(set)
for b in BD:
    if b['ownership_status'] in ('OWNED_HERE', 'OWNED_ELSEWHERE', 'INTERIM_HOME_HERE', 'COMMERCIAL_PAGE_OWNER', 'CONDITIONAL_OWNER_NOT_BUILT'):
        owners[b['concept'].strip().lower()].add(b['owner_page_id'])
bad8 = {c: o for c, o in owners.items() if len(o) > 1}
xk = defaultdict(set)
for g in GAPS:
    for k in re.findall(r'\[xkey:([^\]]+)\]', g['notes']):
        xk[k].add(g['owner_page_id'])
bad8x = {k: v for k, v in xk.items() if len(v) > 1 and not (k == 'LG_PROCESS' and v == {'EDU-LG-04', 'EDU-LG-00'})}
b_owner_mismatch = [b['concept'][:40] for b in BD if b['ownership_status'] == 'OWNED_HERE' and b['owner_page_id'] != b['target_page_id']]
check(8, 'No concept receives a second owner (boundary concepts map to one owner; Stage 18 cross-key owners unchanged; interim pair LG-04/LG-00 allowed)',
      not bad8 and not bad8x and not b_owner_mismatch, str(list(bad8.items())[:3]) + str(bad8x) + str(b_owner_mismatch[:3]))

# 9 Stage 15 keyword ownership unchanged
k15_changed = [p for p in SNAP if p.startswith(('architecture/15_', 'content-strategy/15_')) and sha(p) != SNAP[p]]
kown = defaultdict(set)
for k in KMAP:
    if k['target_id']:
        kown[k['keyword']].add(k['target_id'])
eqk = defaultdict(set)
for e in EQ:
    eqk[e['mapped_target_id']].add(e['keyword'])
bad9 = []
for r in RG:
    t = r['target_page_id']
    kws = [x.strip() for x in re.split(r'\s*\|\s*co-primary:\s*|;', r['primary_keyword'] + ';' + r['secondary_keywords']) if x.strip()]
    for kw in kws:
        if t not in kown.get(kw, set()) and kw not in eqk[t]:
            bad9.append((t, kw))
check(9, 'Stage 15 keyword ownership unchanged (15_* files byte-identical; every brief keyword is mapped to that page in Stage 15)', not k15_changed and not bad9,
      str(k15_changed + bad9[:5]))

# 10 Stage 16 links unchanged and only Stage 16 relationships used
l16_changed = [p for p in SNAP if p.startswith('architecture/16_') and sha(p) != SNAP[p]]
rows16 = {f'L16-{i:03d}': r for i, r in enumerate(L16, 1)}
bad10 = []
for l in LK:
    s = rows16.get(l['stage16_row'])
    if not s or any(s[k] != l[k] for k in ('source_page_id', 'target_page_id', 'link_type', 'priority', 'recommended_anchor', 'anchor_type')):
        bad10.append(l['stage16_row'])
    if l['link_type'] not in CONTEXTUAL:
        bad10.append(('structural', l['stage16_row']))
expected = {(rid, 'OUTGOING', r['source_page_id']) for rid, r in rows16.items() if r['link_type'] in CONTEXTUAL and r['source_page_id'] in T} | \
           {(rid, 'INCOMING', r['target_page_id']) for rid, r in rows16.items() if r['link_type'] in CONTEXTUAL and r['target_page_id'] in T}
got = {(l['stage16_row'], l['direction'], l['brief_page_id']) for l in LK}
link_text = ' '.join(r['internal_link_context'] for r in BR)
invented = [m for m in re.findall(r'OUT->([A-Z0-9-]+) \[([A-Z_]+)/', link_text)
            if not any(x['target_page_id'] == m[0] and x['link_type'] == m[1] for x in L16)]
check(10, 'Stage 16 links unchanged (16_* files byte-identical; every link row equals a Stage 16 contextual row; complete; none invented)',
      not l16_changed and not bad10 and got == expected and not invented, str(l16_changed + bad10[:3] + invented[:3]) + f' missing={len(expected - got)} extra={len(got - expected)}')

# 11 ranking equity
eq_changed = sha(f'{CS}/15_ranking_equity_protection.csv') != SNAP[f'{CS}/15_ranking_equity_protection.csv']
rg = {r['target_page_id']: r for r in RG}
bad11 = []
for e in EQ:
    t = e['mapped_target_id']
    if t in rg:
        if e['keyword'] not in rg[t]['existing_ranking_equity'] or e['ranking_url'] not in rg[t]['url']:
            bad11.append(e['keyword'])
    elif e['keyword'] != 'cvd/hpht diamond tester':
        bad11.append(e['keyword'])
url_ok = all(REG15[i]['existing_url'] in rg[REG15[i]['target_id']]['url'] for i in range(len(REG15)) if REG15[i]['existing_url'])
check(11, 'Ranking-equity protections unchanged (28 rows; 27 quoted with unchanged URL on their page; tester row excluded)', len(EQ) == 28 and not eq_changed and not bad11 and url_ok, str(bad11))

# 12 tester excluded
kw_fields = ' '.join(r['primary_keyword'] + ' ' + r['secondary_keywords'] for r in RG).lower()
heads = ' '.join(r['heading'] for r in BR).lower()
tb = [b for b in BD if 'cvd/hpht diamond tester' in b['concept'] and b['ownership_status'] == 'EXCLUDED_AVOID']
check(12, '"cvd/hpht diamond tester" remains excluded (not a brief keyword or heading; EXCLUDED boundaries on LG-03 and LG-09)',
      'cvd/hpht diamond tester' not in kw_fields and 'cvd/hpht diamond tester' not in heads and {b['target_page_id'] for b in tb} >= {'EDU-LG-03', 'EDU-LG-09'})

# 13 engagement ring settings review
rv = rg['EDU-RJG-01']['ownership_review']
others = [r['target_page_id'] for r in RG if r['target_page_id'] != 'EDU-RJG-01' and r['ownership_review'] != 'NONE']
check(13, '"engagement ring settings" flagged OWNERSHIP_REVIEW_REQUIRED on EDU-RJG-01 with no second owner',
      rv.startswith('OWNERSHIP_REVIEW_REQUIRED') and 'EDU-RJG-01' in rv and 'separate decision' in rv and not others
      and not [b for b in BD if 'engagement ring settings' in b['concept'].lower() and b['ownership_status'] == 'OWNED_HERE'])

# 14 business-dependent claims not invented
claim_re = re.compile(r"\bHOD(?:'s)? (?:offers|sells|uses|provides|grows|guarantees|sources|stones are|diamonds are|is carbon|is conflict)\b", re.I)
hedge = re.compile(r'whether|which|if |confirm|unknown|never|\bno\b|\bnot\b|until|any |before|once|what |how ', re.I)
bad14 = []
for v in ALL_TEXT:
    for m in claim_re.finditer(v):
        if not hedge.search(v[max(0, m.start() - 60):m.start()]):
            bad14.append(v[max(0, m.start() - 40):m.end() + 20])
bad14 += [f['fact'][:40] for f in BF if not f['source_required'].strip() or f['blocking_status'] not in ('BLOCKING', 'NON_BLOCKING')]
check(14, 'Business-dependent claims are not invented (no unhedged HOD claim; every fact has a source requirement and blocking status)', not bad14, str(bad14[:3]))

# 15 unsupported HOD facts marked
x4 = {r['target_page_id']: r['evidence_source'] + ' ' + r['required_concepts'] for r in CONTROL if r['heading'] == 'BUSINESS FACTS REQUIRED'}
bus = [g for g in GAPS if g['gap_severity'] == 'BUSINESS_DEPENDENT' or g['business_dependency']]
bad15 = [g['gap_id'] for g in bus if g['gap_id'] not in x4.get(g['target_page_id'], '')]
pages_bus = {g['target_page_id'] for g in GAPS if g['gap_severity'] == 'BUSINESS_DEPENDENT'}
bad15 += [t for t in pages_bus if not any(f['target_page_id'] == t for f in BF)]
check(15, f'Unsupported HOD facts are marked as required facts ({len(bus)} business-dependent gaps in X4 rows; every such page has fact rows)', not bad15, str(bad15))

# 16 no search volume
bad16 = [h for rows in (BR, RG, BD, BF, LK) for h in rows[0].keys() if 'volume' in h.lower()]
for v in ALL_TEXT:
    for m in re.finditer(r'(?<![$\d])\b\d{1,3}(?:,\d{3})+\b', v):
        bad16.append(v[max(0, m.start() - 30):m.end() + 5])
    if re.search(r'(search volume|monthly searches|msv)\s*(of|:|=)?\s*\d', v, re.I):
        bad16.append(v[:60])
check(16, 'No unsupported search volume (no volume column, no volume figures)', not bad16, str(bad16[:3]))

# 17-18 guarantees
def unnegated(pattern, text):
    out = []
    for m in re.finditer(pattern, text, re.I):
        pre = text[max(0, m.start() - 50):m.start()].lower()
        if not re.search(r'\bno\b|\bnot\b|nothing|never|without|none|does not|doesn|cannot|no format', pre):
            out.append(text[max(0, m.start() - 40):m.end() + 20])
    return out


g17 = [x for v in ALL_TEXT for x in unnegated(r'guarantee|\b(will|to) rank\b|\brank(ing)? #?1 for\b|top[- ](3|three|10) (position|ranking)|ranking prediction', v)]
check(17, 'No ranking guarantees', not g17, str(g17[:2]))
g18 = [x for v in ALL_TEXT for x in unnegated(r'(will|ensures?|secures?|guarantees?|assures?) (appear|be featured|be cited|be included|win|trigger|rank|feature)[^.\n]{0,40}ai overview', v)]
g18 += [x for v in ALL_TEXT for x in unnegated(r'ai overview (inclusion|placement) (is )?(guaranteed|assured|certain)', v)]
check(18, 'No AI Overview guarantees', not g18, str(g18[:2]))

# 19 existing-page body coverage not falsely claimed
existing = {r['target_id'] for r in REG15 if r['existing_or_proposed'] == 'EXISTING'}
bad19 = []
for r in BR:
    txt = ' '.join(r.values())
    if re.search(r'(current|existing) (article|page|post|blog|content)[^.|]{0,60}(lacks|is missing|does not (cover|include)|doesn.t (cover|include)|omits|fails to)', txt, re.I):
        bad19.append(r['section_id'])
    if re.search(r'CONFIRMED_MISSING|BODY_COVERAGE=(FULL|MISSING|PARTIAL|THIN)', txt):
        bad19.append(r['section_id'])
    if r['target_page_id'] in existing and r['heading_level'] != 'CONTROL' and 'BODY_COVERAGE=UNKNOWN' not in r['notes']:
        bad19.append(('no UNKNOWN note', r['section_id']))
bad19 += [t for t in existing if 'BODY_COVERAGE=UNKNOWN' not in rg[t]['notes']]
check(19, f'Existing-page body coverage is not falsely claimed ({len(existing)} existing pages; UNKNOWN recorded on every section)', not bad19, str(bad19[:4]))

# 20 no article copy
VERBS = {'Explain', 'Open', 'Short', 'Give', 'Provide', 'Compare', 'Summarise', 'Answer', 'List', 'Name', 'State', 'Show', 'Describe', 'Point', 'Separate',
         'Mention', 'Present', 'Guide', 'Link', 'Route', 'Distinguish', 'Acknowledge', 'Set', 'Frame', 'Contrast', 'Correct', 'Discuss', 'Note', 'Help',
         'Illustrate', 'Walk', 'Hand', 'Write', 'Sections', 'Concepts', 'HOD', 'Evidence', 'Questions'}
bad20 = []
for r in BR:
    if r['section_purpose'].split()[0] not in VERBS:
        bad20.append(('verb', r['section_id']))
    for k in ('section_purpose', 'heading', 'comparison_requirements', 'format'):
        v = r[k]
        if len(v) > 450 or len(re.findall(r'[.!?](\s|$)', v)) > 3:
            bad20.append((k, r['section_id']))
for f in ('searcher_need',):
    bad20 += [r['target_page_id'] for r in RG if len(r[f]) > 300]
copy_md = [n for n, t in MD.items() if re.search(r'^\s*(meta description|title tag|seo title)\s*:', t, re.I | re.M)]
check(20, 'No full article copy (instructional purposes, short fields, no titles/metas as copy)', not bad20 and not copy_md, str(bad20[:4] + copy_md))

# 21 no new URL
known_urls = {r['existing_url'] for r in REG15 if r['existing_url']} | {r['proposed_url'] for r in REG15 if r['proposed_url'].startswith('/')}
known_urls |= {r['source_url_or_expression'] for r in L16} | {r['target_url_or_expression'] for r in L16}
known_urls |= {e['ranking_url'] for e in EQ}
known_urls |= {r['url'].replace('https://www.houseofdiams.com', '') for r in rd(f'{CS}/10_existing_content_inventory.csv')}
bad21 = []
for v in ALL_TEXT:
    for m in re.finditer(r'(?<![\w.])/(?:blog|education|engagement-rings|shop|wedding-bands|fine-jewellery|faq|bespoke)[\w/\-]*', v):
        u = m.group(0).rstrip('/-')
        if u not in known_urls and u + '/' not in known_urls:
            bad21.append(u)
bad21 += [r['target_page_id'] for r in RG if not all(p in known_urls or p == 'URL_PENDING' for p in re.findall(r'(?:current|proposed): (\S+)', r['url']))]
check(21, 'No new URL created (every path is a Stage 10/15/16 URL; URL_PENDING kept)', not bad21, str(sorted(set(bad21))[:5]))

# 22 no new cluster
cls = {c for v in ALL_TEXT for c in re.findall(r'\bCL-\d{3}\b', v)}
check(22, 'No new cluster created', cls <= CL11 and 'cluster_id' not in BR[0], str(cls - CL11))

# 23 visual evidence
def visual_ok(r):
    ev = r['evidence_source']
    for g in re.findall(r'G18-\d{4}', ev):
        if GAP[g]['recommended_treatment'] == 'VISUAL_CHART' or GAP[g]['gap_type'] in ('SERP_FORMAT_GAP', 'EXAMPLE_GAP'):
            return True
    for c in re.findall(r'CL185-\d{3}', ev):
        if CLID[c]['affected_target_id'] == r['target_page_id']:
            return True
    for v in re.findall(r'V185:([^;]+)', ev):
        vr = V185[v.strip()]
        if vr['images'] == 'YES' or vr['video'] == 'YES' or 'VISUAL' in vr['content_format_pattern'] or 'printable' in vr['content_format_pattern']:
            return True
    return False


vis = [r for r in CONTENT if re.search(r'VISUAL_CHART|IMAGE|DIAGRAM|INTERACTIVE_TOOL', r['format'])]
bad23 = [r['section_id'] for r in vis if not visual_ok(r)]
check(23, f'Every visual requirement has evidence ({len(vis)} visual sections)', vis and not bad23, str(bad23))

# 24 FAQ evidence
bad24 = []
faq_secs = [r for r in CONTENT if r['heading'] == 'FAQ']
for r in faq_secs:
    has_q = bool(re.search(r'Q18-\d{3}|V185:', r['evidence_source']))
    has_g = any(GAP[g]['recommended_treatment'] == 'FAQ' for g in re.findall(r'G18-\d{4}', r['evidence_source']))
    if not (has_q or has_g):
        bad24.append(r['section_id'])
for r in BR:
    for qid, cls_ in re.findall(r'(Q18-\d{3}|V185:[^\[]+?) \[(FAQ)\]', r['required_questions']):
        if qid.startswith('Q18'):
            q = QID[qid]
            if q['owner_page_id'] != r['target_page_id'] and not any(g['owner_page_id'] == q['owner_page_id'] and g['owner_status'] == 'INTERIM_HOME_HERE'
                                                                   and g['target_page_id'] == r['target_page_id'] for g in GAPS):
                bad24.append((r['section_id'], qid, 'owned elsewhere'))
        if r['heading'] != 'FAQ':
            bad24.append((r['section_id'], qid, 'FAQ outside FAQ section'))
check(24, f'Every FAQ has evidence ({len(faq_secs)} FAQ sections; FAQ questions carry Q18/V185 IDs and are owned by the page)', not bad24, str(bad24[:4]))

# 25 boundary owners
STAT = {'OWNED_HERE', 'OWNED_ELSEWHERE', 'COMMERCIAL_PAGE_OWNER', 'CONDITIONAL_OWNER_NOT_BUILT', 'INTERIM_HOME_HERE', 'EXCLUDED_AVOID'}
bad25 = [b['concept'][:40] for b in BD if not b['owner_page_id'].strip() or b['ownership_status'] not in STAT or not b['evidence'].strip()
         or (b['ownership_status'] == 'EXCLUDED_AVOID') != (b['owner_page_id'] == 'EXCLUDED')]
check(25, f'Every cross-page boundary has an owner ({len(BD)} rows; EXCLUDED only for AVOID rows)', not bad25, str(bad25[:3]))

# 26 upstream files unchanged + only Stage 19 files added + no raw API files
changed = [p for p, h in SNAP.items() if p not in LOGS and (not os.path.exists(P(p)) or sha(p) != h)]
now = set()
for root, dirs, files in os.walk(BASE):
    if '/.' in root:
        continue
    for f in files:
        if not f.startswith('.'):
            now.add(os.path.relpath(os.path.join(root, f), BASE))
new = sorted(now - set(SNAP) - ALLOWED_NEW)
stage_files = [p for p in SNAP if re.match(r'(architecture|content-strategy|serp/analysis|scripts)/.*1[4-8]', p)]
cl = rd('cost-log.csv')
s19 = [r for r in cl if 'Stage 19' in r['stage']]
check(26, f'All Stage 14–18.5 files unchanged ({len(stage_files)} stage files, {len(SNAP)} snapshot files); only Stage 19 files added; $0 spend',
      not changed and not new and all(float(r['actual_cost_usd']) == 0 for r in s19), str(changed[:3] + new[:3]))

# 27 upstream QC
UP = list(BASEQ.keys())[1:]
bad27 = []
summary27 = []
for s in UP:
    out = subprocess.run([sys.executable, P(s)], capture_output=True, text=True, cwd=BASE).stdout
    fails = [l.strip() for l in out.splitlines() if re.match(r'\s*\[?FAIL', l)]
    allowed = BASEQ[s]['pre_stage19'] + BASEQ[s]['stage19_point_in_time']
    unexpected = [l for l in fails if not any(re.match(r'\[?FAIL\]?\s+' + re.escape(a) + r'(\s|\.|$)', l) for a in allowed)]
    bad27 += [(s, l[:80]) for l in unexpected]
    summary27.append(f'{os.path.basename(s)}:{len(fails)}F')
check(27, 'Upstream QC re-run: only pre-Stage-19 failures and the documented Stage 19 point-in-time checks fail (' + ', '.join(summary27) + ')',
      not bad27, str(bad27[:3]))

# 28 checksums
cs = {p: sha(p) for p in OUTS + [f'{CS}/scripts/build_19.py', f'{CS}/scripts/qc_19.py']}
json.dump(cs, open(P(CS, 'scripts', '19_output_checksums.json'), 'w'), indent=1)
reread = json.load(open(P(CS, 'scripts', '19_output_checksums.json')))
check(28, 'Checksums saved (Stage 19 outputs + scripts; pre-stage snapshot present)', reread == cs and len(SNAP) > 200 and all(os.path.getsize(P(p)) > 0 for p in OUTS))

npass = sum(r[2] for r in R)
for n, name, ok, d in R:
    print(f'[{"PASS" if ok else "FAIL"}] {n:>2}. {name}' + (f'  ({d})' if d and not ok else ''))
print(f'\n{npass}/{len(R)} PASS')
sys.exit(0 if npass == len(R) else 1)
