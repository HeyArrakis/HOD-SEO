# Stage 8 — SERP Validation Preflight (NOT YET EXECUTED)

Date: 2026-09-17
Status: **PREFLIGHT ONLY — no paid call made. Awaiting explicit approval.**

This document covers steps 1–15 of the Stage 8 brief: keyword selection and endpoint/cost verification. No SERP data has been collected. Stage 8 is not marked complete.

---

## 1. Selection source and method

Selected programmatically from `dataforseo/processed/07_hod_master_keyword_database.csv` (1,936 unique keywords). Eligible pool = `status IN (INCLUDE, AMBIGUOUS)` = 1,436 keywords (1,258 INCLUDE + 178 AMBIGUOUS). NOISE (457) and COMPETITOR_BRAND (43) were excluded from the pool entirely — no competitor/brand term was selected, since none was judged necessary to understand a relevant SERP behavior.

Selection ran as nine ordered pools against a hard cap of 100, each pool skipping keywords already selected by an earlier pool (a keyword keeps every reason tag it earns). Pool order was chosen so the explicitly-called-out Stage 6 concepts (moissanite/diamond-tester queries) and the ambiguous-keyword sample could not get crowded out by the time the 100-cap was hit; Long-tail (Pool G) was designated to absorb any final truncation, since it's the most redundant with Informational/Commercial-research coverage.

## 2. Selection breakdown (100 keywords, one keyword can carry multiple reasons)

| Pool | Reason tag | Count | Rule |
|---|---|---|---|
| A | CURRENT_RANKING | 28 | **All** Stage 3 current-ranking keywords included, regardless of volume (all 28 were already status=INCLUDE) |
| I | NEW_STAGE6_CONCEPT | 8 | Moissanite / diamond-tester / authenticity queries newly surfaced in Stage 6 — validating, not assuming, per instruction |
| B | COMMERCIAL_CATEGORY | 27 | Up to 2 representative keywords per controlled business area (see §3) |
| C | INFORMATIONAL | 10 | Diverse informational-intent topics (4Cs, certification, lab-grown mechanics, moissanite definition, authenticity) spread across business areas |
| D | COMMERCIAL_RESEARCH | 8 | `intent=commercial` keywords not already selected, spread across business areas |
| E | TRANSACTIONAL | 8 | `intent=transactional` keywords not already selected, spread across business areas |
| H | AMBIGUOUS | 5 | Highest-volume `status=AMBIGUOUS` keywords — validating what Google actually resolves the query to mean |
| F | HIGH_VOLUME | 4 | Highest remaining search-volume keywords not yet captured by any other pool (deliberately capped low — not a top-100-by-volume list) |
| G | LONG_TAIL | 3 | Lowest-volume, ≥6-word queries not yet captured (this pool absorbed the final truncation at the 100 cap) |

**Total: 100 unique keywords.**

## 3. Commercial/product category coverage (Section 5B)

Up to 2 representative keywords were selected per controlled business area, preferring commercial/transactional intent and higher volume as a tie-break (never as the sole driver):

