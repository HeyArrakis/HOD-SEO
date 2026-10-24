# 05 — Methodology and Data Limitations

Research date: **2026-10-10** (one day, one vantage point). Workstream: off-page / backlink acquisition. **Research and planning only.**

---

## 1. Scope and rules followed
- **No changes** to the website, CMS, DNS, AWS, redirects, sitemap, robots, metadata or internal links.
- **No changes** to the final blog calendar, keyword ownership, `QA/01–06`, the Step 2 package, `blogs/` (including BC-001), project instructions or memory.
- No outreach sent, no form submitted, no account created, no Git commit.
- `.env` was not read. No credential appears in any file.
- Paid calls: six DataForSEO Backlinks API calls, **each listed and approved by the user in chat before running** (§3).
- All new files are inside `Off-page SEO/Backlink Acquisition/`.

## 2. Tool and data access (checked 2026-10-10)

| Source | Status | Use |
|---|---|---|
| **DataForSEO Backlinks API** (MCP) | **Available**, pay-as-you-go. The free `appendix/user_data` call ($0.00) showed Backlinks pricing enabled at $0.024/request + $0.000036/row; account balance ≈ $47.55 | C1–C6 |
| DataForSEO docs | Free | Endpoint and pricing verification |
| **Ahrefs** (marketing plugin) | **Not available**: the MCP server needs user authentication (claude.ai connector settings or `/mcp`) | Not used. No Ahrefs DR exists in this database |
| Similarweb, Semrush | Not available (Similarweb needs auth; Semrush is not configured) | Not used |
| Google Search Console | Not available (per project notes). The GSC API has no Links report anyway | Manual Actions check is **VERIFY** |
| Public web search | Available | Prospect discovery, mention search, platform status |
| curl (GET only) | Available | Live page verification (status, title, outbound competitor links + `rel`, HOD link/mention, public `mailto:`) |
| Built-in browser | Available | 6 checks on Cloudflare-protected pages |

## 3. Paid calls (all approved; actual cost $0.213552)

| Call | Endpoint | Configuration | Actual cost |
|---|---|---|---|
| C1 | backlinks/backlinks/live | target houseofdiams.com, mode one_per_domain, limit 1000 | 0.024756 |
| C2 | backlinks/page_intersection/live | targets brilliantearth.com, bluenile.com, ritani.com; exclude houseofdiams.com; filter page_from_language = en; order page_from_rank desc; limit 1000 | 0.048084 |
| C3 | backlinks/page_intersection/live | targets vrai.com, cleanorigin.com, withclarity.com; same settings | 0.026916 |
| C4 | backlinks/domain_intersection/live | targets the 5 competitors; exclude houseofdiams.com; order rank desc; limit 1000 | 0.044916 |
| C5 | backlinks/backlinks/live | target brilliantearth.com, one_per_domain, filters is_broken = true AND page_from_language = en, limit 1000 | 0.041928 |
| C6 | backlinks/bulk_ranks/live | 82 domains (prospects + HOD + competitors), default 0–1000 scale | 0.026952 |

Additional free calls: `appendix/user_data` (×2, $0.00).

**Deviation, recorded honestly:** C5 was approved as one call covering Brilliant Earth **and** Blue Nile. The endpoint accepts a single target, so the one approved call ran for Brilliant Earth only. Blue Nile broken backlinks remain **unqueried**; covering them would need one more call (≤ $0.06) and a new approval.

**Logging note:** per the brief, project logs outside this folder were not modified, so this spend is recorded here. The project's `cost-log.csv` / `progress.md` convention asks for paid calls to be logged there too. Appending these six rows is a pending user decision.

Raw outputs: `_raw/dataforseo/C1…C6_*.json` (unaltered API JSON for C1–C5; C6 is an exact transcription of the inline response, labeled as such). Processed CSVs: `C2/C3/C4/C5_processed.csv` (built by `_build/parse_intersections.py` and inline parsers).

## 4. Competitor selection logic
- Started from Stage 9 `09_hod_competitor_frequency.csv` (SERP frequency across 100 validated US keywords).
- Chose direct online jewelry competitors with HIGH classification confidence and a business model close to HOD's: online engagement rings and fine jewelry, lab-grown-led catalog.
- Set A = the three most frequent direct DTC competitors. Set B = the lab-grown DTC peers. Set C (domain overlap) = A + VRAI + Clean Origin.
- Not expanded: no clear business rationale required it. Kay, Zales, Tiffany and similar brands are a different (store/heritage) model, but their links appear in the live-check output for reference.
- **Stage 9 data was never used as backlink evidence.**

## 5. Verification process
1. **Provider evidence:** a DataForSEO row (C2/C3/C5) naming the referring page and competitor target URL, or a C4 domain-level row.
2. **Live page check** (`_build/verify_pages.py`, 2026-10-10): records HTTP status, final URL, title, every outbound link to 22 tracked competitor domains (href, anchor, `rel`), any HOD link or text mention, and public `mailto:` addresses. Output: `_raw/page-checks/gap_pages_*.json`, `extra_pages_*.json`.
3. **Route discovery** (`_build/find_routes.py`): homepage and sub-page scan for **published** contact, submission, press and membership links. Email addresses were recorded only when they appear as `mailto:` links or page text. **No address was guessed or pattern-generated.**
4. **Browser checks** where Cloudflare blocked curl (`_raw/page-checks/browser_checks_2026-10-10.json`).
5. **Cross-check against C1:** a prospect is "Existing HOD backlink = No" only when its domain is absent from HOD's C1 referring-domain list. No prospect domain appears in C1.
6. **Evidence classes:** PROVIDER_AND_LIVE_VERIFIED, LIVE_PAGE_VERIFIED, PROVIDER_VERIFIED_BROKEN, PROVIDER_DOMAIN_LEVEL, PROVIDER_VERIFIED_SOURCE_GONE, PROVIDER_FLAG_STALE, PUBLIC_SOURCE_PROSPECT (no competitor-link evidence collected).

