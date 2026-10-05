#!/usr/bin/env python3
"""Stage 16 QC — internal linking architecture. Exits non-zero on any failure. Local-only."""
import csv, collections, hashlib, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = lambda *a: os.path.join(ROOT, *a)
rd = lambda p: list(csv.DictReader(open(P(p), newline='', encoding='utf-8')))
results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))


LM = rd('architecture/16_internal_link_map.csv')
PR = rd('architecture/16_page_link_requirements.csv')
AN = rd('architecture/16_anchor_strategy.csv')
OC = rd('architecture/16_orphan_and_connectivity.csv')
REG = {r['target_id']: r for r in rd('architecture/15_target_page_registry.csv')}
KMAP = rd('architecture/15_keyword_url_map.csv')
PROT = rd('content-strategy/15_ranking_equity_protection.csv')
ARCH = {r['topic_id']: r for r in rd('architecture/14_education_architecture.csv')}
HIER = rd('architecture/14_education_hierarchy.csv')
PAGES = {r['page_id']: r for r in PR}
STRUCT = {'GLOBAL_NAV', 'PRIMARY_NAV', 'CATEGORY_NAV', 'BREADCRUMB', 'FOOTER'}
CTX = {'CONTEXTUAL', 'RELATED_CONTENT', 'EDITORIAL', 'EDUCATIONAL_CTA', 'COMMERCIAL_CTA', 'PRODUCT_RECOMMENDATION'}
LINK_TYPES = STRUCT | CTX
ANCHOR_TYPES = {'BRANDED', 'PARTIAL_MATCH', 'DESCRIPTIVE', 'NATURAL_LANGUAGE', 'EXACT_MATCH_ALLOWED', 'NAVIGATIONAL'}
PRIOS = {'REQUIRED': 'YES', 'RECOMMENDED': 'NO', 'OPTIONAL': 'NO', 'CONDITIONAL': 'CONDITIONAL'}
COND_COP = {'CONDITIONAL', 'EXISTING_CONDITIONAL'}
norm = lambda s: re.sub(r'\s+', ' ', re.sub(r"[^a-z0-9/ ]", ' ', s.lower().replace('-', ' '))).strip()

# 0. schema
check('00 link map columns', list(LM[0].keys()) == ['source_page_id', 'source_page_type', 'source_url_or_expression', 'source_business_area', 'target_page_id',
      'target_page_type', 'target_url_or_expression', 'target_business_area', 'link_type', 'relationship_type', 'priority', 'required_at_launch', 'anchor_type',
      'recommended_anchor', 'anchor_variants', 'context_reason', 'ranking_equity_protection', 'cannibalization_risk', 'notes'])
check('00 page requirements columns', list(PR[0].keys()) == ['page_id', 'page_type', 'business_area', 'current_or_proposed', 'incoming_required', 'incoming_recommended',
      'outgoing_required', 'outgoing_recommended', 'parent_page_id', 'child_page_ids', 'related_page_ids', 'ranking_protected', 'orphan_status',
      'launch_linking_requirement', 'notes'])
check('00 anchor strategy columns', list(AN[0].keys()) == ['target_page_id', 'target_page_type', 'primary_topic', 'anchor_type', 'recommended_anchor',
      'usage_guidance', 'avoid_anchor', 'reason'])
check('00 connectivity columns', list(OC[0].keys()) == ['page_id', 'page_type', 'current_or_proposed', 'incoming_link_count', 'contextual_incoming_count',
      'structural_incoming_count', 'outgoing_link_count', 'status', 'risk', 'required_fix', 'notes'])
check('00 link_type / anchor_type / priority vocabularies', all(r['link_type'] in LINK_TYPES and r['anchor_type'] in ANCHOR_TYPES
      and PRIOS.get(r['priority']) == r['required_at_launch'] for r in LM))
check('00 every contextual row records why it exists', all(r['context_reason'].strip() for r in LM if r['link_type'] in CTX))

