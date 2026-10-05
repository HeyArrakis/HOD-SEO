# Stage 17 — Keyword deep dives (keyword intelligence): summary

Date: 2026-09-24. Status: **COMPLETE** (local analysis). **No DataForSEO call or other API call was made. Spend: $0.00.** Cumulative project spend is unchanged at $0.33536.

Stage 17 records what each target page has to satisfy at keyword level. It is not a content brief, not a priority list and not a scoring model. No URL, keyword owner, cluster or link relationship was created or changed.

## 1. Scope

- **Unit of analysis:** the Stage 15 target page (27 targets), built from Stage 15 ownership, Stage 11 clusters, Stage 7 metrics, Stage 8 SERPs, Stage 10/13 existing content, Stage 15 ranking equity and Stage 16 linking context.
- **Keywords in scope:** all 1,936 Stage 15 keywords appear exactly once in `17_keyword_deep_dive.csv`, each keeping its Stage 15 disposition. Depth depends on disposition:

| Tier | Stage 15 dispositions | Keywords | Treatment |
|---|---|---|---|
| DEEP | MAP_EXISTING_URL, MAP_EXISTING_URL_KEEP, MAP_PROPOSED_URL, MAP_INTERIM_HOME | 659 | Full profile: role, modifiers, intent reading, coverage, gap |
| HELD | CONDITIONAL_NOT_MAPPED, DEFERRED_NOT_MAPPED | 267 | Recorded as `RELATED_BUT_DISTINCT`, grouped as `NO_TARGET::<topic>`, not treated as opportunities |
| REVIEW | REVIEW_REQUIRED | 156 | Kept in a review group (`NO_TARGET::REVIEW_REQUIRED`), not promoted |
| EXCLUDED_LIGHT | EXCLUDE_COMMERCIAL, EXCLUDE_OFF_SCOPE | 95 | Pass-through, `EXCLUDE` |
| EXCLUDED_NO_ANALYSIS | EXCLUDE_NOISE, EXCLUDE_COMPETITOR_BRAND | 759 | Pass-through, `EXCLUDE`, no analysis effort |

## 2. Method

1. **Primary terms.** Chosen per target by hand, not by volume. Criteria: relevance, Stage 8 intent, page type, Stage 15 ownership, ranking equity. 8 targets have a co-primary where one term cannot carry the page need. The reason for each choice is in `17_topic_intelligence.csv` (`primary_selection_rationale`).
2. **Keyword roles.** Assigned by rules applied in order: PRIMARY → CLOSE_VARIANT (listed variant or same canonical form) → POSSIBLE_OVERLAP (ambiguous "vs") → SUBTOPIC (interim home or non-core cluster) → QUESTION → COMPARISON → LONG_TAIL (5+ words) → ATTRIBUTE → SUPPORTING.
3. **Intent.** Stage 8 validated intent controls wherever it exists (47 of the 659 deep keywords). Otherwise the DataForSEO label is kept and marked unvalidated. Two conflict cases are flagged, not resolved:
   - a question-form query with a transactional/navigational label;
   - a DataForSEO TRANSACTIONAL label with no commercial modifier (e.g. `cvd diamond`, `diamond inclusions`, `gia lab diamonds`), which is read as UNCLEAR.

   36 deep keywords carry a conflict flag. No intent was ever upgraded to TRANSACTIONAL.
4. **Modifiers and commercial signal.** Detected with lexicons (19 modifier types). Commercial words are classified as TRANSACTIONAL (Stage 8), TRANSACTIONAL_MODIFIER, COMMERCIAL_RESEARCH_MODIFIER or INFORMATIONAL_WITH_COMMERCIAL_WORD. SERP evidence controls.
5. **Questions (AEO).** Two sources:
   - question-form owned keywords, collapsed by searcher need (the most specific matching concept) so near-duplicates become one question with its variants listed;
   - the 389 People Also Ask questions already in the raw Stage 8 SERP files (paid for in Stage 8, re-read locally), each routed by hand to its owner, or marked off-topic.
6. **Semantic concepts.** A curated concept lexicon per target. A concept is kept only if it matches an owned keyword, a routed PAA question or a Stage 8 related search for that target. 5 lexicon concepts had no evidence and were dropped.
7. **Existing content.** Assessed from Stage 1/10 title, H1 and topic strings, plus Stage 3/13/15 ranking and decisions. **No page body was audited** (no body extract exists and no live-site request was made). So no keyword is marked FULL coverage. A concept not visible in the title/H1/topic is marked UNKNOWN, not THIN.

## 3. Source files (read only)

