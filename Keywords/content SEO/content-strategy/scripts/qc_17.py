#!/usr/bin/env python3
"""Stage 17 QC. Local only. Exit code 1 if any check fails."""
import collections
import csv
import glob
import hashlib
import json
import os
import re
import sys

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = lambda *a: os.path.join(BASE, *a)


def rd(p):
    with open(P(p), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))


CONF = {'HIGH', 'MEDIUM', 'LOW', 'INSUFFICIENT_EVIDENCE'}
ROLES = {'PRIMARY', 'CLOSE_VARIANT', 'LONG_TAIL', 'QUESTION', 'COMPARISON', 'ATTRIBUTE', 'SUBTOPIC', 'SUPPORTING',
         'RELATED_BUT_DISTINCT', 'POSSIBLE_OVERLAP', 'EXCLUDE'}
GAPS = {'NO_CONTENT', 'MISSING_SUBTOPIC', 'MISSING_QUESTION', 'MISSING_COMPARISON', 'MISSING_ENTITY',
        'MISSING_COMMERCIAL_CONTEXT', 'MISSING_AEO_COVERAGE', 'MISSING_SERP_FORMAT', 'NO_CLEAR_GAP'}
COVER = {'FULL', 'PARTIAL', 'THIN', 'MISSING', 'UNKNOWN'}
ECS = {'STRONG_EXISTING_CONTENT', 'PARTIAL_EXISTING_CONTENT', 'WEAK_EXISTING_CONTENT', 'NO_EXISTING_CONTENT', 'FUTURE_PAGE'}
INTENTS = {'INFORMATIONAL', 'COMMERCIAL_RESEARCH', 'TRANSACTIONAL', 'NAVIGATIONAL', 'MIXED', 'UNCLEAR'}
CTYPES = {'PRIMARY_CONCEPT', 'SUPPORTING_CONCEPT', 'RELATED_ENTITY', 'OPTIONAL_CONTEXT'}
SERP_TYPES = {'EDITORIAL_GUIDE', 'COMPARISON', 'CATEGORY', 'PRODUCT', 'BRAND', 'REFERENCE', 'FORUM', 'MARKETPLACE',
              'MIXED', 'OTHER', 'UNCLEAR', 'EDUCATIONAL', 'NOT_VALIDATED'}
TESTER = 'cvd/hpht diamond tester'

M15 = rd('architecture/15_keyword_url_map.csv')
B15 = {r['keyword']: r for r in M15}
REG15 = {r['target_id']: r for r in rd('architecture/15_target_page_registry.csv')}
REP15 = rd('content-strategy/15_ranking_equity_protection.csv')
REG11 = {r['cluster_id'] for r in rd('clusters/11_cluster_registry.csv')}
S8 = {r['keyword']: r for r in rd('serp/analysis/08_hod_serp_validation.csv')}
S7 = {r['keyword']: r for r in rd('dataforseo/processed/07_hod_master_keyword_database.csv')}
PLR16 = {r['page_id']: r for r in rd('architecture/16_page_link_requirements.csv')}

DD = rd('content-strategy/17_keyword_deep_dive.csv')
TI = rd('content-strategy/17_topic_intelligence.csv')
SC = rd('content-strategy/17_semantic_concepts.csv')
QM = rd('content-strategy/17_question_map.csv')
KR = rd('content-strategy/17_keyword_relationships.csv')
GR = rd('content-strategy/17_gap_register.csv')
DDK = {r['keyword']: r for r in DD}

PAA, REL = collections.defaultdict(set), collections.defaultdict(set)
for f in glob.glob(P('serp/raw/08_stage8_by_id/*.json')):
    d = json.load(open(f, encoding='utf-8'))
    for t in d.get('tasks') or []:
        for res in t.get('result') or []:
            for it in res.get('items') or []:
                if it.get('type') == 'people_also_ask':
                    for q in it.get('items') or []:
                        PAA[res['keyword']].add((q.get('title') or '').replace('’', "'").replace('‘', "'"))
                if it.get('type') == 'related_searches':
                    for q in it.get('items') or []:
                        REL[res['keyword']].add(q if isinstance(q, str) else q.get('title'))

