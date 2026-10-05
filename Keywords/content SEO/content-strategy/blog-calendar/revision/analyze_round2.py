"""Round 2 SERP analysis (hard revision). Local files only; no API call.
Reads dataforseo/raw/blog_calendar/revision/R2_serp/<tag>.json (full) or <tag>_condensed.json.
Writes revision/round2_serp_analysis.csv, round2_paa_questions.csv, round2_serp_overlap.csv.
Page-type labels are a disclosed URL/domain/title heuristic, not a manual page audit.
"""
import json, csv, os, re, glob, itertools, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
D = os.path.join(ROOT, 'dataforseo/raw/blog_calendar/revision/R2_serp')
OUT = os.path.join(ROOT, 'content-strategy/blog-calendar/revision')
roles = json.load(open(os.path.join(ROOT, 'content-strategy/blog-calendar/revision/round2_serp_payload.json')))['roles']
manifest = list(csv.DictReader(open(os.path.join(D, 'manifest.csv'))))

FORUM = r'reddit\.com|quora\.com|community\.|forum|weddingwire\.com/wedding-forums|theknot\.com/community'
SOCIAL = r'youtube\.com|tiktok\.com|instagram\.com|facebook\.com|pinterest\.|x\.com|twitter\.com'
MARKET = r'amazon\.|etsy\.com|ebay\.|walmart\.com|target\.com|costco\.com|macys\.com|nordstrom\.com|kohls\.com|jcpenney|zales\.com|kay\.com|jared\.com'
MEDIA = r'vogue|brides\.com|theknot\.com|harpersbazaar|nytimes|cosmopolitan|oprahdaily|people\.com|today\.com|goodhousekeeping|glamour|elle\.com|instyle|byrdie|marthastewart|realsimple|townandcountrymag|businessinsider|cnn\.com|forbes|nbcnews|usatoday|buzzfeed|refinery29|wikihow|verywell|bustle|thezoereport|whowhatwear|mindbodygreen|womansday|countryliving|housebeautiful|southernliving|parents\.com|thebump|whattoexpect|popsugar|nbc|cbs|abc|foxnews|washingtonpost|wsj|nypost|dailymail|yahoo|msn|hallmark|shutterfly|zola\.com|junebugweddings|stylemepretty|weddingwire|nationaljeweler|rapaport|idexonline|jckonline|gia\.edu|igi\.org|4cs'
REF = r'wikipedia\.org|britannica|merriam-webster|dictionary\.|almanac'
EDIT_PATH = r'/blog|/blogs/|/journal|/guide|/guides|/learn|/education|/article|/articles|/news|/stories|/advice|/magazine|/inspiration|/resources|/the-edit|/edit/|/ideas|/how-to|/faq'
PROD_PATH = r'/products?/|/collections?/|/shop|/category|/c/|/jewelry/|/rings?/|/engagement-rings|/wedding-bands|/earrings|/necklaces|/bracelets|/gifts?(/|$)|/p/|/dp/|/itm/|/ip/|/listing/'

def page_type(url, domain, title):
    u = (url or '').lower(); d = (domain or '').lower(); t = (title or '').lower()
    if re.search(FORUM, d + u): return 'FORUM'
    if re.search(SOCIAL, d): return 'SOCIAL_VIDEO'
    if re.search(REF, d): return 'REFERENCE'
    if re.search(MARKET, d): return 'MARKETPLACE_OR_BIG_RETAIL'
    listicle = bool(re.match(r'^\s*(the\s+)?\d{1,3}\s', t)) or bool(re.search(r'\b(best|top)\s+\d{1,3}\b|\b\d{1,3}\s+(best|gift|ideas|ways|gifts)', t))
    if re.search(MEDIA, d): return 'EDITORIAL_LISTICLE' if listicle else 'EDITORIAL_MEDIA'
    if re.search(EDIT_PATH, u): return 'RETAILER_GUIDE_LISTICLE' if listicle else 'RETAILER_GUIDE'
    if re.search(PROD_PATH, u) or re.search(r'\bshop\b|\bbuy\b|for sale|\| .*jewel', t): return 'PRODUCT_OR_CATEGORY'
    return 'LISTICLE_OTHER' if listicle else 'OTHER'

def load(tag):
    f = os.path.join(D, tag + '.json'); fc = os.path.join(D, tag + '_condensed.json')
    if os.path.exists(f):
        j = json.load(open(f)); t = j['tasks'][0]; r = (t.get('result') or [None])[0]
        if not r: return None
        items = r.get('items') or []
        aio = [i for i in items if i['type'] == 'ai_overview']
        paa = [e for i in items if i['type'] == 'people_also_ask' for e in (i.get('items') or [])]
        org = [i for i in items if i['type'] == 'organic']
        rel = [x for i in items if i['type'] == 'related_searches' for x in (i.get('items') or [])]
        refs = []
        for a in aio:
            refs += [x.get('domain') for x in (a.get('references') or []) if x.get('domain')]
        return {'mode': 'FULL', 'cost': t.get('cost'), 'item_types': r.get('item_types') or [],
                'aio_present': bool(aio), 'aio_md': '\n'.join(a.get('markdown') or '' for a in aio),
                'aio_async': [a.get('asynchronous_ai_overview') for a in aio], 'aio_ref_domains': refs,
                'paa': [(e.get('title'), e.get('seed_question')) for e in paa],
                'organic': [(o.get('rank_group'), o.get('domain'), o.get('url'), o.get('title')) for o in org],
                'related': rel}
    if os.path.exists(fc):
        c = json.load(open(fc)); a = c.get('ai_overview') or {}
        return {'mode': 'CONDENSED', 'cost': c.get('task_cost'), 'item_types': c.get('item_types') or [],
                'aio_present': bool(a.get('present')), 'aio_md': a.get('markdown') or '', 'aio_async': [a.get('asynchronous_ai_overview')],
                'aio_ref_domains': a.get('reference_domains') or [],
                'paa': [((p.get('title') if isinstance(p, dict) else p), (p.get('seed_question') if isinstance(p, dict) else None)) for p in c.get('people_also_ask') or []],
                'organic': [(o.get('rank_group'), o.get('domain'), o.get('url'), o.get('title')) for o in c.get('organic') or []],
                'related': c.get('related_searches') or []}
    return None