- Stage 7: `07_hod_master_keyword_database.csv`, `07_hod_master_keyword_summary.md`
- Stage 8: `08_hod_serp_validation.csv`, `08_hod_serp_validation_summary.md`, and the raw `serp/raw/08_stage8_by_id/*.json` (PAA, related searches)
- Stage 9: `competitors/analysis/*` (context only; Stage 8 carries the SERP evidence used here)
- Stage 10: inventory, keyword coverage, equity, overlap, SERP alignment, business-area coverage
- Stage 11: registry, keyword map, relationships, summary
- Stages 12–16: all listed files, plus `README.md`, `CLAUDE.md`, `progress.md`, `decision-log.md`

**Upstream check:** a SHA-256 snapshot of all 203 pre-Stage-17 files is stored in `content-strategy/scripts/17_upstream_checksums.json`. QC confirms none of them changed.

## 4. Outputs

| File | Rows | Contents |
|---|---|---|
| `17_keyword_deep_dive.csv` | 1,936 | One row per Stage 15 keyword: role, intent reading and basis, SERP evidence, modifiers, coverage, gap, confidence |
| `17_topic_intelligence.csv` | 52 | 27 target rows, plus 24 held-topic rows and 1 review row (labelled `NO_TARGET::`; no page implied) |
| `17_semantic_concepts.csv` | 205 | Concepts per target, typed and evidenced |
| `17_question_map.csv` | 243 | 97 keyword-question groups and 146 routed PAA questions (17 marked `EXCLUDE_OFF_TOPIC`) |
| `17_keyword_relationships.csv` | 1,083 | Keyword→primary roles (632), Stage 11 cluster relationships (93), Stage 17 overlap flags (14), Stage 8 related searches (344) |
| `17_gap_register.csv` | 70 | Gap signals per target, with evidence and confidence (not briefs) |
| `scripts/build_17.py`, `scripts/qc_17.py` | — | Build and QC; `17_build_stats.json` holds the run statistics |

## 5. Counts

- **Keyword records analysed in depth:** 659, across 27 targets and 61 Stage 11 clusters. All 1,936 records are carried, spanning 92 cluster IDs: 89 registry clusters plus the NOISE, COMPETITOR_BRAND and UNCLUSTERED_REVIEW buckets.
- **Deep keyword roles:**

  | Role | Keywords |
  |---|---|
  | PRIMARY | 35 |
  | CLOSE_VARIANT | 112 |
  | QUESTION | 182 |
  | SUBTOPIC | 159 |
  | SUPPORTING | 62 |
  | ATTRIBUTE | 44 |
  | COMPARISON | 41 |
  | LONG_TAIL | 19 |
  | POSSIBLE_OVERLAP | 5 |

- **Questions:** 243 rows, 226 of them relevant.

  | Role | Questions |
  |---|---|
  | CORE_ANSWER | 41 |
  | SECTION_QUESTION | 98 |
  | FAQ_CANDIDATE | 84 |
  | CATEGORY_COPY_CANDIDATE | 3 |
  | EXCLUDE_OFF_TOPIC | 17 |

  - PAA: 389 PAA occurrences across the 100 Stage 8 SERPs (299 unique question texts). 146 unique questions are routed to a target. 172 occurrences were left unrouted because they came from held, excluded or noise SERPs. The 4 occurrences on the `cvd/hpht diamond tester` SERP were deliberately not used.
- **Semantic concepts:** 205.

  | Concept type | Count |
  |---|---|
  | PRIMARY_CONCEPT | 63 |
  | SUPPORTING_CONCEPT | 97 |
  | RELATED_ENTITY | 19 |
  | OPTIONAL_CONTEXT | 26 |

  Confidence: HIGH 64, MEDIUM 76, LOW 65.
- **Related searches not in the Stage 7 universe:** 324 rows (248 unique strings). These are raw material for Stage 18.

## 6. Ranking equity — all 28 Stage 3 ranking keywords

Every ranking URL is kept. Nothing here recommends a move.

