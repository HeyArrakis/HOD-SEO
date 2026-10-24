"""Read-only QC for the Backlink Acquisition workstream. Exit code 1 if any check fails.
Usage: python3 _build/qc_backlink_db.py [--live]   (--live re-checks evidence URLs not already in page-check JSON)"""
import csv, json, os, re, sys, subprocess, glob
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); RAW = os.path.join(ROOT, '_raw')
DB = os.path.join(ROOT, '01-HOD-BACKLINK-ACQUISITION-DATABASE.csv')
results = []
def check(name, ok, detail=''):
    results.append((ok, name, detail)); print(('PASS ' if ok else 'FAIL ') + name + (f' — {detail}' if detail else ''))

REQ = ['Opportunity ID', 'Prospect domain', 'Prospect URL / source-page URL', 'Source-page title', 'Opportunity category',
       'Domain relevance', 'Target audience relevance', 'Authority metric', 'Authority metric provider', 'Authority metric type',
       'Competitor linking?', 'Competitor domain(s)', 'Verified competitor backlink URL', 'Existing HOD backlink?',
       'Link type / acquisition route', 'Link attributes, where verifiable', 'Potential HOD target page',
       'Potential anchor text or citation wording', 'Outreach angle', 'Contact name, if verified',
       'Public contact email or contact-page URL', 'Contact/source evidence URL', 'Acquisition feasibility', 'Priority',
       'Priority rationale', 'Outreach status', 'Next action', 'Research source / provider', 'Date researched',
       'Verification notes', 'Limitations / dependencies']
CAT = {'COMPETITOR_BACKLINK_GAP', 'EDITORIAL_PUBLICATION', 'WEDDING_PUBLICATION', 'LUXURY_PUBLICATION', 'DIAMOND_RESOURCE',
       'INDUSTRY_ASSOCIATION', 'RELEVANT_DIRECTORY', 'UNLINKED_MENTION', 'DIGITAL_PR', 'RESOURCE_PAGE', 'BROKEN_LINK_OPPORTUNITY',
       'EXPERT_CONTRIBUTION', 'OTHER'}
STATUS = {'UNRESEARCHED', 'VERIFICATION_REQUIRED', 'VERIFIED_PROSPECT', 'PRIORITIZED', 'OUTREACH_READY', 'CONTACTED',
          'RESPONDED', 'WON', 'LOST', 'REVISIT_LATER', 'DISQUALIFIED'}
ROUTE = {'EDITORIAL_ROUNDUP_INCLUSION', 'EDITORIAL_PITCH', 'EXPERT_COMMENTARY', 'JOURNALIST_REQUEST_PLATFORM', 'PRESS_RELEASE_NEWS',
         'MEMBERSHIP_DIRECTORY', 'BRAND_DIRECTORY_SUBMISSION', 'REVIEW_REQUEST', 'VENDOR_LISTING', 'SUBMISSION_FEATURE',
         'BROKEN_LINK_REPLACEMENT', 'RESOURCE_PAGE_SUGGESTION', 'AFFILIATE_PROGRAM_DEPENDENT', 'COMMUNITY_PARTICIPATION', 'NONE'}
LVL = {'HIGH', 'MEDIUM', 'LOW'}
GAP_EV = {'PROVIDER_AND_LIVE_VERIFIED', 'LIVE_PAGE_VERIFIED', 'PROVIDER_VERIFIED_BROKEN', 'PROVIDER_DOMAIN_LEVEL',
          'PROVIDER_VERIFIED_SOURCE_GONE', 'PROVIDER_FLAG_STALE'}

# 1. encoding + structure
raw = open(DB, 'rb').read()
try:
    raw.decode('utf-8'); check('CSV decodes as UTF-8', True)
except UnicodeDecodeError as e:
    check('CSV decodes as UTF-8', False, str(e))
recs = list(csv.reader(open(DB, encoding='utf-8', newline='')))
hdr = recs[0]
check('All 31 required columns present in order', hdr[:31] == REQ, f'{len(hdr)} columns total')
check('Every row has the header field count', all(len(r) == len(hdr) for r in recs[1:]), f'{len(recs) - 1} rows')
rows = list(csv.DictReader(open(DB, encoding='utf-8', newline='')))

