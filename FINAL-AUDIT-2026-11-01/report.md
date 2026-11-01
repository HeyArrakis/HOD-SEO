# House of Diams — Final SEO Audit Report

**Site:** https://houseofdiams.com · **Date:** 1 November 2026 · **Market:** United States (US English)
**Scope:** the full brief in `00-AUDIT-PROMPT.md`.
- All 246 sitemap pages, plus 20 probes, crawled.
- Lighthouse on 14 templates, mobile and desktop.
- Search Console, GA4, Tag Manager, Ahrefs, Merchant Center and Business Profile read in the owner's Chrome.
- Storefront and admin code reviewed.
- Every project spec checked against the live site.

**Evidence:** `Technical/2026-11-01-live-validation/` (crawl, spec comparison, probes, deep scan, `full_audit_2026-11-01.json`, Lighthouse JSON, `platforms_2026-11-01.md`).
**Fixes:** every issue below has an ID that matches `changes.md`.

---

## 1. Total SEO score: **63 / 100**

The site's **foundation is now strong**:
- Clean indexing signals, unique metadata, schema on every template.
- AI crawlers allowed; accessibility 96–100; Ahrefs site health 100.

**Results are held back by four things:**
1. Almost no genuine backlinks (Domain Rating 4).
2. Slow mobile pages (LCP 4.6–7.2 s on shopping templates).
3. Too little published content: 21 articles and 1 Education page, against 62 planned.
4. Tracking that can't measure sales: no ecommerce events reach GA4, and the Merchant Center return policy is rejected.

Today almost all search clicks are brand searches: **143 of 149 clicks; non-brand gets 6 clicks from 12,411 impressions**. Fixing the four points above is what turns impressions into visits.

### Score by area (weighted)

| # | Area | Weight | Score | Weighted | One-line reason |
|---|---|---|---|---|---|
| 1 | Technical SEO | 18 % | **80** | 14.4 | All 246 URLs 200 + indexable + self-canonical, `lastmod`, robots and filters correct, www 301. Missing: HTML caching (TTFB ≈ 1 s), 301s for old URLs, apex sitemap in GSC, slug-change redirects |
| 2 | Performance & Core Web Vitals | 12 % | **55** | 6.6 | Mobile Performance 38–89 (median ≈ 66), mobile LCP 4.6–7.2 s on commerce pages, product pages 14–22 MB (video), `/engagement-rings` TBT 5.2 s. CLS 0. No field data yet |
| 3 | On-page SEO | 14 % | **78** | 10.9 | Unique titles/metas/H1 everywhere, 49/54 spec titles live. The ranking articles still use their first paragraph as the meta, 13 blog titles > 60 characters, 3 boilerplate + 9 short metas |
| 4 | Content & keyword strategy | 14 % | **55** | 7.7 | Excellent research and 10 correct blog packages, but 11 calendar items are overdue (incl. the must-publish "What are lab-grown diamonds?"), Education has 1 article, the main topics rank at position 26–40 |
| 5 | Internal linking & architecture | 8 % | **68** | 5.4 | All 52 specified links live, breadcrumbs everywhere. Blog posts get 1 internal link each, Education hubs not built, 13 links to empty pages |
| 6 | Structured data | 8 % | **72** | 5.8 | Full Organization/WebSite/Breadcrumb/ItemList/Product/BlogPosting set. Errors: `deliveryTime` missing (182 pages), duplicate `material`, 249-country lists (15 KB per page) |
| 7 | AI search visibility (GEO/AEO) | 7 % | **65** | 4.6 | All AI bots allowed, Ahrefs AI Discoverability 100, **ChatGPT already sends 46 sessions/month**. Thin `llms.txt`, weak entity (no reviews, no knowledge-panel signals, almost no citations) |
| 8 | Off-page & backlinks | 7 % | **12** | 0.8 | DR 4; GSC sees 5 links from 3 sites; 46 of the top 50 linking domains are spam; outreach not started |
| 9 | Local SEO & entity | 4 % | **45** | 1.8 | Business Profile verified with products, but no phone, "Open 24 hours", 0 reviews, no photos, no citations |
| 10 | Measurement & tracking | 4 % | **55** | 2.2 | GSC + GA4 + Merchant Center + Bing connected; but no ecommerce/lead events in GA4, INR currency, internal traffic unfiltered, only the www sitemap submitted, return policy rejected |
| 11 | UX, accessibility, trust & QA | 4 % | **75** | 3.0 | A11y 96–100, Agentic 100, no console errors. Best Practices fell to 77 (cookies before consent); "overnight / same-day / 24 hours" wording still contradicts the facts |
| | **Total** | **100 %** | | **63.2 → 63** | |