| Ranking URL (position) | Keywords | Target | Stage 17 reading | Additional supporting opportunities |
|---|---|---|---|---|
| `/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams` | are cvd diamonds real (27); lab-grown diamond cvd vs hpht (32); cvd diamond vs lab grown (33); what is cvd diamond vs lab grown (35); what is cvd lab grown diamond (36); lab grown diamonds cvd vs hpht (41); which is better cvd or hpht diamond (43); lab grown hpht diamonds (44); cvd or hpht (44); lab grown diamond hpht (46); lab diamond cvd vs hpht (46); lab grown diamonds hpht (48); cvd vs hpht lab diamonds (48); hpht lab grown diamonds (49); hpht lab grown diamond (49); cvd vs hpht which is better (51); cvd vs hpht lab diamond (52); hpht vs cvd (54) | EDU-LG-03 (18 kw) | PRIMARY `hpht vs cvd`. Comparison variants are CLOSE_VARIANT. HPHT/CVD single-method variants are SUBTOPIC. All PARTIAL (title covers CVD/HPHT). | `cvd diamond` (3,600) and `cvd lab grown diamonds` (720) have no rank. Repeated PAA: CVD disadvantages, CVD-vs-HPHT price, "worth buying", Type IIa, HPHT treatment vs growth |
| same URL | **cvd/hpht diamond tester (68)** | none, excluded | EXCLUDE. Not used as evidence; its SERP's PAA not used. | n/a |
| `/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams` | which is better lab grown diamonds or natural diamonds (29); what's better lab grown or natural diamonds (36); which diamond is better lab grown or natural (40) | EDU-LG-02 | QUESTION / PARTIAL | Head `lab grown vs natural diamonds` (22,200) has no rank. Interim CL-012 worth-it/cons family (1,900 / 1,300 / 880) |
| `/blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide` | how to choose a lab grown diamond (35) | EDU-LG-10 | PRIMARY / PARTIAL | `should i buy a lab grown diamond engagement ring` (30 ×2). Boundary depends on unapproved D-19 |
| `/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams` | which one is better 14k or 18k gold (81); is 14k diamond good (84); is 18k gold or 14k gold better (95) | EDU-MET-01 | PRIMARY `is 18k gold or 14k gold better`; all PARTIAL | 10k subtopic (validated); PAA on daily wear and resale; karat-vs-carat clarification (serves `is 14k diamond good`) |
| `/engagement-rings/by-desgin/side-stone-rings` | side stones engagement rings (104) | COM-ER-SIDESTONE | PRIMARY / THIN (CATEGORY SERP, format aligned) | Definitional PAA as short category copy |
| `/shop/oval-floral-diamond-ring` | marquise oval diamond (90) | COM-PDP-OVAL-FLORAL | PRIMARY / PARTIAL (PRODUCT SERP, aligned) | None evidenced locally |

28/28 represented, with positions and URLs identical to `15_ranking_equity_protection.csv`.

## 7. Existing-content coverage (title/H1/topic level; bodies not audited)

| Target | Existing URL | Status | Covered at title level | Evident gaps |
|---|---|---|---|---|
| EDU-LG-01 | /blog/are-lab-grown-diamonds-real… | WEAK (0 rankings for a 14,800 head) | "real" | "fake" variants; COMPARISON-led SERP format |
| EDU-LG-02 | /blog/lab-grown-vs-natural… | PARTIAL (ranks 29–40) | vs / which / better | CL-012 worth-it, pros/cons, perception |
| EDU-LG-03 | /blog/cvd-vs-hpht… | PARTIAL (18 protected, 27–54) | CVD, HPHT | CVD single-method depth, Type IIa, method PAA |
| EDU-LG-10 | /blog/how-to-choose-a-lab-grown-diamond… | PARTIAL (35) | choose | Engagement-ring boundary (D-19) |
| EDU-4C-00 | /blog/the-4cs-of-lab-grown-diamonds… | WEAK (0 rankings) | 4Cs, lab-grown, clarity | General grading-scale framing (8,100 / 4,400 heads); colour–clarity combinations |
| EDU-SHP-00 | /blog/the-best-lab-grown-diamond-shapes… | WEAK (0 rankings) | shape, "which shape" | Radiant / asscher / emerald / princess; head SERP partly geometric |
| EDU-CERT-00 | /blog/igi-certification… (retarget) | WEAK (0 rankings) | IGI | GIA lab-grown (2,400 head), certification basics, report verification |
| EDU-CERT-01 | /education/…gia-vs-igi… | WEAK (0 rankings) | GIA, IGI, report | Other labs (AGS/EGL/GSI/GCAL); AEO |
| EDU-MET-01 | /blog/14k-vs-18k-gold… | WEAK (81–95) | 14k, 18k | 10k; durability and resale PAA; karat/carat |
| EDU-RJG-02 | /blog/how-to-find-your-ring-size… | WEAK (0 rankings) | ring size | Resizing (owned keywords are mostly resizing) |
| COM-ER-SIDESTONE | /engagement-rings/by-desgin/side-stone-rings | WEAK / THIN (104) | side stone | Thin category (template meta, about 4 products) |
| COM-PDP-OVAL-FLORAL | /shop/oval-floral-diamond-ring | WEAK (90) | marquise, oval | No clear gap |

