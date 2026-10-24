"""Write QA deliverables 01-06 from rows.json (built by mm_build.py)."""
import csv, json, collections, re, os, sys, datetime
sys.path.insert(0, ".")
import lib_research as L
from mm_core import *
import mm_special, mm_helpers as H

OUT = "/Users/manavdesai/Desktop/HOD SEO/QA/"
rows = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "evidence", "rows.json")))
TODAY = "2026-10-09"

LIVE_G = ("CORE LIVE", "HUBS", "COMMERCIAL CATEGORY", "COMMERCIAL SUBCATEGORY", "PRODUCT PAGES", "EXISTING ARTICLES (Education-owned)")
live = [r for r in rows if r["Row Group"] in LIVE_G]
planned = [r for r in rows if r["Row Group"] in ("PLANNED EDUCATION", "PLANNED BLOG")]
cond = [r for r in rows if r["Row Group"] in ("CONDITIONAL EDUCATION", "CONDITIONAL COMMERCIAL")]
legacy = [r for r in rows if r["Row Group"] == "LEGACY / REDIRECT"]
TECH_KW = ["schema", "template", "redirect", "301", "noindex", "sitemap", "slug", "pagination", "canonical", "image url", "page build", "contact page", "child-page", "hub listing", "author", "url move", "variant", "naming", "decision", "any template"]


def is_tech(r):
    return any(any(k in b.lower() for k in TECH_KW) for b in r["_aws"][1])


def md_esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def table(headers, data):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for d in data:
        out.append("| " + " | ".join(md_esc(x) for x in d) + " |")
    return "\n".join(out)


def short(s, n=170):
    s = re.sub(r"\s+", " ", str(s)).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def path_of(u):
    return u.replace(BASE, "") or "/"


# ------------------------------------------------------------------ 01 CSV
def write_csv():
    with open(OUT + "01-MASTER-SEO-IMPLEMENTATION-MAP.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(COLS)
        for r in rows:
            w.writerow([r.get(c, "") for c in COLS])
    # PDP appendix
    app = mm_special.pdp_appendix()
    with open(OUT + "06-PDP-AUDIT-APPENDIX.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(app[0].keys()), quoting=csv.QUOTE_ALL)
        w.writeheader(); w.writerows(app)
    return app


# ------------------------------------------------------------------ stats
def stats():
    S = {}
    S["total_rows"] = len(rows)
    S["live_rows"] = len(live)
    S["live_urls_sitemap_nonpdp"] = len([u for u in sitemap_urls if "/shop/" not in u])
    S["pdp_sitemap"] = len([u for u in sitemap_urls if "/shop/" in u])
    S["sitemap_total"] = len(sitemap_urls)
    S["planned"] = len(planned); S["cond"] = len(cond); S["legacy"] = len(legacy)
    S["opt_live"] = sum(r["Recommended Action"] in ("OPTIMIZE", "EXPAND") for r in live)
    S["noaction"] = sum(r["Recommended Action"] == "NO ACTION" for r in rows)
    S["noaction_live"] = sum(r["Recommended Action"] == "NO ACTION" for r in live)
    for key, col in (("meta", "Flag: Metadata Opp"), ("h1", "Flag: H1 Opp"), ("links", "Flag: Internal-Link Opp"), ("schema", "Flag: Schema Opp"), ("aeo", "Flag: AEO Opp"), ("geo", "Flag: GEO/Entity Opp"), ("conf", "Flag: Ownership Conflict"), ("cann", "Flag: Cannibalization Review")):
        S[key + "_live"] = sum(r[col] == "Y" for r in live)
        S[key + "_planned"] = sum(r[col] == "Y" for r in planned)
        S[key + "_all"] = sum(r[col] == "Y" for r in rows)
    S["tech_b"] = sum(is_tech(r) for r in rows)
    S["tech_b_live"] = sum(is_tech(r) for r in live)
    S["publish_b"] = sum(1 for r in planned)
    S["blocked_fact"] = sum(r["Recommended Action"] == "BLOCKED" for r in rows)
    S["actions"] = collections.Counter(r["Recommended Action"] for r in rows)
    S["prio"] = collections.Counter(r["Priority"] for r in rows)
    S["group_action"] = collections.Counter((r["Row Group"], r["Recommended Action"]) for r in rows)
    return S


S = stats()