# 1. every Stage 15 target page represented
check('01 every Stage 15 target page is in page requirements', set(REG) <= set(PAGES), sorted(set(REG) - set(PAGES)))
check('01 every Stage 15 target page is in connectivity file', set(REG) <= {r['page_id'] for r in OC})

# 2. no unknown page IDs
ids = {r['source_page_id'] for r in LM} | {r['target_page_id'] for r in LM} | {r['target_page_id'] for r in AN} | {r['page_id'] for r in OC}
check('02 no source/target row points to an unknown page ID', ids <= set(PAGES), sorted(ids - set(PAGES)))
DEFERRED = {t for t, a in ARCH.items() if a['architecture_status'] == 'DEFERRED'} | {'COM-NAT-HUB'}
check('02 no link to or from a DEFERRED page', not (ids & DEFERRED), sorted(ids & DEFERRED))

# 3. no new keyword owner
check('03 Stage 16 files contain no keyword-ownership column', not any('keyword' in c for f in (LM, PR, AN, OC) for c in f[0].keys()))
nonreg_claims = [r['page_id'] for r in PR if r['page_id'] not in REG and 'Stage 15 keyword owner' in r['notes']]
reg_ok = all(PAGES[t]['notes'].startswith('Stage 15 keyword owner') for t in REG)
check('03 only Stage 15 registry pages are labelled keyword owners', not nonreg_claims and reg_ok, nonreg_claims)
check('03 anchor strategy flags non-owning pages as such', all(a['primary_topic'].startswith('No keyword ownership') for a in AN if a['target_page_id'] not in REG))

# 4-5. ranking protection
prot_urls = collections.Counter(p['ranking_url'] for p in PROT)
url2pid = {r['existing_url']: t for t, r in REG.items() if r['existing_or_proposed'] == 'EXISTING'}
check('04 all 28 Stage 3 ranking keywords map to a protected page', len(PROT) == 28 and all(p['ranking_url'] in url2pid for p in PROT))
prot_pages = {url2pid[u]: n for u, n in prot_urls.items()}
check('04 6 ranking URLs flagged ranking_protected with correct counts',
      len(prot_pages) == 6 and all(PAGES[p]['ranking_protected'].startswith(f'YES ({n} ') for p, n in prot_pages.items())
      and all(PAGES[p]['ranking_protected'] == 'NO' for p in PAGES if p not in prot_pages))
bad = [(r['source_page_id'], r['target_page_id']) for r in LM if r['target_page_id'] in prot_pages
       and r['target_url_or_expression'] != REG[r['target_page_id']]['existing_url']]
check('05 every link to a protected page uses its current ranking URL (no move)', not bad, bad)
check('05 protected rows are labelled', all(r['ranking_equity_protection'].startswith('SUPPORTS_PROTECTED') == (r['target_page_id'] in prot_pages) for r in LM))
mv = [r for r in LM if re.search(r'\b(redirect|301|move (it|this|the url)|change the (url|slug))\b', (r['notes'] + r['context_reason']).lower())]
check('05 no link row recommends a redirect, move or slug change', not mv, [(r['source_page_id'], r['target_page_id']) for r in mv])

# 6. cvd/hpht diamond tester
tester = 'cvd/hpht diamond tester'
tp = [p for p in PROT if p['keyword'] == tester]
in_anchor = [r for r in LM if tester in (r['recommended_anchor'] + ' ' + r['anchor_variants']).lower()] + \
            [a for a in AN if tester in a['recommended_anchor'].lower()]
check('06 cvd/hpht diamond tester stays excluded (Stage 15) and is never an anchor',
      len(tp) == 1 and tp[0]['mapped_target_id'].startswith('(none') and tp[0]['action'] == 'KEEP_EXISTING_URL_NOT_TARGETED' and not in_anchor
      and any(tester in a['avoid_anchor'] for a in AN))

