import os
import csv, json, collections, sys, re
sys.path.insert(0, ".")
import lib_research as L
from mm_core import *
import mm_live, mm_cat, mm_special, mm_content

rows = []
rows += mm_live.core_rows()
rows += mm_content.hub_rows()
rows += mm_cat.hub_rows()
rows += mm_cat.sub_rows()
rows += mm_special.special_rows()
rows += mm_content.existing_rows()
rows += mm_content.planned_edu_rows()
rows += mm_content.blog_rows()

# fill defaults + validate
for i, r in enumerate(rows, 1):
    for c in COLS:
        if c not in r:
            r[c] = ""
    if not r["GSC Clicks"]:
        gsc_na(r)
    for c in ("Current SEO Title", "Current Meta Description", "Current H1", "Current Canonical", "Current Indexability", "Current URL Status", "Current Schema"):
        if not r[c]:
            r[c] = UNK
    r["Row ID"] = r["Row ID"] or f"R{i:03d}"
    assert r["Recommended Action"] in ACTIONS, (r["URL"], r["Recommended Action"])
    assert r["Priority"] in PRIOS, (r["URL"], r["Priority"])
    assert r["Page Role"], r["URL"]
    assert r["Primary Keyword"], r["URL"]
    for c in COLS[:50]:
        if r[c] == "":
            r[c] = "—"

ORDER = ["CORE LIVE", "HUBS", "COMMERCIAL CATEGORY", "COMMERCIAL SUBCATEGORY", "PRODUCT PAGES", "EXISTING ARTICLES (Education-owned)", "LEGACY / REDIRECT", "PLANNED EDUCATION", "CONDITIONAL EDUCATION", "CONDITIONAL COMMERCIAL", "PLANNED BLOG"]
rows.sort(key=lambda r: ORDER.index(r["Row Group"]))
json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "evidence", "rows.json"), "w"), indent=1)
print(len(rows))
print(collections.Counter(r["Row Group"] for r in rows))
print(collections.Counter(r["Recommended Action"] for r in rows))
print(collections.Counter(r["Priority"] for r in rows))
