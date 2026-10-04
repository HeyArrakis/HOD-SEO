# Stage 18 — Semantic gap analysis: summary

Date: 2026-09-25. Status: **COMPLETE (local evidence).** **No DataForSEO call, paid or free, returned data. Spend: $0.00.** A free `appendix/user_data` price check was attempted and returned 40100 (not authorised), at no charge. Cumulative project spend is unchanged at $0.33536.

Stage 18 records which concepts, entities, questions and formats each Stage 15 target page has to account for. It is not a content brief, not a keyword-ownership change, not a page score and not a page-creation decision. Stage 15 ownership, Stage 16 links and Stage 17 intelligence were treated as fixed; `qc_18` confirms by sha256 that all 214 pre-Stage-18 files are unchanged.

## 1. Methodology

1. **Concept lexicon per target (curated, then evidence-gated).** For each of the 27 targets, I drafted the concepts a searcher would need, following the chain query → need → intent → SERP expectation → concepts → questions → entities → attributes → comparisons → trust → decision. Each concept has a pattern. It is written to the register only if the pattern matches real project evidence. 8 concepts matched nothing and were dropped; they are logged in `scripts/18_build_stats.json`.
2. **Evidence engine.** Each concept is counted against:
   - the target's own Stage 8 SERPs: AI Overview text, and organic titles and snippets (counted as SERPs matched out of SERPs available);
   - PAA questions that Stage 17 routed to the target;
   - related searches on the target's SERPs;
   - keywords Stage 15 assigns to the target;
   - Stage 17 concepts;
   - AI Overviews on the SERPs of Stage 16-linked targets (reported separately as weak adjacent context).

   **Evidence strength:**
   - STRONG = 2+ independent own SERPs, or 1 SERP plus PAA or related-search support, or 3+ PAA.
   - MODERATE = 1 SERP, 1 PAA, 2+ related searches or 3+ owned keywords.
   - WEAK = anything less.
3. **Severity is a rule, not a score:**

   | Concept role | STRONG / MODERATE evidence | WEAK evidence |
   |---|---|---|
   | CORE | CRITICAL | IMPORTANT |
   | SUPPORTING | STRONG → IMPORTANT; MODERATE → SUPPORTING | SUPPORTING or OPTIONAL |
   | OPTIONAL / AVOID | OPTIONAL_CONTEXT | OPTIONAL_CONTEXT |

   - Business facts that HOD must supply → BUSINESS_DEPENDENT.
   - Unmeasured head terms and pages with no SERP → INSUFFICIENT_EVIDENCE.
   - A concept owned by another page is capped at IMPORTANT, because it only needs a brief mention on this page.

   Pages are not compared or ranked against each other.
4. **Ownership.** Every concept that belongs to another page carries an anchor keyword. QC checks that Stage 15 maps that keyword to the stated owner, or, for conditional owners, to the stated Stage 14 topic. Shared concepts carry an `[xkey]`. QC confirms that no xkey is OWNED_HERE on two pages and that every OWNED_ELSEWHERE xkey has a home row at its owner.
5. **Existing content.** No page body was audited, and no live-site request was made. Coverage is judged on title and H1 only:
   - BODY_UNKNOWN: the concept is evident in the title/H1, but its depth in the body is unknown;
   - TITLE/H1_NOT_EVIDENT;
   - FUTURE_PAGE.

   CONFIRMED_MISSING is never used, because no file proves absence.
6. **AEO language.** Format signals (answer-first blocks, comparison tables, charts, step sequences) are recorded as "SERP evidence suggests…". None is claimed to guarantee AI Overview inclusion.

## 2. Evidence hierarchy used

Evidence was weighted in this order:

1. Stage 8 validated SERPs, including AI Overview text and organic snippets. This is 47 SERPs mapped to 20 targets. The `cvd/hpht diamond tester` SERP is excluded.
2. Stage 8 PAA (146 routed questions).
3. Stage 8 related searches (324 rows not in Stage 7).
4. Stage 17 questions, concepts and relationships.
5. Stage 11 relationships.
6. Stage 7 keywords.
7. Stage 10/13 existing-content data.
8. Stage 14 architecture.
9. Stage 16 linking context.

Volume was never used as semantic evidence.

## 3. Outputs

| File | Rows | Contents |
|---|---|---|
| `18_semantic_gap_register.csv` | 304 | Concept-level coverage requirements and gaps for all 27 targets |
| `18_entity_coverage.csv` | 304 | Entities per target: type, evidence, owner, required/supporting |
| `18_question_coverage.csv` | 268 | 146 routed PAA + 97 keyword-question groups (owner rows), plus 25 rows where a PAA appeared on a non-owner's SERP |
| `18_serp_semantic_patterns.csv` | 62 | 47 SERP rows, 6 aggregate rows (targets with 2+ SERPs, recurring items only) and 9 NO_STAGE8_SERP rows |
| `18_cross_page_semantic_ownership.csv` | 66 | Concepts a page must mention but does not own |
| `18_related_search_classification.csv` (supporting) | 262 | Related-search strings: 251 exact (248 case-insensitive) not in Stage 7, plus 11 already in Stage 7 |
| `scripts/build_18.py`, `qc_18.py`, `18_build_stats.json`, `18_upstream_checksums.json` | — | Build, QC, statistics, upstream snapshot |

