import re, json, time, sys, urllib.request, urllib.error, html, http.client
from urllib.parse import urlparse, urljoin

BASE = "https://www.houseofdiams.com"
UA = "Mozilla/5.0 (compatible; HODSEOAudit/1.0; read-only)"
urls = [u.strip() for u in open('urls.txt') if u.strip()]
extra = ["/contact", "/hiphop", "/engagement-rings/by-desgin/side-stone-rings", "/engagement-rings/by-desgin",
         "/shop/fine-jewellery-test-product", "/shop/marquise-floral-diamond-engagement-ring",
         "/wedding-bands/for-her/anniversary", "/robots.txt", "/llms.txt", "/education/lab-grown-diamonds",
         "/cart", "/login", "/search?q=ring", "/shop?sort=price"]
for e in extra:
    u = BASE + e
    if u not in urls:
        urls.append(u)

import subprocess
def fetch(u):
    try:
        p = subprocess.run(["curl","-sS","-m","30","-A",UA,"-D","-","-o","-",u],capture_output=True,timeout=40)
    except Exception as ex:
        return 0,{},'',str(ex)
    raw = p.stdout
    # split header blocks (could be multiple with 100-continue; no redirects followed)
    i = raw.find(b"\r\n\r\n")
    head = raw[:i].decode('utf-8','replace'); body = raw[i+4:].decode('utf-8','replace')
    lines = head.split("\r\n")
    try: st = int(lines[0].split()[1])
    except Exception: return 0,{},'',p.stderr.decode()[:200]
    h = {}
    for l in lines[1:]:
        if ':' in l:
            k,v = l.split(':',1); h[k.strip().lower()] = v.strip()
    return st,h,body,h.get('location')

def strip(s):
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))).strip()


from concurrent.futures import ThreadPoolExecutor
def work(u):
    st, h, body, loc = fetch(u)
    row = {"url": u, "status": st, "location": h.get('location','') if st in (301,302,307,308) else '',
           "x_robots": h.get('x-robots-tag', ''), "content_type": h.get('content-type', ''), "server_time_hint": ''}
    if body and 'html' in row['content_type']:
        t = re.search(r'<title[^>]*>(.*?)</title>', body, re.S)
        row['title'] = strip(t.group(1)) if t else ''
        m = re.search(r'<meta[^>]+name="description"[^>]*content="([^"]*)"', body) or re.search(r'<meta[^>]+content="([^"]*)"[^>]*name="description"', body)
        row['meta_description'] = html.unescape(m.group(1)) if m else ''
        m = re.search(r'<meta[^>]+name="robots"[^>]*content="([^"]*)"', body)
        row['meta_robots'] = m.group(1) if m else ''
        m = re.search(r'<link[^>]+rel="canonical"[^>]*href="([^"]*)"', body)
        row['canonical'] = m.group(1) if m else ''
        row['h1s'] = [strip(x) for x in re.findall(r'<h1[^>]*>(.*?)</h1>', body, re.S)]
        row['h2s'] = [strip(x) for x in re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S)][:25]
        ld = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', body, re.S)
        types = []; ldsamples = []
        for blk in ld:
            try:
                d = json.loads(blk)
            except Exception:
                types.append('INVALID_JSON'); continue
            ldsamples.append(d)
            def walk(o):
                if isinstance(o, dict):
                    t = o.get('@type')
                    if t: types.extend(t if isinstance(t, list) else [t])
                    for v in o.values(): walk(v)
                elif isinstance(o, list):
                    for v in o: walk(v)
            walk(d)
        row['schema_types'] = sorted(set(types))
        row['ld_blocks'] = len(ld)
        row['ld_json'] = json.dumps(ldsamples)[:6000]
        m = re.search(r'<meta[^>]+property="og:title"[^>]*content="([^"]*)"', body)
        row['og_title'] = html.unescape(m.group(1)) if m else ''
        main = re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>', ' ', body, flags=re.S)
        row['word_count'] = len(strip(main).split())
        imgs = re.findall(r'<img\b[^>]*>', body)
        row['img_count'] = len(imgs)
        row['img_no_alt'] = sum(1 for x in imgs if not re.search(r'alt="[^"]+"', x))
        links = set()
        for hrefm in re.findall(r'<a\b[^>]*href="([^"#]+)"', body):
            p = urlparse(urljoin(u, hrefm))
            if p.netloc.endswith('houseofdiams.com'):
                links.add(p.path.rstrip('/') or '/')
        row['internal_links'] = sorted(links)
        row['hreflang'] = len(re.findall(r'hreflang=', body))
        row['html_bytes'] = len(body.encode('utf-8'))
    elif body:
        row['body_head'] = body[:300]
    sys.stderr.write(f"{st} {u}\n")
    return row

with ThreadPoolExecutor(max_workers=4) as ex:
    out = list(ex.map(work, urls))
json.dump(out, open('crawl/crawl.json', 'w'), indent=1)
sys.stderr.write("DONE\n")
