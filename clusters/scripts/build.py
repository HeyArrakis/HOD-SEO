"""Stage 11 builder: applies the rule set (11_clustering_rules.py) to the Stage 7 master database and joins
Stage 3/5/8/9/10 evidence. Reads only local project files. Makes no API calls."""
import csv, re, sys, os, json, glob, math, statistics, itertools, collections as C
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine
from engine import ROOT, norm, load, master, s8, CL, classify
import rules
from rules import I, CR, T, N, M, U, A_UNK

OUT = ROOT + 'clusters/'
byid = {c['id']: c for c in CL}
CONTROLLED = ["1. Engagement Rings", "2. Wedding Bands", "3. Earrings", "4. Necklaces & Pendants", "5. Bracelets", "6. Fine Jewellery",
              "7. Bespoke / Custom Jewellery", "8. Lab-Grown Diamonds", "9. Natural Diamonds", "10. Diamond Shapes", "11. Diamond Cuts",
              "12. Diamond Quality / 4Cs", "13. Diamond Certification", "14. Diamond Buying / Education", "15. Jewellery Materials / Metals", "16. Gemstones"]

# ------------------------------------------------------------------ evidence loading
s5 = {r['keyword'].lower().strip(): r for r in load('dataforseo/processed/05_hod_keyword_classification.csv')}
landscape = load('competitors/analysis/09_hod_competitor_landscape.csv')
coverage = load('content-strategy/10_content_keyword_coverage.csv')
inventory = load('content-strategy/10_existing_content_inventory.csv')
overlaps10 = load('content-strategy/10_content_overlap_analysis.csv')

def relpath(u):
    return u.replace('https://www.houseofdiams.com', '') or '/'

# raw SERP top-10 (Stage 8) -> normalized URL sets
SERP = {}
for f in glob.glob(ROOT + 'serp/raw/08_stage8_by_id/*.json'):
    t = json.load(open(f))['tasks'][0]
    kw = t['data']['keyword'].lower().strip()
    urls = []
    for it in t['result'][0]['items']:
        if it.get('type') == 'organic' and it.get('url') and it.get('rank_group', 99) <= 10:
            u = urlparse(it['url'])
            urls.append((u.netloc.lower() + u.path.rstrip('/')).lower())
    SERP[kw] = set(urls)
assert len(SERP) == 100

def ov(a, b):
    return len(SERP[a] & SERP[b])

# Stage 9 competitor presence per validated keyword
comp_by_kw = C.defaultdict(list)
for r in landscape:
    comp_by_kw[r['validated_keyword'].lower().strip()].append(r)

# Stage 10 per keyword
cov_by_kw = C.defaultdict(list)
for r in coverage:
    cov_by_kw[r['keyword'].lower().strip()].append(r)

# ------------------------------------------------------------------ intent
def pattern_intent(kn):
    if re.match(r'^(what|how|why|when|where|who|which|is|are|can|do|does|will|should|did)\b', kn):
        if re.search(r'\b(vs|versus|better|best|difference|worth it|should i|or)\b', kn):
            return CR
        return I
    if re.search(r'\b(buy|shop|for sale|wholesale|price|cost|cheapest|near me|online|store|discount|clearance|order|supplier|manufacturer)\b', kn):
        return T
    if re.search(r'\b(vs|versus|difference between|better|best|top|review|reviews|compare|comparison|alternative|alternatives|pros and cons)\b', kn):
        return CR
    if re.search(r'\b(meaning|definition|history|explained|guide|facts|process|wiki|wikipedia|synonyms?|types of|chart|scale|grades?)\b', kn):
        return I
    return None

DFS = {'informational': I, 'transactional': T, 'commercial': CR, 'navigational': N}

def kw_intent(m, c, s8row):
    """Precedence: brand > Stage 8 validated SERP intent > explicit text cue (Stage 11 pattern) > Stage 5 explicit intent
    (Stage 5 never assigned TRANSACTIONAL and defaulted bare phrases to INFORMATIONAL, so a bare INFORMATIONAL is only
    trusted when DataForSEO agrees) > Stage 8 unclear/mixed > DataForSEO label (weakest, flagged)."""
    if c['disp'] == 'COMPETITOR_BRAND':
        return N, 'BRAND_KEYWORD'
    if s8row:
        vi = s8row['validated_intent'].upper()
        if vi not in ('UNCLEAR', 'MIXED', ''):
            return vi, 'STAGE8_SERP_VALIDATED'
    p = pattern_intent(c['kn'])
    if p:
        return p, 'STAGE11_TEXT_CUE'
    st5 = m['stage5_intent']
    if st5 in (CR, N, M):
        return st5, 'STAGE5_ANALYST_INTENT'
    if s8row:
        return s8row['validated_intent'].upper(), 'STAGE8_SERP_UNCLEAR_OR_MIXED'
    d = DFS.get(m['intent'])
    if st5 == I:
        if d == I:
            return I, 'STAGE5_AND_DATAFORSEO_AGREE'
        if d:
            return U, 'NO_TEXT_CUE_STAGE5_DEFAULT_VS_DATAFORSEO_DISAGREE'
        return I, 'STAGE5_DEFAULT_INFORMATIONAL_WEAK'
    if d:
        return d, 'DATAFORSEO_LABEL_ONLY'
    return U, 'NONE'