## 4. Semantic gaps found (304)

| Severity | Rows |
|---|---|
| CRITICAL_COVERAGE | 88 (56 of them HIGH confidence) |
| IMPORTANT_COVERAGE | 63 |
| SUPPORTING_COVERAGE | 60 |
| OPTIONAL_CONTEXT | 48 (includes 4 AVOID rows) |
| BUSINESS_DEPENDENT | 21 |
| INSUFFICIENT_EVIDENCE | 24 |

- **Coverage status:** 162 FUTURE_PAGE, 115 TITLE/H1_NOT_EVIDENT, 27 BODY_UNKNOWN, 0 CONFIRMED_MISSING.
- **Ownership:** 238 OWNED_HERE, 47 OWNED_ELSEWHERE, 5 INTERIM_HOME_HERE, 7 CONDITIONAL_OWNER_NOT_BUILT, 7 COMMERCIAL_PAGE_OWNER.
- **Largest gap types:** ATTRIBUTE 73, SERP_FORMAT 41, CORE_CONCEPT 29, COMMERCIAL_CONTEXT 24, COMPARISON 21, QUESTION 21, DEFINITION 20.

### Validated known-gap areas (brief section 15)

| Area | Finding | Evidence |
|---|---|---|
| A. CVD/HPHT (EDU-LG-03) | 8 CRITICAL gaps. Confirmed: both processes, CVD in its own right, growth-shape/characteristic differences, "no visual difference / same 4Cs", which is better, a differences table, and the price difference. IMPORTANT: pros/cons, worth buying, treatment vs growth, Type IIa (owner EDU-GEN-01), colour tendencies, CVD full form. | 16–18 of 18 SERPs for the core concepts |
| B. 4Cs | Confirmed for clarity, SI, VVS/IF/FL, colour and cut. Clarity, colour and cut SERPs are chart- and scale-led, so a VISUAL_CHART is CRITICAL for clarity and colour. Carat (EDU-4C-07) has no SERP: its CRITICAL gaps (weight vs size; "is N carat big enough" as one section) rest on 33–37 owned keywords. | Stage 8 SERPs; owned keywords (carat) |
| C. Certification | EDU-CERT-00 CRITICAL: what a report is, whether lab-grown stones get one, which labs, what a report includes, how to verify. GIA-vs-IGI depth stays on EDU-CERT-01, whose CRITICAL gaps are grading approach, method disclosure, cost, choice and a comparison table. Other labs (GCAL, AGS, EGL, GSI) are SUPPORTING. | GCAL appears in the AI Overview |
| D. Metals | EDU-MET-01 CRITICAL: purity, daily-wear durability, appearance, price, which is better, a comparison table. IMPORTANT: 10k, resale/melt value, karat-vs-carat, skin sensitivity. White gold vs platinum is CRITICAL on EDU-MET-00, where platinum appears in 4 of 5 AI Overviews, but the head term is unmeasured. | Stage 8 SERPs |
| E. Ring guides | EDU-RJG-01 is fully evidenced: setting types, sparkle-vs-security trade-off, a visual chart. EDU-RJG-02 has no SERP, so resizing is CRITICAL (owned keywords) and measuring and the chart are IMPORTANT. Measuring rests on Stage 14 scope, not demand data. | Stage 8 (settings); keywords and Stage 14 (sizing) |
| F. Shapes | Confirmed: overview of 10 shapes, shape-vs-cut, engagement-ring choice. Geometric intent is recorded as AVOID. Per-shape depth stays inside the pillar (EDU-SHP-01 deferred). | AI Overview lists 10 shapes |
| G. Lab-grown | See the table below. | — |

| Lab-grown sub-topic | Owner | Finding |
|---|---|---|
| Definition, terminology | EDU-LG-00 | CRITICAL, but keyword-only evidence (no SERP) |
| Authenticity | EDU-LG-01 | CRITICAL, HIGH confidence |
| Process | EDU-LG-00 (interim home for EDU-LG-04) | — |
| Quality / appearance | EDU-LG-08 | — |
| Price / value | EDU-LG-05 | — |
| Ethics | EDU-LG-07 | — |
| Certification | EDU-CERT-00 | — |
| Choosing | EDU-LG-10 | — |

