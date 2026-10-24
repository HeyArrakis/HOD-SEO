# 03 — SEO Implementation Priorities

Generated 2026-10-09. Derived from the master map (`01-…csv`). **Planning only — no website change has been made, and nothing here should be implemented without the AWS migration plan.** Each priority is split into **PRE-AWS PREPARATION**, **POST-AWS IMPLEMENTATION** and **POST-AWS VERIFICATION**.

**Rubric (no scores, no fake precision).** *Critical* = index-integrity or ranking-equity risk, a public statement that contradicts a confirmed HOD fact, a test artifact, or a MUST_PUBLISH time-critical calendar item. *High* = live commercial hubs/articles with clear metadata/ownership/duplication problems, empty indexable pages, high-intent calendar items. *Medium* = worthwhile optimization without integrity risk. *Low* = polish, conditional/deferred, low-value legacy.

**Counts:** CRITICAL 13, HIGH 64, MEDIUM 49, LOW 21 (total 147 rows).

## Top 10 priorities (cross-cutting order)

1. **Put the redirect map into the AWS migration plan.** All `/engagement-rings/by-desgin/*` URLs return 404; the Stage 15 keyword-owner URL for side-stone rings is among them. Add a 1:1 301 and keep intentional `/contact` (307) and `/hiphop` (308) behaviour. *(CRITICAL; prepare now, implement + verify after AWS.)*
2. **Take test, placeholder and empty pages out of the indexable set.** 18 pages (incl. `/hiphop/test-subcat`, `/collection`, `/engagement-rings/round-rings`, all `For Him` pages) are in the sitemap with 0 products — Stage 12 D-13 says none may be indexable. Decide noindex/sitemap exclusion vs populate.
3. **Correct the trust-critical copy.** /bespoke says '4-6 week typical lead time' (confirmed fact ≈3–4 weeks); /shipping shows placeholder text; /returns has no return terms; certification/shipping claims on home and bespoke need confirmation.
4. **Ratify commercial keyword ownership (D-19) from existing data.** No commercial hub or subcategory owns a ratified keyword. Candidate heads are already in the project datasets (CSV column *Primary Keyword*); decide hub-vs-child ownership and the unowned 135,000/mo 'lab grown diamonds' head (COM-LG-HUB).
5. **Replace boilerplate metadata and add unique hub copy.** 50 category/subcategory pages use 'Browse X in Y.' metas; homepage title has no brand and overlaps /engagement-rings (OV-13). Drafts are in the CSV.
6. **Update, never move, the ranking-equity articles.** CVD vs HPHT (19 ranked keywords), lab-grown vs natural, 14K vs 18K, how-to-choose: update in place, baseline GSC first, keep URL/H1 core terms.
7. **Resolve ownership items before writing the new Education pages.** 8 calendar items need ownership confirmation; 12 Education pages have different primary keywords in the Stage 19 brief vs the final calendar (see `04-…`).
8. **Unblock and sequence publishing.** 10 approved article packages exist; 6 dated items have passed with nothing live; 3 items are blocked on business facts. Confirm whether the CMS can publish during the AWS content freeze.
9. **Schema and entity clean-up at template level.** BreadcrumbList on articles, one author entity policy, retire boilerplate FAQPage on 35 pages (no rich result since 2026-05), enrich Organization (sameAs; founders once confirmed), keep Product/image URLs valid when hosts change.
10. **Capture baselines now, verify after cut-over.** GSC export (16 months), CrUX/PageSpeed for template URLs, TTFB baseline (1.2–4.5 s in this audit), indexed-page counts, sitemap/robots/canonical snapshots — then run the C-checklist after migration.

## Priority 1 — Critical

*Must address.* — 13 rows.


**Core Live** (1)

| ID | Page | Action | What / why |
|---|---|---|---|
| COM-BESPOKE | /bespoke | OPTIMIZE | OPTIMIZE: (1) CORRECT the lead-time claim: the page says '4-6 week typical lead time' but the confirmed HOD fact is 'typically 2–3 weeks to make + ~6–9 days delivery (~3–4 weeks), stone-dependent, ne… |

**Commercial Subcategory** (2)

| ID | Page | Action | What / why |
|---|---|---|---|
| /engagement-rings/by-design/side-stone-rings | /engagement-rings/by-design/side-stone-rings | OPTIMIZE | OPTIMIZE: Only subcategory that passes the D-07 gate and the Stage 15 keyword owner ('side stones engagement rings'); replace boilerplate meta, add unique intro; protect through the by-desgin → by-design URL change. |
| /hiphop/test-subcat | /hiphop/test-subcat | REVIEW | REVIEW: Test artifact ('test subcat') live in the sitemap — remove from sitemap and set noindex/delete (Stage 12 D-13). |

**Legacy / Redirect** (1)