The other 15 targets are FUTURE_PAGE (432 deep keywords, coverage MISSING). There are no STRONG_EXISTING_CONTENT targets: no HOD page ranks in the top 20 for any owned keyword.

## 8. Major findings

1. **The keyword universe is missing core head terms.** This is the most consequential finding. Stage 7 has no row for:
   - 4Cs: "4cs of diamonds", "diamond 4cs";
   - colour/clarity/carat/cut: "diamond color chart", "diamond clarity chart", "diamond carat", "diamond cut";
   - shapes: "diamond shapes";
   - metals: "14k vs 18k gold", "white gold vs platinum";
   - ring size: "ring size chart", "ring size guide";
   - settings: "engagement ring settings", "prong setting", "bezel setting";
   - lab-grown definition: "what are lab grown diamonds".

   Consequences:
   - For 9 targets (EDU-4C-00, 4C-05, 4C-06, 4C-07, SHP-00, MET-00, MET-01, RJG-01, RJG-02) the primary term is a stand-in and the main demand is unmeasured.
   - "Diamond color chart" appears as a Google related search on the Stage 8 clarity SERP, so the demand exists.
2. **"diamond shape" (60,500) is partly non-jewellery.** Its Stage 8 PAA are geometric ("Is a diamond a rhombus or a kite?"), and related searches include "diamond shape face" and "drawings". Realistic demand for EDU-SHP-00 is below the raw figure.
3. **CVD/HPHT (EDU-LG-03) has the strongest AEO evidence in the project:**
   - 18 validated SERPs: 17 with AI Overview, 18 with PAA;
   - the same PAA repeat across them (CVD disadvantages, price difference, "worth buying", tester behaviour);
   - HOD ranks 27–54 on comparison and HPHT variants but not at all for "cvd diamond" (3,600).
4. **The authenticity SERP ("are lab grown diamonds real", 14,800) is COMPARISON-led.** This confirms the Stage 14 MEDIUM risk against EDU-LG-02. EDU-LG-01 must handle the natural-vs-lab framing without taking over the comparison.
5. **Ambiguous "vs" in the 4Cs clusters.** "f vs diamond", "g vs diamond", "g-h vs diamond" and similar likely mean colour + VS clarity combinations (CL-048), not "versus". Flagged POSSIBLE_OVERLAP; Stage 15 ownership unchanged.
6. **Karat/carat confusion** at EDU-MET-01. Evidence: the ranking keyword "is 14k diamond good" and PAA "Are 14k diamonds real?" / "How much is a 14 carat diamond worth?".
7. **Question inflation is avoidable.** For example, 34 "is N carat diamond good/too big" keywords collapse into one size-perception question, and 26 tester variants collapse into one core question.
8. **DataForSEO TRANSACTIONAL labels on informational heads are unreliable.** 35 deep keywords (e.g. `cvd diamond`, `diamond inclusions`, `gia lab diamonds`, `diamond facet`) carry a TRANSACTIONAL label with no commercial modifier. They are read as UNCLEAR, not commercial.

## 9. High-confidence gaps (Stage 8 evidence or direct data facts)

- EDU-LG-03: method PAA not reflected (repeated across the 18 validated SERPs). CVD single-method depth is missing (no rank for 3,600 / 720).
- EDU-4C-02 (SI) and EDU-4C-03 (VVS/IF/FL): no content. Both have validated editorial SERPs with AI Overview + PAA + Shopping.
- EDU-RJG-01 (settings): no content. Validated editorial SERP with AI Overview + PAA.
- EDU-CERT-00: certification-basics questions are validated (PAA "Do lab-grown diamonds get a certificate?", "Does GIA still certify…"). The existing page is IGI-only.
- EDU-MET-01: validated PAA on durability and resale across all 4 SERPs. The 10k subtopic is not in the title.
- EDU-SHP-00: SERP-format gap (geometric intent dilution).
- Keyword-universe gaps (HIGH as data facts): 4Cs, colour, cut, carat, shapes, 14k-vs-18k, metals, settings and ring-size head terms are absent from Stage 7.

## 10. Low-confidence areas / needs validation