# 7. URL_PENDING not invented
pend = {t for t, r in REG.items() if r['existing_or_proposed'] == 'PROPOSED' and r['proposed_url'] == 'URL_PENDING'}
badu = [r for r in LM for side in ('source', 'target') if r[f'{side}_page_id'] in pend and r[f'{side}_url_or_expression'] != 'URL_PENDING']
check('07 URL_PENDING pages carry URL_PENDING (no invented URL)', not badu and len(pend) == 9, len(badu))
exp = {t: (r['existing_url'] if r['existing_or_proposed'] == 'EXISTING' else r['proposed_url']) for t, r in REG.items()}
badx = [r['target_page_id'] for r in LM if r['target_page_id'] in exp and r['target_url_or_expression'] != exp[r['target_page_id']]]
check('07 registry URLs match Stage 15 exactly (current URL or Stage 15 expression)', not badx, sorted(set(badx)))
check('07 no /education/ URL invented for a non-registry page', not [p for p in PAGES if p not in REG and '/education/' in p and p != 'EDU-ROOT'])

# 8. Education not a commercial substitute
COMREL = {'CATEGORY_TO_SUBCATEGORY', 'CATEGORY_TO_PRODUCT', 'PRODUCT_TO_CATEGORY', 'BLOG_TO_CATEGORY', 'FAQ_TO_CATEGORY', 'EDUCATION_TO_CATEGORY', 'HOME_TO_CATEGORY'}
b8 = [r for r in LM if r['target_page_id'].startswith('EDU') and (r['relationship_type'] in COMREL or r['link_type'] == 'COMMERCIAL_CTA')]
check('08 no commercial relationship or commercial CTA targets an Education page', not b8, [(r['source_page_id'], r['target_page_id']) for r in b8])
shopw = [r for r in LM if r['target_page_id'].startswith('EDU') and re.search(r'\b(shop|buy|browse)\b', r['recommended_anchor'].lower())]
check('08 no shopping-verb anchor points to Education', not shopw, [(r['source_page_id'], r['target_page_id']) for r in shopw])
check('08 Education pages are never parents of commercial pages', not [r for r in LM if r['link_type'] == 'BREADCRUMB' and r['source_page_id'].startswith('COM') and r['target_page_id'].startswith('EDU')])

# 9. Blog not an Education owner
blog = [p for p in PAGES if PAGES[p]['page_type'] in ('BLOG_HUB', 'BLOG_POST_TEMPLATE')]
check('09 no Blog page is a Stage 15 owner', not (set(blog) & set(REG)))
check('09 no REQUIRED Education -> Blog link (optional/conditional only)', not [r for r in LM if r['source_page_id'].startswith('EDU') and r['target_page_id'].startswith('BLOG') and r['priority'] == 'REQUIRED'])
ownedk = {norm(k['keyword']) for k in KMAP if k['target_id'].startswith('EDU')}
b9 = [r for r in LM if r['target_page_id'].startswith('BLOG') and norm(r['recommended_anchor']) in ownedk]
check('09 no Education-owned keyword used as an anchor to a Blog page', not b9)
check('09 every concept-bearing Blog template links to at least one Education owner',
      all(any(r['source_page_id'] == b and r['target_page_id'].startswith('EDU') for r in LM) for b in ['BLOG-CRAFT', 'BLOG-STYLE', 'BLOG-GIFTS', 'BLOG-LAUNCH', 'BLOG-INDUSTRY']))

# 10. cannibalization: anchors vs Stage 15 ownership
owner = {}
for k in KMAP:
    n = norm(k['keyword'])
    if k['target_id']:
        o = k['target_id']
    elif k['cluster_id'] == 'CL-001':
        o = 'COM-LG-HUB'
    elif k['stage14_topic_id']:
        o = k['stage14_topic_id']
    else:
        o = 'NO_HOD_TARGET:' + k['mapping_disposition']
    owner.setdefault(n, set()).add(o)
conf = []
for r in LM:
    for a in [r['recommended_anchor']] + [v for v in r['anchor_variants'].split(' | ') if v]:
        n = norm(a)
        if n in owner and r['target_page_id'] not in owner[n]:
            conf.append((r['source_page_id'], r['target_page_id'], a, sorted(owner[n])))