# ------------------------------------------------------------------ classify every keyword
rows = []
for m in master:
    c = classify(m)
    c['m'] = m
    c['s8'] = s8.get(m['keyword'].lower().strip())
    rows.append(c)
assert len(rows) == 1936 == len({r['keyword'] for r in rows})

# validated peers per cluster
members = C.defaultdict(list)
for c in rows:
    if c['disp'] == 'CLUSTERED':
        members[c['cluster']].append(c)

def val_key(c):
    return c['keyword'].lower().strip()

for cid, g in members.items():
    v = [x for x in g if x['s8']]
    for x in v:
        peers = [(ov(val_key(x), val_key(y)), y['keyword']) for y in v if y is not x]
        x['peer_max'] = max([p[0] for p in peers], default=None)
        x['peer_best'] = [p[1] for p in sorted(peers, reverse=True)[:2] if p[0] >= 3]

def money(x):
    return x if x not in ('', 'NOT_AVAILABLE', 'NOT_APPLICABLE') else ''

def vol_num(m):
    try:
        return int(float(m['search_volume']))
    except Exception:
        return None

# ------------------------------------------------------------------ keyword-level fields
def stage3_text(m):
    if m['stage3_current_rank'] in ('', 'NOT_APPLICABLE'):
        return 'NO'
    return f"YES: position {m['stage3_current_rank']} ({relpath(m['stage3_ranking_url'])})"

def stage9_text(kw, s8row):
    if not s8row:
        return 'NOT_ASSESSED (no Stage 8 SERP for this keyword)'
    rr = sorted(comp_by_kw.get(kw, []), key=lambda r: int(r['organic_position']))
    rel = [r for r in rr if r['business_relevance'] == 'RELEVANT']
    if not rel:
        return f"NO_CLASSIFIED_RELEVANT_COMPETITOR_IN_TOP10 ({len(rr)} organic results observed; HOD not observed in top 10)"
    top = '; '.join(f"{r['domain']}@{r['organic_position']}" for r in rel[:3])
    return f"YES: {len(rel)} classified-RELEVANT competitor domains in top 10 (top: {top}); HOD not observed in top 10"

def stage10_info(kw, st):
    rr = cov_by_kw.get(kw, [])
    ranks = [r for r in rr if r['relationship'].startswith('STAGE3_RANKS')]
    topic = [r for r in rr if r['relationship'].startswith('TOPIC_STRING_MATCH')]
    nomatch = [r for r in rr if r['relationship'].startswith('NO_EXISTING_CONTENT_MATCH')]
    urls = sorted({relpath(r['url']) for r in ranks + topic})
    if ranks:
        return 'STAGE3_RANKS: ' + '; '.join(sorted({relpath(r['url']) for r in ranks})), urls, True
    if topic:
        return 'TOPIC_STRING_MATCH_ONLY: ' + '; '.join(urls), urls, False
    if nomatch:
        return 'NO_EXISTING_CONTENT_MATCH (Stage 8 validated keyword)', [], False
    if st == 'INCLUDE':
        return 'NO_TOPIC_MATCH_FOUND_BY_STAGE10 (absence of a string match is not proof of no content)', [], False
    return f'NOT_ASSESSED_BY_STAGE10 (Stage 7 status {st})', [], False

def area_for(c):
    m = c['m']
    if c['disp'] == 'CLUSTERED':
        return byid[c['cluster']]['area'], 'CLUSTER_AREA'
    if c['disp'] == 'NOISE':
        return A_UNK, 'NOISE_NOT_ASSIGNED_TO_AREA'
    a5 = m['stage5_business_area']
    if a5 in CONTROLLED:
        return a5, 'STAGE5_BUSINESS_AREA'
    a6 = m['stage6_business_area_best_effort']
    if a6 in CONTROLLED:
        return a6, 'STAGE6_BEST_EFFORT_AREA'
    if c['disp'] == 'COMPETITOR_BRAND' and re.search(r'lab (grown|created)|lab diamond|lab-grown', c['kn']):
        return '8. Lab-Grown Diamonds', 'BRAND_KEYWORD_LAB_GROWN_MODIFIER'
    return A_UNK, 'INSUFFICIENT_EVIDENCE'