# 1 every Stage 15 keyword exactly once
cnt = collections.Counter(r['keyword'] for r in DD)
check('01 every Stage 15 keyword appears exactly once in 17_keyword_deep_dive',
      set(cnt) == set(B15) and all(v == 1 for v in cnt.values()) and len(DD) == len(M15), f'{len(DD)} rows / {len(M15)} Stage 15')

# 2 excluded noise not treated as opportunity
exc = [r for r in DD if r['stage15_disposition'].startswith('EXCLUDE')]
qsrc = {q['source_keyword'] for q in QM if q['source_type'] == 'STAGE15_KEYWORD'}
csrc = {c['source_keyword'] for c in SC}
GSUP = {re.sub(r' \([^)]*\)$', '', x) for g in GR for x in g['supporting_keywords'].split(' | ') if x}
bad = [r['keyword'] for r in exc if r['target_page_id'] or r['keyword_role'] != 'EXCLUDE' or r['gap_type'] != 'NOT_ASSESSED'
       or r['keyword'] in qsrc or r['keyword'] in csrc or r['keyword'] in GSUP]
check('02 excluded keywords (noise, competitor, commercial, off-scope) are not treated as opportunities', not bad, f'{len(exc)} excluded; bad={bad[:5]}')

# 3 ownership unchanged
bad = [r['keyword'] for r in DD if r['target_page_id'] != B15[r['keyword']]['target_id']
       or r['stage15_disposition'] != B15[r['keyword']]['mapping_disposition'] or r['stage15_target_url'] != B15[r['keyword']]['target_url']]
check('03 Stage 15 target ownership / disposition / target URL unchanged for every keyword', not bad, str(bad[:5]))

# 4 cluster ids valid
valid = REG11 | {'UNCLUSTERED_REVIEW', 'NOISE', 'COMPETITOR_BRAND'}   # Stage 11 registry + its three assignment buckets
bad = [r['keyword'] for r in DD if r['cluster_id'] not in valid or r['cluster_id'] != B15[r['keyword']]['cluster_id']]
bad += ['C:' + c['concept'] for c in SC if c['cluster_id'] not in valid]
bad += ['Q:' + q['question'] for q in QM if q['cluster_id'] not in valid]
bad += ['G:' + g['cluster_id'] for g in GR for c in g['cluster_id'].split(';') if c.strip() not in valid]
bad += ['R:' + r['keyword'] for r in KR if r['cluster_id'] not in valid or r['related_cluster_id'] not in valid | {'NOT_IN_STAGE7'}]
check('04 all Stage 11 cluster IDs valid and equal to Stage 15', not bad, str(bad[:5]))

# 5 Stage 8 validated intent preserved
bad = [r['keyword'] for r in DD if (r['keyword'] in S8 and (r['validated_intent'] != S8[r['keyword']]['validated_intent']
                                                               or r['stage17_intent_reading'] != S8[r['keyword']]['validated_intent']))
       or (r['keyword'] not in S8 and r['validated_intent'])]
check('05 Stage 8 validated intent preserved (and controls the Stage 17 reading)', not bad, str(bad[:5]))

# 6 no invented SERP evidence
FEAT = [('ai_overview_presence', 'AI Overview'), ('paa_presence', 'PAA'), ('featured_snippet_presence', 'Featured Snippet'),
        ('video_presence', 'Video'), ('image_presence', 'Images'), ('shopping_presence', 'Shopping'), ('local_presence', 'Local Pack')]