| Business area | Keywords selected | Note |
|---|---|---|
| 1. Engagement Rings | `mixed metal ring`, `rhodium plating ring` | |
| 2. Wedding Bands | `is tungsten good for wedding bands`, `is titanium good for wedding bands` | Only 2 candidates exist in the master DB for this area (confirmed thin coverage, carried forward from Stage 4/5/6) |
| 3. Earrings | `can you shower with real diamond earrings`, `can you turn diamond earring into ring` | Only 3 candidates exist; thinnest of all areas |
| 4. Necklaces & Pendants | `will a gold plated necklace tarnish`, `can you wear silver bracelet with gold necklace` | Only 2 candidates exist |
| 5. Bracelets | `diesel bracelet`, `how can you tell if a tiffany bracelet is real` | Only 2 candidates exist; `diesel bracelet` is a borderline/brand-adjacent term but is the only transactional-intent candidate in this area — included to see what the SERP actually shows, not as an endorsement of relevance |
| 6. Fine Jewellery | **NO_SUITABLE_MASTER_KEYWORD_FOR_SERP_VALIDATION** | Zero keywords with this business area exist anywhere in the 1,936-keyword master database. Not invented, per instruction. |
| 7. Bespoke / Custom Jewellery | **NO_SUITABLE_MASTER_KEYWORD_FOR_SERP_VALIDATION** | Same — zero candidates. Confirms the Stage 4/5/6 coverage gap persists all the way through Stage 7's consolidated database. |
| 8. Lab-Grown Diamonds | `lab grown diamonds`, `lab diamonds` | Largest single area (511 eligible candidates) — capped at 2 per the representation-over-volume principle |
| 9. Natural Diamonds | `natural diamonds`, `natural diamond wholesale` | |
| 10. Diamond Shapes | `asscher cut diamond`, `asscher diamond` | |
| 11. Diamond Cuts | `diamond cut grade` | Only 1 candidate exists in this area |
| 12. Diamond Quality / 4Cs | `si2 diamond clarity`, `si2 diamond` | |
| 13. Diamond Certification | `lab-grown diamond certification`, `gia vs igi lab diamond` | |
| 14. Diamond Buying / Education | `lab diamond tester`, `thermal tester diamond` | |
| 15. Jewellery Materials / Metals | `rhodium ring`, `is a 10k gold ring worth anything` | |
| 16. Gemstones | `moissanite`, `morganite rings` | |

**Confirmed absence, not invented:** Fine Jewellery and Bespoke/Custom Jewellery have zero suitable master-database keywords. This is the same gap Stages 4/5/6 already documented (their discovery methods don't surface HOD's thinnest catalog categories) — Stage 8 does not fabricate keywords to fill it; it is flagged here for whoever scopes future keyword-discovery work.

