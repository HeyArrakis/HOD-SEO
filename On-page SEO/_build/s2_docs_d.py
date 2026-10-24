# -*- coding: utf-8 -*-
"""Docs 02, 08, 09 (register with final dispositions), 10, 11, 12, 13, README + the commercial keyword CSV."""
import collections, re
from s2_docs_a import mdt, short, TODAY, counts
from s2_load import CAL
import s2_final as FN, s2_edu
from s2_docs_c import OD as OD_ORIG
from s2_build import vol_of, stage15_str

KWCOLS = ["Row ID", "URL", "Page", "Assignment State", "Primary Keyword", "Volume (US/mo)", "KD", "DFS Intent Label", "SERP Evidence", "Secondary / Held Keywords",
          "Confidence", "Rationale", "Boundary (must not target)", "Caveat / Review Trigger"]


def kw_rows(rows):
    out = []
    for r in rows:
        rid = r["Row ID"]
        a = FN.A.get(rid)
        if not a:
            continue
        p = a["primary"]
        v, kd, it = FN.kwi(p) if p else (None, "", "")
        sec = []
        for s in a["sec"]:
            b = s.rstrip("*")
            sec.append(b if ("→" in b or "(" in b) else FN.fmt(b) + (" [conditional]" if s.endswith("*") else ""))
        out.append({"Row ID": rid, "URL": r["URL"], "Page": r["Page Name"], "Assignment State": a["state"], "Primary Keyword": p or "—",
                    "Volume (US/mo)": (format(int(v), ",") if v is not None else ("" if not p else "not measured")), "KD": kd, "DFS Intent Label": it,
                    "SERP Evidence": a["serp"] + (" | VOLUME IS A PROXY" if a["proxy"] else ""), "Secondary / Held Keywords": "; ".join(sec), "Confidence": a["conf"],
                    "Rationale": a["why"], "Boundary (must not target)": a["boundary"], "Caveat / Review Trigger": a["caveat"]})
    return out


