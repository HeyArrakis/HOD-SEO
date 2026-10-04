# Stage 10 — Existing Content & Blog Equity Analysis

Date: 2026-09-24
Scope: evidence only. This stage makes no retain/improve/merge/retire decisions, recommends no URLs, redirects, deletions or new pages, and does no clustering. Those decisions belong to later stages.

**Stage 10 completed with $0 additional DataForSEO spend.** No DataForSEO endpoint, paid or free, was called.

---

## 0. How to read the evidence

| Label | What it is | What it is not |
|---|---|---|
| **Stage 3** | A DataForSEO Labs `ranked_keywords/live` snapshot for houseofdiams.com in the US in English. Keyword data is dated Aug–Sep 2026 and the project pulled it on 2026-09-17. | Not a live Google rank. Not GSC data. |
| **Stage 8** | Google SERPs observed by DataForSEO on 2026-09-17 for 100 keywords (US/en, desktop, depth 10). Page type and intent were assigned by a disclosed rule-based heuristic. | Not a manual audit. Only 100 of 1,936 master keywords were checked. |
| **Stage 9** | Competitor data re-parsed from the raw Stage 8 SERPs. Only the 91 domains that repeat were classified. | Not a separate data pull. |
| **Topic string-match** (new here) | A Stage 10 regex heuristic that links master keywords to the subject of an existing page. The patterns are in the script logic described in §9. | **Not a keyword-to-URL assignment**, and not evidence that the page ranks. |
| **Nav check** (new here) | Read-only HTTP GETs of the live site on 2026-09-24, used to verify URLs. | Not a crawl, and not a CMS or site change. |

Where this stage found **"no evidence"**, it means nothing turned up in the project datasets. It does **not** mean the thing is absent from the site or from Google.

---

## 1. What was analyzed

| Group | Count | Source |
|---|---|---|
| Blog articles | **10** | Stage 1 blog inventory (all 10) |
| Education articles | **1** | Stage 1 content inventory |
| Blog hub and Education hub | 2 | Stage 1 |
| Category, listing, service and brand pages from the sitemap | 16 | Home, /shop, /collection, /engagement-rings, /wedding-bands, /fine-jewellery, /t-bar, /hiphop, /bespoke, /faq, /about, /contact, /shipping, /returns, /privacy-policy, /terms |
| Product page with a Stage 3 ranking | 1 | /shop/oval-floral-diamond-ring |
| **Subcategory pages that are in the site nav but not in the sitemap** | **41** | Stage 10 nav check (see §1a) |
| **Total rows in `10_existing_content_inventory.csv`** | **71** | |

The other 168 product pages are out of scope because they have no ranking or content evidence. They are still recorded in Stage 1.

### 1a. New finding: Stage 1's inventory missed a layer of subcategory URLs

Stage 3 records a ranking on `/engagement-rings/by-desgin/side-stone-rings`. That URL is **not in `sitemap.xml`**, so Stage 1 never inventoried it. Stage 10 checked it and found:

- It is live (HTTP 200, self-referencing canonical, no meta robots).
- The main category pages link to **41 subcategory URLs**, and none of them are in the sitemap:
  - `/engagement-rings/by-desgin/*` (9)
  - `/wedding-bands/for-her|for-him/*` (11)
  - `/fine-jewellery/earrings/*` (6)
  - `/fine-jewellery/necklaces/*` (9)
  - `/fine-jewellery/bracelet/*` (4)
  - `/fine-jewellery/rings/*` (2)
- All 41 returned HTTP 200 and have a self-referencing canonical, no meta robots, and a template meta description ("Browse {X} in {Parent}.").
- **13 of the 41 showed "No pieces match" (they look empty):**
  - Earrings: personalized-charm, tennis-earrings
  - Necklaces: initials, tennis-necklace
  - Rings: eternity-rings
  - Wedding bands for her: cigar-band, nature, pavee, solid
  - Wedding bands for him: the hub, classic, designer, diamonds
- Several slugs are misspelled as live: `by-desgin`, `solitare`, `anniversay`, `pavee`.