bad = []
for r in DD:
    s = S8.get(r['keyword'])
    if s:
        exp = [n for c, n in FEAT if s[c] == 'YES'] + (['Forums'] if 'discussions_and_forums' in s['serp_features'] else [])
        if r['serp_page_type'] != s['dominant_serp_page_type'] or r['serp_confidence'] != s['validation_confidence'] or r['serp_features'] != '; '.join(exp):
            bad.append(r['keyword'])
    elif r['serp_page_type'] != 'NOT_VALIDATED' or r['serp_features'] or r['serp_confidence'] != 'INSUFFICIENT_EVIDENCE':
        bad.append(r['keyword'])
    if r['stage7_labs_serp_items_unvalidated'] != S7[r['keyword']]['serp_summary']:
        bad.append('S7:' + r['keyword'])
for q in QM:
    if q['source_type'] == 'STAGE8_PAA':
        if q['question'] not in PAA.get(q['source_keyword'], set()):
            bad.append('PAA:' + q['question'])
    elif (q['serp_validated'] == 'YES') != any(k in S8 for k in q['variant_keywords'].split(' | ')):
        bad.append('QV:' + q['question'])
for r in KR:
    if r['relationship_source'] == 'STAGE8_RELATED_SEARCHES' and r['related_keyword'] not in REL.get(r['keyword'], set()):
        bad.append('REL:' + r['related_keyword'])
bad += ['TI:' + t['target_page_id'] for t in TI if t['dominant_serp_type'] != 'NOT_VALIDATED' and not any(
    DDK[k]['serp_page_type'] != 'NOT_VALIDATED' for k in DDK if DDK[k]['target_page_id'] == t['target_page_id'] or DDK[k]['topic_group_id'] == t['target_page_id'])]
check('06 no invented SERP evidence (page types, features, PAA and related searches all traceable to Stage 8)', not bad, str(bad[:5]))

# 7 no invented search volume
bad = [r['keyword'] for r in DD if r['search_volume'] != B15[r['keyword']]['search_volume'] or r['search_volume'] != S7[r['keyword']]['search_volume']]
bad += ['TI:' + t['target_page_id'] for t in TI if t['primary_keyword'] and t['primary_keyword_volume'] != B15[t['primary_keyword']]['search_volume']]
bad += ['Q:' + q['question'] for q in QM if q['max_search_volume'] and q['max_search_volume'] != B15[q['source_keyword']]['search_volume']]
check('07 no invented search volume (deep dive = Stage 15 = Stage 7; topic and question volumes traceable)', not bad, str(bad[:5]))

# 8 28 ranking keywords represented
bad = [x['keyword'] for x in REP15 if x['keyword'] not in DDK or DDK[x['keyword']]['current_rank'] != x['ranking_position']
       or DDK[x['keyword']]['ranking_url'] != x['ranking_url']]
check('08 all 28 Stage 3 ranking keywords represented with position and URL', len(REP15) == 28 and not bad, f'{28 - len(bad)}/28')

# 9 protected URLs unchanged
bad = []
for x in REP15:
    t = x['mapped_target_id']
    if t in REG15:
        row = [r for r in TI if r['target_page_id'] == t][0]
        if REG15[t]['existing_url'] not in x['ranking_url'] or row['target_url'] != REG15[t]['existing_url']:
            bad.append(x['keyword'])
bad += [r['keyword'] for r in DD if r['ranking_url'] != B15[r['keyword']]['existing_ranking_url']]
check('09 protected ranking URLs unchanged (targets keep their current ranking URL)', not bad, str(bad[:5]))

# 10 tester keyword excluded
t = DDK[TESTER]
used = (TESTER in qsrc or TESTER in csrc or TESTER in GSUP or any(TESTER in (r['keyword'], r['related_keyword']) for r in KR)
        or any(q['source_keyword'] == TESTER for q in QM))
check('10 "cvd/hpht diamond tester" remains excluded and unused as evidence',
      t['target_page_id'] == '' and t['keyword_role'] == 'EXCLUDE' and t['stage15_disposition'].startswith('EXCLUDE') and not used,
      f"role={t['keyword_role']} disp={t['stage15_disposition']} used={used}")

