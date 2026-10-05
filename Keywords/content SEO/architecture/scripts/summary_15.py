#!/usr/bin/env python3
"""Writes architecture/15_keyword_url_mapping_summary.md from the Stage 15 CSVs (run after build_15.py)."""
import csv, collections, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
rd = lambda p: list(csv.DictReader(open(os.path.join(ROOT, p), newline='', encoding='utf-8')))
vol = lambda x: int(float(x)) if x not in ('', 'NOT_AVAILABLE', None) and x.replace('.', '', 1).isdigit() else 0

K = rd('architecture/15_keyword_url_map.csv')
R = rd('architecture/15_target_page_registry.csv')
C = rd('architecture/15_cluster_page_map.csv')
P = rd('content-strategy/15_ranking_equity_protection.csv')
Z = rd('architecture/15_cannibalization_check.csv')
d = collections.Counter(r['mapping_disposition'] for r in K)
mapped = [r for r in K if r['target_id']]
ex = [r for r in R if r['existing_or_proposed'] == 'EXISTING']
pr = [r for r in R if r['existing_or_proposed'] == 'PROPOSED']
pend = [r for r in R if 'URL_PENDING' in r['proposed_url']]
L = []
w = L.append

w('# Stage 15 — Keyword → URL mapping: summary')
w('')
w('Date: 2026-09-24. Status: **COMPLETE**. Local project files only. **No DataForSEO call, no other API call and no spend ($0.00).** Cumulative project spend is unchanged at $0.33536.')
w('')
w('This is an inventory of where each keyword is owned. It is not a priority list and contains no scores. Proposed URLs are *expressions* built from Stage 12 D-12 principles; they are not implemented, and the path prefix depends on the platform (Stage 12 D-17).')
w('')
w('| File | Contents |')
w('|---|---|')
w(f'| `architecture/15_keyword_url_map.csv` | {len(K)} rows, one per Stage 7 keyword |')
w(f'| `architecture/15_target_page_registry.csv` | {len(R)} target pages that own at least one keyword |')
w(f'| `architecture/15_cluster_page_map.csv` | {len(C)} rows, one per Stage 11 cluster |')
w(f'| `architecture/15_cannibalization_check.csv` | {len(Z)} check rows (A–E + special checks) |')
w(f'| `content-strategy/15_ranking_equity_protection.csv` | {len(P)} rows, all Stage 3 ranking keywords |')
w('| `architecture/15_keyword_mapping_decision_log.md` | Decisions D15-01 to D15-16 |')
w('| `architecture/scripts/build_15.py`, `summary_15.py`, `qc_15.py` | Build, summary and QC |')
w('')
w('## 1–10. Keyword dispositions')
w('')
w('| # | Disposition | Keywords | Meaning |')
w('|---|---|---|---|')
meaning = {
    'MAP_EXISTING_URL': 'Existing URL owns it now; a planned move/retarget happens only under Stage 13 conditions (1:1 301)',
    'MAP_EXISTING_URL_KEEP': 'Existing URL owns it and stays where it is (DO_NOT_MOVE_NOW, update in place, migration deferred, or commercial URL kept)',
    'MAP_PROPOSED_URL': 'Stage 14 PROPOSED / PROPOSED_PROVISIONAL resource that does not exist yet',
    'MAP_INTERIM_HOME': "Primary topic is CONDITIONAL; Stage 14 names an interim home",
    'CONDITIONAL_NOT_MAPPED': 'Owner is a CONDITIONAL page (Education or commercial); no URL until the condition is met',
    'DEFERRED_NOT_MAPPED': 'Owner is DEFERRED (Education, commercial, or Blog with no article planned)',
    'EXCLUDE_COMMERCIAL': 'Commercial query with no HOD destination (not in catalogue / NOT_PROPOSED / non-indexable filter)',
    'EXCLUDE_NOISE': 'Stage 7/11 noise',
    'EXCLUDE_COMPETITOR_BRAND': 'Competitor or third-party brand',
    'EXCLUDE_OFF_SCOPE': 'No jewelry need, or third-party lab navigation',
    'REVIEW_REQUIRED': 'Ambiguous; needs evidence or a business answer',
}
order = ['MAP_EXISTING_URL', 'MAP_EXISTING_URL_KEEP', 'MAP_PROPOSED_URL', 'MAP_INTERIM_HOME', 'CONDITIONAL_NOT_MAPPED', 'DEFERRED_NOT_MAPPED',
         'EXCLUDE_COMMERCIAL', 'EXCLUDE_NOISE', 'EXCLUDE_COMPETITOR_BRAND', 'EXCLUDE_OFF_SCOPE', 'REVIEW_REQUIRED']
for i, k in enumerate(order, 1):
    w(f'| {i} | {k} | {d[k]} | {meaning[k]} |')