**Scoring method:** each area was scored against a checklist of what a well-optimized luxury e-commerce site has, from 0 (absent) to 100 (best practice, fully applied). Weights reflect how much each area moves organic and AI visibility for e-commerce, with technical, on-page and content weighted highest. Search results (clicks, positions) are reported as KPIs in §4, not scored, because they lag the fixes by weeks.

### Platform scorecards (each /100, not part of the total)

| Platform | Score | Why |
|---|---|---|
| Google Search Console health | **60** | Verified domain property; no manual actions or security issues; merchant listings, product snippets and breadcrumbs 0 invalid. But 453 "not indexed" (mostly old www and image URLs; about 50 real pages "crawled, not indexed"), only the www sitemap submitted, no Core Web Vitals data yet, 5 old blog URLs 404 without redirects |
| GA4 tracking | **45** | Page views and sessions work; **no `view_item` / `begin_checkout` / `purchase` / `generate_lead`** reach GA4 (Tag Manager has no event tags); currency INR; internal (Surat/Satara) traffic and `accounts.google.com` referrals pollute the data |
| Merchant Center | **70** | 236 products, all approved, 90 free-listing clicks in 28 days. **Return policy Rejected** (35 % restocking fee not on the site), about 54 extra products not in the site feed, store-quality "missing signals" in the US, AU and IN |
| Ahrefs | Health **100** · Authority **4** | Site Audit 100 and AI Discoverability 100 (apex). Domain Rating 4; new "rich results validation error" on 182 product pages; old www project 69 (archive it) |
| Lighthouse (lab) | **74** | Average of Perf (mobile ≈ 66, desktop ≈ 78), A11y ≈ 99, Best Practices 77, SEO 100, Agentic 100 |
| PageSpeed (field / CrUX) | **Not measured** | Google has no field data for the site yet, and the PageSpeed API quota was exhausted. Field data appears once traffic grows |
| AI readiness | **70** | Bots allowed, clean HTML, answer-first articles, entity data, ChatGPT referrals. Missing: fact-rich `llms.txt`, reviews, third-party citations, Education hubs |
| Google Business Profile | **45** | Verified with products; missing phone, real hours, photos, reviews, description check |

---

## 2. What to do first (top 12, in order)

