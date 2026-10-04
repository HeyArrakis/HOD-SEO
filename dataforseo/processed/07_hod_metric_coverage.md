# Stage 7 — Metric Coverage Report

Date: 2026-09-17

## Coverage overview

| Metric | Value |
|---|---|
| Total master keywords | 1,936 |
| Keywords eligible for enrichment (status ≠ NOISE/COMPETITOR_BRAND, i.e. INCLUDE + AMBIGUOUS) | 1,436 |
| Keywords actually enriched (have `search_volume` from a reused source) | 1,929 / 1,936 (99.6%) |
| Eligible (INCLUDE/AMBIGUOUS) keywords enriched | 1,429 / 1,436 (99.5%) |
| Eligible keywords with zero volume data | 7 / 1,436 (0.5%) |

"Enriched" here means the keyword carries a DataForSEO-sourced `search_volume` value with documented provenance (`metric_source`) — not that a new paid call was made this stage. All enrichment was achieved by reusing Stage 3/4/6's already-collected metrics; **zero new paid DataForSEO calls were made in Stage 7.**

## Fields successfully populated (reused, not invented)

| Field | Populated | % of 1,936 |
|---|---|---|
| search_volume | 1,929 | 99.6% |
| intent (main_intent/search_intent) | 1,929 | 99.6% |
| cpc | 1,238 | 63.9% |
| competition | 1,841 | 95.1% |
| keyword_difficulty | 1,612 | 83.3% |
| monthly_search_data | 1,929 | 99.6% |
| serp_summary | 736 | 38.0% |

## Fields/rows not populated, and why

- **7 keywords, 0% of any metric** — long-tail Stage-6-only terms DataForSEO's own keyword database has no Google Ads volume data for. Listed in `07_hod_master_keyword_summary.md` §10–11. Filling these would require a new `keyword_overview/live` call; per CLAUDE.md this needs a separate, explicit cost-gate approval before running (see final Stage 7 report) — not performed automatically.
- **698 keywords missing `cpc`** (691 with volume but no cpc, + 7 with nothing) — reflects genuinely absent Google Ads bid data for low-commercial-intent or very-low-volume terms in DataForSEO's source data, not a Stage 7 gap. A fresh call against the same backend database would very likely return the same null.
- **95 keywords missing `competition`** — same underlying reason as cpc.
- **324 keywords missing `keyword_difficulty`** — same underlying reason.
- **1,200 keywords missing `serp_summary`** — mechanical: these rows' best-available metric source was Stage 6 (`keyword_ideas/live`), which was run with `include_serp_info=false` (per the Stage 6 cost/scope decision already logged) — not a per-keyword data gap, a stage-level scope choice made and disclosed in Stage 6.

## Exclusions from enrichment eligibility

- **457 NOISE-status keywords** — deliberately not prioritized for enrichment attention (all already carry whatever metric came from their origin pull; not treated as "missing" in any special sense, but excluded from the "strategic eligible" count above per CLAUDE.md instruction to avoid spending analysis effort on confirmed noise). Metrics are still preserved in the master database, not deleted.
- **43 COMPETITOR_BRAND-status keywords** — same treatment; reserved for Stage 9 competitor-gap analysis, not enrichment-prioritized here.

## Reasons for the "eligible but no metric" residual (7 keywords)

All 7 are Stage-6-only, i.e. never appeared in Stage 3 (current rankings) or Stage 4 (domain-relevance discovery, itself independently checked at 518,487 candidate size). `keyword_ideas/live` (Stage 6) can return an idea keyword with no `search_volume` field when DataForSEO's Keyword Database has the keyword's *existence* (e.g., as a synonym/related term) but no measurable Google Ads search volume for it in the current dataset. This is a genuine data-absence, not a Stage 7 processing failure.
