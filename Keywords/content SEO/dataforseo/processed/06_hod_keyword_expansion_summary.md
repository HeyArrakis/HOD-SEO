# House of Diams — Stage 6: Controlled Keyword Expansion Summary

Date: 2026-09-17

**Paid DataForSEO API calls this stage: 1. Actual cost: $0.132.**

---

## 1. Seed registry size

89 unique combined seeds. Registry: [`06_hod_seed_registry.csv`](06_hod_seed_registry.csv).

## 2. Stage 5 seed count

55 (all `seed_eligibility = YES` rows from [`05_hod_strategic_seed_universe.csv`](05_hod_strategic_seed_universe.csv); the REVIEW queue and NO/noise rows were not used).

## 3. Catalog-derived seed count

34, built directly from actual HOD site inventory evidence (live category pages and product-slug patterns documented in [`site/01_site_inventory.csv`](../../site/01_site_inventory.csv)) — every catalog seed's `catalog_evidence` field in the registry cites the specific PDPs or category page it's based on. Covers all 7 required commercial areas: Engagement Rings (9), Wedding Bands (4), Earrings (5), Necklaces & Pendants (4), Bracelets (4), Fine Jewellery (3), Bespoke/Custom Jewellery (5, one seed — "bespoke engagement rings" — conceptually spans both Engagement Rings and Bespoke). Deliberately excluded "men's wedding bands" (no men's products found in the 169-PDP catalog audit) and "wedding ring styles" (no direct catalog support).

## 4. Combined seed count

89 unique (55 + 34, **0 exact-string overlaps** between the two sources, verified programmatically).

## 5. API success/failure

**Success.** `status_code 20000 / "Ok."`, `tasks_error: 0`.

## 6. Result count

1,000 keyword ideas returned (`items_count`), out of `total_count = 139,845` relevant keywords in DataForSEO's database for this combined 89-seed set — this pull captured the top 0.7% by the endpoint's default relevance sort.

## 7. Actual API cost

**$0.132** (from the API response's `cost` field) — this equals the pre-approved maximum exactly, because the full 1,000-item `limit` was returned.

## 8. Maximum approved cost

$0.132 (shown and approved in the pre-flight cost gate before execution).

## 9. Exact endpoint used

`POST /v3/dataforseo_labs/google/keyword_ideas/live` — exactly one task, exactly one paid call this stage. No other paid endpoint was called.

## 10. US location / English verification

`location_code: 2840`, `language_code: "en"` — both confirmed in the API response's `data` object, matching the values verified in Stage 2 (not re-guessed).

## 11. Search-volume distribution

| Range | Count |
|---|---:|
| 0–9 | 7 |
| 10–99 | 330 |
| 100–999 | 452 |
| 1,000–9,999 | 190 |
| 10,000–99,999 | 19 |
| 100,000–999,999 | 2 (`moissanite` 201,000; `helzberg diamonds` 135,000) |

Median volume: 260. Long-tail/low-volume-heavy, similar in shape to Stage 4's distribution, though with far less noise (see §19).

## 12. Intent distribution (DataForSEO's own `search_intent_info.main_intent`, not re-derived)

| Intent | Count |
|---|---:|
| informational | 545 |
| transactional | 331 |
| commercial | 102 |
| navigational | 22 |

This is preserved as DataForSEO's own field, per project rule not to treat it as the only signal — a separate analyst read (business-area tagging) is provided alongside it, not as a replacement.

## 13. Business-area distribution (best-effort tagging, see limitations §21)

| Business area | Count |
|---|---:|
| UNCLASSIFIED | 474 |
| 8. Lab-Grown Diamonds | 431 |
| 16. Gemstones | 44 |
| 9. Natural Diamonds | 14 |
| 1. Engagement Rings | 11 |
| 12. Diamond Quality / 4Cs | 7 |
| 14. Diamond Buying / Education | 5 |
| 10. Diamond Shapes | 4 |
| 5. Bracelets | 2 |
| 2. Wedding Bands | 2 |
| 4. Necklaces & Pendants | 2 |
| 15. Jewellery Materials / Metals | 1 |
| 3. Earrings | 1 |
| 11. Diamond Cuts | 1 |
| 13. Diamond Certification | 1 |
| **6. Fine Jewellery** | **0** |
| **7. Bespoke / Custom Jewellery** | **0** |

## 14. Expansion coverage by business area

Full detail with representative examples per role (head/category/product/attribute/question/comparison/long-tail): [`06_hod_seed_expansion_coverage.md`](06_hod_seed_expansion_coverage.md).

## 15. Commercial-category coverage — did Stage 6 correct Stage 5's blind spot?

**Only partially, and the honest answer is mostly no.** This is the single most important finding of this stage.

| Area | HEAD | CATEGORY | PRODUCT | ATTRIBUTE | TRANSACTIONAL | COMMERCIAL_RESEARCH |
|---|---|---|---|---|---|---|
| Engagement Rings | NOT FOUND | NOT FOUND | NOT FOUND | `engagement ring stone hardness` (10) | `should i buy a lab grown diamond engagement ring` (30) | NOT FOUND |
| Wedding Bands | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND |
| Earrings | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND |
| Necklaces & Pendants | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND |
| Bracelets | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND | `diesel bracelet` (1,300 — brand relevance unresolved) | NOT FOUND |
| Fine Jewellery | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND |
| Bespoke / Custom Jewellery | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND |

**None of the 34 catalog-derived seeds themselves — e.g. `diamond engagement rings`, `halo engagement rings`, `diamond wedding bands`, `diamond earrings`, `diamond bracelets`, `fine jewellery`, `bespoke jewellery` — appear anywhere in the 1,000 returned ideas.** This was checked directly, keyword-by-keyword, against the raw response (verified programmatically: 0 of 34 catalog seeds present in the 1,000 items).

**Why this happened (mechanical explanation, not a demand judgment):** `keyword_ideas/live` runs one relevance-ranked query across the *entire combined seed set* and returns the single globally-top-1000 result (of 139,845 available) for that blended set — it does not guarantee even representation per seed or per business area. Because 55 of the 89 seeds (62%) are Stage 5's lab-grown/education/certification/comparison terms and only 34 (38%) are the catalog commercial seeds, the algorithm's category-relevance signal skewed the top-1000 heavily toward the lab-grown-diamond-education cluster (431 of 1,000 items) and largely away from the discrete product-category clusters. This is a property of running one combined task with default relevance sorting and a 1,000-item cap, not evidence that Wedding Bands, Earrings, Necklaces & Pendants, Bracelets, Fine Jewellery, or Bespoke/Custom Jewellery lack US search demand — per CLAUDE.md, absence of a field here must not be read as zero demand.

**Not resolved this stage, no additional paid call made** (per instruction). Flagged for a future stage's consideration — e.g. running separate `keyword_ideas` (or another approved endpoint) tasks split by business area rather than one 89-seed blended task, or using `closely_variants: true` / seed subsets — as a **recommendation to consider**, not a decision made here.

## 16. Stage 3 overlap (current HOD rankings)

4 of the 1,000 expansion items exactly match HOD's current 28 ranked keywords: `lab grown diamonds hpht`, `lab grown diamonds cvd vs hpht`, `lab grown diamond hpht`, `cvd diamond vs lab grown` — all `CURRENTLY_RANKS`, all in the Lab-Grown Diamonds area, consistent with Stage 3's finding that HOD's existing footprint is concentrated there. The remaining 996 are `NOT_CURRENTLY_RANKING` (not labeled "opportunities," per instruction).

## 17. Stage 4 overlap

- **Exact overlap:** 87 of 1,000 Stage 6 items (8.7%) also appear in Stage 4's 1,000-keyword universe.
- **Newly discovered (not in Stage 4):** 913 of 1,000 (91.3%).
- **Percentage of Stage 4 covered by Stage 6:** 8.7% (87 of Stage 4's 1,000 rows).
- **Major concepts present in Stage 4 but not reappearing in this Stage 6 pull:** the large industrial-diamond-tooling and video-game/mineral noise clusters that dominated Stage 4 (Minecraft, home-security "Ring," industrial abrasives) are almost entirely absent here (only 9 flagged noise items vs. Stage 4's 448) — expected, since Stage 6's seed set was pre-filtered rather than a raw domain-relevance pull.
- **Major concepts newly introduced by the catalog-derived seeds specifically:** the handful of Engagement Rings (11), Wedding Bands (2), Earrings (1), Necklaces & Pendants (2), and Bracelets (2) items are new relative to Stage 4, which had confirmed zero matches in Wedding Bands/Necklaces/Bracelets/Fine Jewellery/Bespoke. This is a small but real, catalog-attributable addition — not the scale of correction the brief was aiming for (see §15).

## 18. Newly discovered major keyword concepts

- A large, previously-unseen **moissanite / diamond-simulant cluster** (`moissanite` 201,000; `is moissanite better than diamond`; `zirconia vs moissanite`; `moissanite vs morganite`; `does moissanite pass a diamond tester` and variants) — 44 Gemstones-tagged items plus several more under Lab-Grown Diamonds and Diamond Buying/Education, none of which appeared in Stage 4.
- A **diamond-authentication-testing sub-cluster** specifically around moissanite passing a diamond tester (5 near-duplicate phrasings, volumes 260–1,900).
- A small **engagement-ring policy/care cluster** (`can you return an engagement ring`, `do you wear engagement ring everyday`, `do men get engagement rings too`).

## 19. Obvious noise examples

9 of 1,000 (0.9%) flagged `possible_noise_flag = YES`: `diamond crystal kosher salt` (Morton Salt product, 60,500), `herkimer diamond` (unrelated quartz mineral, 33,100), `is oura ring waterproof` (unrelated wearable-tech brand, 6,600), plus 6 more preserved with reasons in the full CSV's `noise_reason` column. All preserved, none deleted.

## 20. Ambiguity examples

43 of 1,000 (4.3%) flagged `possible_ambiguity_flag = YES` — short, potentially cryptic strings whose intent isn't confidently readable from the text alone (e.g. bare 2–3-word "[X] diamond(s)" fragments). Preserved, not force-classified.

## 21. Important limitations

1. **No per-item seed attribution is available from this endpoint.** `keyword_ideas/live` returns a `seed_keywords` array only at the task level (the full list of all 89 keywords submitted) — it does **not** return which specific seed(s) produced each individual idea. This was verified directly against the raw response schema before building the cleaned CSV. As a result, `source_seeds`, `seed_count`, and `expansion_source` (STAGE5_VALIDATED / HOD_CATALOG / BOTH) **cannot be honestly populated per keyword** and are marked `NOT_AVAILABLE_FROM_API_RESPONSE` / `UNKNOWN_NOT_ESTABLISHABLE_FROM_API_RESPONSE` throughout the cleaned dataset, rather than invented or approximated. This is disclosed here explicitly per the project's "never invent DataForSEO metrics" / "avoid fake precision" rules.
2. **None of the 34 catalog-derived seeds themselves were returned as ideas**, and the specific commercial-category areas they targeted are barely represented in the top 1,000 results — see §15 for the full explanation. This is a property of the single-blended-task, default-relevance-sort, 1,000-item-cap approach used here (as instructed), not a demand finding.
3. **`business_area_best_effort`, `possible_noise_flag`, and role tags (QUESTION/COMPARISON/LONG_TAIL) are lightweight pattern-matching, not a certified taxonomy** — they exist to support the required coverage/commercial-check reporting for this stage, not to replace Stage 5-style classification or any future stage's clustering work.
4. **Category codes are preserved as DataForSEO's raw numeric codes**, not resolved to human-readable names — Stage 6's instructions restrict free reference calls this stage to endpoint-configuration/pricing verification only, so the (separately free) categories-name lookup used in Stage 4 was not repeated here.
5. This pull is 1,000 of 139,845 keywords DataForSEO's database associates with this specific 89-seed combination — a different seed mix, sort order, or `closely_variants`/`ignore_synonyms` setting would very likely surface a materially different set, particularly for the underrepresented commercial-category areas.
6. No clustering, page/URL recommendations, opportunity scoring, or competitor research was performed this stage, per instruction.

---

## Quality control checklist

- [x] All 55 Stage 5 `YES` seeds used
- [x] Catalog-derived seeds sourced from actual HOD site inventory (every row cites specific PDPs/category page)
- [x] Total seed count (89) ≤ 200
- [x] Exactly one paid task executed
- [x] No second paid endpoint called
- [x] `include_clickstream_data = false`
- [x] `include_serp_info = false`
- [x] `location_code = 2840` (US)
- [x] `language_code = "en"` (English)
- [x] Raw JSON saved: [`dataforseo/raw/06_hod_keyword_ideas_raw.json`](../raw/06_hod_keyword_ideas_raw.json) (does not overwrite prior raw files)
- [x] Cleaned CSV exists: [`06_hod_keyword_expansion.csv`](06_hod_keyword_expansion.csv)
- [x] Summary exists (this file)
- [x] Seed registry exists: [`06_hod_seed_registry.csv`](06_hod_seed_registry.csv)
- [x] High-value examples file exists: [`06_hod_expansion_high_value_examples.csv`](06_hod_expansion_high_value_examples.csv)
- [x] No keyword silently dropped — all 1,000 returned items appear in the cleaned CSV, including flagged noise/ambiguous ones
- [x] Duplicate keywords: none found within the returned 1,000 (verified programmatically)
- [x] Obvious noise flagged, not deleted
- [x] No clustering performed
- [x] No page/URL recommendations made
- [x] No competitor research performed (competitor/brand terms encountered were preserved, not analyzed)
- [x] No blog recommendations made
- [x] No opportunity score invented
