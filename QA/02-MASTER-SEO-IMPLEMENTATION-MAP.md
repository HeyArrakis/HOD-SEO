# 02 — Master SEO Implementation Map (human-readable)

Generated 2026-10-09. Companion to `01-MASTER-SEO-IMPLEMENTATION-MAP.csv` (the operational file). This is an **implementation map, not a new strategy**: every recommendation traces to the existing HOD research or to a read-only observation of the live site on 2026-10-09. **Nothing on the website, in the research files, in the final calendar, or in the keyword database was modified.**

## 1. Purpose

Turn the finished HOD research (Stages 1–19, final blog calendar, publishing context) into one operational map that says, for every important page: what it is, which keyword/intent it owns, what is on it today, what should change, how it links, which schema and AEO/GEO work fits, how urgent it is, and what must wait for, or be verified after, the AWS migration.

## 2. Methodology

1. **Read the rules:** `CLAUDE.md`, `reference/SEO_PLAYBOOK.md`, `reference/BLOG_PUBLISHING_CONTEXT.md` (+ the 2026-10-04 verification audit, which changes some playbook claims, e.g. FAQ rich results are deprecated).
2. **Loaded the existing system, without re-researching:** Stage 15 keyword→URL map (1,936 keywords, 27 target pages), Stage 12 IA, Stage 13 existing-content decisions, Stage 14 Education architecture, Stage 16 link map/anchors, Stage 17/18 questions + entities + gaps, Stage 19 briefs, the final calendar (62 scheduled items) and the 10 drafted blog packages.
3. **Observed the live site read-only** (HTTP GET only, 4 parallel workers, no forms, no logins): fetched all 256 sitemap URLs plus 14 extra probes (legacy URLs, `/contact`, `/hiphop`, `/cart`, `/login`, parameter URLs, `robots.txt`, `llms.txt`) and extracted status, `<title>`, meta description, H1, canonical, robots directives, JSON-LD types, internal links and image-alt counts. Raw data: `QA/_build/evidence/`.
4. **Joined** live state to research by URL/ID and generated each row with a repeatable script (`QA/_build/scripts/`). Hand-written judgments are limited to the ~30 core/hub rows; everything else is data-driven.
5. **Marked unknowns** as `UNKNOWN — VERIFY`; GSC fields are `NOT AVAILABLE`. **No paid DataForSEO call was made** (cost $0.00); commercial keyword candidates reuse volumes already in `blog_keyword_research.csv`.

## 3. Scope — what a 'row' is

**147 rows** (one per important URL/page). The live sitemap holds 256 URLs (184 product pages + 72 others); **all 72 non-product sitemap URLs have their own row**. The 184 product pages are represented by one template row, the keyword-owning PDP, and a per-product audit in `06-PDP-AUDIT-APPENDIX.csv` (avoids 184 low-signal rows).

| Row group | Rows | What it covers |
|---|---|---|
| CORE LIVE | 11 | Homepage, /shop, /collection, /bespoke, /about, /contact, /faq, /shipping, /returns, /privacy-policy, /terms |
| HUBS | 2 | /blog, /education |
| COMMERCIAL CATEGORY | 9 | Engagement rings, wedding bands, fine jewellery umbrella, earrings, necklaces, bracelets, FJ rings, T-Bar |
| COMMERCIAL SUBCATEGORY | 40 | Style / type / gender subcategories + Hip Hop children (now in the sitemap) |
| PRODUCT PAGES | 2 | PDP template (184 URLs) + the keyword-owning PDP |
| EXISTING ARTICLES (Education-owned) | 11 | 10 /blog articles + 1 /education article |
| LEGACY / REDIRECT | 5 | Old `by-desgin` URLs (404), /hiphop (308), two removed product URLs |
| PLANNED EDUCATION | 20 | New Education pages scheduled in the final calendar (incl. 4 not yet in Stage 14/15) |
| CONDITIONAL EDUCATION / COMMERCIAL | 14 | Conditional/deferred owners (e.g. EDU-LG-04, EDU-GEM-*, COM-LG-HUB) — documented, not to be built yet |
| PLANNED BLOG | 33 | Blog posts scheduled in the final calendar (the BC-004 December refresh is merged into BC-004) |

Excluded (by rule, not mapped as pages): cart, checkout, login/signup/profile/wishlist, search results, sort/filter/shape/metal parameter URLs, tracking URLs. Observed behaviour: `/cart` and `/login` are `noindex, nofollow`; `?sort=` and `?shape=`/`?metal=` return `noindex, follow` with a canonical to the base URL; `/search?q=` returns 404 + noindex. This matches the architecture (filters are filters).

