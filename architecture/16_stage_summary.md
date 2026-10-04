# Stage 16: Internal linking architecture (summary)

Date: 2026-09-24. Status: **COMPLETE**, with one label exception that needs sign-off (see Unresolved). Local project files only. **No DataForSEO call, no other API call, no live-site request, $0.00.** Cumulative project spend is unchanged at $0.33536.

## Scope

This stage designs the internal-link architecture: which pages link to which, of what link type, with which anchor, at what priority, and when. It does **not** change or recommend:

- URLs, slugs, redirects or canonicals
- indexability
- keyword owners
- page creation, merges or deletions
- platform implementation

Stage 15 ownership and the Stage 12/14 hierarchy are upstream constraints.

## Files read

- **Stage 7:** master keyword database and summary.
- **Stage 8:** SERP validation and summary.
- **Stage 10:**
  - existing content inventory
  - keyword coverage, equity, overlap, SERP alignment and business-area coverage
  - summary: nav check §1a; no internal-link data, §9
- **Stage 11:** cluster registry, keyword cluster map, relationships, summary and methodology.
- **Stage 12:**
  - IA proposed structure
  - page-type framework
  - current vs proposed IA
  - IA decision log (D-01 to D-19) and summary
- **Stage 13:**
  - existing content decisions
  - ranking equity analysis
  - Blog/Education framework
  - migration risk
  - blog strategy and stage summary
- **Stage 14:**
  - Education architecture and hierarchy
  - cluster consolidation
  - page-type framework
  - existing-content mapping
  - decision log (D14-01 to D14-30) and summary
- **Stage 15:**
  - keyword→URL map
  - target page registry
  - cluster page map
  - cannibalization check
  - decision log
  - ranking equity protection
  - summary
- **Project files:** `README.md`, `progress.md`, `decision-log.md`, `CLAUDE.md`.

## Methodology

1. **Page set.** The page set has 70 pages plus 2 site templates:
   - **27 Stage 15 target IDs, unchanged.**
   - **43 architecture nodes that own no keyword.** Their IDs follow the prefixes in `build_16.py`.
     - Education root and the Ring & Jewellery Guides index.
     - 13 Stage 14 CONDITIONAL topics.
     - Commercial hubs, categories and subcategory groups.
     - Bespoke, the PDP template, the Blog hub and 6 Blog category templates.
     - FAQ, policies, About and Contact.
     - The deferred online-ring article.
   - **Not given an ID, and never linked:** Stage 14 DEFERRED topics (per-shape pages, IGI-only, moissanite explained, gemstones, engagement-ring buying guide) and Stage 12 deferred or not-proposed nodes (natural commercial hub, loose/carat pages, wholesale, Hip Hop placeholder).
2. **Hierarchy links generated from Stage 14.** Hub → child and child → hub breadcrumb rows were generated programmatically from `14_education_hierarchy.csv`, so the Education parent/child structure cannot drift from Stage 14.
3. **Commercial, Blog, FAQ and cross-system rows written one by one.** Each has a `context_reason` citing its evidence (D-xx, D14-xx, Stage 13 §, Stage 15 pair).
4. **Anchors.**
   - Each anchor is typed.
   - Each anchor and variant is tested against every Stage 15 keyword. An anchor that equals a keyword owned or held by a different page fails QC.
   - Exact-match anchors must be keywords the target already owns.
5. **Connectivity.**
   - **Existing pages:** status comes from observed facts only (sitemap, Stage 10 nav check, hub listings). There is no crawl data, so there are no invented counts.
   - **Proposed pages:** get `LINKING_REQUIREMENT_AT_LAUNCH`.
   - **All non-conditional pages:** a planned-connectivity bar is tested.
6. **QC.** `architecture/scripts/qc_16.py` runs 69 checks: the 20 brief checks, plus schema, density, connectivity and relationship-coverage checks. It includes sha256 checks of the 191 pre-Stage-16 files and reruns the earlier-stage QC scripts.

## Numbers

| Item | Count |
|---|---|
| Source→target relationships | **390**: 153 REQUIRED, 79 RECOMMENDED, 42 OPTIONAL, 116 CONDITIONAL |
| Structural / contextual rows | 169 / 221 |
| Pages assessed | **70** (28 existing, 1 existing PDP group, 5 existing-conditional, 16 proposed, 5 Blog templates, 15 conditional) + 2 templates |
| Anchor-strategy rows | 157 |
| Anchor types | NAVIGATIONAL 183 · DESCRIPTIVE 106 · NATURAL_LANGUAGE 68 · BRANDED 17 · PARTIAL_MATCH 12 · **EXACT_MATCH_ALLOWED 4** |
| Rows on flagged adjacent-intent pairs | 39 (HIGH 4 · MEDIUM 23 · LOW 10 · INSUFFICIENT_EVIDENCE 2), each with a guard |