for c in rows:
    m = c['m']; kw = val_key(c); s8row = c['s8']
    c['intent'], c['intent_src'] = kw_intent(m, c, s8row)
    c['area'], c['area_basis'] = area_for(c)
    c['s10_text'], c['s10_urls'], c['s10_rank'] = stage10_info(kw, m['status'])
    c['s3'] = stage3_text(m)
    c['s9'] = stage9_text(kw, s8row)
    if c['disp'] == 'CLUSTERED':
        cl_ = byid[c['cluster']]
        cin = {cl_['primary_intent']} | set(cl_['secondary_intents']) | {M, U}
        verified = c['intent_src'] in ('STAGE8_SERP_VALIDATED', 'STAGE5_ANALYST_INTENT', 'STAGE11_TEXT_CUE', 'STAGE5_AND_DATAFORSEO_AGREE')
        c['intent_fit'] = 'IN_CLUSTER_INTENTS' if c['intent'] in cin else ('OUTSIDE_CLUSTER_INTENTS' if verified else 'INTENT_UNVERIFIED')
        if c['intent'] not in cin and not verified:
            c['intent_fit'] = 'INTENT_UNVERIFIED'
        secondary = (c['strength'] == 'L') or (m['status'] == 'AMBIGUOUS') or (c['intent_fit'] == 'OUTSIDE_CLUSTER_INTENTS')
        c['assign'] = 'SECONDARY_CLUSTER' if secondary else 'PRIMARY_CLUSTER'
        # evidence
        if s8row:
            vi = s8row['validated_intent'].upper()
            if c.get('peer_max') is not None and c['peer_max'] >= 3:
                c['ev'] = 'HIGH'
                c['ev_txt'] = f"Stage 8 SERP similarity confirmed: shares >=3 top-10 URLs with {', '.join(repr(p) for p in c['peer_best'])}"
            elif vi not in ('UNCLEAR', 'MIXED') and c['intent_fit'] != 'OUTSIDE_CLUSTER_INTENTS':
                c['ev'] = 'HIGH'
                c['ev_txt'] = f"Stage 8 validated ({vi}, {s8row['dominant_serp_page_type']}) is consistent with cluster intent; no same-cluster validated peer with >=3 shared URLs" if c.get('peer_max') is not None else f"Stage 8 validated ({vi}, {s8row['dominant_serp_page_type']}) is consistent with cluster intent; sole validated member"
            else:
                c['ev'] = 'MEDIUM'
                c['ev_txt'] = f"Stage 8 validated but SERP intent {vi}/{s8row['dominant_serp_page_type']} is unclear or differs; placed on semantics"
        else:
            c['ev'] = 'MEDIUM' if c['strength'] == 'S' else 'LOW'
            c['ev_txt'] = 'No direct SERP evidence (not Stage 8 validated); ' + ('strong semantic + intent rule match' if c['strength'] == 'S' else 'topic/lexical-only rule match')
        if m['status'] == 'AMBIGUOUS' and not s8row:
            c['ev'] = 'LOW'; c['ev_txt'] += '; Stage 7 status AMBIGUOUS clustered only because the cluster rule is topic-strong'
        if c['ev'] == 'HIGH' and c['assign'] == 'PRIMARY_CLUSTER':
            c['conf'] = 'HIGH'
        elif c['ev'] == 'HIGH' or (c['ev'] == 'MEDIUM' and c['assign'] == 'PRIMARY_CLUSTER'):
            c['conf'] = 'MEDIUM'
        else:
            c['conf'] = 'LOW'
    else:
        c['intent_fit'] = 'NOT_APPLICABLE'
        c['assign'] = c['disp']
        if s8row:
            c['ev'] = 'HIGH' if c['disp'] in ('NOISE', 'COMPETITOR_BRAND') else 'NOT_APPLICABLE'
            c['ev_txt'] = f"Stage 8 SERP observed ({s8row['validated_intent']}/{s8row['dominant_serp_page_type']}); disposition {c['disp']} {c['basis']}"
        else:
            c['ev'] = 'NOT_APPLICABLE'; c['ev_txt'] = c['basis']
        c['conf'] = 'NOT_APPLICABLE'

# secondary-cluster tag for reader: other clusters whose rules also fired
for c in rows:
    c['others_txt'] = ';'.join(c.get('others', []))

# ------------------------------------------------------------------ keyword map rows
def short_pat(p):
    p = p.replace(rules.LG, '<LG>')
    return p if len(p) < 100 else p[:97] + '...'

