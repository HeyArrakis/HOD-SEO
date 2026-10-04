# Blog Content Calendar: summary (after the hard SEO revision)

**Window:** Tue 29 Sep 2026 → Thu 31 Dec 2026 (14 planning weeks).
**Status:** revised calendar complete and awaiting review. This is research and planning only: no article copy, final SEO titles or meta descriptions. No Stage 1–19 file was changed (QC check 25).
**Revision:** the original 34-blog calendar (built 2026-09-29) was put through a stricter SEO review using three new rounds of DataForSEO research. Every decision was approved by the user before the calendar was rewritten in place.

## 1. Result at a glance

| | Original | Revised |
|---|---|---|
| Scheduled blogs | 34 | **28 scheduled** (+26 slots explicitly unused) |
| Primary-keyword demand | ~82,950 / month | **~270,210 / month** |
| Primary + secondary demand | not recorded | ~497,780 / month |
| Primaries under 300 / month | 12 | 4, each with a documented justification (BC-001, BC-015, BC-016, BC-019) |
| Primaries checked against the live Google results page | 0 | 28 of 28 |
| AI Overview captured | – | 27 of 28 present (BC-025: absent, recorded) |
| People Also Ask captured | – | 28 of 28; 123 question placements written into the calendar |
| Evergreen / seasonal / festival | 15 / 9 / 10 | 16 / 7 / 5 |
| Blog type (Stage 13/16) | Gifts 15, Style 11, Craft 4, Industry 4 | Gifts 10, Style 12, Craft 2, Industry 4 |
| Priority | 8 P1 · 17 P2 · 6 P3 · 3 P4 | 7 P1 · 18 P2 · 3 P3 · 0 P4 |
| QC | 27 checks | **28 checks, matching the revision brief's QA list** (`blog_calendar_qc.py`), mutation-tested |

## 2. What changed

**Removed (8)** because the live results page showed the blog could not compete or the intent did not fit HOD. Where useful, their demand survives as a section elsewhere:

| ID | Topic | Evidence | Where it went |
|---|---|---|---|
| BC-012 | jewelry gifts for mom (1,000) | 7 of 10 results are product/category pages; no AI Overview | Section in BC-004; commercial gifts collection recommended |
| BC-013 | luxury christmas gifts for her (260) | Fashion, perfume and beauty brands | Section in BC-004 |
| BC-020 | hanukkah jewelry (140) | Judaica and novelty marketplace | Section in BC-004 |
| BC-026 | three stone ring meaning (110) | Too little demand | Section in BC-031 |
| BC-027 | right hand ring (2,900) | Transactional (product pages) | Meaning section in BC-038 |
| BC-028 | last minute christmas gifts for her (210) | Generic non-jewellery lists | Ready-to-ship section in BC-004 (December refresh) |
| BC-030 | new years eve jewelry (480) | Product-leaning | none |
| BC-033 | valentines day jewelry (2,900) | 10 of 10 product/category pages | Commercial Valentine's collection recommended |

**Merged (3):** BC-002 into BC-015 (industry note), BC-010 into BC-001 (making stages), BC-029 into BC-017 (NYE proposals).

**Primary keyword upgraded (6):**

| ID | From | To | Why |
|---|---|---|---|
| BC-003 | what is a push present (5,400) | push present (18,100) | Both results pages informational; jewellery retailers rank |
| BC-006 | how to layer necklaces (2,400) | necklace layering (14,800) | The two phrasings share 4 top-10 results |
| BC-018 | diamond anniversary (2,900) | anniversary gifts by year (74,000) | "Diamond anniversary" results are cards and cakes |
| BC-024 | average engagement ring cost (8,100) | how much should an engagement ring cost (6,600), combined with average cost, how much to spend and budget (~34,000) | Identical AI Overview text and overlapping questions; user approved one article |
| BC-025 | what are huggie earrings (1,300) | different types of earrings (1,600) + earring backs (3,600) | Huggies leans product-led; "types" is 8 style guides |
| BC-034 | valentines day proposal ideas (390) | valentines day proposal (720) | Informational (The Knot, Vogue) |

**Added (5), all from the new discovery research and validated against the live results page:**

| ID | Primary | Monthly searches |
|---|---|---|
| BC-035 | 10 year anniversary gift | 33,100 |
| BC-036 | what finger does a wedding ring go on | 27,100 (+ wedding ring finger 18,100, what hand 6,600) |
| BC-037 | engagement ring vs wedding ring | 18,100 |
| BC-038 | ring finger meaning | 9,900 (+ per-finger meanings) |
| BC-039 | what finger does a promise ring go on | 12,100 (Dec 1.64×) |

