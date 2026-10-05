"""Stage 11 QC + summary writer. Imports the builder (which applies the rules) and derives every number from the data."""
import csv, re, sys, os, itertools, collections as C
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
from build import rows, registry, regmap, relationships, kmap, members, byid, master, ov, val_key, vol_num, ROOT, OUT, CONTROLLED

# ------------------------------------------------------------------ QC
qc = []
def check(name, ok, detail=''):
    qc.append((name, 'PASS' if ok else 'FAIL', detail))
    if not ok:
        print('QC FAIL:', name, detail)

mk = {r['keyword']: r for r in master}
check('1936 unique keywords in the map equal the Stage 7 master set', len(kmap) == 1936 and {r['keyword'] for r in kmap} == set(mk), f"{len(kmap)} rows")
check('No duplicate keyword-cluster mappings (one row per keyword)', len({r['keyword'] for r in kmap}) == len(kmap))
st7 = C.Counter(r['status'] for r in master)
disp_by_status = C.defaultdict(C.Counter)
for c in rows:
    disp_by_status[c['m']['status']][c['disp']] += 1
check('Every Stage 7 INCLUDE keyword has exactly one disposition', sum(disp_by_status['INCLUDE'].values()) == st7['INCLUDE'] == 1258, str(dict(disp_by_status['INCLUDE'])))
check('All Stage 7 NOISE keywords remain NOISE', disp_by_status['NOISE'] == C.Counter({'NOISE': st7['NOISE']}))
check('All Stage 7 COMPETITOR_BRAND keywords remain COMPETITOR_BRAND', disp_by_status['COMPETITOR_BRAND'] == C.Counter({'COMPETITOR_BRAND': st7['COMPETITOR_BRAND']}))
clustered = [c for c in rows if c['disp'] == 'CLUSTERED']
check('Registry keyword_count sums to clustered keywords in the map', sum(int(r['keyword_count']) for r in registry) == len(clustered) == sum(1 for r in kmap if r['cluster_id'].startswith('CL-')), f"{len(clustered)}")
per = C.Counter(r['cluster_id'] for r in kmap if r['cluster_id'].startswith('CL-'))
check('Per-cluster counts: registry equals map for every cluster', all(int(regmap[k]['keyword_count']) == v for k, v in per.items()) and set(per) == set(regmap))
check('Cluster IDs unique; cluster names unique', len({r['cluster_id'] for r in registry}) == len(registry) == len({r['cluster_name'] for r in registry}))
check('AMBIGUOUS keywords are only clustered on a topic-strong rule or Stage 8 evidence (no forced clustering)', all(c['m']['status'] != 'AMBIGUOUS' or c['disp'] != 'CLUSTERED' or byid[c['cluster']]['ambiguous_ok'] or c['s8'] for c in rows))
check('Metrics preserved unchanged from Stage 7 (volume/cpc/competition/difficulty)', all(r['search_volume'] == mk[r['keyword']]['search_volume'] and r['cpc'] == mk[r['keyword']]['cpc'] and r['competition'] == mk[r['keyword']]['competition'] and r['keyword_difficulty'] == mk[r['keyword']]['keyword_difficulty'] for r in kmap))
check('Stage 7 provenance preserved (status and source_stages)', all(r['stage7_status'] == mk[r['keyword']]['status'] and r['stage7_source_stages'] == mk[r['keyword']]['source_stages'] for r in kmap))
s3rows = [r for r in kmap if r['Stage3_current_ranking'] != 'NO']
check('All 28 Stage 3 ranking keywords preserved with rank/URL', len(s3rows) == 28 and all(r['Stage3_current_ranking'].startswith('YES: position') for r in s3rows))
check('All 100 Stage 8 validated keywords preserved', sum(1 for r in kmap if r['Stage8_validated'] == 'YES') == 100)
check('All 28 Stage 3 keywords are clustered (none lost to noise/brand/review)', all(r['cluster_id'].startswith('CL-') for r in s3rows))
check('Relationships reference valid clusters and use only the five permitted types', all(r['cluster_a'] in regmap and r['cluster_b'] in regmap for r in relationships) and {r['relationship_type'] for r in relationships} <= {'DISTINCT_INTENT', 'RELATED_BUT_DISTINCT', 'POSSIBLE_OVERLAP', 'STRONG_OVERLAP', 'INSUFFICIENT_EVIDENCE'})
# cross-cluster fragmentation check: validated keywords in different clusters sharing >=5 top-10 URLs
val = [c for c in clustered if c['s8']]
frag = []
for a, b in itertools.combinations(val, 2):
    if a['cluster'] != b['cluster']:
        n = ov(val_key(a), val_key(b))
        if n >= 5:
            frag.append((n, a['keyword'], a['cluster'], b['keyword'], b['cluster']))
check('No cross-cluster fragmentation signal: no validated pair in different clusters shares >=5 top-10 URLs', not frag, str(sorted(frag, reverse=True)[:5]))
frag4 = sorted([(ov(val_key(a), val_key(b)), a['keyword'], a['cluster'], b['keyword'], b['cluster']) for a, b in itertools.combinations(val, 2) if a['cluster'] != b['cluster'] and ov(val_key(a), val_key(b)) == 4], reverse=True)
# within-cluster cohesion: validated same-cluster pair sharing 0 URLs
zero = C.defaultdict(list)
for cid, g in members.items():
    v = [x for x in g if x['s8']]
    for a, b in itertools.combinations(v, 2):
        zero[cid].append(ov(val_key(a), val_key(b)))