RES = {
 "OD-01": dict(
   res="Keyword ownership is assigned for the 9 category hubs, the subcategories and /bespoke — one primary keyword per URL (hub = broad head, child = specific type, bespoke/custom kept distinct from the engagement-ring catalog). Full table: `10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv`. Stage 15 itself is untouched; this log is the ratification record.",
   why="Existing US datasets already hold measured heads for most pages (volume + DFS intent label). Where no head is measured the page is deliberately not promoted rather than forced. Inventory facts come from the 2026-10-09 initial-HTML product sets.",
   ev="blog_keyword_research.csv / master keyword DB / QA evidence kwlookup.json (volumes, KD, DFS labels); Stage 8 SERP validation (only 'side stones engagement rings', 'lab grown diamonds', 'lab diamonds', 'natural diamonds'); Stage 12 D-03/D-05/D-07/D-08/D-18; Stage 16 anchor strategy; crawl 2026-10-09.",
   conf="HIGH for hub heads and the side-stone owner; MEDIUM for most children (volume measured, SERP type NOT validated); LOW for thin-inventory pages.",
   dep="None blocking. GSC Queries (G-02) later confirm or overturn volume-only assignments.", rev="Reversible per page; review triggers in §6."),
 "OD-02": dict(
   res="No separate commercial Lab-Grown hub now. 'lab grown diamond engagement rings' / 'lab grown diamond rings' (90,500 each) become secondary targets of /engagement-rings once HOD confirms all catalog stones are lab-grown; the head terms 'lab grown diamonds' (135,000), 'lab diamonds' (27,100), 'lab created diamonds' (12,100) stay unowned by design; EDU-LG-00 stays informational.",
   why="A hub would duplicate /shop (finished jewelry only, all lab-grown), fail D-07 distinctness/one-home, and compete on a SERP of loose-stone retailer collections HOD cannot match without loose stones.",
   ev="Stage 8 (lab grown diamonds = NAVIGATIONAL; lab diamonds = TRANSACTIONAL, retailer collection pages); Stage 12 D-05; Stage 16 §3.3; catalog = rings/bands/earrings/necklaces/bracelets only (crawl); PDP spec tables 'Stone Type: Lab Grown Diamond'.",
   conf="MEDIUM (no SERP evidence for the engagement-ring variant).", dep="F-E1 (all stones lab-grown?) activates the secondary heads; F-E2 (loose lab-grown stones sold/planned?) is the single fact that would reverse the recommendation.",
   rev="Preferred option if F-E2 = yes: build the hub (own the head terms; Stage 16 hub links activate)."),
 "OD-03": dict(
   res="R2 adopted for all 12: calendar (SERP-validated) term is primary, the Stage 17/19 term is co-primary or a section question; page owners unchanged; titles/H1s updated (see §4).",
   why="Each pair points to one page; the calendar terms carry the larger, SERP-validated demand (e.g. ring size chart 165,000 vs 1,000). No source contradicts R2; 2 pairs are mere wording variants (shapes, VVS).",
   ev="QA/04 §3a; calendar rounds + Stage 18.5; Stage 15 map; Stage 19 briefs.", conf="HIGH.", dep="Four of the pages sit on ranking-equity or Stage 13 URLs: MET-01 title change waits for the GSC baseline.", rev="Fully reversible (titles only)."),
 "OD-04": dict(
   res="All 8 items resolved: EDU-RJG-BR, EDU-RJG-NL, EDU-INS, EDU-WB-GUIDE, EDU-LG-09, EDU-RJG-01, EDU-RJG-03 are Education owners; 'types of wedding rings' is a single Education page (EDU-WB-TYPES, calendar ID BLOG-WR-TYPES kept as alias, date/slot unchanged).",
   why="Stage 13 §3 assigns sizing, care, testing/identification and permanent buying guides to Education; §4 tests (shelf-life, question, ownership, brand) point 'types of wedding rings' to Education ('if tests disagree, Education wins for anything a searcher would ask repeatedly'). Blog posts BC-037/007/022/023 stay Blog and link to it.",
   ev="13_blog_strategy.md §3–4; Stage 14 EDU-RJG-* rows; calendar boundary notes; Stage 19 ownership review; S18.5 'engagement ring settings' conflict.", conf="HIGH (Education vs Blog); MEDIUM for EDU-INS (cost/insurance content is partly time-bound).",
   dep="None blocking. Hub-index page EDU-RJG-00 now meets its activation condition (≥2 child guides) — documented follow-up, not scheduled.", rev="Calendar annotation done 2026-10-10: BLOG-WR-TYPES target_owner = EDU-WB-TYPES (the only calendar field changed)."),
 "OD-05": dict(res="American English everywhere customer-facing (jewelry, color, center, customize). Slugs unchanged.", why="Confirmed project rule (US market).", ev="User instruction 2026-10-10; Stage 12 D-15; 23 vs 1 keyword usage.", conf="HIGH.", dep="None.", rev="n/a"),
 "OD-06": dict(
   res="Developer redirect map adopted: 8 style URLs + the group URL, each 1:1 301 from /engagement-rings/by-desgin/<x> → /engagement-rings/by-design/<x> (targets confirmed live). The /engagement-rings/by-design duplicate group page gets canonical → /engagement-rings, leaves the sitemap, and stops being linked; children preserved.",
   why="Identical product set (24 = 24) and FAQ; D-03/P-DEPTH. Redirecting the group page is held back only because PDP breadcrumbs still link to it (E-13) and GSC evidence is absent.",
   ev="crawl 2026-10-09 (404s, targets 200 in sitemap); Stage 10; Stage 12 D-03; Stage 16 §5.", conf="HIGH (1:1 redirects); MEDIUM (canonical vs redirect for the group page).",
   dep="E-03/E-04 (implementation); GSC G-03 confirms indexed state — non-blocking.", rev="Group page → 301 later once no internal link points to it."),
 "OD-07": dict(
   res="Rule adopted and applied page by page (§5): 0 products → noindex,follow + out of sitemap/nav/llms.txt until populated; test artifact removed; no redirect to irrelevant pages; legitimate children preserved.",
   why="Stage 12 D-13/P-EMPTY/P-NO-TEST; reversible (population simply re-enables indexing).", ev="crawl 2026-10-09 product counts; Stage 12 D-13.", conf="HIGH.", dep="E-05 (per-page noindex + sitemap exclusion).", rev="Re-evaluate on population with the D-07 gate."),
 "OD-08": dict(
   res="Bespoke timeline applied everywhere ('typically 2–3 weeks to make, ~6–9 days delivery, generally ~3–4 weeks from design approval to delivery; stone-dependent; not guaranteed'). Every other unverified or contradictory claim is removed or made neutral. One consolidated questionnaire issued (`11-HOD-CLIENT-FACTS-REQUEST.md`).",
   why="Only the bespoke timeline is confirmed; guessing shipping, returns, warranty, certification or founder facts would create public false statements.", ev="confirmed_business_facts.md; user instruction 2026-10-10; live pages re-read 2026-10-09.", conf="HIGH.",
   dep="HOD answers (F-A1…F-E7) complete /shipping, /returns, /about, /contact and upgrade claims elsewhere.", rev="n/a"),
 "OD-09": dict(res="A real, crawlable /contact page is adopted (200, indexable, self-canonical, in sitemap; /?contact=open canonicalises to it) with the existing enquiry fields; no contact details invented.",
   why="Stage 12 expects a BRAND-CONTACT page; entity/NAP consistency; FAQ already points at /contact.", ev="Stage 12; crawl (307 → modal); modal topics.", conf="MEDIUM-HIGH.", dep="F-C2 (public contact set); E-12 (build).", rev="Fallback: keep modal and fix references."),
 "OD-10": dict(res="FAQ answers become one line + link to the Education owner; policy answers neutral until F-A1/F-A2.", why="Stage 14 D14-30; Stage 12 D-18.", ev="QA/04 §4b.", conf="HIGH.", dep="None.", rev="n/a"),
 "OD-11": dict(res="Default byline and schema author = 'House of Diams' (Organization). A named person only where identity, role and credentials are verified; visible byline and structured data must match. The approved packages' 'Written By = HOD Team' is standardized to 'House of Diams' at CMS entry (packages not edited).",
   why="No verified expert identities exist; founder names are inconsistent (F-C1).", ev="Package seo-metadata.md (author Person 'HOD Team'); live bylines.", conf="HIGH.", dep="E-07 (template author field); F-C1 only for named authors.", rev="n/a"),
 "OD-12": dict(res="Public section name standardized to 'Blog' (URL /blog unchanged; 'Back to Journal' → 'Back to Blog'; anchors updated). H1 'Stories from House of Diams' kept. Paginated listings: self-referencing canonicals, 'Page N' titles where supported.",
   why="Nav and URL already say Blog; consistency; Stage 13 category rules unchanged.", ev="crawl (/blog H1/canonical behavior); Stage 16.", conf="HIGH.", dep="E-06 (template support for page-number titles; canonical is the minimum).", rev="n/a"),
 "OD-13": dict(res="No URL moves in this phase. Education-owned /blog articles are listed on /education by topic; the Blog hub keeps listing them until their Education path exists (Stage 16).", why="Stage 13 move conditions are not met; ranking URLs.", ev="Stage 13 content-migration risk; Stage 16 §4/§8.", conf="HIGH.", dep="None.", rev="Moves re-open only with a Stage 13 plan."),
 "OD-14": dict(res="Keep the 10 carat-variant PDP URLs; no merge, delete or redirect now. Review after cut-over with GSC data.", why="No consolidation evidence; each variant has distinct carat/price.", ev="QA/06 flags; IA D-11.", conf="HIGH.", dep="G-01 for the later review; E-09.", rev="n/a"),
 "OD-15": dict(res="Title 2.5 ct Oval Marquise Diamond Engagement Ring; H1 'Oval Marquise Diamond Engagement Ring'; Product schema name = H1; slug unchanged. Live change waits for the GSC baseline.", why="Stage 15 owner of 'marquise oval diamond' (est. pos 90 = DataForSEO estimate); keeps COM-ER-SIDESTONE separate.", ev="live PDP re-read (JSON-LD name ≠ H1).", conf="HIGH.", dep="G-01/G-02.", rev="n/a"),
 "OD-16": dict(res="One home per intent: eternity → /wedding-bands/for-her/eternity (FJ eternity page empty/noindex); toi et moi ring ≠ necklace (disjoint sets); T-bar stays a separate collection (0 overlap with pendants); solitaire pendant vs pendant necklace (0 overlap) split by qualifier; stud earrings child owns 'diamond stud earrings', hub keeps 'diamond earrings'.",
   why="Initial-HTML product sets are disjoint for every pair except hub-vs-child (stud: expected). No merges needed.", ev="crawl product-set comparison 2026-10-09; Stage 12 D-07 #4–5.", conf="MEDIUM (volume-only; informational-labelled heads unvalidated).", dep="G-02 later.", rev="Each default is reversible; no URL changes."),
 "OD-17": dict(res="Engineering intake prepared (`12-ENGINEERING-INPUTS.md`, E-01…E-13). Specification is not blocked; every Class B item stays post-migration.", why="These are engineering facts.", ev="QA/02 §8.", conf="n/a", dep="E-01…E-13.", rev="n/a"),
 "OD-18": dict(res="GSC request prepared (`13-GSC-DATA-REQUEST.md`, G-01…G-06). Only edits to ranking-equity URLs wait for it.", why="No GSC data; DataForSEO positions are estimates.", ev="CLAUDE.md §5.", conf="n/a", dep="G-01…G-06.", rev="n/a"),
 "OD-19": dict(res="Bundled with the HOD questionnaire (F-E2). Education framing stays neutral; no claim that HOD sells natural or loose stones.", why="Offer unconfirmed.", ev="Stage 12 D-05 deferred question.", conf="n/a", dep="F-E2.", rev="n/a"),
}


