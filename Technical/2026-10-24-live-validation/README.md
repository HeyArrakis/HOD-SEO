# Live validation record — 2026-10-24

**Type:** fresh, dated, read-only check of the public site after the reported AWS migration. It supplements, and does not replace, the 2026-10-09 baseline in `QA/_build/evidence/` (unchanged).
**Method:** `curl` GET/HEAD requests only (no forms, logins, carts or payments), user-agent `HODSEOAudit/1.0; read-only`, 4 parallel workers. Nothing on the site was changed.
**Vantage point:** one location (India, IPv4). Currency/country cookies are set from IP; US behaviour was tested only by sending `detected_country=US; detected_currency=USD` cookies, not from a US IP.

## Files

| File | Content |
|---|---|
| `sitemap_2026-10-24.xml` | The live sitemap as fetched (261 URLs, apex host, no `<lastmod>`) |
| `crawl_2026-10-24.json` | 287 responses: every sitemap URL plus probes (status, redirect, canonical, meta robots, title, meta description, H1, schema types, currencies, TTFB, internal links, headers) |
| `targeted_probes_2026-10-24.json` | Empty-listing check (15 pages), trust-page keyword counts, robots/llms.txt hosts, homepage and PDP host/image checks, PDP currency under three cookie variants |
| `planned_path_probes_2026-10-24.json` | HTTP status of the documented planned paths (10 published blog posts → 200; 6 Education paths → 404) |
| `_scripts/crawl_validate.py`, `_scripts/probe2.py` | The scripts used (pass an output folder as argument; do not overwrite this folder — create a new dated one) |

## Key findings (full list in `DEVELOPER-HANDOFF/03-DEVELOPER-REMAINING-FIXES.csv`)

**Confirmed changed since 2026-10-09**
* Every response is served via CloudFront in front of nginx (Ubuntu); images come from `media.houseofdiams.com`; no Supabase/R2 references in the JSON-LD of any crawled page.
* Preferred host is now the apex `houseofdiams.com` (canonicals, sitemap, robots `Sitemap:` line, llms.txt); `www` still answers 200 with a canonical to the apex and no redirect.
* Sitemap 256 → 261 URLs: ten blog posts added (BC-001, 003, 004, 006, 007, 008, 009, 018, 035, 036) and `/fine-jewellery/bracelet/tennis-bracelet`; removed `/hiphop/chains`, `/hiphop/chains/cuban-links`, `/hiphop/test-subcat`, two PDPs and `/fine-jewellery/bracelet/tennis` (now a 301). Test sub-category and the two Hip Hop children return 404.
* Article schema: BlogPosting + BreadcrumbList on 21 articles; Organization author on 19 (two older articles still use a Person).
* All 180 analysed PDPs output `priceCurrency: USD` in server-rendered JSON-LD under default, US and India cookies.

**Confirmed unchanged / still open**
* The nine `/engagement-rings/by-desgin/*` URLs still return 404 (no 301).
* 15 empty listings (`0 pieces`) are still indexable and in the sitemap.
* `/engagement-rings/by-design` is still self-canonical and in the sitemap.
* FAQPage on 35 pages; boilerplate metas on 42 pages; 63 PDP titles over 60 characters.
* `/shipping` still shows test text; `/returns` has no return window; `/bespoke` still contains a "4–6" week lead time; the homepage still contains IGI / Certified / Lifetime / Overnight wording; `/contact` is still a 307.

**Needs a decision / alert**
* BC-001 is live and says "6–9 days of insured shipping" although publication was held pending HOD confirmation.
* Host choice (apex vs www) and the `tennis-bracelet` slug are not part of the approved plan.

**Limits**
* Interactive behaviour (checkout, login, WhatsApp link, keyboard order, coupon quiz, search suggestions), JavaScript-injected analytics tags, rendered-page content and Core Web Vitals were not testable with HTTP fetches. Two PDPs returned 502 during the parallel crawl and 200 on retest.
* Googlebot-specific rendering and GSC indexing state were not checked (no GSC data).
