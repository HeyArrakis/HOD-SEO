# Stage 7 — Master Keyword Database Summary

Date: 2026-09-17
Output: `07_hod_master_keyword_database.csv` (1,936 rows)

## 1. Total unique keywords across Stages 3–6

- Stage 3 (current rankings): 28 rows
- Stage 4 (domain keyword universe): 1,000 rows
- Stage 5 (strategic seed universe, YES-eligible subset of Stage 4): 55 rows — **not counted separately**, since every Stage 5 seed is already one of the 1,000 Stage 4 rows (Stage 5 is a classification of Stage 4, not a new keyword pull; `set(Stage4) == set(Stage5)` verified programmatically).
- Stage 6 (keyword expansion): 1,000 rows
- Raw row total across the three keyword-bearing pulls (Stage 3 + Stage 4 + Stage 6): 2,028

## 2. Number retained after normalization/deduplication

**1,936 unique keywords.** Normalization = lowercase + trim + collapse repeated whitespace only (no stemming, no singular/plural merging, no semantic grouping — e.g. `lab grown diamonds` and any distinct `lab grown diamond` variant, had both existed, would have remained separate rows).

92 raw rows were duplicate mentions of a keyword already counted from another stage, removed by exact-normalized-string dedup:
- Stage 3 ∩ Stage 4 only (not also in Stage 6): 1
- Stage 3 ∩ Stage 6 only (not also in Stage 4): 2
- Stage 4 ∩ Stage 6 only (not also in Stage 3): 85
- Stage 3 ∩ Stage 4 ∩ Stage 6 (all three): 2 (`cvd diamond vs lab grown`, `lab grown diamonds cvd vs hpht`)

Verified via inclusion-exclusion: 28 + 1,000 + 1,000 − 3 − 4 − 87 + 2 = 1,936. No internal duplicates existed within any single source file before merging.

## 3. Number from each source stage (a keyword can count in more than one)

| Source | Keyword count |
|---|---|
| STAGE3_CURRENT_RANKING | 28 |
| STAGE4_DOMAIN_UNIVERSE | 1,000 |
| STAGE5_STRATEGIC_SEED (subset of Stage 4, `seed_eligibility=YES`) | 55 |
| STAGE6_EXPANSION | 1,000 |

## 4. Number appearing in multiple stages

**144 keywords** carry more than one `source_stages` tag (this includes all 55 Stage 5 seeds, since every one is also tagged STAGE4_DOMAIN_UNIVERSE by definition, plus the 3/4/87/2 raw overlaps above). A keyword's provenance is preserved as a semicolon-separated list in the `source_stages` field — nothing was collapsed to a single source.

## 5–9. Status distribution

Status is derived primarily from Stage 5's full-taxonomy `primary_relevance_class` where a keyword was classified there (all 1,000 Stage 4/5 keywords). For the 936 keywords Stage 5 never saw (28 Stage-3-only + ~908 Stage-6-only, after excluding the 87 that also appear in Stage 4), status falls back to Stage 6's lightweight noise/ambiguity flags, or — for the small number of Stage-3-only keywords — to the fact that they are an existing, real organic ranking keyword on HOD's own domain. See `notes` field on every row for the exact basis used.