def doc02(rows):
    c = counts(rows)
    grp = []
    for g, n in sorted(c["Row Group"].items(), key=lambda x: -x[1]):
        sub = [r for r in rows if r["Row Group"] == g]
        grp.append([g, n] + [sum(1 for r in sub if r["Priority"] == p) for p in ("CRITICAL", "HIGH", "MEDIUM", "LOW")])
    st = [[k, v] for k, v in sorted(c["Status"].items(), key=lambda x: -x[1])]
    ready = c["Status"]["READY FOR IMPLEMENTATION POST-AWS"]
    blocked = sum(c["Status"][k] for k in ("HOD INPUT REQUIRED", "ENGINEERING INPUT REQUIRED", "GSC BASELINE REQUIRED", "CONDITIONAL — PRODUCT/OFFER CONFIRMATION"))
    return """# 02 — On-Page SEO Master (human-readable)

Generated %s (Step 2A decision resolution + Step 2B finalization of the 2026-10-09 package). **Everything here is a specification. Nothing was implemented; no website, CMS, redirect, sitemap, robots.txt or schema was touched; no paid DataForSEO call was made.** The operational file is `01-ON-PAGE-SEO-MASTER.csv` (%d rows, one per important page of the Step 1 map).

## 1. What changed in Step 2A/2B

* **Decisions OD-01…OD-19 were resolved** under the user's delegation (2026-10-10): 15 adopted, 1 partly adopted pending HOD facts, 3 awaiting external input with the specification not blocked. Record: `10-DECISIONS-RESOLUTION-LOG.md`; original proposals preserved in `09`.
* **Commercial keyword ownership is assigned** for the category hubs, subcategories and /bespoke (`10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv`) — one primary per URL, no duplicates, SERP-validation status stated per row.
* **Education**: all 12 primary-keyword mismatches resolved (R2) and all 8 ownership items resolved; 'types of wedding rings' is a single Education page.
* **American English** is applied to all recommended copy, nav labels and anchors; slugs unchanged.
* **Status vocabulary replaced**: rows are now `READY FOR IMPLEMENTATION POST-AWS`, `PRE-AWS PREPARATION`, `HOD INPUT REQUIRED`, `ENGINEERING INPUT REQUIRED`, `GSC BASELINE REQUIRED`, `CONDITIONAL — PRODUCT/OFFER CONFIRMATION`, `NO CHANGE REQUIRED`, `NOT PLANNED — CONDITIONAL`. Engineering/HOD/GSC dependencies are itemised per row in `Remaining Dependencies`.
* New deliverables: `11-HOD-CLIENT-FACTS-REQUEST.md`, `12-ENGINEERING-INPUTS.md`, `13-GSC-DATA-REQUEST.md`.

## 2. Scope and counts

Rows: **%d** (all Step 1 rows; excluded by rule: cart, checkout, login/signup/profile/wishlist, search, sort/filter/shape/metal parameter URLs, tracking URLs). The 184 PDPs are covered by one template row + the priority list in `07`.

%s

**Priority:** CRITICAL %d · HIGH %d · MEDIUM %d · LOW %d

**Status (primary):**

%s

**Readiness view:** **%d rows are ready for implementation after AWS**; %d are blocked by a specific external input (HOD %d · GSC baseline %d · product/offer confirmation %d); %d are pre-AWS writing tasks (content still to be written — the specification is final); %d need no change; %d are conditional/not planned.
**AWS class** (class of the implementation step): A = prepare/write now (%d rows) · B = apply after AWS (%d rows) · C = verify only (%d rows). Every live-page change also has a Class C verification step after cut-over.
**Dependency flags (independent of status):** %d rows list HOD facts (most are enhancements — the page ships with neutral wording), %d rows list a GSC dependency (blocking only where Status says so), %d rows list engineering inputs (E-01/E-02 apply to all Class B rows).

## 3. Facts verified live (read-only, 2026-10-09; unchanged by Step 2A)

| Check | Result | Consequence |
|---|---|---|
| Title suffix | `<title>` = `og:title` + ` \\| House of Diams`; the homepage uses an absolute title | All titles are **pre-suffix values**; the CSV also shows the rendered title and its length |
| Step 1 draft metas | Several repeated unconfirmed claims (free insured delivery, 15-day returns, family-run since 2014, free CAD consultation) | Not adopted; no recommended title/meta/H1 contains such a claim |
| PDP structured data | JSON-LD name ≠ H1; sku UUID ≠ visible SKU; six metals with one price; schema breadcrumb ≠ visible path | In `07` |
| PDP descriptions | 'IGI certified GH / VVS', 'Care & Warranty', shipping block | Unverified — replaced with neutral policy links until F-A/F-B answers |
| Product-set comparison (initial HTML) | /wedding-bands = /for-her (7 = 7); /engagement-rings = /by-design (24 = 24); T-bar, pendant, solitaire and toi et moi sets are disjoint | Drives OD-06 and OD-16 |

## 4. Controlled vocabularies

* **Priority:** CRITICAL (index-integrity / trust-fact / ranking-equity risk, or a MUST_PUBLISH page due within ~2 weeks) · HIGH · MEDIUM · LOW.
* **Ownership Status:** `RATIFIED 2026-10-10 (delegated)` · `RATIFIED — Stage 15 owner` · `RESERVED — INACTIVE UNTIL POPULATED` · `HELD — AMBIGUOUS` · `NOT BUILT` · `NO KEYWORD BY DESIGN` · `NO KEYWORD — NO MEASURED DEMAND` · `BLOG-OWNED` · `CONDITIONAL — NOT PLANNED`.
* **Action labels:** `REPLACE — FINAL`, `KEEP`, `HOLD` (noindex/canonical rows), `CARRY APPROVED` (packaged posts), `FINAL DRAFT` (pages to be written).
* **Remaining Dependencies:** `HOD: F-xx` (see 11) · `ENG: E-xx` (see 12) · `GSC: G-xx` (see 13).

## 5. Page-family rules (final)

| Family | Title | Meta | H1 | Content | Notes |
|---|---|---|---|---|---|
| Homepage | Brand-led, absolute | Offer summary, no claims | Keep tagline | Entity intro (verified facts only); remove unverified badges | D-18 |
| Commercial hubs / subcategories | Assigned keyword in plain US wording | "Shop <type>: <what defines it>" — no shipping/returns/certification | Plain type name | Short unique intro, 1–2 Education links, no boilerplate FAQ | Empty pages noindex; duplicates canonicalised |
| PDP | Template: shape + type + carat (≤~43 chars pre-suffix) | Spec-based, from the product record | Visible name = schema name | Specs, description and variant rules | `07` |
| Existing Education articles | Keep when aligned; assigned primary otherwise | Answer-first rewrite | Keep when aligned | Refresh in place; PAA as sections | URL never changes; GSC baseline for equity URLs |
| New Education pages | Calendar primary | Final draft | Final draft | Stage 19 brief sections | Owners ratified |
| Blog posts | 10 approved values carried; others final drafts | ≤155 chars, no unverified claims | Draft | Per calendar + PAA | Packages untouched (BC-001 DNM) |
| Policy / trust pages | Plain descriptive | Neutral | Keep | Rewrite from confirmed facts only | HOD questionnaire |

## 6. How to use the CSV

Filter `Status` + `AWS Class` for queues; `Remaining Dependencies` for what each row still needs; `Decision Resolution` links each row to its adopted decision (`10`). Titles/metas/H1/links/schema columns are copy-ready for rows whose Status allows.

## 7. Limits

* No GSC data (nothing here uses clicks, impressions, CTR or positions; DataForSEO positions quoted for equity URLs are Stage 3 estimates).
* No new keyword research; volumes/KD/intent labels come from existing project files. **SERP type is NOT validated for most commercial heads** (only side-stone, 'lab grown diamonds', 'lab diamonds', 'natural diamonds').
* Post-AWS state (URLs, templates, image hosts, CMS) is UNKNOWN; observations are dated 2026-10-09 and must be re-verified (Class C).
* Titles/metas are display guidelines (~60 / ~155 characters), not ranking rules.
""" % (TODAY, len(rows), len(rows), mdt(["Row group", "Rows", "CRITICAL", "HIGH", "MEDIUM", "LOW"], grp),
       c["Priority"]["CRITICAL"], c["Priority"]["HIGH"], c["Priority"]["MEDIUM"], c["Priority"]["LOW"], mdt(["Status", "Rows"], st),
       ready, blocked, c["Status"]["HOD INPUT REQUIRED"], c["Status"]["GSC BASELINE REQUIRED"], c["Status"]["CONDITIONAL — PRODUCT/OFFER CONFIRMATION"],
       c["Status"]["PRE-AWS PREPARATION"], c["Status"]["NO CHANGE REQUIRED"], c["Status"]["NOT PLANNED — CONDITIONAL"],
       c["AWS Class"]["A"], c["AWS Class"]["B"], c["AWS Class"]["C"],
       sum(1 for r in rows if r["HOD Facts Needed"] == "Y"), sum(1 for r in rows if r["GSC Data Needed"] == "Y"), sum(1 for r in rows if r["Engineering Input Needed"] == "Y"))