kmap = []
for c in rows:
    m = c['m']; kw = c['keyword']; s8row = c['s8']
    cid = cname = parent = ''
    if c['disp'] == 'CLUSTERED':
        cl_ = byid[c['cluster']]
        cid, cname, parent = cl_['id'], cl_['name'], cl_['parent']
        reason = f"Rule match ({short_pat(c['matched'])}) -> cluster subject/need; intent {c['intent']} via {c['intent_src']}; {c['ev_txt']}"
    elif c['disp'] == 'NOISE':
        reason = c['basis']
        cid, cname, parent = 'NOISE', 'NOISE', 'NOISE'
    elif c['disp'] == 'COMPETITOR_BRAND':
        reason = c['basis'] + (f" ({c['brand']})" if c['brand'] else '')
        cid, cname, parent = 'COMPETITOR_BRAND', 'COMPETITOR_BRAND', 'COMPETITOR_BRAND'
    else:
        reason = c['basis']
        cid, cname, parent = 'UNCLUSTERED_REVIEW', 'UNCLUSTERED_REVIEW', 'UNCLUSTERED_REVIEW'
    stg5 = m['stage5_relevance_class'] if m['stage5_relevance_class'] != 'UNKNOWN' else 'NOT_CLASSIFIED_BY_STAGE5 (Stage 6-only or Stage 3-only keyword)'
    kmap.append({
        'keyword': kw, 'cluster_assignment_type': c['assign'], 'cluster_id': cid, 'cluster_name': cname, 'parent_topic': parent,
        'business_area': c['area'], 'business_area_basis': c['area_basis'],
        'search_intent': c['intent'], 'intent_source': c['intent_src'], 'intent_fit_to_cluster': c['intent_fit'],
        'stage5_relevance': stg5, 'stage7_status': m['status'], 'stage7_source_stages': m['source_stages'],
        'search_volume': m['search_volume'], 'cpc': m['cpc'], 'competition': m['competition'], 'keyword_difficulty': m['keyword_difficulty'],
        'dataforseo_intent_label': m['intent'],
        'Stage3_current_ranking': c['s3'],
        'Stage8_validated': 'YES' if s8row else 'NO',
        'Stage8_validated_intent': s8row['validated_intent'] if s8row else 'NOT_VALIDATED',
        'Stage8_dominant_page_type': s8row['dominant_serp_page_type'] if s8row else 'NOT_VALIDATED',
        'Stage9_competitor_presence': c['s9'],
        'Stage10_existing_content_match': c['s10_text'],
        'clustering_evidence_level': c['ev'], 'clustering_reason': reason,
        'cluster_confidence': c['conf'],
        'stage11_status_override': ('YES: Stage 7 %s -> Stage 11 %s' % (m['status'], c['disp'])) if (
            (c['basis'].startswith('STAGE11') ) or (m['status'] == 'INCLUDE' and c['disp'] == 'UNCLUSTERED_REVIEW') or (m['status'] == 'AMBIGUOUS' and c['disp'] == 'CLUSTERED')) else 'NO',
        'other_matching_cluster_ids': c['others_txt'],
    })

# ------------------------------------------------------------------ cluster registry
# Stage 10 documented page-pair classifications (rel paths)
DOC_PAIRS = {}
for r in overlaps10:
    for a_ in [u.strip() for u in re.split(r'[;,]', r['url_a']) if u.strip()]:
        for b_ in [u.strip() for u in re.split(r'[;,]', r['url_b']) if u.strip()]:
            DOC_PAIRS[frozenset((relpath(a_), relpath(b_)))] = (r['overlap_id'], r['classification'])

def cluster_existing_rel(g):
    """Part 7 classification from Stage 10 links (topic string-match + Stage 3 rankings)."""
    matched = [x for x in g if x['s10_urls']]
    ranking = [x for x in g if x['s10_rank']]
    n = len(matched)
    urlc = C.Counter(u for x in matched for u in x['s10_urls'])
    thr = max(2 if len(g) > 3 else 1, math.ceil(0.25 * n)) if n else 1
    rank_urls = {relpath(x['m']['stage3_ranking_url']) for x in ranking}
    sig = sorted({u for u, k in urlc.items() if k >= thr} | rank_urls)
    doc = []
    for a_, b_ in itertools.combinations(sig, 2):
        d = DOC_PAIRS.get(frozenset((a_, b_)))
        if d:
            doc.append(d)
    all_distinct = len(sig) >= 2 and len(doc) == len(list(itertools.combinations(sig, 2))) and all(d[1] == 'DISTINCT' for d in doc)
    if len(sig) >= 2 and not all_distinct:
        rel = 'MULTIPLE_EXISTING_CONTENT_POSSIBLE_OVERLAP'
    elif len(sig) >= 1:
        rel = 'STRONG_EXISTING_CONTENT_SIGNAL' if (len(ranking) >= 2 and rank_urls <= set(sig) and len(sig) == 1) else 'EXISTING_CONTENT_SIGNAL'
    elif n:
        rel = 'INSUFFICIENT_EVIDENCE'
    else:
        rel = 'INSUFFICIENT_EVIDENCE' if len(g) <= 2 else 'NO_EXISTING_CONTENT_EVIDENCE'
    return rel, sorted(urlc), sig, len(matched), len(ranking), urlc, sorted({f"{d[0]}:{d[1]}" for d in doc})