**Kept but corrected:**
- BC-017 dropped "christmas proposal" as a secondary (Google shows the Hallmark movie for that search).
- BC-022 deliberately was **not** upgraded to "ring stacking" (40,500): 7 of 10 results are product pages and there is no AI Overview.
- BC-007's "which hand" phrasings moved to BC-036 to avoid overlap.
- BC-008 and BC-009 are kept at P3 with a commercial-leaning flag (retailer gift categories dominate; editorial lists also rank).

**Not scheduled, by user decision:** NEW-06 "does the man wear an engagement ring" (8,100). EDU-RJG-04 ownership is unchanged.

## 3. Research performed in the revision

| Round | Endpoint | What it did | Returned | Cost |
|---|---|---|---|---|
| Round 1 | 2 × `keyword_ideas`, 6 × `keyword_suggestions` (D1, D2, S1, S5–S9; S2/S3/S4/S10 not run) | Broad high-volume discovery for styling, meaning, gifts, occasions and questions | 3,606 unique keywords (2,978 demand groups) | $0.54108 |
| Round 2 | `serp/google/organic/task_post` (72 tasks; AI Overview loading + 1 level of People Also Ask) | Live results-page check of every current primary, 23 upgrade candidates and 15 new topics | 72 results pages; 432 PAA questions (342 unique); AI Overview on 67 | $0.0972 billed |
| Round 3 | `keyword_overview` (145 keywords) | Measured the related-search and question phrases of the kept topics | 99 with data | $0.02388 |
| **Revision total** | | | | **$0.66216** of the $4 cap |

Notes:
- Round 2 results report lower final per-task costs ($0.057), which suggests refunds of unused AI Overview charges. The account balance does not yet show them; it implies $0.09804 for Round 2 ($0.00084 above the billed $0.0972, unexplained).
- 21 of the 72 Round 2 responses came back inline and were saved as condensed files with the key fields copied verbatim (AI Overview text and references, all PAA questions, the organic results, related searches). The other 51 are complete raw files.
- Original stage call (seasonal keyword_overview, 292 keywords): $0.04404. Blog-calendar work total: $0.7062.

## 4. How decisions were made (no volume-only selection)

Every candidate was judged on search demand, verified search intent, the mix of result types on the live page, HOD fit, content job (Blog vs Education vs commercial), seasonality, commercial value, cannibalisation risk and AI Overview / PAA potential. Concretely:

- **High-volume shopping searches were not turned into blogs.** Examples: tennis bracelet 135,000; promise rings 301,000; ring stacking 40,500; eternity ring 12,100; Valentine's jewellery. Each article targets the informational neighbour instead, e.g. "what is a tennis bracelet" or "how to stack rings".
- **Generic gift searches were rejected** where Google shows non-jewellery lists HOD cannot satisfy: christmas gifts for her, wife, girlfriend and mom; gifts for mother-in-law; valentine gifts for her.
- **Permanent reference topics stayed with Education:** metals (14k vs 18k 12,100; white vs yellow gold 9,900), sizing, eye-clean, moissanite, engagement ring styles (18,100).
- **Merges and splits followed result-page overlap:** 3+ shared top-10 results means one article; fewer than 2 means separate articles. Examples: layering phrasings share 4 (merged); ring-finger meaning phrasings share 3 (merged); wedding-ring finger vs promise-ring finger share fewer than 2 (separate).
- **The full ranked opportunity table** (`revision/blog_high_volume_opportunity_table.csv`, 983 rows) gives a written decision for every relevant demand group of ≥5,000/month and every validated topic. No relevant ≥5,000 group is left undecided (QC check 9).

## 5. AI Overview and People Also Ask in the calendar

