# 05 — Final Pre-Delivery Master Fix List (technical SEO, on-page, QA, performance, analytics)

**Date:** 2026-10-29 · **Site:** https://houseofdiams.com (canonical host = apex) · **Prepared for:** the developer, to hand directly to Claude Code.
**Evidence:** `Technical/2026-10-29-live-validation/` (full crawl of 246 sitemap URLs + probes, deep schema/text scan, Lighthouse 13.6 on 11 templates × mobile/desktop), live browser QA (desktop + 375 px mobile), Ahrefs Site Audit (both projects, crawls of 28 Oct), Google Search Console (domain property), GA4 (property "House of Diams").
**Not tested on purpose:** the payment step and order placement (the owner tests these). No form was submitted, no message sent; test bags were emptied afterwards.

---

## PART A — PROMPT FOR CLAUDE CODE (copy everything from here to the end of the file)

You are working in the House of Diams website codebase (Next.js App Router behind nginx + CloudFront on AWS; media on `media.houseofdiams.com` / `content.houseofdiams.com`; GTM `GTM-TJ5HTTSD`, GA4 `G-0LVQJ1YDJ0`). Implement every item in Part C, in the priority order given, then run the acceptance checks in Part E.

**Rules — follow exactly:**
1. **Do not invent business facts.** Customer-facing copy may only state the facts in Part B. If a fix needs a fact that is not in Part B, leave the text out (do not guess) and list it in your final report under "Needs HOD".
2. **Do not touch payment/checkout logic** (Razorpay, order creation, pricing, tax calculation). Text/labels on the cart page are in scope; payment code is not.
3. **Do not change any URL slug** except where an item says so. Every URL that stops returning 200 must get a 1:1 301 to its replacement. Never 302/307 for permanent moves.
4. **No test content on production.** Test products/articles/categories must stay unpublished, excluded from the sitemap, `noindex`, and out of listings/search/related items. Do QA on a staging host that sends `X-Robots-Tag: noindex` and is not linked from production.
5. **American English** in all customer-facing copy, nav labels, alt text and anchors ("jewelry", "color", "center" — never "jewellery/jewelery/jwelery"). Do **not** rename the `/fine-jewellery/` URLs.
6. **Do not add FAQPage schema** anywhere except `/faq` (already correct). Do not fabricate reviews/ratings, GTINs, awards, or certifications in schema.
7. Keep changes small and reviewable: one commit per item ID (e.g. `fix(T-01): www→apex 301`). Do not refactor unrelated code.
8. After each P0/P1 item, run the item's **Done when** check yourself and paste the result into your report.

---

## PART B — Confirmed HOD facts (the only claims allowed on the site)

| Topic | Approved wording basis |
|---|---|
| Shipping | Free shipping to every country; every order is insured; same-day overnight shipping; no order cut-off time |
| Returns | Returns within **15 days** of delivery, unworn; refund issued once the piece reaches HOD; return shipping and duties paid by the customer. Bespoke/custom pieces are not returnable unless the finished piece does not match the agreed design |
| Certification | IGI and GIA certificates |
| Services | Free resizing; free annual cleaning |
| Warranty | "Free lifetime warranty" may be shown (no terms published yet). **Remove** "craftsmanship warranty" and any "lifetime buyback" wording |
| Bespoke timing | Typically 2–3 weeks to make + about 6–9 days delivery; about 3–4 weeks from design approval; depends on the selected stone; estimates, not guarantees |
| Company | Founders Krish Babariya and Akshar Korat; in the trade since 2014 ("a decade in the trade" OK); public email **admin@houseofdiams.com** only |
| Social | Instagram `https://www.instagram.com/houseofdiams_/`, Facebook `https://www.facebook.com/profile.php?id=61593287138869`, Pinterest `https://in.pinterest.com/HouseofDiams_/` |

**NOT confirmed — remove or hide until HOD confirms:** the New York address "36 W 44th Street, Suite 1000B, New York 10036" (see L-01), "UPS" as the carrier, "40+ countries", "Established networks in 20+ countries", "Conflict Free" / "Ethically" claims, "In-stock pieces usually ship within 2–3 business days", any promo/sale not currently running.

---

## PART C — FIX LIST

Priority: **P0** = must fix before delivery (blocks indexing, tracking or trust) · **P1** = needed for the 100/100 targets · **P2** = polish.

### C1. Why Ahrefs shows two different scores (answer + fix)

You have two Ahrefs projects for the same site:

| Project | Score | What it crawls | Why |
|---|---|---|---|
| `www.houseofdiams.com` | **69 %**, 312 URLs with errors (+306) | the `www` host | `www` is still a full copy of the site (HTTP 200, no redirect). During its crawl (28 Oct, 10:17 PM) **8 core JavaScript chunks returned 500/502** from the origin. Every page loads those chunks, so Ahrefs flagged **"Page has broken JavaScript" on 304 pages** and **"JavaScript broken" on 8 files**. The other issues come from the `www` pages canonicalising to the apex ("Canonical URL changed" 291, "Indexable page became non-indexable" 269) |
| `houseofdiams.com` | **100 %**, 0 errors | the apex host (the canonical one) | Its crawl an hour later got 200s for the same JS files. It still has **30 warnings/notices** (C2 list) |