**This corrects a Stage 1 statement.** Stage 1 said "No dedicated category URL exists yet for earrings, necklaces/pendants, or bracelets." In fact these URLs do exist: `/fine-jewellery/earrings`, `/fine-jewellery/necklaces` and `/fine-jewellery/bracelet`. They are simply not in the sitemap. The Stage 1 files were not edited; the correction is recorded here and in `decision-log.md`.

---

## 2. Content → keyword coverage (Part 2)

Source: `10_content_keyword_coverage.csv`, 389 rows. It holds three kinds of rows:

- 28 `STAGE3_RANKS` rows
- 313 `TOPIC_STRING_MATCH_ONLY` rows
- 48 `NO_EXISTING_CONTENT_MATCH` rows (Stage 8 keywords that match no existing page)

Only **6 URLs** have any Stage 3 ranking keyword. All 28 Stage 3 keywords map to exactly one URL each.

| URL | Stage 3 keywords | Best position (keyword) | Highest-volume keywords | Intent (DataForSEO → Stage 8 validated) | SERP-validated in Stage 8 |
|---|---|---|---|---|---|
| /blog/cvd-vs-hpht-lab-grown-diamonds-… | **19** | 27 (*are cvd diamonds real*, vol 30) | *hpht lab grown diamonds* / *diamond* (8,100 each, pos 49); *hpht vs cvd* (720, pos 54) | DataForSEO: mixed info/commercial/transactional. Stage 8: 16 INFORMATIONAL, 1 TRANSACTIONAL, 1 MIXED, 1 UNCLEAR | 19/19 |
| /blog/lab-grown-vs-natural-diamonds-… | 3 | 29 (*which is better lab grown diamonds or natural diamonds*, 30) | all vol 20–30 | Stage 8: 2 INFORMATIONAL, 1 UNCLEAR | 3/3 |
| /blog/14k-vs-18k-gold-… | 3 | 81 (*which one is better 14k or 18k gold*, 20) | all vol 20–30 | Stage 8: 3 INFORMATIONAL | 3/3 |
| /blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide | 1 | 35 (*how to choose a lab grown diamond*, 30) | same keyword | Stage 8: INFORMATIONAL | 1/1 |
| /shop/oval-floral-diamond-ring (PDP; live title "Oval Marquise Side-Stone Engagement Ring") | 1 | 90 (*marquise oval diamond*, 390) | same keyword | Stage 8: TRANSACTIONAL | 1/1 |
| /engagement-rings/by-desgin/side-stone-rings (not in sitemap) | 1 | 104 (*side stones engagement rings*, 1,000) | same keyword | Stage 8: TRANSACTIONAL | 1/1 |

The following have **no Stage 3 ranking keyword**:

- 6 of the 10 blog articles: are-real, 4Cs, engagement-ring-online, shapes, ring-size, IGI certification
- The education article
- Both hubs
- All sitemap category, service and brand pages
- 40 of the 41 nav subcategories

Coverage by articles is lopsided: 26 of the 28 Stage 3 rankings sit on 4 blog articles, and none sit on the education section.

---

## 3. Existing content equity: the measurable evidence (Part 3)

Source: `10_content_equity_analysis.csv` (71 rows). This section has no score, tier or ranking. It lists the facts only.

**URLs with measurable ranking equity in project data (Stage 3):**

1. **The CVD vs HPHT blog article**
   - 19 keywords at positions 27–68. By band: 1 in 21–30, 14 in 31–50, and 4 in 51–100.
   - These keywords are one related query family (CVD/HPHT variants), all repeatedly pointing at this single URL.
   - Their summed volume is 17,380, but most of that is two near-duplicate keywords (*hpht lab grown diamond(s)*, 8,100 each). Summed volume double-counts this kind of variant.
   - All 19 were SERP-validated. HOD appeared in 0 of those top-10 SERPs.
   - Stage 9 found the same topic covered by ritani, regalhattongarden, miadonna, lgdusallc, stienhardt and gia.edu, mostly in editorial-guide format.