registry = []
CLUSTER_URLS = {}
CLUSTER_URLC = {}
for cid in sorted(members):
    cl_ = byid[cid]; g = members[cid]
    v = [x for x in g if x['s8']]
    pair_ov = [ov(val_key(a), val_key(b)) for a, b in itertools.combinations(v, 2)]
    ev_counts = C.Counter(x['ev'] for x in g)
    if len(v) >= 2 and pair_ov and max(pair_ov) >= 3:
        ev = 'HIGH'
    elif len(v) >= 1 or (ev_counts['MEDIUM'] + ev_counts['HIGH']) >= 0.5 * len(g):
        ev = 'MEDIUM'
    else:
        ev = 'LOW'
    rel, urls, sig, matched_n, rank_n, urlc, docs = cluster_existing_rel(g)
    CLUSTER_URLS[cid] = sig; CLUSTER_URLC[cid] = urlc
    vols = [(vol_num(x['m']), x['keyword']) for x in g if vol_num(x['m']) is not None]
    head = max(vols)[1] if vols else ''
    hv = max(vols)[0] if vols else ''
    idist = C.Counter(x['intent'] for x in g)
    dom_types = C.Counter(x['s8']['dominant_serp_page_type'] for x in v)
    comp = C.Counter()
    for x in v:
        for r in comp_by_kw.get(val_key(x), []):
            if r['business_relevance'] == 'RELEVANT':
                comp[r['domain']] += 1
    notes = cl_['notes']
    extra = []
    if len(g) == 1:
        extra.append('SINGLETON: only one keyword in the master database maps to this subject/need')
    if v and len(v) >= 2 and pair_ov:
        extra.append(f"Stage 8 pairwise URL overlap among {len(v)} validated members: mean {sum(pair_ov)/len(pair_ov):.1f}, min {min(pair_ov)}, max {max(pair_ov)}")
    n_amb = sum(1 for x in g if x['m']['status'] == 'AMBIGUOUS')
    if n_amb:
        extra.append(f"{n_amb} Stage 7 AMBIGUOUS keyword(s) clustered on strong topical rule or Stage 8 evidence")
    registry.append({
        'cluster_id': cid, 'cluster_name': cl_['name'], 'parent_topic': cl_['parent'], 'business_area': cl_['area'],
        'primary_intent': cl_['primary_intent'], 'secondary_intents': ';'.join(cl_['secondary_intents']) or 'NONE',
        'evidence_level': ev, 'cluster_definition': cl_['definition'],
        'keyword_count': len(g), 'validated_keyword_count': len(v),
        'existing_HOD_content_count': len(sig), 'current_HOD_ranking_keyword_count': sum(1 for x in g if x['s3'] != 'NO'),
        'notes': ' | '.join([n_ for n_ in [notes] + extra if n_]),
        'existing_content_relationship': rel,
        'existing_HOD_content_urls_linked': '; '.join(sig),
        'existing_HOD_content_urls_isolated_matches_only': '; '.join(u for u in urls if u not in sig),
        'existing_content_keyword_match_count': matched_n,
        'stage10_documented_page_pair_classifications': '; '.join(docs) or 'NONE',
        'primary_assignment_count': sum(1 for x in g if x['assign'] == 'PRIMARY_CLUSTER'),
        'secondary_assignment_count': sum(1 for x in g if x['assign'] == 'SECONDARY_CLUSTER'),
        'head_keyword_by_volume': head, 'max_keyword_volume': hv,
        'keyword_volume_sum_raw_not_a_demand_estimate': sum(v_[0] for v_ in vols),
        'intent_distribution': '; '.join(f"{k}:{n_}" for k, n_ in idist.most_common()),
        'stage8_dominant_page_types': '; '.join(f"{k}:{n_}" for k, n_ in dom_types.most_common()) or 'NO_VALIDATED_MEMBERS',
        'stage9_top_competitor_domains': '; '.join(f"{d}({n_})" for d, n_ in comp.most_common(5)) or 'NOT_ASSESSED',
        'stage7_ambiguous_member_count': n_amb,
        'cluster_size_flag': 'SINGLETON' if len(g) == 1 else ('SMALL(2-3)' if len(g) <= 3 else ('LARGE(30+)' if len(g) >= 30 else 'NORMAL')),
    })
regmap = {r['cluster_id']: r for r in registry}

# ------------------------------------------------------------------ cross-cluster SERP evidence + relationships
def cross_ov(a, b):
    va = [val_key(x) for x in members[a] if x['s8']]
    vb = [val_key(x) for x in members[b] if x['s8']]
    vals = [ov(x, y) for x in va for y in vb]
    return vals

relationships = []
seen = set()
def add_rel(a, b, rtype, basis, evidence, conf, cannib='NOT_DEMONSTRATED (no keyword has two HOD URLs ranking; Stage 3/10)'):
    key = tuple(sorted((a, b)))
    if key in seen:
        return
    seen.add(key)
    relationships.append({'relationship_id': f"REL-{len(relationships)+1:03d}", 'cluster_id': a, 'cluster_a': a, 'cluster_a_name': byid[a]['name'],
                          'cluster_b': b, 'cluster_b_name': byid[b]['name'], 'relationship_type': rtype, 'relationship_basis': basis,
                          'evidence': evidence, 'confidence': conf, 'cannibalization_evidence': cannib})

def serp_evidence(a, b):
    vals = cross_ov(a, b)
    if not vals:
        return None
    return dict(n=len(vals), mean=sum(vals) / len(vals), mx=max(vals), zero=sum(1 for x in vals if x == 0))

def classify_serp(ev):
    if ev['mean'] >= 4:
        return 'STRONG_OVERLAP'
    if ev['mx'] >= 3 or ev['mean'] >= 1.5:
        return 'POSSIBLE_OVERLAP'
    return 'RELATED_BUT_DISTINCT'

def serp_conf(ev):
    return 'HIGH' if ev['n'] >= 4 else ('MEDIUM' if ev['n'] >= 2 else 'LOW')

def serp_text(ev):
    return (f"Stage 8 cross-cluster SERP comparison: {ev['n']} validated keyword pair(s); mean shared top-10 URLs {ev['mean']:.1f}, max {ev['mx']}, "
            f"{ev['zero']} of {ev['n']} pairs share 0 URLs.")