w(f'| | **Total** | **{sum(d.values())}** | Every Stage 7 keyword appears exactly once |')
w('')
w(f'- Mapped to a URL owner (existing + existing-keep + proposed + interim): **{len(mapped)}** keywords.')
w(f"- Existing URLs (MAP_EXISTING_URL + MAP_EXISTING_URL_KEEP): **{d['MAP_EXISTING_URL'] + d['MAP_EXISTING_URL_KEEP']}**. Proposed URLs: **{d['MAP_PROPOSED_URL']}**. Interim homes: **{d['MAP_INTERIM_HOME']}**.")
w(f"- Conditional + deferred: **{d['CONDITIONAL_NOT_MAPPED'] + d['DEFERRED_NOT_MAPPED']}**. Exclusions (commercial + noise + competitor + off-scope): **{d['EXCLUDE_COMMERCIAL'] + d['EXCLUDE_NOISE'] + d['EXCLUDE_COMPETITOR_BRAND'] + d['EXCLUDE_OFF_SCOPE']}**. Review-required: **{d['REVIEW_REQUIRED']}** (154 inherited from Stage 11 UNCLUSTERED_REVIEW + 2 added here).")
conf = collections.Counter(r['mapping_confidence'] for r in mapped)
w(f"- Confidence of the {len(mapped)} mapped keywords: HIGH {conf['HIGH']}, MEDIUM {conf['MEDIUM']}, LOW {conf['LOW']}. LOW is mostly provisional topics, interim homes and unvalidated TRANSACTIONAL/NAVIGATIONAL labels inside informational owners. Only 100 of 1,936 keywords have a Stage 8 SERP.")
w('')
w('## 11–12. Target pages')
w('')
w(f'- **{len(R)} target pages** own keywords: **{len(ex)} existing URLs** and **{len(pr)} proposed pages**.')
w(f"- Of the {len(pr)} proposed pages, {sum(1 for r in pr if r['proposed_url'].startswith('/'))} have a proposed URL expression and {sum(1 for r in pr if 'URL_PENDING' in r['proposed_url'])} are URL_PENDING.")
w(f"- Of the {len(ex)} existing URLs, {sum(1 for r in ex if r['status'].startswith('EXISTING_KEEP'))} stay where they are and {sum(1 for r in ex if not r['status'].startswith('EXISTING_KEEP'))} have a future Education destination that is used only when the Stage 13 migration conditions are met.")
w('- Architecture nodes with no keyword ownership are not in the registry: the Education root (/education), the Ring & Jewellery Guides index (EDU-RJG-00), the commercial category hubs (Engagement Rings, Wedding Bands, Fine Jewellery and children, Bespoke). The commercial hubs have no keywords because the master database has almost no commercial category queries (Stage 12 evidence constraint; D-19 unapproved). This is a data gap, not a lack of demand.')
w('')
w('## 13. Keywords per target page')
w('')
w('| target_id | Page | Status | Current / proposed URL | Keywords | Clusters |')
w('|---|---|---|---|---|---|')
for r in sorted(R, key=lambda r: r['target_id']):
    url = r['existing_url'] or r['proposed_url']
    w(f"| {r['target_id']} | {r['target_page_name']} | {r['status']} | `{url}` | {r['keyword_count']} | {r['cluster_ids']} |")
w('')
w('## 14. Highest-volume keyword per target page')
w('')
w('Listed by the single highest-volume mapped keyword. This describes where large queries sit; it is not a ranking of page importance. Several are unvalidated or LOW-confidence (see the map).')
w('')
w('| target_id | Highest-volume mapped keyword | SERP evidence on this target |')
w('|---|---|---|')
for r in sorted(R, key=lambda r: -vol(r['highest_search_volume'].rsplit('(', 1)[1].rstrip(')')))[:12]:
    w(f"| {r['target_id']} | {r['highest_search_volume']} | {r['serp_evidence']} |")
w('')
w('## 15. Existing ranking URLs protected')
w('')
urls = collections.OrderedDict()
for p in P:
    urls.setdefault(p['ranking_url'], []).append(p)
w(f'All {len(P)} Stage 3 ranking keywords are accounted for, on **{len(urls)} ranking URLs**. **Every one of the {len(urls)} URLs is preserved.** No ranking keyword is reassigned to a new page.')
w('')
w('| Ranking URL | Ranking kw | Action | Migration status |')
w('|---|---|---|---|')
for u, ps in urls.items():
    acts = collections.Counter(p['action'] for p in ps)
    w(f"| `{u}` | {len(ps)} | {'; '.join(f'{a} ×{n}' for a, n in acts.items())} | {ps[0]['migration_status']} |")