def doc08(rows):
    c = counts(rows)
    crit = [r for r in rows if r["Priority"] == "CRITICAL"]
    high = [r for r in rows if r["Priority"] == "HIGH"]
    n_new = sum(1 for r in rows if r["Row Group"] == "PLANNED EDUCATION")
    n_ref = sum(1 for r in rows if r["Recommended Action"] in ("REFRESH IN PLACE", "RETARGET + REFRESH"))
    n_draft = sum(1 for r in rows if r["Row Group"] == "PLANNED BLOG" and not r["Recommended Action"].startswith(("PUBLISH", "HOLD PUBLICATION")))
    n_held = sum(1 for r in rows if r["Row Group"] == "PLANNED BLOG" and r["Status"] == "HOD INPUT REQUIRED" and r["Row ID"] != "BC-001")

    def lst(rs):
        return mdt(["Row", "Page", "Action", "Status", "AWS", "Remaining dependencies"], [[r["Row ID"].replace("SUB:", ""), short(r["Page Name"], 50), r["Recommended Action"], r["Status"], r["AWS Class"], short(r["Remaining Dependencies"], 70)] for r in rs])

    top10 = [
     "**Fix the trust-critical copy** — delete the /shipping placeholder, publish returns terms, correct /bespoke ('4–6 weeks' → typically 2–3 weeks + ~6–9 days, generally ~3–4 weeks from design approval to delivery) and remove unverified badges. *Bespoke/badge/placeholder fixes are ready (B); policy text needs F-A1/F-A2.*",
     "**Hand the redirect and index-control spec to developers** — 9 by-desgin 301s (the side-stone keyword-owner URL is a 404), canonical for the duplicate group page, noindex + sitemap/nav exclusion for 18 empty/test pages (`10` §5).",
     "**Write the new Education pages in calendar order** — owners and primaries are ratified; EDU-LG-00 is due 2026-10-21 (CRITICAL); then ring size chart (165,000), diamond shapes/cut (60,500), clarity chart (33,100).",
     "**Apply commercial metadata, H1s and unique intros** for 9 hubs, 23 live subcategories and /bespoke with the assigned keywords (final; Class B).",
     "**Refresh the ranking-equity articles in place** after the GSC baseline — CVD vs HPHT (19 keywords), lab-grown vs natural, how-to-choose, 14K vs 18K; rewrite metas first.",
     "**Fix the 19 REQUIRED internal links missing from live pages** and ship the Step 2A additions (Education index listings, wedding-band pair).",
     "**PDP templates + the 8 flagged PDPs** — unique titles/metas, schema name/sku/breadcrumb alignment, neutral policy links instead of unverified claims.",
     "**Schema and entity clean-up** — retire boilerplate FAQPage (35 pages), BreadcrumbList + Organization byline on articles, one Organization @id.",
     "**Send the HOD questionnaire and the engineering intake** (`11`, `12`) and the GSC request (`13`) — they unlock the remaining %d blocked rows." % sum(1 for r in rows if r["Status"] in ("HOD INPUT REQUIRED", "GSC BASELINE REQUIRED", "CONDITIONAL — PRODUCT/OFFER CONFIRMATION")),
     "**Unblock publishing** — %d packaged posts are ready for human review (BC-001 is held until HOD confirms 'insured shipping', F-A1); 6 dated 2026-10-04…09 have passed; confirm the migration-safe window (E-01)." % sum(1 for r in rows if r["Recommended Action"] == "PUBLISH (packaged)"),
    ]
    wp = [
     ["WP-1", "Trust-critical copy (/shipping, /returns, /bespoke, /about, /contact, homepage badges, PDP blocks)", "Placeholder removal, bespoke fix, badge removal = READY; policy/entity text = HOD INPUT REQUIRED", "F-A1, F-A2, F-B1, F-C1, F-C2, F-D1", "Apply copy (E-02)", "Re-read pages; schema valid"],
     ["WP-2", "Redirect & index control (9 redirects, group canonical, 18 empty/test pages, /contact)", "READY FOR IMPLEMENTATION POST-AWS", "—", "Implement (E-03…E-05)", "Status codes, canonicals, sitemap membership"],
     ["WP-3", "Education: %d new pages + %d refreshes" % (n_new, n_ref), "PRE-AWS PREPARATION (write) / READY (refresh) / GSC BASELINE REQUIRED (4 equity URLs)", "G-01, G-02 for equity URLs", "Publish in the migration-safe window", "URL live, schema, links, CWV"],
     ["WP-4", "Commercial metadata, H1s, intros (assigned keywords)", "READY FOR IMPLEMENTATION POST-AWS", "—", "Apply metadata/intros/nav clean-up", "Rendered titles/metas/H1s"],
     ["WP-5", "Internal links (19 missing REQUIRED + launch links + Step 2A additions)", "READY FOR IMPLEMENTATION POST-AWS", "—", "Edit templates/pages", "Crawl REQUIRED rows"],
     ["WP-6", "Schema & entity (Organization @id, article BreadcrumbList/byline, FAQPage retirement, Product fixes)", "READY FOR IMPLEMENTATION POST-AWS", "F-C1/F-C2 for sameAs/founder fields", "Template/schema changes (E-07…E-10)", "Rich Results Test, Schema.org validator"],
     ["WP-7", "PDP templates + flagged PDPs", "READY FOR IMPLEMENTATION POST-AWS; oval PDP = GSC BASELINE REQUIRED", "F-A/F-B upgrades; G-01 for oval", "Apply in product data/templates", "Re-crawl 184 PDPs"],
     ["WP-8", "Blog pipeline (10 packaged + %d drafts; %d drafts held for HOD facts; BC-001 publication held)" % (n_draft, n_held), "READY (9 packaged) / HOD INPUT REQUIRED (BC-001 publication; BC-005, BC-015 writing) / PRE-AWS PREPARATION (drafts)", "F-A1 (BC-001), F-E6", "Publish in the window", "URL, canonical, schema, links"],
    ]
    return """# 08 — On-Page Implementation Priorities

Generated %s. Derived from `01-ON-PAGE-SEO-MASTER.csv` after the Step 2A resolutions. **Planning only — nothing has been implemented.** Class **A** = prepare/write now · **B** = apply after AWS · **C** = verify after cut-over.

**Counts:** CRITICAL %d · HIGH %d · MEDIUM %d · LOW %d (total %d). **Ready for implementation after AWS: %d · blocked by a specific external input: %d.**

**Rubric:** CRITICAL = index-integrity, trust-fact or ranking-equity risk, or a MUST_PUBLISH page due within ~2 weeks; HIGH = live pages with clear problems or high-value pages with a ready specification; MEDIUM = worthwhile optimization without integrity risk; LOW = polish, low-demand, conditional. Volume alone never set priority; effort and AWS dependency were weighed.

## 1. Top 10 on-page priorities

%s

## 2. Work packages

%s

## 3. CRITICAL (%d)

%s

## 4. HIGH (%d)

%s

## 5. By AWS class

* **A — now (%d rows):** write the %d new Education pages and %d Blog drafts; human-review the 9 publish-ready packaged posts (BC-001 stays held for F-A1); hand over the redirect/index-control spec, link spec and schema spec; send `11`, `12`, `13`.
* **B — after AWS (%d rows):** live metadata, H1s, intros, schema/template changes, canonical/noindex/sitemap rules, redirects, pagination, image-host updates, publishing into the new CMS. *If engineering confirms the content store is editable and outside the freeze (E-01/E-02), copy-only items may go earlier — their call, not assumed.*
* **C — verify (%d rows + the C-step of every B row):** 200/301/404, self-canonicals, indexability, sitemap membership, robots/AI-bot allowances, rendered titles/metas/H1s, schema validity, internal links, PDP currency, CWV against the pre-cut-over baseline.

## 6. Date-sensitive items (final calendar)

| Date | Item | Needs |
|---|---|---|
| 2026-10-21 | EDU-LG-00 What are lab-grown diamonds? (MUST_PUBLISH, CRITICAL) | Write + review now; `/education` index must link it; publishing window (E-01) |
| 2026-10-23 | BC-024 engagement-ring cost (MUST_PUBLISH) | Draft + review; window |
| 2026-11-12 / 11-13 | EDU-RJG-02 ring size, EDU-SHP-00 shapes (MUST_PUBLISH) | Write/refresh (primaries ratified) |
| 2026-11-25 | EDU-LG-02 refresh before December (MUST_PUBLISH) | GSC baseline (G-01) |
| 2026-12-01 / 12-08 | BC-031 trends, BC-034 Valentine's (MUST_PUBLISH) | Drafts |
| Passed, not live | BC-001, 004, 035, 018, 036, 006 (2026-10-04…09) | E-01 — is publishing paused for AWS? |
""" % (TODAY, c["Priority"]["CRITICAL"], c["Priority"]["HIGH"], c["Priority"]["MEDIUM"], c["Priority"]["LOW"], len(rows),
       c["Status"]["READY FOR IMPLEMENTATION POST-AWS"],
       sum(c["Status"][k] for k in ("HOD INPUT REQUIRED", "ENGINEERING INPUT REQUIRED", "GSC BASELINE REQUIRED", "CONDITIONAL — PRODUCT/OFFER CONFIRMATION")),
       "\n".join("%d. %s" % (i + 1, t) for i, t in enumerate(top10)),
       mdt(["WP", "Scope", "State", "Needs", "Class B", "Class C"], wp),
       len(crit), lst(crit), len(high), lst(high), c["AWS Class"]["A"], n_new, n_draft, c["AWS Class"]["B"], c["AWS Class"]["C"])