**Root causes found:**
1. **CloudFront is not caching `/_next/static/*`.** Every request for immutable JS/CSS is `X-Cache: Miss from cloudfront` and goes to nginx/Next.js (0.3–1.9 s per file, measured 29 Oct). Under a crawler's burst the origin returned 500/502. Real visitors can hit the same failure during traffic spikes or deploys.
2. **`www` is not redirected to the apex.** Google still ranks the `www` URLs (Search Console: homepage 165 clicks on `www` vs 9 on apex; the top blog posts are all `www`). Ahrefs reports **"Non-canonical page receives organic traffic"** for `www` URLs.

**What to do in Ahrefs after T-01 and T-02 are live:** run a new crawl of the apex project, then delete (or archive) the `www` project. Once `www` 301s, that project can only show redirects. Score yourself on the apex project.

### C2. Technical SEO

| ID | Pri | Item | Current (evidence) | Fix | Done when |
|---|---|---|---|---|---|
| T-01 | **P0** | `www` → apex 301 | `https://www.houseofdiams.com/*` returns 200 (same HTML, canonical → apex). `http://www…` → `https://www…` → (200), a 2-hop chain. GSC: ranking URLs are `www` | One rule at CloudFront (Function on viewer-request) or nginx: any request with `Host: www.houseofdiams.com` (http or https) → **301** to `https://houseofdiams.com` + same path + same query. `http://houseofdiams.com/*` → 301 to https apex (already OK). Single hop from every variant | `curl -sI https://www.houseofdiams.com/shop?page=2` → `301` `location: https://houseofdiams.com/shop?page=2`; `curl -sI http://www.houseofdiams.com/x` → one 301 straight to `https://houseofdiams.com/x` |
| T-02 | **P0** | Cache static assets at CloudFront | `/_next/static/*`, `/_next/image*`, `media.*`, `content.*` all `Miss from cloudfront` on repeat requests; origin returned 500/502 to Ahrefs | Add cache behaviors: `/_next/static/*` → managed policy **CachingOptimized** (no cookies, no query strings, no headers forwarded except Accept-Encoding); `/_next/image*` → cache on `url,w,q` query keys + `Accept` header; media/content buckets → CachingOptimized with `Cache-Control: public, max-age=31536000, immutable`. Enable Brotli/Gzip compression on the distributions | Second request to any `/_next/static/chunks/*.js` returns `x-cache: Hit from cloudfront`; 200 parallel requests (`xargs -P 50`) to the JS chunks return 0 non-200 |
| T-03 | **P0** | Keep old chunks available across deploys | Ahrefs/GSC saw 5xx on `www` blog pages on 23–24 Oct and on JS chunks on 28 Oct (deploy windows) | Keep the previous build's `/_next/static` assets for ≥7 days after each deploy (upload to S3/static origin, don't delete on deploy). Unknown chunk → **404**, never 500 | A chunk URL from the previous build still returns 200 after a new deploy |
| T-04 | **P1** | HTML caching / TTFB | Every HTML response is `cache-control: private, no-cache, no-store` and sets `detected_country/currency` cookies → TTFB ≈ 1.0–1.3 s (median 0.99 s, max 3.4 s); blocks back/forward cache on every page (Lighthouse `bf-cache` fails on all 22 runs) | Serve public pages (home, categories, PDPs, blog, education, policy pages) with ISR/`revalidate` + `Cache-Control: public, s-maxage=300, stale-while-revalidate=86400`. Move country/currency detection to the edge (`CloudFront-Viewer-Country` header) or client side, so public HTML does not `Set-Cookie`. Keep `no-store` only on cart/checkout/account/API | TTFB < 200 ms on a CloudFront hit (`curl -w %{time_starttransfer}` twice); Lighthouse `bf-cache` passes on content pages |
| T-05 | **P0** | Test content safeguards | 28 Oct test article + test product went live; now 404/301 (fixed). The redirect `/shop/produt-1` → `/engagement-rings` exists | Keep both gone. Add a publish guard: items with "test" in title/slug, or flagged draft, are excluded from sitemap, listings, search, related items and `llms.txt`. Remove the `/shop/produt-1` 301 (let it 404/410) | Sitemap and `/llms.txt` contain no `test`/`produt` URLs |
| T-06 | **P1** | Sitemap host + GSC | GSC's only submitted sitemap is `https://www.houseofdiams.com/sitemap.xml` (247 URLs) | (Owner, in GSC) submit `https://houseofdiams.com/sitemap.xml`; remove the `www` one after T-01 is live. Developer: add `<lastmod>` (real content-modified dates) to every sitemap URL | GSC Sitemaps shows the apex sitemap "Success" |
| T-07 | **P1** | Footer Pinterest link → redirect | Ahrefs "Page has links to redirect" on **268 indexable + 340 non-indexable pages**: the only redirected link is `https://pin.it/3G2ogNJNq` (308) | Replace with `https://in.pinterest.com/HouseofDiams_/`. Add the missing **Facebook** icon/link (Part B URL). Replace the Instagram URL (`…?igsh=…&utm_source=qr`) with the clean `https://www.instagram.com/houseofdiams_/` | Ahrefs "Page has links to redirect" = 0 |
| T-08 | **P1** | Absolute `www` internal link | Hero slide CTA "SHOP ENGAGEMENT RINGS" links to `https://www.houseofdiams.com/engagement-rings`; "DISCOVER NOW" uses an absolute apex URL | All internal links relative (`/engagement-rings`). Grep the codebase and CMS content for `www.houseofdiams.com` and `https://houseofdiams.com/` in hrefs | `curl -s https://houseofdiams.com/ | grep -c 'href="https://www.houseofdiams'` = 0 |
| T-09 | **P1** | Nav/footer links to empty `noindex` pages | 13 links sitewide go to empty, `noindex,follow` listings: `/wedding-bands/for-him` + `/classic` `/diamonds` `/designer`; `/wedding-bands/for-her/nature` `/solid` `/cigar-band` `/pavee`; `/fine-jewellery/necklaces/initials` `/tennis-necklace`; `/fine-jewellery/rings/eternity-rings`; footer "Explore Collection" → `/collection` (0 pieces) | Hide a menu/footer item automatically when its category has 0 published products; show it again when it has stock. Keep the pages themselves `noindex,follow` + out of the sitemap while empty (as now) | No rendered nav/footer link points to a page with 0 products |
| T-10 | **P1** | Pagination | `?page=N` pages are indexable and self-canonical (correct). Ahrefs flags 22 "Indexable page not in sitemap" (all `?page=N` + `/promo-codes-and-offers`) and 23 "only one incoming internal link". `/engagement-rings/by-design?page=2/3` is self-canonical while `/engagement-rings/by-design` canonicalises to `/engagement-rings` | Keep `?page=N` self-canonical + indexable (Google's recommendation). Give paginated pages unique titles: `Engagement Rings – Page 2 | House of Diams`. Make `/engagement-rings/by-design?page=N` canonical to `/engagement-rings?page=N` (consistent with its page 1). Link page numbers 1…N (not only "next") | Paginated titles unique; by-design page 2+ canonical consistent |
| T-11 | **P1** | `/promo-codes-and-offers` | Indexable, not in sitemap, only content is "View gift: Princess Halo Stud Earrings" (thin) | If an offer is live, give the page real offer terms; otherwise `noindex` it and remove the link. (Also see Q-05 "September sale") | Page is either complete + in sitemap, or noindex + unlinked |
| T-12 | **P2** | Media host root | GSC "Blocked due to access forbidden (403)": `https://media.houseofdiams.com/` (S3 root) | Return 404 at the bucket root and add `X-Robots-Tag: noindex` on the media/content hosts for non-image responses | Root returns 404 |
| T-13 | **P2** | IndexNow | Ahrefs notice "Changed pages not submitted to IndexNow" (266) | Optional: implement IndexNow ping (Bing/Yandex) on publish/update. Not used by Google | — |
| T-14 | **P2** | Search results page | `/search?q=ring` → 404; pressing **Enter** in the search box does nothing | Add `/search?q=` results page (`noindex,follow`, excluded from sitemap); Enter submits to it | Enter in search opens results |

### C3. On-page SEO and content

| ID | Pri | Item | Current | Fix | Done when |
|---|---|---|---|---|---|
| O-01 | **P0** | PDP claims (all 182 product pages) | "Enjoy complimentary returns on items returned within **30 days**" (182 PDPs), "**craftsmanship warranty**" (180 PDPs), "complimentary **UPS** Overnight shipping", "In-stock pieces usually ship within 2-3 business days" | Returns: "Returns accepted within 15 days of delivery for unworn pieces; return shipping and duties are paid by the customer." Remove "craftsmanship warranty" (may say "Free lifetime warranty"). Shipping: "Free, insured overnight shipping to every country." Remove "UPS" and "2–3 business days" until HOD confirms | Sitewide text search finds 0 × "30 days", 0 × "craftsmanship warranty" |
| O-02 | **P0** | "Apply September sale" promo | On all 182 PDPs, cart and checkout: "Apply September sale · Princess Halo Stud Earrings · On orders $1,000+ · FREE" | Remove, or rename to the current live offer with real terms (HOD to confirm the offer still runs) | No "September" text on site |
| O-03 | **P0** | Delivery-time conflict | Cart summary shows "**Approximately 3 to 4 weeks**" for an in-stock bracelet, while `/shipping` says "same-day overnight dispatch" | Show the bespoke 3–4 weeks estimate only for made-to-order items; for ready-to-ship items show the shipping promise from Part B. **Needs HOD:** which products are ready-to-ship vs made-to-order | In-stock item in cart shows the overnight-shipping line |
| O-04 | **P0** | `/bespoke` claims | "Fully insured worldwide delivery — complimentary to **40+ countries**" (contradicts "every country"); "Full IGI / GIA certification included" | "Fully insured delivery, free to every country." The IGI/GIA line is OK (confirmed) | No "40+" on site |
| O-05 | **P1** | `/about` unconfirmed claims | "Established networks in 20+ countries"; "Conflict Free", "Ethically"; founder line "Akshar korat co founder" (lower case) | Remove "20+ countries" and the ethics/conflict-free badges until HOD supplies proof; fix to "Akshar Korat, Co-founder" and the same format for Krish Babariya | — |
| O-06 | **P1** | Typos and labels | Top bar "**FINE JWELERY AVAILABLE**"; nav "**T- BAR**"; menu mixes "Toi-et moi" (necklaces) and "Toi-moi Rings"; footer "Surat, Gujarat **india**"; cart "1 **items**", "Shape: **round**"; about image `alt="Fine Jewellery"`; 29 pages still show the word "Jewellery" (mostly old blog titles and the mega-menu image alt) | "Fine jewelry available" (or remove the bar); "T-Bar"; one consistent label "Toi et Moi"; "Surat, Gujarat, India"; pluralise ("1 item"); capitalise option values ("Round"); alt "Fine jewelry". Keep URL slugs | Sitewide search finds 0 × "Jwelery/Jewelery", 0 × "T- BAR" |
| O-07 | **P1** | The top-bar "FREE WORLDWIDE SHIPPING" link | Links to `/fine-jewellery/earrings/stud-earrings` (unrelated) | Link to `/shipping` or make it plain text | — |
| O-08 | **P1** | Homepage H1 changes with the slider | Static HTML H1 = "THE BEGINNING OF FOREVER" (approved), but the rendered H1 after the carousel moves = "Where Diamonds Find Their Voice" (each slide renders its own `<h1>`) | One fixed `<h1>` for the page ("The Beginning of Forever" per spec); other slide headings `<h2>`/`<p>` | One `<h1>` in the DOM at all times |
| O-09 | **P1** | Title lengths | Ahrefs "Title too long" on 23 indexable pages (my crawl: 67 PDP + 16 blog titles > 60 chars incl. " \| House of Diams") | PDPs: use the `07-PDP-ON-PAGE-SEO.md` formula: `{Product name} \| House of Diams`, product name ≤ 45 chars; drop "Lab-Grown Diamond" from names where it pushes over 60 (keep it in H1/description). Blogs: shorten the 10 non-refresh posts; the refresh posts (4Cs, shapes, ring size, 14K vs 18K, how-to-choose, certification) wait for GSC — leave them | Ahrefs "Title too long" ≤ refresh-post count |
| O-10 | **P1** | Short / placeholder metas | Ahrefs "Meta description too short" on 43 indexable pages. Placeholder-style metas: `/shop/round-radiant-drops` "Earrings · 10K White Gold - House of Diams", `/shop/round-hoop-drops`, `/shop/round-solitaire-studs`; boilerplate `/wedding-bands/for-her` "Browse For Her in Wedding Bands.", `/fine-jewellery/bracelet/bangles` "Browse Bangles in Fine Jewelry."; `/privacy-policy`, `/terms` one-liners | Write 120–155-char metas for every indexable page: PDP pattern "{Product}: {key specs — shape, total carat, setting} in 10K or 14K gold. Free insured shipping to every country from House of Diams." Category metas from `On-page SEO/01` | Ahrefs "Meta description too short" = 0 on indexable pages |
| O-11 | **P1** | Duplicates | Duplicate H1 "Round Baguette Three-Stone Ring" (2 PDPs); duplicate meta "A three-stone engagement ring featuring a round center diamo…" (2 PDPs) | Make both product names/metas unique (add the distinguishing spec) | No duplicate titles/H1s/metas |
| O-12 | **P1** | Open Graph incomplete | `og:image` and `twitter:image` missing on 11 pages: `/t-bar` and 10 blog posts (christmas, wife, girlfriend, anniversary-by-year, 10-year anniversary, what-finger, push-present, necklace-layering, how-to-wear, custom-engagement-ring) | Default `og:image` = the article hero/featured image (fallback: brand image 1200×630) | Ahrefs "Open Graph tags incomplete" = 0 |
| O-13 | **P1** | Orphan products | 6 PDPs in the sitemap have **no internal links**: `elaris-emerald-twist-diamond-ring`, `east-west-oval-diamond-bezel-pendant`, `aurevane-sunburst-round-diamond-halo-stud-earrings`, `virelle-round-twist-diamond-ring`, `seraphina-oval-diamond-pendant-with-accent-bail`, `amora-heart-cut-solitaire-pendant-necklace` | Assign each to its category so it appears in a listing (and in related items) | Each has ≥ 2 internal inlinks |
| O-14 | **P1** | Bangles taxonomy (F-E7) | `/fine-jewellery/bracelet/bangles` holds link bracelets; title "Bangles \| Fine Jewelry" vs spec "Diamond Link Bracelets" | Apply spec title/H1/meta from `On-page SEO/01` ("Diamond Link Bracelets") until HOD adds real bangles | — |
| O-15 | **P2** | Mobile menu missing key pages | Mobile menu: Home, Fine Jewelry, Engagement Rings, Wedding Bands, T-Bar, Wishlist, About, Contact, Cart, Profile — **no Bespoke, Blog/Education** | Add "Bespoke", "Education" and "Blog" to the mobile and desktop nav | — |

**Already correct (do not redo):** the 10 blog packages; titles/metas/H1s on 44 of 49 ready pages (the other 5 are refresh posts waiting for GSC); `/contact`, `/bespoke`, `/shipping`, `/returns`, `/about` titles + H1s; FAQPage only on `/faq`; Organization author on all 21 articles; BreadcrumbList on 245/246 pages; `by-desgin` URLs now 301 to `by-design`; all 52 previously missing internal links present; nav label typos "Solitare/Anniversay" fixed.

### C4. Structured data

| ID | Pri | Item | Current | Fix | Done when |
|---|---|---|---|---|---|
| S-01 | **P0** | Merchant listing warnings (GSC) | GSC Merchant listings: 35 valid items, each with **Missing `hasMerchantReturnPolicy`**, **Missing `shippingDetails`**, **Duplicate field `material`**. All 182 Product blocks lack both fields | In every `Offer`: `shippingDetails` (`OfferShippingDetails`: `shippingRate` value 0 USD, `shippingDestination` = all countries you ship to (list ISO codes, or US first), `deliveryTime` handling 0–1 day + transit 1–2 days **only if HOD confirms transit time — otherwise omit deliveryTime**) and `hasMerchantReturnPolicy` (`MerchantReturnPolicy`: `returnPolicyCategory` FiniteReturnWindow, `merchantReturnDays` 15, `returnMethod` ReturnByMail, `returnFees` ReturnShippingFees, `applicableCountry`). Emit `material` once (array if several). Better still, add the return policy once at Organization level (`hasMerchantReturnPolicy`) and reference it | Rich Results Test on 3 PDPs: no warnings; GSC Merchant listings warnings start validating |
| S-02 | **P0** | Unconfirmed New York address in schema | Organization `address` has a second `PostalAddress` New York, NY, US on all 246 pages; the contact modal shows "36 W 44th Street, Suite 1000B, New York, 10036, USA" | Remove both until HOD confirms it is a real, staffed location (see L-01) | No "New York" in the HTML |
| S-03 | **P1** | Organization completeness | Surat address in schema has no street or postal code, though the footer shows "PRAGATI IT WORLD, 831, Yogi Chowk, Surat, Gujarat 395010" | Use the same full NAP in schema and footer: `streetAddress` "831, Pragati IT World, Yogi Chowk", `addressLocality` Surat, `addressRegion` Gujarat, `postalCode` 395010, `addressCountry` IN; `telephone` "+91 93285 36178". Keep `founder`, `sameAs` (Part B URLs), `logo` ≥ 112×112 | — |
| S-04 | **P1** | Category ItemList | Ahrefs "Category page missing ItemList schema" on `/`, `/shop`, `/engagement-rings`, `/fine-jewellery` (other categories have it) | Add `ItemList` of the products shown (url + position) on those 4 | Ahrefs issue = 0 |
| S-05 | **P1** | Homepage BreadcrumbList | Missing only on `/` | Optional — a homepage breadcrumb is not required; leave as is or add a single-item list | — |
| S-06 | **P2** | WebSite schema | Not present | Add `WebSite` (`name`, `url`) on the homepage (no SearchAction needed) | — |

### C5. Performance (Lighthouse / PageSpeed)

**Measured 29 Oct (Lighthouse 13.6, local run, simulated mobile throttling):**

| Template | Mobile Perf | Mobile LCP | Desktop Perf | A11y | Best Pr. | SEO | Agentic |
|---|---|---|---|---|---|---|---|
| Home | 65 | 7.0 s | 76 | 92 | 100 | 100 | 2/3 |
| /shop | 70 | 6.2 s | 77 | 92 | 100 | 100 | 2/3 |
| /engagement-rings | 54 | 6.5 s (TBT 540 ms) | 77 | 92 | 100 | 100 | 2/3 |
| Category (tennis bracelet) | 72 | 6.2 s | 74 | 92 | 100 | 100 | 2/3 |
| PDP (bracelet) | 63 | 7.4 s (8.2 MB page) | 73 | 92 | 100 | 100 | 2/3 |
| /blog · article | 85 · 91 | 3.4 · 2.4 s | 79 · 86 | 96 | 100 | 100 | 2/3 |
| /bespoke · /about · /contact · /faq | 76 · 83 · 90 · 92 | 5.1 · 3.6 · 2.4 · 2.4 s | 81 · 76 · 83 · 85 | 91–96 | 100 | 100 | 2/3 |

No Core Web Vitals field data exists yet in GSC ("No data"), so Google currently has no CWV signal for the site.

| ID | Pri | Item | Evidence | Fix |
|---|---|---|---|---|
| P-01 | **P0** | LCP image is lazy-loaded | LCP element on home = slider image `alt="SHOP ENGAGEMENT RINGS"` with `loading="lazy"`; on /shop, /engagement-rings and categories = first product card image with `loading="lazy"` (resource load delay 1.0–1.3 s) | First hero slide and the first 2 (mobile) / 4 (desktop) product-card images: `priority` (`fetchpriority="high"`, no lazy). Slider must not auto-advance before first paint; only slide 1 is preloaded |
| P-02 | **P0** | PDP autoplay video (BUG-008) | 6.7 MB MP4 autoplays on the bracelet PDP; total page 8.2 MB; LCP 7.4 s; LCP element is an `aria-hidden` poster image | Poster image first (priority); load video only after user interaction or when idle + in viewport; serve a ≤ 1.5 MB 720p H.264/WebM; `preload="none"`, no autoplay on mobile/save-data |
| P-03 | **P1** | Oversized images | "Improve image delivery" 477 KiB on PDP: the gift thumbnail (Princess Halo Stud) is a **250 KB** image shown at 46×46 px; gallery thumbs 68 KB each | Route every image through `next/image` with correct `sizes`; thumbnails ≤ 15 KB; AVIF/WebP; quality 70–75 |
| P-04 | **P1** | Element render delay 1.0–2.0 s | H1/text LCP on article, FAQ, contact waits for client JS (fade-in animation / hydration) | Render text LCP elements server-side without opacity animation; remove entry animations above the fold |
| P-05 | **P1** | Render-blocking CSS / legacy JS / unused JS | 3 CSS files (33 KB main) block render; 14 KB legacy polyfills; ~21 KB unused JS; TBT 540 ms on /engagement-rings | Inline critical CSS (Next `experimental.optimizeCss` or critters); modern `browserslist` (no ES5 polyfills); code-split filters/quiz/reels/cookie modal with `dynamic(() => …, { ssr:false })`; defer GTM until after load (`afterInteractive`/`lazyOnload`) |
| P-06 | **P1** | Third-party preload of flag icon | Every page preloads `cdn.jsdelivr.net/gh/lipis/flag-icons/.../us.svg` (extra origin) | Self-host the one flag SVG inline; drop the jsdelivr preload |
| P-07 | **P1** | Fonts | Inter variable font 109 KB | Subset to Latin, `font-display: swap`, preload only the weight used above the fold |
| P-08 | **P1** | Caching | `cache-insight` fails on all pages (product images from `/products/draft/…` served with 0 cache to the browser in the Lighthouse run) | Covered by T-02; also move published images out of the `draft/` path |

**Realistic targets (be honest with the owner):** Accessibility 100, Best Practices 100, SEO 100 and Agentic Browsing 3/3 are fully achievable on every template. Performance **≥ 95 desktop and ≥ 90 mobile** on the key templates (home, category, PDP, blog) is achievable with T-02, T-04 and P-01…P-07. A guaranteed 100 mobile Performance on an image- and video-led jewelry store is not realistic, and it is not needed: the ranking signal is the field Core Web Vitals (LCP < 2.5 s, INP < 200 ms, CLS < 0.1), not the lab score.

### C6. Accessibility + Agentic Browsing (Lighthouse "Agentic Browsing" 3/3)

The Agentic Browsing category (Lighthouse 13.6) scores the applicable checks: **agent accessibility tree** (fails), **CLS** (passes), **llms.txt** (passes). WebMCP and ARD checks are not applicable (no WebMCP, no `/.well-known/ard.json`), which is fine. One element fails the tree check on every page:

| ID | Pri | Item | Evidence | Fix |
|---|---|---|---|---|
| A-01 | **P0** | `presentation-role-conflict` (fails Agentic + A11y on all 22 runs) | Currency selector flag: `<img aria-label="United States" alt="" src=".../flags/4x3/us.svg">` | Use `alt="United States"` and remove `aria-label` (or keep `alt=""` + `aria-hidden="true"` with the visible "United States (USD)" text as the button name). **This alone makes Agentic Browsing 3/3** |
| A-02 | **P1** | `color-contrast` | "USD ONLY" (`text-white/45`, 4.42:1), cookie banner eyebrow "COOKIES" (#91969e on white, 2.97:1), PDP "On orders $1,000+" | Raise to ≥ 4.5:1 (e.g. `text-white/70`, `#6b7078`) |
| A-03 | **P1** | `button-name` on `/bespoke` form | Radix Select triggers "Piece Type *", "Preferred Stone", "Approx. Carat", "Preferred Metal" have no accessible name | `aria-labelledby` pointing to each field label |
| A-04 | **P1** | `aria-allowed-attr` on `/faq` | `<input type="search" aria-expanded …>` | Add `role="combobox"` (or drop `aria-expanded`) |
| A-05 | **P1** | `aria-prohibited-attr` on home | `<div aria-label="Instagram reel navigation">` | Add `role="group"` |
| A-06 | **P1** | `target-size` | Product-card image dots 5×5 / 10×5 px on /shop, categories; PDP "Apply September sale" | ≥ 24×24 px hit area (padding), or hide dots on mobile |
| A-07 | **P2** | Image-only links | Mega-menu image tiles are links whose only content is an image; check each `<img>` has a meaningful `alt` (category name) so the link has a name | — |
| A-08 | **P2** | Agentic extras (optional) | — | Keep `/llms.txt` current (it passes). Optionally publish `/.well-known/ard.json` later; not required for 3/3 |

### C7. Frontend QA (tested 29 Oct; payment/checkout not tested)

**Works:** home and all nav links resolve (200); mobile menu opens with submenus and no horizontal scroll at 375 px; search suggestions show correct products with images; add to bag from a bracelet PDP and a ring PDP; love-letter dialog; cart drawer; cart page quantity +/−, totals update, Remove, Clear bag; WhatsApp link (`wa.me/919328536178`); `mailto:admin@`; `/contact` form renders with labelled required fields; cookie Reject stores `hod_consent` with analytics/marketing false.

| ID | Pri | Bug | Steps / evidence | Fix |
|---|---|---|---|---|
| Q-01 | **P0** | Ring size silently pre-selected | Ring PDP (e.g. `/shop/elowen-round-halo-engagement-ring`) → Add To Bag without choosing a size → bag gets **US 4** (`aria-pressed=true` by default) | No default size; Add To Bag disabled (or inline error "Select your ring size") until a size is chosen. Same for bracelet length (defaults to 6 Inch) |
| Q-02 | **P1** | Search Enter does nothing | Type "tennis" → Enter → nothing happens | See T-14 |
| Q-03 | **P1** | Cookie banner overlaps dialogs | On first visit the cookie banner sits on top of the "Add a private love letter" dialog | Give dialogs a higher z-index than the banner, or show the banner first and block other modals until it is answered |
| Q-04 | **P1** | Cart flashes "(0 items)" | `/cart` server-renders "MY BAG (0 items)" before the client loads `hod_cart` | Render a skeleton until the cart state is hydrated |
| Q-05 | **P0** | Promo / placeholder text | "Apply September sale" (see O-02). "tesxt 1" no longer found (fixed) | — |
| Q-06 | **P1** | Tax line for non-US visitors | From India (`detected_country=IN`) the cart adds 12 % tax ($40.20 on $335) while prices are USD-only | Developer to confirm tax rules per destination; the owner checks this at checkout |
| Q-07 | **P1** | Login host | Login sends customers to `auth-uat.houseofdiams.com` (UAT-named host on production) | Use a production auth host (e.g. `auth.houseofdiams.com`); `noindex` it |
| Q-08 | **P2** | Clear bag has no confirmation | One click empties the bag | Optional confirm or "Undo" toast |
| Q-09 | **P2** | Contact page | No visible email/phone/hours on `/contact` itself (only in the footer and the modal) | Show the approved NAP block + reply time on the page (see L-02) |

**Regression checks the developer must run before delivery (desktop + 375 px mobile):** every header/mega-menu/footer link returns 200 and lands on a page with products; search suggestions + Enter; PDP option selection (metal, size/length, engraving) → Add To Bag → drawer → View Cart → quantity/remove/clear → Checkout button opens checkout (stop there); wishlist add/remove when logged out (should prompt login) and logged in; contact and bespoke forms show validation on empty submit; WhatsApp/mailto/tel links; cookie Reject/Accept/Customize persist across pages; 404 page for an unknown URL returns HTTP 404 with `noindex`.

### C8. Local SEO (site side only)

| ID | Pri | Item | Fix |
|---|---|---|---|
| L-01 | **P0** | New York address | It is not a confirmed HOD fact. If it is a virtual office or mail-forwarding address, do not publish it (it can't be used for a Google Business Profile and creates inconsistent NAP). Remove it from the contact modal and schema until HOD confirms it is a real, staffed location |
| L-02 | **P1** | One consistent NAP everywhere | Footer, `/contact`, `/about` and schema must show the same block: **House of Diams, 831, Pragati IT World, Yogi Chowk, Surat, Gujarat 395010, India · +91 93285 36178 · admin@houseofdiams.com · Headquarters & workshop, by appointment only**. Fix the lowercase "india" |
| L-03 | **P1** | Contact page | Add the NAP block, "Replies within 24 hours", an embedded map of the Surat workshop (lazy-loaded, click-to-load iframe so it doesn't hurt LCP) and opening/appointment hours once HOD supplies them |
| L-04 | **P2** | LocalBusiness schema | Only after HOD confirms visiting hours: add `JewelryStore` on `/contact` with the Part B/L-02 NAP, `openingHoursSpecification`, `geo`, `hasMap`. Not before (no invented hours) |
| L-05 | owner | Google Business Profile | Off-site (owner task): create/verify a GBP for the Surat workshop with the identical NAP and link it to `https://houseofdiams.com/contact` |

### C9. GA4 / GTM / consent (site-side errors)

Observed in GA4 (property "House of Diams", stream `G-0LVQJ1YDJ0`) and on the site:
* Stream URL is still `https://www.houseofdiams.com/` (owner updates to `https://houseofdiams.com` in GA4 Admin → Data streams).
* Events received in the last 28 days: `page_view, session_start, first_visit, user_engagement, scroll, click, file_download, form_start, add_to_cart`. **Missing:** `view_item_list`, `select_item`, `view_item`, `add_to_wishlist`, `remove_from_cart`, `view_cart`, `begin_checkout`, `add_shipping_info`, `add_payment_info`, `purchase` (key event with **no data**), `generate_lead`, `view_search_results`/`search`. `close_convert_lead` and `qualify_lead` are unused key events.
* No tags load until the visitor accepts. After Accept, the dataLayer gets `gtag('consent','default',{…granted})` **twice**, then GA4 is configured **twice** (`config` with `send_page_view:false`, then `config` with `page_path`), **and** GTM (`GTM-TJ5HTTSD`) loads Clarity and the Pinterest tag. Enhanced Measurement page views are also on, so there is a real risk of double `page_view`s on route changes.

| ID | Pri | Fix |
|---|---|---|
| G-01 | **P0** | **Consent Mode v2 (advanced):** load GTM on every page; before it, push `gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',wait_for_update:500})`; on the visitor's choice push `gtag('consent','update',{…})` — never a second `default`. Persist and re-apply the stored choice on each page load |
| G-02 | **P0** | **One GA4 path only:** remove the hard-coded `gtag('config','G-0LVQJ1YDJ0')` calls and fire GA4 only from GTM (Google tag + event tags), **or** remove GA4 from GTM — not both. Send exactly one `page_view` per App Router navigation (either Enhanced Measurement "page changes based on browser history events" **or** a manual event, not both). Verify in GTM Preview + GA4 DebugView |
| G-03 | **P0** | **GA4 ecommerce dataLayer** (standard schema with `items[]`: `item_id` = SKU, `item_name`, `item_category`, `item_variant` = metal, `price`, `quantity`, `currency:'USD'`): `view_item_list` (category/shop/search), `select_item`, `view_item` (PDP), `add_to_cart`, `remove_from_cart`, `view_cart`, `add_to_wishlist`, `begin_checkout`, `add_shipping_info`, `add_payment_info`, `purchase` (on the order-confirmation page **once per transaction_id**, with `value`, `tax`, `shipping`, `coupon`) |
| G-04 | **P1** | Lead events: `generate_lead` on successful contact/bespoke submit (with `form_name`), `sign_up`/`login`, `view_search_results` with `search_term`. Mark `purchase` and `generate_lead` as key events; delete the unused `close_convert_lead`/`qualify_lead` (owner, in GA4) |
| G-05 | **P1** | Owner settings in GA4: data retention 14 months; Google Signals per privacy policy; internal-traffic filter; unwanted referrals (payment gateway domain `razorpay.com`) so purchases are not attributed to the gateway; link GA4 ↔ Search Console (domain property) |
| G-06 | **P1** | CSP is `report-only` and already allows GTM/GA/Clarity/Pinterest — keep it in sync with any new tag before enforcing |

### C10. Google Search Console (owner actions + what the fixes above solve)

Current: **148 indexed / 453 not indexed** — page with redirect 101, crawled-currently-not-indexed 190 (includes `/engagement-rings/by-design/pave`, `/halo-ring`, `/nature-inspired-rings`, `/fine-jewellery/bracelet`, `/fine-jewellery/necklaces/solitare` and several blog posts), discovered-not-indexed 113, noindex 18, 404 14, alternate-canonical 8, 5xx 5 (`www` blog posts on 23–24 Oct), 403 1 (media root), redirect error 1 (`http://houseofdiams.com/fine-jewellery`, now redirects correctly), robots 2. Clicks ~205 in 3 months; homepage CTR 9.9 % on `www`.

| ID | Who | Action |
|---|---|---|
| GSC-01 | owner | After T-01: submit `https://houseofdiams.com/sitemap.xml`, remove the `www` sitemap; URL-inspect + "Request indexing" for the homepage, `/engagement-rings`, `/fine-jewellery`, `/wedding-bands`, `/bespoke` and the top 5 blog posts |
| GSC-02 | owner | Start "Validate fix" on: Server error (5xx), Redirect error, Not found (404), Merchant listings warnings (after S-01) |
| GSC-03 | dev | The "Crawled – currently not indexed" category pages need unique, useful content: a 60–120-word intro above the grid and a short buying guide/FAQ block below it (text from `On-page SEO/04`, facts from Part B only), unique title/meta, and links from the relevant blog/education posts. Thin grids that only repeat product cards are why Google skips them |
| GSC-04 | owner | Settings → check "Search generative AI" is not set to exclude; check Crawl stats for 5xx after T-02/T-03 |

---

## PART D — Items that need HOD (do not implement until answered)

1. Is "36 W 44th Street, Suite 1000B, New York" a real, staffed HOD location? (L-01, S-02)
2. Which products are ready-to-ship (overnight) vs made-to-order (3–4 weeks)? (O-03)
3. Is the carrier UPS? Real transit time for `deliveryTime` in schema? (O-01, S-01)
4. Is any promo running now (replaces "September sale")? (O-02, T-11)
5. Proof for "20+ countries", "Conflict Free", "Ethically"? (O-05)
6. Visiting / appointment hours for the Surat workshop? (L-03, L-04)
7. BC-001 "insured shipping" — now a confirmed fact, so the live post is consistent; no change needed.

## PART E — Acceptance checks (run all; paste the output into the delivery report)

```bash
# 1. Host + redirects (expect one 301 each, straight to https://houseofdiams.com/...)
for u in http://www.houseofdiams.com/ https://www.houseofdiams.com/shop?page=2 http://houseofdiams.com/fine-jewellery; do curl -sI "$u" | grep -iE '^HTTP|^location'; done
# 2. Static assets cached (second call must say Hit)
u=https://houseofdiams.com$(curl -s https://houseofdiams.com/ | grep -oE '/_next/static/chunks/[^"]+\.js' | head -1); curl -sI $u >/dev/null; curl -sI $u | grep -i x-cache
# 3. Burst test: 0 non-200
curl -s https://houseofdiams.com/ | grep -oE '/_next/static/[^"]+\.(js|css)' | sort -u | sed 's#^#https://houseofdiams.com#' | xargs -P 50 -n 1 curl -s -o /dev/null -w '%{http_code}\n' | sort | uniq -c
# 4. Forbidden text sitewide (expect no output)
curl -s https://houseofdiams.com/sitemap.xml | grep -oE 'https://[^<]+' | xargs -P 6 -n 1 curl -s | grep -oiE '30 days|craftsmanship warranty|september sale|jwelery|jewelery|tesxt|40\+ countries|New York|pin\.it|www\.houseofdiams' | sort | uniq -c
# 5. Lighthouse (mobile + desktop) on: / /shop /engagement-rings /fine-jewellery/bracelet/tennis-bracelet /shop/rosette-five-flower-bracelet /blog /bespoke
npx lighthouse@13.6.0 https://houseofdiams.com/ --only-categories=performance,accessibility,best-practices,seo,agentic-browsing --output=json --output-path=./lh-home-mobile.json
```

Plus: Google Rich Results Test on 3 PDPs (0 warnings); GTM Preview + GA4 DebugView walk-through (list → item → add_to_cart → view_cart → begin_checkout, one `page_view` per navigation, consent default denied before choice); new Ahrefs crawl of the apex project (0 errors, and warnings limited to the GSC-gated refresh posts); PageSpeed Insights mobile + desktop on the same 7 URLs.

**Targets at delivery:** Ahrefs apex project health 100 % with no "links to redirect", "OG incomplete", "ItemList missing" or "meta too short" warnings · Lighthouse Accessibility / Best Practices / SEO = 100 and Agentic Browsing 3/3 on every template · Performance ≥ 90 mobile / ≥ 95 desktop on key templates · GSC: apex sitemap "Success", 5xx/redirect-error validation passed, Merchant listings without warnings · GA4: full ecommerce funnel + leads, one page_view per navigation, Consent Mode v2 active.