# no forbidden outputs
hdr = ''.join(kmap[0].keys()) + ''.join(registry[0].keys())
check('No URL/slug/page-recommendation columns in outputs', not re.search(r'slug|recommended_url|target_url|redirect|canonical', hdr, re.I))

# ------------------------------------------------------------------ numbers for the summary
n_total = len(rows)
disp = C.Counter(c['assign'] for c in rows)
n_clusters = len(registry)
single = [r for r in registry if r['cluster_size_flag'] == 'SINGLETON']
small = [r for r in registry if r['cluster_size_flag'] == 'SMALL(2-3)']
large = [r for r in registry if r['cluster_size_flag'] == 'LARGE(30+)']
ov_noise_inc = sum(1 for c in rows if c['disp'] == 'NOISE' and c['m']['status'] == 'INCLUDE')
ov_noise_amb = sum(1 for c in rows if c['disp'] == 'NOISE' and c['m']['status'] == 'AMBIGUOUS')
ov_brand_inc = sum(1 for c in rows if c['disp'] == 'COMPETITOR_BRAND' and c['m']['status'] == 'INCLUDE')
ov_brand_amb = sum(1 for c in rows if c['disp'] == 'COMPETITOR_BRAND' and c['m']['status'] == 'AMBIGUOUS')
rev_inc = sum(1 for c in rows if c['disp'] == 'UNCLUSTERED_REVIEW' and c['m']['status'] == 'INCLUDE')
rev_amb = sum(1 for c in rows if c['disp'] == 'UNCLUSTERED_REVIEW' and c['m']['status'] == 'AMBIGUOUS')
amb_clustered = sum(1 for c in rows if c['disp'] == 'CLUSTERED' and c['m']['status'] == 'AMBIGUOUS')

def md_table(headers, rows_):
    out = ['| ' + ' | '.join(headers) + ' |', '|' + '|'.join(['---'] * len(headers)) + '|']
    for r in rows_:
        out.append('| ' + ' | '.join(str(x).replace('|', '/') for x in r) + ' |')
    return '\n'.join(out)

def fmt(n):
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)

# area table
area_stats = C.defaultdict(lambda: [0, 0, []])
for r in registry:
    a = area_stats[r['business_area']]
    a[0] += 1; a[1] += int(r['keyword_count']); a[2].append(r['cluster_id'])
area_rows = []
for a in CONTROLLED + ['UNCLASSIFIED_OR_UNKNOWN']:
    s = area_stats.get(a, [0, 0, []])
    area_rows.append((a, s[0], fmt(s[1]), ', '.join(s[2]) or 'none'))

# intent table
int_stats = C.defaultdict(lambda: [0, 0])
for r in registry:
    i = int_stats[r['primary_intent']]
    i[0] += 1; i[1] += int(r['keyword_count'])
int_rows = [(k, v[0], fmt(v[1])) for k, v in sorted(int_stats.items(), key=lambda kv: -kv[1][0])]

# high volume clusters (by head keyword volume; descriptive ordering only)
hv = sorted([r for r in registry if str(r['max_keyword_volume']) not in ('', 'None')], key=lambda r: -int(r['max_keyword_volume']))[:20]
hv_rows = [(r['cluster_id'], r['cluster_name'], r['head_keyword_by_volume'], fmt(r['max_keyword_volume']), r['keyword_count'], r['validated_keyword_count'], r['evidence_level']) for r in hv]

# Stage 8 evidence
v_clusters = [r for r in registry if int(r['validated_keyword_count']) > 0]
v2 = [r for r in registry if int(r['validated_keyword_count']) >= 2]
coh_rows = []
for r in v2:
    ps = zero[r['cluster_id']]
    coh_rows.append((r['cluster_id'], r['cluster_name'], r['validated_keyword_count'], f"{sum(ps)/len(ps):.1f}", min(ps), max(ps), r['evidence_level'], r['stage8_dominant_page_types']))
ev_counts = C.Counter(r['evidence_level'] for r in registry)
kw_ev = C.Counter(c['ev'] for c in clustered)

# existing content
rel_groups = C.defaultdict(list)
for r in registry:
    rel_groups[r['existing_content_relationship']].append(r)
rel_rows = []
for k in ['STRONG_EXISTING_CONTENT_SIGNAL', 'EXISTING_CONTENT_SIGNAL', 'MULTIPLE_EXISTING_CONTENT_POSSIBLE_OVERLAP', 'NO_EXISTING_CONTENT_EVIDENCE', 'INSUFFICIENT_EVIDENCE']:
    g = rel_groups.get(k, [])
    rel_rows.append((k, len(g), ', '.join(x['cluster_id'] for x in g)))