| # | Action | ID in changes.md | Owner | Expected effect |
|---|---|---|---|---|
| 1 | Add GA4 event tags in Tag Manager and set consent on Clarity and Pinterest | D-01, D-02 | Developer / owner | Sales and leads become measurable; Best Practices back to 100; consent compliance |
| 2 | Fix the rejected Merchant Center return policy (remove or confirm the 35 % fee) and clean the 54 extra products | D-05, F-01 | Owner | Restores return info on free listings, which already bring 90 clicks/month |
| 3 | Submit the apex sitemap in GSC; "Validate fix" on merchant listings | D-04 | Owner | Faster move of the www impressions to apex URLs |
| 4 | Remove the hard-coded "overnight / same-day / 24 hours / Ready to Ship" wording | A-01 | Developer | Claims match the facts; trust and AI answers stay correct |
| 5 | Fix product schema: one `material`, `itemCondition`, a short country list, `deliveryTime` once the courier is known | A-02, F-02, F-03 | Developer / owner | Clears the 182-page rich-results error and the GSC warning; cuts 15 KB per product page |
| 6 | Apply the spec metas and H1s to the 8 ranking articles (baseline now captured) and fix the "how to layer necklaces" snippet | E-01, E-08 | Claude in the CMS (owner OK) | CTR on 10k+ monthly impressions; the necklace page ranks #3 with 0 clicks |
| 7 | Publish the 11 overdue calendar items, starting with "What are lab-grown diamonds?" and the Black Friday / Christmas posts | E-05 | Claude writes, owner reviews | Topical depth; seasonal demand in November–December |
| 8 | Mobile speed: product video, prefetch storm, duplicate API calls, fonts, listing JavaScript | A-05, A-06 | Developer | LCP target < 2.5 s; mobile Perf ≥ 85 |
| 9 | Cache public HTML at CloudFront | A-04, C-03 | Developer | TTFB from ≈ 1 s to < 200 ms |
| 10 | 301 the old 404/5xx blog URLs; add a redirect manager and auto-301 on slug change in the admin | A-03, B-01, B-02 | Developer | Keeps link equity; prevents future breakage |
| 11 | Business Profile: phone, hours, photos, description, first reviews | D-07, F-06, F-08 | Owner | Local and brand trust; review stars help AI and Shopping |
| 12 | Start link building with the plan in `Off-page SEO/` (PR, jewelry and wedding directories, supplier and partner pages) and stop worrying about the spam links (no disavow needed without a manual action) | G-02, F-09 | Owner / SEO | DR and non-brand rankings |

---

## 3. Findings by area

### 3.1 Technical SEO — 80/100
**Good**
- **Sitemap:** 246 URLs, all return 200, are indexable and self-canonical, and have `lastmod`. No noindex or non-200 URLs in it.
- **Hosts and redirects:** `www` → apex in one 301 on https. `by-desgin` → `by-design` 301s are live.
- **Filters and pagination:** `?sort/?metal` URLs are `noindex, follow` with a clean canonical. `/shop?page=2` is self-canonical. `/blog?page=2` → `/blog` (correct, single page).
- **robots.txt:** allows Googlebot, OAI-SearchBot, ChatGPT-User, GPTBot, Google-Extended, ClaudeBot, Claude-SearchBot and PerplexityBot. Private routes are disallowed and the sitemap is declared.
- **Security headers:** HSTS, X-Frame-Options, nosniff, Referrer-Policy, Permissions-Policy, CSP (report-only).
- **Deploys:** old JS chunks now survive a deploy (T-03 fixed). No 5xx anywhere today.

**Issues**
- HTML is never cached (`private, no-store`, CloudFront Miss on 246/246). TTFB median 0.97 s, p90 1.27 s, max 3.2 s. HTML median 434 KB (the RSC payload). → **A-04, C-03**
- 5 old blog URLs that Google still knows (they returned 5xx) now return **404 with no 301**. Also `/b2b` (404, the page calls `notFound()`), `/shop/produt-1` (301 to a category instead of 404/410), and timestamped old product slugs. → **A-03, F-07**
- Only the www sitemap is submitted in GSC. → **D-04**
- Admin renames change slugs with no 301, and there is no redirect manager. → **B-01, B-02**
- `http://www` takes 2 hops (T-01); the media host root returns 403 (T-12). → **C-01, C-02**
- `X-Powered-By: Next.js` header; CSP still report-only. → **A-11**
- 13 links (on category, sub-category and home pages) point to empty `noindex` listings. → **A-07**

### 3.2 Performance — 55/100

Lighthouse 13.6, 1 November:

| Template | Mobile Perf | Mobile LCP | Desktop Perf | Weight |
|---|---|---|---|---|
| Home | 66 | 5.8 s | 70 | 1.5–2.2 MB |
| /shop | 66 | 6.1 s | 75 | 1.4 MB |
| /engagement-rings | **38** | 6.5 s (TBT **5.2 s**) | 73 | 1.7 MB |
| /fine-jewellery | 63 | **7.2 s** | 78 | 1.9–2.1 MB |
| Category (tennis) | 65 | 6.1 s | 81 | 1.5 MB |
| PDP bracelet / earrings | 63 / 69 | 5.2 / 4.6 s | 69 / 78 | **17–22 MB desktop, 14 MB mobile** |
| /blog / article | 54 / 84 | 4.8 / 2.4 s | 75 / 85 | 1.2–1.5 MB |
| /education | 68 | 5.3 s | 77 | 1.2 MB |
| /bespoke · /about · /contact · /faq | 65 · 72 · 89 · 88 | 5.9 · 5.1 · 2.4 · 2.3 s | 78 · 80 · 84 · 84 | 1.1–1.8 MB |

CLS is 0 everywhere.

**Causes and fixes:**
- **Product video:** 14–22 MB on product pages. → **A-06**
- **Prefetch and duplicate calls:** about 25 menu-route prefetches on every page load; `settings`, `footer-content` and `promotion-popup` each fetched twice; an empty product search on every page. → **A-05**
- **Fonts:** 5 font families loaded sitewide. → **A-05**
- **JavaScript:** 190–240 KB unused; main-thread work 3–11 s on mobile. → **A-05**
- **Server:** no HTML caching. → **A-04**

**Field data:** none yet (CrUX). The target is LCP < 2.5 s, INP < 200 ms and CLS < 0.1 at the 75th percentile once data appears in GSC.

### 3.3 On-page SEO — 78/100
**Good**
- Every indexable page has one H1, a unique title, a unique meta description and a canonical.
- `og:` and `twitter:` tags are on every page.
- No image is missing an `alt` attribute (the 6,374 empty `alt=""` are decorative hover images and icons, which is correct).
- 49 of 54 "ready" spec titles are live; product SEO titles were shortened on 31 Oct.

**Issues**
- **Ranking articles with untargeted metadata.** These have Search Console data and were waiting for a baseline. Their meta is the first paragraph and some H1s differ from the spec. → **E-01**

  | Article | Impressions | Position |
  |---|---|---|
  | Lab-grown vs natural | 6,256 | 26.5 |
  | 14K vs 18K | 1,142 | 11.6 |
  | Ring size | 1,049 | 27.5 |
  | CVD vs HPHT | 921 | 32.5 |
  | Diamond shapes | 845 | 8.2 |
  | 4Cs | 321 | 8.7 |
  | IGI certification | — | — |
  | How to choose | — | — |

- "How to layer necklaces" ranks **#3.3 with 172 impressions and 0 clicks**: the snippet doesn't earn the click. → **E-08**
- 13 blog titles are 61–78 characters, so they're truncated in results. → **E-02**
- 3 boilerplate metas ("Browse … in …": `/wedding-bands/for-her`, `/fine-jewellery/bracelet/bangles`, `/fine-jewellery/necklaces/pendant-necklace`) and 9 short metas (31–68 characters). → **E-03**
- The bangles page still says "Bangles"; it waits for the owner's new name. → **F-04, B-04**
- Oval floral product page spec (OD-15) not applied; it was waiting for the baseline, which is now captured. → **E-04**
- `/contact` title is 27 characters (fine; the brand suffix makes it 44).

### 3.4 Content & keyword strategy — 55/100
**Good**
- Stages 1–19 research: 1,936 keywords mapped to owners, clusters, SERP/PAA/AIO capture, briefs and boundaries.
- All 10 blog packages are live and correct (title, meta, H1, canonical, links, blog index).
- No keyword cannibalization in titles or H1s (0 duplicates).
- E-E-A-T: Organization author, founders, address and facts are now consistent.