check('10 no anchor equals a Stage 15 keyword owned/held by a different page', not conf, conf[:5])
ex = [r for r in LM if r['anchor_type'] == 'EXACT_MATCH_ALLOWED']
exbad = [(r['target_page_id'], r['recommended_anchor']) for r in ex if r['target_page_id'] not in owner.get(norm(r['recommended_anchor']), set())]
check('10 EXACT_MATCH anchors are keywords the target already owns in Stage 15', not exbad and ex, exbad)
same = collections.defaultdict(set)
for r in LM:
    if r['link_type'] in CTX and not r['recommended_anchor'].startswith('('):
        same[(r['source_page_id'], norm(r['recommended_anchor']))].add(r['target_page_id'])
check('10 no source uses one anchor for two different targets', all(len(v) == 1 for v in same.values()), [k for k, v in same.items() if len(v) > 1])
FLAG15 = [('EDU-LG-01', 'EDU-LG-02'), ('EDU-LG-02', 'EDU-LG-05'), ('EDU-LG-00', 'EDU-LG-03'), ('EDU-4C-00', 'EDU-4C-01'), ('EDU-CERT-00', 'EDU-CERT-01'),
          ('EDU-4C-06', 'EDU-SHP-00'), ('EDU-LG-08', 'EDU-LG-01'), ('EDU-LG-09', 'EDU-LG-01'), ('EDU-4C-02', 'EDU-4C-01'), ('EDU-4C-03', 'EDU-4C-01'),
          ('EDU-LG-00', 'COM-LG-HUB')]
fr = [r for r in LM if frozenset([r['source_page_id'], r['target_page_id']]) in {frozenset(p) for p in FLAG15}]
check('10 every row between Stage 15 flagged pairs carries the risk and a guard', fr and all(r['cannibalization_risk'] not in ('NONE_IDENTIFIED', 'NONE (structural)') and 'Guard:' in r['notes'] for r in fr))
headlg = [r for r in LM if norm(r['recommended_anchor']) in ('lab grown diamonds', 'lab diamonds') and r['target_page_id'] != 'COM-LG-HUB']
check('10 bare lab-grown head-term anchor only ever points to the conditional commercial hub', not headlg)
check('10 no anchor uses the natural commercial head term', not [r for r in LM if norm(r['recommended_anchor']) == 'natural diamonds'])

# 11. parent/child agree with Stage 14
H2P = {h['hierarchy_id']: h['topic_or_pillar_id'] for h in HIER if h['node_type'] == 'HUB' and h['topic_or_pillar_id']}
par = {}
for h in HIER:
    t = h['topic_or_pillar_id']
    if h['node_type'] == 'TOPIC' and t:
        par[t] = 'EDU-ROOT' if (h['level'] == 'L1_PILLAR' or h['parent_id'] == 'H-00') else H2P[h['parent_id']]
edu = [p for p in PAGES if p.startswith('EDU-') and p != 'EDU-ROOT']
check('11 parent_page_id of every Education page equals its Stage 14 parent', all(PAGES[p]['parent_page_id'] == par[p] for p in edu),
      [p for p in edu if PAGES[p]['parent_page_id'] != par.get(p)])
bc = [r for r in LM if r['source_page_id'] in par and r['link_type'] == 'BREADCRUMB']
check('11 every Education breadcrumb points to its Stage 14 parent', all(r['target_page_id'] == par[r['source_page_id']] for r in bc) and len(bc) == len(edu))
h2c = [r for r in LM if r['relationship_type'] == 'HUB_TO_CHILD' and r['target_page_id'] in par]
check('11 every Education HUB_TO_CHILD row comes from the Stage 14 parent', all(r['source_page_id'] == par[r['target_page_id']] for r in h2c)
      and {r['target_page_id'] for r in h2c} == set(edu))
