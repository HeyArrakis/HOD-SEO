import sys; sys.path.insert(0, ".")
from mm_docs import *

PHASE = ["PRE-AWS PREPARATION (A — safe to do now)", "POST-AWS IMPLEMENTATION (B — wait for AWS)", "POST-AWS VERIFICATION (C — verify after migration)"]


def agg_tasks(rs, i, top=14):
    c = collections.defaultdict(list)
    for r in rs:
        for t in r["_aws"][i]:
            c[t].append(r["Row ID"])
    out = []
    for t, ids in sorted(c.items(), key=lambda x: -len(x[1]))[:top]:
        ex = ", ".join(i_.replace("SUB:/", "/") for i_ in ids[:4]) + (f" … (+{len(ids)-4})" if len(ids) > 4 else "")
        out.append(f"- {t} — **{len(ids)} row(s)** ({ex})")
    return out or ["- (none)"]


# ================================================================== 03
def doc03():
    L_ = []
    A = L_.append
    A("# 03 — SEO Implementation Priorities")
    A(f"\nGenerated {TODAY}. Derived from the master map (`01-…csv`). **Planning only — no website change has been made, and nothing here should be implemented without the AWS migration plan.** Each priority is split into **PRE-AWS PREPARATION**, **POST-AWS IMPLEMENTATION** and **POST-AWS VERIFICATION**.\n")
    A("**Rubric (no scores, no fake precision).** *Critical* = index-integrity or ranking-equity risk, a public statement that contradicts a confirmed HOD fact, a test artifact, or a MUST_PUBLISH time-critical calendar item. *High* = live commercial hubs/articles with clear metadata/ownership/duplication problems, empty indexable pages, high-intent calendar items. *Medium* = worthwhile optimization without integrity risk. *Low* = polish, conditional/deferred, low-value legacy.\n")
    A("**Counts:** " + ", ".join(f"{p} {S['prio'][p]}" for p in ("CRITICAL", "HIGH", "MEDIUM", "LOW")) + f" (total {S['total_rows']} rows).\n")
    A("## Top 10 priorities (cross-cutting order)\n")
    A(TOP10_TEXT)
    for pname, p, blurb in (("Priority 1 — Critical", "CRITICAL", "Must address."), ("Priority 2 — High", "HIGH", "Important optimization."), ("Priority 3 — Medium", "MEDIUM", "Useful improvements."), ("Priority 4 — Low", "LOW", "Polish / future work.")):
        rs = [r for r in rows if r["Priority"] == p]
        A(f"\n## {pname}\n\n*{blurb}* — {len(rs)} rows.\n")
        if p in ("CRITICAL", "HIGH"):
            for grp in ORDER_G:
                g = [r for r in rs if r["Row Group"] == grp]
                if not g:
                    continue
                A(f"\n**{grp.title()}** ({len(g)})\n")
                A(table(["ID", "Page", "Action", "What / why"], [[r["Row ID"].replace("SUB:", ""), rid_url(r) if r["URL"].startswith(BASE) else short(r["Page/Content Name"], 60), r["Recommended Action"], headline(r)] for r in g]))
        else:
            for grp in ORDER_G:
                g = [r for r in rs if r["Row Group"] == grp]
                if not g:
                    continue
                A(f"\n**{grp.title()}** ({len(g)}): " + "; ".join(f"`{rid_url(r) if r['URL'].startswith(BASE) else r['Row ID']}` ({r['Recommended Action']})" for r in g))
        for i, ph in enumerate(PHASE):
            A(f"\n### {ph} — {pname.split(' — ')[1]}\n")
            A("\n".join(agg_tasks(rs, i)))
    A("\n## Items needing a human decision before they can be prioritised further\n")
    dec = [r for r in rows if r["Recommended Action"] in ("REVIEW", "BLOCKED")]
    A(f"{len(dec)} rows are `REVIEW` or `BLOCKED` (decision, ownership confirmation or business fact needed). By group: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(r["Row Group"] for r in dec).most_common()) + ".\n")
    open(OUT + "03-SEO-IMPLEMENTATION-PRIORITIES.md", "w").write("\n".join(L_))


ORDER_G = ["CORE LIVE", "HUBS", "COMMERCIAL CATEGORY", "COMMERCIAL SUBCATEGORY", "PRODUCT PAGES", "EXISTING ARTICLES (Education-owned)", "LEGACY / REDIRECT", "PLANNED EDUCATION", "CONDITIONAL EDUCATION", "CONDITIONAL COMMERCIAL", "PLANNED BLOG"]

TOP10 = [
    ("Put the redirect map into the AWS migration plan", "All `/engagement-rings/by-desgin/*` URLs return 404; the Stage 15 keyword-owner URL for side-stone rings is among them. Add a 1:1 301 and keep intentional `/contact` (307) and `/hiphop` (308) behaviour. *(CRITICAL; prepare now, implement + verify after AWS.)*"),
    ("Take test, placeholder and empty pages out of the indexable set", f"{len(empty_rows)} pages (incl. `/hiphop/test-subcat`, `/collection`, `/engagement-rings/round-rings`, all `For Him` pages) are in the sitemap with 0 products — Stage 12 D-13 says none may be indexable. Decide noindex/sitemap exclusion vs populate."),
    ("Correct the trust-critical copy", "/bespoke says '4-6 week typical lead time' (confirmed fact ≈3–4 weeks); /shipping shows placeholder text; /returns has no return terms; certification/shipping claims on home and bespoke need confirmation."),
    ("Ratify commercial keyword ownership (D-19) from existing data", "No commercial hub or subcategory owns a ratified keyword. Candidate heads are already in the project datasets (CSV column *Primary Keyword*); decide hub-vs-child ownership and the unowned 135,000/mo 'lab grown diamonds' head (COM-LG-HUB)."),
    ("Replace boilerplate metadata and add unique hub copy", f"{boiler_meta} category/subcategory pages use 'Browse X in Y.' metas; homepage title has no brand and overlaps /engagement-rings (OV-13). Drafts are in the CSV."),
    ("Update, never move, the ranking-equity articles", "CVD vs HPHT (19 ranked keywords), lab-grown vs natural, 14K vs 18K, how-to-choose: update in place, baseline GSC first, keep URL/H1 core terms."),
    ("Resolve ownership items before writing the new Education pages", "8 calendar items need ownership confirmation; 12 Education pages have different primary keywords in the Stage 19 brief vs the final calendar (see `04-…`)."),
    ("Unblock and sequence publishing", "10 approved article packages exist; 6 dated items have passed with nothing live; 3 items are blocked on business facts. Confirm whether the CMS can publish during the AWS content freeze."),
    ("Schema and entity clean-up at template level", "BreadcrumbList on articles, one author entity policy, retire boilerplate FAQPage on 35 pages (no rich result since 2026-05), enrich Organization (sameAs; founders once confirmed), keep Product/image URLs valid when hosts change."),
    ("Capture baselines now, verify after cut-over", "GSC export (16 months), CrUX/PageSpeed for template URLs, TTFB baseline (1.2–4.5 s in this audit), indexed-page counts, sitemap/robots/canonical snapshots — then run the C-checklist after migration."),
]
TOP10_TEXT = "\n".join(f"{i}. **{t}.** {d}" for i, (t, d) in enumerate(TOP10, 1))
doc02()
doc03()
print("02+03 done")