- **Primary term marked LOW:** EDU-LG-00 (synthetic diamonds), EDU-LG-07, EDU-LG-08, EDU-4C-00, EDU-4C-05, EDU-4C-07, EDU-RJG-02. The reason is no SERP validation and/or a missing head term.
- **No Stage 8 evidence at all** (serp_confidence INSUFFICIENT_EVIDENCE): EDU-LG-00, LG-05, LG-07, LG-08, NAT-00, 4C-00, 4C-07, RJG-02, GEN-01.
- **Validated but UNCLEAR:** "diamond clarity grading scale" (OTHER; reference-led) and "which diamond is better lab grown or natural".
- **Ambiguous terms:** "how are diamonds made" (natural vs lab); the colour-letter "vs" set; "diamond shape" (geometry); "diamond facet" / "milgrain ring" (TRANSACTIONAL labels).
- **Business dependencies without catalogue evidence:**
  - tungsten/titanium bands (EDU-MET-00);
  - treated stones (EDU-LG-08);
  - buy-back / trade-in (EDU-LG-05);
  - adding side stones / bespoke (COM-ER-SIDESTONE);
  - carbon-neutral claims (EDU-LG-07).
- **URL_PENDING targets (9)** and **interim homes (56 keywords)** stay conditional on Stage 14 decisions.
- **Existing-content body coverage is unknown** everywhere: 101 deep keywords are UNKNOWN. A free, read-only fetch of the H2s of the 12 existing URLs would firm this up. That is not done here (local-only rule).

## 11. Unresolved items (carried, not decided)

- Stage 16 sign-off: Education labels "Lab-Grown Diamond Guide" / "Natural Diamond Guide" (affects EDU-LG-00 and EDU-NAT-00 naming only; not ownership).
- D-19 commercial keyword/SERP supplement (unapproved). Affects the EDU-LG-10 vs EDU-RJG-04 engagement-ring buying-guide boundary and EXIST-BLOG-ER-ONLINE.
- D14-29 SERP batch (unapproved). Affects 8 INSUFFICIENT_EVIDENCE Stage 14 boundaries.
- 156 REVIEW_REQUIRED keywords remain in review.
- 267 held keywords wait for their conditional/deferred owners. The largest groups are Gemstones 136, CL-001 commercial lab-grown head 27, fancy colour 15 and natural value 14.

## 12. Is additional paid research necessary?

**Recommended, but not required to complete Stage 17. Not executed and not authorised.** The one call that would materially change Stage 17/18 confidence is a metrics lookup for the missing head terms (finding 1). The existing data cannot supply it: those keywords are not in any Stage 3–7 pull, and Stage 8 SERPs only prove they exist as related searches, with no volume.

- **Endpoint:** `POST /v3/dataforseo_labs/google/keyword_overview/live` (DataForSEO Labs organic metrics, the same endpoint used in Stage 7; not Google Ads, not clickstream).
- **Request:**
  - 1 task
  - `location_code` 2840 (United States, verified Stage 2)
  - `language_code` "en"
  - `include_serp_info` false
  - `include_clickstream_data` false
  - `keywords` (36): 4cs of diamonds; diamond 4cs; 4 cs of diamonds; diamond color chart; diamond color scale; diamond clarity chart; diamond carat; diamond carat size chart; carat weight; diamond cut; diamond cut chart; diamond shapes; diamond shapes chart; 14k vs 18k gold; 10k vs 14k gold; 14k gold; 18k gold; ring size chart; ring size guide; how to measure ring size; ring sizer; engagement ring settings; ring settings; prong setting; bezel setting; white gold vs platinum; platinum vs white gold; what are lab grown diamonds; lab grown diamonds meaning; vvs diamonds; vs1 diamond; vs2 diamond; si1 diamond; igi certification; gia certification; diamond certificate.
- **Expected results:** at most 36 rows. Keywords outside the Labs database return no row.
- **Maximum cost:** $0.012 per request + $0.00012 × 36 results = **$0.01632**. These are the account price-table rates verified on 2026-09-17 (Stage 7, `appendix/user_data`); re-verify with that free endpoint before running.
- **What it would not do:** validate SERP intent. It does not replace D14-29 or D-19. Ownership of any new head term would be a Stage 15-style decision, not a Stage 17 one.

## 13. QC

`python3 content-strategy/scripts/qc_17.py` → **28/28 PASS**. That covers:

- the 20 brief checks;
- REVIEW not promoted;
- controlled vocabularies;
- one topic row per target;
- no FULL coverage claimed without a body audit;
- no HIGH confidence on unvalidated keywords;
- Stage 16 parent consistency;
- gap evidence;
- qc_16 still passes except its point-in-time "no new files" chain. That check now also lists the Stage 17 deliverables, which is expected, the same way qc_15 flagged Stage 16.

Stage 18 has not been started.
