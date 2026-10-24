"""Core helpers for the master map build: columns, crawl join, defaults."""
import json, re, collections
import lib_research as L

BASE = "https://www.houseofdiams.com"
UNK = "UNKNOWN — VERIFY"
NA_GSC = "NOT AVAILABLE"
GSC_RANGE = "NOT AVAILABLE (no GSC access in this session: SEO Gets connector requires a subscription; no GSC export found in the project)"
CRAWL_DATE = "2026-10-09"

COLS = [
    "URL", "Page Type", "Page/Content Name", "SEO Cluster / Topic", "Page Role",
    "Primary Keyword", "Secondary Keywords", "Related/Semantic Concepts", "Search Intent", "Keyword Owner",
    "Existing Keyword Ownership Conflict?", "Cannibalization Risk",
    "Current SEO Title", "Current Meta Description", "Current H1", "Current Canonical", "Current Indexability", "Current URL Status",
    "Recommended SEO Title", "Recommended Meta Description", "Recommended H1", "Recommended Content/Section Changes", "Recommended Image/Alt-Text Changes",
    "Recommended Internal Links IN", "Recommended Internal Links OUT", "Recommended Anchor Context", "Internal-Link Priority",
    "Current Schema", "Recommended Schema", "Schema Validation/Review Needed?",
    "AEO Opportunity", "Primary Questions to Answer", "Answer-First Opportunity", "PAA/Question Coverage Needed?",
    "GEO/AI Search Opportunity", "Important Entities", "Entity Clarity Needed?", "Brand/Expertise/Trust Signal Opportunity",
    "GSC Clicks", "GSC Impressions", "GSC CTR", "GSC Average Position", "GSC Data Date Range",
    "Recommended Action", "Priority", "Implementation Dependency", "AWS Migration Dependency", "Status", "Evidence / Source", "Notes",
    # helper columns (after the 50 specified fields)
    "Row ID", "Registry/Calendar ID", "Row Group", "AWS Class (A/B/C)",
    "Flag: Metadata Opp", "Flag: H1 Opp", "Flag: Internal-Link Opp", "Flag: Schema Opp", "Flag: AEO Opp", "Flag: GEO/Entity Opp",
    "Flag: Ownership Conflict", "Flag: Cannibalization Review", "Flag: AWS-Blocked",
]
assert len(COLS) == 50 + 13

ACTIONS = {"KEEP", "OPTIMIZE", "CREATE", "EXPAND", "CONSOLIDATE", "REDIRECT", "REVIEW", "NO ACTION", "BLOCKED"}
PRIOS = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}

crawl = {r["url"]: r for r in json.load(open(L.SCR + "crawl/crawl.json"))}
sitemap_urls = set(re.findall(r"<loc>([^<]+)</loc>", open(L.SCR + "sitemap_live.xml").read()))
old_sitemap = set(re.findall(r"<loc>([^<]+)</loc>", open(L.R + "site/raw_sitemap.xml").read()))


def cr(path):
    return crawl.get(BASE + path if path.startswith("/") else path)


def norm(u):
    return u.rstrip("/").lower()


def cur_fields(path):
    """Return dict of the 'current state' fields from the live crawl."""
    r = cr(path)
    d = {}
    if not r:
        for k in ("Current SEO Title", "Current Meta Description", "Current H1", "Current Canonical", "Current Indexability", "Current URL Status", "Current Schema"):
            d[k] = UNK
        return d
    st = r["status"]
    if st in (301, 302, 307, 308):
        d["Current URL Status"] = f"{st} redirect → {r.get('location','?')} (crawl {CRAWL_DATE})"
    else:
        d["Current URL Status"] = f"{st} (crawl {CRAWL_DATE})"
    if "title" not in r:
        for k in ("Current SEO Title", "Current Meta Description", "Current H1", "Current Canonical", "Current Schema"):
            d[k] = UNK
        d["Current Indexability"] = "NOT INDEXABLE AS CRAWLED (non-200 or non-HTML) — VERIFY" if st != 200 else UNK
        return d
    d["Current SEO Title"] = r["title"] or "MISSING"
    d["Current Meta Description"] = r["meta_description"] or "MISSING"
    h1s = r.get("h1s", [])
    d["Current H1"] = " | ".join(h1s) if h1s else "NO H1 FOUND IN INITIAL HTML (VERIFY rendered DOM)"
    d["Current Canonical"] = r["canonical"] or "MISSING"
    ins = BASE + path
    in_sm = (ins in sitemap_urls) or (ins.rstrip("/") in {u.rstrip("/") for u in sitemap_urls})
    robots = r.get("meta_robots", "")
    xr = r.get("x_robots", "")
    canon_self = norm(r["canonical"]) == norm(ins) if r["canonical"] else False
    bits = []
    if st == 200:
        bits.append("HTTP 200")
    bits.append(f"meta robots: {robots or 'none'}")
    if xr:
        bits.append(f"X-Robots-Tag: {xr}")
    bits.append("self-canonical" if canon_self else ("canonical → " + r["canonical"] if r["canonical"] else "no canonical"))
    bits.append("in sitemap" if in_sm else "NOT in live sitemap")
    ind = ("INDEXABLE" if st == 200 and "noindex" not in (robots + xr).lower() and (canon_self or not r["canonical"]) else "REVIEW")
    d["Current Indexability"] = f"{ind} — " + "; ".join(bits) + " (robots.txt does not block this path; Google index state not verified — no GSC)"
    types = r.get("schema_types", [])
    d["Current Schema"] = ", ".join(types) if types else "NONE FOUND in initial HTML (JSON-LD blocks: %d)" % r.get("ld_blocks", 0)
    return d


def new_row():
    return {c: "" for c in COLS}


def gsc_na(row):
    row["GSC Clicks"] = row["GSC Impressions"] = row["GSC CTR"] = row["GSC Average Position"] = NA_GSC
    row["GSC Data Date Range"] = GSC_RANGE


def aws_text(a=(), b=(), c=()):
    parts = []
    if a:
        parts.append("A — SAFE TO PREPARE NOW: " + "; ".join(a))
    if b:
        parts.append("B — WAIT UNTIL AFTER AWS: " + "; ".join(b))
    if c:
        parts.append("C — VERIFY AFTER MIGRATION: " + "; ".join(c))
    return " || ".join(parts)


def aws_class(a=(), b=(), c=()):
    return "".join(x for x, v in (("A", a), ("B", b), ("C", c)) if v)


def yn(b):
    return "Y" if b else ""