with_content = [r for r in registry if r['existing_content_relationship'] in ('STRONG_EXISTING_CONTENT_SIGNAL', 'EXISTING_CONTENT_SIGNAL', 'MULTIPLE_EXISTING_CONTENT_POSSIBLE_OVERLAP')]
content_rows = []
for r in with_content:
    urls = [u.replace('/blog/', 'blog/').replace('-house-of-diams', '')[:70] for u in r['existing_HOD_content_urls_linked'].split('; ') if u]
    content_rows.append((r['cluster_id'], r['cluster_name'], r['existing_content_relationship'].replace('_EXISTING_CONTENT', ''), r['current_HOD_ranking_keyword_count'], '; '.join(urls), r['stage10_documented_page_pair_classifications']))
# url -> clusters
url_cl = C.defaultdict(list)
for r in with_content:
    for u in r['existing_HOD_content_urls_linked'].split('; '):
        if u:
            url_cl[u].append(r['cluster_id'])
url_rows = [(u.replace('-house-of-diams', ''), len(v), ', '.join(v)) for u, v in sorted(url_cl.items(), key=lambda kv: -len(kv[1])) if len(v) >= 2]

# relationships
rel_type = C.Counter(r['relationship_type'] for r in relationships)
poss = [r for r in relationships if r['relationship_type'] in ('POSSIBLE_OVERLAP', 'STRONG_OVERLAP')]
poss_rows = [(r['cluster_a'], r['cluster_a_name'][:42], r['cluster_b'], r['cluster_b_name'][:42], r['relationship_type'], r['confidence'], r['relationship_basis']) for r in poss]
dist = [r for r in relationships if r['relationship_type'] == 'DISTINCT_INTENT']
dist_rows = [(r['cluster_a'], r['cluster_b'], r['evidence'][:110]) for r in dist]

# overrides
ov_reason = C.Counter()
for c in rows:
    if c['basis'].startswith('STAGE11_OFFTOPIC'):
        ov_reason[c['basis'].split(': ', 1)[1].split(' (')[0]] += 1
brand_ov = C.Counter(c['brand'] for c in rows if c['basis'].startswith('STAGE11_BRAND'))
review_reasons = C.Counter(c['basis'].split(':')[0] for c in rows if c['disp'] == 'UNCLUSTERED_REVIEW')

# inspection results
def insp(group):
    return [r for r in B.inspect_rows if r['inspection_group'] == group]
def disp_of(rr):
    return C.Counter(r['disposition'] for r in rr)
top60 = insp('HIGH_VOLUME_TOP60')
top25 = top60[:25]
top25_rows = [(r['keyword'], fmt(r['search_volume']), r['stage7_status'], r['disposition'], (r['cluster_id'] + ' ' + r['cluster_name'][:40]).strip()) for r in top25]
s8i = insp('STAGE8_VALIDATED_100')
s8_non = [r for r in s8i if r['disposition'] != 'CLUSTERED']
s8_non_rows = [(r['keyword'], r['stage7_status'], r['disposition'], r['basis'][:70]) for r in s8_non]
s5i = insp('STAGE5_STRATEGIC_SEED_55')
comm = insp('COMMERCIAL_CATEGORY_TERMS')
s3_by_cluster = C.Counter((r['cluster_id'], r['cluster_name']) for r in insp('STAGE3_RANKING_28'))
s3_rows = [(k[0], k[1], v) for k, v in sorted(s3_by_cluster.items())]

# keywords tagged with areas that have no cluster
gap_rows = []
for c in sorted(rows, key=lambda c: c['keyword']):
    m = c['m']
    tag = m['stage5_business_area'] if m['stage5_business_area'] in CONTROLLED else (m['stage6_business_area_best_effort'] if m['stage6_business_area_best_effort'] in CONTROLLED else None)
    if tag and tag not in [a for a in area_stats] and m['status'] in ('INCLUDE', 'AMBIGUOUS'):
        gap_rows.append((c['keyword'], tag, m['status'], c['disp'], (c['cluster'] or '') + (' ' + byid[c['cluster']]['name'][:38] if c['cluster'] else '')))
# structural gaps
zero_areas = [a for a in CONTROLLED if a not in area_stats]

def cstats(a, b):
    v = B.cross_ov(a, b)
    return (len(v), sum(v) / len(v), min(v), max(v)) if v else None

def within(cid):
    v = [ov(val_key(x), val_key(y)) for x, y in itertools.combinations([z for z in members[cid] if z['s8']], 2)]
    return (len(v), sum(v) / len(v), min(v), max(v)) if v else None

def rng(t):
    return f"mean {t[1]:.1f}, range {t[2]}-{t[3]} over {t[0]} pair(s)"