w('')
w("- The one keyword that is not targeted is `cvd/hpht diamond tester` (pos 68): its SERP is CATEGORY (tester shopping) and Stage 13 classed it MISALIGNED. The URL is untouched and keeps whatever ranking it has; no page targets the keyword (EXCLUDE_COMMERCIAL).")
w('')
w('## 16. Cannibalization warnings')
w('')
zc = collections.Counter((z['check'], z['severity']) for z in Z)
w('| Check | Result |')
w('|---|---|')
w(f"| A. Many keywords → one URL | {sum(v for (c, s), v in zc.items() if c.startswith('A_'))} targets listed (expected) |")
w(f"| B. Same keyword → multiple URLs | {'PASS: 0' if zc[('B_SAME_KEYWORD_MULTIPLE_URLS', 'PASS')] else 'FAIL'}. Near-duplicate variants split across targets: {sum(v for (c, s), v in zc.items() if c == 'B_NEAR_DUPLICATE_VARIANTS_SPLIT')}. Variant status inconsistencies (unmapped, inherited): {sum(v for (c, s), v in zc.items() if c == 'B_VARIANT_STATUS_INCONSISTENCY')} |")
cc = [z for z in Z if z['check'].startswith('C_')]
w(f"| C. Same cluster → multiple targets | {len(cc)} clusters: {', '.join(z['subject'] + ('*' if z['severity'] == 'REVIEW' else '') for z in cc)}. * = a target outside the cluster's Stage 14 PRIMARY/SECONDARY rows, used by a documented keyword-level intent rule (D15-09, D15-10) |")
dd = [z for z in Z if z['check'].startswith('D_') and z['severity'] == 'FLAG']
w(f"| D. Existing ranking URL vs proposed URL | {len(P) - len(dd)} of {len(P)} ranking keywords map to their current ranking URL. {len(dd)} flagged: {', '.join(z['subject'] for z in dd)} (not targeted; URL preserved) |")
ee = [z for z in Z if z['check'].startswith('E_')]
w(f"| E. Owners with adjacent intent | {len(ee)} pairs flagged: {sum(1 for z in ee if z['severity'] == 'HIGH')} HIGH, {sum(1 for z in ee if z['severity'] == 'MEDIUM')} MEDIUM, {sum(1 for z in ee if z['severity'] == 'LOW')} LOW, {sum(1 for z in ee if z['severity'] == 'INSUFFICIENT_EVIDENCE')} INSUFFICIENT_EVIDENCE |")
sp = [z for z in Z if z['check'].startswith('SPECIAL_')]
w(f"| Special checks (CVD, HPHT, lab-vs-natural, are-real, 4Cs, clarity, shapes, IGI, commercial SERPs) | {sum(1 for z in sp if z['severity'] == 'PASS')}/{len(sp)} PASS |")
w('')
w('Pairs flagged under E:')
w('')
for z in ee:
    w(f"- **{z['severity']}** {z['subject']}: {z['detail']}")
w('')
w('No actual cannibalization is demonstrated: no keyword has two HOD URLs ranking (Stage 3/10/11). The warnings above are boundaries to enforce in content (Stage 19) and linking (Stage 16).')
w('')
w('## 17. Unresolved URL decisions')
w('')
w(f'{len(pend)} registry targets have a URL_PENDING element:')
w('')
for r in pend:
    w(f"- **{r['target_id']}** ({r['target_page_name']}): {r['notes']}")
w('')
w('Other open questions (details in the decision log):')
w('')
w('- Platform (Stage 12 D-17): every proposed URL expression assumes a custom/headless path structure. A native Shopify build would express these as `/blogs/<blog>/…` or `/pages/…`; the logical owner does not change.')
w('- "Jewellery" vs "jewelry" (Stage 12 D-15): blocks the Ring & Jewellery Guides and Metals hub slugs.')
w('- Existing slugs with brand suffixes or misspellings (GIA-vs-IGI education article; `/by-desgin/` side-stone subcategory): kept. Any change is an implementation migration with 1:1 301s; Stage 15 does not recommend a stand-alone change.')
w(f"- {d['REVIEW_REQUIRED']} REVIEW_REQUIRED keywords, led by 'diamond stone' (18,100; dual meaning per Stage 8).")
w("- Commercial owners that are CONDITIONAL or DEFERRED in Stage 12 (Lab-Grown commercial hub, Earrings > Studs, Natural hub, loose/carat pages, wholesale, Fine Jewellery > Rings). Their keywords are held, not mapped.")
w('')
w('## Paid research')
w('')
w('None was run. The Stage 14 D14-29 SERP batch (16 tasks, max $0.0096) and the Stage 12 D-19 commercial supplement remain NOT approved. Stage 15 did not need them to produce a complete mapping: every keyword they would affect is already held as CONDITIONAL, DEFERRED, INTERIM or LOW confidence. What they would change is listed in decision D15-15.')
w('')
w('## Next stage')
w('')
w('Stage 16 (internal linking) is **not started**, per instruction.')
open(os.path.join(ROOT, 'architecture/15_keyword_url_mapping_summary.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('summary written')
