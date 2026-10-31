"""Targeted read-only checks for the 2026-10-27 verification. Usage: probe_2026-10-27.py <crawl.json> <out.json>"""
import subprocess, re, html, json, sys, glob, csv, collections
from urllib.parse import urlparse
ROOT="/Users/manavdesai/Desktop/HOD SEO/"
UA="Mozilla/5.0 (compatible; HODSEOAudit/1.0; read-only)"; B="https://houseofdiams.com"
crawl=json.load(open(sys.argv[1])); OUT=sys.argv[2]
def P(u): p=urlparse(u); return p.path.rstrip("/") or "/"
by={}
for x in crawl:
    if not urlparse(x["url"]).query: by.setdefault(P(x["url"]),x)
def get(p):
    r=subprocess.run(["curl","-sS","-m","40","-A",UA,"-w","\n@@%{http_code}",B+p],capture_output=True,text=True).stdout
    i=r.rfind("\n@@"); return r[:i], r[i+3:]
def text(b): return html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>"," ",b,flags=re.S))))
def robots(b): m=re.search(r'name="robots"[^>]*content="([^"]*)"',b); return m.group(1) if m else ""
o={}
sm=open(ROOT+"Technical/2026-10-31-live-validation/sitemap_2026-10-31.xml").read()
smp={P(u) for u in re.findall(r"<loc>([^<]+)</loc>",sm)}
# 1 empty listings
emp=["/collection","/engagement-rings/round-rings","/wedding-bands/for-him","/wedding-bands/for-him/classic","/wedding-bands/for-him/diamonds","/wedding-bands/for-him/designer","/wedding-bands/for-her/nature","/wedding-bands/for-her/solid","/wedding-bands/for-her/cigar-band","/wedding-bands/for-her/pavee","/fine-jewellery/earrings/tennis-earrings","/fine-jewellery/earrings/personalized-charm","/fine-jewellery/necklaces/tennis-necklace","/fine-jewellery/necklaces/initials","/fine-jewellery/rings/eternity-rings"]
o["empty"]={}
for p in emp:
    b,s=get(p); t=text(b); m=re.search(r"(\d+)\s+pieces?",t)
    o["empty"][p]=dict(status=s,robots=robots(b),in_sitemap=p in smp,pieces=m.group(0) if m else None,product_links=len(set(re.findall(r'href="(/shop/[^"#?]+)"',b))))
# 2 trust/policy text (static HTML)
kws=["test desc","new test","tesxt","new pointer","New line","insured","Insured","overnight","Overnight","IGI","Certified","certified","Lifetime","lifetime","warranty","Warranty","15-day","15 day","30-day","30 day","4–6","4-6","2–3 weeks","3–4 weeks","6–9","September sale","HOUSEOFDIAMS2026","free worldwide","Free Worldwide","FREE WORLDWIDE"]
o["text"]={}
for p in ["/","/shipping","/returns","/faq","/bespoke","/about","/contact","/engagement-rings","/shop/rosette-five-flower-bracelet","/shop/oval-floral-diamond-ring","/blog/how-long-does-a-custom-engagement-ring-take"]:
    b,s=get(p); t=text(b)
    hits={k:t.count(k) for k in kws if t.count(k)}
    ctx={k:[t[max(0,m.start()-70):m.end()+70] for m in re.finditer(re.escape(k),t)][:2] for k in hits}
    o["text"][p]=dict(status=s,hits=hits,ctx=ctx,h1=[text(x).strip() for x in re.findall(r"<h1[^>]*>(.*?)</h1>",b,re.S)][:2],mailto=sorted(set(re.findall(r'mailto:([^"?\\]+)',b))))
# 3 education hubs + planned paths must not be public
hubs=["lab-grown-diamonds","diamond-4cs","diamond-shapes","certification-and-grading","metals-and-materials","ring-and-jewelry-guides"]
o["hubs"]={}
for h in hubs:
    b,s=get("/education/"+h); o["hubs"][h]=dict(status=s,robots=robots(b),in_sitemap=("/education/"+h) in smp)
o["education_sitemap"]=sorted(p for p in smp if p.startswith("/education"))
o["blog_sitemap"]=sorted(p for p in smp if p.startswith("/blog/"))
# 4 blogs vs packages
blog_index=set()
for q in ["/blog","/blog?page=2","/blog?page=3"]:
    b,s=get(q); blog_index|=set(re.findall(r'href="(?:https?://[^/"]+)?(/blog/[^"#?]+)"',b))