**Issues**
- **Volume.** 21 blog URLs and **1 Education article** are live. The calendar had 62 items scheduled by 30 March; **21 were due by 1 Nov and 11 are not live**:

  | Item | Due | Note |
  |---|---|---|
  | BC-011 | 16 Oct | |
  | BC-037 | 19 Oct | |
  | BC-014 | 20 Oct | |
  | **EDU-LG-00 "What are lab-grown diamonds?"** | 21 Oct | MUST_PUBLISH |
  | BC-015 | 22 Oct | Needs facts |
  | BC-024 | 23 Oct | |
  | BC-016 | 26 Oct | |
  | BC-017 | 27 Oct | |
  | EDU-RJG-BR | 28 Oct | |
  | BC-005 | 29 Oct | Now possible: the owner confirmed in-house cutting |
  | BC-019 | 30 Oct | Black Friday |

  32 more items are due in November–December. → **E-05**
- **Rankings.** The topic with the most demand (lab-grown vs natural, about 4,000 impressions across variants) sits at position 26–31. The 6 Education hubs and 19 Education drafts are unpublished, so the site has no hub ↔ spoke depth for Google to trust. → **E-05, E-09**
- **Categories.** Category pages have no intro or buying-guide copy (364–659 words, mostly product cards). The owner said to leave this for now. → **E-06 (on hold)**
- **Non-brand clicks.** 6 in 3 months. 181 non-brand queries already rank 4–10 and 119 rank 11–20; these are the quickest wins. → **E-01, E-08, E-09**

### 3.5 Internal linking & architecture — 68/100
**Good**
- All 52 specified internal links are live.
- Breadcrumbs (visible and schema) on 246/246 pages.
- Menu hides empty listings; By-Design canonicals are correct.

**Issues**
- Most blog posts get **one internal link** (from `/blog`). Related-post and product modules don't add crawlable links to other articles, and category pages don't link to the guides. → **A-13, E-09**
- 6 product pages are reachable only from listing page 2+ (fine for crawling, but weak). Education hubs return 404, so there is no topic hub. → **E-05**
- 13 links to empty `noindex` listings from category and sub-category grids. → **A-07**

### 3.6 Structured data — 72/100
**Good**
- **Organization:** address, phone, email, logo and sameAs; founders as Person.
- **WebSite, BreadcrumbList and ItemList** where they belong.
- **Product + Offer** on 182 product pages, with price in USD, availability, brand, SKU, `shippingDetails` and `hasMerchantReturnPolicy`.
- **BlogPosting** with an Organization author.
- **FAQPage** only on `/faq`.

**Issues**
- `deliveryTime` is missing in `shippingDetails`, which Ahrefs flags as a rich-results error on all 182 product pages. It needs the owner's courier and handling days. → **A-02, F-02, F-03**
- `material` is an array of 6 metals (GSC: "Duplicate field 'material'"). Use a single value, or `ProductGroup` + `hasVariant`. → **A-02**
- Each product lists all 249 countries twice (about 15 KB of JSON-LD). Define the policies once at Organization level, or list the main markets. → **A-02**
- No `itemCondition`. No reviews or ratings (only add them when real reviews exist). → **A-02, F-08**

### 3.7 AI search visibility — 65/100
**Good**
- All AI crawlers are allowed, and `llms.txt` and `llms-full.txt` exist.
- Ahrefs AI Discoverability scores 100.
- Articles are answer-first, and the entity facts are consistent across the site and schema.
- **GA4 shows chatgpt.com sending 46 sessions** in 28 days, so the brand is already cited in ChatGPT answers.

**Issues**
- `llms.txt` is mostly a product list. It has no "key facts" block and no links to the buying guides or Education. → **A-08**
- The entity is weak outside the site: no reviews, almost no third-party mentions, and the brand name is easily confused with "House of Diamonds". → **G-01, G-02, F-08**
- No Education hub pages, which are the pages AI tools most like to cite. → **E-05**

### 3.8 Off-page & backlinks — 12/100
- Ahrefs: Domain Rating **4**, 734 "referring domains", but **46 of the top 50 by DR are spam link farms** (buybacklinks.agency, seoexpress.shop …). They are mostly nofollow and ignored by Google. There's no manual action, so **no disavow is needed**; keep monitoring. → **F-09**
- GSC counts 5 real external links from 3 sites. The backlink research (77-row database, outreach queue, brand sheet) exists in `Off-page SEO/`, but **outreach has not started**. → **G-02**