w16, w17, w18 = within('CL-016'), within('CL-017'), within('CL-018')
x1617, x1618, x1718 = cstats('CL-016', 'CL-017'), cstats('CL-016', 'CL-018'), cstats('CL-017', 'CL-018')
x9192, x1011, x3033, x0910 = cstats('CL-091', 'CL-092'), cstats('CL-010', 'CL-011'), cstats('CL-030', 'CL-033'), cstats('CL-090', 'CL-092')
w001 = within('CL-001')
n_ear = int(regmap['CL-125']['keyword_count'])
big_names = ', '.join(f"{r['cluster_id']} ({r['keyword_count']})" for r in sorted(registry, key=lambda r: -int(r['keyword_count']))[:8])
TODAY = '2026-09-24'
def write_summary():
    L = []
    A = L.append
    A('# Stage 11 — Semantic Keyword Clustering Summary')
    A('')
    A(f'Date: {TODAY}. Scope: clustering only. This stage makes no URL, slug, page, merge, redirect, canonical, architecture, prioritization or scoring decision. **A cluster is not a page and not a recommendation.** It is a structured representation of related search demand and intent.')
    A('')
    A('**Stage 11 completed with $0 additional DataForSEO spend.** No DataForSEO endpoint (paid or free) was called. Cumulative spend is unchanged at $0.33536.')
    A('')
    A('Files: `11_cluster_registry.csv` (one row per cluster), `11_keyword_cluster_map.csv` (one row per keyword), `11_cluster_relationships.csv` (cluster pairs), `11_cluster_qc_inspection.csv` (manual-inspection groups), `11_cluster_methodology.md` (method, written before clustering), `scripts/rules.py`, `scripts/engine.py`, `scripts/build.py` and `scripts/summary.py` (the auditable rule set and builder; run `python3 clusters/scripts/summary.py` to regenerate every output).')
    A('')
    A('---')
    A('')
    A('## 1. What was processed')
    A('')
    A(f'- **Total keywords processed: {n_total:,}.** This is the full Stage 7 master database, with nothing dropped. Each keyword has exactly one row in the map.')
    A(f'- **Total meaningful clusters: {n_clusters}.** They hold {len(clustered):,} keywords. {len(single)} are single-keyword clusters and {len(small)} have 2 to 3 keywords. Both are flagged in `cluster_size_flag`.')
    A(f'- **Unclustered / review: {disp["UNCLUSTERED_REVIEW"]}** ({rev_inc} Stage 7 INCLUDE and {rev_amb} Stage 7 AMBIGUOUS).')
    A(f'- **Noise: {disp["NOISE"]}.** Stage 7 NOISE is preserved: {st7["NOISE"]}. Stage 11 added {ov_noise_inc + ov_noise_amb} more ({ov_noise_inc} INCLUDE and {ov_noise_amb} AMBIGUOUS). See section 9.')
    A(f'- **Competitor / brand: {disp["COMPETITOR_BRAND"]}.** Stage 7 COMPETITOR_BRAND is preserved: {st7["COMPETITOR_BRAND"]}. Stage 11 added {ov_brand_inc + ov_brand_amb} more ({ov_brand_inc} INCLUDE and {ov_brand_amb} AMBIGUOUS).')
    A('')
    A(md_table(['Disposition in the map', 'Keywords'], [
        ('PRIMARY_CLUSTER', fmt(disp['PRIMARY_CLUSTER'])), ('SECONDARY_CLUSTER', fmt(disp['SECONDARY_CLUSTER'])),
        ('UNCLUSTERED_REVIEW', fmt(disp['UNCLUSTERED_REVIEW'])), ('NOISE', fmt(disp['NOISE'])), ('COMPETITOR_BRAND', fmt(disp['COMPETITOR_BRAND'])), ('**Total**', f'**{fmt(sum(disp.values()))}**')]))
    A('')
    A('Stage 7 status against Stage 11 disposition:')
    A('')
    ds = disp_by_status
    A(md_table(['Stage 7 status', 'Keywords', 'Clustered', 'UNCLUSTERED_REVIEW', 'NOISE', 'COMPETITOR_BRAND'],
               [(s, fmt(st7[s]), ds[s]['CLUSTERED'], ds[s]['UNCLUSTERED_REVIEW'], ds[s]['NOISE'], ds[s]['COMPETITOR_BRAND']) for s in ['INCLUDE', 'AMBIGUOUS', 'NOISE', 'COMPETITOR_BRAND']]))
    A('')
    A('The Stage 7 master file was **not edited**. Every map row keeps its `stage7_status`, and `stage11_status_override` marks each keyword whose Stage 11 disposition differs from it.')
    A('')
    A('**Assignment types.**')
    A('- `PRIMARY_CLUSTER`: a core member. Its rule match is specific, its intent fits the cluster, and it is not a Stage 7 AMBIGUOUS keyword.')
    A(f'- `SECONDARY_CLUSTER`: a peripheral member. Either only a topic/lexical rule matched, or its verified intent is outside the cluster\'s intents, or Stage 7 marked it AMBIGUOUS and it was clustered on a topic-strong rule or Stage 8 evidence ({amb_clustered} AMBIGUOUS keywords).')
    A('- `other_matching_cluster_ids` lists other clusters whose rules also fired for the keyword. Use it to see where topics touch.')
    A('')
    A('**Evidence labels.**')
    A('- `HIGH`: direct Stage 8 SERP evidence. Either the keyword shares 3 or more top-10 URLs with a validated peer in its cluster, or its own validated SERP intent and page type are consistent with the cluster.')
    A('- `MEDIUM`: a strong semantic and intent rule match with no direct SERP evidence, or a Stage 8 validated keyword whose SERP intent is unclear.')
    A('- `LOW`: a topic/lexical rule only, or a Stage 7 AMBIGUOUS keyword.')
    A(f'- Keyword-level evidence for the {len(clustered):,} clustered keywords: HIGH {kw_ev["HIGH"]}, MEDIUM {kw_ev["MEDIUM"]}, LOW {kw_ev["LOW"]}. Only 100 of 1,936 keywords (5.2%) have direct SERP evidence, so most MEDIUM labels rest on semantics.')
    A(f'- Cluster-level evidence: HIGH {ev_counts["HIGH"]}, MEDIUM {ev_counts["MEDIUM"]}, LOW {ev_counts["LOW"]}. A cluster is HIGH only when it has 2 or more validated members and at least one validated pair shares 3 or more top-10 URLs.')
    A('')
    A('## 2. Clusters by business area')
    A('')
    A('The area is set per cluster from its subject. It is not copied from Stage 5, and it is not forced when evidence is thin.')
    A('')
    A(md_table(['Business area', 'Clusters', 'Keywords', 'Cluster IDs'], area_rows))
    A('')
    A(f'Areas with **no cluster**: {", ".join(zero_areas)}. That is a keyword-data gap, not evidence of low demand. Earlier stages (4 to 10) repeatedly flagged thin or absent coverage for these areas. A few master keywords carry a Stage 5/6 area tag for them (table below), but they are questions about metals, wear and authenticity, so they were clustered by subject or set aside as brand queries, not by the tag.')
    A('')
    A('Master keywords tagged (Stage 5, else Stage 6 best-effort) with an area that has no cluster, and where they went:')
    A('')
    A(md_table(['Keyword', 'Tagged area', 'Stage 7', 'Disposition', 'Cluster'], gap_rows))
    A('')
    A('## 3. Clusters by primary intent')
    A('')
    A(md_table(['Primary intent of the cluster', 'Clusters', 'Keywords'], int_rows))
    A('')
    A('Each registry row also carries `secondary_intents` and an `intent_distribution` computed from its members. Intent was kept separate wherever the searcher need differs. Examples:')
    A('- What lab-grown diamonds are (CL-002).')
    A('- Lab-grown vs natural (CL-011).')
    A('- Are they real (CL-010).')
    A('- Are they worth it (CL-012).')
    A('- Head terms and shopping (CL-001).')
    A('- Wholesale (CL-007).')
    A('- Certification (CL-030 to CL-034).')
    A('')
    A('Keyword-level intent precedence, recorded in `intent_source`:')
    A('1. Stage 8 validated SERP intent.')
    A('2. An explicit text cue: question form, comparison words, or purchase words.')
    A('3. Stage 5 explicit analyst intent.')
    A('4. Stage 5 INFORMATIONAL only where DataForSEO agrees.')
    A('5. The DataForSEO label alone, flagged `DATAFORSEO_LABEL_ONLY`.')
    A('')
    A('Stage 5 never assigned TRANSACTIONAL and defaulted bare phrases to INFORMATIONAL. Stage 8 showed DataForSEO\'s label disagrees with the SERP for 62% of validated keywords. So **' + str(sum(1 for r in kmap if r['intent_source'] == 'DATAFORSEO_LABEL_ONLY' and r['cluster_id'].startswith('CL-'))) + ' clustered keywords carry only a weak DataForSEO-label intent**, and ' + str(sum(1 for r in kmap if r['intent_source'] == 'NO_TEXT_CUE_STAGE5_DEFAULT_VS_DATAFORSEO_DISAGREE' and r['cluster_id'].startswith('CL-'))) + ' are UNCLEAR because Stage 5 and DataForSEO disagree and there is no text cue.')
    A('')
    A('## 4. High-volume clusters')
    A('')
    A('Ordered by the volume of the cluster\'s largest keyword. This is descriptive. It is not a ranking of opportunity, and per-keyword volumes are not summed into a demand figure because near-duplicate variants double-count. The registry keeps `keyword_volume_sum_raw_not_a_demand_estimate` for reference only.')
    A('')
    A(md_table(['Cluster', 'Name', 'Head keyword', 'Volume', 'Keywords', 'Validated', 'Evidence'], hv_rows))
    A('')
    A('## 5. Clusters with Stage 8 SERP evidence')
    A('')
    A(f'{len(v_clusters)} of {n_clusters} clusters contain at least one of the 100 validated keywords. {len(v2)} contain two or more, so SERP similarity could be measured inside them. Overlap counts are shared top-10 organic URLs, computed from the raw Stage 8 SERP files.')
    A('')
    A(md_table(['Cluster', 'Name', 'Validated', 'Mean shared URLs', 'Min', 'Max', 'Cluster evidence', 'Dominant SERP page types'], coh_rows))
    A('')
    A('**Where SERP evidence decided a split or merge (not word overlap):**')
    A(f'- CVD vs HPHT (CL-016), HPHT (CL-017) and CVD (CL-018) are three clusters. Shared top-10 URLs inside each: CL-016 {rng(w16)}; CL-017 {rng(w17)}; CL-018 {rng(w18)}. Across clusters: CL-016 to CL-017 {rng(x1617)}; CL-016 to CL-018 {rng(x1618)}; CL-017 to CL-018 {rng(x1718)}. Cross-cluster relationships are marked POSSIBLE_OVERLAP. QC caught two "CVD vs lab grown" queries that shared 4 to 5 URLs with the CVD-vs-HPHT SERPs, so they were moved into CL-016 (SERP evidence overrides wording).')
    A(f'- Moissanite vs diamond (CL-091) and moissanite vs lab-grown diamond (CL-092): {rng(x9192)}. Moissanite head terms and moissanite vs lab-grown (CL-090 vs CL-092): {rng(x0910)}. Moissanite tester questions (CL-093) form their own tight group.')
    A(f'- The five certification clusters (CL-030 to CL-034) are separate. The general lab-grown certification SERP and the GIA-vs-IGI SERP (CL-033 vs CL-030): {rng(x3033)}. Stage 8 labelled the AGS grading SERP BRAND-dominant (navigational).')
    A(f'- "Are lab-grown diamonds real" (CL-010) and "lab-grown vs natural" (CL-011) are separate: {rng(x1011)}.')
    A('- "Natural diamond wholesale" was merged into the natural head-term cluster (CL-070) because it shares 5 URLs with "natural diamonds".')
    A('- "Diamond stone" (18,100) was **not clustered**. Its SERP mixes an NBA player, sharpening stones and GIA.')
    A(f'- Head terms (`lab grown diamonds`, `lab diamonds`, `diamond growing lab`, `lab diamond companies`) sit together in CL-001 ({rng(w001)}) even though they carry different Stage 8 labels (NAVIGATIONAL, TRANSACTIONAL). That is why CL-001\'s intent is MIXED.')
    A('')
    A('## 6. Clusters and existing HOD content')
    A('')
    A('This records only the relationship between a cluster and existing HOD content, as evidence from Stage 10. It does **not** mean keep, merge, create or retire anything. The basis is Stage 10\'s topic string-match plus Stage 3 rankings. A URL counts when it is linked to at least 2 members and at least 25% of the cluster\'s matched members (1 member for clusters of 3 or fewer), or when it holds a Stage 3 ranking for a member. Stage 10 states that a string match is not proof of relevance, and no match is not proof of absence.')
    A('')
    A(md_table(['Relationship', 'Clusters', 'Cluster IDs'], rel_rows))
    A('')
    A('Clusters with an existing-content signal:')
    A('')
    A(md_table(['Cluster', 'Name', 'Relationship', 'Stage 3 ranking keywords', 'Linked HOD URLs', 'Stage 10 documented page-pair label'], content_rows))
    A('')
    A(f'Existing HOD ranking equity is confined to {sum(1 for r in registry if int(r["current_HOD_ranking_keyword_count"]) > 0)} clusters, all at Stage 3 positions 27 to 104. HOD was in 0 of 795 organic results across the 100 Stage 8 SERPs. This is Stage 3/8/10 evidence restated, not a new finding.')
    A('')
    A('| Stage 3 ranking keywords by cluster | Cluster | Keywords |')
    A('|---|---|---|')
    for cid, nm, n in s3_rows:
        A(f'| {cid} | {nm} | {n} |')
    A('')
    A('## 7. Cluster-level overlap and possible cannibalization')
    A('')
    A(f'`11_cluster_relationships.csv` has {len(relationships)} rows: ' + ', '.join(f'{v} {k}' for k, v in rel_type.most_common()) + '.')
    A('- Rows come from three bases: Stage 8 cross-cluster SERP overlap, semantic judgment, and existing HOD content shared between clusters.')
    A('- There are no STRONG_OVERLAP rows. No pair of validated keywords in different clusters shares 5 or more top-10 URLs (QC check in section 11).')
    A('- SERP-overlap evidence exists only where both clusters have validated members. Elsewhere the row says so, with LOW confidence.')
    A('')
    A('**No actual cannibalization is claimed.** Stage 3 found no keyword with two HOD URLs ranking, and Stage 11 adds no new evidence of it. The cannibalization column reads NOT_DEMONSTRATED throughout. The overlap shown is topic overlap and SERP-sharing between clusters.')
    A('')
    A('POSSIBLE_OVERLAP pairs:')
    A('')
    A(md_table(['A', 'Name A', 'B', 'Name B', 'Type', 'Confidence', 'Basis'], poss_rows))
    A('')
    A('DISTINCT_INTENT pair(s), where the subject is shared but the need differs:')
    A('')
    A(md_table(['A', 'B', 'Evidence'], dist_rows))
    A('')
    A('Existing HOD content linked to more than one cluster (a fact about the current content set, not a recommendation):')
    A('')
    A(md_table(['HOD URL', 'Clusters', 'Cluster IDs'], url_rows))
    A('')
    A('The 4Cs, IGI and GIA-vs-IGI articles link to many clusters largely because Stage 10\'s topic patterns are broad. For example, all 58 certification keywords match both certification pages by construction (Stage 10 OV-01, CLEAR_OVERLAP at topic level, not proven cannibalization).')
    A('')
    A('## 8. Sub-topic checks called out in the brief')
    A('')
    A(md_table(['Topic', 'Cluster(s)', 'Note'], [
        ('Lab-grown diamonds', 'CL-001 to CL-015, CL-019 to CL-024, CL-026', 'Split by searcher need: head/shopping, definition, names, types, geo, carat, wholesale, industry, price, value, authenticity, vs natural, worth-it, ethics, history, process, appearance, detection, testers, quality charts.'),
        ('CVD / HPHT', 'CL-016, CL-017, CL-018', 'Three SERP-supported clusters; the tester-device query sits in CL-022.'),
        ('Lab-grown vs natural', 'CL-011 (plus CL-010, CL-070)', 'Comparison intent kept apart from authenticity and from natural head terms.'),
        ('Certification', 'CL-030 to CL-034', 'GIA vs IGI, GIA, IGI, general lab-grown, other labs/lookup.'),
        ('4Cs', 'CL-040 to CL-049, CL-050, CL-089', 'Scales, SI, VS, VVS, grade comparisons, best clarity, inclusions, colour, colour+clarity, carat, cut, treatments.'),
        ('Diamond shapes', 'CL-060 to CL-065', 'Overview, Asscher, Radiant, Marquise-oval/Moval, shape choice, types overview.'),
        ('Engagement rings', 'CL-120 to CL-124', 'Side-stone (category SERP), setting types (editorial SERP), practicalities, mixed metal, sizing.'),
        ('Wedding bands', 'none of its own; CL-113 (metals)', 'Keyword data gap.'),
        ('Earrings', 'CL-125', f'{n_ear} keywords; a thin area.'),
        ('Necklaces / pendants, Bracelets, Fine jewellery, Bespoke/custom', 'none', 'No cluster subject falls in these areas (keyword-data gap, consistent with Stages 4 to 10). The few keywords that mention necklaces or bracelets are metal/wear questions (CL-112, CL-115) or third-party brand queries.'),
        ('Gemstones', 'CL-100 to CL-105', 'Sapphire, emerald, lab-created stones, natural stones, morganite, coloured-gem rings.'),
        ('Metals', 'CL-110 to CL-115, CL-123', 'Gold karat, rhodium, metal types, tungsten/titanium bands, alternative-material rings, tarnish/wear, mixed metal.'),
        ('Moissanite', 'CL-090 to CL-093, CL-096', 'Clustered on the evidence only. **Clustering is not an endorsement as a HOD target**; business relevance is left to later stages.'),
        ('Diamond simulants / CZ', 'CL-094, CL-095', 'Kept separate from moissanite clusters.'),
    ]))
    A('')
    A('## 9. Stage 7 status overrides (audit)')
    A('')
    A('Stage 7 marked many keywords INCLUDE because Stage 6 only applied lightweight noise flags. Reading the keywords, and using Stage 8 SERPs where available, showed off-topic and brand keywords inside INCLUDE. Stage 11 does not put them in a meaningful cluster. They are **overridden and labelled** in the map (`stage11_status_override`, `clustering_reason`). Stage 7 is untouched.')
    A('')
    A(md_table(['Override reason (off-topic)', 'Keywords'], [(k, v) for k, v in ov_reason.most_common()]))
    A('')
    A(f'Brand overrides ({ov_brand_inc + ov_brand_amb} keywords) name a recognizable retailer or brand or follow the "<name> lab grown diamonds" pattern Stage 5 already used. Named entities: ' + ', '.join(f'{k}' for k, _ in brand_ov.most_common(60)) + '.')
    A('')
    A(f'Company-style names whose brand identity is **not verified** in project data (for example "providence diamond", "universal diamonds", "canos diamonds") were not labelled brands. They stay in UNCLUSTERED_REVIEW with the reason `POSSIBLE_BRAND_NAME_NOT_VERIFIED`. Review reasons: ' + ', '.join(f'{k} ({v})' for k, v in review_reasons.most_common()) + '.')
    A('')
    A('Stage 8 evidence used for overrides and holds:')
    A('- `thc diamond(s)`, `thca diamond` and `dust diamonds` are off-topic (cannabis / diamond painting).')
    A('- `diamond construction`, `detailing`, `recycling` and `equipment` return local businesses. `diamond deshields` and `reed diamond` return people.')
    A('- `diamond stone` is dual-meaning and is held for review.')
    A('')
    A('## 10. Important uncertainties')
    A('')
    A(f'1. **SERP evidence covers 100 of 1,936 keywords (5.2%).** {kw_ev["MEDIUM"] + kw_ev["LOW"]} of {len(clustered):,} clustered keywords rely on semantic or lexical judgment. Cluster boundaries away from the validated keywords may move if more SERPs are checked. No new SERP call was made.')
    A('2. **The engine is rule-based, not a keyword-by-keyword manual judgment.** The rules are explicit and auditable (`clusters/scripts/rules.py`). Every cluster\'s member list was read in full and rules were corrected from that reading (see the inspection log). Some mis-assignments may remain, especially in the larger clusters.')
    A(f'3. **Broad clusters.** The clusters with 30 or more keywords are {", ".join(r["cluster_id"] for r in large)}. The largest clusters are {big_names}. Sub-needs inside them may separate once SERPs are checked. CL-005 spans US and non-US modifiers.')
    A('4. **Heterogeneous SERPs inside clusters.** CL-022 (testers) and CL-113 (tungsten vs titanium) contain validated pairs sharing 0 URLs. They are grouped by searcher need across different entities, so treat the boundary as uncertain.')
    A('5. **Ambiguous senses.** "Types of diamonds", "diamond shape" and "how are diamonds made" may serve more than one sense (shapes / natural vs lab / formation vs manufacture). CL-065 is MIXED and CL-075/CL-015 are flagged POSSIBLE_OVERLAP for that reason.')
    A('6. **Intent labels are weak for many keywords** (see section 3). Stage 8 inferred intent and page type with a disclosed heuristic (24% OTHER/UNCLEAR). Stage 11 inherits that limit.')
    A('7. **Stage 10 topic matching is coarse.** It over-links (certification, 4Cs) and misses (single-keyword matches). Existing-content labels are evidence, not a content audit. INSUFFICIENT_EVIDENCE is used where only isolated single-keyword matches exist.')
    A('8. **Thin or absent commercial coverage.** Wedding Bands, Necklaces & Pendants, Bracelets, Fine Jewellery and Bespoke have no clusters, and Earrings has one small cluster. Commercial category clusters that exist are engagement-ring side-stone/settings and gemstone/metal shopping terms. The master database is dominated by lab-grown education and 4Cs queries (Stage 4-7 sampling limits carried forward), so a cluster map built from it says nothing about demand for the missing areas.')
    A(f'9. **{disp["UNCLUSTERED_REVIEW"]} keywords are held in UNCLUSTERED_REVIEW.** Most are company-style names ("ab diamonds"), truncated phrases and dual-meaning terms. {amb_clustered} Stage 7 AMBIGUOUS keywords were clustered because they were validated in Stage 8 or matched a topic-strong rule, and are marked SECONDARY (evidence LOW unless validated).')
    A(f'10. **Singleton clusters.** {len(single)} clusters contain a single keyword: ' + ', '.join(f'{r["cluster_id"]} ({r["head_keyword_by_volume"]})' for r in single) + '. They are kept because each is a distinct validated or ranking search need with no variants in the data, not because it is a page.')
    A('11. **Business relevance is not judged here.** Clusters on moissanite, CZ, industrial-adjacent science, synonyms and trade topics exist because the data has them. Whether they matter to HOD is for later stages.')
    A('12. **Volume caveat.** Raw volumes are not summed into demand estimates, and no cluster is scored or ranked.')
    A('')
    A('## 11. QC results')
    A('')
    A(md_table(['Check', 'Result', 'Detail'], qc))
    A('')
    A('**Manual inspection log** (Part 9). Files: `11_cluster_qc_inspection.csv`.')
    A('')
    A(md_table(['Inspection group', 'Rows', 'Dispositions'], [
        ('Top 60 keywords by volume', len(top60), dict(disp_of(top60))),
        ('Stage 3 ranking keywords (28)', len(insp('STAGE3_RANKING_28')), dict(disp_of(insp('STAGE3_RANKING_28')))),
        ('Stage 8 validated keywords (100)', len(s8i), dict(disp_of(s8i))),
        ('Stage 5 strategic seeds (55)', len(s5i), dict(disp_of(s5i))),
        ('Commercial category terms (rings, bands, earrings, necklaces, bracelets, fine/bespoke)', len(comm), dict(disp_of(comm))),
        ('Ambiguous or review keywords', len(insp('AMBIGUOUS_OR_REVIEW')), dict(disp_of(insp('AMBIGUOUS_OR_REVIEW')))),
    ]))
    A('')
    A('Top 25 keywords by volume and where they went:')
    A('')
    A(md_table(['Keyword', 'Volume', 'Stage 7', 'Disposition', 'Cluster'], top25_rows))
    A('')
    A('Stage 8 validated keywords not placed in a meaningful cluster (all deliberate, with reasons):')
    A('')
    A(md_table(['Keyword', 'Stage 7', 'Disposition', 'Basis'], s8_non_rows))
    A('')
    A('Corrections made during manual inspection (each was a first-pass error found by reading the member lists):')
    A('- Lab-grown emerald/sapphire "are real" and "vs natural" queries had landed in the lab-grown diamond authenticity and comparison clusters. They were moved to the emerald and sapphire clusters.')
    A('- Moissanite queries that had landed in worth-it, tester and comparison clusters were rerouted to the moissanite clusters (rule priority).')
    A('- A regex bug matched "cvd diamond full form" (via "or" inside "form") to CVD-vs-HPHT. CVD-vs-HPHT now requires both CVD and HPHT tokens.')
    A('- Minecraft "y level", THC "liquid diamonds", local businesses and sports names inside Stage 7 INCLUDE were moved to NOISE (section 9).')
    A('- "Diamond stone" moved from a facts cluster to review because of its mixed SERP.')
    A('- "Natural diamond wholesale" merged into CL-070 on SERP evidence (shares 5 URLs).')
    A('- Cluster-level primary intents were reset after computing intent distributions from members, for example price/worth-it/carat to INFORMATIONAL and geo to MIXED.')
    A('- Names such as "providence diamond" were downgraded from brand to review because the brand identity is unverified.')
    A('')
    A('## 12. DataForSEO spend')
    A('')
    A('**Stage 11 completed with $0 additional DataForSEO spend.** Every question was answered from existing Stage 3-10 data, including the raw Stage 8 SERP files re-read for cross-cluster URL overlap. No paid endpoint was proposed or called, and no clickstream data was used. Cumulative spend remains $0.33536 of $51.00.')
    A('')
    open(OUT + '11_cluster_summary.md', 'w').write('\n'.join(L) + '\n')

if __name__ == '__main__':
    B.build_all()
    write_summary()
    print('QC:', C.Counter(r[1] for r in qc))
    for q in qc:
        print(q[1], '-', q[0], '|', q[2][:100])
    print('fragmentation pairs with 4 shared URLs across clusters:', frag4[:6])
