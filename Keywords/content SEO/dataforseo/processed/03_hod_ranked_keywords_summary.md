# House of Diams — Stage 3: Current US Organic Keyword Landscape

Date: 2026-09-17
Source: DataForSEO Labs, Google, `ranked_keywords/live` — 1 API task, target `houseofdiams.com`, location_code 2840 (United States), language_code en (English), limit 1000.
Raw response: [`dataforseo/raw/03_hod_ranked_keywords_raw.json`](../raw/03_hod_ranked_keywords_raw.json)
Cleaned dataset: [`03_hod_ranked_keywords.csv`](03_hod_ranked_keywords.csv)

This is a **current-state snapshot only**. No clustering, page recommendations, blog/Education recommendations, or existing-content (retain/rewrite/redirect/retire) decisions are made here — those come in later stages once demand, intent, SERP evidence, and competitor gaps have all been layered on.

---

## 1. Total ranking keywords returned

**28 keywords.** The endpoint's own `total_count`/`items_count` both report 28 — this is the complete set the API has on file for this domain in the US/English index right now, not a truncated sample (the request allowed up to 1,000). All 28 are **organic**; the `paid` metrics block returned all zeros (HOD is not shown to be running Google Ads currently, per this data source).

## 2–6. Ranking position distribution

| Position band | Count |
|---|---|
| 1–3 | 0 |
| 4–10 | 0 |
| 11–20 | 0 |
| 21–30 | 2 |
| 21–50 (full band, includes the 2 above) | 19 |
| 51–100 | 8 |
| 100+ (not requested, but present in the data) | 1 (rank 104) |

**HOD currently has zero keywords ranking on page 1 (positions 1–10) or even in positions 11–20.** Every ranking keyword sits on page 3 or later (rank 21+). This is consistent with a small, pre-relaunch site with limited topical footprint and backlink profile — not evidence of a specific problem, just the current baseline.

## 7. Top keywords by search volume

| Keyword | Volume | Rank | Intent | Ranking URL |
|---|---|---|---|---|
| hpht lab grown diamonds | 8,100 | 49 | transactional | `/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams` |
| hpht lab grown diamond | 8,100 | 49 | transactional | same blog URL |
| side stones engagement rings | 1,000 | 104 | transactional | `/engagement-rings/by-desgin/side-stone-rings` |
| hpht vs cvd | 720 | 54 | informational | `/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams` |
| marquise oval diamond | 390 | 90 | transactional | `/shop/oval-floral-diamond-ring` |
| (remaining 23 keywords) | 20–30 each | 27–95 | mixed | mostly the same blog URL |

Per the project's interpretation rules, high volume here is reported as a fact about search demand, not a claim that these are "opportunities" — position, difficulty, and business relevance haven't been jointly assessed yet.

## 8. Top commercial-intent keywords

7 keywords carry `commercial` intent, all volume 20–30, all ranking 32–95: e.g. *lab-grown diamond cvd vs hpht* (30, rank 32), *cvd diamond vs lab grown* (30, rank 33), *is 18k gold or 14k gold better* (30, rank 95). No commercial-intent keyword in this dataset has meaningful volume relative to the two 8,100-volume transactional terms above.

## 9. Top informational-intent keywords

14 keywords carry `informational` intent — the largest intent group in this dataset. By far the highest-volume one is **hpht vs cvd** (720, rank 54). The rest (*are cvd diamonds real*, *how to choose a lab grown diamond*, *which is better cvd or hpht diamond*, etc.) sit at volume 20–30, ranks 27–84.

## 10. Top ranking URLs by number of ranking keywords

| Ranking URL | # keywords |
|---|---|
| `/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams` | 19 |
| `/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams` | 3 |
| `/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams` | 3 |
| `/blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide` | 1 |
| `/shop/oval-floral-diamond-ring` | 1 |
| `/engagement-rings/by-desgin/side-stone-rings` | 1 |

One single blog article (the CVD vs HPHT comparison) accounts for **68% of all 28 ranking keywords**. This is a concentration fact, not a recommendation to expand, retire, or split that article.

## 11. Keywords where HOD is already on page 1

