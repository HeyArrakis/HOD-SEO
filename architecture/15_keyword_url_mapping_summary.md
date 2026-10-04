# Stage 15 — Keyword → URL mapping: summary

Date: 2026-09-24. Status: **COMPLETE**. Local project files only. **No DataForSEO call, no other API call and no spend ($0.00).** Cumulative project spend is unchanged at $0.33536.

This is an inventory of where each keyword is owned. It is not a priority list and contains no scores. Proposed URLs are *expressions* built from Stage 12 D-12 principles; they are not implemented, and the path prefix depends on the platform (Stage 12 D-17).

| File | Contents |
|---|---|
| `architecture/15_keyword_url_map.csv` | 1936 rows, one per Stage 7 keyword |
| `architecture/15_target_page_registry.csv` | 27 target pages that own at least one keyword |
| `architecture/15_cluster_page_map.csv` | 89 rows, one per Stage 11 cluster |
| `architecture/15_cannibalization_check.csv` | 83 check rows (A–E + special checks) |
| `content-strategy/15_ranking_equity_protection.csv` | 28 rows, all Stage 3 ranking keywords |
| `architecture/15_keyword_mapping_decision_log.md` | Decisions D15-01 to D15-16 |
| `architecture/scripts/build_15.py`, `summary_15.py`, `qc_15.py` | Build, summary and QC |

## 1–10. Keyword dispositions

| # | Disposition | Keywords | Meaning |
|---|---|---|---|
| 1 | MAP_EXISTING_URL | 127 | Existing URL owns it now; a planned move/retarget happens only under Stage 13 conditions (1:1 301) |
| 2 | MAP_EXISTING_URL_KEEP | 73 | Existing URL owns it and stays where it is (DO_NOT_MOVE_NOW, update in place, migration deferred, or commercial URL kept) |
| 3 | MAP_PROPOSED_URL | 403 | Stage 14 PROPOSED / PROPOSED_PROVISIONAL resource that does not exist yet |
| 4 | MAP_INTERIM_HOME | 56 | Primary topic is CONDITIONAL; Stage 14 names an interim home |
| 5 | CONDITIONAL_NOT_MAPPED | 140 | Owner is a CONDITIONAL page (Education or commercial); no URL until the condition is met |
| 6 | DEFERRED_NOT_MAPPED | 127 | Owner is DEFERRED (Education, commercial, or Blog with no article planned) |
| 7 | EXCLUDE_COMMERCIAL | 59 | Commercial query with no HOD destination (not in catalogue / NOT_PROPOSED / non-indexable filter) |
| 8 | EXCLUDE_NOISE | 649 | Stage 7/11 noise |
| 9 | EXCLUDE_COMPETITOR_BRAND | 110 | Competitor or third-party brand |
| 10 | EXCLUDE_OFF_SCOPE | 36 | No jewelry need, or third-party lab navigation |
| 11 | REVIEW_REQUIRED | 156 | Ambiguous; needs evidence or a business answer |
| | **Total** | **1936** | Every Stage 7 keyword appears exactly once |

- Mapped to a URL owner (existing + existing-keep + proposed + interim): **659** keywords.
- Existing URLs (MAP_EXISTING_URL + MAP_EXISTING_URL_KEEP): **200**. Proposed URLs: **403**. Interim homes: **56**.
- Conditional + deferred: **267**. Exclusions (commercial + noise + competitor + off-scope): **854**. Review-required: **156** (154 inherited from Stage 11 UNCLUSTERED_REVIEW + 2 added here).
- Confidence of the 659 mapped keywords: HIGH 83, MEDIUM 192, LOW 384. LOW is mostly provisional topics, interim homes and unvalidated TRANSACTIONAL/NAVIGATIONAL labels inside informational owners. Only 100 of 1,936 keywords have a Stage 8 SERP.

## 11–12. Target pages

- **27 target pages** own keywords: **12 existing URLs** and **15 proposed pages**.
- Of the 15 proposed pages, 6 have a proposed URL expression and 9 are URL_PENDING.
- Of the 12 existing URLs, 6 stay where they are and 6 have a future Education destination that is used only when the Stage 13 migration conditions are met.
- Architecture nodes with no keyword ownership are not in the registry: the Education root (/education), the Ring & Jewellery Guides index (EDU-RJG-00), the commercial category hubs (Engagement Rings, Wedding Bands, Fine Jewellery and children, Bespoke). The commercial hubs have no keywords because the master database has almost no commercial category queries (Stage 12 evidence constraint; D-19 unapproved). This is a data gap, not a lack of demand.