# 11 no new URLs
known = set()
for r in REG15.values():
    known |= {r['existing_url'], r['proposed_url']}
for r in M15:
    known |= {r['target_url'], r['existing_ranking_url'], r['existing_content_url']}
known |= {r['url'] for r in rd('content-strategy/10_existing_content_inventory.csv')}
knownp = {re.sub(r'^https?://[^/]+', '', k) for k in known if k}
found = set()
for rows in (DD, TI, SC, QM, KR, GR):
    for r in rows:
        for v in r.values():
            for m in re.findall(r'(?<![\w.])(/(?:education|blog|shop|engagement-rings|wedding-bands|fine-jewellery)[\w/-]*)', v or ''):
                found.add(m)
new = sorted(u for u in found if u not in knownp and not any(k.startswith(u) for k in knownp))
bad_t = [r['target_page_id'] for r in TI if r['target_page_id'] in REG15 and r['target_url'] not in (REG15[r['target_page_id']]['existing_url'] or REG15[r['target_page_id']]['proposed_url'], REG15[r['target_page_id']]['proposed_url'])]
check('11 no new URLs (every URL/path in the outputs exists in Stage 10/15)', not new and not bad_t, f'new={new[:5]} bad_targets={bad_t}')

# 12 no keyword ownership changes anywhere
bad = [r['keyword'] for r in KR if r['keyword'] in B15 and r['target_page_id'] != B15[r['keyword']]['target_id']]
bad += [r['related_keyword'] for r in KR if r['related_keyword'] in B15 and r['related_target_page_id'] != B15[r['related_keyword']]['target_id']]
bad += [q['source_keyword'] for q in QM if q['source_type'] == 'STAGE15_KEYWORD' and B15[q['source_keyword']]['target_id'] != q['target_page_id']]
bad += [t['primary_keyword'] for t in TI if t['primary_keyword'] and B15[t['primary_keyword']]['target_id'] != t['target_page_id']]
for t in TI:
    for k in [x for x in (t['co_primary_keywords'] + ' | ' + t['primary_keyword_variants']).split(' | ') if x]:
        if B15[k]['target_id'] != t['target_page_id']:
            bad.append(k)
check('12 no keyword ownership change (relationships, questions, primaries and variants all agree with Stage 15)', not bad, str(bad[:5]))

# 13 no cluster merges
rel_types = {r['relationship_type'] for r in KR}
check('13 no cluster merges (cluster set identical to Stage 15; relationship vocabulary contains no merge)',
      {r['cluster_id'] for r in DD} == {r['cluster_id'] for r in M15} and rel_types <= ROLES and not any('MERGE' in x for x in rel_types),
      str(sorted(rel_types)))

# 14 no content brief
brief_cols = {'outline', 'h1', 'h2', 'meta_title', 'meta_description', 'word_count', 'title_tag', 'brief'}
cols = set()
for f in glob.glob(P('content-strategy/17_*.csv')):
    cols |= set(next(csv.reader(open(f, encoding='utf-8'))))
brief_files = [f for f in glob.glob(P('**/*'), recursive=True) if re.search(r'brief|(^|/)19_', os.path.basename(f), re.I)]
check('14 no content brief created (no brief-style columns; no brief/Stage 19 files)', not (cols & brief_cols) and not brief_files, f'{sorted(cols & brief_cols)} {brief_files[:3]}')

# 15 every question has a target page
bad = [q['question'] for q in QM if q['target_page_id'] not in REG15]
check('15 every question has a Stage 15 target page', not bad, f'{len(QM)} questions')

# 16 every concept has evidence
bad = []
for c in SC:
    t = c['target_page_id']
    owned = {r['keyword'] for r in M15 if r['target_id'] == t}
    txt = set()
    for k in owned:
        txt |= PAA.get(k, set()) | REL.get(k, set())
    txt |= {q['question'] for q in QM if q['target_page_id'] == t}
    if not c['source_keyword'] or not c['evidence_source'] or (c['source_keyword'] not in owned and c['source_keyword'] not in txt) or t not in REG15:
        bad.append(c['concept'])