EDU-LG-02 has 6 CRITICAL gaps (similarities, origin, price, resale, comparison table, decision framing), all on 3–4 of 4 SERPs.

## 5. Entity gaps

304 entity rows; **54 are entity gaps** (REQUIRED or SUPPORTING, and FUTURE_PAGE or TITLE/H1_NOT_EVIDENT).

| Target | Entity gaps | Entities |
|---|---|---|
| EDU-SHP-00 | 10 | The 10 shapes named in the AI Overview; none visible in the title/H1 |
| EDU-MET-00 | 7 | Yellow gold, white gold, platinum, silver, tungsten, titanium, nickel |
| EDU-4C-01 | 6 | Clarity grade groups, inclusions |
| EDU-RJG-01 | 6 | Prong, bezel, pavé, halo, channel, tension |
| EDU-4C-06 | 4 | Cut scale, light performance, polish/symmetry, facets |

Entities whose depth belongs to another page are marked OWNED_ELSEWHERE and are not counted as gaps. Examples: CVD/HPHT outside EDU-LG-03, GIA/IGI outside EDU-CERT-00, moissanite (EDU-GEM-01, conditional).

## 6. Question gaps

- 268 rows. **186 are question gaps**: an owned question with a treatment other than NOT_NEEDED, and no evident coverage.
- Treatments across the 146 PAA owner rows:

  | Treatment | PAA rows |
  |---|---|
  | SUPPORTING_SECTION | 53 |
  | FAQ | 46 |
  | CORE_SECTION | 23 |
  | NOT_NEEDED | 18 (17 off-topic + 1 service question) |
  | INLINE_ANSWER | 3 |
  | CATEGORY_COPY | 3 |

- Six Stage 17 roles were adjusted, each with its reason in the notes. Example: "Can I add side stones…" → NOT_NEEDED, because it is a business-dependent service question.
- 25 cross rows cover PAA that surfaced on a non-owner's SERP. They are INLINE_ANSWER with a link, never a duplicate FAQ.

## 7. SERP semantic patterns

AI Overview structures recur consistently. SERP evidence suggests these page structures:

| SERP type | AI Overview structure | Pages |
|---|---|---|
| Comparison SERPs | similarities/differences, or per-option blocks | EDU-LG-02, LG-03, CERT-01, MET-01 |
| Grade SERPs | definition → pros/cons → buying tips | SI, VVS |
| Scale SERPs | graded list | clarity, cut |
| Type-list SERPs | list of types | settings, shapes, metals |
| Calculation steps | melt value | 10k gold |

AI Overviews often end with decision prompts: budget, carat size, shape, metal. These are recorded as decision attributes. Across EDU-LG-03's 18 SERPs, AI Overview appears on 17, PAA on 18 and video on 14. HOD content needs its own process visuals; no video claim is made.

## 8. Cross-page ownership (66 rows)

Semantic completeness never creates a second owner:

| Concept | Owner |
|---|---|
| CVD vs HPHT | EDU-LG-03 |
| Authenticity | EDU-LG-01 |
| Lab vs natural | EDU-LG-02 |
| Worth-it / pros-cons | EDU-LG-06, interim home EDU-LG-02 |
| Detection | EDU-LG-09 |
| Certification basics | EDU-CERT-00 |
| GIA vs IGI | EDU-CERT-01 |
| Hardness | EDU-GEN-01 |
| Karat/carat | EDU-MET-01 |
| VS grades | EDU-4C-04, interim home EDU-4C-01 |
| Report reading | EDU-CERT-02, interim home EDU-CERT-00 |
| Rhodium | EDU-MET-02, interim home EDU-MET-00 |

Each row states the treatment on the current page (a one-line answer or a short mention plus a link) and what to avoid.

## 9. High-confidence gaps (examples; 56 CRITICAL/HIGH in total)

- **EDU-LG-03:** single-method CVD section; growth-shape/characteristics; "which is better" answer-first; differences table; price by method.
- **EDU-LG-02:** similarities/differences structure; price and resale rows; decision framing by priority.
- **EDU-LG-01:** answer-first "same material, different origin" block. The comparison framing is borrowed from EDU-LG-02 as a brief mention only.
- **EDU-4C-01 / 4C-05 / 4C-06:** scale plus visual chart; eye-clean/best-value clarity; "is G–H good"; light performance.
- **EDU-4C-02 / 4C-03:** definition, pros/cons, buying tips; VVS1 vs VVS2; "is VVS worth it".
- **EDU-CERT-00 / CERT-01, EDU-MET-01, EDU-RJG-01, EDU-LG-09:** as described in §4.

## 10. Business-dependent gaps (21)