## 13. Keywords per target page

| target_id | Page | Status | Current / proposed URL | Keywords | Clusters |
|---|---|---|---|---|---|
| COM-ER-SIDESTONE | Engagement rings: side-stone (style subcategory) | EXISTING_KEEP | `/engagement-rings/by-desgin/side-stone-rings` | 1 | CL-120 |
| COM-PDP-OVAL-FLORAL | Oval floral diamond ring (product page) | EXISTING_KEEP | `/shop/oval-floral-diamond-ring` | 1 | CL-063 |
| EDU-4C-00 | The 4Cs of diamond quality (4Cs hub pillar, incl. lab-grown grading) | EXISTING_MOVE_WHEN_CONDITIONS_MET | `/blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat-house-of-diams` | 42 | CL-023; CL-040; CL-048 |
| EDU-4C-01 | Diamond clarity guide | PROPOSED | `/education/diamond-4cs/diamond-clarity` | 35 | CL-040; CL-042; CL-044; CL-045; CL-046; CL-048 |
| EDU-4C-02 | SI clarity diamonds (SI1, SI2, SI3) | PROPOSED | `/education/diamond-4cs/si-clarity-diamonds` | 8 | CL-041 |
| EDU-4C-03 | VVS, IF & flawless clarity diamonds | PROPOSED | `/education/diamond-4cs/vvs-diamonds` | 10 | CL-023; CL-043; CL-044 |
| EDU-4C-05 | Diamond color guide (D to Z) | PROPOSED | `/education/diamond-4cs/diamond-color` | 28 | CL-047 |
| EDU-4C-06 | Diamond cut guide (cut grade, facets, light performance) | PROPOSED | `/education/diamond-4cs/diamond-cut` | 13 | CL-050; CL-088 |
| EDU-4C-07 | Diamond carat guide | PROPOSED_PROVISIONAL | `URL_PENDING` | 38 | CL-049; CL-125 |
| EDU-CERT-00 | Diamond certification explained (Certification hub pillar) | EXISTING_RETARGET_THEN_MOVE | `/blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of-diams` | 53 | CL-031; CL-032; CL-033; CL-034 |
| EDU-CERT-01 | GIA vs IGI (comparison) | EXISTING_KEEP | `/education/lab-grown-diamond-certification-explained-gia-vs-igi-house-of-diams` | 8 | CL-030 |
| EDU-GEN-01 | Diamond properties: composition, hardness & durability | PROPOSED_PROVISIONAL | `URL_PENDING` | 74 | CL-080; CL-081; CL-082; CL-083; CL-087 |
| EDU-LG-00 | Lab-grown diamonds explained (Lab-Grown Education hub pillar) | PROPOSED | `/education/lab-grown-diamonds` | 49 | CL-002; CL-003; CL-004; CL-014; CL-015 |
| EDU-LG-01 | Are lab-grown diamonds real? (authenticity) | EXISTING_MOVE_WHEN_CONDITIONS_MET | `/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide` | 17 | CL-010 |
| EDU-LG-02 | Lab-grown vs natural diamonds (comparison) | EXISTING_KEEP | `/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams` | 52 | CL-011; CL-012 |
| EDU-LG-03 | CVD vs HPHT (single home for CVD and HPHT) | EXISTING_KEEP | `/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams` | 31 | CL-015; CL-016; CL-017; CL-018 |
| EDU-LG-05 | Lab-grown diamond price, value & resale | PROPOSED_PROVISIONAL | `URL_PENDING` | 37 | CL-008; CL-009; CL-086 |
| EDU-LG-07 | Lab-grown diamond ethics & sustainability | PROPOSED_PROVISIONAL | `URL_PENDING` | 16 | CL-013 |
| EDU-LG-08 | Lab-grown diamond appearance & durability | PROPOSED_PROVISIONAL | `URL_PENDING` | 18 | CL-019; CL-089 |
| EDU-LG-09 | Detecting lab-grown diamonds (testers & identification) | PROPOSED_PROVISIONAL | `URL_PENDING` | 45 | CL-020; CL-021; CL-022 |
| EDU-LG-10 | How to choose a lab-grown diamond (buying guide) | EXISTING_KEEP_MIGRATION_DEFERRED | `/blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide` | 3 | CL-024 |
| EDU-MET-00 | Jewelry metals guide (Metals hub pillar) | PROPOSED_PROVISIONAL | `URL_PENDING` | 19 | CL-111; CL-112; CL-113 |
| EDU-MET-01 | 14k vs 18k gold (and 10k) | EXISTING_MOVE_WHEN_CONDITIONS_MET | `/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams` | 4 | CL-110 |
| EDU-NAT-00 | Natural diamonds: formation & origin (Natural Education hub pillar) | PROPOSED_PROVISIONAL | `URL_PENDING` | 31 | CL-070; CL-071; CL-074; CL-075 |
| EDU-RJG-01 | Ring settings guide | PROPOSED | `URL_PENDING` | 11 | CL-121; CL-125 |
| EDU-RJG-02 | Ring size guide (tool embedded by default) | EXISTING_MOVE_WHEN_CONDITIONS_MET | `/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams` | 6 | CL-124 |
| EDU-SHP-00 | Diamond shapes guide (Shapes hub pillar, incl. engagement-ring shape choice) | EXISTING_MOVE_WHEN_CONDITIONS_MET | `/blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of-diams` | 9 | CL-060; CL-061; CL-062; CL-064 |