2. **The lab-grown vs natural blog article.** 3 keywords at positions 29–40, volume 20–30 each, all validated. The exact-match head term *lab grown vs natural diamonds* (22,200) is not among HOD's rankings.
3. **The 14K vs 18K gold blog article.** 3 keywords at positions 81–95, volume 20–30 each, all validated.
4. **The how-to-choose buyer's guide.** 1 keyword at position 35, volume 30.
5. **The oval marquise PDP.** 1 keyword at position 90, volume 390.
6. **The side-stone subcategory.** 1 keyword at position 104, volume 1,000.

**What the evidence shows:**

- Every known ranking is position 27 or lower, so there is no page-1 or page-2 presence.
- HOD was observed in **0 of 795** organic results across the 100 Stage 8 SERPs.
- The only URL with rankings across a family of related queries is the CVD/HPHT article.

**Evidence that does not exist in the project** (so equity cannot be fully judged):

- No GSC clicks or impressions
- No backlink or referring-domain data
- No internal-link counts
- No word counts or content-quality audit
- No index-coverage status (only meta robots was observed)
- No rank data deeper than depth 10 beyond the single Stage 3 snapshot

If no ranking is on record for a page, that does not prove it has zero visibility.

---

## 4. Overlap between existing pages (Part 4)

Source: `10_content_overlap_analysis.csv` (18 pairs). Result: **1 CLEAR_OVERLAP, 11 POSSIBLE_OVERLAP, 6 DISTINCT.**

In every one of the 18 pairs, cannibalization is **not proven**: Stage 3 has no keyword for which more than one HOD URL ranks.

| ID | Pages | Class | Key evidence |
|---|---|---|---|
| OV-01 | IGI certification blog ↔ GIA-vs-IGI education article | **CLEAR_OVERLAP** | Same subject, business area and informational intent, split across /blog and /education. Both match the same 58 certification master keywords. Neither ranks. The two validated certification SERPs (*gia vs igi lab diamond*, *lab-grown diamond certification*) share 0 top-10 URLs. No IGI-only keyword was validated. **Topic overlap is confirmed; harmful cannibalization is not demonstrated.** |
| OV-02 | are-real ↔ lab-vs-natural | POSSIBLE | Both validated SERPs are COMPARISON-dominant. They share 1 URL and 4 domains (reddit, brilliantearth, kay, youtube). The keyword families are disjoint. |
| OV-03 | are-real ↔ CVD vs HPHT | POSSIBLE | *are cvd diamonds real* ranks on the **CVD** article (position 27, its best), not on the legitimacy article. Its SERP shares 1 URL and 3 domains with *are lab grown diamonds real*. |
| OV-04 | CVD vs HPHT ↔ lab-vs-natural | DISTINCT | Ranking sets are disjoint. The SERPs share 0 URLs. |
| OV-05 | how-to-choose ↔ are-real | DISTINCT | Both titles say "Complete Buyer's Guide", but the SERPs share 0 URLs. |
| OV-06/07/08 | how-to-choose ↔ engagement-ring-online ↔ 4Cs | POSSIBLE | This is the 3-way buying-guide overlap Stage 1 found at content level. The only measured SERP pair shares nothing. No ring-buying-guide keyword was validated. |
| OV-09 | engagement-ring-online ↔ shapes / 14k-18k / ring-size | DISTINCT | The online guide only covers these as steps. |
| OV-10 | FAQ ↔ legitimacy / lab-vs-natural / certification articles | POSSIBLE | Same questions answered in a different format. No ranking or SERP evidence. |
| OV-11 | Oval marquise PDP ↔ shapes article | DISTINCT | The SERP is PRODUCT-dominant, and the PDP is the page that ranks. |
| OV-12 | /blog hub ↔ /education hub | POSSIBLE | Section-level overlap (see §7). |
| OV-13 | Homepage ↔ /engagement-rings | POSSIBLE | Title-level only: the homepage title targets "Lab-Grown Diamond Engagement Rings". |
| OV-14 | /wedding-bands/for-her/eternity ↔ /fine-jewellery/rings/eternity-rings | POSSIBLE | Structural only. The second page is empty, and there are 0 "eternity" master keywords. |
| OV-15 | /shop ↔ /collection | POSSIBLE | Structural. /collection is empty (Stage 1). |
| OV-16 | /t-bar ↔ /fine-jewellery/necklaces (+ pendant-necklace) | POSSIBLE | Structural. There are 0 t-bar master keywords. |
| OV-17 | /engagement-rings ↔ side-stone subcategory | DISTINCT | Parent/child. The CATEGORY SERP ranks the narrower URL. |
| OV-18 | engagement-ring pavé ↔ wedding-band pavé | DISTINCT | Different product types. |