Each scheduled blog now carries:
- `ai_overview` and `aio_structure` (the AI Overview's section headings);
- `paa_questions`, each tagged with where it goes: answer-first block, H2, H3, FAQ, table, list, numbered steps, or "link to owner";
- `aeo_answer_format`;
- `related_searches`;
- the verified SERP intent and page-type mix.

Questions that belong to another page are routed there, not answered:
- budget questions → BC-024;
- hardness → EDU-GEN-01;
- lab-grown price → EDU-LG-05.

Recurring rule questions ("2:1:1 rule" 70/mo, "3 month rule" ~10/mo) are FAQ one-liners only.

## 6. Schedule and lead times

| Week | Posts |
|---|---|
| W01 (Sep 28–Oct 4) | BC-001 custom ring timeline · BC-018 anniversary by year · BC-003 push present |
| W02 (Oct 5–11) | BC-004 holiday gift hub · BC-035 10-year anniversary · BC-036 wedding-ring finger · BC-006 necklace layering |
| W03 (Oct 12–18) | BC-008 wife · BC-009 girlfriend · BC-007 how to wear · BC-011 promise ring |
| W04 (Oct 19–25) | BC-037 engagement vs wedding ring · BC-014 proposal ideas · BC-015 industry/Surat (Diwali Nov 8) · BC-024 ring cost |
| W05 (Oct 26–Nov 1) | BC-016 engagement season · BC-017 Christmas & NYE proposals · BC-005 diamond cutting · BC-019 Black Friday timing |
| W06 (Nov 2–8) | BC-021 tennis bracelet · BC-039 promise-ring finger · BC-022 stacking rings · BC-038 ring finger meaning |
| W07 (Nov 9–15) | BC-023 eternity ring meaning · BC-025 types of earrings |
| W10 (Nov 30–Dec 6) | BC-031 engagement ring trends · BC-032 jewellery trends |
| W11 (Dec 7–13) | BC-034 Valentine's proposal |
| W08, W09, W12–W14 | Unused (reasons in each `SLOT-` row). W11 capacity is reserved for the BC-004 December refresh (shipping cut-offs, ready-to-ship). |

Timing rules (enforced by QC checks 14–18):
- Christmas gift posts ≥45 days ahead; other Christmas content ≥28 days.
- Black Friday ≥21 days ahead (BC-019: 28 days).
- Valentine's: one post on Dec 8, ~4 weeks before the January surge.
- Diwali piece Oct 22.
- Engagement-season piece Oct 26 (before Thanksgiving).

High-volume evergreen articles were front-loaded so they have the longest time to be indexed.

## 7. Confirmed business fact used

Bespoke jewellery typically takes 2–3 weeks to make plus about 6–9 days for delivery: generally around 3–4 weeks, depending on the stone. It is used in BC-001, BC-017 and BC-034, always as "typically", never as a guarantee. Source: `revision/confirmed_business_facts.md`.

## 8. Ownership and cannibalisation

- **Stage 15/19:** no conflicts. All blog keywords were checked against the 1,936-keyword map and Stage 19's excluded concepts.
- **Documented boundaries with Education:**
  - BC-005 vs EDU-GEN-01 (cutting process vs hardness);
  - BC-001 vs EDU-NAT-00 (ring-making vs diamond formation);
  - BC-015 vs EDU-LG-00 (where vs how), EDU-NAT-00 and EDU-GEN-01.
- **Removed during the revision:** "when did lab grown diamonds become popular" as a BC-015 secondary (near-match to an EDU-LG-02 keyword).
- **BC-024:** one Blog article owns cost + budget (user decision). None of these keywords is in Stage 15. EDU-RJG-04 is unchanged; if it is built, it should link to BC-024 for budget.
- **Blog-to-blog:** no keyword is used by two blogs. Similar-wording pairs (e.g. BC-036/BC-039, BC-007/BC-036, BC-018/BC-035) are separate results pages with fewer than 2 shared top-10 results, and are documented in QC.

## 9. Remaining items for review

1. **Commercial owners suggested by the evidence** (not blog work): a seasonal Valentine's jewellery collection, a gifts-for-her/mom collection, and possibly a stackable-rings collection.
2. **Education evidence to act on** (outside this stage):
   - ring-size guide demand peaks in December;
   - metals comparisons (14k vs 18k 12,100; white vs yellow gold 9,900);
   - Education gaps: engagement ring and jewellery insurance (8,100 / 14,800), necklace length and bracelet size guides;
   - engagement ring styles 18,100 → EDU-RJG-01.
3. **Business facts still needed:**
   - holiday shipping cut-offs (for the BC-004 refresh);
   - whether HOD cuts or polishes in-house;
   - soldering service;
   - full-eternity resizing;
   - earring backs used;
   - whether HOD runs a Black Friday offer;
   - whether HOD sells platinum or vermeil.
4. **BC-008/BC-009** are commercial-leaning; revisit once a gifts collection exists.

## 10. Files

| File | Contents |
|---|---|
| `blog_content_calendar.csv` | **The single calendar** (updated in place): 28 blogs + 26 unused slots, with search, AI Overview and People Also Ask fields |
| `blog_calendar_revision_log.csv` | Every original BC-001–BC-034 plus the 5 new IDs, with action and reason |
| `blog_topic_backlog.csv` | 46 rows, including the removed topics and the revision rejections |
| `blog_keyword_research.csv` | 4,027 rows labelled `data_source` + `research_round` (R0 seasonal, R1 discovery, R3 measured questions, Stage 7). Round 2 search-results evidence joined in. New research is kept separate from the Stage 7 master. |
| `revision/` | Round 1–3 processing, Round 2 search-results analysis, PAA list, overlap matrix, decision table, high-volume opportunity table, confirmed business facts |
| `blog_calendar_decision_log.md` | Original decisions D-BC-01–24 plus revision decisions R-01 onward |
| `blog_calendar_qc.py` | 28 checks |
| `dataforseo/raw/blog_calendar/` | All raw API responses and price/balance checks |
