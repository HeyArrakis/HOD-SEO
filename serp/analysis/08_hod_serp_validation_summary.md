# Stage 8 — US Google SERP Validation Summary

Date: 2026-09-17
Status: **COMPLETE**

This stage validates what Google actually shows for 100 representative HOD-relevant keywords. It does not decide URLs, clusters, competitors, or content — those are later stages. Every field below is either a **directly observed SERP fact** (organic results, domains, URLs, `item_types`) or an explicitly labeled **interpretation** (`dominant_serp_page_type`, `validated_intent`, `validation_confidence`) derived from those facts by a disclosed rule-based heuristic — never DataForSEO's raw metrics re-invented.

## 1. Execution recap

- 100 Google Organic SERP tasks submitted via `POST /v3/serp/google/organic/task_post` (location_code 2840, language_code en, depth 10, device desktop, priority normal, no optional paid parameters), exactly as approved.
- Results retrieved via 100 free `GET /v3/serp/google/organic/task_get/advanced/{id}` calls.
- **Actual cost: $0.06** — confirmed two ways: (a) sum of the `cost` field across all 100 `task_get` responses = $0.06 exactly; (b) account balance before ($50.282136) minus after ($50.222136) = $0.06 exactly. No double-charging from the free retrieval calls, no additional paid parameters used.
- Raw responses: `serp/raw/08_stage8_by_id/{task_id}.json` (100 files) + `serp/raw/08_stage8_manifest.csv` (task_id → keyword → item_types map). One file (`natural diamond wholesale`) was the last of the 100 to finish processing on DataForSEO's side and was retrieved and saved separately after the other 99; all 100 are now present and verified.
- **Disclosed limitation:** a small number of the 99 raw files saved by an assisting subagent were saved as cleaned/condensed JSON (verbose fields like `xpath` paths and null `cache_url` entries trimmed) rather than byte-for-byte identical to the API response. All substantive SERP content — organic results, People Also Ask, related searches, local pack, images, video, AI Overview, knowledge graph — was preserved in every file; this was spot-checked across a sample of files before processing. This is disclosed here rather than presented as unqualified raw output.

## 2. SERP feature presence across the 100 keywords (observed fact)

| Feature | Present | % |
|---|---|---|
| People Also Ask | 98 | 98% |
| AI Overview | 78 | 78% |
| Video (video or short_videos) | 43 | 43% |
| Shopping/product signals (popular_products, product_considerations) | 39 | 39% |
| Images | 32 | 32% |
| Local Pack / Map | 10 | 10% |
| **Featured Snippet** | **0** | **0%** |

**Notable finding:** classic Featured Snippets did not appear on any of the 100 SERPs. AI Overview appeared on 78% instead — in this niche, Google's AI-generated answer box has functionally displaced the traditional featured snippet as the dominant "position zero" element. This has direct AEO relevance for later content-brief stages, but no content or URL decision is made here.

## 3. Dominant SERP page type (interpretation, from top-5 organic results per keyword)

| Dominant type | Count |
|---|---|
| EDITORIAL_GUIDE | 39 |
| OTHER (no confident majority classification) | 24 |
| BRAND | 14 |
| CATEGORY | 9 |
| COMPARISON | 8 |
| MIXED | 3 |
| PRODUCT | 1 |
| MARKETPLACE | 1 |
| EDUCATIONAL | 1 |

**Method and limitation, disclosed:** each of the top 5 organic results per keyword was classified by a simple URL/domain/title pattern-matcher (e.g., `/blog/` → EDITORIAL_GUIDE, `/products/` → PRODUCT, known marketplace domains → MARKETPLACE, "vs"/"compare"/"difference" in title → COMPARISON). This is a **rule-based approximation, not a manual page-by-page audit of all 500 top-ranking URLs**. 24% of keywords landed in OTHER because their top domains use retailer-specific URL structures the simple pattern-matcher couldn't confidently classify (e.g., `brilliantearth.com/diamonds/...`-style deep paths). The full top-5 domains and URLs are preserved unedited in `08_hod_serp_validation.csv` for every keyword, including the OTHER ones, so nothing is lost — only the automated label is uncertain. `validation_confidence` (HIGH/MEDIUM/LOW) flags exactly this: 49 HIGH, 48 MEDIUM, 3 LOW.

## 4. DataForSEO intent vs. validated SERP intent

| | Count |
|---|---|
| MATCH (DataForSEO intent = validated SERP intent) | 38 |
| MISMATCH | 62 |

**This is the single most important finding of Stage 8.** DataForSEO's automated intent label matched what Google's actual SERP shows for only 38 of 100 keywords. The dominant mismatch pattern: DataForSEO labeled many long-tail question keywords `transactional` or `commercial`, while the actual SERP is dominated by Reddit threads, forum discussions, and editorial guide content — i.e., genuinely informational.

Concrete example: 15 of the 28 current-ranking (Stage 3) keywords carry a DataForSEO intent of `transactional` or `commercial`, but 25 of those 28 keywords' SERPs validate as INFORMATIONAL or COMPARISON-dominated (editorial guide / comparison page types, AI Overview present on 25/28). This confirms, with direct SERP evidence rather than inference, the Stage 3 observation that HOD's existing organic footprint sits almost entirely on informational/comparison ground — not that DataForSEO mislabeled these as an error, but that DataForSEO's `main_intent` field is a coarse signal that this project should not treat as authoritative for page-type decisions, consistent with CLAUDE.md principle 1 ("search intent is more important than keyword wording") and the instruction not to force a classification when the SERP doesn't clearly establish one.