## 14. Highest-volume keyword per target page

Listed by the single highest-volume mapped keyword. This describes where large queries sit; it is not a ranking of page importance. Several are unvalidated or LOW-confidence (see the map).

| target_id | Highest-volume mapped keyword | SERP evidence on this target |
|---|---|---|
| EDU-SHP-00 | diamond shape (60500) | 1 validated: EDITORIAL_GUIDE:1 |
| EDU-LG-02 | lab grown vs natural diamonds (22200) | 4 validated: COMPARISON:3; OTHER:1 |
| EDU-4C-03 | v v s diamond (18100) | 1 validated: EDITORIAL_GUIDE:1 |
| EDU-LG-01 | are lab grown diamonds real (14800) | 1 validated: COMPARISON:1 |
| EDU-NAT-00 | how are diamonds created (12100) | No validated keyword |
| EDU-4C-01 | diamond clarity grading scale (12100) | 1 validated: OTHER:1 |
| EDU-LG-03 | hpht lab grown diamond (8100) | 18 validated: EDITORIAL_GUIDE:15; COMPARISON:1; OTHER:1; MIXED:1 |
| EDU-4C-00 | grading system for diamonds (8100) | No validated keyword |
| EDU-4C-05 | colorless diamond (3600) | 1 validated: EDITORIAL_GUIDE:1 |
| EDU-GEN-01 | what are diamonds made of (3600) | No validated keyword |
| EDU-LG-00 | synthetic diamonds (2900) | No validated keyword |
| EDU-LG-05 | are lab grown diamonds cheaper (2400) | No validated keyword |

## 15. Existing ranking URLs protected

All 28 Stage 3 ranking keywords are accounted for, on **6 ranking URLs**. **Every one of the 6 URLs is preserved.** No ranking keyword is reassigned to a new page.

| Ranking URL | Ranking kw | Action | Migration status |
|---|---|---|---|
| `/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams` | 3 | KEEP_EXISTING_URL ×3 | MOVE_WHEN_CONDITIONS_MET |
| `/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams` | 19 | KEEP_EXISTING_URL ×18; KEEP_EXISTING_URL_NOT_TARGETED ×1 | STAY_AT_CURRENT_URL_EDUCATION_OWNED |
| `/blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide` | 1 | KEEP_EXISTING_URL ×1 | DEFERRED |
| `/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams` | 3 | KEEP_EXISTING_URL ×3 | STAY_AT_CURRENT_URL_EDUCATION_OWNED |
| `/engagement-rings/by-desgin/side-stone-rings` | 1 | KEEP_EXISTING_URL ×1 | NO_MIGRATION_RECOMMENDED (commercial URL; Stage 13 NO_ACTION) |
| `/shop/oval-floral-diamond-ring` | 1 | KEEP_EXISTING_URL ×1 | NO_MIGRATION_RECOMMENDED (commercial URL; Stage 13 NO_ACTION) |

