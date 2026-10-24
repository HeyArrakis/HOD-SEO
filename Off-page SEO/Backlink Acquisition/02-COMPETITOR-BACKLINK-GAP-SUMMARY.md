# 02 — Competitor Backlink Gap Summary

Research date: **2026-10-10** · Market: United States · Status: **research and planning only** (no outreach sent, no site change).
Operational file: [`01-HOD-BACKLINK-ACQUISITION-DATABASE.csv`](01-HOD-BACKLINK-ACQUISITION-DATABASE.csv) (77 rows). Method and limits: [`05`](05-METHODOLOGY-AND-DATA-LIMITATIONS.md).

> **Two numbers that must not be confused**
> - **Provider-verified referring domains collected:** 677 unique domains (C2 112 + C3 28 + C4 581, de-duplicated) link to the competitor sets and, per DataForSEO, not to HOD. Most of these were *not* individually reviewed, and 442 of the 581 C4 domains are spam-pattern sites.
> - **Prospects researched and carried into the database:** 72 domains / 77 rows. Of these, **44 rows (40 domains) are verified competitor-gap opportunities** that were not disqualified, and 26 rows are standalone prospects with no competitor-link evidence collected.

---

## 1. HOD's own backlink baseline (C1, DataForSEO, 2026-10-10)

| Measure | Value |
|---|---|
| Referring domains in the DataForSEO index | **21** |
| Legitimate editorial / industry links among them | **0** |
| Pattern | 17 domains use an identical template page (`/all/1371/21.html` or `/all/252/11.html`) with the anchor "High Quality Dofollow Backlinks DA 50 PA". 4 are `seo-…-hub.shop` / `seopxl-…lab.shop` sites with the anchor "houseofdiams.com". Spam scores 60–75; first seen 2026-06-11 to 2026-10-09. |
| DataForSEO domain Rank for houseofdiams.com | **0** (0–1000 scale) |

**What this means:** as far as this index shows, HOD has no earned editorial links today, so almost every relevant publisher is a "gap". The spam links' origin is **UNKNOWN**: they could be automated spam, or links someone bought. Nothing here shows HOD placed them.

**Recommendation (not an action taken):** do **not** disavow by default. Google's disavow help page says to disavow only when there are "a considerable number of spammy, artificial, or low-quality links" *and* they have caused, or will likely cause, a manual action. It also says "most sites will not need to use this tool". Two follow-ups:
1. Check Search Console → Manual Actions. GSC is not available in this environment, so this is **VERIFY**.
2. Ask HOD whether any link-building service was ever bought. If one was, stop it and revisit the disavow question.

## 2. Competitor set and why

Selected from Stage 9 (`competitors/analysis/09_hod_competitor_frequency.csv`) by frequency in US SERPs for HOD-relevant queries **and** business-model fit (online engagement-ring/fine-jewelry retailers, lab-grown focus). No new competitor discovery was needed.

| Set | Competitors | Stage 9 validated-keyword count | Rationale |
|---|---|---|---|
| A — top direct DTC | brilliantearth.com, bluenile.com, ritani.com | 41 / 19 / 23 | The three most frequent direct jewelry e-commerce competitors |
| B — lab-grown / DTC peers | vrai.com, cleanorigin.com, withclarity.com | 9 / 7 / 14 | Lab-grown-led DTC brands closest to HOD's catalog positioning |
| C — five-way domain overlap | A + vrai.com + cleanorigin.com | — | Finds publishers that link to the whole category (repeatable outreach types) |

Excluded on purpose: platforms (Reddit, YouTube, Instagram), education and certification bodies (GIA, IGI — classified separately as resources), comparison engines (Rare Carat), and UK retailers (Taylor & Hart, Queensmith), which are outside the US market. Remember that Stage 9 shows **SERP presence**, not links. No competitor link in this database was inferred from Stage 9.

## 3. Data collected (provider evidence)

| Call | Endpoint / configuration | Result | Cost (USD) |
|---|---|---|---|
| C1 | `backlinks/backlinks` — houseofdiams.com, one_per_domain | 21 referring domains (all spam-pattern) | 0.024756 |
| C2 | `backlinks/page_intersection` — Set A, exclude HOD, English pages | 669 pages on 112 domains link to **all three** | 0.048084 |
| C3 | `backlinks/page_intersection` — Set B, exclude HOD, English pages | 81 pages on 28 domains | 0.026916 |
| C4 | `backlinks/domain_intersection` — Set C, exclude HOD | 581 domains link to all five (442 have an average backlink spam score ≥ 40 on their links to Brilliant Earth) | 0.044916 |
| C5 | `backlinks/backlinks` — brilliantearth.com, `is_broken = true`, English, one_per_domain | 498 broken links (157 → 404, 335 → 403, 6 → 504) | 0.041928 |
| C6 | `backlinks/bulk_ranks` — 82 domains | Authority metric for every prospect + HOD + competitors | 0.026952 |
| | | **Total actual spend** | **0.213552** |

All six calls were approved by the user in chat on 2026-10-10, max $0.36. C5 was approved as one call covering Brilliant Earth and Blue Nile, but the endpoint takes one target, so **only Brilliant Earth was queried**. No second call was made, and Blue Nile broken links remain uncovered. Raw outputs are in `_raw/dataforseo/`.