check('11 no Education page is linked as a child of a Stage 14 sibling (transitional rows only from EDU-ROOT/BLOG-HUB)',
      all(r['source_page_id'] in ('EDU-ROOT', 'BLOG-HUB') for r in LM if r['relationship_type'] == 'HUB_TO_CHILD_TRANSITIONAL'))

# 12. every proposed target has a launch requirement
prop = [p for p in PAGES if PAGES[p]['current_or_proposed'] in ('PROPOSED', 'PROPOSED_PROVISIONAL', 'PROPOSED_TEMPLATE', 'CONDITIONAL')]
check('12 every proposed/conditional page has a launch linking requirement and LINKING_REQUIREMENT_AT_LAUNCH status',
      all(PAGES[p]['launch_linking_requirement'] and PAGES[p]['orphan_status'] == 'LINKING_REQUIREMENT_AT_LAUNCH' for p in prop), len(prop))
check('12 no proposed page is called an orphan', not [r for r in OC if r['current_or_proposed'] not in ('EXISTING', 'EXISTING_GROUP', 'EXISTING_CONDITIONAL') and r['status'] in ('TRUE_ORPHAN', 'WEAKLY_CONNECTED', 'NAV_ONLY', 'WELL_CONNECTED')])
reqin = [p for p in PAGES if PAGES[p]['current_or_proposed'] in ('PROPOSED', 'PROPOSED_PROVISIONAL') and PAGES[p]['incoming_required'] == '0']
check('12 every proposed (non-conditional) page has >=1 REQUIRED incoming link', not reqin, reqin)
check('12 existing pages use only the four observed statuses', all(r['status'] in ('TRUE_ORPHAN', 'WEAKLY_CONNECTED', 'NAV_ONLY', 'WELL_CONNECTED')
      for r in OC if r['current_or_proposed'] in ('EXISTING', 'EXISTING_GROUP', 'EXISTING_CONDITIONAL')))

# 13-14. self links and duplicates
selfl = [r for r in LM if r['source_page_id'] == r['target_page_id']]
check('13 self-links only where structural template relationship is justified', all('SELF_TEMPLATE_JUSTIFIED' in r['notes'] and r['source_page_id'] == 'COM-PDP' for r in selfl), len(selfl))
pairs = collections.Counter((r['source_page_id'], r['target_page_id']) for r in LM)
check('14 no duplicate source -> target rows', all(v == 1 for v in pairs.values()), [k for k, v in pairs.items() if v > 1])

# 15. anchors not identical exact-match everywhere
exc = collections.Counter(r['target_page_id'] for r in ex)
check('15 at most one EXACT_MATCH source per target', all(v <= 1 for v in exc.values()), exc)
check('15 exact-match anchors are a small minority of contextual links', len(ex) <= 0.1 * len([r for r in LM if r['link_type'] in CTX]), len(ex))
div = []
for t in {r['target_page_id'] for r in LM}:
    cx = [norm(r['recommended_anchor']) for r in LM if r['target_page_id'] == t and r['link_type'] in CTX and not r['recommended_anchor'].startswith('(')]
    if len(cx) >= 3 and max(collections.Counter(cx).values()) > 2:
        div.append(t)
check('15 no target receives the same contextual anchor from more than two sources', not div, div)
check('15 no EXACT_MATCH in nav, footer, breadcrumb or template sources',
      not [r for r in ex if r['link_type'] in STRUCT or r['source_page_id'] in ('TPL-HEADER', 'TPL-FOOTER', 'COM-PDP')])

# 16. protected URLs have contextual support
ps = {}
for p in prot_pages:
    cx = [r for r in LM if r['target_page_id'] == p and r['link_type'] in CTX and r['priority'] != 'CONDITIONAL' and r['source_page_id'] != p]
    ps[p] = (len(cx), sum(r['priority'] == 'REQUIRED' for r in cx), sum(r['priority'] in ('REQUIRED', 'RECOMMENDED') for r in cx))
