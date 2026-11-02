"""Compare the dated live crawl with the approved on-page spec (read-only). Usage: verify_spec.py <crawl.json> <out.json>"""
import csv, json, re, sys, html
from urllib.parse import urlparse
ROOT="/Users/manavdesai/Desktop/HOD SEO/"
crawl=json.load(open(sys.argv[1])); out=sys.argv[2]
def P(u):
    p=urlparse(u); return p.path.rstrip("/") or "/"
by={}
for x in crawl:
    if urlparse(x["url"]).query: continue
    by.setdefault(P(x["url"]),x)
def norm(s): return re.sub(r"\s+"," ",html.unescape(s or "")).replace("’","'").strip().lower()
rows=list(csv.DictReader(open(ROOT+"On-page SEO/01-ON-PAGE-SEO-MASTER.csv",encoding="utf-8-sig")))
res=[]
for r in rows:
    if not r["URL"].startswith("https://") or "<slug>" in r["URL"]: continue
    p=P(r["URL"]); x=by.get(p)
    if not x: res.append(dict(id=r["Row ID"],path=p,status=r["Status"],live="not crawled")); continue
    e=dict(id=r["Row ID"],path=p,spec_status=r["Status"],action=r["Recommended Action"],http=x["status"])
    if x["status"]==200 and "title" in x:
        T=r["Rendered Title Preview"]; M=r["Recommended Meta"]; H=r["Recommended H1"]
        e.update(live_title=x["title"],spec_title=T,title_ok=(norm(x["title"])==norm(T)) if T not in("","N/A","—") else None,
                 live_meta=x.get("meta_description",""),spec_meta=M,meta_ok=(norm(x.get("meta_description"))==norm(M)) if M not in("","N/A","—") else None,
                 live_h1=(x.get("h1s") or [""])[0],spec_h1=H,h1_ok=(norm((x.get("h1s") or [""])[0])==norm(H)) if H not in("","N/A","—") else None,
                 robots=x.get("meta_robots",""),canonical=x.get("canonical",""),schema=x.get("schema_types",[]))
    res.append(e)
json.dump(res,open(out,"w"),indent=1)
import collections
live=[e for e in res if e.get("live_title") is not None]
ready=[e for e in live if e["spec_status"]=="READY FOR IMPLEMENTATION POST-AWS"]
print("rows with live page:",len(live),"ready:",len(ready))
for k in("title_ok","meta_ok","h1_ok"):
    print(k,"ready:",collections.Counter(e[k] for e in ready),"all:",collections.Counter(e[k] for e in live))
