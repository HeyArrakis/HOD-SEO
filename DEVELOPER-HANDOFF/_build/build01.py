import csv, json, re, sys
from urllib.parse import urlparse
ROOT="/Users/manavdesai/Desktop/HOD SEO/"
OUT=ROOT+"DEVELOPER-HANDOFF/01-PAGE-BY-PAGE-KEYWORD-IMPLEMENTATION.csv"
op=list(csv.DictReader(open(ROOT+"On-page SEO/01-ON-PAGE-SEO-MASTER.csv",encoding="utf-8-sig")))
qa={x["Row ID"]:x for x in csv.DictReader(open(ROOT+"QA/01-MASTER-SEO-IMPLEMENTATION-MAP.csv",encoding="utf-8-sig"))}
reg={x["target_id"]:x for x in csv.DictReader(open(ROOT+"Keywords/content SEO/architecture/15_target_page_registry.csv",encoding="utf-8-sig"))}
asg={x["Row ID"]:x for x in csv.DictReader(open(ROOT+"On-page SEO/10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv",encoding="utf-8-sig"))}
crawl={}
for x in json.load(open(ROOT+"Technical/2026-10-24-live-validation/crawl_2026-10-24.json")):
    p=urlparse(x["url"]); key=(p.path.rstrip("/") or "/")+(("?"+p.query) if p.query else "")
    # prefer first (sitemap apex) record
    crawl.setdefault(key,x)

def path_of(u):
    if not u.startswith("http"): return None
    p=urlparse(u); return p.path.rstrip("/") or "/"

def norm(s): return re.sub(r"\s+"," ",(s or "").replace("&amp;","&")).strip().lower()

def clip(s,n):
    s=re.sub(r"\s+"," ",s or "").strip()
    return s if len(s)<=n else s[:n-1].rstrip()+"…"

def intent(s): return clip(s.split(" | ")[0],120)

def primary(x):
    a=asg.get(x["Row ID"])
    if a and a["Assignment State"].startswith("ASSIGNED"):
        vol=f" ({a['Volume (US/mo)']}/mo; KD {a['KD']})" if a["Volume (US/mo)"] else ""
        return f"{a['Primary Keyword']}{vol} [{a['Assignment State'].replace('ASSIGNED','ASSIGNED 2026-10-10',1)}]"
    p=x["Primary Keyword"].strip()
    if p.startswith("NONE BY DESIGN"): return "NONE BY DESIGN (brand/utility/index/policy/template page)"
    if p.startswith("NONE — no measured demand"): return "NONE (no measured demand in project datasets; not promoted)"
    if p.startswith("NONE (legacy"): return "NONE (legacy URL)"
    if p.startswith("NONE ASSIGNED"): return "NONE ASSIGNED (conditional/deferred; not planned)"
    if p.startswith("RESERVED"): return clip(p,170)
    p=re.sub(r"^FINAL[^:]*:\s*","",p)
    return clip(p,200)

def secondary(x):
    a=asg.get(x["Row ID"])
    if a and a["Assignment State"].startswith("ASSIGNED") and a["Secondary / Held Keywords"].strip():
        return clip(a["Secondary / Held Keywords"],230)
    s=x["Secondary Keywords"].strip()
    return clip(s,230) if s and s!="—" else ""

def live_overlay(x):
    path=path_of(x["URL"]); st=x["Status"]; cur=x["Current URL Status"]
    notlive=cur.startswith("NOT LIVE") or cur.startswith("NOT BUILT") or x["URL"].startswith(("PLANNED","NOT PLANNED","NOT BUILT"))
    c=crawl.get(path) if path and "<slug>" not in (path or "") else None
    if notlive and c and c["status"]==200: notlive=False
    return path,notlive,c

