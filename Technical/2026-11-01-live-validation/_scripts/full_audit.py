"""Sitewide on-page/technical analysis of a crawl JSON (read-only). Usage: full_audit.py <crawl.json> <deep_scan.json> <sitemap.xml> <out.json>"""
import json, sys, re, ast, collections
crawl, deep, smf, out = sys.argv[1:5]
pages = json.load(open(crawl))
dscan = json.load(open(deep))
sm = set(re.findall(r'<loc>([^<]+)</loc>', open(smf).read()))
def L(v):
    try: return ast.literal_eval(v) if isinstance(v, str) and v.startswith('[') else (v or [])
    except Exception: return []
B = 'https://houseofdiams.com'
P = []
for p in pages:
    p = dict(p); p['path'] = p['url'].replace(B, '') or '/'
    for k in ('h1s','schema_types','internal_links','price_currencies'): p[k] = L(p.get(k))
    for k in ('word_count','img_count','img_no_alt','html_bytes'): p[k] = int(p.get(k) or 0)
    for k in ('ttfb','total'): p[k] = float(p.get(k) or 0)
    P.append(p)
ok = [p for p in P if str(p['status'])=='200' and 'noindex' not in (p.get('meta_robots') or '').lower() and p['url'] in sm]
def ttype(path):
    if path=='/': return 'home'
    s = path.split('/')[1]
    return {'shop':'pdp','blog':'blog','education':'education'}.get(s, 'category' if s in ('engagement-rings','wedding-bands','fine-jewellery','t-bar','collection') else 'other')
for p in P: p['type'] = ttype(p['path'])
R = {}
R['status_counts'] = collections.Counter(p['status'] for p in P)
R['non200'] = [(p['path'], p['status'], p.get('location','')) for p in P if str(p['status'])!='200']
R['sitemap_count'] = len(sm)
R['sitemap_non200_or_noindex'] = [p['path'] for p in P if p['url'] in sm and (str(p['status'])!='200' or 'noindex' in (p.get('meta_robots') or '').lower())]
# titles
tl = collections.defaultdict(list)
for p in ok: tl[p['title']].append(p['path'])
R['title_dupes'] = {t:v for t,v in tl.items() if len(v)>1}
R['title_too_long'] = sorted([(len(p['title']), p['path']) for p in ok if len(p['title'])>60], reverse=True)
R['title_too_short'] = [(len(p['title']), p['path']) for p in ok if len(p['title'])<30]
R['title_missing'] = [p['path'] for p in ok if not p['title']]
# metas
ml = collections.defaultdict(list)
for p in ok: ml[p.get('meta_description','')].append(p['path'])
R['meta_dupes'] = {m:v for m,v in ml.items() if len(v)>1 and m}
R['meta_missing'] = [p['path'] for p in ok if not p.get('meta_description')]
R['meta_too_long'] = sorted([(len(p['meta_description']), p['path']) for p in ok if len(p.get('meta_description') or '')>160], reverse=True)
R['meta_too_short'] = sorted([(len(p['meta_description']), p['path']) for p in ok if 0<len(p.get('meta_description') or '')<70])
R['meta_boilerplate'] = [p['path'] for p in ok if re.match(r'^(Browse|Shop) [^.]{0,40} in [^.]{0,40}\.$', p.get('meta_description') or '')]
# h1
R['h1_missing'] = [p['path'] for p in ok if not p['h1s']]
R['h1_multiple'] = [(p['path'], p['h1s']) for p in ok if len(p['h1s'])>1]
hl = collections.defaultdict(list)
for p in ok:
    if p['h1s']: hl[p['h1s'][0].lower()].append(p['path'])