| Validated intent | Count |
|---|---|
| INFORMATIONAL | 48 |
| UNCLEAR | 24 |
| NAVIGATIONAL | 14 |
| TRANSACTIONAL | 10 |
| MIXED | 3 |
| COMMERCIAL_RESEARCH | 1 |

24 keywords validated as UNCLEAR (no forced classification) rather than guessed — consistent with instruction §18.

## 5. Current-ranking (Stage 3) keyword validation

All 28 of HOD's current organic-ranking keywords were included and validated. Full detail in `08_hod_serp_validation.csv`. Headline finding: **25 of 28 show AI Overview present, and the large majority validate as EDITORIAL_GUIDE or COMPARISON dominant page types** — HOD's actual page ranking for these terms (mostly the CVD-vs-HPHT blog article) matches what Google is currently rewarding: long-form comparison/education content, not a commercial page. This is a fact pattern for later stages (SERP validation feeding architecture) to build on — no architecture or content decision is made here.

## 6. Ambiguous keyword resolution (5 of 5 validated)

Stage 5/6 flagged these as AMBIGUOUS because keyword text alone couldn't establish meaning. The SERP resolves three of them decisively:

- **`thc diamond` / `thc diamonds` / `thca diamond`** — SERPs are dominated by cannabis/CBD retailers and forums (`recovered.org`, `fluresh.com`, `astriafarm.com`, `smokymountaincbd.com`). Google resolves these as a cannabis-concentrate term ("THC diamonds"), **not** a jewelry query. Validated as off-topic for HOD, on direct SERP evidence.
- **`dust diamonds`** — resolves to diamond-painting/craft-kit supplies (`patrickadairsupplies.com`, `diamondartclub.com`), not jewelry. Same as the previously-noted `diamond dotz` pattern.
- **`raw diamond`** — resolves to genuine rough/uncut natural diamond dealers and educational content. On-topic.

This is exactly what SERP validation is for: keyword text alone (Stage 5) could not resolve these; the actual SERP does. No status field in the master database was changed by this — that reclassification, if wanted, is a decision for a later stage to make deliberately, informed by this evidence.

## 7. New Stage 6 concepts: moissanite / diamond-tester queries (8 of 8 validated)

Per instruction, these are **validated, not treated as opportunities**:

- The moissanite query space is real and active: `moissanite` itself (201,000 volume) shows a MIXED SERP — a genuine moissanite retailer (`moissaniteco.com`), Wikipedia, and `charlesandcolvard.com` (a real branded moissanite manufacturer) all rank, alongside informational content.
- All 6 comparison/definition-style moissanite queries (`is moissanite better than diamond`, `moissanite vs lab grown diamond which is better`, `is a lab grown diamond the same as moissanite`, `can moissanite pass diamond tester`, `moissanite clarity chart`) validate as INFORMATIONAL or COMPARISON, dominated by Reddit, `brilliantearth.com`, and `charlesandcolvard.com` — **not** by transactional product pages.
- `does moissanite pass a diamond tester` and `natural moissanite` validated UNCLEAR (Reddit/forum-heavy, no confident single page-type majority).

Fact pattern only: this space is genuinely informational/comparison-driven in the SERP today, not dominated by any retailer's commercial page — no relevance, priority, or content decision is made from this here.

## 8. Thin commercial-category keywords (Wedding Bands / Earrings / Necklaces / Bracelets)

All 8 available keywords from these four thin categories were validated. Every one is Reddit/forum/editorial-dominated and validates as INFORMATIONAL (7 of 8) or UNCLEAR (`diesel bracelet`, `can you turn diamond earring into ring`) — none validate as a commercial CATEGORY or PRODUCT page type. This is consistent with, and adds direct SERP evidence to, the Stage 4/5/6/7 finding that the master database's available keyword coverage for these categories skews informational/care-question rather than commercial-category — not evidence about demand for a category page itself, since no such keyword was in the validation set (Fine Jewellery and Bespoke had zero candidates at all, as documented in the Stage 8 preflight).

## 9. Fine Jewellery / Bespoke Custom Jewellery

Not represented in this validation set — the Stage 8 preflight confirmed zero suitable keywords exist anywhere in the 1,936-keyword master database for these two business areas (`NO_SUITABLE_MASTER_KEYWORD_FOR_SERP_VALIDATION`, not invented). This gap is unchanged by Stage 8 and is carried forward for whoever scopes future keyword-discovery work.

## 10. What Stage 8 does NOT conclude

Per instruction, none of the following were decided in this stage: which keyword is a priority, which page HOD should build, whether any keyword is a content opportunity, how keywords should cluster, or how competitors compare. `top_ranking_domains` / `top_ranking_urls` are preserved as raw observed fact for Stage 9 (competitor gap analysis) to use — no competitor conclusion is drawn here.

## 11. Files produced

- `serp/raw/08_stage8_by_id/*.json` (100 raw task_get responses)
- `serp/raw/08_stage8_manifest.csv` (task_id/keyword/item_types index)
- `serp/analysis/08_hod_serp_validation.csv` (100 rows, full field set per keyword)
- `serp/analysis/08_hod_serp_validation_selection.csv` (unchanged from preflight)
- `serp/analysis/08_hod_serp_validation_preflight.md` (unchanged from preflight)
- `serp/analysis/08_hod_serp_validation_summary.md` (this file)