check('16 every protected ranking URL has >=2 contextual incoming recommendations (>=1 REQUIRED or RECOMMENDED)',
      all(v[0] >= 2 and v[2] >= 1 for v in ps.values()), ps)
check('16 every protected URL has anchor guidance with avoid list', all(any(a['target_page_id'] == p and a['avoid_anchor'] for a in AN) for p in prot_pages))

# 17. no unsupported business assumption
condp = {p for p in PAGES if PAGES[p]['current_or_proposed'] in COND_COP}
b17 = [r for r in LM if (r['source_page_id'] in condp or r['target_page_id'] in condp) and r['priority'] != 'CONDITIONAL']
check('17 every row touching a conditional page is CONDITIONAL', not b17, [(r['source_page_id'], r['target_page_id']) for r in b17])
biz = re.compile(r'business fact|ships with a grading report|offer both karats|natural offering|hub is approved|if hod|sell moissanite')
b17b = [r for r in LM if biz.search((r['context_reason'] + r['notes']).lower()) and r['priority'] != 'CONDITIONAL']
check('17 rows that depend on an unconfirmed business fact are CONDITIONAL', not b17b, [(r['source_page_id'], r['target_page_id']) for r in b17b])
check('17 no commercial link to moissanite, gemstone, natural, loose or wholesale pages', not [r for r in LM if re.search(r'moissanite|gemstone|loose|wholesale|natural', r['target_page_type'].lower() + r['target_business_area'].lower()) and r['target_page_id'].startswith('COM')])
check('17 Natural Education sends no commercial link', not [r for r in LM if r['source_page_id'].startswith('EDU-NAT') and r['target_page_id'].startswith('COM')])
check('17 Gemstones & Alternatives pages send no commercial link', not [r for r in LM if r['source_page_id'].startswith('EDU-GEM') and r['target_page_id'].startswith('COM')])

# 18-19. no live-site change, no API
src = open(P('architecture/scripts/build_16.py')).read() + open(__file__).read()
net = re.compile(r'^\s*(import|from)\s+(requests|urllib|http\.client|socket|aiohttp|httpx)\b', re.M)
check('18 Stage 16 scripts import no network library (no live-site request possible)', not net.search(src))
snap = json.load(open(P('architecture/scripts/16_upstream_checksums.json')))
raw_now = {os.path.relpath(os.path.join(d, f), ROOT) for d, _, fs in os.walk(P('dataforseo')) for f in fs if f != '.DS_Store'} | \
          {os.path.relpath(os.path.join(d, f), ROOT) for d, _, fs in os.walk(P('serp')) for f in fs if f != '.DS_Store'}
raw_snap = {p for p in snap if p.startswith('dataforseo/') or p.startswith('serp/')}
check('19 no new DataForSEO/SERP raw or processed file since Stage 15', raw_now == raw_snap, sorted(raw_now ^ raw_snap)[:5])
cl = rd('cost-log.csv')
s16 = [r for r in cl if 'Stage 16' in r['stage']]
check('19 cost-log Stage 16 row records $0.00 and 0 requests', len(s16) == 1 and float(s16[0]['actual_cost_usd']) == 0 and s16[0]['number_of_requests'] == '0')

# 20. upstream files unchanged
changed = [p for p, h in snap.items() if not os.path.exists(P(p)) or hashlib.sha256(open(P(p), 'rb').read()).hexdigest() != h]
check('20 all pre-Stage-16 files unchanged (sha256 snapshot)', not changed, changed)
s15 = json.load(open(P('architecture/scripts/15_upstream_checksums.json')))
ch15 = [p for p, h in s15.items() if os.path.exists(P(p)) and hashlib.sha256(open(P(p), 'rb').read()).hexdigest() != h]
check('20 files checksummed at Stage 15 still unchanged', not ch15, ch15)
stage_files = [p for p in snap if re.match(r'.*/(0[7-9]|1[0-5])_', p)]
check('20 Stage 7-15 outputs are part of the snapshot', len(stage_files) >= 40, len(stage_files))