| ID | Page | Action | What / why |
|---|---|---|---|
| LEG-ER-SIDESTONE | /engagement-rings/by-desgin/side-stone-rings | REDIRECT | REDIRECT: Add a 1:1 301 from /engagement-rings/by-desgin/side-stone-rings → /engagement-rings/by-design/side-stone-rings (and equivalent 301s for any other old /by-desgin/* URLs that were ever indexe… |

**Planned Education** (1)

| ID | Page | Action | What / why |
|---|---|---|---|
| EDU-LG-00 | /education/lab-grown-diamonds | CREATE | CREATE: Lab-grown diamonds pillar (MUST_PUBLISH 2026-10-21): resolve primary keyword ('synthetic diamonds' 2,900 in Stage 19 brief vs 'what are lab grown diamonds' 12,100 in the calendar) before writing; must not target the commercial head terms. |

**Planned Blog** (8)

| ID | Page | Action | What / why |
|---|---|---|---|
| BC-001 | /blog/how-long-does-a-custom-engagement-ring-take | CREATE | CREATE: how long does a custom engagement ring take (210/mo; KD 0) — LOCKED_CARRIED_FORWARD; calendar date 2026-10-04 [DATE PASSED, NOT LIVE] |
| BC-004 | /blog/christmas-jewelry-gifts-a-holiday-gift-guide | CREATE | CREATE: christmas jewelry gifts (390/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-10-05 [DATE PASSED, NOT LIVE] |
| BC-024 | How much should an engagement ring cost? Average prices, bu… | CREATE | CREATE: how much should an engagement ring cost (6600/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-10-23 |
| BC-016 | When is engagement season? Why so many proposals happen bet… | CREATE | CREATE: when is engagement season (170/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-10-26 |
| BC-017 | Christmas and New Year's Eve proposal ideas: festive ways t… | CREATE | CREATE: christmas proposal ideas (480/mo; KD 1) — LOCKED_CONFIRMED; calendar date 2026-10-27 |
| BC-019 | Is Black Friday a good time to buy an engagement ring? The… | CREATE | CREATE: best time to buy an engagement ring (210/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-10-30 |
| BC-031 | Engagement ring trends for 2027: toi et moi, east-west, bez… | CREATE | CREATE: engagement ring trends (1600/mo; KD 4) — LOCKED_CONFIRMED; calendar date 2026-12-01 |
| BC-034 | Valentine's Day proposal ideas: romantic ways to propose on… | CREATE | CREATE: valentines day proposal (720/mo; KD 26) — LOCKED_CONFIRMED; calendar date 2026-12-08 |

### PRE-AWS PREPARATION (A — safe to do now) — Critical

- draft/approve content, metadata, link plan — **8 row(s)** (BC-001, BC-004, BC-024, BC-016 … (+4))
- correct lead-time copy — **1 row(s)** (COM-BESPOKE)
- metadata drafts — **1 row(s)** (COM-BESPOKE)
- FAQ rewrite — **1 row(s)** (COM-BESPOKE)
- metadata/copy drafts — **1 row(s)** (/engagement-rings/by-design/side-stone-rings)
- decision memo — **1 row(s)** (/hiphop/test-subcat)
- redirect map entry (spreadsheet) — **1 row(s)** (LEG-ER-SIDESTONE)
- brief, draft, metadata, link plan — **1 row(s)** (EDU-LG-00)

### POST-AWS IMPLEMENTATION (B — wait for AWS) — Critical

- publish into CMS inside the migration-safe window (content-freeze plan UNKNOWN — VERIFY) — **9 row(s)** (EDU-LG-00, BC-001, BC-004, BC-024 … (+5))
- any template change — **1 row(s)** (COM-BESPOKE)
- template schema change — **1 row(s)** (/engagement-rings/by-design/side-stone-rings)
- noindex / sitemap rules / slug changes — **1 row(s)** (/hiphop/test-subcat)
- implement 301 in the AWS routing/edge config — DO NOT IMPLEMENT WITHOUT MIGRATION PLAN — **1 row(s)** (LEG-ER-SIDESTONE)

### POST-AWS VERIFICATION (C — verify after migration) — Critical

- URL live, canonical, indexability, schema, links, CWV — **8 row(s)** (BC-001, BC-004, BC-024, BC-016 … (+4))
- status, canonical, indexability, sitemap membership — **2 row(s)** (/engagement-rings/by-design/side-stone-rings, /hiphop/test-subcat)
- status/canonical/indexability, form submission still works — **1 row(s)** (COM-BESPOKE)
- 301 status, target 200, GSC URL inspection — **1 row(s)** (LEG-ER-SIDESTONE)
- URL live, canonical, indexability, schema, internal links, CWV — **1 row(s)** (EDU-LG-00)

## Priority 2 — High

*Important optimization.* — 64 rows.


**Core Live** (4)

| ID | Page | Action | What / why |
|---|---|---|---|
| NAV-HOME | / | OPTIMIZE | OPTIMIZE: (1) Add a short factual brand/entity intro (who, where, since when) using only confirmed facts — the FAQ already states a family-run manufacturer in Surat in the trade since 2014 and About… |
| COM-COLLECTION | /collection | REVIEW | REVIEW: Page renders '0 pieces / No pieces match your filters'. Decide: (a) noindex + remove from sitemap until it holds products, or (b) populate with a real curated collection and give it unique… |
| SUP-POLICIES-SHIP | /shipping | OPTIMIZE | OPTIMIZE: DEFECT: visible placeholder text 'new test black / test desc' on the live page. The visible body has no concrete timelines even though header badges promise 'Free Worldwide Insured Shipping… |
| SUP-POLICIES-RET | /returns | OPTIMIZE | OPTIMIZE: The visible body shows the 'Is House of Diams legitimate?' FAQ answer, a Quick Actions block and contact details but NO actual return terms (window, condition, bespoke exclusions, refund me… |

**Hubs** (1)

| ID | Page | Action | What / why |
|---|---|---|---|
| EDU-ROOT | /education | EXPAND | EXPAND: Hub lists 1 article today (GIA vs IGI) although 10 more Education-owned articles live at /blog. Per Stage 14 the root index should list the eight topic hubs (Lab-Grown, Natural, 4Cs, Shapes… |

**Commercial Category** (5)

| ID | Page | Action | What / why |
|---|---|---|---|
| COM-ER | /engagement-rings | OPTIMIZE | OPTIMIZE: Page is a product grid + generic 'Engagement Rings FAQ' (sitewide boilerplate, e.g. 'How is House of Diams different…'). Add unique intro (2–3 short paragraphs: styles, how to choose, lab-g… |
| COM-WB | /wedding-bands | OPTIMIZE | OPTIMIZE: Only 7 products are linked; 'for him' branch is empty. Add unique intro + links to the metals guides (EDU-MET-00/01) and ring-size guide (Stage 16 REQUIRED/RECOMMENDED). Do not publish a me… |
| COM-FJ-EARRINGS | /fine-jewellery/earrings | OPTIMIZE | OPTIMIZE: Product grid (24 per page, 5 child types listed as tabs) + boilerplate FAQ. Add short buying guidance with links to the 4Cs and metals pages (Stage 16 recommended) and to BC-025 when live.… |
| COM-FJ-NECKLACES | /fine-jewellery/necklaces | OPTIMIZE | OPTIMIZE: Add unique intro + link to the planned necklace-length chart (EDU-RJG-NL) and BC-006 when live. Hub currently lists 8 child types; 2 are empty (tennis necklace, initials). Products shown: ≥… |
| COM-ER-STYLES-GROUP | /engagement-rings/by-design | REVIEW | REVIEW: Do NOT merge or delete automatically. Options for the decision: (a) canonical → /engagement-rings and drop from sitemap; (b) 301 → /engagement-rings once the new hierarchy is chosen; (c) ke… |

**Commercial Subcategory** (16)

| ID | Page | Action | What / why |
|---|---|---|---|
| /engagement-rings/round-rings | /engagement-rings/round-rings | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: measured (candidate) ; SERP type: NOT validated; inventory: 0 produ… |
| /wedding-bands/for-him | /wedding-bands/for-him | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: measured (candidate) ; SERP type: NOT validated; inventory: 0 produ… |
| /wedding-bands/for-her/nature | /wedding-bands/for-her/nature | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: NOT measured; SERP type: NOT validated; inventory: 0 product links… |
| /wedding-bands/for-her/solid | /wedding-bands/for-her/solid | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: NOT measured; SERP type: NOT validated; inventory: 0 product links… |
| /wedding-bands/for-her/cigar-band | /wedding-bands/for-her/cigar-band | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: NOT measured; SERP type: NOT validated; inventory: 0 product links… |
| /wedding-bands/for-her/pavee | /wedding-bands/for-her/pavee | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: NOT measured; SERP type: NOT validated; inventory: 0 product links… |
| /wedding-bands/for-him/classic | /wedding-bands/for-him/classic | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: NOT measured; SERP type: NOT validated; inventory: 0 product links… |
| /wedding-bands/for-him/diamonds | /wedding-bands/for-him/diamonds | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: NOT measured; SERP type: NOT validated; inventory: 0 product links… |
| /wedding-bands/for-him/designer | /wedding-bands/for-him/designer | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: NOT measured; SERP type: NOT validated; inventory: 0 product links… |
| /fine-jewellery/earrings/tennis-earrings | /fine-jewellery/earrings/tennis-earrings | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: NOT measured; SERP type: NOT validated; inventory: 0 product links… |
| /fine-jewellery/earrings/personalized-charm | /fine-jewellery/earrings/personalized-charm | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: measured (candidate) ; SERP type: NOT validated; inventory: 0 produ… |
| /fine-jewellery/necklaces/tennis-necklace | /fine-jewellery/necklaces/tennis-necklace | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: measured (candidate) ; SERP type: NOT validated; inventory: 0 produ… |
| /fine-jewellery/necklaces/initials | /fine-jewellery/necklaces/initials | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: measured (candidate) ; SERP type: NOT validated; inventory: 0 produ… |
| /fine-jewellery/rings/eternity-rings | /fine-jewellery/rings/eternity-rings | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: measured (candidate) ; SERP type: NOT validated; inventory: 0 produ… |
| /hiphop/chains | /hiphop/chains | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: measured (candidate) ; SERP type: NOT validated; inventory: 0 produ… |
| /hiphop/chains/cuban-links | /hiphop/chains/cuban-links | REVIEW | REVIEW: EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. D-07 gate check — demand: measured (candidate) ; SERP type: NOT validated; inventory: 0 produ… |

**Product Pages** (1)

| ID | Page | Action | What / why |
|---|---|---|---|
| COM-PDP | /shop/<slug> | OPTIMIZE | OPTIMIZE: (1) Fix 6 placeholder-style metas and duplicate title/meta groups (list in 06-PDP-AUDIT-APPENDIX.csv). (2) Resolve the 'Gold Vermil' truncated material label visible on listings. (3) Varian… |

**Existing Articles (Education-Owned)** (7)

| ID | Page | Action | What / why |
|---|---|---|---|
| EDU-LG-03 | /blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams | OPTIMIZE | OPTIMIZE: Stage 13 decision: UPDATE_IN_PLACE — Education-owned evergreen comparison (Lab-Grown topic), kept at its current URL until the migration conditions are met. Calendar refresh 2027-01-21 (SCH… |
| EDU-LG-02 | /blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams | OPTIMIZE | OPTIMIZE: Stage 13 decision: UPDATE_IN_PLACE — Education-owned evergreen comparison (Lab-Grown topic; primary home for CL-011), kept at its current URL until the migration conditions are . Calendar r… |
| EDU-LG-01 | /blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide | OPTIMIZE | OPTIMIZE: Stage 13 decision: MOVE_TO_EDUCATION — Education evergreen explainer (Lab-Grown topic; primary home for CL-010 authenticity). Calendar refresh 2026-12-02 (SCHEDULED_REFRESH): Are lab-grown… |
| EDU-4C-00 | /blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat-house-of-diams | OPTIMIZE | OPTIMIZE: Stage 13 decision: MOVE_TO_EDUCATION — Education reference (Diamond Quality / 4Cs topic). Calendar refresh 2026-12-10 (SCHEDULED_REFRESH): The 4Cs of diamonds: cut, colour, clarity and cara… |
| EDU-SHP-00 | /blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of-diams | OPTIMIZE | OPTIMIZE: Stage 13 decision: MOVE_TO_EDUCATION — Education reference (Diamond Shapes & Cuts topic). Calendar refresh 2026-11-13 (SCHEDULED_REFRESH): Diamond shapes guide: the 10 main shapes, a shape… |
| EDU-RJG-02 | /blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams | OPTIMIZE | OPTIMIZE: Stage 13 decision: MOVE_TO_EDUCATION — Education practical guide (Ring & Jewellery Guides); possibly a TOOL page. Calendar refresh 2026-11-12 (SCHEDULED_REFRESH): Ring size guide: ring size… |
| EDU-CERT-00 | /blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of-diams | OPTIMIZE | OPTIMIZE: Stage 13 decision: RETARGET — Education certification explainer for a non-comparison intent (general lab-grown certification or IGI report), no longer competing with the . Calendar refresh… |

**Planned Education** (11)

| ID | Page | Action | What / why |
|---|---|---|---|
| EDU-LG-09 | Detecting lab-grown diamonds (testers & identification) | REVIEW | REVIEW: do lab grown diamonds pass a diamond tester — SCHEDULED_NEW; calendar date 2026-11-30 |
| EDU-4C-01 | /education/diamond-4cs/diamond-clarity | CREATE | CREATE: diamond clarity grading scale — SCHEDULED_NEW; calendar date 2026-11-11 |
| EDU-4C-03 | /education/diamond-4cs/vvs-diamonds | CREATE | CREATE: v v s diamond — SCHEDULED_NEW; calendar date 2026-11-20 |
| EDU-4C-05 | /education/diamond-4cs/diamond-color | CREATE | CREATE: color grade diamond — SCHEDULED_NEW; calendar date 2026-11-16 |
| EDU-4C-06 | /education/diamond-4cs/diamond-cut | CREATE | CREATE: diamond cut grade — SCHEDULED_NEW; calendar date 2026-11-17 |
| EDU-4C-07 | Diamond carat guide | CREATE | CREATE: is 1 carat diamond good — SCHEDULED_NEW; calendar date 2026-11-19 |
| EDU-MET-00 | Jewelry metals guide (Metals hub pillar) | CREATE | CREATE: types of jewelry metals — SCHEDULED_NEW; calendar date 2026-11-24 |
| EDU-RJG-01 | Ring settings guide | REVIEW | REVIEW: types of diamond settings — SCHEDULED_NEW; calendar date 2027-01-04 |
| EDU-RJG-BR | Bracelet size chart (planned Education practical guide) | REVIEW | REVIEW: bracelet size chart — SCHEDULED_NEW; calendar date 2026-10-28 |
| EDU-RJG-NL | Necklace length chart (planned Education practical guide) | REVIEW | REVIEW: necklace length chart — SCHEDULED_NEW; calendar date 2026-11-04 |
| EDU-WB-GUIDE | How to choose a wedding band (planned Education buying guid… | REVIEW | REVIEW: how to choose a wedding band — SCHEDULED_NEW; calendar date 2027-01-11 |

**Conditional Commercial** (1)

| ID | Page | Action | What / why |
|---|---|---|---|
| COM-LG-HUB | Lab-Grown Diamonds — commercial hub (COM-LG-HUB) | REVIEW | REVIEW: Business decision needed: confirm the catalogue is lab-grown (all PDP copy says so) and whether to activate this hub (a curated collection page listing products with origin/certification fa… |

**Planned Blog** (18)

| ID | Page | Action | What / why |
|---|---|---|---|
| BC-035 | /blog/10-year-anniversary-gift-ideas-tin-and-diamond | CREATE | CREATE: 10 year anniversary gift (33100/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-10-06 [DATE PASSED, NOT LIVE] |
| BC-018 | /blog/anniversary-gifts-by-year-traditional-and-modern | CREATE | CREATE: anniversary gifts by year (74000/mo; KD 11) — LOCKED_CARRIED_FORWARD; calendar date 2026-10-07 [DATE PASSED, NOT LIVE] |
| BC-036 | /blog/what-finger-does-a-wedding-ring-go-on | CREATE | CREATE: what finger does a wedding ring go on (27100/mo; KD 1) — LOCKED_CONFIRMED; calendar date 2026-10-08 [DATE PASSED, NOT LIVE] |
| BC-006 | /blog/necklace-layering-how-to-layer-necklaces | CREATE | CREATE: necklace layering (14800/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-10-09 [DATE PASSED, NOT LIVE] |
| BC-003 | /blog/push-present-what-it-is-and-jewelry-ideas | CREATE | CREATE: push present (18100/mo; KD 0) — LOCKED_CARRIED_FORWARD; calendar date 2026-10-14 |
| BC-007 | /blog/how-to-wear-an-engagement-ring-and-wedding-band | CREATE | CREATE: how to wear engagement ring and wedding band (3600/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-10-15 |
| BC-011 | What is a promise ring? Meaning, who gives one, and how it… | CREATE | CREATE: what is a promise ring (22200/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-10-16 |
| BC-037 | Engagement ring vs wedding ring: what is the difference (an… | CREATE | CREATE: engagement ring vs wedding ring (18100/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-10-19 |
| BC-014 | Proposal ideas: how to plan a proposal she will remember (w… | CREATE | CREATE: proposal ideas (14800/mo; KD 9) — LOCKED_CONFIRMED; calendar date 2026-10-20 |
| BC-015 | Where are lab-grown diamonds made? Surat, India, China and… | BLOCKED | BLOCKED: where are lab grown diamonds made (210/mo; KD 30) — LOCKED_CONFIRMED; calendar date 2026-10-22 |
| BC-005 | How diamonds are cut and polished: the five steps inside a… | BLOCKED | BLOCKED: how diamonds are cut (1900/mo; KD 18) — LOCKED_CONFIRMED; calendar date 2026-10-29 |
| BC-021 | What is a tennis bracelet? Why it is called that, and how t… | CREATE | CREATE: what is a tennis bracelet (3600/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-11-02 |
| BC-039 | What finger does a promise ring go on? Placement, hand and… | CREATE | CREATE: what finger does a promise ring go on (12100/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-11-03 |
| BC-022 | How to stack rings: engagement ring, wedding band and etern… | CREATE | CREATE: how to stack rings (590/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-11-05 |
| BC-038 | Ring finger meaning: what a ring on each finger symbolises… | CREATE | CREATE: ring finger meaning (9900/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-11-06 |
| BC-025 | Different types of earrings: studs, huggies, hoops and drop… | CREATE | CREATE: different types of earrings (1600/mo; KD 0) — LOCKED_CONFIRMED; calendar date 2026-11-10 |
| BC-032 | Fine jewelry trends for 2027: diamond earrings, bracelets a… | CREATE | CREATE: jewelry trends (2900/mo; KD 34) — LOCKED_CONFIRMED; calendar date 2026-12-03 |
| BLOG-WR-TYPES | Types of wedding rings: wedding band styles explained (clas… | REVIEW | REVIEW: types of wedding rings (12100/mo; KD 0) — SCHEDULED_NEW; calendar date 2026-12-04 |

### PRE-AWS PREPARATION (A — safe to do now) — High

- decision memo — **19 row(s)** (COM-COLLECTION, COM-ER-STYLES-GROUP, /engagement-rings/round-rings, /wedding-bands/for-him … (+15))
- draft/approve content, metadata, link plan — **18 row(s)** (BC-035, BC-018, BC-036, BC-006 … (+14))
- brief, draft, metadata, link plan — **11 row(s)** (EDU-LG-09, EDU-4C-01, EDU-4C-03, EDU-4C-05 … (+7))
- metadata + content update drafts (Stage 19 brief) — **7 row(s)** (EDU-LG-03, EDU-LG-02, EDU-LG-01, EDU-4C-00 … (+3))
- link additions — **7 row(s)** (EDU-LG-03, EDU-LG-02, EDU-LG-01, EDU-4C-00 … (+3))
- link plan — **5 row(s)** (NAV-HOME, COM-ER, COM-WB, COM-FJ-EARRINGS … (+1))
- metadata + intro-copy drafts — **4 row(s)** (COM-ER, COM-WB, COM-FJ-EARRINGS, COM-FJ-NECKLACES)
- keyword-ratification memo (reuse existing data) — **4 row(s)** (COM-ER, COM-WB, COM-FJ-EARRINGS, COM-FJ-NECKLACES)
- metadata drafts — **1 row(s)** (NAV-HOME)
- intro copy — **1 row(s)** (NAV-HOME)
- claim verification list — **1 row(s)** (NAV-HOME)
- copy/facts, placeholder removal — **1 row(s)** (SUP-POLICIES-SHIP)
- copy/facts — **1 row(s)** (SUP-POLICIES-RET)
- hub listing plan — **1 row(s)** (EDU-ROOT)

### POST-AWS IMPLEMENTATION (B — wait for AWS) — High

- publish into CMS inside the migration-safe window (content-freeze plan UNKNOWN — VERIFY) — **29 row(s)** (EDU-LG-09, EDU-4C-01, EDU-4C-03, EDU-4C-05 … (+25))
- noindex / sitemap rules / slug changes — **16 row(s)** (/engagement-rings/round-rings, /wedding-bands/for-him, /wedding-bands/for-her/nature, /wedding-bands/for-her/solid … (+12))
- BreadcrumbList/author schema template — **7 row(s)** (EDU-LG-03, EDU-LG-02, EDU-LG-01, EDU-4C-00 … (+3))
- any URL move — **7 row(s)** (EDU-LG-03, EDU-LG-02, EDU-LG-01, EDU-4C-00 … (+3))
- schema/template changes — **4 row(s)** (COM-ER, COM-WB, COM-FJ-EARRINGS, COM-FJ-NECKLACES)
- schema template — **2 row(s)** (SUP-POLICIES-SHIP, SUP-POLICIES-RET)
- Organization/WebSite schema edits (template) — **1 row(s)** (NAV-HOME)
- noindex / sitemap exclusion — **1 row(s)** (COM-COLLECTION)
- template: hub listing logic, H2 bug — **1 row(s)** (EDU-ROOT)
- canonical/redirect/sitemap change — **1 row(s)** (COM-ER-STYLES-GROUP)
- schema/spec-block template; image URL changes; variant redirects — **1 row(s)** (COM-PDP)
- page build — **1 row(s)** (COM-LG-HUB)

### POST-AWS VERIFICATION (C — verify after migration) — High

- URL live, canonical, indexability, schema, links, CWV — **18 row(s)** (BC-035, BC-018, BC-036, BC-006 … (+14))
- status, canonical, indexability, sitemap membership — **16 row(s)** (/engagement-rings/round-rings, /wedding-bands/for-him, /wedding-bands/for-her/nature, /wedding-bands/for-her/solid … (+12))
- URL live, canonical, indexability, schema, internal links, CWV — **11 row(s)** (EDU-LG-09, EDU-4C-01, EDU-4C-03, EDU-4C-05 … (+7))
- canonical, indexability, schema, CWV, internal links render — **7 row(s)** (EDU-LG-03, EDU-LG-02, EDU-LG-01, EDU-4C-00 … (+3))
- canonical, indexability, sitemap membership, status, CWV baseline — **4 row(s)** (COM-ER, COM-WB, COM-FJ-EARRINGS, COM-FJ-NECKLACES)
- status, canonical — **2 row(s)** (SUP-POLICIES-SHIP, SUP-POLICIES-RET)
- canonical, indexability, 200 status, US-visitor rendering, CWV baseline — **1 row(s)** (NAV-HOME)
- status, indexability, sitemap membership — **1 row(s)** (COM-COLLECTION)
- canonical, links to hubs, sitemap — **1 row(s)** (EDU-ROOT)
- canonical, sitemap, status — **1 row(s)** (COM-ER-STYLES-GROUP)
- Product schema validity, image URLs resolve, canonical, price/availability, CWV — **1 row(s)** (COM-PDP)
- n/a until built — **1 row(s)** (COM-LG-HUB)

## Priority 3 — Medium

*Useful improvements.* — 49 rows.


**Core Live** (4): `/shop` (OPTIMIZE); `/about` (OPTIMIZE); `/contact` (REVIEW); `/faq` (OPTIMIZE)

**Hubs** (1): `/blog` (OPTIMIZE)

**Commercial Category** (4): `/fine-jewellery` (OPTIMIZE); `/fine-jewellery/bracelet` (OPTIMIZE); `/fine-jewellery/rings` (REVIEW); `/t-bar` (REVIEW)

**Commercial Subcategory** (22): `/engagement-rings/by-design/solitare-rings` (OPTIMIZE); `/engagement-rings/by-design/halo-ring` (OPTIMIZE); `/engagement-rings/by-design/toi-moi-rings` (OPTIMIZE); `/engagement-rings/by-design/pave` (OPTIMIZE); `/engagement-rings/by-design/nature-inspired-rings` (OPTIMIZE); `/engagement-rings/by-design/three-stone-rings` (OPTIMIZE); `/engagement-rings/by-design/bezel-rings` (OPTIMIZE); `/wedding-bands/for-her` (OPTIMIZE); `/wedding-bands/for-her/eternity` (OPTIMIZE); `/wedding-bands/for-her/anniversay` (OPTIMIZE); `/fine-jewellery/earrings/stud-earrings` (OPTIMIZE); `/fine-jewellery/earrings/hoops-huggies` (OPTIMIZE); `/fine-jewellery/earrings/drop-dangle` (OPTIMIZE); `/fine-jewellery/necklaces/solitare` (OPTIMIZE); `/fine-jewellery/necklaces/pendant-necklace` (OPTIMIZE); `/fine-jewellery/necklaces/charm-necklace` (OPTIMIZE); `/fine-jewellery/necklaces/multi-stone` (OPTIMIZE); `/fine-jewellery/necklaces/lariat-necklace` (OPTIMIZE); `/fine-jewellery/necklaces/toi-et-moi` (OPTIMIZE); `/fine-jewellery/bracelet/tennis` (OPTIMIZE); `/fine-jewellery/bracelet/bangles` (OPTIMIZE); `/fine-jewellery/bracelet/chain-link` (OPTIMIZE)

**Product Pages** (1): `/shop/oval-floral-diamond-ring` (OPTIMIZE)

**Existing Articles (Education-Owned)** (4): `/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams` (OPTIMIZE); `/blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide` (OPTIMIZE); `/blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-of-diams` (REVIEW); `/education/lab-grown-diamond-certification-explained-gia-vs-igi-house-of-diams` (OPTIMIZE)

**Legacy / Redirect** (1): `/hiphop` (REVIEW)

**Planned Education** (6): `EDU-LG-05` (CREATE); `EDU-NAT-00` (CREATE); `/education/diamond-4cs/si-clarity-diamonds` (CREATE); `EDU-GEN-01` (CREATE); `EDU-RJG-03` (REVIEW); `EDU-INS` (REVIEW)

**Conditional Education** (1): `EDU-RJG-00` (CREATE)

**Planned Blog** (5): `/blog/meaningful-jewelry-gifts-for-your-wife` (CREATE); `/blog/jewelry-gifts-for-your-girlfriend-diamond-ideas` (CREATE); `BC-023` (CREATE); `BLOG-WB-BUYS` (CREATE); `BLOG-NPD` (CREATE)

### PRE-AWS PREPARATION (A — safe to do now) — Medium

- metadata/copy drafts — **23 row(s)** (COM-SHOP, /engagement-rings/by-design/solitare-rings, /engagement-rings/by-design/halo-ring, /engagement-rings/by-design/toi-moi-rings … (+19))
- link plan — **6 row(s)** (COM-SHOP, SUP-FAQ, COM-FJ, COM-FJ-BRACELETS … (+2))
- brief, draft, metadata, link plan — **6 row(s)** (EDU-LG-05, EDU-NAT-00, EDU-4C-02, EDU-GEN-01 … (+2))
- draft/approve content, metadata, link plan — **5 row(s)** (BC-008, BC-009, BC-023, BLOG-WB-BUYS … (+1))
- metadata + intro-copy drafts — **4 row(s)** (COM-FJ, COM-FJ-BRACELETS, COM-FJ-RINGS, COM-CURATED-TBAR)
- keyword-ratification memo (reuse existing data) — **4 row(s)** (COM-FJ, COM-FJ-BRACELETS, COM-FJ-RINGS, COM-CURATED-TBAR)
- metadata + content update drafts (Stage 19 brief) — **4 row(s)** (EDU-MET-01, EDU-LG-10, EXIST-BLOG-ER-ONLINE, EDU-CERT-01)
- link additions — **4 row(s)** (EDU-MET-01, EDU-LG-10, EXIST-BLOG-ER-ONLINE, EDU-CERT-01)
- decision memo — **2 row(s)** (BRAND-CONTACT, COM-HIPHOP)
- metadata drafts — **2 row(s)** (BLOG-HUB, COM-PDP-OVAL-FLORAL)
- copy + metadata drafts — **1 row(s)** (BRAND-ABOUT)
- fact confirmation — **1 row(s)** (BRAND-ABOUT)
- copy edits — **1 row(s)** (SUP-FAQ)
- naming decision — **1 row(s)** (BLOG-HUB)

### POST-AWS IMPLEMENTATION (B — wait for AWS) — Medium

- template schema change — **19 row(s)** (/engagement-rings/by-design/halo-ring, /engagement-rings/by-design/toi-moi-rings, /engagement-rings/by-design/pave, /engagement-rings/by-design/nature-inspired-rings … (+15))
- publish into CMS inside the migration-safe window (content-freeze plan UNKNOWN — VERIFY) — **11 row(s)** (EDU-LG-05, EDU-NAT-00, EDU-4C-02, EDU-GEN-01 … (+7))
- schema/template changes — **4 row(s)** (COM-FJ, COM-FJ-BRACELETS, COM-FJ-RINGS, COM-CURATED-TBAR)
- BreadcrumbList/author schema template — **4 row(s)** (EDU-MET-01, EDU-LG-10, EXIST-BLOG-ER-ONLINE, EDU-CERT-01)
- any URL move — **4 row(s)** (EDU-MET-01, EDU-LG-10, EXIST-BLOG-ER-ONLINE, EDU-CERT-01)
- noindex / sitemap rules / slug changes — **3 row(s)** (/engagement-rings/by-design/solitare-rings, /wedding-bands/for-her/anniversay, /fine-jewellery/necklaces/solitare)
- pagination title template — **1 row(s)** (COM-SHOP)
- schema template — **1 row(s)** (BRAND-ABOUT)
- contact page build/keep decision — **1 row(s)** (BRAND-CONTACT)
- schema decision (template) — **1 row(s)** (SUP-FAQ)
- pagination canonical / category pages — **1 row(s)** (BLOG-HUB)
- none — **1 row(s)** (COM-PDP-OVAL-FLORAL)
- child-page cleanup — **1 row(s)** (COM-HIPHOP)

### POST-AWS VERIFICATION (C — verify after migration) — Medium

- status, canonical, indexability, sitemap membership — **22 row(s)** (/engagement-rings/by-design/solitare-rings, /engagement-rings/by-design/halo-ring, /engagement-rings/by-design/toi-moi-rings, /engagement-rings/by-design/pave … (+18))
- URL live, canonical, indexability, schema, internal links, CWV — **6 row(s)** (EDU-LG-05, EDU-NAT-00, EDU-4C-02, EDU-GEN-01 … (+2))
- URL live, canonical, indexability, schema, links, CWV — **5 row(s)** (BC-008, BC-009, BC-023, BLOG-WB-BUYS … (+1))
- canonical, indexability, sitemap membership, status, CWV baseline — **4 row(s)** (COM-FJ, COM-FJ-BRACELETS, COM-FJ-RINGS, COM-CURATED-TBAR)
- canonical, indexability, schema, CWV, internal links render — **4 row(s)** (EDU-MET-01, EDU-LG-10, EXIST-BLOG-ER-ONLINE, EDU-CERT-01)
- canonical, status — **2 row(s)** (BRAND-ABOUT, SUP-FAQ)
- canonical + noindex on parameters, sitemap inclusion, product count, CWV — **1 row(s)** (COM-SHOP)
- redirect type and target, sitemap — **1 row(s)** (BRAND-CONTACT)
- canonical on ?page=N, sitemap, status — **1 row(s)** (BLOG-HUB)
- status, canonical, schema — **1 row(s)** (COM-PDP-OVAL-FLORAL)
- redirect type/target — **1 row(s)** (COM-HIPHOP)

## Priority 4 — Low

*Polish / future work.* — 21 rows.


**Core Live** (2): `/privacy-policy` (NO ACTION); `/terms` (NO ACTION)

**Legacy / Redirect** (3): `/engagement-rings/by-desgin` (REDIRECT); `/shop/fine-jewellery-test-product` (NO ACTION); `/shop/marquise-floral-diamond-engagement-ring` (REVIEW)

**Planned Education** (2): `EDU-LG-07` (CREATE); `EDU-LG-08` (CREATE)

**Conditional Education** (12): `EDU-LG-04` (REVIEW); `EDU-LG-06` (REVIEW); `EDU-NAT-01` (REVIEW); `EDU-NAT-02` (REVIEW); `EDU-4C-04` (REVIEW); `EDU-4C-08` (REVIEW); `EDU-CERT-02` (REVIEW); `EDU-MET-02` (REVIEW); `EDU-GEM-00` (REVIEW); `EDU-GEM-01` (REVIEW); `EDU-GEM-02` (REVIEW); `EDU-GEN-02` (REVIEW)

**Planned Blog** (2): `BLOG-ER-HISTORY` (CREATE); `BLOG-WR-HISTORY` (CREATE)

### PRE-AWS PREPARATION (A — safe to do now) — Low

- none — **16 row(s)** (SUP-POLICIES-PRIV, SUP-POLICIES-TERMS, LEG-fine-jewellery-test-product, LEG-marquise-floral-diamond-engage … (+12))
- brief, draft, metadata, link plan — **2 row(s)** (EDU-LG-07, EDU-LG-08)
- draft/approve content, metadata, link plan — **2 row(s)** (BLOG-ER-HISTORY, BLOG-WR-HISTORY)
- redirect map entry — **1 row(s)** (LEG-ER-GROUP)

### POST-AWS IMPLEMENTATION (B — wait for AWS) — Low

- publish into CMS inside the migration-safe window (content-freeze plan UNKNOWN — VERIFY) — **4 row(s)** (EDU-LG-07, EDU-LG-08, BLOG-ER-HISTORY, BLOG-WR-HISTORY)
- implement 301 — **1 row(s)** (LEG-ER-GROUP)

### POST-AWS VERIFICATION (C — verify after migration) — Low

- status — **3 row(s)** (LEG-ER-GROUP, LEG-fine-jewellery-test-product, LEG-marquise-floral-diamond-engage)
- status, canonical after migration — **2 row(s)** (SUP-POLICIES-PRIV, SUP-POLICIES-TERMS)
- URL live, canonical, indexability, schema, internal links, CWV — **2 row(s)** (EDU-LG-07, EDU-LG-08)
- URL live, canonical, indexability, schema, links, CWV — **2 row(s)** (BLOG-ER-HISTORY, BLOG-WR-HISTORY)

## Items needing a human decision before they can be prioritised further

48 rows are `REVIEW` or `BLOCKED` (decision, ownership confirmation or business fact needed). By group: COMMERCIAL SUBCATEGORY 17, CONDITIONAL EDUCATION 12, PLANNED EDUCATION 7, COMMERCIAL CATEGORY 3, PLANNED BLOG 3, CORE LIVE 2, LEGACY / REDIRECT 2, EXISTING ARTICLES (Education-owned) 1, CONDITIONAL COMMERCIAL 1.