By the areas the brief asked about:

- **Certification:** clear overlap (OV-01).
- **Lab-grown:** possible overlap (OV-02, OV-03), and distinct for CVD vs origin (OV-04).
- **Shapes:** distinct (OV-09, OV-11).
- **4Cs:** possible (OV-07, OV-08).
- **Buying/education:** possible (OV-06, OV-10, OV-12).

---

## 5. Content → SERP alignment (Part 5)

Source: `10_content_serp_alignment.csv` (59 rows). There are two bases:

- **28 rows based on Stage 3 ranking keywords.** This is the Part 5 scope.
- **31 supplementary rows** for topic-related validated keywords where HOD does not rank.

**On the Stage 3 basis (pages that actually rank): 24 ALIGNMENT, 1 PAGE_TYPE_MISMATCH, 3 INSUFFICIENT_EVIDENCE.**

- **ALIGNMENT (24 rows)**
  - 16 CVD-article keywords: the article matches EDITORIAL_GUIDE/COMPARISON SERPs. Note that for *hpht lab grown diamonds* the #1 result is a londongold.com CATEGORY page, although the SERP is COMPARISON-dominant overall.
  - 2 lab-vs-natural keywords: COMPARISON SERPs.
  - 3 14k-vs-18k keywords: EDITORIAL_GUIDE.
  - How-to-choose: EDITORIAL_GUIDE.
  - Oval marquise PDP: PRODUCT SERP.
  - Side-stone subcategory: CATEGORY SERP.
- **PAGE_TYPE_MISMATCH (1 row):** *cvd/hpht diamond tester* (30, position 68). The SERP is CATEGORY/TRANSACTIONAL (gemtrue, septools tool listings), and HOD's page is an article.
- **INSUFFICIENT_EVIDENCE (3 rows):** *are cvd diamonds real* (OTHER), *what is cvd lab grown diamond* (MIXED, LOW confidence), and *which diamond is better lab grown or natural* (OTHER). The top-5 page types for each are listed in the CSV.

**Corrections to Stage 9 Type C:**

- Stage 9 described the HOD page as "blog/editorial-guide format" for *marquise oval diamond* and *side stones engagement rings*. That is wrong: the pages are a PDP and a category URL, and both **align** with their SERPs.
- Stage 9 counted OTHER/MIXED dominant types as "differs". Stage 10 treats them as insufficient evidence instead.

The Stage 9 file was not edited. See `decision-log.md`.

**Supplementary rows (no HOD ranking), shown for context:**

- 14 are aligned in page type, for example *diamond shape* (60,500) against the shapes article and *v v s diamond* (18,100) against the 4Cs article.
- 11 differ in page type:
  - Category pages paired with informational SERPs: wedding bands (*is tungsten good for wedding bands*), earrings, necklaces and bracelets.
  - The shapes article paired with *marquise oval diamond* (a PRODUCT SERP) and *asscher diamond* (a BRAND SERP).
  - Both certification pages paired with *ags diamond grading* (a BRAND SERP).
- 6 have insufficient evidence.

---

## 6. Gaps vs absence (Part 6)

These are the categories from `part6_category` in the coverage CSV. **None of them is called an "opportunity".**