- The one keyword that is not targeted is `cvd/hpht diamond tester` (pos 68): its SERP is CATEGORY (tester shopping) and Stage 13 classed it MISALIGNED. The URL is untouched and keeps whatever ranking it has; no page targets the keyword (EXCLUDE_COMMERCIAL).

## 16. Cannibalization warnings

| Check | Result |
|---|---|
| A. Many keywords → one URL | 27 targets listed (expected) |
| B. Same keyword → multiple URLs | PASS: 0. Near-duplicate variants split across targets: 0. Variant status inconsistencies (unmapped, inherited): 1 |
| C. Same cluster → multiple targets | 6 clusters: CL-015, CL-023, CL-040, CL-044, CL-048*, CL-125*. * = a target outside the cluster's Stage 14 PRIMARY/SECONDARY rows, used by a documented keyword-level intent rule (D15-09, D15-10) |
| D. Existing ranking URL vs proposed URL | 27 of 28 ranking keywords map to their current ranking URL. 1 flagged: cvd/hpht diamond tester (not targeted; URL preserved) |
| E. Owners with adjacent intent | 12 pairs flagged: 1 HIGH, 7 MEDIUM, 3 LOW, 1 INSUFFICIENT_EVIDENCE |
| Special checks (CVD, HPHT, lab-vs-natural, are-real, 4Cs, clarity, shapes, IGI, commercial SERPs) | 8/8 PASS |

Pairs flagged under E:

- **MEDIUM** EDU-LG-01 ↔ EDU-LG-02: Authenticity vs comparison: REL-020 max 2 shared URLs, both SERPs COMPARISON-dominant (D14-07). Enforce the boundary in content.
- **MEDIUM** EDU-LG-02 ↔ EDU-LG-05: Worth-it pros/cons (interim on LG-02) vs price/value/resale: money-worry overlap (D14-10; D14-27).
- **HIGH** EDU-LG-00 ↔ EDU-LG-03: CL-015 process queries are split between the pillar (general) and CVD vs HPHT (methods). If EDU-LG-04 is ever created, it must not target CVD/HPHT method queries (D14-08).
- **MEDIUM** EDU-4C-00 ↔ EDU-4C-01: Lab-grown clarity-chart queries (CL-023) sit on the 4Cs pillar while general clarity-scale queries sit on the clarity guide. Separation is INSUFFICIENT_EVIDENCE (D14-15; D14-29 #3).
- **MEDIUM** EDU-CERT-00 ↔ EDU-CERT-01: General certification vs GIA-vs-IGI: 0 shared URLs (D14-18). Both changes must ship together (Stage 13) or OV-01 persists.
- **MEDIUM** EDU-4C-06 ↔ EDU-SHP-00: Cut grade vs shape: 'cut' is ambiguous (grade vs shape). Cut-grade queries → EDU-4C-06; shape queries → EDU-SHP-00 (D14-02 SPLIT).
- **MEDIUM** EDU-LG-08 ↔ EDU-LG-01: 'do lab-grown diamonds look real' is appearance (EDU-LG-08), not authenticity (D14-07).
- **LOW** EDU-LG-09 ↔ EDU-LG-01: 'do lab grown diamonds test real' wording mixes detection and authenticity; detection owns tester questions (D14-13).
- **MEDIUM** EDU-LG-00 ↔ CL-001 commercial Lab-Grown hub (conditional): Pillar must not target the head terms; REL-004 DISTINCT_INTENT (D14-05).
- **INSUFFICIENT_EVIDENCE** EDU-LG-10 ↔ EDU-RJG-04 (deferred): 'should i buy a lab grown diamond engagement ring' sits on the lab-grown buying guide; boundary with the deferred engagement-ring guide is unresolved (OV-06; D-19).
- **LOW** EDU-4C-02 ↔ EDU-4C-01: SI SERP shares 0 URLs with the clarity scale (D14-14).
- **LOW** EDU-4C-03 ↔ EDU-4C-01: VVS SERP shares 1 URL with the clarity scale (D14-14).

No actual cannibalization is demonstrated: no keyword has two HOD URLs ranking (Stage 3/10/11). The warnings above are boundaries to enforce in content (Stage 19) and linking (Stage 16).

## 17. Unresolved URL decisions

13 registry targets have a URL_PENDING element:

- **EDU-LG-05** (Lab-grown diamond price, value & resale): Provisional topic (LOW evidence). Candidate slug: /education/lab-grown-diamonds/lab-grown-diamond-value.
- **EDU-LG-07** (Lab-grown diamond ethics & sustainability): Provisional topic. Candidate slug: /education/lab-grown-diamonds/are-lab-grown-diamonds-ethical.
- **EDU-LG-08** (Lab-grown diamond appearance & durability): Provisional topic. Candidate slug: /education/lab-grown-diamonds/lab-grown-diamond-appearance.
- **EDU-LG-09** (Detecting lab-grown diamonds (testers & identification)): Provisional topic. Candidate slug: /education/lab-grown-diamonds/do-lab-grown-diamonds-pass-a-diamond-tester.
- **EDU-LG-10** (How to choose a lab-grown diamond (buying guide)): Topic PROPOSED in Stage 14; the existing article ranks (pos 35). Migration DEFERRED by Stage 13 pending D-19 (boundary with EDU-RJG-04).
- **EDU-NAT-00** (Natural diamonds: formation & origin (Natural Education hub pillar)): Provisional hub (LOW evidence). Candidate slug: /education/natural-diamonds. Must not target natural commercial head terms (CL-070/071).
- **EDU-4C-07** (Diamond carat guide): Provisional (LOW evidence; page type untested, D14-29 #12). Candidate slug: /education/diamond-4cs/diamond-carat.
- **EDU-MET-00** (Jewelry metals guide (Metals hub pillar)): Provisional hub. Candidate slug: /education/jewelry-metals (spelling per D-15). Interim home for rhodium (CL-111). Includes 6 interim-home keyword(s).
- **EDU-MET-01** (14k vs 18k gold (and 10k)): Moves only once the Metals section exists (Stage 13). Future slug pending because the Metals hub slug is provisional. Candidate: /education/{metals-hub}/14k-vs-18k-gold.
- **EDU-RJG-01** (Ring settings guide): Topic PROPOSED; slug pending because the hub label/spelling is open (Stage 12 D-15). Candidate: /education/{ring-guides-hub}/ring-settings.
- **EDU-RJG-02** (Ring size guide (tool embedded by default)): Future slug pending (hub label, D-15). Candidate: /education/{ring-guides-hub}/ring-size-guide. Tool (EDU-RJG-05) is not a separate target.
- **EDU-GEN-01** (Diamond properties: composition, hardness & durability): Provisional root-level article; none of its clusters is SERP-validated. Candidate slug: /education/diamond-properties.
- **COM-ER-SIDESTONE** (Engagement rings: side-stone (style subcategory)): Only style subcategory that passes the D-07 gate. Stage 12 D-03 removes the grouping segment in the future hierarchy; that path change is implementation (1:1 301), not recommended as a stand-alone change here.

Other open questions (details in the decision log):

- Platform (Stage 12 D-17): every proposed URL expression assumes a custom/headless path structure. A native Shopify build would express these as `/blogs/<blog>/…` or `/pages/…`; the logical owner does not change.
- "Jewellery" vs "jewelry" (Stage 12 D-15): blocks the Ring & Jewellery Guides and Metals hub slugs.
- Existing slugs with brand suffixes or misspellings (GIA-vs-IGI education article; `/by-desgin/` side-stone subcategory): kept. Any change is an implementation migration with 1:1 301s; Stage 15 does not recommend a stand-alone change.
- 156 REVIEW_REQUIRED keywords, led by 'diamond stone' (18,100; dual meaning per Stage 8).
- Commercial owners that are CONDITIONAL or DEFERRED in Stage 12 (Lab-Grown commercial hub, Earrings > Studs, Natural hub, loose/carat pages, wholesale, Fine Jewellery > Rings). Their keywords are held, not mapped.

## Paid research

None was run. The Stage 14 D14-29 SERP batch (16 tasks, max $0.0096) and the Stage 12 D-19 commercial supplement remain NOT approved. Stage 15 did not need them to produce a complete mapping: every keyword they would affect is already held as CONDITIONAL, DEFERRED, INTERIM or LOW confidence. What they would change is listed in decision D15-15.

## Next stage

Stage 16 (internal linking) is **not started**, per instruction.
