"""Ranked high-volume opportunity table (hard revision, Section 17). Local files only.
One row per demand group >= 5,000/mo that is jewellery-relevant (NOT_RELEVANT excluded), plus every Round 2 decision row.
Ranked by demand, with written reasoning (no composite score)."""
import csv, os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')); os.chdir(ROOT)
KR = list(csv.DictReader(open('content-strategy/blog-calendar/blog_keyword_research.csv')))
SERP = {r['keyword']: r for r in csv.DictReader(open('content-strategy/blog-calendar/revision/round2_serp_analysis.csv'))}
DEC = list(csv.DictReader(open('content-strategy/blog-calendar/revision/round2_decision_table.csv')))
MANUAL = {
 'ring finger': ('VARIANT_OF_SCHEDULED', 'BC-036', 'Ambiguous head (anatomy vs ring); the jewellery sense is covered by BC-036 (which finger) and BC-038 (meaning).'),
 'bride ring finger': ('VARIANT_OF_SCHEDULED', 'BC-036', 'Same intent as "what finger does a wedding ring go on".'),
 'what hand wedding ring finger': ('VARIANT_OF_SCHEDULED', 'BC-036', 'Same intent as BC-036.'),
 'what hand is the ring finger': ('VARIANT_OF_SCHEDULED', 'BC-036', 'Same intent as BC-036.'),
 'finger for proposal ring': ('VARIANT_OF_SCHEDULED', 'BC-036', 'Engagement-ring finger question; answered in BC-036.'),
 'how much does engagement ring cost': ('VARIANT_OF_SCHEDULED', 'BC-024', 'Same AIO/PAA intent as BC-024 (cost + budget).'),
 'ring types engagement': ('ROUTE_TO_EDUCATION', 'EDU-RJG-01', 'Same demand group as "engagement ring styles" (18,100): permanent style/setting guide.'),
 'budget engagement rings': ('RESERVED_COMMERCIAL_PAGE', 'COM-ER', 'Transactional shopping intent (product SERP features); BC-024 links to COM-ER for budget shopping.'),
 'vermeil in gold': ('EDUCATION_OWNER_OR_GAP', 'EDU-MET-00 scope', 'Metals reference; depends on whether HOD sells vermeil (business fact).'),
 'what is gold vermeil': ('EDUCATION_OWNER_OR_GAP', 'EDU-MET-00 scope', 'Metals reference (Dec 1.69x); business fact needed.'),
 'jewelry cleaner': ('EDUCATION_OWNER_OR_GAP', 'EDU-RJG-03 (conditional)', 'Care product/how-to; Education care page, not Blog.'),
 'jewelry insurance': ('EDUCATION_OWNER_OR_GAP', 'Education gap', 'Practical ownership topic; Education gap (with engagement ring insurance 8,100).'),
 '14k vs 18k gold': ('EXISTING_PAGE_OWNER', 'EDU-MET-01', 'Owned by the existing ranking 14k-vs-18k article.'),
 'white gold vs yellow gold': ('EXISTING_PAGE_OWNER', 'EDU-MET-00', 'Metals comparison owned by the Metals hub.'),
 'how to tell if gold is real': ('NOT_HOD_FIT', 'none', 'Gold-testing intent; not a diamond-jewellery buying journey.'),
 'is it real gold': ('NOT_HOD_FIT', 'none', 'Gold-testing intent.'),
 'what is permanent jewelry': ('NOT_HOD_FIT', 'none', 'HOD does not offer welded permanent jewellery.'),
 'what is moissanite diamond': ('EXISTING_PAGE_OWNER', 'EDU-GEM-03 (deferred)', 'Gemstones & alternatives Education (deferred).'),
 'diamond eye clean': ('EXISTING_PAGE_OWNER', 'EDU-4C-01', 'Clarity guide owns eye-clean.'),
 'how to size my finger for a ring': ('EXISTING_PAGE_OWNER', 'EDU-RJG-02', 'Ring size guide owns sizing.'),
}
SUIT = {'PRIMARY': 'BLOG (scheduled)', 'SECONDARY': 'BLOG (scheduled, secondary)', 'VARIANT_OF_SCHEDULED': 'BLOG (covered by scheduled article)',
        'RESERVED_COMMERCIAL_PAGE': 'COMMERCIAL/CATEGORY', 'COMMERCIAL_PROMO_NOT_BLOG': 'COMMERCIAL/CATEGORY', 'ROUTE_TO_COMMERCIAL': 'COMMERCIAL/CATEGORY',
        'EDUCATION_OWNER_OR_GAP': 'EDUCATION', 'EXISTING_PAGE_OWNER': 'EDUCATION / EXISTING OWNER', 'ROUTE_TO_EDUCATION': 'EDUCATION', 'EDUCATION_GAP': 'EDUCATION',
        'NOT_HOD_FIT': 'NOT RELEVANT TO HOD', 'REJECTED_SERP_INTENT': 'NOT A FIT (SERP intent)', 'REMOVED_IN_REVISION': 'REMOVED (see revision log)',
        'COVERED_AS_SECTION': 'BLOG SECTION', 'BACKLOG_REVISION': 'BACKLOG'}