- HOD growth-method disclosure; treated-stone disclosure.
- Which labs grade HOD stones, and whether each product has its own report.
- Buy-back / trade-in / upgrade policy; resizing policy (FAQ/policy pages).
- Karat and metal options; whether tungsten/titanium are sold.
- Whether natural diamonds are offered; COM-LG-HUB status.
- Carbon-neutral claims.
- Adding side stones / enhancers / bespoke; side-stone category assortment depth.
- SI/VVS grade display in the catalogue; loose-stone offer; shape x jewellery shopping; PDP product facts.

## 11. Insufficient-evidence gaps (24)

- **14 head-term rows.** The core query for these pages has no Stage 7 row or Stage 8 SERP; no volume is assumed:
  - 4Cs, clarity chart / VS, SI, VVS;
  - colour chart/scale, cut, carat;
  - shapes, certification, white gold vs platinum, 14k vs 18k;
  - settings, ring size;
  - lab-grown definition.
- **9 targets with no SERP**, so page format is unvalidated: EDU-LG-00, LG-05, LG-07, LG-08, NAT-00, 4C-00, 4C-07, RJG-02, GEN-01.
- **1 boundary row:** the EDU-LG-10 engagement-ring decision depends on the unapproved D-19.

## 12. DataForSEO

**Calls made: none.** The free price endpoint (`GET /v3/appendix/user_data`) returned 40100 (not authorised); no data, no charge.

**Calls not made:**

1. **Recommended, NOT executed, awaiting approval.** A small SERP batch would give the 9 no-SERP targets and the head-term pages real structure evidence. That could move 24 INSUFFICIENT_EVIDENCE rows and change Stage 19 section structure.

   | Setting | Value |
   |---|---|
   | CALL | `POST /v3/serp/google/organic/task_post` (standard queue, normal priority), then free `task_get/advanced` |
   | PURPOSE | What page type, AI Overview structure, PAA and entities Google shows for the core query of each page that currently has no SERP evidence |
   | TASKS (17) | what are lab grown diamonds; do lab grown diamonds hold their value; are lab grown diamonds ethical; do lab grown diamonds get cloudy; how are diamonds formed; 4cs of diamonds; diamond color chart; diamond carat size chart; diamond cut; diamond shapes; diamond certificate; 14k vs 18k gold; white gold vs platinum; engagement ring settings; ring size chart; how to measure ring size; what are diamonds made of |
   | LOCATION / LANGUAGE | 2840 / en |
   | DEPTH / DEVICE | 10 / desktop |
   | CLICKSTREAM | false |
   | PRICE | $0.0006 per task (Stage 8 verified rate, 2026-09-17). **Could not be re-verified today** (40100); must be re-verified before running. |
   | MAX COST | 17 × $0.0006 = **$0.0102** |
   | WHY NECESSARY | Existing data has no SERP for these queries. Stage 17 related searches show only that some of them exist. SERP structure changes section, format and entity requirements; volume does not. |

2. **Not recommended for Stage 18:** the Stage 17 `keyword_overview/live` metrics call (36 terms, max $0.01632). Search volume would not change semantic coverage. It remains relevant only to a future Stage 15-style ownership review.

**Exact Stage 18 spend: $0.00.**

## 13. Unresolved items

- Stage 16 label sign-off ("Lab-Grown Diamond Guide" / "Natural Diamond Guide").
- D-19 (commercial supplement) and D14-29 (SERP batch) remain unapproved; the Stage 18 SERP proposal above overlaps part of D14-29's purpose.
- Body coverage of the 12 existing URLs is unknown. A free, read-only fetch of their headings would turn 115 TITLE/H1_NOT_EVIDENT rows into confirmed findings, but it needs explicit authorisation.
- Business-fact questions for HOD (§10).
- Pricing endpoint authorisation (40100).

## 14. Stage 19 implications

- Build briefs from CRITICAL + IMPORTANT rows (151). Use SUPPORTING rows where space allows. Hold BUSINESS_DEPENDENT rows until HOD answers, and INSUFFICIENT_EVIDENCE rows until the SERP batch runs or the risk is accepted.
- Use `recommended_treatment` for section type: CORE_SECTION, COMPARISON_TABLE, VISUAL_CHART, STEP_SEQUENCE, DEFINITION_BLOCK, FAQ, INLINE_ANSWER, CATEGORY_COPY. Use `18_cross_page_semantic_ownership.csv` for what each brief must only mention and link.
- Existing URLs (12) need a heading-level check before briefs are finalised, because Stage 18 cannot say what their bodies already cover.
- No brief should create a new page; conditional topics stay interim sections where Stage 15 put them.

## 15. QC

`python3 content-strategy/scripts/qc_18.py` → **29/29 PASS**: the 25 brief checks plus vocabulary, ID/stat consistency, "related searches carry no ownership" and qc_17 status.

`qc_17.py` now reports 26/28. Its point-in-time "no new files" checks list the Stage 18 deliverables, which is expected; the same pattern appeared at earlier stages.

Stage 19 has not been started.