# (1) SERP-derived pairs
cids = sorted(members)
for a, b in itertools.combinations(cids, 2):
    ev = serp_evidence(a, b)
    if ev and (ev['mx'] >= 3 or ev['mean'] >= 1.5):
        add_rel(a, b, classify_serp(ev), 'SERP_OVERLAP', serp_text(ev), serp_conf(ev))

# (2) curated semantic pairs (default type/evidence when SERP evidence does not exist; SERP result overrides type when it exists)
CURATED = [
    ("CL-001", "CL-002", "DISTINCT_INTENT", "Head-term SERP is retailer/brand-dominant (navigational/commercial); definitional queries are informational."),
    ("CL-001", "CL-005", "RELATED_BUT_DISTINCT", "Same subject; location modifier changes the need to local/regional purchase."),
    ("CL-001", "CL-006", "RELATED_BUT_DISTINCT", "Same subject; carat-specific shopping intent versus broad head terms."),
    ("CL-001", "CL-007", "DISTINCT_INTENT", "Consumer head terms versus B2B wholesale/supplier need (Stage 8 wholesale SERP lists suppliers)."),
    ("CL-001", "CL-008", "RELATED_BUT_DISTINCT", "Head terms versus price/affordability questions."),
    ("CL-009", "CL-012", "RELATED_BUT_DISTINCT", "Value/resale versus purchase-decision evaluation; overlapping searcher worry, different question."),
    ("CL-008", "CL-012", "RELATED_BUT_DISTINCT", "Price versus overall worth-it evaluation."),
    ("CL-011", "CL-012", "RELATED_BUT_DISTINCT", "Head-to-head comparison versus single-product pros/cons evaluation; no SERP evidence for the pros/cons phrasing."),
    ("CL-012", "CL-013", "RELATED_BUT_DISTINCT", "Ethics/environment is a sub-question of the worth-it decision but a distinct informational need."),
    ("CL-013", "CL-073", "POSSIBLE_OVERLAP", "Both answer 'ethical diamonds'; lab-grown ethics versus natural blood/conflict-free sourcing. No Stage 8 SERP for the lab-grown side."),
    ("CL-015", "CL-075", "POSSIBLE_OVERLAP", "'How are diamonds made' is ambiguous between lab manufacture and natural formation; no SERP evidence separates them."),
    ("CL-015", "CL-016", "RELATED_BUT_DISTINCT", "General process versus the CVD-vs-HPHT method comparison."),
    ("CL-016", "CL-017", "POSSIBLE_OVERLAP", "Method comparison versus single-method HPHT queries; Stage 8 shows partial URL sharing."),
    ("CL-016", "CL-018", "POSSIBLE_OVERLAP", "Method comparison versus single-method CVD queries; Stage 8 shows partial URL sharing."),
    ("CL-017", "CL-018", "RELATED_BUT_DISTINCT", "Sibling single-method clusters."),
    ("CL-020", "CL-021", "RELATED_BUT_DISTINCT", "Identification/detection versus tester-result questions."),
    ("CL-021", "CL-093", "POSSIBLE_OVERLAP", "Same searcher need (does the tester read it as diamond) for lab-grown versus moissanite; no validated lab-grown-tester keyword to compare SERPs."),
    ("CL-021", "CL-022", "RELATED_BUT_DISTINCT", "Result questions versus tester devices/methods."),
    ("CL-022", "CL-093", "RELATED_BUT_DISTINCT", "Tester devices versus moissanite tester-result questions."),
    ("CL-010", "CL-011", "RELATED_BUT_DISTINCT", "Authenticity ('is it real') versus comparison with natural."),
    ("CL-030", "CL-031", "POSSIBLE_OVERLAP", "GIA-vs-IGI comparison overlaps GIA-specific report queries; Stage 10 OV-01 documents topic overlap between the IGI blog and the GIA-vs-IGI education article."),
    ("CL-030", "CL-032", "POSSIBLE_OVERLAP", "GIA-vs-IGI comparison overlaps IGI-specific queries (Stage 10 OV-01)."),
    ("CL-031", "CL-032", "RELATED_BUT_DISTINCT", "Sibling lab-specific certification clusters."),
    ("CL-033", "CL-031", "POSSIBLE_OVERLAP", "General lab-grown certification overlaps GIA-specific queries (e.g. 'are lab grown diamonds GIA certified')."),
    ("CL-033", "CL-032", "POSSIBLE_OVERLAP", "General lab-grown certification overlaps IGI-specific queries."),
    ("CL-033", "CL-034", "RELATED_BUT_DISTINCT", "General certification versus other labs/lookup."),
    ("CL-033", "CL-023", "RELATED_BUT_DISTINCT", "Certification reports versus lab-grown grade/clarity charts."),
    ("CL-040", "CL-023", "RELATED_BUT_DISTINCT", "General grading scales versus lab-grown-specific grade/quality charts."),
    ("CL-041", "CL-044", "RELATED_BUT_DISTINCT", "Single-grade explainer versus adjacent-grade comparison."),
    ("CL-042", "CL-044", "RELATED_BUT_DISTINCT", "Single-grade explainer versus adjacent-grade comparison."),
    ("CL-043", "CL-044", "RELATED_BUT_DISTINCT", "Single-grade explainer versus adjacent-grade comparison."),
    ("CL-045", "CL-044", "RELATED_BUT_DISTINCT", "'Which clarity to buy' versus grade-to-grade comparison."),
    ("CL-047", "CL-048", "RELATED_BUT_DISTINCT", "Color-only versus color+clarity combination queries."),
    ("CL-041", "CL-046", "RELATED_BUT_DISTINCT", "SI grade explainer versus inclusion/eye-clean explainer."),
    ("CL-094", "CL-095", "POSSIBLE_OVERLAP", "Cubic zirconia is one diamond simulant; queries can share a SERP. No Stage 8 SERP for either."),
    ("CL-092", "CL-091", "RELATED_BUT_DISTINCT", "Moissanite compared with lab-grown diamond versus with diamond in general."),
    ("CL-090", "CL-091", "RELATED_BUT_DISTINCT", "Moissanite head/what-is queries versus moissanite-vs-diamond comparison."),
    ("CL-090", "CL-092", "RELATED_BUT_DISTINCT", "Moissanite head/what-is queries versus moissanite-vs-lab-grown comparison."),
    ("CL-090", "CL-093", "RELATED_BUT_DISTINCT", "Moissanite head queries versus tester-result questions."),
    ("CL-095", "CL-090", "RELATED_BUT_DISTINCT", "Simulant/alternative queries versus moissanite-specific queries."),
    ("CL-100", "CL-102", "POSSIBLE_OVERLAP", "Lab-grown sapphire appears in both the sapphire cluster and lab-created gemstones; no SERP evidence."),
    ("CL-101", "CL-102", "POSSIBLE_OVERLAP", "Lab-grown emerald appears in both the emerald cluster and lab-created gemstones; no SERP evidence."),
    ("CL-103", "CL-100", "RELATED_BUT_DISTINCT", "Other natural stones versus sapphire."),
    ("CL-104", "CL-105", "RELATED_BUT_DISTINCT", "Morganite rings (CATEGORY SERP) versus other coloured-gem rings."),
    ("CL-110", "CL-112", "RELATED_BUT_DISTINCT", "Gold karat choice versus general metal selection."),
    ("CL-111", "CL-112", "RELATED_BUT_DISTINCT", "Rhodium plating versus general metal selection."),
    ("CL-123", "CL-112", "RELATED_BUT_DISTINCT", "Mixed-metal ring shopping (CATEGORY SERP) versus metal-selection education."),
    ("CL-113", "CL-114", "RELATED_BUT_DISTINCT", "Tungsten/titanium wedding bands versus other alternative-material rings."),
    ("CL-113", "CL-112", "RELATED_BUT_DISTINCT", "Wedding-band metal suitability versus general metal selection."),
    ("CL-120", "CL-121", "DISTINCT_INTENT", "Side-stone category (CATEGORY SERP) versus setting-type education (EDITORIAL SERP)."),
    ("CL-121", "CL-125", "POSSIBLE_OVERLAP", "Stud-earring setting queries fit both the settings and stud-earring clusters; no SERP evidence."),
    ("CL-115", "CL-125", "RELATED_BUT_DISTINCT", "Water/wear care versus stud-earring shopping/sizing."),
    ("CL-060", "CL-065", "RELATED_BUT_DISTINCT", "'Diamond shape' versus broad 'types of diamonds' (sense unresolved)."),
    ("CL-061", "CL-062", "RELATED_BUT_DISTINCT", "Sibling shape clusters; asscher-vs-radiant comparison touches both."),
    ("CL-063", "CL-064", "RELATED_BUT_DISTINCT", "Marquise-oval hybrid versus general shape selection."),
    ("CL-070", "CL-071", "RELATED_BUT_DISTINCT", "Natural head terms versus rough/raw."),
    ("CL-070", "CL-011", "DISTINCT_INTENT", "Natural head/brand-dominant SERP versus lab-vs-natural comparison."),
    ("CL-085", "CL-009", "RELATED_BUT_DISTINCT", "General diamond investment versus lab-grown value/resale."),
    ("CL-086", "CL-009", "RELATED_BUT_DISTINCT", "Selling/pawning versus value/resale."),
    ("CL-080", "CL-082", "RELATED_BUT_DISTINCT", "Composition/structure versus hardness/durability."),
    ("CL-081", "CL-082", "RELATED_BUT_DISTINCT", "Heat resistance versus scratch/break durability."),
    ("CL-051", "CL-010", "RELATED_BUT_DISTINCT", "Fancy-colour authenticity ('are black diamonds real') versus lab-grown authenticity."),
    ("CL-124", "CL-122", "RELATED_BUT_DISTINCT", "Ring sizing versus other engagement-ring practicalities."),
]
for a, b, rtype, txt in CURATED:
    ev = serp_evidence(a, b)
    if ev:
        t = classify_serp(ev)
        add_rel(a, b, t, 'SEMANTIC+SERP_OVERLAP', txt + ' ' + serp_text(ev), serp_conf(ev))
    else:
        add_rel(a, b, rtype, 'SEMANTIC', txt + ' No cross-cluster Stage 8 SERP comparison is possible (one or both clusters have no validated keyword).', 'LOW' if rtype in ('POSSIBLE_OVERLAP',) else 'MEDIUM')