o["blogs"]={}
for f in sorted(glob.glob(ROOT+"Keywords/content SEO/blogs/bc-*/seo-metadata.md")):
    bc=f.split("/")[-2]; t=open(f).read()
    title=re.search(r"\*\*SEO title\*\* \| (.*?) \|",t).group(1).strip()
    meta=re.search(r"\*\*Meta description\*\* \| (.*?)(?: \(\d+ characters\))? \|",t).group(1).strip()
    h1=re.search(r"\*\*H1\*\* \| (.*?) \|",t).group(1).strip()
    slug=re.search(r"`(/blog/[^`]+)`",t).group(1)
    il=open(f.replace("seo-metadata.md","internal-links.md")).read()
    sec=il.split("## Template-level")[0]
    want=[]
    for line in sec.splitlines():
        if not line.startswith("|") or "LIVE" not in line: continue
        m=re.search(r"`(/[^`]*)`",line)
        if m: want.append(m.group(1).rstrip("/") or "/")
    b,s=get(slug); tt=text(b)
    lt=html.unescape((re.search(r"<title[^>]*>(.*?)</title>",b,re.S) or [0,""])[1]).replace(" | House of Diams","").strip()
    lm=html.unescape((re.search(r'name="description"[^>]*content="([^"]*)"',b) or [0,""])[1])
    lh=[text(x).strip() for x in re.findall(r"<h1[^>]*>(.*?)</h1>",b,re.S)][:1]
    canon=(re.search(r'rel="canonical"[^>]*href="([^"]*)"',b) or [0,""])[1]
    links={ (urlparse(u).path.rstrip("/") or "/") for u in re.findall(r'<a\b[^>]*href="([^"#]+)"',b) if "houseofdiams.com" in u or u.startswith("/")}
    imgs=re.findall(r"<img\b[^>]*>",b)
    # article body images only (inside <article> if present)
    art=re.search(r"<article\b.*?</article>",b,re.S); aimgs=re.findall(r"<img\b[^>]*>",art.group(0)) if art else []
    o["blogs"][bc]=dict(slug=slug,status=s,title_ok=lt==title,meta_ok=lm.strip()==meta.strip(),h1_ok=(lh[:1]==[h1]),live_h1=lh,pkg_h1=h1,canonical=canon,
        self_canonical=canon.rstrip("/").endswith(slug),in_sitemap=slug in smp,in_blog_index=slug in blog_index,
        pkg_links=len(want),missing_links=[w for w in want if w not in links],
        article_imgs=len(aimgs),article_imgs_no_alt=sum(1 for x in aimgs if not re.search(r'alt="[^"]+"',x)),
        img_hosts=sorted(set(re.findall(r'src="https?://([^/"]+)/',art.group(0) if art else ""))),
        insured="insured" in tt.lower(), words=len(tt.split()))
# 5 nav / labels (homepage + engagement rings + wedding bands + fine jewellery static HTML)
lab={}
for p in ["/","/engagement-rings","/wedding-bands","/fine-jewellery"]:
    b,s=get(p); t=text(b)
    for k in ["SOLITARE","Solitare","Anniversay","ANNIVERSAY","BY DESGIN","By Desgin","TOI-MOI","Toi-Moi","Pavee","PAVEE","Jewellery","JEWELLERY","Solatire"]:
        c=t.count(k)
        if c: lab.setdefault(p,{})[k]=c
o["labels"]=lab
# 6 llms.txt
b,s=get("/llms.txt"); o["llms"]=dict(status=s,removed_or_empty_listed=[p for p in emp+["/hiphop/test-subcat","/hiphop/chains"] if re.search(re.escape(p)+r"[)\s\"]",b)],www=b.count("www.houseofdiams.com"))
# 7 PDP name vs H1, titles
mism=[]; long=0; tot=0
for p,x in by.items():
    if not p.startswith("/shop/") or "Product" not in x.get("schema_types",[]) : continue
    tot+=1
    names=re.findall(r'"@type": "Product", "name": "([^"]*)"',x["ld_json"]) or re.findall(r'"name": "([^"]*)"[^{}]*"@type": "Product"',x["ld_json"])
    if not names:
        try:
            d=json.loads(x["ld_json"]); 
            def w(o_,acc):
                if isinstance(o_,dict):
                    if o_.get("@type")=="Product": acc.append(o_.get("name"))
                    for v in o_.values(): w(v,acc)
                elif isinstance(o_,list):
                    for v in o_: w(v,acc)
            acc=[]; w(d,acc); names=acc
        except Exception: pass
    h=(x.get("h1s") or [""])[0]
    if names and (names[0] or "").strip().lower()!=h.strip().lower(): mism.append((p,h,names[0]))
    if len(x["title"])>60: long+=1
o["pdp"]=dict(analysed=tot,name_ne_h1=len(mism),examples=mism[:5],title_over_60=long)
# 8 internal links spec (51 previously missing)
lk=list(csv.DictReader(open(ROOT+"On-page SEO/05-INTERNAL-LINK-IMPLEMENTATION.csv",encoding="utf-8-sig")))
links={P(x["url"]):set(x.get("internal_links",[])) for x in crawl if x["url"].startswith(B) and x["status"]==200 and "internal_links" in x}
res=collections.Counter(); still=[]
for r in lk:
    if not r["Present In Live HTML?"].startswith("NOT FOUND"): continue
    s_=P(r["Source URL"]) if r["Source URL"].startswith("/") else None; t_=r["Destination URL"].rstrip("/") or "/"
    if s_ not in links: res["source not crawled"]+=1; continue
    if t_ in links[s_]: res["now present"]+=1
    else: res["still missing"]+=1; still.append((r["Link ID"],s_,t_,r["Stage 16 Priority"]))
o["links51"]=dict(counts=res,still=still)
req=collections.Counter()
for r in lk:
    if r["Required At Launch"]=="YES" and r["Source Status"].startswith("LIVE") and not r["Destination Status"].startswith("PLANNED"):
        s_=P(r["Source URL"]); t_=r["Destination URL"].rstrip("/") or "/"
        req["src_not_crawled" if s_ not in links else ("present" if t_ in links[s_] else "missing")]+=1
o["required_live_links"]=req
json.dump(o,open(OUT,"w"),indent=1)
print(json.dumps({k:(v if k not in("text","blogs") else None) for k,v in o.items()},indent=0)[:5000])
