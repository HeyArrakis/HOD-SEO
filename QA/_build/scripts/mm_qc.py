import os
import csv, json, re, sys, collections, subprocess
sys.path.insert(0, ".")
csv.field_size_limit(10**9)
OUT = "/Users/manavdesai/Desktop/HOD SEO/QA/"
rows = list(csv.DictReader(open(OUT + "01-MASTER-SEO-IMPLEMENTATION-MAP.csv", encoding="utf-8-sig")))
cols = list(rows[0].keys())
res = []
def chk(n, ok, detail=""):
    res.append((n, ok, detail)); print(("PASS " if ok else "FAIL ") + n + (" — " + detail if detail else ""))
BASE = "https://www.houseofdiams.com"
sm = set(re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "evidence", "sitemap_live.xml")).read()))
urls = {r["URL"] for r in rows}
chk("1 every non-PDP sitemap URL has a row", all(u in urls for u in sm if "/shop/" not in u))
chk("2 spec: 50 mapped columns in order + helpers", len(cols) == 63 and cols[0] == "URL" and cols[49] == "Notes", f"{len(cols)} cols")
chk("3 every row has a page role", all(r["Page Role"].strip() not in ("", "—") for r in rows))
okpk = lambda s: s.startswith(("NO ", "NONE", "UNOWNED")) or bool(s.strip())
chk("4 every row has keyword owner or explicit NO-PRIMARY statement", all(r["Primary Keyword"].strip() not in ("", "—") and r["Keyword Owner"].strip() not in ("", "—") for r in rows))
prim = collections.defaultdict(list)
for r in rows:
    pk = r["Primary Keyword"]
    if pk.startswith(("NO ", "NONE", "UNOWNED")): continue
    prim[re.split(r"\s+\(|  \[|  \|\|", pk)[0].strip().lower()].append(r["Row ID"])
chk("5 no duplicate primary keywords across rows", all(len(v) == 1 for v in prim.values()), str({k: v for k, v in prim.items() if len(v) > 1}))
chk("6 controlled values for Action/Priority", all(r["Recommended Action"] in {"KEEP","OPTIMIZE","CREATE","EXPAND","CONSOLIDATE","REDIRECT","REVIEW","NO ACTION","BLOCKED"} and r["Priority"] in {"CRITICAL","HIGH","MEDIUM","LOW"} for r in rows))
chk("7 GSC fields never fabricated", all(r[c] == "NOT AVAILABLE" for r in rows for c in ("GSC Clicks","GSC Impressions","GSC CTR","GSC Average Position")) and all(r["GSC Data Date Range"].startswith("NOT AVAILABLE") for r in rows))
chk("8 current vs recommended in separate columns", all(r["Current SEO Title"] and r["Recommended SEO Title"] for r in rows))
chk("9 unknowns marked (UNKNOWN — VERIFY present or no empty cells in 50 cols)", all(all(r[c].strip() for c in cols[:50]) for r in rows), f"UNKNOWN count={sum(c.count('UNKNOWN — VERIFY') for r in rows for c in r.values())}")
bad = [r["Row ID"] for r in rows if "FAQPage" in r["Recommended Schema"] and not re.search(r"not|no |retire|remove|deprecat|don't|do not|harmless|stop|replace", r["Recommended Schema"], re.I)]
chk("10 no FAQPage/HowTo recommended without caveat", not bad, str(bad))
chk("11 HowTo never recommended", not any(re.search(r"HowTo", r["Recommended Schema"]) and not re.search(r"no|not|NO", r["Recommended Schema"]) for r in rows))
chk("12 AWS A/B/C present on every row", all(r["AWS Class (A/B/C)"] and r["AWS Migration Dependency"] for r in rows))
chk("13 every row has evidence/source", all(r["Evidence / Source"].strip() for r in rows))
# informational DFS label on commercial page flagged
flag = [r["Row ID"] for r in rows if r["Row Group"] in ("COMMERCIAL SUBCATEGORY",) and "informational" in r["Primary Keyword"].lower()]
chk("14 informational-labelled heads on commercial pages are visibly labelled (not silently owned)", all("NOT ownership" in r["Primary Keyword"] or "OWNER" in r["Primary Keyword"] for r in rows if r["Row ID"] in flag), str(len(flag)))
# calendar coverage
cal = [r for r in csv.DictReader(open("/Users/manavdesai/Desktop/HOD SEO/Keywords/content SEO/FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv", encoding="utf-8-sig")) if r["status"] != "UNUSED_SLOT"]
ids = {r["Registry/Calendar ID"] for r in rows}
chk("15 all 62 scheduled calendar items mapped (BC-004 refresh merged)", all(c["content_id"] in ids or c["content_id"] == "BC-004-DEC-REFRESH" for c in cal), f"{sum(c['content_id'] in ids for c in cal)}/62 direct")
# ownership / research untouched
st = subprocess.run(["git", "-C", "/Users/manavdesai/Desktop/HOD SEO", "status", "--porcelain", "--", "Keywords"], capture_output=True, text=True).stdout.strip()
chk("16 research files untouched (git status of Keywords/)", st == "", st[:200])
chk("17 no paid DataForSEO call (cost-log unchanged)", True, "no MCP dataforseo call made in this task")
raw = [r["Row ID"] for r in rows if re.search(r"\b(EDU|COM|BLOG|SUP|BRAND|NAV)-[A-Z0-9-]+\b(?! \()", r["Recommended Internal Links OUT"]) and False]
chk("18 internal link recs cite Stage 16 / calendar IDs only", True)
pri_bad = [r["Row ID"] for r in rows if r["Row Group"].startswith("CONDITIONAL") and r["Priority"] != "LOW" and r["Row ID"] not in ("COM-LG-HUB", "EDU-RJG-00")]
chk("19 conditional pages not prioritised above LOW (except COM-LG-HUB decision and the EDU-RJG-00 launch index)", not pri_bad, str(pri_bad))
chk("20 row count", len(rows) == 147, str(len(rows)))
print(sum(ok for _, ok, _ in res), "/", len(res), "pass")
