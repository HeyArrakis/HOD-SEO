"""Read-only deep scan: visible text claims/typos, schema fields, link hygiene, head tags. Usage: deep_scan.py <sitemap.xml> <crawl.json> <out.json>"""
import re, json, sys, html, subprocess
from concurrent.futures import ThreadPoolExecutor
SM, CRAWL, OUT = sys.argv[1:4]
urls = re.findall(r"<loc>([^<]+)</loc>", open(SM).read())
crawl = {x["url"].rstrip("/"): x for x in json.load(open(CRAWL))}
def get(u):
    p = subprocess.run(["curl","-sS","-m","40","-A","Mozilla/5.0 (compatible; HODSEOAudit/1.0; read-only)",u],capture_output=True)
    return p.stdout.decode("utf-8","replace")
def txt(b):
    b = re.sub(r"<(script|style|noscript|svg)[^>]*>.*?</\1>"," ",b,flags=re.S)
    return html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",b))).strip()
CLAIMS = {"30 days":r"30[- ]day|30 days","craftsmanship warranty":r"craftsmanship warranty","3 PM":r"3 ?PM","September sale":r"September","buyback":r"buy-?back","tesxt":r"tesxt","Jwelery/Jewelery":r"J[a-z]*welery|Jwel","Hero banner":r"Hero banner","Solitare/Anniversay (visible)":r"Solitare|Anniversay|Solatire","Jewellery (visible)":r"Jewellery","40+ countries":r"40\+ countries","New York":r"New York","lorem/test":r"\blorem\b|\btest (desc|product|article)\b|new test","Vermil":r"Vermil\b"}
def scan(u):
    b = get(u); t = txt(b); row = {"url":u}
    row["claims"] = {k:len(re.findall(v,t,re.I)) for k,v in CLAIMS.items() if re.search(v,t,re.I)}
    row["www_links"] = len(re.findall(r'href="https://www\.houseofdiams\.com',b))
    row["abs_apex_links"] = len(re.findall(r'href="https://houseofdiams\.com',b))
    row["lang"] = (re.search(r'<html[^>]*lang="([^"]*)"',b) or [None,None])[1]
    row["og"] = sorted(set(re.findall(r'property="(og:[a-z:_]+)"',b)))
    row["twitter"] = sorted(set(re.findall(r'name="(twitter:[a-z:_]+)"',b)))
    row["viewport"] = bool(re.search(r'name="viewport"',b))
    imgs = re.findall(r"<img\b[^>]*>", b)
    row["img_empty_alt"] = sum(1 for x in imgs if re.search(r'alt=""',x)); row["img_missing_alt"] = sum(1 for x in imgs if "alt=" not in x)
    row["img_no_dims"] = sum(1 for x in imgs if "width=" not in x)
    row["img_hosts"] = sorted(set(re.findall(r'src="https?://([^/"]+)',"".join(imgs))))
    row["h2"] = len(re.findall(r"<h2\b",b))
    lds = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', b, re.S); objs=[]; errs=0
    for l in lds:
        try:
            j = json.loads(l); objs += j if isinstance(j,list) else [j]
        except Exception: errs += 1
    row["ld_errors"] = errs
    flat=[]
    def walk(o):
        if isinstance(o,dict):
            flat.append(o); [walk(v) for v in o.values()]
        elif isinstance(o,list): [walk(v) for v in o]
    walk(objs)
    prod = [o for o in flat if o.get("@type")=="Product"]
    if prod:
        p=prod[0]; off=p.get("offers") or {}
        if isinstance(off,list): off=off[0] if off else {}
        row["product"] = {"name":p.get("name"),"brand":bool(p.get("brand")),"sku":bool(p.get("sku")),"image":bool(p.get("image")),"description":bool(p.get("description")),"rating":bool(p.get("aggregateRating")),"review":bool(p.get("review")),"offer_type":off.get("@type"),"price":off.get("price") or off.get("lowPrice"),"currency":off.get("priceCurrency"),"availability":off.get("availability"),"priceValidUntil":bool(off.get("priceValidUntil")),"shippingDetails":bool(off.get("shippingDetails")),"returnPolicy":bool(off.get("hasMerchantReturnPolicy")),"url":off.get("url"),"gtin_mpn":bool(p.get("gtin") or p.get("gtin13") or p.get("mpn")),"material":p.get("material")}
    arts = [o for o in flat if o.get("@type") in ("BlogPosting","Article","NewsArticle")]
    if arts:
        a=arts[0]; au=a.get("author"); au=au[0] if isinstance(au,list) else au
        row["article"]={"author_type":(au or {}).get("@type"),"author":(au or {}).get("name"),"datePublished":a.get("datePublished"),"dateModified":a.get("dateModified"),"image":bool(a.get("image")),"publisher":bool(a.get("publisher"))}
    row["types"] = sorted(set(str(o.get("@type")) for o in flat))
    c = crawl.get(u.rstrip("/"),{})
    row["title"]=c.get("title"); row["meta"]=c.get("meta_description"); row["h1s"]=c.get("h1s"); row["canonical"]=c.get("canonical"); row["robots"]=c.get("meta_robots"); row["words"]=c.get("word_count"); row["links"]=c.get("internal_links",[])
    return row
with ThreadPoolExecutor(6) as ex: rows = list(ex.map(scan, urls))
json.dump(rows, open(OUT,"w"), ensure_ascii=False, indent=1)
print("scanned", len(rows))