groups = {}
for r in KR:
    if not r['search_volume'].isdigit() or int(r['search_volume']) < 5000 or r['disposition'] in ('NOT_RELEVANT', 'NO_DATA'): continue
    g = r['candidate_group'].split(' / ')[0] if r['research_round'].startswith('R1') else 'R0:' + r['keyword']
    if g in groups and groups[g]['disposition'] in ('PRIMARY', 'SECONDARY'): continue
    if g not in groups or r['disposition'] in ('PRIMARY', 'SECONDARY'): groups[g] = r
out = []
for g, r in groups.items():
    k = r['keyword']; disp, owner, why = r['disposition'], r['target_page_or_category'], r['disposition_reason']
    if k in MANUAL: disp, owner, why = MANUAL[k]
    s = SERP.get(k, {})
    out.append({'keyword': k, 'search_volume': int(r['search_volume']), 'peak_month': r.get('peak_month_last12', ''), 'dfs_intent': r.get('dfs_main_intent', ''),
                'serp_type_verified': s.get('serp_intent_verified', 'not SERP-checked') + (f" ({s['top10_page_types']})" if s else ''),
                'ai_overview': s.get('ai_overview', 'n/a'), 'paa': ('YES' if s.get('paa_present') == 'True' else 'n/a'),
                'hod_fit': 'LOW' if disp in ('NOT_HOD_FIT', 'REJECTED_SERP_INTENT') else 'MEDIUM-HIGH', 'blog_suitability': SUIT.get(disp, disp),
                'existing_owner': owner, 'recommended_action': disp, 'reason': why, 'research_round': r['research_round'], 'demand_group': g})
for d in DEC:  # every SERP-validated decision row, even if <5,000
    m = re.search(r'^(.+?) \((\d+|n/a)\)', d['recommended_primary'])
    if not m or any(o['keyword'] == m.group(1) for o in out): continue
    out.append({'keyword': m.group(1), 'search_volume': int(m.group(2)) if m.group(2).isdigit() else 0, 'serp_type_verified': d['serp_intent_and_composition'],
                'ai_overview': d['ai_overview_structure'][:7], 'paa': 'YES', 'hod_fit': 'see decision', 'blog_suitability': d['recommended_action'], 'existing_owner': d['ownership_cannibalization'][:120],
                'recommended_action': d['recommended_action'], 'reason': d['reason'], 'research_round': 'R2 decision table', 'demand_group': d['blog_id']})
out.sort(key=lambda o: -o['search_volume'])
for i, o in enumerate(out, 1): o['rank_by_demand'] = i
cols = ['rank_by_demand', 'keyword', 'search_volume', 'peak_month', 'dfs_intent', 'serp_type_verified', 'ai_overview', 'paa', 'hod_fit', 'blog_suitability', 'existing_owner', 'recommended_action', 'reason', 'research_round', 'demand_group']
with open('content-strategy/blog-calendar/revision/blog_high_volume_opportunity_table.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); [w.writerow({c: o.get(c, '') for c in cols}) for o in out]
import collections
print(len(out), collections.Counter(o['blog_suitability'] for o in out).most_common())
print('unreviewed >=5k:', [o['keyword'] for o in out if o['recommended_action'] == 'DISCOVERED_NOT_PRIORITISED'])
