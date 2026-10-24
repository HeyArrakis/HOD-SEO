"""Read-only live validation crawl (GET only, no forms/logins). Output dir passed as argv[1]."""
import re, json, sys, html, subprocess, os
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
OUT = sys.argv[1]
BASE = "https://www.houseofdiams.com"
UA = "Mozilla/5.0 (compatible; HODSEOAudit/1.0; read-only)"
SENT = b"\n@@CURLW@@"

def fetch(u, cookie=None, follow=False):
    cmd = ["curl","-sS","-m","40","-A",UA,"-D","-","-o","-","-w","\n@@CURLW@@%{time_starttransfer} %{time_total} %{size_download} %{num_redirects} %{url_effective}"]
    if cookie: cmd += ["-H","Cookie: "+cookie]
    if follow: cmd += ["-L"]
    cmd.append(u)
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=60)
    except Exception as ex:
        return dict(status=0, err=str(ex))
    raw = p.stdout
    k = raw.rfind(SENT)
    w = raw[k+len(SENT):].decode().split() if k >= 0 else []
    raw = raw[:k] if k >= 0 else raw
    # take LAST header block when following redirects
    parts = raw.split(b"\r\n\r\n")
    # find the last block starting with HTTP/
    idx = max(i for i,b in enumerate(parts[:-1] if len(parts)>1 else parts) if b.startswith(b"HTTP/")) if any(b.startswith(b"HTTP/") for b in parts) else 0
    head = parts[idx].decode("utf-8","replace"); body = b"\r\n\r\n".join(parts[idx+1:]).decode("utf-8","replace")
    lines = head.split("\r\n")
    try: st = int(lines[0].split()[1])
    except Exception: return dict(status=0, err=p.stderr.decode()[:200])
    h = {}
    for l in lines[1:]:
        if ":" in l:
            a,b = l.split(":",1); h[a.strip().lower()] = h.get(a.strip().lower(), "") + (", " if a.strip().lower() in h else "") + b.strip()
    r = dict(status=st, headers=h, body=body)
    if w:
        r.update(ttfb=float(w[0]), total=float(w[1]), bytes=int(w[2]), redirects=int(w[3]))
    return r

def strip(s): return html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",s))).strip()

def parse(u, r):
    h = r.get("headers",{}); body = r.get("body","")
    row = dict(url=u, status=r["status"], location=h.get("location",""), x_robots=h.get("x-robots-tag",""),
               content_type=h.get("content-type",""), ttfb=r.get("ttfb"), total=r.get("total"),
               html_bytes=r.get("bytes"), cache_control=h.get("cache-control",""), via=h.get("via",""),
               server=h.get("server",""), x_cache=h.get("x-cache",""), set_cookie_currency=("detected_currency" in h.get("set-cookie","")))
    if body and "html" in row["content_type"]:
        t = re.search(r"<title[^>]*>(.*?)</title>", body, re.S); row["title"] = strip(t.group(1)) if t else ""
        m = re.search(r'<meta[^>]+name="description"[^>]*content="([^"]*)"', body) or re.search(r'<meta[^>]+content="([^"]*)"[^>]*name="description"', body)
        row["meta_description"] = html.unescape(m.group(1)) if m else ""
        m = re.search(r'<meta[^>]+name="robots"[^>]*content="([^"]*)"', body); row["meta_robots"] = m.group(1) if m else ""
        m = re.search(r'<link[^>]+rel="canonical"[^>]*href="([^"]*)"', body); row["canonical"] = m.group(1) if m else ""
        row["h1s"] = [strip(x) for x in re.findall(r"<h1[^>]*>(.*?)</h1>", body, re.S)]
        ld = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', body, re.S)
        types=[]; cur=[]; samples=[]
        for blk in ld:
            try: d=json.loads(blk)
            except Exception: types.append("INVALID_JSON"); continue
            samples.append(d)
            def walk(o):
                if isinstance(o,dict):
                    tt=o.get("@type")
                    if tt: types.extend(tt if isinstance(tt,list) else [tt])
                    if "priceCurrency" in o: cur.append(o["priceCurrency"])
                    for v in o.values(): walk(v)
                elif isinstance(o,list):
                    for v in o: walk(v)
            walk(d)
        row["schema_types"]=sorted(set(types)); row["price_currencies"]=sorted(set(cur)); row["ld_blocks"]=len(ld)
        row["ld_json"]=json.dumps(samples)[:5000]
        main = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>"," ",body,flags=re.S)
        row["word_count"]=len(strip(main).split())
        imgs=re.findall(r"<img\b[^>]*>", body); row["img_count"]=len(imgs); row["img_no_alt"]=sum(1 for x in imgs if not re.search(r'alt="[^"]+"',x))
        links=set()
        for hm in re.findall(r'<a\b[^>]*href="([^"#]+)"', body):
            p=urlparse(urljoin(u,hm))
            if p.netloc.endswith("houseofdiams.com"): links.add(p.path.rstrip("/") or "/")
        row["internal_links"]=sorted(links)
        row["hreflang"]=len(re.findall(r"hreflang=",body))
    elif body:
        row["body_head"]=body[:200]
    return row

def work(item):
    u, cookie = item
    r = fetch(u, cookie)
    row = parse(u, r); row["cookie_variant"] = cookie or ""
    sys.stderr.write(f"{row['status']} {u}\n"); return row

if __name__ == "__main__":
    sm = fetch(BASE+"/sitemap.xml")
    open(os.path.join(OUT,"sitemap_2026-10-24.xml"),"w").write(sm["body"])
    urls = re.findall(r"<loc>([^<]+)</loc>", sm["body"])
    extra = ["/contact","/hiphop","/engagement-rings/by-desgin","/engagement-rings/by-desgin/side-stone-rings",
             "/engagement-rings/by-design","/engagement-rings/by-design/side-stone-rings",
             "/shop/fine-jewellery-test-product","/wedding-bands/for-him","/collection","/engagement-rings/round-rings",
             "/hiphop/test-subcat","/robots.txt","/llms.txt","/cart","/login","/search?q=ring",
             "/shop?sort=price","/shop?page=2","/engagement-rings?page=2","/blog?page=2","/this-url-should-404-xyz",
             "/engagement-rings/","/shipping","/returns","/bespoke","/about"]
    for e in extra:
        if BASE+e not in urls: urls.append(BASE+e)
    items=[(u,None) for u in urls]
    with ThreadPoolExecutor(max_workers=4) as ex: out=list(ex.map(work, items))
    json.dump(out, open(os.path.join(OUT,"crawl_2026-10-24.json"),"w"), indent=1)
    sys.stderr.write("DONE\n")