## 4. Verification of individual pages

- 69 source pages were fetched live (GET only) on 2026-10-10: 56 gap pages and 13 extra pages.
  - **47** returned 200 with competitor links present.
  - 7 were blocked (403 / Cloudflare).
  - 4 are gone (404/410). The page is gone, so the gap no longer exists.
- **No page linked to or mentioned House of Diams.**
- 6 checks were done in the built-in browser where scripted access was blocked. They covered 5 Brilliant Earth targets (4 confirmed 404; `highest-karat-gold` now redirects, so DataForSEO's broken flag was stale) and the Love You Tomorrow article.
- Evidence classes in the database:

| Evidence class | Meaning | Rows (non-disqualified gap rows) |
|---|---|---|
| PROVIDER_AND_LIVE_VERIFIED | DataForSEO lists the link **and** the live page still shows it | 32 |
| LIVE_PAGE_VERIFIED | Found by web search/C5 and confirmed on the live page | 5 |
| PROVIDER_VERIFIED_BROKEN | DataForSEO shows a link to a dead competitor URL | 1 |
| PROVIDER_DOMAIN_LEVEL | C4 shows the domain links to all five competitors; no page URL retrieved | 6 |
| **Total verified competitor-gap opportunities** | | **44 rows / 40 domains** |

## 5. Link attributes on the 47 live-verified pages

| Competitor links on the page | Pages |
|---|---|
| No `nofollow`/`sponsored` (normally followed) | 28 |
| All `nofollow` or `sponsored` | 11 |
| All `sponsored` (commerce/affiliate) | 4 |
| Mixed | 4 |

Followed or not, these are attributes of the **competitor** links. A future HOD link may be marked differently. `sponsored` links pass no ranking credit; their value is referral traffic and brand visibility only.

## 6. Recurring publisher patterns (what is repeatable)

1. **"Best places to buy engagement rings online" roundups**: bridal blogs (Bridal Musings), men's advice (The Plunge, AskMen), lifestyle (Best Life, Reviewed), personal finance (My Millennial Guide, HowToMoney). This is the most repeatable route: one fact sheet serves many editors.
2. **Shape/style buyer's guides on wedding sites** (The Plunge radiant/heart guides, Munaluchi "unconventional rings"). These match HOD's real products: toi-et-moi, east-west, radiant, heart.
3. **Independent review and scoring sites** (Rings.com Buyer Protection Scores, Carat Brands, Lab Diamond Reviews, RingReel). They judge **published policies**. HOD's `/shipping` placeholder and empty `/returns` would score at the minimum today.
4. **Commerce/affiliate shopping posts** (BuzzFeed, Fox News Deals, PureWow, Krazy Coupon Lady, Grown Diamond): all `sponsored`. Not reachable without an affiliate program, which is a business decision.
5. **Trade press** (JCK; National Jeweler as a standalone prospect): domain-level evidence; needs real news.
6. **Wedding submission sites** (Style Me Pretty, Wedding Chicks, Green Wedding Shoes): credit vendors in real shoots, so they work only through genuine photographer collaborations. Their paid vendor guides are excluded.
7. **Spam networks**: 442 of 581 five-way domains are spam "DA checker"/link-farm sites. Competitors receive spam links too. This is noise, not a model to copy.

## 7. Broken-link findings

- 157 Brilliant Earth backlinks point to URLs DataForSEO saw as 404. Most broken sources are low-quality or competitor sites, or link to Brilliant Earth **moissanite** content that HOD does not have.
- Usable replacements are few:
  - **PureWow** and **Destination I Do** (GAP-027, GAP-040) can be partly matched by HOD's "Are lab-grown diamonds real?" guide, which covers simulants in one paragraph.
  - **The Plunge** (GAP-006) has a dead product link; HOD's heart halo ring would be the replacement.
- Four candidates were rejected (GAP-041–044): the source is gone, the source is a low-quality marketplace or article directory, or the target is no longer broken.

## 8. Priority takeaways

- **P1 (5):** Bridal Musings roundup (GAP-002), Love You Tomorrow custom-designer roundup (GAP-001), Qwoted source profile (DPR-001), The Plunge online-vs-store guide (GAP-004), Munaluchi Bride (GAP-012).
- **Nothing is outreach-ready.** Every row is gated by G0: fix `/shipping` and `/returns`, confirm contact and company identity, name a spokesperson, and remove unverified trust claims (see 03 §1).
- The fastest legitimate wins are **roundup inclusions and expert commentary**, not directories.
- Affiliate-dependent commerce coverage and membership listings are business decisions for HOD and are flagged rather than pursued.

## 9. Limitations specific to this summary

- One index (DataForSEO) and one date. Ahrefs/Semrush were not available (the Ahrefs connector needs authentication), so coverage is not exhaustive.
- C4's `exclude_targets` was not fully reliable: some spam domains that link to HOD per C1 (e.g. `kernelpanicpodcast.com`) still appeared in C4. Every prospect was therefore cross-checked against C1 directly.
- Pages behind Cloudflare could not be fetched by script; they remain provider-verified only.
- Blue Nile broken links were not queried (see §3).
