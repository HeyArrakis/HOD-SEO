"""Read-only checks of the sonder-hod-seo items against the crawl and live URLs. Usage: check_branch_items.py <date>"""
import json,re,subprocess,sys,collections,html,concurrent.futures as cf
D=sys.argv[1]; B='https://houseofdiams.com'
c=json.load(open(f'crawl_{D}.json')); by={p['url']:p for p in c}
sm=re.findall(r'<loc>([^<]+)</loc>',open(f'sitemap_{D}.xml').read())
def get(u):
    return subprocess.run(['curl','-s','--max-time','40',u],capture_output=True,text=True,errors='ignore').stdout
out={}
# A-01/A-17 sitewide visible text
terms=['overnight','same-day','same day','ready to ship','duties may','signature is required','24 hours','free return','apprais','30-day','30 day','40+ countries','lifetime buyback','craftsmanship warranty','order before']
hits=collections.defaultdict(list)
def scan(u):
    s=get(u); v=re.sub(r'<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>',' ',s,flags=re.S); v=html.unescape(re.sub(r'<[^>]+>',' ',v))
    return u,[(t,re.findall(r'.{0,40}'+re.escape(t)+r'.{0,30}',v,re.I)[:1]) for t in terms if re.search(re.escape(t),v,re.I)]
with cf.ThreadPoolExecutor(4) as ex:
    for u,r in ex.map(scan,sm):
        for t,e in r: hits[t].append((u.replace(B,''),e[0] if e else ''))
out['text_hits']={k:{'pages':len(v),'sample':v[:4]} for k,v in hits.items()}
# A-02 product schema
pd=[];keys=collections.Counter();sizes=[];mat=collections.Counter()
for u in sm:
    p=by.get(u)
    if not p or '/shop/' not in u: continue
    blocks=p.get('ld_json') or []
    if isinstance(blocks,str):
        try: blocks=json.loads(blocks)
        except Exception: blocks=[]
    for b in blocks:
        try: d=json.loads(b) if isinstance(b,str) else b
        except Exception: continue
        for x in (d if isinstance(d,list) else d.get('@graph',[d])):
            if isinstance(x,dict) and x.get('@type')=='Product':
                sizes.append(len(json.dumps(x)))
                m=x.get('material'); mat['list' if isinstance(m,list) else 'single' if m else 'none']+=1
                o=x.get('offers'); o=o[0] if isinstance(o,list) else (o or {})
                sd=o.get('shippingDetails'); sd=sd[0] if isinstance(sd,list) else (sd or {})
                rp=o.get('hasMerchantReturnPolicy') or {}
                keys['product']+=1
                keys['itemCondition_offer']+=bool(o.get('itemCondition')); keys['itemCondition_product']+=bool(x.get('itemCondition'))
                keys['deliveryTime']+=bool(sd.get('deliveryTime')); keys['restockingFee']+=bool(rp.get('restockingFee'))
                keys['countries_le_50']+=len(rp.get('applicableCountry') or [])<=50
out['product_schema']={'counts':dict(keys),'material':dict(mat),'max_bytes':max(sizes or [0]),'median_bytes':sorted(sizes or [0])[len(sizes)//2]}
# A-03
paths=open('../../storefront/next.config.ts',encoding='utf-8').read()
pairs=re.findall(r"\['(/[^']+)',\s*'(/[^']+)'\]",paths)
gone=re.findall(r"'(/[^']+)'",open('../../storefront/lib/gone-paths.ts',encoding='utf-8').read())
def head(u):
    return subprocess.run(['curl','-s','-o','/dev/null','--max-time','40','-w','%{http_code} %{redirect_url}',u],capture_output=True,text=True).stdout
out['redirects']=[(a,head(B+a).replace(B,''),head(B+t).split()[0],t) for a,t in pairs]
out['gone']=[(g,head(B+g).split()[0]) for g in gone]
# A-08
l=get(B+'/llms.txt'); f=get(B+'/llms-full.txt')
out['llms']={'bytes':len(l.encode()),'head':l[:260],'full_bytes':len(f.encode())}
# A-13 inbound links to articles; A-07 links to noindex listings
def links(p):
    v=p.get('internal_links') or []
    if isinstance(v,str):
        try: v=json.loads(v)
        except Exception:
            try:
                import ast; v=ast.literal_eval(v)
            except Exception: v=[]
    return v if isinstance(v,list) else []
arts=[u for u in sm if re.search(r'/(blog|education)/[^/]+',u.replace(B,''))]
inb=collections.Counter()
for u in sm:
    for h in set(links(by[u])) if u in by else []:
        h=h.split('?')[0].split('#')[0]
        h=h if h.startswith('http') else B+h
        if h in arts and h!=u:
            typ='art' if u in arts else ('cat' if not '/shop/' in u else 'pdp')
            if typ in('art','cat'): inb[h]+=1
out['articles']={'n':len(arts),'lt3':[(a.replace(B,''),inb[a]) for a in arts if inb[a]<3],'links_field_type':type(next(iter(by.values())).get('internal_links')).__name__,'sample_links':len(links(by[sm[0]]))}
# Organization
home=by[B+'/'] if B+'/' in by else by.get(B)
txt=json.dumps(home.get('ld_json'))
out['org']={k:(k in txt) for k in ['foundingDate','jobTitle','areaServed','sameAs','founder']}
json.dump(out,open(f'branch_items_{D}.json','w'),indent=1,ensure_ascii=False)
print(json.dumps(out,indent=0,ensure_ascii=False)[:6500])
