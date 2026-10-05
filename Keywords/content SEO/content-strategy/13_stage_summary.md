# Stage 13 Summary: Future Blog Strategy and Existing-Content Decisions

Date: 2026-09-24. Local project files only. **No DataForSEO call (paid or free), no live-site request, and no site, CMS, URL, redirect, canonical, robots or sitemap change.** Nothing was moved, deleted, merged or rewritten. Every action below is a recommendation.

Outputs (all in `content-strategy/`):

| File | Rows | Content |
|---|---|---|
| `13_existing_content_decisions.csv` | 16 | 10 blog articles, 1 education article, 2 hubs, the FAQ, and the 2 ranking commercial URLs |
| `13_ranking_equity_analysis.csv` | 28 | Every Stage 3 ranking keyword |
| `13_blog_education_framework.csv` | 25 | Topic types |
| `13_content_migration_risk.csv` | 16 | Risk and required conditions per URL |
| `13_blog_strategy.md` | — | Blog strategy |
| `13_stage_summary.md` | — | This file |
| `scripts/build_13_csvs.py`, `scripts/qc_13.py` | — | Builder and QC |

---

## 1. Executive summary

- **The Blog has no editorial content today.** All 10 blog articles are evergreen reference or buying-decision pieces. Under Stage 12's rule that each evergreen topic has one home, all 10 are **Education-owned**. The future Blog (craft, style, launches, stories) has to be built from scratch.
- **Ownership changes now; ranked URLs do not move yet.** The two articles holding real equity, *CVD vs HPHT* (19 keywords) and *Lab-Grown vs Natural* (3 keywords, HOD's second-best position), are **UPDATE_IN_PLACE** at their current `/blog` URLs. They are HIGH migration risk, the Education destination does not exist yet, and Stage 8/9 show competitors rank for these topics on `/blog/` paths. The path change therefore brings no demonstrated ranking benefit.
- **Five articles are cleared to move to Education.** Four have no ranking equity (are-lab-grown-real, 4Cs, shapes, ring size). The fifth, 14k vs 18k, has 3 rankings at positions 81–95. All five move only when the destination exists, with 1:1 301s.
- **Certification overlap: differentiate, don't merge.** The two certification SERPs share 0 top-10 URLs. The Education GIA-vs-IGI article keeps the comparison intent. The IGI blog article is **RETARGETED** to the non-comparison certification need and homed in Education.
- **Buying guides: DEFER.** The how-to-choose and buy-online guides possibly overlap, but the ring-buying side has no keyword or SERP evidence. If consolidation is chosen later, how-to-choose (it holds the ranking) is the presumed survivor.
- **No cannibalization is demonstrated anywhere.** No keyword has two HOD URLs ranking.
- **Spend:** $0.00 this stage. Cumulative $0.33536.

## 2. Existing content decisions

| Article | Current | Rankings (best) | Overlap | Action | Risk | Conf. |
|---|---|---|---|---|---|---|
| CVD vs HPHT | Blog | 19 (27) | POSSIBLE (OV-03) | **UPDATE_IN_PLACE**; Education-owned, URL kept | HIGH | MEDIUM |
| Lab-Grown vs Natural | Blog | 3 (29) | POSSIBLE (OV-02) | **UPDATE_IN_PLACE**; Education-owned, URL kept | HIGH | MEDIUM |
| 14K vs 18K Gold | Blog | 3 (81) | DISTINCT | **MOVE_TO_EDUCATION** (conditional) | MEDIUM | MEDIUM |
| How to Choose a Lab-Grown Diamond | Blog | 1 (35) | POSSIBLE (OV-06/07) | **DEFER** | MEDIUM | LOW |
| Are Lab-Grown Diamonds Real? | Blog | 0 | POSSIBLE (OV-02/03) | **MOVE_TO_EDUCATION** | LOW | MEDIUM |
| 4Cs of Lab-Grown Diamonds | Blog | 0 | POSSIBLE (sub-topic) | **MOVE_TO_EDUCATION** | LOW | MEDIUM |
| Lab-Grown Engagement Ring Online | Blog | 0 | POSSIBLE (OV-06/08) | **DEFER** | LOW | LOW |
| Best Lab-Grown Shapes for Engagement Rings | Blog | 0 | DISTINCT | **MOVE_TO_EDUCATION** | LOW | MEDIUM |
| Ring Size Guide | Blog | 0 | DISTINCT | **MOVE_TO_EDUCATION** | LOW | MEDIUM |
| IGI Certification for Lab-Grown | Blog | 0 | CLEAR (OV-01) | **RETARGET** (+ Education home) | LOW | MEDIUM |
| GIA vs IGI (Education) | Education | 0 | CLEAR (OV-01) | **UPDATE_IN_PLACE** | LOW | MEDIUM |

**Totals for the 11 articles:**

| Action | Count |
|---|---|
| KEEP_BLOG | 0 |
| MOVE_TO_EDUCATION | 5 |
| MERGE | 0 |
| UPDATE_IN_PLACE | 3 |
| RETARGET | 1 |
| DEFER | 2 |
| NO_ACTION | 0 |

**Supporting rows:**
- Blog hub: KEEP_BLOG. It keeps its URL and takes the new role.
- Education hub: NO_ACTION. Stage 14 decides its structure.
- FAQ: NO_ACTION. Its role was set in Stage 12 D-18.
- Ranking PDP: NO_ACTION.
- Side-stone subcategory: NO_ACTION. Any URL change is Stage 15's decision.

"Move" means a recommended future change during the rebuild, not something done now.

## 3. Ranking equity

All 28 Stage 3 ranking keywords are carried over in `13_ranking_equity_analysis.csv`, with their positions unchanged.

**Alignment** (judged on cluster, SERP intent and page type, not position):

| Alignment | Count | Keywords |
|---|---|---|
| ALIGNED | 20 | See file |
| PARTIALLY_ALIGNED | 7 | All on the CVD vs HPHT article: 5 single-method HPHT queries (CL-017) and 2 single-method CVD queries (CL-018) |
| MISALIGNED | 1 | *cvd/hpht diamond tester*: a TRANSACTIONAL tool-retail SERP, and HOD does not sell testers |

**Equity risk** (descriptive bands, not a score):

| Risk | Count | Definition |
|---|---|---|
| HIGH | 19 | Aligned or partial, at positions 27–50 |
| MEDIUM | 7 | Positions 51–100 |
| LOW | 2 | The tester query, and side-stone at 104 |

**Special-attention URLs:**

- **CVD vs HPHT.** 11 core comparison keywords are aligned (positions 32–54). Seven partial keywords sit in adjacent single-method clusters.
  - About 34 of this URL's ~36.5 Stage 3 ETV comes from two **HPHT** 8,100-volume variants at position 49. Its most valuable equity is therefore the adjacent "what is HPHT" need, not the comparison itself.
  - Stage 14 must weigh this before creating a separate HPHT page. A new HPHT page could **fragment** this equity rather than consolidate it.
- **Lab-Grown vs Natural.**
  - Two variants are aligned with COMPARISON SERPs.
  - The third variant is aligned on topic, but its SERP was typed OTHER.
  - This article is the foothold in CL-011, whose head term has 22,200 volume.
- **14k vs 18k.** 3 aligned keywords at 81–95. The positional equity is negligible.
- **How to Choose.** 1 aligned keyword at position 35. The cluster (CL-024) is tiny, with a maximum volume of 30.
- **Oval/Marquise PDP.** Aligned: a PRODUCT SERP served by a PDP. Out of scope for content migration.
- **Side-stone category.** Aligned: a CATEGORY SERP served by a category page. Low positional equity, but it is HOD's only commercial-category ranking. URL questions go to Stage 15.

**Caveat.** Every Stage 3 row is a single DataForSEO Labs snapshot with `is_new=True`, not a live rank. The project has no GSC, backlink or click data. Equity judgments are therefore partial, and every move condition requires that data first.

## 4. Blog strategy (see `13_blog_strategy.md`)

- **Purpose:** HOD's editorial and brand voice. It shows who makes the jewellery and how, covers what is changing, and carries readers to Education and categories.
- **Owns:** craft and making-of (Surat workshop), style and trends, gifts and occasions, collections and launches, brand stories, and dated industry notes. Bespoke client stories are a FUTURE POSSIBILITY.
- **Does not own:** any evergreen diamond, lab-grown, certification, 4Cs, shape, metal, sizing or buying-guide topic, and it never targets shopping queries.
- **Six proposed editorial categories.** A category goes live only once it holds real posts. Tag archives are not indexable.
- **Lifecycle:** refresh, keep as record, consolidate, promote to Education, or retire with a recorded redirect decision.
- **Freshness:** a recurring seasonal topic reuses one URL. No fixed publishing quota, because no capacity or demand data supports one.
- **Trust:** a named author on every post, first-hand photography and process detail, substantiated claims, and client consent.

## 5. Blog vs Education framework

`13_blog_education_framework.csv` classifies 25 topic types:

| Home | Topic types |
|---|---|
| Education | 15 (one of them, gemstones and alternatives, is conditional) |
| Blog | 8 |
| Commercial pages | 1 |
| FAQ | 1 |

**Four tests, applied in order:** shelf-life, question, ownership, brand.
- Education wins for repeatable searcher questions.
- Blog wins for dated or HOD-specific stories.

Existing ranking equity overrides simple classification: a topic can be Education-owned while its URL stays on `/blog`.

## 6. Overlap and cannibalization findings

The Stage 10 classifications are unchanged. Stage 13 reads them as follows:

| Pair | Stage 10/11 | Stage 13 reading |
|---|---|---|
| IGI blog ↔ GIA-vs-IGI education (OV-01) | CLEAR_OVERLAP | Confirmed topic overlap. Resolved by intent differentiation (§7). Not cannibalization, since neither ranks. |
| Are-real ↔ lab-vs-natural (OV-02) | POSSIBLE | Kept as two topics. CL-010 vs CL-011 is RELATED_BUT_DISTINCT (HIGH), and they share 1 top-10 URL. |
| Are-real ↔ CVD vs HPHT (OV-03) | POSSIBLE | Limited to *are cvd diamonds real* (30), which only the CVD article ranks for. No action. |
| How-to-choose ↔ online-ring (OV-06) | POSSIBLE | INSUFFICIENT_EVIDENCE to merge. DEFER. |
| How-to-choose / online-ring ↔ 4Cs (OV-07/08) | POSSIBLE | Shared sub-topic, different primary intent. The one measured SERP pair shares 0 URLs. Not a blocker. |
| Online-ring ↔ shapes / 14k / ring-size (OV-09) | DISTINCT | Unchanged. |
| FAQ ↔ articles (OV-10) | POSSIBLE | Format overlap. The FAQ gives a one-line answer plus a link (D-18). |
| Blog hub ↔ Education hub (OV-12) | POSSIBLE | Resolved by role separation. |
| CL-016 ↔ CL-017 / CL-018 (REL-001/002) | POSSIBLE_OVERLAP (HIGH confidence) | Handled by one article today. Whether HPHT or CVD gets its own page is a Stage 14 decision, with a fragmentation warning. |
| CL-030 ↔ CL-031 / CL-032, CL-033 ↔ CL-031 / CL-032 | POSSIBLE_OVERLAP (LOW) | Affects the IGI retarget choice. No SERP evidence. Deferred. |

**Cannibalization:** 0 cases demonstrated, because Stage 3 has no keyword with two HOD URLs ranking. The word is used nowhere in the outputs as a finding.

## 7. Certification analysis (OV-01)

1. **Why they overlap.** The two articles share the same subject, business area and informational intent. Both string-match the same 58 certification keywords. The Education title ("Certification Explained: GIA vs IGI") mixes two intents.
2. **Distinct search intent?** Yes, at SERP level:
   - *gia vs igi lab diamond* (140) is served by comparison guides (bluenile, stienhardt, plumdiamonds, whiteflash).
   - *lab-grown diamond certification* (390) is served by the labs themselves (igi.org, gia.edu) and general guides.
   - The two SERPs share **0 top-10 URLs**.
3. **Does SERP evidence support separation?** Yes, for comparison vs general certification. It does **not** yet show whether IGI-specific queries (CL-032, head 1,000) form a third intent, because none was SERP-validated.
4. **Primary evergreen resource.** The Education GIA-vs-IGI article becomes the primary home for the **comparison** (CL-030). It is already in the correct system. Action: UPDATE_IN_PLACE, narrowed to the comparison.
5. **The other article.** The IGI blog article is **RETARGETED** to the non-comparison certification need and homed in Education. The two pages cross-link.
6. **Is migration justified?** Yes, at low risk. Neither URL has ranking equity, and differentiation is supported by the 0-shared-URL SERP evidence. A **merge is not recommended**: the evidence points to two intents.
7. **Evidence still missing:**
   - SERPs for IGI-specific queries (to choose between CL-032 and CL-033)
   - A content audit of the two pages (how much text is actually duplicated)
   - GSC and backlink data
   - Whether HOD's stones are IGI- or GIA-graded, which is a business fact that affects emphasis

## 8. Buying-guide analysis

| Topic | Evidence | Status |
|---|---|---|
| Choosing a lab-grown **stone** (how-to-choose) | 1 ranking; EDITORIAL_GUIDE SERP; CL-024 has max volume 30 | Distinct buyer decision (probable). Presumed survivor. DEFER until the ring side is evidenced. |
| Buying an engagement **ring** online | 0 rankings; no validated SERP; the relevant keywords are missing from the master DB | **Needs more evidence** (D-19 commercial supplement). DEFER. |
| 4Cs | Reference, not a buying guide. The measured SERP pair with how-to-choose shares 0 URLs | **Genuinely distinct.** MOVE_TO_EDUCATION. |
| Shapes / 14k vs 18k / ring size as steps in the online guide | OV-09 DISTINCT | **Distinct.** The online guide should link to them, not repeat them. |
| "Is it worth it" (CL-012), best clarity (CL-045), carat suitability (CL-049) | No HOD content; no validated SERP | Education gaps (Stage 14). |

**Consolidation needed now:** none is proven. The only candidate is how-to-choose + online-ring, and it is deferred.

## 9. Lab-grown content analysis

| Cluster | HOD content today | Ranking equity | Home | Note |
|---|---|---|---|---|
| CL-001 general/head (135,000) | none | 0 | **Commercial** Lab-Grown hub (conditional, D-05) | The SERP is commercial, so this is not Education or Blog |
| CL-002 what are / CL-015 how made | none | 0 | Education | Gap |
| CL-010 are they real (14,800) | are-real blog | 0 | Education | MOVE_TO_EDUCATION |
| CL-011 lab vs natural (22,200) | lab-vs-natural blog | 3 (29–40) | Education (URL kept) | UPDATE_IN_PLACE |
| CL-016 CVD vs HPHT | CVD blog | 11 | Education (URL kept) | UPDATE_IN_PLACE |
| CL-017 HPHT (8,100) | CVD blog | 5 (44–49) | Education | **Defer to Stage 14:** separate page or keep in CVD article (fragmentation risk) |
| CL-018 CVD (3,600) | CVD blog | 2 (27, 36) | Education | Same as CL-017 |
| CL-022 testers | CVD blog (incidental) | 1 (68), MISALIGNED | Not targeted | HOD doesn't sell testers |
| CL-020/021 identification / pass a tester | lab-vs-natural blog (signal only) | 0 | Education | Gap |
| CL-030–034 certification | IGI blog + GIA-vs-IGI education | 0 | Education | §7 |
| CL-024 choosing lab-grown | how-to-choose, online-ring | 1 (35) | Education | DEFER |
| CL-023 lab-grown quality charts | 4Cs blog | 0 | Education | Stage 14 decides overview vs lab-grown scope |
| CL-008/009 pricing, value/resale | are-real (signal) | 0 | Education (principles); Blog (dated price commentary) | Gap |
| CL-013 ethics | none | 0 | Education (explainer); Blog (HOD sourcing stories) | Gap |
| CL-014 history/market trends | none | 0 | **Blog** (dated) | Low measured demand |

**Deferred to Stage 14:**
- The lab-grown topic-hub sub-structure
- Whether HPHT and CVD get their own pages
- The CL-010/CL-011 scope boundary
- 4Cs scope
- Certification retarget target
- The inventory of gap articles

## 10. Migration risk

`13_content_migration_risk.csv` covers all 16 rows.

| Risk | URLs | Decision |
|---|---|---|
| **HIGH** | CVD vs HPHT; Lab-Grown vs Natural | **DO_NOT_MOVE_NOW.** Revisit only when all conditions are met (below). |
| **MEDIUM** | 14k vs 18k (MOVE, conditional); How to Choose (DEFER) | 14k: proceed when conditions are met. How-to-choose: DEFER. |
| **LOW** | 4 unranked moves, IGI retarget, GIA-vs-IGI update, online-ring (DEFER), hubs, FAQ, PDP, side-stone | Proceed when conditions are met, or not applicable |

**Conditions for HIGH-risk moves.** All must hold:
1. The Education owner hub is live.
2. GSC and backlink data have been reviewed.
3. The move is a 1:1 301 to a page with the same intent. No merge into a broader page.
4. Coverage of every ranking keyword's intent is kept.
5. Links, sitemap and canonical are updated in the same release.
6. The move is batched with the rebuild.
7. Rankings are monitored for 8–12 weeks, with a rollback plan.
8. For CVD vs HPHT specifically: Stage 14 has settled the CL-017 and CL-018 page question.
9. For Lab-Grown vs Natural specifically: Stage 14 has settled the CL-010/CL-011 boundary.

The "-house-of-diams" slug suffix (a Stage 12 deferred question) is **not a sufficient reason on its own** to move a ranking URL. Slug clean-up for unranked URLs is low risk and goes to Stage 15.

## 11. Content gaps

- **Strategically valuable existing content:**
  - CVD vs HPHT and Lab-Grown vs Natural: aligned, in HIGH-evidence clusters, holding HOD's only real foothold.
  - Are-lab-grown-real: no equity, but it targets a 14,800 authenticity need.
- **Strong equity, weak architecture:** CVD vs HPHT. It holds the most equity, but it sits in the time-bound system under a brand-suffixed slug, and most of its value comes from the adjacent HPHT need.
- **Weak or unclear:**
  - The online-ring guide: unevidenced intent, and it overlaps other guides.
  - The IGI blog: duplicates the Education article's ground.
  - 14k vs 18k: negligible positions.
  - Content quality for all 11 articles is **unmeasured** (no word-count or quality audit).
- **Education gaps (Stage 14):**
  - What lab-grown diamonds are, and how they are made
  - Value and resale; ethics; identification and testing
  - Natural diamonds
  - Cut quality
  - Grade comparisons (clarity/colour)
  - Carat suitability
  - "Is it worth it"
  - Jewellery care
  - Gemstones and alternatives (conditional)
  - Wedding-band, earring and necklace guidance (keyword-data gap)
- **Blog gaps:**
  - Craftsmanship and making-of (largest, relative to the Surat positioning)
  - Collections and launches (T-Bar, Hip Hop)
  - Gifts and occasions
  - Brand stories
  - Bespoke stories (future possibility)

## 12. Deferred decisions

| Question | Where it is resolved |
|---|---|
| HPHT/CVD separate pages vs one article (with fragmentation warning) | Stage 14 |
| CL-010/CL-011 boundary; 4Cs scope; shapes scope; ring-size tool vs article | Stage 14 |
| IGI retarget target (CL-032 vs CL-033) | Stage 14 (needs IGI-query SERP evidence) |
| How-to-choose vs online-ring consolidation | After the D-19 commercial supplement, then Stage 14 |
| Exact URLs, slug clean-up, redirect targets | Stage 15 |
| Blog/Education/category link map | Stage 16 |
| Timing of the 14k move and the unranked moves | Rebuild release, after the destinations exist |
| Editorial capacity, author expertise, bespoke-story consent, business facts (natural, loose stones, gemstones) | User / business |
| GSC, backlink and content-quality audit before any 301 | User (no API spend needed if GSC is connected) |

## 13. Next stage

**Stage 14: Education strategy** (topic hubs, article inventory, URL depth under `/education`, author profiles), building on the ownership and deferrals above. **Not started, per instruction.**

Recommendations that were not executed:
- **Stage 12 D-19 (commercial keyword/SERP supplement).** Still recommended before Stage 15. It would also settle the DEFER on the online-ring guide. It needs its own endpoint check, cost estimate and approval.
- **GSC data.** Connecting Google Search Console data before Stage 15 would replace the Stage 3 snapshot as the equity basis for every migration condition. The desktop session has an SEO Gets/GSC connector available, but it was **not used**: this stage was restricted to local files.