## 6. Filtering rules (rejection criteria)
Reject, or never add:
- Spam-pattern domains (C4: 442 of 581 have an average backlink spam score ≥ 40, mostly "DA/PA checker" and link-farm sites).
- Generic link directories.
- Open article directories.
- Marketplace content blogs.
- Guest-post or sponsored-content sellers.
- Paid listings whose value depends on passing ranking credit.
- Pages that no longer exist.
- Broken targets that are no longer broken.
- Competitor retailers' own blogs.
- Off-topic or non-US sites without a clear fit.

**Disqualified rows are kept in the database** (status `DISQUALIFIED`, priority `NONE`) so the same prospects are not re-researched. Affiliate-dependent commerce placements are **not** disqualified: they are legitimate but conditional on a business decision (`REVISIT_LATER`).

## 7. Prioritization framework (transparent and reproducible)

Six components, each scored by analyst judgment against the rubric below and stored per row (`Score R/Q/P/G/F/V`):

| Component | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **R** topical + audience relevance | off-topic | adjacent | relevant topic or audience | core: engagement rings / fine jewelry / bridal, US buyers |
| **Q** editorial credibility / source quality | low-quality or unknown | small or affiliate-led site | established niche publication | major or established editorial brand / trade authority |
| **P** acquisition pathway evidence | none found | route plausible but unverified | public route verified (contact or submission page) | named public route matching the opportunity (e.g. published email or platform sign-up) |
| **G** competitor-gap evidence (computed from evidence class) | none | provider-only, live-only, domain-level or broken | provider **and** live verified | — |
| **F** feasibility after gate G0 | unrealistic now | needs a business decision or unconfirmed product (affiliate program, platinum, men's range, loose stones) | needs ordinary preparation | low effort |
| **V** likely business value to HOD | none | brand visibility only | relevant referral/brand value | high-intent buyers (engagement-ring / bespoke shoppers) |

**Score = R + Q + P + G + F + V (0–17).**

- **P1:** score ≥ 14 **and** R = 3, F ≥ 2, P ≥ 2. Strong, relevant and realistically actionable, so a big-name site with no route cannot be P1.
- **P2:** score 10–13, or a P1-level score that misses one gate.
- **P3:** score ≤ 9.
- **NONE:** disqualified.

Authority metrics are **not** in the score. DataForSEO Rank is shown for context only. It is a third-party estimate (0–1000), not a Google metric and not a measure of editorial quality. Missing metrics stay blank (none were missing for prospect domains; C6 covered all 72).

## 8. Global readiness gate G0
No row may move to `OUTREACH_READY` until G0 clears:
- G0-1/G0-2: `/shipping` and `/returns` are real (F-A1, F-A2).
- G0-3: unverified trust claims are fixed (F-B1, F-A3).
- G0-4: a named spokesperson and company identity (F-C1).
- G0-5: a public contact (F-C2).
- G0-6: `/bespoke` lead time is corrected.
- G0-7: link-target URL stability is known (AWS).

Full detail in 03 §1.

## 9. Coverage gaps and uncertainty
- **Single backlink index** (DataForSEO). Ahrefs, Moz and Semrush indexes would surface different pages. The database is **not exhaustive**.
- Intersections need a page to link to **all** targets in the set. Pages linking to only one or two competitors were not pulled; that would mean per-competitor `referring_domains` calls, each needing approval.
- English filter only; US relevance was judged by the analyst, not filtered by country.
- Blue Nile broken links were not queried (C5 deviation).
- C4 `exclude_targets` was imperfect (spam domains linking to HOD still appeared), so C1 cross-checks were done manually.
- 7 live pages were blocked (403); their gap status is provider-only.
- Contact routes behind Cloudflare (Love You Tomorrow, JCK, Best Life) were seen in navigation but not fetched.
- Mention search relied on a general web search engine (see 04 §1).
- Facts about membership terms (LGDC, JA, AGS, RJC), HARO and Source of Sources come partly from secondary coverage and are marked `VERIFICATION_REQUIRED`.
- All findings are point-in-time (2026-10-10). Links and pages change, so re-verify before acting.

## 10. Work requiring approval or input
| Item | Type | Est. cost |
|---|---|---|
| Blue Nile broken-backlink pull (`backlinks/backlinks`, is_broken, en) | Paid DataForSEO call | ≤ $0.06 |
| Per-competitor referring-domain pulls (e.g. Ritani, VRAI single-target, US-filtered) to widen coverage beyond intersections | Paid DataForSEO calls | ≤ $0.06 each |
| Brand-mention search (DataForSEO Content Analysis) | Paid; pricing not yet checked | quote first |
| Ahrefs connector authentication (for DR and a second index) | User action (`/mcp` or claude.ai connector settings) | subscription-dependent |
| Append C1–C6 spend to `cost-log.csv` / `progress.md` | User decision (files outside this workstream) | — |
| Affiliate program yes/no; memberships (LGDC, JA, AGS, RJC) yes/no | HOD business decisions | — |
| G0 facts (F-A1, F-A2, F-B1, F-A3, F-C1, F-C2, F-E3, F-E4, F-E6) | HOD | — |
| Manual Actions check in GSC | User (GSC access) | — |