check('16 every semantic concept has a traceable source keyword/PAA/related search and evidence', not bad, str(bad[:5]))

# 17 confidence vocabulary
bad = []
for rows, colset in ((DD, ['evidence_confidence', 'serp_confidence']), (TI, ['serp_confidence', 'evidence_confidence']),
                     (SC, ['confidence']), (QM, ['confidence']), (KR, ['confidence']), (GR, ['confidence', 'stage18_relevance'])):
    for r in rows:
        for c in colset:
            if r[c] not in CONF:
                bad.append(f'{c}={r[c]}')
check('17 every confidence value uses HIGH / MEDIUM / LOW / INSUFFICIENT_EVIDENCE', not bad, str(sorted(set(bad))[:5]))

# 18 no unsupported commercial assumptions
TM = re.compile(r'\bbuy\b|\bshop\b|for sale|near me|online|\bstore\b|jewell?ers?\b|wholesale|supplier|\brings?\b|earrings|necklace|bracelet|\bbands?\b|collection|custom|bespoke|\bsale\b')
bad = [r['keyword'] for r in DD if r['stage17_intent_reading'] == 'TRANSACTIONAL' and not (
    (r['keyword'] in S8 and S8[r['keyword']]['validated_intent'] == 'TRANSACTIONAL') or r['intent'] == 'TRANSACTIONAL')]
bad += [r['keyword'] for r in DD if r['commercial_signal'] == 'TRANSACTIONAL (Stage 8)' and S8.get(r['keyword'], {}).get('validated_intent') != 'TRANSACTIONAL']
bad += [t['target_page_id'] for t in TI if t['target_page_id'].startswith('EDU') and t['primary_intent'].startswith('TRANSACTIONAL')]
bad += [r['keyword'] for r in DD if r['target_page_id'].startswith('EDU') and r['keyword_role'] == 'PRIMARY' and r['stage17_intent_reading'] == 'TRANSACTIONAL']
check('18 no unsupported commercial assumptions (no intent upgraded to TRANSACTIONAL; Education primaries not transactional)', not bad, str(bad[:5]))

# 19 upstream files unchanged
snap = json.load(open(P('content-strategy/scripts/17_upstream_checksums.json')))
LOGS = {'progress.md', 'cost-log.csv', 'decision-log.md'}
changed = [p for p, h in snap.items() if p not in LOGS and (not os.path.exists(P(p)) or hashlib.sha256(open(P(p), 'rb').read()).hexdigest() != h)]
now = set()
for root, ds, fs in os.walk(BASE):
    for f in fs:
        rel = os.path.relpath(os.path.join(root, f), BASE)
        if not rel.startswith('.') and not f.startswith('.') and '/.' not in rel and '__pycache__' not in rel:
            now.add(rel)
newf = sorted(now - set(snap))
unexpected = [f for f in newf if not re.match(r'content-strategy/(17_|scripts/(build_17|qc_17|17_))', f)]
stage_files = [p for p in snap if re.match(r'(dataforseo/processed/07|serp/|competitors/|content-strategy/1[0-6]_|clusters/11|architecture/1[2-6])', p)]
check('19 Stage 7–16 files unchanged (sha256 vs pre-Stage-17 snapshot); only Stage 17 files added',
      not changed and not unexpected, f'{len(snap)} snapshot files ({len(stage_files)} Stage 7–16 data files); changed={changed[:3]} unexpected_new={unexpected[:3]}')