852 keywords across `UNCLASSIFIED_OR_UNKNOWN`/`18. Other / Unclear` exist in the eligible pool but were not the focus of category-representation picks — a sample of them entered via the Informational/Commercial-research/Transactional/High-volume/Long-tail pools instead (38 of the final 100 fall in this business-area bucket, reflecting how much of Stage 6's discovery volume was never mapped to a controlled business area — a known, already-disclosed Stage 5/6 limitation, not a Stage 8 defect).

## 4. New Stage 6 concepts included (Section 5I)

`moissanite`, `moissanite vs lab grown diamond which is better`, `does moissanite pass a diamond tester`, `can moissanite pass diamond tester`, `is moissanite better than diamond`, `natural moissanite`, `moissanite clarity chart`, `is a lab grown diamond the same as moissanite`

These are being **validated**, not assumed to be opportunities — Stage 8 will only show what Google currently displays for them (dominant page type, ranking domains, SERP features). No relevance or priority judgment is made here.

## 5. Full selection matrix

See [`08_hod_serp_validation_selection.csv`](08_hod_serp_validation_selection.csv) — 100 rows with `keyword, search_volume, intent, business_area, source_stages, current_HOD_rank, status, selection_reason`.

---

## 6. Endpoint verification (Section 8)

Checked live against current DataForSEO documentation (`docs_search`) and the account's own price table (`GET /v3/appendix/user_data`, fetched fresh this stage):

- **Task submission:** `POST /v3/serp/google/organic/task_post` — queue-based ("Standard"). Up to **100 tasks per POST call** (a POST with more is rejected with error 40006 for the excess). Our 100 keywords fit in **exactly one** task_post call.
- **Result retrieval:** `GET /v3/serp/google/organic/task_get/advanced/$id` — one call per task id, **$0.00** ("Your account will be charged only for posting a task. You can get the results of the task within the next 30 days for free."). Using the `advanced` result type (rather than `regular`) costs nothing extra and returns full `item_types` coverage: `organic`, `shopping`, `featured_snippet`, `people_also_ask`, `ai_overview`, `images`, `video`, `knowledge_graph`, `local_pack`, `map`, `related_searches`, and more — everything Section 12 asks Stage 8 to capture.
- **Live alternative** (`POST /v3/serp/google/organic/live/advanced` or `/live/regular`) was also checked: single synchronous call, no polling required, but **more expensive per task** (see pricing below) for no additional data richness over Standard+advanced-retrieval.

## 7. Exact current pricing (verified from account price table, not assumed)

| Item | Cost type | Cost (USD) |
|---|---|---|
| `task_post`, priority **normal** (default) | per task | **$0.0006** |
| `task_post`, priority high | per task | $0.0012 |
| `task_get` (regular / advanced / html), within 30 days | per task | **$0.00** |
| `live/regular`, `live/advanced`, `live/html` | per task | $0.002 |

These figures match the user-provided reference figures exactly (Standard Normal $0.0006, Standard High $0.0012, Live $0.002), now confirmed against the live account price table rather than assumed. Account balance at verification: **$50.282136** of $51.00 deposited.

**5x keyword multiplier check:** applies only if a keyword contains search-operator syntax (`site:`, `intitle:`, etc.). None of the 100 selected keywords contain any such syntax — confirmed by inspection. No multiplier applies.

## 8. Proposed configuration and cost calculation

| Parameter | Value |
|---|---|
| Endpoint | `POST /v3/serp/google/organic/task_post` (submit) + `GET /v3/serp/google/organic/task_get/advanced/$id` (retrieve, free) |
| Number of keywords | 100 |
| Number of tasks | 100 (one task = one keyword SERP) |
| Number of task_post calls | **1** (100 tasks fit in one POST call; the 100-task-per-call limit is met exactly, not exceeded) |
| location_code | 2840 (United States) |
| language_code | en (English) |
| depth | 10 (default — first-page only, no extra charge) |
| device | desktop (default) |
| priority | 1 / normal (default — cheapest) |
| Optional paid parameters enabled | **None** — `calculate_rectangles`, `load_async_ai_overview`, `people_also_ask_click_depth`, `priority=high` are all left off |

**Cost calculation:**
- 100 tasks × $0.0006/task (task_post, normal priority) = **$0.06 maximum**
- Result retrieval (100× `task_get/advanced`) = **$0.00** (free within 30 days)
- **Total maximum cost: $0.06**
- Expected cost: $0.06 exactly (task_post cost is fixed per task regardless of what the SERP returns — unlike the Stage 3/4/6 Labs endpoints, there is no per-result variable component here)

This is **one exact paid call configuration** (one `task_post` request containing all 100 tasks). The subsequent 100 `task_get` retrieval requests are free and not a separate cost decision.

## 9. Why this configuration is sufficient

- depth=10 covers the full first page, which is what Section 10 asks for (page-1 structure, not deep ranking data)
- desktop device matches the project's stated default and keeps the configuration consistent across all 100 keywords
- `task_get/advanced` (retrieved for free) provides the full SERP feature/item_type breakdown needed for Section 12's checklist (organic, shopping, featured snippets, PAA, AI Overview, images, video, knowledge panels, local results) without paying Live pricing or any optional per-feature surcharge
- Standard Normal priority is ~3.3x cheaper than Live for identical first-page data, satisfying the project's "use the cheapest suitable endpoint" rule and the instruction's explicit preference

## 10. One or multiple calls required?

**One paid call.** A single `task_post` request with an array of 100 task objects (keyword + location_code 2840 + language_code en + depth 10 + device desktop, default normal priority) satisfies the entire validation set. Results will then be pulled via 100 free `task_get/advanced/$id` requests once tasks complete (Standard/queued tasks typically finish within seconds to a couple of minutes for depth=10; execution will poll for readiness rather than assume immediate availability).

---

## STOP — awaiting your explicit approval

Configuration proposed for approval: **1 × `task_post` call, 100 tasks, location_code=2840, language_code=en, depth=10, device=desktop, priority=normal (default), no optional paid parameters — maximum cost $0.06, expected cost $0.06.**

No paid call has been made. Stage 8 is not complete. Please confirm before I execute.