# SERP-derived rows that were added before curated ones keep SERP basis; enrich them with curated text if any
cur_txt = {tuple(sorted((a, b))): txt for a, b, _, txt in CURATED}
for r in relationships:
    k = tuple(sorted((r['cluster_a'], r['cluster_b'])))
    if r['relationship_basis'] == 'SERP_OVERLAP' and k in cur_txt:
        r['relationship_basis'] = 'SEMANTIC+SERP_OVERLAP'; r['evidence'] = cur_txt[k] + ' ' + r['evidence']

# (3) shared existing HOD content (Part 8): pairs of clusters each with >=3 members matched to the same HOD URL
url_clusters = C.defaultdict(list)
for cid, urlc in CLUSTER_URLC.items():
    for u, k in urlc.items():
        if k >= 3:
            url_clusters[u].append((cid, k))
shared_pairs = C.defaultdict(list)
for u, lst in url_clusters.items():
    for (a, ka), (b, kb) in itertools.combinations(sorted(lst), 2):
        shared_pairs[(a, b)].append((u, ka, kb))
n_shared_added = 0
for (a, b), lst in sorted(shared_pairs.items()):
    key = tuple(sorted((a, b)))
    txt = 'Stage 10 topic string-match links members of both clusters to the same existing HOD URL(s): ' + '; '.join(f"{u} ({ka} vs {kb} keywords)" for u, ka, kb in lst) + '. This is topic overlap only, not proven cannibalization.'
    if key in seen:
        for r in relationships:
            if tuple(sorted((r['cluster_a'], r['cluster_b']))) == key:
                r['evidence'] += ' | ' + txt
                r['relationship_basis'] += '+SHARED_EXISTING_CONTENT'
        continue
    same_parent = byid[a]['parent'] == byid[b]['parent']
    if same_parent:
        add_rel(a, b, 'RELATED_BUT_DISTINCT', 'SHARED_EXISTING_CONTENT', txt, 'LOW')
        n_shared_added += 1