# 20 no DataForSEO call
raw_new = [f for f in newf if f.startswith(('dataforseo/', 'serp/', 'competitors/'))]
cost_rows = [r for r in csv.DictReader(open(P('cost-log.csv'), encoding='utf-8')) if 'Stage 17' in r.get('stage', '')]
spent = [r for r in cost_rows if (r.get('actual_cost_usd') or '0') not in ('0', '0.00', '0.0') or (r.get('number_of_requests') or '0') not in ('0',)]
check('20 no DataForSEO call occurred (no new raw API files; Stage 17 cost-log rows show $0.00 and 0 requests)', not raw_new and not spent,
      f'raw_new={raw_new} stage17_cost_rows={len(cost_rows)} nonzero={len(spent)}')

# ---- additional integrity checks
check('21 REVIEW_REQUIRED keywords kept in review (not promoted, no target, not a question/concept source)',
      all(r['target_page_id'] == '' and r['analysis_tier'] == 'REVIEW' and r['keyword'] not in qsrc and r['keyword'] not in csrc
          for r in DD if r['stage15_disposition'] == 'REVIEW_REQUIRED'))
check('22 vocabularies respected (keyword_role, gap_type, content_coverage, existing_content_status, concept_type, intents, SERP types)',
      all(r['keyword_role'] in ROLES | {'REVIEW_REQUIRED'} for r in DD)
      and all(r['gap_type'] in GAPS | {'NOT_ASSESSED'} for r in DD) and all(g['gap_type'] in GAPS for g in GR)
      and all(r['content_coverage'] in COVER | {'NOT_ASSESSED'} for r in DD)
      and all(r['existing_content_status'] in ECS | {'NOT_ASSESSED'} for r in DD)
      and all(c['concept_type'] in CTYPES for c in SC)
      and all(r['stage17_intent_reading'] in INTENTS for r in DD)
      and all(r['serp_page_type'] in SERP_TYPES for r in DD))
tids = [t['target_page_id'] for t in TI if not t['target_page_id'].startswith('NO_TARGET::')]
check('23 topic intelligence has exactly one row per Stage 15 target (27); other rows are labelled NO_TARGET::',
      sorted(tids) == sorted(REG15) and all(t['target_page_id'] in REG15 or t['target_page_id'].startswith('NO_TARGET::') for t in TI), f'{len(tids)} targets')
check('24 no FULL coverage claimed without a body audit', not any(r['content_coverage'] == 'FULL' for r in DD))
check('25 unvalidated keywords never carry HIGH evidence confidence',
      not any(r['keyword'] not in S8 and r['evidence_confidence'] == 'HIGH' and r['analysis_tier'] in ('DEEP', 'HELD', 'REVIEW') for r in DD))
check('26 Stage 16 linking context matches the Stage 16 parent page for every target',
      all(('parent=' + (PLR16[t['target_page_id']]['parent_page_id'] or '-')) in t['stage16_linking_context'] for t in TI if t['target_page_id'] in REG15))
check('27 every gap row names a Stage 15 target and a supporting-evidence description',
      all(g['target_page_id'] in REG15 and g['gap_description'] for g in GR))

import subprocess  # noqa: E402
out = subprocess.run([sys.executable, P('architecture/scripts/qc_16.py')], capture_output=True, text=True).stdout
fails = [l for l in out.splitlines() if l.startswith('FAIL')]
extra = re.findall(r"'([^']+)'", fails[0]) if len(fails) == 1 else []
only17 = [f for f in extra if not f.startswith(('architecture/16_', 'architecture/scripts/'))]
check('28 qc_16 still passes except its point-in-time "no new files" chain, which flags only Stage 16/17 deliverables',
      len(fails) == 1 and fails[0].startswith('FAIL  20') and all(re.match(r'content-strategy/(17_|scripts/(build_17|qc_17|17_))', f) for f in only17),
      f'{len(fails)} fail(s)')

npass = sum(ok for _, ok, _ in results)
for name, ok, detail in results:
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{detail}]' if detail and not ok else ''))
print(f'\n{npass}/{len(results)} PASS')
sys.exit(0 if npass == len(results) else 1)