# 2. required values + controlled vocab
for col in ['Opportunity ID', 'Prospect domain', 'Prospect URL / source-page URL', 'Opportunity category', 'Priority',
            'Outreach status', 'Date researched', 'Research source / provider', 'Priority rationale', 'Next action']:
    check(f'No blank "{col}"', all(r[col].strip() for r in rows), str([r['Opportunity ID'] for r in rows if not r[col].strip()]))
check('Category values controlled', all(r['Opportunity category'] in CAT for r in rows))
check('Status values controlled', all(r['Outreach status'] in STATUS for r in rows))
check('Route values controlled', all(r['Link type / acquisition route'] in ROUTE for r in rows))
check('Relevance/feasibility values controlled', all(r['Domain relevance'] in LVL and r['Target audience relevance'] in LVL and r['Acquisition feasibility'] in LVL for r in rows))
check('Priority values controlled', all(r['Priority'] in {'P1', 'P2', 'P3', 'NONE'} for r in rows))
check('Competitor linking? values controlled', all(r['Competitor linking?'] in {'Yes', 'No', 'Unknown'} for r in rows))
check('Date researched present and ISO (2026-10-10)', all(r['Date researched'] == '2026-10-10' for r in rows))

# 3. duplicates
ids = Counter(r['Opportunity ID'] for r in rows)
check('Opportunity IDs unique', all(v == 1 for v in ids.values()))
keys = Counter((r['Prospect domain'], r['Prospect URL / source-page URL'], r['Link type / acquisition route']) for r in rows)
check('No duplicate (domain, URL, route) opportunity', all(v == 1 for v in keys.values()), str([k for k, v in keys.items() if v > 1]))

# 4. authority metric provenance
ranks = {i['target']: i['rank'] for i in json.load(open(os.path.join(RAW, 'dataforseo', 'C6_bulk_ranks_2026-10-10.json')))['items']}
check('Every authority metric has provider + metric type', all((r['Authority metric'] == '') or (r['Authority metric provider'] and r['Authority metric type']) for r in rows))
check('Every authority value matches C6 raw data', all(r['Authority metric'] == '' or int(r['Authority metric']) == ranks.get(r['Prospect domain']) for r in rows))
check('Every prospect domain has a C6 metric', all(r['Prospect domain'] in ranks for r in rows), str([r['Prospect domain'] for r in rows if r['Prospect domain'] not in ranks]))

# 5. competitor-link claims supported
c1 = json.load(open(os.path.join(RAW, 'dataforseo', 'C1_hod_backlinks_one_per_domain_2026-10-10.json')))
hod_ref = {i['domain_from'].replace('www.', '') for i in c1['tasks'][0]['result'][0]['items']}
bad = [r['Opportunity ID'] for r in rows if r['Competitor linking?'] == 'Yes' and (r['Evidence class'] not in GAP_EV or not r['Competitor domain(s)'])]
check('Every "Competitor linking = Yes" has provider/live evidence + named competitor', not bad, str(bad))
bad = [r['Opportunity ID'] for r in rows if r['Evidence class'] == 'PUBLIC_SOURCE_PROSPECT' and r['Competitor linking?'] != 'Unknown']
check('Standalone prospects are not labelled as competitor-linking', not bad, str(bad))
prov_urls = set()
for fn in ['C2_processed.csv', 'C3_processed.csv', 'C5_processed.csv']:
    prov_urls |= {re.sub(r'^https?://(www\.)?', '', x['url_from']).rstrip('/') for x in csv.DictReader(open(os.path.join(RAW, 'dataforseo', fn), encoding='utf-8'))}
bad = [r['Opportunity ID'] for r in rows if r['Evidence class'].startswith('PROVIDER') and r['Evidence class'] != 'PROVIDER_DOMAIN_LEVEL'
       and re.sub(r'^https?://(www\.)?', '', r['Prospect URL / source-page URL']).rstrip('/') not in prov_urls]
