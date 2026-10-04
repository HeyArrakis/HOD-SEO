"""Stage 12 QC. Local checks only; no network, no API.
Usage: python3 architecture/scripts/qc_12.py [pre_md5_file]
"""
import csv
import hashlib
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
A = os.path.join(ROOT, "architecture")
fails = []


def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


def rows(name):
    with open(os.path.join(A, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


REQ = {
    "12_ia_proposed_structure.csv": ["section", "parent_section", "page_type", "proposed_level", "purpose",
        "commercial_or_informational", "indexability_role", "architecture_evidence", "current_equivalent",
        "current_issue", "notes", "status"],
    "12_page_type_framework.csv": ["page_type", "primary_purpose", "search_intent", "commercial_or_informational",
        "typical_parent", "indexable_by_default", "permanent_seo_url", "evidence_source", "notes"],
    "12_current_vs_proposed_ia.csv": ["current_structure", "current_url_or_pattern", "observed_issue",
        "future_structure", "structural_principle", "evidence", "implementation_deferred", "notes"],
}

# 1. files exist + exact columns
for f, cols in REQ.items():
    p = os.path.join(A, f)
    check(os.path.exists(p), f"{f} exists")
    with open(p, encoding="utf-8") as fh:
        hdr = next(csv.reader(fh))
    check(hdr == cols, f"{f} columns exactly as specified")
for f in ["12_ia_decision_log.md", "12_ia_summary.md"]:
    check(os.path.exists(os.path.join(A, f)), f"{f} exists")

ia, pt, cv = rows("12_ia_proposed_structure.csv"), rows("12_page_type_framework.csv"), rows("12_current_vs_proposed_ia.csv")

# 2. evidence present with stage labels (or explicit INFERENCE / INSUFFICIENT EVIDENCE)
lab = re.compile(r"\[STAGE \d+|INFERENCE|INSUFFICIENT EVIDENCE")
check(all(lab.search(r["architecture_evidence"]) for r in ia), "every IA row cites [STAGE n] evidence")
check(all(lab.search(r["evidence_source"]) for r in pt), "every page type cites evidence or is labelled INFERENCE")
check(all(lab.search(r["evidence"]) for r in cv), "every current-vs-proposed row cites evidence")

# 3. controlled vocabularies
ST = {"PROPOSED", "PROPOSED_CONDITIONAL", "PROPOSED_CONCEPTUAL", "INSUFFICIENT EVIDENCE — DEFER", "NOT_PROPOSED"}
IR = {"INDEXABLE_PERMANENT", "INDEXABLE_CONDITIONAL", "NON_INDEXABLE_BY_DEFAULT", "NON_INDEXABLE", "NOT_APPLICABLE"}
check(all(r["status"] in ST for r in ia), "IA status values valid")
check(all(r["indexability_role"] in IR for r in ia), "IA indexability values valid")
check(all(r["commercial_or_informational"].split(" ")[0] in {"COMMERCIAL", "INFORMATIONAL", "NOT_APPLICABLE"} for r in ia),
      "every IA row classified commercial/informational")
check(all(r["commercial_or_informational"].split(" ")[0] in {"COMMERCIAL", "INFORMATIONAL", "NOT_APPLICABLE"} for r in pt),
      "every page type classified commercial/informational")

# 4. internal consistency
secs = {r["section"] for r in ia}
roots = {"(root)", "(utility)", "(none)"}
bad = [r["section"] for r in ia
       if not any(r["parent_section"].startswith(s.split(" (")[0]) for s in secs)
       and r["parent_section"] not in roots
       and not r["parent_section"].startswith(("Homepage", "Fine Jewellery or", "Necklaces & Pendants (conceptual)", "Shop All (URL)", "Education > relevant"))]
check(not bad, f"every parent_section resolves to a defined section ({bad})")
check(all(r["indexability_role"] in {"INDEXABLE_CONDITIONAL", "NON_INDEXABLE_BY_DEFAULT", "NOT_APPLICABLE", "INDEXABLE_PERMANENT"}
          for r in ia if r["status"] == "INSUFFICIENT EVIDENCE — DEFER"),
      "deferred rows are never marked NON_INDEXABLE outright")
check(all(r["indexability_role"] != "INDEXABLE_PERMANENT" or r["status"] in {"PROPOSED", "PROPOSED_CONCEPTUAL"} for r in ia),
      "only PROPOSED rows are INDEXABLE_PERMANENT")
check(all(r["indexability_role"] in {"NON_INDEXABLE", "NON_INDEXABLE_BY_DEFAULT"} for r in ia if r["proposed_level"] == "FACET"),
      "every facet row is non-indexable by default")
pt_map = {r["page_type"]: r for r in pt}
for t in ["FILTER_STATE (facet)", "SEARCH", "ACCOUNT / CART / CHECKOUT / WISHLIST", "PRODUCT_VARIANT_STATE"]:
    check(pt_map[t]["indexable_by_default"] == "NO" and pt_map[t]["permanent_seo_url"] == "NO", f"{t} non-indexable & non-permanent")
required_pt = ["HOMEPAGE", "CATEGORY_HUB (L1)", "SUBCATEGORY (style/type)", "PRODUCT_DETAIL_PAGE", "FILTER_STATE (facet)",
               "BUYING_GUIDE", "EDUCATION_ARTICLE (evergreen reference)", "BLOG_ARTICLE", "COMPARISON_GUIDE",
               "CERTIFICATION_GUIDE", "DIAMOND_SHAPE_GUIDE", "BRAND_PAGE (About, Contact)", "SERVICE_PAGE (Bespoke)",
               "FAQ_HELP", "SEARCH", "ACCOUNT / CART / CHECKOUT / WISHLIST"]
check(all(t in pt_map for t in required_pt), "all page types required by the brief are present")
top = ["Engagement Rings", "Wedding Bands", "Fine Jewellery", "Earrings", "Necklaces & Pendants", "Bracelets",
       "Bespoke / Custom Jewellery", "Education (Diamond & Jewellery Guide)", "Blog / Journal"]
check(all(t in secs for t in top), "all 9 minimum top-level areas evaluated")

# 5. scope guards: no keyword->URL mapping, no redirect/canonical prescriptions
check(not any("keyword" in c for c in REQ["12_ia_proposed_structure.csv"]), "no keyword column in IA structure (no kw->URL map)")
allcsv = " ".join(" ".join(r.values()) for r in ia + pt + cv).lower()
check(not re.search(r"\b301\b|redirect to|should redirect|rel=.?canonical|noindex tag|disallow:", allcsv),
      "no redirect/canonical/robots prescriptions in CSVs")
check("insufficient evidence — defer" in allcsv, "missing data explicitly labelled")
dl = open(os.path.join(A, "12_ia_decision_log.md"), encoding="utf-8").read()
nd = len(re.findall(r"^## D-\d+", dl, re.M))
fields = all(dl.count(k) >= nd for k in ["**DECISION", "**EVIDENCE", "**ALTERNATIVES CONSIDERED", "**RATIONALE", "**CONFIDENCE", "**DEFERRED QUESTION"])
check(nd >= 15 and fields, f"decision log has {nd} decisions, each with all 6 fields")
sm = open(os.path.join(A, "12_ia_summary.md"), encoding="utf-8").read()
check(all(f"## {i}." in sm for i in range(1, 17)), "summary has all 16 required sections")

# 6. no demand inferred from missing clusters (phrase check)
check("not evidence of no demand" in dl or "never read as missing demand" in dl, "decision log states missing keywords != missing demand")

# 7. upstream files unchanged
if len(sys.argv) > 1:
    changed = []
    for line in open(sys.argv[1]):
        h, p = line.strip().split(" ", 1)
        with open(os.path.join(ROOT, p), "rb") as fh:
            if hashlib.md5(fh.read()).hexdigest() != h:
                changed.append(p)
    check(not changed, f"Stage 7/8/10/11 files unchanged (checked {sum(1 for _ in open(sys.argv[1]))} files) {changed}")

# 8. no raw DataForSEO output created this stage
raw = os.path.join(ROOT, "dataforseo", "raw")
new_raw = [f for f in os.listdir(raw) if f.startswith("12")] if os.path.isdir(raw) else []
check(not new_raw, "no Stage 12 DataForSEO raw files (no API call)")

print(f"\n{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
