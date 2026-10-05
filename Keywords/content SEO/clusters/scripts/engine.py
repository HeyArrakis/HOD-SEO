"""Stage 11 engine: disposition + first-match cluster assignment. Local files only; no API calls."""
import csv, re, sys, os, collections as C
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rules
ROOT = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'


def norm(k):
    k = k.lower().replace("'", "").replace("’", "")
    k = re.sub(r"[-–/]", " ", k)
    return re.sub(r"\s+", " ", k).strip()


def load(path):
    return list(csv.DictReader(open(ROOT + path, encoding='utf-8')))


master = load('dataforseo/processed/07_hod_master_keyword_database.csv')
s8 = {r['keyword'].lower().strip(): r for r in load('serp/analysis/08_hod_serp_validation.csv')}

CL = sorted(rules.CLUSTERS, key=lambda c: (c['prio'], c['id']))
for c in CL:
    c['_re'] = [(re.compile(p), s) for p, s in c['patterns']]
BRAND = [(re.compile(p), n) for p, n in rules.BRAND_REGEX]
WEAK = re.compile(rules.WEAK_BRAND_REGEX)
NOISE = [(re.compile(p), n) for p, n in rules.NOISE_REGEX]


def classify(r):
    kw = r['keyword']; kn = norm(kw); st = r['status']
    validated = kw.lower().strip() in s8
    out = dict(keyword=kw, kn=kn, status=st, validated=validated, cluster=None, strength=None, others=[], disp=None, basis='', brand='')
    if st == 'NOISE':
        out.update(disp='NOISE', basis='STAGE7_NOISE_PRESERVED'); return out
    if st == 'COMPETITOR_BRAND':
        out.update(disp='COMPETITOR_BRAND', basis='STAGE7_COMPETITOR_BRAND_PRESERVED'); return out
    if WEAK.search(kn):
        out.update(disp='UNCLUSTERED_REVIEW', basis='POSSIBLE_BRAND_NAME_NOT_VERIFIED: company-style name; brand identity not independently verified in project data'); return out
    for rx, name in BRAND:
        if rx.search(kn):
            out.update(disp='COMPETITOR_BRAND', basis='STAGE11_BRAND_OVERRIDE', brand=name); return out
    for rx, why in NOISE:
        if rx.search(kn):
            out.update(disp='NOISE', basis='STAGE11_OFFTOPIC_OVERRIDE: ' + why); return out
    if kn in rules.FORCE_REVIEW:
        out.update(disp='UNCLUSTERED_REVIEW', basis='SERP_OR_SEMANTIC_DUAL_MEANING: ' + rules.FORCE_REVIEW[kn]); return out
    hits = []
    for c in CL:
        if kn in c['exact']:
            hits.append((c, 'S', 'exact:' + kn)); continue
        for rx, s in c['_re']:
            if rx.search(kn):
                hits.append((c, s, rx.pattern)); break
    if st == 'AMBIGUOUS':
        hits = [h for h in hits if h[0]['ambiguous_ok'] or validated]
    if hits:
        c, s, pat = hits[0]
        out.update(cluster=c['id'], strength=s, matched=pat, others=[h[0]['id'] for h in hits[1:]], disp='CLUSTERED')
    else:
        out.update(disp='UNCLUSTERED_REVIEW', basis='NO_RULE_MATCH' if st == 'INCLUDE' else 'STAGE7_AMBIGUOUS_NO_STRONG_EVIDENCE')
    return out


if __name__ == '__main__':
    res = [classify(r) for r in master]
    byid = {c['id']: c for c in CL}
    print(C.Counter(x['disp'] for x in res))
    mode = sys.argv[1] if len(sys.argv) > 1 else 'summary'
    vol = {r['keyword']: r['search_volume'] for r in master}
    if mode == 'members':
        groups = C.defaultdict(list)
        for x in res:
            if x['disp'] == 'CLUSTERED': groups[x['cluster']].append(x)
        only = sys.argv[2:]
        for cid in sorted(groups):
            if only and cid not in only: continue
            g = groups[cid]
            print(f"\n## {cid} {byid[cid]['name']} ({len(g)})")
            print('; '.join(f"{x['keyword']}|{vol[x['keyword']]}" + ('*' if x['others'] else '') for x in sorted(g, key=lambda x: x['keyword'])))
        print('\nEmpty clusters:', [c['id'] for c in CL if c['id'] not in groups])
    elif mode == 'residual':
        print('; '.join(f"{x['keyword']}|{vol[x['keyword']]}|{x['status'][0]}" for x in sorted(res, key=lambda x: x['keyword']) if x['disp'] == 'UNCLUSTERED_REVIEW'))
    elif mode == 'noise':
        print('; '.join(f"{x['keyword']}" for x in sorted(res, key=lambda x: x['keyword']) if x['basis'].startswith('STAGE11_OFFTOPIC')))
    elif mode == 'brand':
        print('; '.join(f"{x['keyword']}[{x['brand']}]" for x in sorted(res, key=lambda x: x['keyword']) if x['basis'].startswith('STAGE11_BRAND')))