## 4. Source-of-truth hierarchy (as applied)

1 Stage 12/14 architecture → 2 Stage 15 keyword→URL ownership → 3 final blog calendar → 4 Stage 19 content boundaries → 5 Stage 11 clusters → 6 SERP/intent research (Stage 8, 18.5, calendar rounds) → 7 AEO/PAA research (Stages 17/18) → 8 the live website → 9 new external research (none used).

Where two sources disagree the row shows **both** values and flags it (`Existing Keyword Ownership Conflict?`); nothing is silently chosen or changed. Volumes shown are DataForSEO Labs values already in the project (US, en); no volume or KD was invented.

## 5. Current state — what the live site looks like (2026-10-09)

| Area | Observation (read-only crawl) |
|---|---|
| Platform | Vercel + Next.js (response headers); HTML sent with `cache-control: private, no-cache, no-store`; HTTP/2. |
| Sitemap | 256 URLs (184 products). Stage 1 (2026-09-17) had 198 → **+62 / −4**. No `<lastmod>`. Every sitemap URL returns 200 and is self-canonical. |
| Index control | robots.txt: allow-all, disallows /api, /cart, /checkout, /login, /signup, /profile, /wishlist, /maintenance; explicit allow blocks for 7 AI user-agents (GPTBot, ChatGPT-User, OAI-SearchBot, Google-Extended, ClaudeBot, Claude-SearchBot, PerplexityBot); `Sitemap:` declared. `/llms.txt` exists (primary pages + ~50 products). No hreflang. |
| Metadata | Title pattern `<Page> \| House of Diams` on 255/256 sitemap pages (homepage has no brand). 50 category/subcategory pages use boilerplate meta ('Browse X in Y.' / 'from the live catalog'). 6 PDPs have placeholder-style meta; 65 PDP titles exceed 60 characters. |
| Headings | Every one of the 256 sitemap pages has exactly one H1 in the initial HTML (Stage 1 found none on /about and /faq — fixed since). Homepage H1 is the tagline 'THE BEGINNING OF FOREVER'. |
| Schema | Organization (+ContactPoint, PostalAddress: Surat IN + New York US) on every page; BreadcrumbList on category/subcategory/shop pages but **not** on blog/education articles; **FAQPage on 35 pages** (boilerplate Q&A repeated across category pages, also on /faq and /returns); Product+Offer+Brand+BreadcrumbList on all 184 PDPs; BlogPosting on the 11 articles with a `Person` author (names vary: 'House of Diams Jewellery Team', 'Krish Babriya, Co-founder'). |
| Thin / empty pages in the sitemap | 18 live pages hold 0 products or are test artifacts (`/collection` plus 17 subcategory pages: `/engagement-rings/round-rings`, all four `/wedding-bands/for-him*`, four `/wedding-bands/for-her/*` styles, five empty Fine Jewellery types, and the `/hiphop/*` children incl. `/hiphop/test-subcat`). Stage 12 D-13 says none of these may be indexable. |
| URL changes since the research | `/engagement-rings/by-desgin/*` → `/engagement-rings/by-design/*`: **all old URLs return 404 (no 301)**, including the Stage 15 keyword-owner URL for side-stone rings. `/contact` → 307 to `/?contact=open` (modal); `/hiphop` → 308 to `/shop`. The test product and one product from the Stage 1 sitemap are gone (404). 15 new PDPs. |
| Slug typos still live | `solitare` (2 URLs), `anniversay`, `pavee`, singular `bracelet`, `toi-moi` vs `toi-et-moi`. Any change is a URL migration (CLAUDE.md rule 12). |
| Content defects | Visible placeholder text 'new test black / test desc' on /shipping; /returns shows no return terms (only a FAQ answer); /bespoke says '4-6 week typical lead time' (confirmed HOD fact: ~3–4 weeks); expired-looking 'September sale … HOUSEOFDIAMS2026' banner on the homepage; PDP material label 'Gold Vermil' truncated. |
| Pagination | /shop and /engagement-rings `?page=2` are self-canonical with identical titles; `/blog?page=2` canonicalises to `/blog`. |
| Performance baseline (indicative, one vantage point, not CrUX) | HTML TTFB 1.2–4.5 s and 130–515 KB per page; largest sitemap page 0.53 MB (far below Googlebot's ~2 MB fetch limit — no byte-optimization needed). Re-measure with PageSpeed/CrUX/GSC CWV after cut-over. |
| Product images | Product schema images are served from a Supabase storage host and a Cloudflare R2 `*.r2.dev` host (path `/products/draft/images/…`) — both change with the AWS move. |
| Calendar vs live | None of the 62 scheduled items is live. Six dated 2026-10-04…10-09 (BC-001, BC-004, BC-035, BC-018, BC-036, BC-006) have passed. Whether publishing is paused for the migration is UNKNOWN — VERIFY. |
| GSC | NOT AVAILABLE (SEO Gets connector needs a subscription; no export in the project). All GSC columns say NOT AVAILABLE; Stage 3 'ranked keywords' positions are DataForSEO estimates, not GSC, and are labelled as such. |

## 6. Major opportunities

- **Protect and repair index integrity.** 18 empty/test pages in the sitemap, the 404ing `by-desgin` URLs, redirect behaviour for `/contact` and `/hiphop`, and unpopulated `For Him` / `Hip Hop` branches. Mostly decisions + sitemap/noindex rules — low effort, high risk-reduction.
- **Close the commercial keyword gap (Stage 12 D-19).** 9 category hubs, 38 of the 39 non-test subcategory pages (all but side-stone) and /bespoke own no ratified keyword. Existing datasets already contain candidate heads (e.g. 'engagement ring' 673,000; 'diamond earrings' 74,000; 'tennis bracelet' 135,000; 'lab grown diamonds' 135,000) — they need ratification, not new research.
- **Replace template metadata.** 50 live pages have a metadata opportunity; drafts for each are in the CSV and in `05-ON-PAGE-OPTIMIZATION-BACKLOG.md`.
- **Make hubs useful pages.** Category and subcategory pages are product grids with boilerplate FAQ copy. Add unique intros with the Stage 16 required Education links; stop repeating the same FAQ.
- **Protect ranking-equity articles while refreshing.** CVD vs HPHT (19 ranked keywords), lab-grown vs natural, 14K vs 18K, how-to-choose: update in place, never change URL, baseline GSC first.
- **Fix the Education information architecture.** Only 1 of 11 Education-owned articles sits under /education; the hub lists one article. Execute Stage 13/14 moves only when the documented conditions are met (1:1 301).
- **Schema clean-up (template level).** Add BreadcrumbList + consistent author entity to articles; stop relying on boilerplate FAQPage (FAQ rich results were deprecated 2026-05); enrich Organization (sameAs, founders once confirmed); keep Product markup valid when image hosts change.
- **Trust-fact consistency (GEO/E-E-A-T).** Lead time, certification labs (IGI vs GIA), contact email, founder names/roles, returns terms and shipping promises differ across pages — AI answers and users will quote whichever they see.
- **Publishing pipeline.** 62 scheduled items; 10 have approved packages; 6 dated items already passed; 8 await ownership confirmation; 3 await business facts (BC-005, BC-015 and the BC-004 December refresh).

## 7. Priority breakdown

| Priority | Rows | Meaning (rubric) |
|---|---|---|
| CRITICAL | 13 | Index-integrity or ranking-equity risk, a public fact that contradicts a confirmed business fact, test artifacts, or a MUST_PUBLISH time-critical calendar item |
| HIGH | 64 | Live commercial hubs/articles with clear metadata/ownership/duplication problems; high-intent or high-demand calendar items; empty indexable pages |
| MEDIUM | 49 | Useful optimization with no integrity risk; normal-priority calendar items |
| LOW | 21 | Polish, conditional/deferred pages, legacy URLs of low value |

Recommended actions: OPTIMIZE 49, REVIEW 46, CREATE 44, NO ACTION 3, REDIRECT 2, BLOCKED 2, EXPAND 1. (`KEEP`/`CONSOLIDATE` are unused on purpose: nothing is merged or kept-as-is without a human decision; items that might consolidate are `REVIEW` with `CANNIBALIZATION REVIEW REQUIRED`.)

Counts used in the executive summary (live = pages that exist today; planned = scheduled in the calendar):

| Measure | Live pages | Planned pages | Total |
|---|---|---|---|
| Metadata opportunities | 50 | 53 | 103 |
| H1 opportunities | 44 | 53 | 97 |
| Internal-link opportunities | 54 | 53 | 107 |
| Schema opportunities | 64 | 53 | 117 |
| AEO opportunities | 13 | 53 | 66 |
| GEO / entity opportunities | 16 | 53 | 69 |
| Keyword-ownership conflicts / items needing ratification | 21 | 15 | 38 |
| Cannibalization reviews | 24 | 11 | 36 |

## 8. AWS migration dependencies

Every row carries codes in `AWS Class (A/B/C)` and the text in `AWS Migration Dependency`:

- **A — SAFE TO PREPARE NOW:** metadata drafts, copy, briefs, link plans, decision memos, redirect-map entries, fact checks.
- **B — WAIT UNTIL AFTER AWS:** template/code changes (schema, breadcrumbs, noindex/sitemap rules, pagination, slug changes, redirects, image URL changes) and publishing new CMS content (the CMS store appears to be part of the Supabase→AWS move — inference; content-freeze plan UNKNOWN — VERIFY).
- **C — VERIFY AFTER MIGRATION:** status codes, canonicals, indexability, robots/sitemap, schema validity, redirects, internal links rendering, CWV vs the baseline above.

76 rows contain a template/URL-level (B) task; 53 planned pages also depend on a safe publishing window. Row-level A/B/C is a *classification*, not a block: nothing here has been implemented.

**Site-level checklist (not tied to one URL) — baseline now, verify after cut-over:**

- Keep `robots.txt` rules and AI-bot allowances; keep `Sitemap:` line; regenerate `sitemap.xml` (consider adding `<lastmod>`); remove empty/test URLs per decisions.
- Preserve HTTP semantics: 200 for sitemap URLs, `noindex, follow` + canonical on `?sort=` / `?shape=` / `?metal=`, 404+noindex for unknown paths, 307 `/contact`, 308 `/hiphop` (or deliberate replacements).
- Ship the redirect map (at minimum `/engagement-rings/by-desgin/side-stone-rings` → `/engagement-rings/by-design/side-stone-rings`) — **do not implement without a migration plan**.
- Canonical host and protocol (`www`, HTTPS) and trailing-slash behaviour must match the current site; canonical for the homepage is currently `https://www.houseofdiams.com` (no slash).
- Product/OG image URLs (Supabase + `*.r2.dev` today) change: update Product/BlogPosting `image` values, OG tags, `/llms.txt`; keep old image URLs resolvable or redirected to protect Google Images.
- Geo/currency: the site sets `detected_country`/`detected_currency` cookies from the visitor IP (this crawl from outside the US received `IN`/`INR` cookies yet showed 'United States (USD)' in the footer). Confirm Googlebot (US IPs) and US users get USD prices/schema (`priceCurrency: USD`).
- Performance: record PageSpeed/CrUX/GSC CWV for 10 template URLs before cut-over (indicative TTFB baseline in §5); HTML `cache-control: no-store` — decide the CDN caching approach on AWS.
- `/llms.txt` and any AI-crawler access rules: keep working after the move.
- GSC: confirm property type (domain vs URL-prefix) and keep the property verified through the cut-over; submit the new sitemap; watch Pages/Crawl-stats reports.

**Open questions for engineering (UNKNOWN — VERIFY):** Is there a content freeze / DB sync window? Are metadata and article edits made in the Supabase-backed CMS or in code? Will URL structure stay identical on AWS? Will the sitemap/robots generators be re-implemented? Who owns the redirect map?

## 9. Important conflicts (documented, not resolved)

| # | Source A says | Source B says | Treatment in this map |
|---|---|---|---|
| C1 | Stage 12/13/15/16 record `/engagement-rings/by-desgin/side-stone-rings` as the keyword-owner URL to keep (NO_ACTION) | Live site: that URL 404s; page moved to `/by-design/` (spelling fixed) with no 301 | Row `LEG-ER-SIDESTONE` (REDIRECT, CRITICAL). Update the research registry only after the redirect decision. |
| C2 | Stage 12 D-13: no empty/placeholder/test pages in the indexable IA | Live sitemap includes 18 empty/test pages (incl. `/hiphop/test-subcat`) | Rows marked REVIEW (HIGH) / test artifact CRITICAL; decision: noindex + sitemap exclusion or populate. |
| C3 | Stage 17/19 primary keyword vs final-calendar primary for 12 Education pages (e.g. EDU-LG-00 'synthetic diamonds' 2,900 vs 'what are lab grown diamonds' 12,100; EDU-4C-06 'diamond cut grade' vs 'diamond cut' 60,500) | Calendar primaries are mostly NOT in the Stage 15 map (new research) | Both shown; Stage 15 page ownership unchanged. See `04-…` §3 for the full list. Ratify before writing. |
| C4 | Calendar: 8 items flagged OWNERSHIP_CONFIRMATION (4 new Education pages with no Stage 14/15 owner, EDU-LG-09 co-primary, EDU-RJG-01 settings, EDU-RJG-03 care activation, BLOG-WR-TYPES Blog-vs-Education) | Stage 14/15 have no owner for them | Action REVIEW; do not write until confirmed. |
| C5 | Calendar says COM-BESPOKE owns 'custom engagement ring' (40,500) and 'design your own engagement ring' (5,400) | Stage 15 maps no commercial keyword to any COM-* page (D-19 gap) | Candidates shown on the /bespoke row as evidence only; needs ratification. |
| C6 | Stage 12 D-05: commercial Lab-Grown hub is 'conditional' | Live homepage/ER title and every PDP already position the catalogue as lab-grown; 135,000/mo 'lab grown diamonds' is unowned | Row `COM-LG-HUB` (REVIEW, HIGH): business decision needed. |
| C7 | Stage 12 proposes /contact as an indexable L1 page; FAQ copy points to houseofdiams.com/contact | Live: /contact is a 307 to a modal and is no longer in the sitemap | Row `BRAND-CONTACT` (REVIEW). |
| C8 | Confirmed HOD fact: bespoke ≈ 2–3 weeks to make + 6–9 days delivery (~3–4 weeks, stone-dependent) | Live /bespoke: '4-6 week typical lead time' | Row `COM-BESPOKE` CRITICAL (copy fix). |
| C9 | Stage 13: /faq NO_ACTION; Stage 14 D14-30: FAQ topic answers should be one line + link | Live FAQ answers lab-grown vs natural, CVD vs HPHT, 4Cs in full | Row `SUP-FAQ` flagged. |
| C10 | Business facts still open (progress.md): certification labs, shipping cut-offs, platinum availability, cleaning/appraisal | Live pages assert 'IGI Certified', 'IGI / GIA', 'Complimentary Overnight Shipping', 'Lifetime Warranty' | Flagged on home, bespoke, shipping, returns, PDP rows — verify before keeping or copying into metadata. |
| C11 | Stage 15 registry lists `/shop/oval-floral-diamond-ring` as the 'marquise oval diamond' owner | Product renamed 'Oval Marquise Side-Stone Engagement Ring' (slug unchanged) | Row `COM-PDP-OVAL-FLORAL`. |
| C12 | Blog drafts' seo-metadata.md say the template emits non-ISO dates, no BreadcrumbList, author=Person | Live crawl: dates are ISO, no BreadcrumbList, author=Person (names vary) | Partly confirmed; ISO point not reproduced on live articles — VERIFY on a CMS-generated post. |
| C13 | Housekeeping | A second copy of the research project exists at `~/Desktop/HOD-SEO-Research` (identical content except `.git`/`.env`); a `.env` file sits in the `HOD SEO` repo root (a `.gitignore` containing `.env` appeared during this session — still untracked, not yet committed) | Pick one source of truth; commit the `.gitignore` so `.env` can never be committed (CLAUDE.md security rule). `.env` was not read or modified. |

## 10. Next actions

1. **Decide (you):** redirect map + the empty/test-page policy (C1, C2) so it can go into the AWS migration plan; Bespoke lead-time correction (C8); whether a crawlable /contact page and a commercial Lab-Grown hub will exist (C6, C7).
2. **Approve (you):** ratification of commercial keyword ownership using the candidate lists already in the CSV (zero paid cost); only if you want SERP validation of the commercial heads, request a priced DataForSEO plan first (CLAUDE.md approval flow) — not run here.
3. **Confirm (you):** the open business facts (certification labs, shipping/returns terms, founder names/roles, Hip Hop range) and the 8 ownership confirmations in the calendar.
4. **Ask engineering:** content-freeze/sync window, who edits metadata (CMS vs code), whether URLs stay identical, and where GSC/CrUX baselines can be captured before cut-over.
5. **Prepare now (SEO, safe):** apply the A-column tasks — metadata/copy drafts, link plans, briefs for the 20 new Education pages, redirect-map spreadsheet, GSC export request (Pages + Queries, 16 months) to fill the NOT AVAILABLE columns.
6. **After AWS:** run the C-column verification checklist, then execute the B-column items in priority order (`03-SEO-IMPLEMENTATION-PRIORITIES.md`).

## 11. How to use the CSV

Filter `Row Group` for a page family, `Priority` + `Recommended Action` for the work queue, `AWS Class (A/B/C)` for timing, and the `Flag:` columns (Y) for counts. Columns 1–50 follow the specification exactly; 13 helper columns follow. Every cell with unverifiable content says `UNKNOWN — VERIFY` or `NOT AVAILABLE`.