rows=[]; stats={}
for x in op:
    rid=x["Row ID"]; path,notlive,c=live_overlay(x); grp=x["Row Group"]; st=x["Status"]
    recT=x["Rendered Title Preview"]; recH=x["Recommended H1"]
    # current URL cell
    if x["URL"].startswith(("PLANNED","NOT PLANNED","NOT BUILT")):
        curl="NOT LIVE — "+clip(x["URL"],110)
    elif notlive:
        curl="NOT LIVE (planned path): "+path
    else:
        curl=path if path else x["URL"]
    # live check text
    lc=""
    state=None
    if c and c["status"]==200 and "title" in c:
        h1=(c.get("h1s") or [""])[0]
        tm = norm(c["title"])==norm(recT) if recT and recT not in("N/A","—") else None
        hm = norm(h1)==norm(recH) if recH and recH not in("N/A","—") else None
        canon_ok = c.get("canonical","")
        lc=f"LIVE 2026-10-24: HTTP 200; title {'= spec' if tm else 'differs from spec'}; H1 {'= spec' if hm else 'differs from spec'}; meta robots: {c.get('meta_robots') or 'none set'}; canonical {canon_ok.replace('https://','')}"
        if notlive: lc=lc.replace("LIVE 2026-10-24","LIVE 2026-10-24 (URL now responds)")
        state=("LIVE_SPEC_APPLIED_VERIFIED" if (tm and (hm or hm is None)) else "LIVE_SPEC_NOT_APPLIED")
    elif c:
        lc=f"LIVE 2026-10-24: HTTP {c['status']}"+(f" → {c['location']}" if c.get('location') else "")
    elif path and not notlive and "<slug>" not in path:
        lc="LIVE 2026-10-24: path not in crawl set"
    if rid=="SUB:/fine-jewellery/bracelet/tennis":
        lc="LIVE 2026-10-24: path 301 → /fine-jewellery/bracelet/tennis-bracelet (200, in sitemap, self-canonical)"; state=None; c=None
    # implementation status (controlled)
    if st=="NO CHANGE REQUIRED": impl="NO_CHANGE_REQUIRED"
    elif st=="NOT PLANNED — CONDITIONAL": impl="NOT_PLANNED"
    elif rid=="BC-001" and c and c["status"]==200: impl="PUBLISHED_LIVE_HOLD_VIOLATED"
    elif st=="HOD INPUT REQUIRED": impl="BLOCKED_BY_CLIENT"
    elif st=="GSC BASELINE REQUIRED": impl="BLOCKED_BY_GSC"
    elif st.startswith("CONDITIONAL"): impl="BLOCKED_BY_CLIENT"
    elif st=="PRE-AWS PREPARATION": impl="PLANNED_NOT_LIVE_WRITE_PENDING"
    elif st=="READY FOR IMPLEMENTATION POST-AWS":
        if x["Recommended Action"].startswith("PUBLISH"): impl="PUBLISHED_LIVE_VERIFIED" if (c and c["status"]==200) else "PLANNED_NOT_LIVE_PACKAGE_READY"
        elif notlive: impl="PLANNED_NOT_LIVE"
        elif state=="LIVE_SPEC_APPLIED_VERIFIED": impl="IMPLEMENTED_VERIFIED_LIVE"
        elif state=="LIVE_SPEC_NOT_APPLIED": impl="READY_NOT_YET_APPLIED"
        elif rid=="SUB:/fine-jewellery/bracelet/tennis": impl="NEEDS_DECISION_URL_CHANGED"
        elif x["Recommended Action"]=="REMOVE" and c and c["status"]==404: impl="IMPLEMENTED_VERIFIED_LIVE"; lc=lc+" (removed: 404 + noindex)"
        elif x["Recommended Action"]=="REDIRECT" and c and c["status"]==404: impl="READY_NOT_YET_APPLIED"; lc=lc+" — still 404, no 301 (verified)"
        else: impl="READY_NOT_YET_APPLIED" if c is None or c["status"]==200 else "NEEDS_RECHECK"
    else: impl="NEEDS_RECHECK"
    stats[impl]=stats.get(impl,0)+1
    # action cells
    if c and c["status"]==200 and "title" in c:
        cur_txt=f"CURRENT (live 2026-10-24): title '{clip(c['title'],80)}'; H1 '{clip((c.get('h1s') or [''])[0],70)}'"
    elif c:
        cur_txt=f"CURRENT (live 2026-10-24): HTTP {c['status']}"
    elif grp in("PLANNED BLOG","PLANNED EDUCATION","CONDITIONAL EDUCATION","CONDITIONAL COMMERCIAL") or notlive:
        cur_txt="CURRENT: not live (no page at the documented path)" if x["URL"].startswith("https://") else "CURRENT: not live (no path decided)"
    else:
        cur_txt=f"CURRENT (2026-10-09 baseline): {clip(x['Current Content State'],110)}"
    cur_vs_rec=f"{cur_txt} → RECOMMENDED: {x['Recommended Action']}"
    meta=f"Title: {recT or 'n/a'} | Meta: {clip(x['Recommended Meta'],170) or 'n/a'} | H1: {recH or 'n/a'} | Content: {clip(x['Content Action'],150)}"
    link_schema=f"Links: {clip(x['Internal Links Out'],220)} | Schema: {x['Schema Action']}"+(f" — {clip(x['Recommended Schema'],120)}" if x['Recommended Schema'] and x['Recommended Schema'] not in('—',) else "")
    dep=x["Remaining Dependencies"]
    reg_id=qa[rid]["Registry/Calendar ID"]
    # documented conflicts
    notes=[]
    if rid=="COM-ER-SIDESTONE" or "side-stone" in rid.lower(): pass
    if rid=="LEG-ER-SIDESTONE": notes.append("SOURCE CONFLICT (resolved OD-06): Stage 15 registry URL /engagement-rings/by-desgin/side-stone-rings is 404; owner URL is /engagement-rings/by-design/side-stone-rings")
    if rid=="EDU-WB-TYPES" or rid=="BLOG-WR-TYPES": notes.append("ID alias: calendar content_id BLOG-WR-TYPES = Education page EDU-WB-TYPES (OD-04; calendar target_owner updated 2026-10-10)")
    if rid=="BC-001": notes.append("ALERT: page is LIVE (verified 2026-10-24) although publication was HELD pending F-A1; live title, meta and body say '6–9 days of insured shipping' (insurance unconfirmed). Package files unedited. See 03 FIX-CNT-01")
    if rid=="SUB:/fine-jewellery/bracelet/tennis": notes.append("URL CHANGE NOT IN APPROVED PLAN: live now 301 → /fine-jewellery/bracelet/tennis-bracelet; ownership files still list /tennis — NEEDS_DECISION (03 FIX-URL-02)")
    if grp=="EXISTING ARTICLES (Education-owned)" and x["Ownership Status"].startswith("RATIFIED — page owner"): notes.append("Primary resolved OD-03 (calendar vs Stage 17/19 mismatch)")
    if dep and dep!="—": pass
    blocker=clip(dep,200)+(" | "+" | ".join(notes) if notes else "")
    src=f"On-page SEO/01-ON-PAGE-SEO-MASTER.csv [{rid}]; QA/01-MASTER-SEO-IMPLEMENTATION-MAP.csv [{reg_id}]"
    if reg_id in reg: src+=f"; Keywords/content SEO/architecture/15_target_page_registry.csv [{reg_id}]"
    src+="; On-page SEO/10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv" if grp in("COMMERCIAL CATEGORY","COMMERCIAL SUBCATEGORY","CONDITIONAL COMMERCIAL","CORE LIVE") else ""
    src+="; Keywords/content SEO/FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv" if grp.startswith(("PLANNED","EXISTING","CONDITIONAL EDU")) or rid.startswith("BC-") else ""
    impl_cell=impl+(" | "+lc if lc else "")
    rows.append([rid, x["Page Type"].split(" (")[0] if grp!="PLANNED BLOG" else x["Page Type"], x["Page Name"], curl, primary(x), secondary(x), intent(x["Search Intent"]), cur_vs_rec, meta, link_schema, impl_cell, blocker, src])
hdr=["Page ID","Page type","Page name","Current URL","Primary keyword/topic","Important secondary keywords/topics","Search intent","Current versus recommended SEO action","Required metadata/H1/content action","Relevant internal-link or schema action","Implementation status","Dependency or blocker","Source file/evidence"]
import os; os.makedirs(ROOT+"DEVELOPER-HANDOFF",exist_ok=True)
with open(OUT,"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f,quoting=csv.QUOTE_MINIMAL); w.writerow(hdr); w.writerows(rows)
print(len(rows),stats)
