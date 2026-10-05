# Stage 9 — Competitor & Keyword Gap Analysis Summary

Date: 2026-09-17
Status: **COMPLETE**

This stage identifies which domains repeatedly appear in Google's US organic results for HOD-relevant search queries, what type of pages they use, and where HOD currently has less/absent representation. It is descriptive evidence only — no clustering, URL planning, prioritization, or content decisions are made here.

## 1. Method

- **No new DataForSEO API call was made this stage. Actual cost: $0.00.** Everything below was built by re-reading data already collected and paid for in Stage 8 (100 SERP tasks, $0.06 total, charged 2026-09-17) and Stage 7 (1,936-keyword master database), per CLAUDE.md's "reuse previously collected datasets" rule and this stage's explicit instruction to attempt Stage 9 without new spend first.
- Stage 8's processed CSV (`08_hod_serp_validation.csv`) only preserves each keyword's **top 5** organic domains/URLs (its own disclosed page-type-classification method used only the top 5). To meet this stage's "top 10 where available" requirement, the 100 raw SERP JSON files (`serp/raw/08_stage8_by_id/*.json`, depth=10, already collected) were re-parsed directly for every `type=organic` item, using DataForSEO's own `rank_group` field (the organic-only rank, 1–10) as the position. This was verified to exactly reproduce Stage 8's top-5 domain list for all 100 keywords before proceeding (0 mismatches) — so the top-10 extraction is a straightforward, low-risk widening of already-verified Stage 8 data, not a new methodology.
- This produced **795 domain × keyword organic appearances across 296 unique domains** for the 100 validated keywords.
- **Competitor type classification** (Part 3 taxonomy) was applied by hand to the **91 domains that appear for 2 or more of the 100 validated keywords** — the "repeatedly appearing" set the stage brief defines as the primary object of study — using the actual observed titles/URLs/breadcrumbs from the raw SERP data plus general knowledge of named, identifiable jewelry/diamond-industry brands. Each classification carries a `classification_confidence` (HIGH/MEDIUM/LOW) and a `classification_note` citing the evidence. **1 of the 91 domains (`lgdusallc.com`) could not be classified with confidence and is marked `UNKNOWN`**, per instruction, rather than guessed.
- The **205 domains that appear for only 1 of the 100 keywords** were **not** individually classified (`competitor_type=UNKNOWN`, `business_relevance=NOT_ASSESSED`) — this is a disclosed scope limit, not an omission; see Limitations (§11). Every one of their 205 appearances is still preserved as raw evidence in the landscape file.
- `dominant_serp_page_type` / `validated_intent` / `business_area` per keyword are reused unchanged from Stage 8 — not recomputed. Per-domain page type (`domain_page_type_this_url`) is reused from Stage 8's own top-5 URL/title pattern-matcher where available; for rank 6–10 appearances (beyond what Stage 8 classified), it is marked `NOT_CLASSIFIED_BEYOND_TOP5` rather than extending Stage 8's heuristic to new, unverified territory.
- **HOD's presence was checked directly against the raw Stage 8 SERP data**, not assumed from Stage 3. Finding: **`houseofdiams.com` does not appear in the observed top-10 organic results of any of the 100 Stage 8 SERPs.** Stage 3's 28 historical rankings (positions 21–104, pulled from DataForSEO's `ranked_keywords` database snapshot, a different data source/time than the live Stage 8 SERP check) are preserved separately in every relevant row for reference — this is consistent (all recorded Stage 3 ranks are beyond position 10), not a contradiction or a new drop.

## 2. Data sources

- `serp/raw/08_stage8_by_id/*.json` (100 files, depth=10 raw organic results) — primary source for this stage
- `serp/analysis/08_hod_serp_validation.csv` (100 rows — business_area, validated_intent, dominant_serp_page_type, top-5 page types, HOD Stage 3 reference)
- `serp/raw/08_stage8_manifest.csv` (task_id ↔ keyword)
- `dataforseo/processed/07_hod_master_keyword_database.csv` (1,936 keywords, for business-area coverage denominators)
- `site/01_site_inventory.md`, `site/01_existing_blog_inventory.csv`, `site/01_existing_content_inventory.csv` (HOD's current blog/education content, for Part 7)

## 3. Competitor extraction (Part 1)

- **296 unique domains** observed across the 795 organic appearances in the 100 validated SERPs.
- **91 domains repeat** (appear for ≥2 of the 100 keywords); **205 appear for exactly 1 keyword** (long tail).
- Top domains by validated-keyword count (full table: `09_hod_competitor_frequency.csv`):

| Domain | Validated keywords | Top-5 appearances | Top-10 appearances | Type |
|---|---|---|---|---|
| www.reddit.com | 61 | 60 | 65 | FORUM_COMMUNITY |
| www.brilliantearth.com | 41 | 24 | 41 | DIRECT_JEWELLERY_ECOMMERCE |
| www.youtube.com | 29 | 13 | 32 | OTHER (video platform, mixed content) |
| www.ritani.com | 23 | 18 | 24 | DIRECT_JEWELLERY_ECOMMERCE |
| www.bluenile.com | 19 | 15 | 19 | DIRECT_JEWELLERY_ECOMMERCE |
| www.gia.edu | 18 | 16 | 18 | DIAMOND_EDUCATION |
| stienhardt.com | 16 | 9 | 16 | DIRECT_JEWELLERY_ECOMMERCE |
| www.rarecarat.com | 15 | 7 | 15 | COMPARISON_REVIEW |
| www.withclarity.com | 14 | 8 | 14 | DIRECT_JEWELLERY_ECOMMERCE |
| en.wikipedia.org | 13 | 10 | 13 | REFERENCE |
| www.miadonna.com | 12 | 10 | 12 | DIRECT_JEWELLERY_ECOMMERCE |
| taylorandhart.com | 11 | 1 | 11 | DIRECT_JEWELLERY_ECOMMERCE |
| www.instagram.com | 11 | 7 | 11 | OTHER (social, mixed content) |

Raw evidence (every domain × keyword organic appearance, all 296 domains) is preserved unedited in `09_hod_competitor_landscape.csv` (795 rows).

## 4. Competitor frequency & types (Parts 1 & 3)

Type breakdown of the **91 classified repeat domains**:

| Competitor type | Count |
|---|---|
| DIRECT_JEWELLERY_ECOMMERCE | 56 |
| OTHER (social platforms, B2B suppliers, video) | 19 |
| DIAMOND_EDUCATION | 6 |
| FORUM_COMMUNITY | 3 |
| MARKETPLACE | 3 |
| COMPARISON_REVIEW | 1 (rarecarat.com) |
| REFERENCE | 1 (Wikipedia) |
| EDITORIAL_GUIDE | 1 (forbes.com — treated as major media, not a jewelry seller) |
| UNKNOWN | 1 (lgdusallc.com — insufficient evidence) |

Business relevance breakdown: **71 RELEVANT**, **10 MIXED** (social/video/marketplace platforms whose individual results vary — YouTube, Instagram, Facebook, Pinterest, TikTok, Amazon, eBay, Etsy, Quora, Yelp), **10 OFF_TOPIC** — all explained by the same word-polysemy pattern Stage 4 first documented: "diamond" as a WNBA/NBA player surname (espn.com, basketball-reference.com), a cannabis-concentrate product ("THC diamonds" — recovered.org, astriafarm.com, shopburb.com, smokymountaincbd.com, fluresh.com, elevationcannabis.co, diamondcbd.com), and unrelated local businesses whose name contains "Diamond" (via facebook.com/linkedin.com company pages).

**No competitor score, ranking, or tier was created.** No domain is called "better" or "stronger" than another.

## 5. HOD vs. competitor presence (Part 2)

- **HOD does not appear in the observed top-10 organic results for any of the 100 validated keywords** (0 of 795 organic appearances belong to houseofdiams.com). This is a directly observed Stage 8 SERP fact, not an inference.
- Of the 100 keywords, **28 have a Stage 3 historical ranking on record** (positions 21–104, all beyond this SERP check's depth-10 window — consistent, not a new loss). The other 72 have no HOD ranking on record from any stage.
- Full per-keyword, per-competitor detail (including HOD's Stage 3 reference position where one exists) is in `09_hod_competitor_landscape.csv`.

## 6. Keyword gap observations (Part 4)

`09_hod_keyword_gap.csv` contains **643 gap-observation rows**, broken out by type. These are observations, not recommendations — no row says HOD "should" build anything.

| Gap type | Rows | What it records |
|---|---|---|
| A — HOD has a master keyword but no observed SERP presence | 100 | One row per validated keyword; true for all 100 (see §5) |
| B — A relevant-type competitor appears where HOD does not | 485 | Every organic appearance (rank 1–10) by a domain classified as one of DIRECT_JEWELLERY_ECOMMERCE / LAB_GROWN_DIAMOND_SPECIALIST / DIAMOND_EDUCATION / EDITORIAL_GUIDE / COMPARISON_REVIEW / MARKETPLACE / FORUM_COMMUNITY / REFERENCE (i.e. excluding OTHER/OFF_TOPIC/UNKNOWN domains) |
| C — HOD's ranking page type vs. the SERP's dominant page type | 28 | 22 keywords where HOD's blog-article format matches the dominant EDITORIAL_GUIDE/COMPARISON pattern (no gap); **6 where it doesn't** (see below) |
| D — Competitor page/topic-type pattern observed per business area | 14 | Aggregate rows, one per business area with both validated keywords and classified relevant competitors |
| E — Business-area coverage | 16 | Aggregate rows, one per controlled business area (§8) |

**Type C detail — the 6 keywords where HOD's existing ranking page type differs from the SERP's dominant pattern:**

| Keyword | HOD Stage 3 position | SERP dominant page type |
|---|---|---|
| are cvd diamonds real | 27 | OTHER |
| cvd/hpht diamond tester | 68 | CATEGORY |
| marquise oval diamond | 90 | PRODUCT |
| side stones engagement rings | 104 | CATEGORY |
| what is cvd lab grown diamond | 36 | MIXED |
| which diamond is better lab grown or natural | 40 | OTHER |

Two of these (`cvd/hpht diamond tester`, `side stones engagement rings`) show a **CATEGORY**-dominant SERP where HOD's only ranking page is an informational blog article — a page-type mismatch worth carrying into a future page-type/architecture stage as evidence, not resolved here.

## 7. Business-area coverage (Part 5)

| Business area | Master keywords (status=INCLUDE) | Validated (Stage 8) keywords | Note |
|---|---|---|---|
| 1. Engagement Rings | 23 | 3 | Coverage observed |
| 2. Wedding Bands | 2 | 2 | Weak master coverage |
| 3. Earrings | 3 | 2 | Weak master coverage |
| 4. Necklaces & Pendants | 2 | 2 | Weak master coverage |
| 5. Bracelets | 2 | 2 | Weak master coverage |
| 6. Fine Jewellery | 0 | 0 | **Absent** — confirmed again, matches Stage 8 preflight |
| 7. Bespoke / Custom Jewellery | 0 | 0 | **Absent** — confirmed again, matches Stage 8 preflight |
| 8. Lab-Grown Diamonds | 509 | 15 | Coverage observed |
| 9. Natural Diamonds | 21 | 4 | Coverage observed |
| 10. Diamond Shapes | 12 | 4 | Coverage observed |
| 11. Diamond Cuts | 1 | 1 | Weak master coverage |
| 12. Diamond Quality / 4Cs | 144 | 5 | Coverage observed |
| 13. Diamond Certification | 33 | 4 | Coverage observed |
| 14. Diamond Buying / Education | 40 | 5 | Coverage observed |
| 15. Jewellery Materials / Metals | 6 | 2 | Weak master coverage |
| 16. Gemstones | 45 | 8 | Coverage observed |

(415 of the 1,936 master keywords, and 38 of the 100 validated keywords, carry `business_area=UNCLASSIFIED_OR_UNKNOWN` from Stage 5/6 — preserved as-is, not force-assigned here.)

For Wedding Bands / Earrings / Necklaces & Pendants / Bracelets, the observed competitor pattern (from the RELEVANT-classified frequency table) includes commercial CATEGORY pages — e.g. `doamore.com` (`/engagement-rings/side-stones/`), `diamonds.zales.com` (`/side-stones-engagement-rings`) — alongside forum/editorial results, consistent with Stage 8's finding that this validated sample skews informational but is not exclusively so.

## 8. Page/topic patterns among frequent competitors (Part 6)

Descriptive only — not a recommendation:

- **EDITORIAL_GUIDE / blog content** is the single most common pattern among DIRECT_JEWELLERY_ECOMMERCE competitors for CVD/HPHT, lab-grown-vs-natural, and 14k-vs-18k-gold topics (e.g. `www.ritani.com/blogs/education/`, `stienhardt.com/blogs/lab-grown-diamond-insights/`, `regalhattongarden.co.uk/blogs/lab-diamonds/`, `www.sylviejewelry.com/blog/`).
- **DIAMOND_EDUCATION domains** (gia.edu, igi.org, americangemsociety.org, gemsociety.org) appear specifically for certification and 4Cs-adjacent queries with dedicated reference/guide pages (e.g. `www.igi.org/reports/lab-grown-diamond-report/`, `4cs.gia.edu/en-us/diamond-clarity/`).
- **COMPARISON_REVIEW** (rarecarat.com) and **FORUM_COMMUNITY** (reddit.com, pricescope.com, quora.com) dominate the broad informational/definitional queries (moissanite comparisons, "is X real", "which is better").
- **CATEGORY-type commercial pages** appear from DIRECT_JEWELLERY_ECOMMERCE competitors specifically on side-stone and shape-specific queries (`doamore.com`, `diamonds.zales.com`, `charlesandcolvard.com`, `moissaniteco.com`).
- **MARKETPLACE** (amazon.com, ebay.com, etsy.com) appears mainly for loose-stone, tester-tool, and craft/novelty ("diamond dotz") queries — a mixed-relevance pattern, not a jewelry-retail pattern.

## 9. Existing HOD content cross-reference (Part 7)

Observation only — no retain/rewrite/merge/redirect/retire decision is made here (that is a later stage).

- **CVD/HPHT topic**: 19 of the 100 validated keywords relate to CVD/HPHT. HOD's only relevant asset is the single blog article `cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know` (Stage 1/3: source of 19 of HOD's 28 current rankings). Competitors covering the same exact topic with dedicated pages include `www.ritani.com`, `stienhardt.com`, `regalhattongarden.co.uk`, `taylorandhart.com`, `www.miadonna.com`, `diamondrensu.com`, `www.gia.edu` — all EDITORIAL_GUIDE or DIAMOND_EDUCATION format, the same format HOD already uses.
- **14K vs 18K gold**: 3 validated keywords (`is 14k diamond good`, `is 18k gold or 14k gold better`, `which one is better 14k or 18k gold`) relate directly to HOD's existing blog article `14k-vs-18k-gold-for-diamond-jewellery-which-is-better`. None of these 3 show houseofdiams.com in the observed SERP; competitors present include `www.sylviejewelry.com`, `www.valeriemadison.com`, `hiholden.com` — all EDITORIAL_GUIDE blog format, same as HOD's existing article.
- **GIA vs IGI certification**: 2 validated keywords (`gia vs igi lab diamond`, `lab-grown diamond certification`) relate to both HOD's blog article (`igi-certification-for-lab-grown-diamonds-what-it-means`) and its education article (`lab-grown-diamond-certification-explained-gia-vs-igi`) — the same duplication across `/blog/` and `/education/` that Stage 1 already flagged. Competitors present for these two keywords include `www.igi.org`, `www.gia.edu`, `stienhardt.com`, `www.plumdiamonds.com`, `www.whiteflash.com`, `washingtondiamond.com`.
- **Lab-grown vs. natural** (HOD's `lab-grown-vs-natural-diamonds-the-honest-comparison`): the exact-match keyword `lab grown vs natural diamonds` (volume 22,200) validates as a **COMPARISON**-dominant SERP led by `www.reddit.com`, `www.kay.com`, `www.brilliantearth.com`, `lioridiamonds.com`, `www.diamondmansion.com` — none of which is houseofdiams.com.
- **Diamond shapes** (HOD's `the-best-lab-grown-diamond-shapes-for-engagement-rings`): the keyword `diamond shape` (volume 60,500) validates EDITORIAL_GUIDE-dominant, led by `4cs.gia.edu`, `www.tiffany.com`, `www.brilliantearth.com`, `www.longsjewelers.com`, `www.bluenile.com` — none of which is houseofdiams.com.
- **4Cs** and **ring-sizing** (HOD's `the-4cs-of-lab-grown-diamonds-explained...` and `how-to-find-your-ring-size-at-home...`): **0 of the 100 validated keywords matched either topic by exact/near string** — these two existing HOD articles have no direct competitor evidence in this validated sample (a sampling gap, not evidence the topics lack competitors generally).

## 10. Limitations

- **This gap analysis is grounded only in the 100 keywords Stage 8 validated**, not the full 1,936-keyword master database. Extrapolating these findings to the other 1,836 keywords would not be evidence-based; a future stage would need its own SERP validation (or accept this as a representative-sample limitation) before relying on gap conclusions for keywords outside this 100.
- **Only the 91 domains that repeat across ≥2 of the 100 keywords were individually classified.** The 205 single-appearance domains are preserved in the landscape file as raw evidence but marked `UNKNOWN`/`NOT_ASSESSED` — classifying all 296 individually was judged disproportionate to this stage's purpose (identifying *repeat* competitors) and was not attempted rather than done with low confidence.
- **Competitor-type classification relies partly on general brand knowledge**, not a page-by-page audit of every domain's full business model; each classification's `classification_confidence` and `classification_note` disclose this, and 1 domain is honestly marked `UNKNOWN`.
- **Per-domain page type for organic ranks 6–10 is not available** — Stage 8's own page-type classifier only covered the top 5 per keyword; extending it to positions 6–10 without the same disclosed rigor was avoided, so those cells read `NOT_CLASSIFIED_BEYOND_TOP5` rather than a newly invented label.
- **`dominant_serp_page_type`, `validated_intent`, and `business_area` are all carried over unchanged from Stage 8** and inherit that stage's own disclosed limitations (24% of keywords labeled OTHER page type; 24% UNCLEAR intent; 38/100 UNCLASSIFIED_OR_UNKNOWN business area) — not re-derived or improved here.
- **Gap Type D/E rows are business-area aggregates**, not individual page recommendations — they describe an observed pattern (competitor page types present in an area) without asserting HOD should replicate it.
- Non-US domains occasionally appear in this US-location SERP pull (e.g. `regalhattongarden.co.uk`, `www.gsdiamonds.com.au`) — preserved as observed fact; not excluded or treated specially.

## 11. Was any additional paid DataForSEO call necessary?

**No.** Every requirement of this stage (competitor extraction, frequency, HOD-vs-competitor presence, keyword gaps, business-area coverage, page/topic patterns, existing-content cross-reference) was answerable from Stage 7/8 data already collected and paid for. No new DataForSEO endpoint — paid or free — was called this stage, and nothing was saved to `competitors/raw/` as a result (it remains empty, correctly, per the stage instruction that raw output is only saved "if — and only if — a paid or free DataForSEO endpoint is actually used").

## 12. Files produced

- `competitors/analysis/09_hod_competitor_landscape.csv` (795 rows — every domain × keyword organic appearance observed)
- `competitors/analysis/09_hod_competitor_frequency.csv` (91 rows — domains appearing for ≥2 of the 100 validated keywords)
- `competitors/analysis/09_hod_keyword_gap.csv` (643 rows — gap types A–E)
- `competitors/analysis/09_hod_competitor_landscape_summary.md` (this file)
