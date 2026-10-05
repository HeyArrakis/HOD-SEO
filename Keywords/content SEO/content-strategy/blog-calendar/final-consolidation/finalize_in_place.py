"""Finalization pass (2026-10-03): edits FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv IN PLACE.
Adds publishing_priority + production_status and a short production note. No dates, topics, keywords or owners change.
"""
import csv, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
F = os.path.join(ROOT, 'FINAL-BLOG-CALENDAR', 'BLOG_CALENDAR_FINAL.csv')
rows = list(csv.DictReader(open(F, encoding='utf-8')))
cols = list(rows[0].keys())
assert 'publishing_priority' not in cols, 'already finalized'

MUST = {'BC-001', 'BC-004', 'BC-016', 'BC-017', 'BC-019', 'BC-024', 'BC-031', 'BC-034', 'EDU-LG-00', 'EDU-RJG-02', 'EDU-LG-02', 'EDU-SHP-00'}
NORMAL = {'BC-008', 'BC-009', 'BC-023', 'BC-004-DEC-REFRESH', 'EDU-RJG-03', 'EDU-LG-05', 'EDU-NAT-00', 'EDU-CERT-00', 'EDU-4C-02', 'EDU-GEN-01', 'EDU-INS', 'BLOG-WB-BUYS', 'BLOG-NPD'}
FLEX = {'BLOG-ER-HISTORY', 'EDU-LG-08', 'EDU-LG-07', 'BLOG-WR-HISTORY'}
PRIO_WHY = {
 'MUST_PUBLISH': 'time-critical seasonal lead time, the largest strategic Education asset, protected ranking equity, or high-intent buying research',
 'HIGH': 'strong demand/SERP opportunity with clear HOD relevance; not date-critical',
 'NORMAL': 'useful supporting content (moderate demand, retention/trust role or dependent on a refresh)',
 'FLEXIBLE': 'low volume; kept for brand/hub completeness - can slip if capacity is limited',
}
OWN = {
 'EDU-RJG-NL': 'new Education page (necklace length) - no Stage 14/15 owner yet; confirm placement under the Ring & Jewellery Guides hub.',
 'EDU-RJG-BR': 'new Education page (bracelet size) - no Stage 14/15 owner yet; confirm placement under the Ring & Jewellery Guides hub.',
 'EDU-INS': 'new Education page (engagement ring insurance) - no Stage 14/15 owner yet; confirm.',
 'EDU-WB-GUIDE': 'new Education page (wedding-band buying guide) - no Stage 14/15 owner yet; confirm.',
 'EDU-LG-09': '"how to tell if a diamond is real" (18,100) is a new keyword proposed as EDU-LG-09 co-primary - not formally confirmed.',
 'EDU-RJG-03': 'activation of conditional Stage 14 topic EDU-RJG-03 (care) is still unresolved.',
 'BLOG-WR-TYPES': 'Blog vs Education ownership of "types of wedding rings" is uncertain (promote-to-Education candidate, as BC-025).',
 'EDU-RJG-01': 'Stage 19 OWNERSHIP_REVIEW of "engagement ring settings" is still open; the guide can be drafted without that keyword.',
}
FACT = {
 'BC-004-DEC-REFRESH': 'holiday shipping cut-off dates and ready-to-ship pieces are not confirmed.',
 'BC-005': 'whether HOD cuts/polishes in-house or via Surat partners is not confirmed (the article premise is a Surat workshop).',
 'BC-015': 'HOD sourcing geography (where HOD stones are grown) and any ethics-claim wording are not confirmed.',
}
READY_NOTE = {
 'BC-001': 'uses the confirmed bespoke fact ("typically" 2-3 weeks to make + ~6-9 days delivery, ~3-4 weeks, stone-dependent, never guaranteed); state no holiday cut-off date until HOD confirms one.',
 'BC-017': 'use the confirmed typical bespoke timeline as planning guidance; no specific order-by date until HOD confirms.',
 'BC-034': 'use the confirmed typical bespoke timeline as planning guidance; no specific order-by date until HOD confirms.',
 'BC-008': 'omit shipping cut-off and returns specifics; link to the existing /shipping and /returns pages.',
 'BC-009': 'omit shipping cut-off and returns specifics; link to the existing /shipping and /returns pages.',
 'BC-019': 'no HOD Black Friday offer is confirmed - frame as buying-timing guidance; never state discounts.',
 'BC-018': 'mention platinum (20th) only if HOD platinum availability is confirmed.',
 'BC-007': 'omit soldering-service claims unless confirmed.',
 'BC-023': 'explain eternity-band resizing generally; no HOD resizing policy claim.',
 'BC-025': 'describe earring-back types generally; do not state which backs HOD uses until confirmed.',
 'EDU-MET-00': 'general comparison; no platinum/alternative-metal availability claims (Stage 19 NON_BLOCKING).',
 'EDU-MET-01': 'no statement of which karats HOD offers until confirmed (Stage 19 NON_BLOCKING).',
 'EDU-CERT-00': 'general guide; do not state which lab grades HOD stones until confirmed (Stage 19 NON_BLOCKING).',
 'EDU-LG-07': 'general article only; any HOD ethics/sustainability statement is BLOCKING until substantiated (Stage 19).',
 'EDU-LG-05': 'no buy-back/trade-in claim; dated sources for any price.',
}
out_cols = cols[:cols.index('status') + 1] + ['publishing_priority', 'production_status'] + cols[cols.index('status') + 1:]
for r in rows:
    cid = r['content_id']
    if r['status'] == 'UNUSED_SLOT':
        r['publishing_priority'] = ''
        r['production_status'] = 'BACKLOG'
        r['notes'] = r['notes'] + ' | Production: BACKLOG - slot intentionally left unused; do not fill just for cadence.'
        continue
    p = 'MUST_PUBLISH' if cid in MUST else 'NORMAL' if cid in NORMAL else 'FLEXIBLE' if cid in FLEX else 'HIGH'
    if cid in OWN: s, why = 'OWNERSHIP_CONFIRMATION', OWN[cid]
    elif cid in FACT: s, why = 'BUSINESS_FACT_REQUIRED', FACT[cid]
    else: s, why = 'READY_TO_WRITE', READY_NOTE.get(cid, 'ownership confirmed in Stages 13-19 / revised calendar; no unconfirmed HOD fact is required.')
    r['publishing_priority'], r['production_status'] = p, s
    r['notes'] = (r['notes'] + ' | ' if r['notes'] else '') + f"Production: {p} ({PRIO_WHY[p]}); {s} - {why}"
with open(F, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=out_cols); w.writeheader()
    for r in rows: w.writerow({c: r.get(c, '') for c in out_cols})
print('finalized in place:', F)