check('Provider-verified rows trace to a DataForSEO url_from', not bad, str(bad))
c4 = {x['referring_domain'] for x in csv.DictReader(open(os.path.join(RAW, 'dataforseo', 'C4_processed.csv'), encoding='utf-8'))}
bad = [r['Opportunity ID'] for r in rows if r['Evidence class'] == 'PROVIDER_DOMAIN_LEVEL' and r['Prospect domain'] not in c4]
check('Domain-level rows trace to C4', not bad, str(bad))
check('No prospect domain is an existing HOD referring domain (C1)', not [r for r in rows if r['Prospect domain'] in hod_ref])
check('"Existing HOD backlink?" never claims Yes without C1', all(not r['Existing HOD backlink?'].startswith('Yes') for r in rows))

# 6. priority logic reproducible
def recompute(r):
    s = sum(int(r[k]) for k in ['Score R (relevance 0-3)', 'Score Q (source quality 0-3)', 'Score P (pathway 0-3)', 'Score G (gap evidence 0-2)', 'Score F (feasibility 0-3)', 'Score V (business value 0-3)'])
    R, P, F = int(r['Score R (relevance 0-3)']), int(r['Score P (pathway 0-3)']), int(r['Score F (feasibility 0-3)'])
    if r['Outreach status'] == 'DISQUALIFIED': return s, 'NONE'
    return s, ('P1' if s >= 14 and F >= 2 and P >= 2 and R >= 3 else 'P2' if s >= 10 else 'P3')
check('Score totals = sum of components', all(int(r['Priority score (0-17)']) == recompute(r)[0] for r in rows))
check('Priority reproduces from the documented formula', all(r['Priority'] == recompute(r)[1] for r in rows))
check('DISQUALIFIED <=> Priority NONE', all((r['Outreach status'] == 'DISQUALIFIED') == (r['Priority'] == 'NONE') for r in rows))
check('No row is OUTREACH_READY while gate G0 is open', not [r for r in rows if r['Outreach status'] == 'OUTREACH_READY'])
p1 = [r for r in rows if r['Priority'] == 'P1']
check('Every P1 has rationale with score, next action, verified route', all('Score' in r['Priority rationale'] and r['Next action'] and r['Public contact email or contact-page URL'] and 'NOT VERIFIED' not in r['Public contact email or contact-page URL'] for r in p1))
check('Every P1 has a queue rank 1-5', sorted(int(r['Queue rank']) for r in p1) == [1, 2, 3, 4, 5])

# 7. emails only from captured evidence
evidence_text = ''
for f in glob.glob(os.path.join(RAW, 'page-checks', '*.json')):
    evidence_text += open(f, encoding='utf-8').read()
# rodney@rings.com was read from the study page via WebFetch; record it in a captured-evidence file
extra_ev = os.path.join(RAW, 'page-checks', 'webfetch_notes_2026-10-10.json')
if os.path.exists(extra_ev):
    evidence_text += open(extra_ev, encoding='utf-8').read()
emails = set()
for r in rows:
    emails |= set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', r['Public contact email or contact-page URL']))
missing = sorted(e for e in emails if e not in evidence_text)
check('Every listed email appears in captured page evidence (none guessed)', not missing, str(missing))

# 8. URL formats + liveness
bad = [r['Opportunity ID'] for r in rows if not r['Prospect URL / source-page URL'].startswith('http')]
check('Prospect URLs are absolute', not bad, str(bad))
checked = {}
for f in glob.glob(os.path.join(RAW, 'page-checks', '*.json')):
    d = json.load(open(f, encoding='utf-8'))
    for x in (d if isinstance(d, list) else d.get('checks', [])):
        checked[x['url']] = x.get('status', x.get('verdict'))
unchecked = sorted({r['Prospect URL / source-page URL'] for r in rows} - set(checked))
if '--live' in sys.argv and unchecked:
    UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'
    live = {}
    for u in unchecked:
        p = subprocess.run(['curl', '-s', '-o', '/dev/null', '-L', '--max-time', '25', '-A', UA, '-w', '%{http_code}', u], capture_output=True, text=True)
        live[u] = p.stdout
    json.dump(live, open(os.path.join(RAW, 'page-checks', 'qc_liveness_2026-10-10.json'), 'w'), indent=1)
    checked.update(live)
    unchecked = []