## Protected ranking URLs

All 28 Stage 3 ranking keywords sit on 6 URLs, and all 6 are linked **at their current URL**.

| Page | URL | Stage 3 kw | Contextual incoming (non-conditional) |
|---|---|---|---|
| EDU-LG-03 | `/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams` | 19 (18 targeted + `cvd/hpht diamond tester` excluded) | 7 |
| EDU-LG-02 | `/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams` | 3 | 11 |
| EDU-MET-01 | `/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams` | 3 | 3 |
| EDU-LG-10 | `/blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide` | 1 | 8 |
| COM-ER-SIDESTONE | `/engagement-rings/by-desgin/side-stone-rings` | 1 | 2 (+ nav, category tile, PDP breadcrumbs) |
| COM-PDP-OVAL-FLORAL | `/shop/oval-floral-diamond-ring` | 1 | 2 (+ 3 product grids) |

The per-URL sources, anchor concepts and "must not use as anchor" rules are in `16_linking_rules.md` §7.

## Orphan and connectivity findings

- **TRUE_ORPHAN: 0 confirmed.** This rests on sitemap, nav and hub-listing evidence. No crawl exists, so this is "none observed", not "none measured".
- **WEAKLY_CONNECTED: 13.** The 9 Education-owned articles are the main finding:
  - They sit on `/blog` URLs and are reachable only from the Blog hub listing. `/education` lists just one article (GIA vs IGI).
  - They include all 4 protected Education URLs.
  - Nav placement of `/education` and `/blog` is not recorded.
- **NAV_ONLY: 20.** This covers all commercial categories and subcategories, the side-stone ranking page (nav-linked, not in the sitemap), PDPs, Bespoke and the support pages. None has recorded contextual support.
- **WELL_CONNECTED: 1** (homepage).
- **Launch requirements: 36 proposed or conditional pages.**
  - 21 non-conditional ones (16 Education, 5 Blog templates) are `LAUNCH_BLOCKER_IF_MISSING`: each ships with its REQUIRED incoming links.
  - 15 are conditional and are linked only if activated.
- **Planned bar:** met by every non-conditional page. One documented exception: the deferred online-ring article, which is deliberately not boosted while the D-19 / OV-06 boundary is open.

## Major architectural relationships

- **Education ↔ commercial.**
  - Buying guides, comparisons, shapes, metals, settings and sizing hand off to Engagement Rings, Wedding Bands or the side-stone subcategory at the decision point.
  - Categories link back to at most 5 Education owners. Engagement Rings links to Shapes, 4Cs and Ring Size (required), Lab-vs-natural (recommended) and How to Choose (optional).
  - PDPs link to at most 3 owners, through template labels.
- **Lab-grown.**
  - The pillar hands CVD/HPHT, lab-vs-natural, authenticity and buying to their owners. These are the only 4 exact-match anchors in the map.
  - The commercial head term is reserved for the CONDITIONAL commercial hub. Until that hub exists, the pillar's commercial exit is Engagement Rings with a descriptive anchor.
- **Natural and Gemstones.** Education-only, with no commercial links.
- **Certification.** The pillar and GIA vs IGI link to each other and ship together. There is no IGI-only target.
- **4Cs.** The pillar links each C to its guide. The clarity guide links to SI and VVS. VS stays a section until EDU-4C-04 is justified.
- **Shapes.** One pillar. It uses cut-grade anchors to point to the cut guide, not to itself. It links the oval PDP as an illustrative example only.
- **Blog.** Six category templates. Each links to the Education owner of any concept it mentions and to the category or product it features. Craft and Stories link to Bespoke.
- **FAQ.** The owners named in D14-30: EDU-LG-01, EDU-LG-02, EDU-CERT-00/01 and EDU-RJG-02. Policies and Contact.
- **Transitional.** `/education` and `/blog` list the Education-owned `/blog` articles (CONDITIONAL rows) until each parent hub is live. A listing is never removed before a replacement path exists.

## Important exceptions

1. **Education hub labels.** Anchors and breadcrumbs read "Lab-Grown Diamond Guide" and "Natural Diamond Guide", because the bare labels are commercial head terms that Stage 15 holds for the conditional or deferred commercial hubs. The Stage 14 hub names are unchanged, but this needs user sign-off.
2. **Education-owned `/blog` URLs** are treated as Education for breadcrumbs and hub listing before any move (Stage 13 §6).
3. **The deferred online-ring article** is intentionally left weakly connected.
4. **Related products** (PDP template → other PDPs) is the only self-row, and it is justified.

## Unresolved questions

These are genuinely unsupported by current evidence:

- **Commercial Lab-Grown hub approval** (D-05). 12 CONDITIONAL rows depend on it.
- **Which products ship with IGI/GIA reports,** and **which karats are offered.** These gate the PDP → certification and PDP → 14k-vs-18k links.
- **Natural, moissanite, gemstones, loose stones and wholesale** (Stage 12 business questions). No commercial links are proposed for them.
- **Which style, type and gender subcategories stay populated** (merchandising and the D-07 gate).
- **D-19 commercial supplement (unapproved).** Decides the online-ring article's role and the engagement-ring buying-guide boundary.
- **D-15 jewellery/jewelry spelling.** Affects nav labels and 2 URL_PENDING hub slugs.
- **Blog editorial capacity.** Craft and story posts must exist before those links activate.
- **Post-launch crawl.** Needed to replace the observed statuses with measured link counts.

## QC result

`python3 architecture/scripts/qc_16.py` gives **69/69 PASS**. This covers:

- all 20 brief checks
- schema and vocabulary checks
- link-density caps
- the planned-connectivity bar
- relationship-family coverage
- sha256 checks showing all 191 pre-Stage-16 files unchanged, including every Stage 7–15 output
- the Stage 15 checksum set still unchanged
- `qc_14.py` still passes, and with it `qc_12` and `qc_13`
- `qc_15.py` passes 59/60. Its only failure is its point-in-time check 19, "no files created after Stage 15", and the only files it flags are the nine Stage 16 deliverables. That is expected, and qc_16 asserts it. Stage 15 files were not edited to silence it.

## No paid API used

No DataForSEO endpoint (paid or free) and no other API was called. No live-site request was made. No site, CMS, URL, redirect, canonical, robots or sitemap change was made. The D14-29 SERP batch and the D-19 supplement remain not approved and were not run.

---

**STAGE 16 STATUS:**
COMPLETE. One item needs review: the Education hub label exception (Lab-Grown / Natural "Guide" labels).

**DATAFORSEO:**
$0.00

**PAID CALLS:**
0

**FILES CREATED:**
- architecture/16_internal_link_map.csv
- architecture/16_page_link_requirements.csv
- architecture/16_anchor_strategy.csv
- architecture/16_orphan_and_connectivity.csv
- architecture/16_linking_rules.md
- architecture/16_stage_summary.md
- architecture/scripts/build_16.py
- architecture/scripts/qc_16.py
- architecture/scripts/16_upstream_checksums.json

Also updated: cost-log.csv (Stage 16 row, $0), progress.md and decision-log.md.

**QC:**
69/69 PASS (qc_15 reports 59/60 only because Stage 16 files now exist; see QC result)

**KEY FINDINGS:**
- The 9 Education-owned `/blog` articles, including all 4 protected Education ranking URLs, are reachable today only through the Blog hub listing; `/education` lists one article. The largest connectivity gain is giving them an Education path (hub listing + breadcrumb + REQUIRED contextual links) without moving them.
- A bare "Lab-Grown Diamonds" or "Natural Diamonds" breadcrumb or nav label on Education would send commercial head terms (135,000 and 18,100) to informational pages. Stage 16 reserves the bare lab-grown label for the conditional commercial hub and uses "Guide" labels in Education.
- Commercial pages are NAV_ONLY today. The side-stone ranking page is linked only from nav (and is not in the sitemap). The map gives it a REQUIRED contextual link from the ring-settings guide plus tile, mega-menu and PDP-breadcrumb support.
- Exact-match anchors are limited to 4, all from the Lab-Grown pillar to children that already own those keywords. The lab-vs-natural comparison receives 13 contextual links with 13 different anchors.

**RANKING EQUITY:**
- 28/28 Stage 3 ranking keywords checked
- protected URLs preserved (all 6 linked at their current URL)
- no ranking URL migrations proposed
- `cvd/hpht diamond tester` remains excluded and is never used as an anchor

**CANNIBALIZATION:**
- No new internal-linking conflict was identified.
- No anchor equals a keyword owned or held by another page.
- No source uses one anchor for two targets, and no Education page receives a commercial CTA.
- The 12 Stage 15 adjacent pairs (plus the D14-27 register pairs) carry guards on all 39 rows between them.

**ORPHAN/CONNECTIVITY:**
- True orphans: 0 confirmed (no crawl data; based on sitemap, nav and hub listings)
- Weakly connected: 13, of which the 9 Education-owned `/blog` articles are the main finding
- Nav-only: 20
- Launch requirements: 36 proposed or conditional pages. 21 are launch blockers without their REQUIRED incoming links; 15 are linked only if activated.

**UNRESOLVED:**
- Commercial Lab-Grown hub approval (D-05)
- Grading-report and karat options per product
- Natural, moissanite, gemstone, loose and wholesale offering
- Which conditional subcategories stay populated
- D-19 supplement (online-ring article / engagement-ring buying guide)
- D-15 spelling
- Blog editorial capacity
- Post-launch crawl for measured link counts
- Sign-off on the Education "Guide" label exception

Stage 17 not started.