R['h1_dupes'] = {h:v for h,v in hl.items() if len(v)>1}
# canonical
R['canonical_missing'] = [p['path'] for p in ok if not p.get('canonical')]
R['canonical_not_self'] = [(p['path'], p['canonical'].replace(B,'')) for p in ok if p.get('canonical') and p['canonical'].rstrip('/') != p['url'].rstrip('/')]
# images
R['img_no_alt_pages'] = sorted([(p['img_no_alt'], p['img_count'], p['path']) for p in ok if p['img_no_alt']>0], reverse=True)[:25]
R['img_no_alt_total'] = sum(p['img_no_alt'] for p in ok); R['img_total'] = sum(p['img_count'] for p in ok)
# thin content by type
wc = collections.defaultdict(list)
for p in ok: wc[p['type']].append(p['word_count'])
R['word_count_by_type'] = {t:{'n':len(v),'min':min(v),'median':sorted(v)[len(v)//2],'max':max(v)} for t,v in wc.items()}
R['thin_pages'] = sorted([(p['word_count'], p['path']) for p in ok if (p['type'] in ('category','other') and p['word_count']<250) or (p['type']=='blog' and p['word_count']<600)])[:40]
# schema
R['schema_by_type'] = {}
for t in wc:
    c = collections.Counter(s for p in ok if p['type']==t for s in p['schema_types'])
    R['schema_by_type'][t] = dict(c.most_common(14))
R['faqpage_on'] = [p['path'] for p in ok if 'FAQPage' in p['schema_types']]
R['pdp_missing_product'] = [p['path'] for p in ok if p['type']=='pdp' and 'Product' not in p['schema_types']]
R['blog_missing_article'] = [p['path'] for p in ok if p['type'] in ('blog','education') and p['path'].count('/')>=2 and not ({'BlogPosting','Article'} & set(p['schema_types']))]
R['breadcrumb_missing'] = [p['path'] for p in ok if 'BreadcrumbList' not in p['schema_types']]
R['person_schema'] = [p['path'] for p in ok if 'Person' in p['schema_types']][:10]
# internal links
inl = collections.Counter()
for p in ok:
    for l in set(p['internal_links']): inl[l.split('?')[0].split('#')[0].rstrip('/') or '/'] += 1
R['inlinks_low'] = sorted([(inl.get(p['path'].rstrip('/') or '/',0), p['path']) for p in ok])[:30]
R['orphans'] = [p['path'] for p in ok if inl.get(p['path'].rstrip('/') or '/',0)==0]
alltargets = set(l.split('?')[0].split('#')[0] for p in ok for l in p['internal_links'] if l.startswith('/'))
known = {p['path'] for p in P}
R['link_targets_not_crawled'] = sorted(t for t in alltargets if t not in known and not t.startswith(('/cart','/checkout','/login','/signup','/profile','/wishlist','/api','/_next','/search')))
# speed / weight / headers
R['ttfb'] = {'median': sorted(p['ttfb'] for p in ok)[len(ok)//2], 'p90': sorted(p['ttfb'] for p in ok)[int(len(ok)*.9)], 'max': max(p['ttfb'] for p in ok)}
R['html_kb'] = {'median': sorted(p['html_bytes'] for p in ok)[len(ok)//2]//1024, 'max': max((p['html_bytes']//1024, p['path']) for p in ok)}
R['cache_control_html'] = collections.Counter(p.get('cache_control') for p in ok).most_common(3)
R['x_cache'] = collections.Counter(p.get('x_cache') for p in ok).most_common(3)
R['hreflang_pages'] = sum(1 for p in ok if str(p.get('hreflang'))!='0')
# deep scan: og + claims
D = dscan if isinstance(dscan, list) else dscan.get('rows', dscan)
rows = D if isinstance(D, list) else list(D.values())
R['og_missing'] = [r.get('url','').replace(B,'') for r in rows if isinstance(r, dict) and not {'og:title','og:description','og:image'} <= set(r.get('og', []))][:20]
R['type_counts'] = collections.Counter(p['type'] for p in ok)
R['indexable_ok'] = len(ok)
json.dump(R, open(out,'w'), indent=1, default=str)
for k,v in R.items():
    s = json.dumps(v, default=str)
    print(f'{k}: {s[:600]}')