1. **EXISTING_CONTENT_WITH_WEAK_RANKING_EVIDENCE.** 28 keyword rows on 6 URLs. They rank, but only at positions 27–104.
2. **EXISTING_CONTENT_WITH_TOPIC_COVERAGE.** 185 unique master keywords string-match the topic of exactly one existing page but have no ranking. The largest groups are:
   - 4Cs article: 95 keywords, including *v v s diamond* (18,100) and *diamond clarity grading scale* (12,100)
   - lab-vs-natural: 22 keywords, including *lab grown vs natural diamonds* (22,200)
   - are-real: 21 keywords, including *are lab grown diamonds real* (14,800)
   - shapes: 17 keywords, including *diamond shape* (60,500)
3. **EXISTING_CONTENT_WITH_OVERLAP.** 58 unique certification keywords string-match **two** HOD pages (OV-01).
4. **MASTER_KEYWORD_WITHOUT_EXISTING_HOD_CONTENT.** 48 of the 100 Stage 8 keywords match no existing inventoried page. They include:
   - lab-grown head and commercial terms: *lab grown diamonds*, *lab diamonds*, *2ct lab created diamond*
   - natural-diamond terms
   - moissanite and diamond-tester queries
   - gemstones
   - settings and metals: *types of diamond settings*, *mixed metal ring*, *rhodium ring*
   - off-topic polysemy terms that Stage 8 already identified

   Absence of a string-match means **"no evidence found"**, not "does not exist".
5. **BUSINESS_AREA_WITH_LITTLE/NO_EXISTING_CONTENT.** See §8.
6. **EXISTING CONTENT BUT SERP PAGE TYPE DIFFERS.** 7 unique keywords: 6 informational queries where only a category page exists (wedding bands, earrings, necklaces, bracelets), plus *marquise oval diamond* against the shapes article. Separately, on the Stage 3 basis, *cvd/hpht diamond tester* is an article ranking in a CATEGORY SERP.

For scale: 1,258 INCLUDE master keywords exist. 249 master keywords (INCLUDE, plus AMBIGUOUS ones that were SERP-validated) string-match at least one existing HOD page. **415 master keywords have no business area** and cannot be placed in any area.

---

## 7. Blog ↔ Education relationship (Part 8)

**What each section contains:**

- `/blog` has 10 long-form articles covering:
  - lab-grown legitimacy, comparison and growth method (4)
  - buying guides (2)
  - 4Cs (1)
  - shapes (1)
  - ring size (1)
  - gold karat (1)
  - IGI certification (1)
- `/education` has 1 long-form article (GIA vs IGI certification). Its hub describes a wider scope (diamonds, craftsmanship, care, buying) that is not yet populated.

**Search intent:** both sections carry informational content. The blog already includes definitional, education-style topics (4Cs, IGI certification, CVD/HPHT) that are the same kind of content as the education article. There is no observable intent or format difference: both are long-form, use the same title pattern, and use the same "-house-of-diams" slug suffix.

**Same topics in both sections:** yes. Certification appears in both (OV-01, CLEAR_OVERLAP).

**Ranking evidence:** all 26 of the article rankings sit in /blog, and 0 sit in /education. Neither certification page ranks, so ranking data cannot show competition between the two sections.

**Is there a clear distinction?** Not from the evidence available. The two content systems are not separated by intent, format or topic.

This is a description only. No blog/education architecture is proposed here.

---

## 8. Content by business area (Part 7)

Source: `10_content_business_area_coverage.csv` (16 rows). Master keyword counts are INCLUDE keywords, assigned to an area by Stage 5 or else the Stage 6 best-effort field.