rows, paa_rows, urls = [], [], {}
for m in manifest:
    s = load(m['tag'])
    if not s:
        rows.append({'tag': m['tag'], 'keyword': m['keyword'], 'retrieval': 'MISSING'}); continue
    types = s['item_types']
    org = s['organic'][:10]
    pts = [page_type(u, d, t) for _, d, u, t in org]
    cnt = collections.Counter(pts)
    commercial = cnt['PRODUCT_OR_CATEGORY'] + cnt['MARKETPLACE_OR_BIG_RETAIL']
    editorial = cnt['EDITORIAL_MEDIA'] + cnt['EDITORIAL_LISTICLE'] + cnt['RETAILER_GUIDE'] + cnt['RETAILER_GUIDE_LISTICLE'] + cnt['LISTICLE_OTHER'] + cnt['REFERENCE']
    ugc = cnt['FORUM'] + cnt['SOCIAL_VIDEO']
    shop_feat = any(x in types for x in ('popular_products', 'shopping', 'refine_products', 'explore_brands', 'product_considerations', 'commercial_units', 'local_pack'))
    if commercial >= 5 or (commercial >= 4 and shop_feat): serp_intent = 'TRANSACTIONAL_OR_COMMERCIAL'
    elif editorial + ugc >= 7 and commercial <= 1: serp_intent = 'INFORMATIONAL' if (cnt['EDITORIAL_LISTICLE'] + cnt['RETAILER_GUIDE_LISTICLE'] + cnt['LISTICLE_OTHER']) < 4 else 'COMMERCIAL_RESEARCH_LISTICLE'
    else: serp_intent = 'MIXED'
    headings = re.findall(r'^#{2,4}\s*(.+)$', s['aio_md'], flags=re.M)
    urls[m['keyword']] = {re.sub(r'[?#].*$', '', u or '').rstrip('/') for _, _, u, _ in org}
    rows.append({'tag': m['tag'], 'keyword': m['keyword'], 'role': roles.get(m['keyword'], ''), 'retrieval': s['mode'], 'task_cost': s['cost'],
                 'ai_overview': s['aio_present'], 'aio_section_headings': ' | '.join(headings[:8]),
                 'aio_reference_domains': '; '.join(list(dict.fromkeys(s['aio_ref_domains']))[:10]),
                 'paa_present': bool(s['paa']), 'paa_count': len(s['paa']), 'paa_questions': ' | '.join(q for q, _ in s['paa'] if q),
                 'related_searches': ' | '.join(s['related'][:8]),
                 'serp_features': ';'.join(types), 'shopping_features': shop_feat,
                 'top10_page_types': '; '.join(f'{k}={v}' for k, v in cnt.most_common()),
                 'commercial_results': commercial, 'editorial_results': editorial, 'forum_social_results': ugc,
                 'dominant_page_type': cnt.most_common(1)[0][0] if cnt else '',
                 'serp_intent_verified': serp_intent,
                 'top5_domains': '; '.join(d for _, d, _, _ in org[:5])})
    for q, seed in s['paa']:
        if q: paa_rows.append({'keyword': m['keyword'], 'tag': m['tag'], 'paa_question': q, 'expanded_from': seed or ''})

cols = list(max(rows, key=len).keys())
with open(os.path.join(OUT, 'round2_serp_analysis.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); [w.writerow({c: r.get(c, '') for c in cols}) for r in rows]
with open(os.path.join(OUT, 'round2_paa_questions.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['keyword', 'tag', 'paa_question', 'expanded_from']); w.writeheader(); w.writerows(paa_rows)
ov = []
for a, b in itertools.combinations(sorted(urls), 2):
    n = len(urls[a] & urls[b])
    if n: ov.append({'keyword_a': a, 'keyword_b': b, 'shared_top10_urls': n})
with open(os.path.join(OUT, 'round2_serp_overlap.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['keyword_a', 'keyword_b', 'shared_top10_urls']); w.writeheader(); w.writerows(sorted(ov, key=lambda r: -r['shared_top10_urls']))
print('serps', sum(1 for r in rows if r['retrieval'] != 'MISSING'), 'missing', sum(1 for r in rows if r['retrieval'] == 'MISSING'),
      'AIO', sum(1 for r in rows if r.get('ai_overview') is True), 'PAA', sum(1 for r in rows if r.get('paa_present') is True),
      'paa_questions', len(paa_rows), 'unique_paa', len({p['paa_question'].lower() for p in paa_rows}),
      'cost_sum', round(sum(float(r['task_cost']) for r in rows if r.get('task_cost') not in ('', None)), 5))