def doc09(rows):
    reg = []
    for oid, name, cur, cand, dec, dep, prov, owner in OD_ORIG:
        reg.append([oid, name, cur, cand, dec, prov, "**" + FN.DISP[oid] + "**", "10 §" + oid])
    return """# 09 — On-Page Decisions Register (original proposals, 2026-10-09)

> **SUPERSEDED for status by `10-DECISIONS-RESOLUTION-LOG.md` (2026-10-10).** This file preserves the original decision register and provisional recommendations so the audit trail is intact; the right-hand columns show the final disposition. The redirect plan, business-fact register, engineering questions and GSC request that used to sit here now live in `10` §5, `11`, `12` and `13` (no duplicates).

## 1. Original register with final disposition

%s

## 2. Original commercial candidate lists (evidence, not ownership at the time)

Candidate heads per page are now in `10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv` with the final assignment, volume, KD, DFS intent label, SERP-evidence status and confidence.

## 3. Original OD-03 mismatch table and OD-04 confirmation list

Final resolutions: `10-DECISIONS-RESOLUTION-LOG.md` §4. The 12 mismatch pairs and 8 ownership items below are unchanged from the 2026-10-09 proposal.

%s

%s
""" % (mdt(["ID", "Decision", "CURRENT STATE (original)", "CANDIDATE / PROPOSED (original)", "DECISION REQUIRED (original)", "PROVISIONAL RECOMMENDATION (original, not adopted at the time)", "FINAL DISPOSITION", "Where"], reg),
       mdt(["Page", "Calendar primary", "Stage 17/19 primary", "Stage 15 mapped keywords", "Original proposal"],
           [[rid, "'%s' (%s/mo)" % (v[1], v[2]), "'%s'" % v[0], stage15_str(rid), "R2: calendar primary, brief term co-primary"] for rid, v in s2_edu.MISMATCH.items()]),
       mdt(["Item", "Calendar primary", "Original question"], [[k, "'%s' (%s/mo)" % (CAL[k]["primary_keyword"], CAL[k]["primary_search_volume"]), "Owner confirmation (OD-04)"] for k in sorted(s2_edu.CONFIRM)]))