| Area | Articles | Category URLs (incl. nav-discovered) | Stage 3 rankings | Master kw (matched to existing page) | Stage 8 validated (matched) |
|---|---|---|---|---|---|
| 1. Engagement Rings | 4 (primary or secondary) | 10 (9 not in sitemap) | 2 (PDP, side-stone) | 23 (13) | 3 (0) |
| 2. Wedding Bands | 0 | 12 (11 not in sitemap; 8 appear empty) | 0 | 2 (2) | 2 (2) |
| 3. Earrings | 0 | 7 (6 not in sitemap) | 0 | 3 (3) | 2 (2) |
| 4. Necklaces & Pendants | 0 | 11 (/t-bar + 9 not in sitemap) | 0 | 2 (2) | 2 (2) |
| 5. Bracelets | 0 | 5 (4 not in sitemap) | 0 | 2 (2) | 2 (2) |
| 6. Fine Jewellery | 0 | 4 (+ /shop, /collection) | 0 | **0** | **0** |
| 7. Bespoke / Custom | 0 | 1 (/bespoke) | 0 | **0** | **0** |
| 8. Lab-Grown Diamonds | 7 | 0 | **22** | 509 (101) | 15 (8) |
| 9. Natural Diamonds | 1 (secondary) | 0 | 0 | 21 (5) | 4 (0) |
| 10. Diamond Shapes | 1 | 0 | 0 | 12 (11) | 4 (3) |
| 11. Diamond Cuts | 0 | 0 | 0 | 1 (1) | 1 (1) |
| 12. Quality / 4Cs | 1 | 0 | 0 | 144 (69) | 5 (5) |
| 13. Certification | 2 (**overlap**) | 0 | 0 | 33 (27) | 4 (3) |
| 14. Buying / Education | 4 | 0 | 1 | 40 (1) | 5 (0) |
| 15. Materials / Metals | 1 | 0 | 3 | 6 (1) | 2 (1) |
| 16. Gemstones | 0 | 0 | 0 | 45 (0) | 8 (0) |

**Areas with existing content:**

- Lab-grown is the only area with both several articles and ranking equity.
- 4Cs, certification, shapes, materials and buying have 1–4 articles each.
- The product areas (1–7) have category URLs but no articles, except the engagement-ring buying guide.

**Areas with little or no existing content, according to the data:**

- **Gemstones:** no URL at all.
- **Diamond Cuts:** no dedicated page.
- **Natural Diamonds:** no dedicated page; only the secondary coverage in the lab-vs-natural article.
- Wedding bands, earrings, necklaces and bracelets have no informational content.

**Areas where keyword data is missing:** Fine Jewellery and Bespoke both have 0 master keywords. That is a gap in the keyword data, **not** evidence of zero demand. Demand is not inferred from absence anywhere in this stage.

---

## 9. Method notes and limitations

- **Topic string-match heuristic.** Regex patterns are set per topic, for example `\b(cvd|hpht)\b` and 4Cs terms (clarity, carat, VVS, SI and so on). Gemstone and moissanite terms are excluded from the lab-grown, 4Cs and shape patterns. The patterns were spot-checked, and false positives found in the first pass were fixed:
  - gemstone "lab vs natural" matches
  - "diamond grading scale" wrongly counted as certification
  - an over-broad "buying" rule

  The heuristic is directional only. For product categories it matches the product noun alone.
- **Page intent** in the inventory is Stage 10's reading of title, H1 and topic, labelled as not SERP-validated. **Business area** per page is assigned the same way.
- **Nav check** captured only the server HTML: title, H1, canonical, meta robots, and a "No pieces match" marker. Product-link counts are approximate. JS-rendered content was not evaluated.
- The analysis inherits all Stage 8 and Stage 9 limitations: 100-keyword sample, heuristic page types, 24% OTHER.
- The project does not cover GSC, backlinks, internal links, word counts or index coverage.

## 10. DataForSEO: was a paid call needed?

**No.** Every part could be answered from the Stage 1–9 data plus free read-only HTTP checks of the public site. A deeper SERP check or a `ranked_keywords` refresh was considered and rejected: it would not change the descriptive conclusions of this stage. **DataForSEO spend this stage: $0.00.** Cumulative spend remains $0.33536.

## 11. Files

- `content-strategy/10_existing_content_inventory.csv` (71 rows)
- `content-strategy/10_content_keyword_coverage.csv` (389 rows)
- `content-strategy/10_content_equity_analysis.csv` (71 rows)
- `content-strategy/10_content_overlap_analysis.csv` (18 rows)
- `content-strategy/10_content_serp_alignment.csv` (59 rows)
- `content-strategy/10_content_business_area_coverage.csv` (16 rows)
- `content-strategy/10_existing_content_summary.md` (this file)
