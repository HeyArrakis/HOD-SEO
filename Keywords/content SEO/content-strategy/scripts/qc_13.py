#!/usr/bin/env python3
"""Stage 13 QC. Run from project root: python3 content-strategy/scripts/qc_13.py"""
import csv
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CS = os.path.join(ROOT, "content-strategy")
fails = []


def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


def rd(path):
    with open(os.path.join(ROOT, path), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


SCHEMAS = {
    "13_existing_content_decisions.csv": "url,title,content_type,business_area,current_role,ranking_keyword_count,ranking_keywords,best_known_position,important_search_volume,stage11_clusters,validated_intent,serp_page_type,overlap_status,overlap_with,proposed_role,action,migration_risk,confidence,evidence,rationale,deferred_question",
    "13_ranking_equity_analysis.csv": "url,keyword,position,search_volume,cluster,intent,serp_page_type,current_page_type,alignment,equity_risk,notes",
    "13_blog_education_framework.csv": "topic_type,primary_home,secondary_role,evergreen_or_timebound,search_intent,example_topics,reason,evidence,notes",
    "13_content_migration_risk.csv": "url,current_type,proposed_action,risk_level,ranking_equity,overlap,destination_exists,reason,required_conditions,decision",
}

# 1. files exist + schemas
for f in list(SCHEMAS) + ["13_blog_strategy.md", "13_stage_summary.md"]:
    check(os.path.isfile(os.path.join(CS, f)), f"exists: {f}")
for f, cols in SCHEMAS.items():
    with open(os.path.join(CS, f), newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    check(rows[0] == cols.split(","), f"schema: {f}")
    check(all(len(r) == len(rows[0]) for r in rows), f"consistent column count: {f}")

dec = rd("content-strategy/13_existing_content_decisions.csv")
eq = rd("content-strategy/13_ranking_equity_analysis.csv")
fw = rd("content-strategy/13_blog_education_framework.csv")
mr = rd("content-strategy/13_content_migration_risk.csv")
inv = rd("content-strategy/10_existing_content_inventory.csv")
s3 = rd("dataforseo/processed/03_hod_ranked_keywords.csv")
ov = rd("content-strategy/10_content_overlap_analysis.csv")

# 2. every blog + education article accounted for
arts = {r["url"] for r in inv if r["content_type"] in ("BLOG_ARTICLE", "EDUCATION_ARTICLE")}
check(len([u for u in arts if "/blog/" in u]) == 10, "Stage 10 inventory has 10 blog articles")
check(len([u for u in arts if "/education/" in u]) == 1, "Stage 10 inventory has 1 education article")
check(arts <= {r["url"] for r in dec}, "every blog/education article has a decision row")

# 3. no duplicates
check(len(dec) == len({r["url"] for r in dec}), "no duplicate URLs in decisions")
check(len(mr) == len({r["url"] for r in mr}), "no duplicate URLs in migration risk")
check({r["url"] for r in dec} == {r["url"] for r in mr}, "decisions and migration risk cover the same URLs")
check(len(eq) == len({(r["url"], r["keyword"]) for r in eq}), "no duplicate URL+keyword rows")

# 4. every Stage 3 ranking keyword preserved with its position
s3set = {(r["ranking_url"], r["keyword"], r["rank_absolute"], r["search_volume"]) for r in s3}
eqset = {(r["url"], r["keyword"], r["position"], r["search_volume"]) for r in eq}
check(len(s3) == 28 and s3set == eqset, "all 28 Stage 3 ranking keywords, positions and volumes preserved")
cnt = Counter(r["ranking_url"] for r in s3)
check(all(str(cnt.get(r["url"], 0)) == r["ranking_keyword_count"] for r in dec), "ranking_keyword_count matches Stage 3")
best = {}
for r in s3:
    best[r["ranking_url"]] = min(best.get(r["ranking_url"], 999), int(r["rank_absolute"]))
check(all(r["best_known_position"] == (str(best[r["url"]]) if r["url"] in best else "") for r in dec),
      "best_known_position matches Stage 3")
check(all(r["url"] in {d["url"] for d in dec} for r in eq), "every ranking URL has a decision row")

# 5. controlled values
ACTIONS = {"KEEP_BLOG", "MOVE_TO_EDUCATION", "MERGE", "UPDATE_IN_PLACE", "RETARGET", "DEFER", "NO_ACTION"}
check(all(r["action"] in ACTIONS for r in dec), "actions use controlled values")
check(all(r["overlap_status"] in {"CLEAR_OVERLAP", "POSSIBLE_OVERLAP", "DISTINCT", "INSUFFICIENT_EVIDENCE"} for r in dec),
      "overlap_status uses controlled values")
check(all(r["migration_risk"] in {"HIGH", "MEDIUM", "LOW"} for r in dec), "migration_risk controlled")
check(all(r["risk_level"] in {"HIGH", "MEDIUM", "LOW"} for r in mr), "risk_level controlled")
check(all(r["alignment"] in {"ALIGNED", "PARTIALLY_ALIGNED", "MISALIGNED"} for r in eq), "alignment controlled")
check(all(r["equity_risk"] in {"HIGH", "MEDIUM", "LOW"} for r in eq), "equity_risk controlled")
check(all(r["confidence"] in {"HIGH", "MEDIUM", "LOW"} for r in dec), "confidence controlled")

# 6. Stage 10 overlap classifications preserved (strongest classification per URL)
RANK = {"CLEAR_OVERLAP": 3, "POSSIBLE_OVERLAP": 2, "DISTINCT": 1}
strongest = {}
for o in ov:
    urls = [o["url_a"].strip()] + [u.strip() for u in o["url_b"].split(";")]
    for u in urls:
        if RANK[o["classification"]] > RANK.get(strongest.get(u), 0):
            strongest[u] = o["classification"]
mism = [r["url"] for r in dec if strongest.get(r["url"]) and strongest[r["url"]] != r["overlap_status"]]
check(not mism, f"Stage 10 overlap classifications preserved {mism}")
check([r["url"] for r in dec if r["overlap_status"] == "CLEAR_OVERLAP"] ==
      [u for u in (r["url"] for r in dec) if strongest.get(u) == "CLEAR_OVERLAP"], "CLEAR_OVERLAP only on OV-01 pair")

# 7. no unsupported cannibalization claims
for f in list(SCHEMAS):
    with open(os.path.join(CS, f), encoding="utf-8") as fh:
        text = fh.read().lower()
    claims = [m for m in re.finditer(r"cannibali[sz]ation", text)
              if not re.search(r"(not|no|never|≠|isn't|without)[^.;]{0,60}$", text[max(0, m.start() - 80):m.start()])
              and not re.match(r"\s+(not|is not|was not)\b", text[m.end():m.end() + 20])]
    check(not claims, f"no positive cannibalization claim in {f}")

# 8. evidence and conditions
check(all(r["evidence"].strip() and r["rationale"].strip() for r in dec), "every decision row has evidence and rationale")
check(all(r["deferred_question"].strip() for r in dec if r["action"] == "DEFER"), "DEFER rows state the open question")
high = [r for r in mr if r["risk_level"] == "HIGH"]
check(all(r["required_conditions"].strip() and not r["decision"].startswith("PROCEED") for r in high),
      "HIGH-risk rows have explicit conditions and no unconditional move")
check(all(d["action"] != "MOVE_TO_EDUCATION" for d in dec if d["migration_risk"] == "HIGH"),
      "no HIGH-risk URL is recommended for MOVE_TO_EDUCATION")
check(all(r["required_conditions"].strip() for r in mr if r["proposed_action"].startswith(("MOVE", "RETARGET"))),
      "every move/retarget has required conditions")
check(all(d["action"] != "MERGE" for d in dec), "no MERGE recommended (evidence insufficient)")

# 9. no keyword->URL mapping columns; framework homes controlled
check(not any("target_url" in c or "mapped_url" in c for c in SCHEMAS.values()), "no keyword→URL mapping columns")
check(all(r["primary_home"] in {"EDUCATION", "BLOG", "COMMERCIAL PAGES", "FAQ / SUPPORT"} for r in fw), "framework primary_home controlled")

# 10. no API/raw output this stage; upstream files older than Stage 13 outputs
for d in ("dataforseo/raw", "serp/raw", "competitors/raw"):
    p = os.path.join(ROOT, d)
    new = [f for f in os.listdir(p) if f.startswith("13")] if os.path.isdir(p) else []
    check(not new, f"no Stage 13 raw API files in {d}")
out_mtime = min(os.path.getmtime(os.path.join(CS, f)) for f in SCHEMAS)
UP = ["dataforseo/processed/03_hod_ranked_keywords.csv", "dataforseo/processed/07_hod_master_keyword_database.csv",
      "serp/analysis/08_hod_serp_validation.csv", "clusters/11_cluster_registry.csv", "clusters/11_keyword_cluster_map.csv",
      "clusters/11_cluster_relationships.csv", "architecture/12_ia_proposed_structure.csv",
      "architecture/12_ia_decision_log.md"] + [f"content-strategy/{f}" for f in os.listdir(CS) if f.startswith("10_")]
check(all(os.path.getmtime(os.path.join(ROOT, f)) < out_mtime for f in UP), "Stage 3-12 source files not modified by Stage 13")

print("\naction counts (11 articles):", dict(Counter(r["action"] for r in dec if r["url"] in arts)))
print("alignment:", dict(Counter(r["alignment"] for r in eq)), "equity_risk:", dict(Counter(r["equity_risk"] for r in eq)))
print("\nRESULT:", "ALL PASS" if not fails else f"{len(fails)} FAIL")
sys.exit(1 if fails else 0)