def doc10(rows, K):
    by = {r["Row ID"]: r for r in rows}
    states = collections.Counter(x["Assignment State"] for x in K)
    summary = []
    for oid, name, cur, cand, dec, dep, prov, owner in OD_ORIG:
        r = RES[oid]
        summary.append([oid, name, "**" + FN.DISP[oid] + "**", short(r["res"], 230), r["conf"].split(";")[0].split(" (")[0].split(".")[0]])
    # OD-01 tables
    def krow(x):
        return [x["Row ID"].replace("SUB:", ""), x["Primary Keyword"], x["Volume (US/mo)"], x["KD"], x["DFS Intent Label"], short(x["Secondary / Held Keywords"], 120) or "—", x["Assignment State"], x["Confidence"]]
    hubs = [x for x in K if not x["Row ID"].startswith("SUB:") and x["Row ID"] not in ("NAV-HOME", "COM-SHOP", "COM-COLLECTION", "BRAND-ABOUT", "BRAND-CONTACT", "SUP-FAQ", "SUP-POLICIES-SHIP", "SUP-POLICIES-RET", "SUP-POLICIES-PRIV", "SUP-POLICIES-TERMS", "BLOG-HUB", "EDU-ROOT", "COM-PDP")]
    subs = [x for x in K if x["Row ID"].startswith("SUB:")]
    kh = ["Row", "Primary", "Vol/mo", "KD", "DFS label", "Secondary / held", "State", "Conf."]
    # OD-03 table
    t3 = []
    for rid, (s19, calp, vol, t_cal, t_br) in s2_edu.MISMATCH.items():
        fp, cop, why = FN.EDU3[rid]
        r = by[rid]
        t3.append([rid, "'%s' (%s/mo)" % (fp, vol), cop, r["Recommended Title (pre-suffix value)"], r["Recommended H1"], r["Status"], why])
    t4 = []
    for rid, (o, treat, src) in FN.EDU4.items():
        r = by[rid]
        t4.append([rid, o, treat, src, r["Status"]])
    redirects = mdt(["#", "Source (404 today)", "Destination (200, in sitemap)", "Type", "Why", "Priority", "Note"], [list(x) for x in FN.REDIR])
    empties = mdt(["Page", "Treatment", "Redirect?", "Note"], [list(x) for x in FN.EMPTY])
    other = mdt(["URL / set", "Treatment", "Dependency"], [list(x) for x in FN.OTHER_PATHS])
    det = []
    for oid, name, cur, cand, dec, dep, prov, owner in OD_ORIG:
        r = RES[oid]
        det.append("### %s — %s\n\n**Disposition: %s**\n\n* **Original proposal (09):** %s\n* **Final resolution:** %s\n* **Rationale:** %s\n* **Evidence / sources:** %s\n* **Confidence:** %s\n* **External dependency:** %s\n* **Reversibility / review:** %s\n"
                   % (oid, name, FN.DISP[oid], prov, r["res"], r["why"], r["ev"], r["conf"], r["dep"], r["rev"]))
    return """# 10 — Decisions Resolution Log (Step 2A)

Date 2026-10-10. **Authority:** the user delegated routine and research-supported decisions on 2026-10-10. **Scope:** decisions only — nothing is implemented; the final calendar, Stage 12–19 research files, Step 1 outputs and approved blog packages were not modified (Stage 15 ownership files are untouched; this log and `10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv` are the ratification record, per CLAUDE.md §10). **No paid DataForSEO call.** The original proposals are preserved in `09`.

## 1. Summary of dispositions (all 19 decisions)

%s

Dispositions: **ADOPTED** (decision made and propagated), **ADOPTED — … PENDING** (decision made; a named external fact/data item refines or reverses it), **INTAKE/REQUEST PREPARED** (genuinely external; specification not blocked). No decision is left silently unresolved.

## 2. Method and evidence rules

* **Evidence types.** *SERP-VALIDATED* (Stage 8/18.5) is claimed for only four head terms: 'side stones engagement rings' (CATEGORY-dominant), 'lab grown diamonds', 'lab diamonds' and 'natural diamonds'. Every other commercial assignment is *volume + DataForSEO intent label (SERP type NOT validated)* — stated per row.
* **Confidence.** HIGH = broad head → hub or unique specific match, measured volume, consistent with the architecture; MEDIUM = measured volume with unvalidated SERP type or some intent ambiguity; LOW = proxy volume, thin inventory or ambiguous head.
* **Inventory** facts come from product links in the initial HTML of the 2026-10-09 crawl (listing pages cap at 24, so large counts are lower bounds).
* **Reversible defaults** are used wherever evidence cannot settle a question; none involves a URL change or an irreversible index action.
* **No fake precision:** no scores, no invented volumes; GSC values are never shown.

## 3. Decisions in detail

%s

## 4. Education resolutions

### OD-03 — the 12 primary-keyword mismatches (R2 adopted)

%s

### OD-04 — the 8 ownership items

%s

## 5. Developer-ready redirect and index-control specification (planning only — Class B)

**Redirects (OD-06)** — 1:1, permanent (301), no chains, query strings preserved (E-04):

%s

**Duplicate grouping page (OD-06):** `%s` — %s. Reason: %s

**Empty and test pages (OD-07)** — each handled individually; none redirected to an irrelevant destination:

%s

**Other URL behaviors:**

%s

**Implementation notes for developers:** (1) apply `noindex,follow` via meta robots (not robots.txt) so crawlers can see the directive; (2) remove the same URLs from sitemap.xml, `/llms.txt` and the header menu; (3) re-add automatically when a listing has ≥1 product only after the D-07 gate has been run (no numeric threshold is invented here — D-07 leaves the minimum to implementation); (4) verify after AWS: 301 → 200 single hop, group-page canonical, noindex present, sitemap membership, no internal links to /by-desgin/.

## 6. Reversible defaults and review triggers

| Item | Default adopted | Review trigger | Evidence needed |
|---|---|---|---|
| Wedding-band hub vs /for-her duplicate | /for-her canonical → hub | Men's range confirmed (F-E3) | F-E3 |
| Thin-inventory assigned pages (bezel 2, toi et moi 1, anniversary 1, lariat 1, chain-link 1, pendant 3, T-bar 4) | Indexable with unique intro | 90 days post-cut-over | G-02 Queries/Pages |
| No-keyword populated pages (pavé, nature-inspired, multi-stone, toi-et-moi necklace) | Indexable, not promoted | 90 days post-cut-over (D-07 gate #1 unmet) | G-02 |
| Bangles category (label vs contents) | Interim title/meta/H1 scoped to 'link bracelets'; copy held; no keyword | HOD answers F-E7 | F-E7 |
| 'toi et moi ring', 'eternity ring/band' (DFS-informational) | Secondary on the commercial page | First GSC Queries read | G-02 / SERP check |
| Shape landing pages (round 22,200; oval 60,500) | Not created — shapes stay filters (D-08) | GSC shows query demand landing on filters | G-02 |
| FJ rings ('diamond ring' 110,000) | HELD, descriptive title | GSC Queries | G-02 |
| Lab-grown commercial hub | Not built | F-E2 = yes | F-E2 |
| Group page canonical → redirect | Canonical | Breadcrumbs repointed + no standalone demand | E-13, G-03 |
| Carat-variant PDP URLs | Keep | Post-cut-over review | G-01, E-09 |

## 7. What could not be fully resolved, and why

* **FJ rings (`/fine-jewellery/rings`)** — HELD: 'diamond ring' (110,000) spans engagement/wedding/fashion intent, the page lists 2 products and its only child is empty; no SERP evidence. Reversible default: descriptive non-bridal title.
* **Informational-labelled heads** ('toi et moi ring', 'eternity ring/band') — assigned as same-page secondaries; SERP type cannot be confirmed without GSC/SERP data.
* **Bangles page (`/fine-jewellery/bracelet/bangles`)** — the category label is 'Bangles' but both listed products are named link bracelets, and no product in the catalog is described as a bangle. Whether HOD sells or plans bangles, and whether the page should be kept, renamed or folded into `/chain-link`, cannot be inferred from the catalog. Resolution: interim copy scoped to 'link bracelets' (no bangle claim), copy HELD, status `CONDITIONAL — PRODUCT/OFFER CONFIRMATION`, one narrow question (F-E7). Product sets of `/bangles` (2), `/chain-link` (1) and `/tennis` (8) are disjoint.
* **Lab-grown hub** — decided (not built), but reverses on one HOD fact (F-E2).
* **Calendar annotation (done 2026-10-10)** — in `Keywords/content SEO/FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv`, the single field `target_owner` of row `content_id = BLOG-WR-TYPES` was changed from 'Blog (Style & Trends)' to `EDU-WB-TYPES` with your explicit approval. Nothing else in the calendar changed (date, slot, title, primary keyword and every other field are untouched); this is separate from the finalized Step 2 specification.

## 8. Correction pass and close-out 2026-10-10

A targeted correction pass and close-out, not a new SEO stage; all 147 rows and all 19 dispositions are unchanged.

1. **Spelling defect (`jewelery`).** Root cause: the generator's US-spelling list replaced the prefix `⟦jeweller⟧` before `⟦jewellery⟧`, producing the misspelling `jewelery`, and its verb stems also turned `symbolism` into `symbolizm`. Fixed at source (`_build/s2_build.py`, `s2_write.py`): longest forms first, verb stems need an inflection suffix, hyphenated words (`ring-centered`, `near-colorless`) are normalized, URL/slug-like tokens are protected, and quoted current-site text is marked verbatim. A generated link-spec note that described anchor spelling as still awaiting OD-05 (22 link rows) was removed; OD-05 is adopted. Current-site text kept verbatim as evidence: the live About tile 'Certified Jewelery', current titles/metas/H1s, schema category values and URL slugs.
2. **Bangles category.** See §7 and F-E7: label vs contents contradiction resolved by scoped interim wording plus a held status.
3. **Bespoke timeline vs shipping facts.** See §9.
4. **BC-001 publication hold (close-out).** The approved package is protected and was **not** edited; only the status of its *future publication* changed. BC-001 moved from `READY FOR IMPLEMENTATION POST-AWS` to `HOD INPUT REQUIRED` (action `HOLD PUBLICATION (pending F-A1)`) because its approved meta, intro and article say '6–9 days of insured shipping' and insurance is unconfirmed (SR-02) — the questionnaire's rule is that unverified claims are not published. If HOD confirms insured shipping, the existing approved wording may proceed after the normal human review; if not, a separate, explicitly authorized content revision is required before publication.
5. **Calendar annotation (close-out).** Done with your approval: only `target_owner` of `BLOG-WR-TYPES` changed, to `EDU-WB-TYPES` (§7).
6. **Root `CLAUDE.md` and project memory** synchronized with the counts above.

## 9. Source reconciliation

| ID | Item | Authoritative source | Result | Action |
|---|---|---|---|---|
| SR-01 | Bespoke timeline start point ('from design approval') | `confirmed_business_facts.md` (user-supplied 2026-09-29) records '2–3 weeks to make + ~6–9 days delivery; generally ~3–4 weeks; depends on the stone selected' and does not name a start point. The project owner stated 'from design approval to delivery' in the 2026-10-10 Step 2A brief, and the approved BC-001 package uses the same bracket. | **Confirmed** — the whole timeline is treated as confirmed. HOD is not asked to repeat it. | Optional housekeeping for the user: add the start point to the protected facts file. |
| SR-02 | 'Insured' shipping wording | Not in the confirmed-facts file, which says only 'delivery'. The approved BC-001 package says '6–9 days of insured shipping'; the live header badge says 'Complimentary Insured Shipping'. | **Unconfirmed.** Insurance, carrier and signature terms belong to the broader shipping policy (F-A1). | BC-001 is protected and not modified, but its **publication is HELD** (status `HOD INPUT REQUIRED`) until F-A1 is answered. If shipments are insured: the approved wording may proceed after the normal human review. If not: a separate, explicitly authorized content revision is required before publication. The bespoke delivery fact itself is unaffected. |

The bespoke **timeline** (confirmed) and the **shipping policy** (regions, carriers, insurance, duties/taxes, free-shipping terms, holiday order-by dates — F-A1) are separate facts: the first is applied everywhere; the second stays removed/neutral until HOD answers.

## 10. Changes made by Step 2A/2B

Master CSV, link spec, PDP priority list and docs `02–09` regenerated from the updated sources (`_build/`); new files `10`, `10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv`, `11`, `12`, `13`. Root `CLAUDE.md` status/decision sections updated per its §17. Nothing else changed.
""" % (mdt(["ID", "Decision", "Disposition", "Final resolution (short)", "Confidence"], summary), "\n".join(det),
       mdt(["Page", "Final primary", "Co-primary / treatment of the brief term", "Final title (pre-suffix)", "Final H1", "Status", "Note"], t3),
       mdt(["Item", "Final owner", "Treatment", "Source rule", "Status"], t4),
       redirects, FN.GROUP[1], FN.GROUP[2], FN.GROUP[3], empties, other) + """
## Appendix — OD-01 assignment summary (%d assignment rows; full detail in the CSV)

Assignment states: %s.

### Category hubs, bespoke and conditional hub

%s

### Subcategories

%s
""" % (len(K), "; ".join("%s %d" % kv for kv in states.most_common()), mdt(kh, [krow(x) for x in hubs]), mdt(kh, [krow(x) for x in subs]))


