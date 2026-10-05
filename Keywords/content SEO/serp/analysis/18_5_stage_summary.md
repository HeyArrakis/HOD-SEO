# Stage 18.5 — Targeted SERP validation: executive summary

**Status: COMPLETE.** Date: 2026-09-25.

## What was run

- **Call:** one approved paid call, `POST /v3/serp/google/organic/task_post`, with **17 tasks**: US (2840), English, depth 10, desktop, normal priority, no clickstream.
- **Results:** retrieved with 17 free `task_get/advanced` calls. **17/17 successful**.
- **Price:** re-verified from the account price table before submission at $0.0006 per task. Approved maximum $0.0102.
- **Actual spend:** **$0.0102**, shown both in the API response and in the balance difference ($49.853896 → $49.843696). Cumulative project spend is now **$0.34556**.
- **Raw data:** `dataforseo/raw/18_5_stage_serp/` holds 17 responses, the task_post response and `manifest.csv`.

## What the SERPs show

- **Intent:** 16 of 17 are informational. The exception is `engagement ring settings`, which is MIXED and commercial-led: shop pages, local pack, products, and an AI Overview section on shopping for settings.
- **SERP features:** AI Overview on 16/17 and PAA on 17/17. `diamond carat size chart` has no AI Overview; it is image-led, and every organic result is a carat-to-mm chart.
- **Formats Google expects:**
  - charts: colour, carat size, and ring size, where the AI Overview contains a US size table;
  - numbered steps for measuring a ring;
  - comparison tables for 14k vs 18k and white gold vs platinum;
  - answer-first blocks for the lab-grown value, ethics and cloudiness questions.
- **Terms with mixed meanings:**
  - `diamond cut` mixes cut quality with shape lists;
  - `diamond certificate` puts the labs' own pages (IGI, GIA) first;
  - `diamond shapes` (plural) is overwhelmingly about jewellery, so the geometric dilution seen in Stage 8 on the singular term is weak here.

## Effect on Stage 18

The Stage 18 files were not edited. 141 change-log rows cover 16 targets:

| Change type | Rows |
|---|---|
| CONFIRMED | 36 |
| STRENGTHENED | 47 (26 imply a higher Stage 19 weight) |
| CHANGED | 19 (all 9 "format unvalidated" rows and 10 head-term rows resolved) |
| NEW_EVIDENCE | 34 |
| WEAKENED | 3 |
| UNCHANGED | 1 |
| CONFLICT | 1 |

Main shifts:
- **Now CRITICAL:** ring-size chart and measuring steps, and kimberlite pipes on the natural-diamond page. The carat-to-mm size chart is a new CRITICAL expectation.
- **Stronger:** 4Cs "order of importance", lab-grown price trend and natural-value comparison, and the mining/labour side of ethics.
- **Previously dropped, now evidenced:** fancy-colour boundary note, care/cleaning, conflict-free mention and price-by-carat context.
- **Weaker:** resizing on the ring-size SERPs, lab-grown grading on the 4Cs head term, and geometric intent on "diamond shapes". All three stay covered at a lower weight.

## Needs your decision (not changed here)

1. **`engagement ring settings` is commercial-led (CONFLICT).** Whether an Education page should own it is a Stage 15-style ownership question.
2. **Business facts:**
   - HOD's energy source and sustainability claims. This now matters more: the ethics SERP names India/China coal grids, and HOD manufactures in Surat.
   - Buy-back policy.
   - Which labs grade HOD stones.
   - Whether HOD sells settings without a centre stone.
   - Metal options.
3. **Search volumes:** none were requested, so demand for these head terms is still unmeasured.

Full detail is in `18_5_semantic_supplement.md`, `18_5_targeted_serp_validation.csv` and `18_5_stage18_change_log.csv`. Stage 19 has not been started.