# 20b. earlier-stage QC scripts (run as subprocesses; local only)
import subprocess
S16 = {'architecture/16_internal_link_map.csv', 'architecture/16_page_link_requirements.csv', 'architecture/16_orphan_and_connectivity.csv',
       'architecture/16_anchor_strategy.csv', 'architecture/16_stage_summary.md', 'architecture/16_linking_rules.md',
       'architecture/scripts/build_16.py', 'architecture/scripts/qc_16.py', 'architecture/scripts/16_upstream_checksums.json'}
o14 = subprocess.run([sys.executable, P('architecture/scripts/qc_14.py')], capture_output=True, text=True, cwd=ROOT)
check('20 qc_14 (incl. qc_12, qc_13) still passes', o14.returncode == 0, o14.stdout[-200:])
o15 = subprocess.run([sys.executable, P('architecture/scripts/qc_15.py')], capture_output=True, text=True, cwd=ROOT)
fails = [l for l in o15.stdout.splitlines() if l.startswith('FAIL')]
only_new = len(fails) == 1 and fails[0].startswith('FAIL 19 no live-site, site-inventory, raw-API or other files created/modified') and \
    set(re.findall(r"'([^']+)'", fails[0].split('->', 1)[1])) <= S16
check('20 qc_15 passes except its point-in-time "no new files" check, which flags only Stage 16 deliverables', only_new, fails)

# extra: density and connectivity
def dens(src_pred, tgt_pred, cap):
    c = collections.Counter(r['source_page_id'] for r in LM if src_pred(r['source_page_id']) and tgt_pred(r['target_page_id'])
                            and r['link_type'] in CTX and r['priority'] in ('REQUIRED', 'RECOMMENDED', 'OPTIONAL'))
    return {k: v for k, v in c.items() if v > cap}
check('X1 category pages: <=5 non-conditional Education links', not dens(lambda s: PAGES[s]['page_type'] in ('CATEGORY_HUB', 'CATEGORY', 'SUBCATEGORY'), lambda t: t.startswith('EDU'), 5))
check('X1 product pages: <=3 non-conditional Education links', not dens(lambda s: 'PRODUCT' in PAGES[s]['page_type'], lambda t: t.startswith('EDU'), 3))
check('X1 Education articles: <=10 non-conditional contextual outgoing links', not dens(lambda s: s.startswith('EDU') and s != 'EDU-ROOT', lambda t: True, 10))
below = [r['page_id'] for r in OC if 'BELOW' in r['notes'] and r['current_or_proposed'] not in COND_COP and r['page_id'] != 'EXIST-BLOG-ER-ONLINE']
check('X2 every non-conditional page meets the planned connectivity bar (documented exception: EXIST-BLOG-ER-ONLINE)', not below, below)
check('X3 required relationship families present', all(any(r['relationship_type'] == t for r in LM) for t in [
    'HUB_TO_CHILD', 'CHILD_TO_HUB', 'CHILD_TO_RELATED_CHILD', 'BLOG_TO_EDUCATION', 'BLOG_TO_CATEGORY', 'BLOG_TO_PRODUCT', 'BLOG_TO_RELATED_BLOG',
    'CATEGORY_TO_SUBCATEGORY', 'CATEGORY_TO_PRODUCT', 'CATEGORY_TO_EDUCATION', 'PRODUCT_TO_CATEGORY', 'PRODUCT_TO_EDUCATION', 'FAQ_TO_EDUCATION',
    'FAQ_TO_CATEGORY', 'EDUCATION_TO_CATEGORY', 'EDUCATION_TO_PRODUCT']))

w = max(len(n) for n, _, _ in results)
for n, ok, d in results:
    print(f"{'PASS' if ok else 'FAIL'}  {n}" + ('' if ok or not d else f'   -> {d}'))
npass = sum(ok for _, ok, _ in results)
print(f'\n{npass}/{len(results)} checks pass')
sys.exit(0 if npass == len(results) else 1)