def doc11():
    t = {1: "MUST ANSWER — blocks page copy or trust claims", 2: "SHOULD ANSWER — changes product architecture or the offer we describe", 3: "NICE TO HAVE — completes copy and structured data"}
    blocks = []
    for tier in (1, 2, 3):
        rows = [[f[0], f[2], f[3], f[4], f[5], f[6]] for f in FN.FACTS if f[1] == tier]
        blocks.append("### %s\n\n%s" % (t[tier], mdt(["#", "Area", "Fact we need", "Where it appears today", "What we do until you answer", "What it unblocks"], rows)))
    return """# 11 — House of Diams: Facts We Need From You

*One consolidated list. Please answer each item with one of: **CONFIRM** (it is true as stated), **CORRECT** (here is the right wording), or **REMOVE** (do not make this claim). If an item does not apply, say "not offered". We will not publish any of these claims until you answer, and we do not assume that every product or service listed below is currently offered.*

## Already confirmed — no action needed

| Fact | Wording we use |
|---|---|
| Bespoke jewelry typically takes **2–3 weeks to make**, followed by **approximately 6–9 days for delivery**; generally about **3–4 weeks from design approval to delivery**; depends on the stone selected | Always "typically / approximately"; never a guaranteed delivery date; no holiday cut-off is stated |

*Source:* the timeline was supplied and confirmed on 2026-09-29 (`confirmed_business_facts.md`); the start point "from design approval" was confirmed by the project owner on 2026-10-10 (that file does not yet record it — see SR-01 in `10-DECISIONS-RESOLUTION-LOG.md` §9). **Nothing to answer here.**

**Not part of that confirmation:** insured shipping, carriers, duties/taxes, free-shipping terms and holiday order-by dates are *shipping-policy* facts (F-A1 below), not part of the bespoke timeline. In particular, the word "insured" in the approved BC-001 article and in the site header badge is unconfirmed until F-A1 is answered (SR-02); BC-001's publication is held until then (the package itself is unedited).

%s

## How your answers are used

* **MUST ANSWER** items complete `/shipping`, `/returns`, `/about`, `/contact`, the bespoke process copy and every trust badge. Until answered, those claims are removed or neutral.
* **SHOULD ANSWER** items decide whether we describe the catalog as lab-grown in titles, whether a separate Lab-Grown Diamonds page makes sense, whether men's/Hip Hop pages stay hidden, and whether the 'Bangles' category stays as labeled (F-E7).
* **NICE TO HAVE** items finish structured data and a few guides.

**Fastest path:** answer the 6 MUST ANSWER items (F-A1, F-A2, F-B1, F-C1, F-C2, F-D1) first.
""" % "\n\n".join(blocks)


def doc12():
    return """# 12 — Engineering Inputs (AWS migration)

Short intake for the developers. **None of these block the On-Page SEO specification**; each blocks only the implementation step shown. Until answered, every Class B action stays post-migration and is listed as awaiting engineering input. Source decisions: `10-DECISIONS-RESOLUTION-LOG.md`.

%s

## Defaults we will assume if there is no answer

* Titles/metas/H1s/category names are edited in the CMS or product data; URLs stay identical; redirects are applied at the edge or application layer with query strings preserved.
* Sitemap and robots generators are re-implemented and can exclude individual URLs.
* Listing pagination keeps `?page=N` with a self-referencing canonical (page-number titles only if the template supports them).
""" % mdt(["ID", "Question", "Why it matters", "Blocked / affected actions"], [list(e) for e in FN.ENG])