# ------------------------------------------------------------------ QC inspection table
inspect_rows = []
def add_inspect(group, c):
    m = c['m']
    inspect_rows.append({'inspection_group': group, 'keyword': c['keyword'], 'search_volume': m['search_volume'], 'stage7_status': m['status'],
                         'disposition': c['disp'], 'cluster_id': c['cluster'] or '', 'cluster_name': byid[c['cluster']]['name'] if c['cluster'] else '',
                         'search_intent': c['intent'], 'stage8_validated': 'YES' if c['s8'] else 'NO', 'stage3_ranking': c['s3'],
                         'basis': c.get('matched', c['basis'])[:120]})
by_kw = {c['keyword']: c for c in rows}
top_vol = sorted([c for c in rows if vol_num(c['m']) is not None], key=lambda c: -vol_num(c['m']))[:60]
for c in top_vol: add_inspect('HIGH_VOLUME_TOP60', c)
for c in rows:
    if c['s3'] != 'NO': add_inspect('STAGE3_RANKING_28', c)
for c in rows:
    if c['s8']: add_inspect('STAGE8_VALIDATED_100', c)
for c in rows:
    if c['m']['stage5_seed_eligibility'] == 'YES': add_inspect('STAGE5_STRATEGIC_SEED_55', c)
COMM = re.compile(r'\b(engagement rings?|wedding bands?|earrings?|studs?|necklaces?|pendants?|bracelets?|fine jewel|bespoke|custom jewel|rings?)\b')
for c in rows:
    if COMM.search(c['kn']) and c['m']['status'] in ('INCLUDE', 'AMBIGUOUS') and c['disp'] != 'NOISE':
        add_inspect('COMMERCIAL_CATEGORY_TERMS', c)
for c in rows:
    if c['disp'] == 'UNCLUSTERED_REVIEW' or c['m']['status'] == 'AMBIGUOUS':
        add_inspect('AMBIGUOUS_OR_REVIEW', c)

# ------------------------------------------------------------------ write CSV outputs
def write_csv(path, rows_, cols=None):
    cols = cols or list(rows_[0].keys())
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows_)

def build_all():
    os.makedirs(OUT, exist_ok=True)
    write_csv(OUT + '11_cluster_registry.csv', registry)
    write_csv(OUT + '11_keyword_cluster_map.csv', sorted(kmap, key=lambda r: (r['cluster_id'] in ('NOISE', 'COMPETITOR_BRAND', 'UNCLUSTERED_REVIEW'), r['cluster_id'], -(vol_num({'search_volume': r['search_volume']}) or -1), r['keyword'])))
    write_csv(OUT + '11_cluster_relationships.csv', relationships)
    write_csv(OUT + '11_cluster_qc_inspection.csv', inspect_rows)

if __name__ == '__main__':
    build_all()
    print('rows', len(rows), C.Counter(r['assign'] for r in rows))
    print('clusters', len(registry), 'relationships', len(relationships), 'shared-content rows added', n_shared_added)
    print(C.Counter(r['evidence_level'] for r in registry), C.Counter(r['existing_content_relationship'] for r in registry))