### 3.9 Local SEO & entity — 45/100
- The Google Business Profile is **verified**, with category "Jewelry manufacturer", a service area, the website and synced products.
- **Missing:**
  - the phone number;
  - real hours (it shows "Open 24 hours"; the HQ is by appointment);
  - photos and reviews;
  - the description (check it);
  - one pending "Google update" to review;
  - a Business Profile link in the Organization `sameAs`.
- **Citations:** none found. NAP is consistent on the site and in schema (Surat address, +91 93285 36178, admin@). → **D-07, F-06, A-20**

### 3.10 Measurement & tracking — 55/100
- **Connected and working:**
  - Search Console (domain property).
  - GA4 (page views, sessions, scroll, add_to_cart until 31 Oct).
  - Merchant Center (236 approved).
  - Bing and Pinterest verification; Microsoft Clarity.
- **Broken or missing:**
  - Tag Manager has only 4 tags and **no GA4 event tags**. → **D-01**
  - Clarity and Pinterest fire before consent. → **D-02**
  - GA4 currency is INR; there's no internal-traffic filter and no referral exclusions. → **D-03**
  - Only the www sitemap is submitted. → **D-04**
  - The Merchant Center return policy is rejected. → **D-05**

### 3.11 UX, accessibility, trust & QA — 75/100
- **Lighthouse:** Accessibility 96–100, Agentic 100 on every template (the product page went from 2/3 to 3/3 after change.md), SEO 100.
- **QA:**
  - No console errors on home, category or product pages.
  - No failed requests (only cancelled prefetches).
  - The cart and bracelet-length flow work.
  - Capitals and "Add To Bag" wording are correct.
- **Issues:**
  - Best Practices dropped from **100 to 77** because of third-party cookies before consent. → **D-02**
  - The "Select Bracelet Length" placeholder contrast is 3.05:1. → **A-09**
  - The top-bar link contrast on home mobile. → **A-10**
  - Hard-coded claims contradict the owner's answers: "Complimentary Overnight Shipping" (home strip and checkout), "same-day overnight dispatch" (`/shipping`, cart), "Ready to Ship", "replies within 24 hours" (contact panel on every page). → **A-01**

---

## 4. KPIs: baseline and 90-day targets

| KPI | Baseline (1 Nov 2026) | Target by 1 Feb 2027 |
|---|---|---|
| Non-brand search clicks / 3 months (GSC) | 6 | 300+ |
| Non-brand queries in top 10 | 201 | 400 |
| Average position, "lab grown vs natural" cluster | 26–31 | ≤ 10 |
| Merchant Center free-listing clicks / 28 days | 90 | 250 |
| ChatGPT/AI referral sessions / 28 days (GA4) | 46 | 100 |
| Mobile LCP on commerce templates (lab) | 4.6–7.2 s | < 2.5 s |
| Domain Rating (Ahrefs) / real referring domains | 4 / ≈ 3 | 15 / 30 |
| GA4 purchases and leads tracked | 0 | 100 % of orders and forms |
| Google reviews | 0 | 20+ |
| Live Education pages | 1 | 15+ |

---

## 5. Not measured, and why
- **Core Web Vitals field data:** none exists yet for the site, and the PageSpeed API quota was used up. Re-check in GSC → Core Web Vitals monthly.
- **AI Overview / AI Mode presence per keyword:** no rank tracker on the Ahrefs free plan. ChatGPT referrals in GA4 are the measurable proxy.
- **Full checkout up to payment:** not run, by rule (no real orders).
- **Bing Webmaster Tools reports:** verification tag present; the account was not opened.

## 6. Files
- `00-AUDIT-PROMPT.md`: the brief.
- `changes.md`: every fix, by owner and priority. It supersedes `DEVELOPER-HANDOFF/05`.
- `Technical/2026-11-01-live-validation/`: evidence (crawl, probes, scans, Lighthouse, platform snapshot).