def doc13():
    return """# 13 — GSC Data Request

Search Console data is not available in the project (the connector requires a subscription and no export exists), so **no clicks, impressions, CTR or positions are used anywhere in the package**; DataForSEO positions quoted for equity URLs are Stage 3 estimates. Routine specification work is not held up — only the items marked *blocking* below.

%s

## Which decisions this can change

| Item | Blocking? | Rows |
|---|---|---|
| Title/H1/body edits on ranking-equity URLs (CVD vs HPHT, lab-grown vs natural, how-to-choose, 14K vs 18K) | **Yes** — baseline first (CLAUDE.md §8) | EDU-LG-03, EDU-LG-02, EDU-LG-10, EDU-MET-01 |
| Oval PDP title/H1/schema-name change | **Yes** | COM-PDP-OVAL-FLORAL |
| 301 for the removed marquise-floral PDP | **Yes** (only redirect if equity) | LEG-marquise-floral… |
| by-desgin → by-design redirects | No — a 1:1 redirect is the safe direction; G-03 only confirms indexed state | R-01…R-09 |
| Thin-inventory/no-keyword page reviews, informational-labelled heads, shape landings, FJ rings | No — 90-day review after cut-over | see `10` §6 |

## Export format

CSV or the GSC UI export is fine: Pages and Queries tabs, 16 months, Search type = Web; one file for United States and one for all countries; include the 'Page × Query' export for the listed URLs if possible.
""" % mdt(["ID", "Export / access", "Used for", "Affects"], [list(g) for g in FN.GSC])


def readme(rows, qc):
    c = counts(rows)
    ready = c["Status"]["READY FOR IMPLEMENTATION POST-AWS"]
    return """# On-page SEO — Step 2 package (finalized 2026-10-10)

**Status:** Step 2A (decision resolution) and Step 2B (finalization) complete. This is a **specification package**: nothing on the live site, the CMS, the research, the keyword-ownership files or the BC-001 package was changed (the only edit outside this folder is the single approved `target_owner` annotation in the final calendar, plus status synchronization of root `CLAUDE.md`), and no paid DataForSEO call was made. Step 1 (`../QA/01–06`) was not modified.

## What is final, what is blocked

* **Final and ready for developers after the AWS migration:** %d of %d rows (`READY FOR IMPLEMENTATION POST-AWS`).
* **Final specification, content still to be written (Class A):** %d rows (`PRE-AWS PREPARATION`).
* **Blocked by one named external input:** %d rows — HOD facts %d (`HOD INPUT REQUIRED`), GSC baseline %d (`GSC BASELINE REQUIRED`), product/offer confirmation %d (`CONDITIONAL — PRODUCT/OFFER CONFIRMATION`). Engineering inputs (E-xx) never change *what* to do, only *how/when*.
* **No change / not planned:** %d rows.
* **Intended implementation:** after the AWS cut-over, in the order of `08`; copy-only items may move earlier only if engineering confirms the content store is editable and outside the freeze (E-01/E-02).

## Close-out status (2026-10-10) and remaining actions outside this package

**Done:**

* **BC-001 publication held.** The approved package is protected and unedited; only the status of its future publication changed (`HOD INPUT REQUIRED`, action `HOLD PUBLICATION (pending F-A1)`). Its approved meta, intro and article say '6–9 days of insured shipping', and insurance is unconfirmed (SR-02). If HOD confirms insured shipping, the existing approved wording may proceed after the normal human review; if not, a separate, explicitly authorized content revision is required before publication.
* **Calendar owner annotation.** In `Keywords/content SEO/FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv`, row `content_id = BLOG-WR-TYPES`, field `target_owner` changed from `Blog (Style & Trends)` to `EDU-WB-TYPES` with the user's approval. No other calendar field changed.
* **Root `CLAUDE.md` and project memory** synchronized with this status.

**Still open (external inputs only):**

1. **HOD facts** (`11`): F-A1 (also decides BC-001 publication), F-A2, F-B1, F-C1, F-C2, F-D1 (must answer); F-A3, F-E1, F-E2, F-E3, F-E7 (should answer); F-E4, F-E5, F-E6 (nice to have).
2. **Engineering inputs** (`12`, E-01…E-13) and the **GSC exports** (`13`, G-01…G-06).
3. **Confirmed-facts file (optional housekeeping, SR-01).** `Keywords/content SEO/content-strategy/blog-calendar/revision/confirmed_business_facts.md` does not record the start point 'from design approval' (stated by the project owner on 2026-10-10). The package already treats the timeline as fully confirmed.

## Files

| File | What it is |
|---|---|
| `01-ON-PAGE-SEO-MASTER.csv` | **Operational file** — %d rows: current vs final title/meta/H1, content, links, schema, AEO/GEO, image rules, priority, AWS class, decision resolution, remaining dependencies, status, evidence. |
| `02-ON-PAGE-SEO-MASTER.md` | Overview, counts, vocabularies, page-family rules, limits. |
| `03-TITLE-META-OPTIMIZATION.md` | Brand-suffix verification, rules, every title and meta, claims removed from the Step 1 drafts. |
| `04-H1-CONTENT-OPTIMIZATION.md` | H1 table, content specs per page, trust-critical pages. |
| `05-INTERNAL-LINK-IMPLEMENTATION.md` + `.csv` | Link specifications with real URLs (Stage 16 + calendar + Step 2A additions). |
| `06-SCHEMA-AEO-GEO-SPEC.md` | Schema (current / recommended / why / dependency / validation), AEO, GEO/entity, image rules. |
| `07-PDP-ON-PAGE-SEO.md` + `07-PDP-PRIORITY-ACTIONS.csv` | PDP rules and the PDPs needing special treatment. |
| `08-ON-PAGE-IMPLEMENTATION-PRIORITIES.md` | Top 10, work packages, CRITICAL/HIGH lists, A/B/C split. |
| `09-ON-PAGE-DECISIONS-REQUIRED.md` | Original decision register (2026-10-09) with final dispositions — audit trail. |
| `10-DECISIONS-RESOLUTION-LOG.md` + `10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv` | All 19 decisions: disposition, rationale, evidence, confidence, dependency; keyword assignments; Education resolutions; redirect/index-control spec. |
| `11-HOD-CLIENT-FACTS-REQUEST.md` | One consolidated questionnaire for HOD. |
| `12-ENGINEERING-INPUTS.md` | Engineering intake and what each answer unblocks. |
| `13-GSC-DATA-REQUEST.md` | GSC exports/access needed and what they affect. |
| `_build/` | Generator, resolution data (`s2_final.py`) and read-only QC (`qc_step2.py`). Do not rerun `s2_write.py` unless asked — it overwrites the files above. |

## Conventions

American English for all customer-facing copy (slugs such as `/fine-jewellery/` are unchanged). Titles are **pre-suffix** values (the template appends ` | House of Diams`; the homepage is absolute). Volumes/KD/intent labels come from existing project files — SERP type is validated for only four head terms. GSC values are never shown. Business facts are never invented: only the bespoke timeline is confirmed.

## QA performed

%s
""" % (ready, len(rows), c["Status"]["PRE-AWS PREPARATION"],
       sum(c["Status"][k] for k in ("HOD INPUT REQUIRED", "ENGINEERING INPUT REQUIRED", "GSC BASELINE REQUIRED", "CONDITIONAL — PRODUCT/OFFER CONFIRMATION")),
       c["Status"]["HOD INPUT REQUIRED"], c["Status"]["GSC BASELINE REQUIRED"], c["Status"]["CONDITIONAL — PRODUCT/OFFER CONFIRMATION"],
       c["Status"]["NO CHANGE REQUIRED"] + c["Status"]["NOT PLANNED — CONDITIONAL"], len(rows), qc)