| Status | Count | Basis |
|---|---|---|
| **INCLUDE** | 1,258 | Stage 5 relevance class A/B/C/E, OR Stage 6 noise=NO & ambiguity=NO (no Stage 5 record), OR Stage-3-only current ranking keyword |
| **NOISE** | 457 | Stage 5 class G (IRRELEVANT_NOISE), OR Stage 6 `possible_noise_flag=YES` (no Stage 5 record) |
| **AMBIGUOUS** | 178 | Stage 5 class F (AMBIGUOUS), OR Stage 6 `possible_ambiguity_flag=YES` (no Stage 5 record) |
| **COMPETITOR_BRAND** | 43 | Stage 5 class D (COMPETITOR_OR_BRAND) — all 43 were already classified in Stage 5; none fell to the Stage-6-only fallback |
| **REVIEW** | 0 | Not needed as a fallback bucket — every keyword resolved to one of the above via Stage 5 or Stage 6 evidence. (Note: Stage 5's own `seed_review_queue`/`REVIEW` seed-eligibility keywords are preserved separately in `stage5_seed_eligibility`, distinct from this top-level status field — they are status=INCLUDE, seed_eligibility=REVIEW.) |

No new relevance judgment was invented beyond: (a) reusing Stage 5's classification verbatim, (b) reusing Stage 6's own noise/ambiguity flags verbatim, and (c) the single documented policy call for Stage-3-only keywords (see `decision-log.md`).

## 10–11. Metric enrichment coverage

**1,929 of 1,936 keywords (99.6%) already carry a reused search-volume metric** from their own origin-stage DataForSEO pull (Stage 3's `ranked_keywords/live`, Stage 4's `keywords_for_site/live`, or Stage 6's `keyword_ideas/live` — all three already returned `search_volume`, `cpc`, `competition`, `keyword_difficulty`, and `main_intent`/`search_intent` fields at collection time). **No new paid DataForSEO call was made or needed to reach this coverage** — per CLAUDE.md rule "reuse previously collected datasets rather than rerunning calls" and Stage 7 instruction 8.9.

**7 keywords (0.4%) have no volume data from any source** — all Stage-6-only, all status=INCLUDE:
`calibrated lab grown diamonds`, `can i buy a tiffany ring without the diamond`, `color grade diamond`, `diamond cut grade`, `diamond vape`, `lab grown diamonds dfw`, `lab grown opal rough`.

These are marked `enriched=NO`, `metric_source=NONE_NO_VOLUME_DATA_IN_ANY_SOURCE_STAGE`, and all metric fields `NOT_AVAILABLE` — not invented. A same-database `keyword_overview/live` call would very likely return nothing new for these (DataForSEO's own docs: "if some keywords are omitted in the results, our database doesn't contain such keywords... you will not be charged"), since `keyword_ideas/live` already queries the same backend keyword database and found no volume. This is flagged as an **optional, separately cost-gated** action for the user — see the final report; it does not block Stage 7 completion.

## 12. Exact metric fields obtained (from reused Stage 3/4/6 data)

`search_volume`, `cpc`, `competition`, `keyword_difficulty`, `intent` (main_intent/search_intent), `monthly_search_data` (raw monthly trend series, 1,929 of 1,936 populated), `serp_summary` (SERP item types — only available where the origin pull requested `include_serp_info`: Stage 3 always did, Stage 4 always did, Stage 6 did not request it — see limitation below).

## 13. Missing metric fields

Reused metrics are themselves partially incomplete **within** their origin stage — this reflects genuine gaps in DataForSEO's underlying keyword database (low-volume/low-ad-demand terms often have no Google Ads CPC/competition data), not a Stage 7 processing gap:

- Has `search_volume` but no `cpc`: 691 keywords
- Has `search_volume` but no `competition`: 88 keywords
- Has `search_volume` but no `keyword_difficulty`: 317 keywords
- `serp_summary` = NOT_AVAILABLE: 1,200 keywords (all 1,000 Stage-6-only-sourced rows whose only source stage was Stage 6, since `keyword_ideas/live` was run with `include_serp_info=false` in Stage 6 — see Stage 6 decision log)

## 14. API limitations carried forward

- **No per-item seed attribution** for any Stage 6-sourced keyword (`stage6_source_seeds` = `NOT_AVAILABLE_FROM_API_RESPONSE` on every row) — `keyword_ideas/live` only returns `seed_keywords` at the task level, per Stage 6's own documented finding. Not reverse-engineered or guessed here.
- Stage 6 metrics reflect one combined 89-seed task's relevance-ranked top-1,000 of 139,845 available — not the full expansion universe (Stage 6 limitation, carried forward unchanged).
- Stage 4 metrics reflect the top-1,000-of-518,487 relevance-ranked sample for the domain (Stage 4 limitation, carried forward unchanged).

## 15. Duplicate-resolution decisions

All 92 duplicate mentions were resolved by keeping one master row per normalized keyword and merging every source stage's fields into that row (see `source_stages`, per-stage-prefixed columns). Where the same keyword had metrics available from more than one stage, the **consolidated** `search_volume`/`cpc`/`competition`/`keyword_difficulty`/`intent` fields use priority Stage 3 > Stage 4 > Stage 6 (per CLAUDE.md rule 4: current-ranking data is not overwritten by newer estimates) — the *stage-prefixed* columns (`stage3_search_volume`, `stage4_search_volume`, `stage6_search_volume`) preserve every stage's own value independently, so no source value was discarded.

## 16. Data-quality issues

- 7 keywords have zero volume data from any source (see §10–11).
- 1,200 rows lack `serp_summary` because their only or primary metric source (Stage 6) did not request SERP info.
- Stage 5's `REVIEW`-eligibility seeds (41 keywords, `stage5_seed_eligibility=REVIEW`) are preserved as-is in `stage5_seed_eligibility`; they are NOT the same thing as this stage's own top-level `status` field, which uses Stage 5's broader `primary_relevance_class` (not `seed_eligibility`) to avoid conflating "not selected as a Stage 6 seed" with "not relevant."

## 17–18. Cost

- **Stage 7 API cost: $0.00.** No new paid DataForSEO call was made — all metrics were reused from Stage 3/4/6's already-paid pulls, per project reuse rule.
- **Cumulative DataForSEO spend to date: $0.27536** ($0.01536 Stage 3 + $0.132 Stage 4 + $0.132 Stage 6; Stages 0/1/2/5 were $0.00), of $51.00 deposited (account balance confirmed $50.282136 as of this stage's pricing-verification lookup).