**None.** Zero keywords rank in positions 1–10.

## 12. Keywords ranking in positions 11–20

**None.**

## 13. Keywords ranking in positions 21–30

**2 keywords:**
- *are cvd diamonds real* (volume 30, rank 27) → `/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams`
- *which is better lab grown diamonds or natural diamonds* (volume 30, rank 29) → `/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams`

## 14. High-demand keywords with weak rankings

Relative to the rest of this dataset (which otherwise tops out at volume 30), four keywords stand out as comparatively high-demand while ranking well outside page 1:
- *hpht lab grown diamonds* / *hpht lab grown diamond* — 8,100 volume, rank 49
- *side stones engagement rings* — 1,000 volume, rank 104
- *hpht vs cvd* — 720 volume, rank 54
- *marquise oval diamond* — 390 volume, rank 90

Per project rules, this is reported as a demand/ranking gap only — it is **not** a claim that these are ranking "opportunities." Keyword difficulty, SERP intent, and competitor occupancy for these terms have not yet been validated (that's stages 7–8), and search volume alone is explicitly excluded as a priority signal.

## 15. Keywords where the ranking URL appears mismatched with search intent

Flagged for later SERP/intent validation, not resolved here:
- **hpht lab grown diamonds / hpht lab grown diamond** (transactional intent, 8,100 volume) rank on a comparison **blog article**, not a commercial/category/product page — the page type doesn't obviously match a transactional query.
- **lab grown diamond hpht** and **lab grown diamonds hpht** (also tagged transactional) rank on the same comparison blog article.
- **cvd/hpht diamond tester** (transactional, volume 30) also ranks on the same blog article rather than a product or tool page.
- By contrast, **side stones engagement rings** (transactional) ranking on `/engagement-rings/by-desgin/side-stone-rings` and **marquise oval diamond** (transactional) ranking on a specific product page look like more intuitive page-type matches, though this hasn't been SERP-validated yet.

These are observations for the SERP validation stage (Stage 8) to confirm or reject — DataForSEO's own intent classification is a model output, not ground truth, and hasn't been checked against the actual live SERP yet.

## 16. Keywords where multiple HOD URLs rank for the same keyword

**None found.** Every one of the 28 keywords maps to exactly one HOD ranking URL — there is no internal keyword cannibalization visible in this current-rankings dataset.

## 17. Initial observations about HOD's existing organic topical footprint

- HOD's entire current organic footprint is **lab-grown diamond education/comparison content** (CVD vs. HPHT, lab-grown vs. natural, 14k vs. 18k gold) plus two isolated commercial hits (a side-stone-ring category page and one product page). There is no visible organic footprint yet for engagement rings, wedding bands, earrings, necklaces, or bracelets as product categories — despite these making up most of the live catalog per the Stage 1 inventory.
- The footprint is **narrow and concentrated**: 3 blog articles account for 25 of the 28 ranking keywords (89%), and one article alone accounts for 19 (68%).
- All rankings sit on page 3 or worse (rank 21+) — there is currently no page-1 or page-2 presence to build from or protect.
- No paid search activity was detected for this domain in this data source.
- This is a **current-state fact pattern**, not a gap analysis or a set of recommendations — competitor gap analysis (Stage 9) and SERP validation (Stage 8) are still required before drawing conclusions about what this footprint means strategically.

---

## Interpretation caveats (per project rules)

- Search volume, keyword difficulty, and intent classification are DataForSEO model outputs as of their `last_updated_time` fields (dataset — August/September 2026) — not verified against a live SERP pull, and not treated as guaranteed ranking probability.
- No keyword here is called an "opportunity," and no keyword difficulty score here is called "easy" — those judgments require SERP evidence (Stage 8) and business-relevance weighting, not yet performed.
- Paid competition (`competition`/`competition_level`, `cpc`) reflects Google Ads paid auction dynamics, not organic ranking difficulty — the two are reported separately in the CSV and were not blended into any single score.
- Product-page URL coverage in this dataset reflects only what currently ranks; it says nothing about the other 168 product URLs in the Stage 1 inventory that aren't yet ranking for anything in the US index.