print('  evidence URLs not yet status-checked:', len(unchecked), unchecked[:5])
dead = [(r['Opportunity ID'], checked.get(r['Prospect URL / source-page URL'])) for r in rows
        if str(checked.get(r['Prospect URL / source-page URL'])) in ('404', '410') and r['Outreach status'] != 'DISQUALIFIED']
check('No non-disqualified row relies on a 404/410 source page', not dead, str(dead))

# 9. counts reconcile with the documents
pr = Counter(r['Priority'] for r in rows)
gap_ok = [r for r in rows if r['Competitor linking?'] == 'Yes' and r['Outreach status'] != 'DISQUALIFIED']
std = [r for r in rows if r['Evidence class'] == 'PUBLIC_SOURCE_PROSPECT']
std_ver = [r for r in std if r['Outreach status'] not in ('DISQUALIFIED', 'VERIFICATION_REQUIRED')]
facts = {'rows': len(rows), 'P1': pr['P1'], 'P2': pr['P2'], 'P3': pr['P3'], 'NONE': pr['NONE'], 'gap_rows': len(gap_ok),
         'gap_domains': len({r['Prospect domain'] for r in gap_ok}), 'standalone': len(std), 'standalone_verified': len(std_ver),
         'domains': len({r['Prospect domain'] for r in rows}), 'mentions': len([r for r in rows if r['Opportunity category'] == 'UNLINKED_MENTION'])}
print('  counts:', facts)
docs = {f: open(os.path.join(ROOT, f), encoding='utf-8').read() for f in ['02-COMPETITOR-BACKLINK-GAP-SUMMARY.md', '03-OUTREACH-PRIORITY-QUEUE.md', '04-UNLINKED-MENTIONS-AND-DIGITAL-PR.md', 'README.md']}
check('02 states 77 rows / 72 domains / 44 gap rows / 40 domains / 26 standalone',
      all(s in docs['02-COMPETITOR-BACKLINK-GAP-SUMMARY.md'] for s in [f"{facts['domains']} domains / {facts['rows']} rows", f"{facts['gap_rows']} rows ({facts['gap_domains']} domains)", f"{facts['standalone']} rows are standalone"]))
check('02 lists exactly the P1 rows', all(r['Opportunity ID'] in docs['02-COMPETITOR-BACKLINK-GAP-SUMMARY.md'] for r in p1) and f"P1 ({pr['P1']})" in docs['02-COMPETITOR-BACKLINK-GAP-SUMMARY.md'])
check('03 queue covers every queue-ranked row', all(r['Opportunity ID'] in docs['03-OUTREACH-PRIORITY-QUEUE.md'] for r in rows if r['Queue rank']))
check('README row count matches', f"{facts['rows']} rows" in docs['README.md'])
check('04 reports 0 verified mentions and DB has 0 mention rows', '**0 verified**' in docs['04-UNLINKED-MENTIONS-AND-DIGITAL-PR.md'] and facts['mentions'] == 0)

# 10. protected files / location
gs = subprocess.run(['git', '-C', os.path.dirname(os.path.dirname(ROOT)), 'status', '--porcelain', '--untracked-files=all'], capture_output=True, text=True).stdout.splitlines()
before = open(sys.argv[sys.argv.index('--before') + 1]).read().splitlines() if '--before' in sys.argv else None
new_paths = [l for l in gs if not l.startswith('?? "Off-page SEO/') and not l.startswith('?? Off-page SEO/')]
if before is not None:
    before_set = set(before)
    # compare at the granularity git reported before (directories may be collapsed there)
    gs_short = subprocess.run(['git', '-C', os.path.dirname(os.path.dirname(ROOT)), 'status', '--short'], capture_output=True, text=True).stdout.splitlines()
    added = [l for l in gs_short if l not in before_set]
    check('Only change vs pre-work git status is the new Off-page SEO/ folder', added == ['?? "Off-page SEO/"'], str(added))

fails = [n for ok, n, _ in results if not ok]
print(f'\n{len(results) - len(fails)}/{len(results)} checks pass')
sys.exit(1 if fails else 0)
