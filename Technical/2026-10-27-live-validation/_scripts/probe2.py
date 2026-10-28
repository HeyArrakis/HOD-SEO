import subprocess, re, html, json, sys
UA="Mozilla/5.0 (compatible; HODSEOAudit/1.0; read-only)"
B="https://houseofdiams.com"
def get(p, cookie=None):
    cmd=["curl","-sS","-m","40","-A",UA,"-w","\n@@%{http_code}"]
    if cookie: cmd+=["-H","Cookie: "+cookie]
    r=subprocess.run(cmd+[B+p],capture_output=True,text=True).stdout
    i=r.rfind("\n@@"); return r[:i], r[i+3:]
def text(b):
    return html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>"," ",b,flags=re.S))))
out={}
empties=["/collection","/engagement-rings/round-rings","/wedding-bands/for-him","/wedding-bands/for-him/classic","/wedding-bands/for-him/diamonds","/wedding-bands/for-him/designer","/wedding-bands/for-her/nature","/wedding-bands/for-her/solid","/wedding-bands/for-her/cigar-band","/wedding-bands/for-her/pavee","/fine-jewellery/earrings/tennis-earrings","/fine-jewellery/earrings/personalized-charm","/fine-jewellery/necklaces/tennis-necklace","/fine-jewellery/necklaces/initials","/fine-jewellery/rings/eternity-rings"]
for p in empties:
    b,s=get(p); t=text(b)
    m=re.search(r"(\d+)\s+pieces?",t); out["empty:"+p]=dict(status=s, pieces=m.group(0) if m else None, no_match=("No pieces match" in t), product_links=len(set(re.findall(r'href="(/shop/[^"#?]+)"',b))), robots=(re.search(r'name="robots"[^>]*content="([^"]*)"',b) or [None,None])[1])
for p,kws in {"/shipping":["test desc","new test","overnight","insur","2–3","business day"],"/returns":["15 day","30 day","15-day","30-day","return window","legitimate"],"/bespoke":["4–6","4-6","2–3 weeks","3–4 weeks","6–9"],"/":["IGI","GIA","Lifetime","Overnight","September sale","HOUSEOFDIAMS2026","New line","Certified"],"/about":["IGI","GIA","Lifetime","founder"],"/faq":["overnight","IGI","insured"],"/contact":["@houseofdiams","mailto"]}.items():
    b,s=get(p); t=text(b)
    out["page:"+p]=dict(status=s, **{"kw:"+k:t.count(k) for k in kws if k!="mailto"}, mailto=sorted(set(re.findall(r'mailto:([^"?]+)',b)))[:3], h1=[text(x) for x in re.findall(r"<h1[^>]*>(.*?)</h1>",b,re.S)][:1])
b,s=get("/robots.txt"); out["robots_sitemap_lines"]=[l for l in b.splitlines() if l.lower().startswith("sitemap")]
b,s=get("/llms.txt"); out["llms_hosts"]={h:b.count(h) for h in ["www.houseofdiams.com","//houseofdiams.com"]}; out["llms_len"]=len(b)
b,s=get("/"); out["home"]=dict(title=(re.search(r"<title[^>]*>(.*?)</title>",b,re.S) or [0,""])[1], www_refs=b.count("www.houseofdiams.com"), apex_refs=b.count("//houseofdiams.com"), og_url=(re.search(r'property="og:url"[^>]*content="([^"]*)"',b) or [0,None])[1], supabase=len(re.findall("supabase",b)), r2=len(re.findall(r"r2\.dev",b)), media_host=b.count("media.houseofdiams.com"), h1=[text(x) for x in re.findall(r"<h1[^>]*>(.*?)</h1>",b,re.S)][:1])
b,s=get("/shop/rosette-five-flower-bracelet"); out["pdp"]=dict(status=s, supabase=len(re.findall("supabase",b)), r2=len(re.findall(r"r2\.dev",b)), media_host=b.count("media.houseofdiams.com"), www_refs=b.count("www.houseofdiams.com"))
# currency check with US cookie
for ck,lab in [(None,"default"),("detected_country=US; detected_currency=USD","US_cookie"),("detected_country=IN; detected_currency=INR","IN_cookie")]:
    b,s=get("/shop/rosette-five-flower-bracelet", ck)
    cur=re.findall(r'"priceCurrency":\s*"([A-Z]{3})"',b); pr=re.findall(r'"price":\s*"?([\d.]+)',b)
    out["pdp_currency_"+lab]=dict(schema_currency=sorted(set(cur)), schema_price=pr[:2], rupee_symbol=text(b).count("₹"), dollar_symbol=text(b).count("$"))
json.dump(out,open(sys.argv[1],"w"),indent=1)
print(json.dumps(out,indent=1)[:6000])
