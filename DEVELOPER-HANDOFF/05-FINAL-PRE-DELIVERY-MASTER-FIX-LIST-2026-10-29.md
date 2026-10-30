# 05 — Final Pre-Delivery Master Fix List (only open items — re-verified 2026-10-30)

**First audit:** 2026-10-29 · **Re-verified:** 2026-10-30 (fresh crawl of all 246 sitemap URLs, deep text/schema scan, Lighthouse 13.6 on 11 templates × mobile/desktop, browser QA). Evidence: `Technical/2026-10-30-live-validation/` (and `2026-10-29-live-validation/` for the first audit).
**Site:** https://houseofdiams.com (canonical host = apex) · **Prepared for:** the developer, to hand directly to Claude Code.

> **Important — nothing new is live yet.** On 2026-10-30 the live site serves exactly the same JavaScript build as on 29 Oct (all 24 `/_next/static` file names and hashes are identical), and the titles, metas, H1s, canonicals, robots tags, schema types and the sitewide text scan are unchanged on all 246 pages. If fixes were made, they are not deployed. **Deploy them, then ask for a re-check.** This file lists only what is still open on the live site; items verified as fixed were removed.

**Not tested on purpose:** the payment step and order placement (the owner tests these). No form was submitted and no message was sent. Cookies were not accepted, and test bags were emptied afterwards.

---

## PART A — PROMPT FOR CLAUDE CODE (copy everything from here to the end of the file)

You are working in the House of Diams website codebase. It is a Next.js App Router site behind nginx + CloudFront on AWS. Media is served from `media.houseofdiams.com` / `content.houseofdiams.com`. Tags: GTM `GTM-TJ5HTTSD`, GA4 `G-0LVQJ1YDJ0`. Implement every item in Part C in the priority order given, **deploy to production**, then run the acceptance checks in Part E.

**Rules — follow exactly:**
1. **Do not invent business facts.** Customer-facing copy may only state the facts in Part B. If a fix needs a fact that is not in Part B, leave the text out and list it in your final report under "Needs HOD".
2. **Do not touch payment/checkout logic** (Razorpay, order creation, pricing, tax calculation). Text and labels on the cart page are in scope; payment code is not.
3. **Do not change any URL slug** unless an item says so. Every URL that stops returning 200 must get a 1:1 301 to its replacement. Never use 302/307 for permanent moves.
4. **No test content on production.** Test products, articles and categories must stay unpublished, excluded from the sitemap, `noindex`, and out of listings, search and related items. Do QA on a staging host that sends `X-Robots-Tag: noindex` and is not linked from production.
5. **American English** in all customer-facing copy, nav labels, alt text and anchors: "jewelry", "color", "center", never "jewellery/jewelery/jwelery". Do **not** rename the `/fine-jewellery/` URLs.
6. **Do not add FAQPage schema** anywhere except `/faq`, where it is already correct. Do not fabricate reviews/ratings, GTINs, awards or certifications in schema.
7. Keep changes small and reviewable: one commit per item ID (e.g. `fix(T-01): www→apex 301`). Do not refactor unrelated code.
8. After each P0/P1 item, run the item's **Done when** check **against the live production site** and paste the result into your report.

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
| Company | Founders **Krish Babariya** and **Akshar Korat**; in the trade since 2014 ("a decade in the trade" OK); public email **admin@houseofdiams.com** only |
| Social | Instagram `https://www.instagram.com/houseofdiams_/`, Facebook `https://www.facebook.com/profile.php?id=61593287138869`, Pinterest `https://in.pinterest.com/HouseofDiams_/` |

**NOT confirmed — remove or hide until HOD confirms:**
- The New York address "36 W 44th Street, Suite 1000B, New York 10036", and the "2018 New York office opens" milestone on `/about`.
- "UPS" as the carrier.
- "40+ countries" and "Established networks in 20+ countries".
- "Conflict Free" and "Ethically" claims.
- "In-stock pieces usually ship within 2–3 business days".
- Any promo or sale that isn't currently running.

---

## PART C — FIX LIST (all items below were still open on 2026-10-30)

Priority: **P0** = must fix before delivery (blocks indexing, tracking or trust) · **P1** = needed for the 100/100 targets · **P2** = polish.

### C1. Why Ahrefs shows two different scores (answer + fix)

| Project | Score | Why |
|---|---|---|
| `www.houseofdiams.com` | **69 %**, 312 URLs with errors | `www` is still a full copy of the site (HTTP 200, no redirect; still true on 30 Oct). During its 28 Oct crawl, 8 core JavaScript chunks returned 500/502 from the origin, so Ahrefs flagged "Page has broken JavaScript" on 304 pages. The other errors come from the `www` pages canonicalizing to the apex |
| `houseofdiams.com` | **100 %**, 0 errors | The apex host. It still has 30 warnings/notices (C2–C4) |

**Root causes (both still present on 30 Oct):**
1. CloudFront does not cache `/_next/static/*`. Repeat requests to a JS chunk still say `x-cache: Miss from cloudfront`.
2. `www` is not redirected to the apex.

**After T-01 and T-02 are live (owner, in Ahrefs):** run a new crawl of the apex project, then delete or archive the `www` project.

### C2. Technical SEO

| ID | Pri | Item | Current (2026-10-30) | Fix | Done when |
|---|---|---|---|---|---|
| T-01 | **P0** | `www` → apex 301 | `https://www.houseofdiams.com/`, `/shop?page=2` and blog posts return **200**. `http://www…` → 301 → `https://www…` (200), a 2-hop chain to a duplicate | One rule at CloudFront (viewer-request Function) or nginx: any request with `Host: www.houseofdiams.com` (http or https) → **301** to `https://houseofdiams.com` + same path + same query. Single hop from every variant | `curl -sI https://www.houseofdiams.com/shop?page=2` → `301` `location: https://houseofdiams.com/shop?page=2`; `curl -sI http://www.houseofdiams.com/x` → one 301 straight to `https://houseofdiams.com/x` |
| T-02 | **P0** | Cache static JS/CSS at CloudFront | `/_next/static/chunks/*.js` sends `cache-control: public, max-age=31536000, immutable` but CloudFront still answers **Miss** on the 2nd and 3rd request. (`media.*` and `/_next/image` now return **Hit** on repeat, so they're fine) | Add a cache behavior for `/_next/static/*` with the managed **CachingOptimized** policy (no cookies, no query strings, no headers except Accept-Encoding). Enable Brotli/Gzip | Second request to any `/_next/static/chunks/*.js` returns `x-cache: Hit from cloudfront` |
| T-03 | **P0** | Keep old chunks available across deploys | Ahrefs/GSC saw 5xx on JS chunks and `www` blog pages during deploy windows (23–24 and 28 Oct) | Keep the previous build's `/_next/static` assets for ≥ 7 days after each deploy (don't delete on deploy). An unknown chunk returns **404**, never 500 | A chunk URL from the previous build still returns 200 after a new deploy |
| T-04 | **P1** | HTML caching / TTFB | Every HTML response is `private, no-cache, no-store` and sets `detected_country`/`detected_currency` cookies. TTFB ≈ 0.97 s. Lighthouse `bf-cache` fails on all 22 runs | Serve public pages (home, categories, PDPs, blog, education, policy pages) with ISR/`revalidate` + `Cache-Control: public, s-maxage=300, stale-while-revalidate=86400`. Move country/currency detection to the edge (`CloudFront-Viewer-Country`) or client side, so public HTML doesn't `Set-Cookie`. Keep `no-store` only on cart/checkout/account/API | TTFB < 200 ms on a CloudFront hit; Lighthouse `bf-cache` passes on content pages |
| T-05 | **P1** | Test-content leftovers | The test pages are gone, but `/shop/produt-1` still **301s to `/engagement-rings`** | Remove that 301 so it returns 404/410. Add a publish guard: items with "test" in the title/slug, or flagged draft, are excluded from the sitemap, listings, search, related items and `llms.txt` | `curl -sI https://houseofdiams.com/shop/produt-1` → 404 or 410 |
| T-06 | **P1** | Sitemap `<lastmod>` + GSC | Only **182 of 246** sitemap URLs have `<lastmod>` (the product pages). GSC still has only the `www` sitemap submitted | Developer: add a real content-modified `<lastmod>` to the remaining 64 URLs (categories, blog, education, policy pages). Owner: submit `https://houseofdiams.com/sitemap.xml` in GSC after T-01 | All 246 sitemap URLs have `<lastmod>`; GSC shows the apex sitemap "Success" |
| T-07 | **P1** | Footer social links | Pinterest still `https://pin.it/3G2ogNJNq` (a redirect, flagged on 600+ pages by Ahrefs). Instagram still has tracking parameters (`?igsh=…&utm_source=qr`). There's no Facebook link | Pinterest → `https://in.pinterest.com/HouseofDiams_/`. Instagram → `https://www.instagram.com/houseofdiams_/`. Add Facebook → `https://www.facebook.com/profile.php?id=61593287138869` | Ahrefs "Page has links to redirect" = 0 |
| T-08 | **P1** | Absolute `www` internal link | Homepage hero "SHOP ENGAGEMENT RINGS" still links to `https://www.houseofdiams.com/engagement-rings`; one absolute apex link `https://houseofdiams.com` | All internal links relative (`/engagement-rings`). Grep code and CMS content for `www.houseofdiams.com` and `https://houseofdiams.com/` in hrefs | `curl -s https://houseofdiams.com/ \| grep -c 'href="https://www.houseofdiams'` = 0 |
| T-09 | **P1** | Menu links to empty `noindex` pages | The mega-menu still links to **10** empty listings: `/wedding-bands/for-him/classic`, `/diamonds`, `/designer`; `/wedding-bands/for-her/nature`, `/solid`, `/cigar-band`, `/pavee`; `/fine-jewellery/necklaces/initials`, `/tennis-necklace`; `/fine-jewellery/rings/eternity-rings` | Hide a menu item automatically while its category has 0 published products; show it again when it has stock. Keep the pages themselves `noindex,follow` and out of the sitemap while empty (already correct) | No rendered menu/footer link points to a page with 0 products |
| T-10 | **P1** | Pagination (remaining part) | `/shop?page=2` and `/engagement-rings?page=2` titles already include "– Page 2" (OK). Still wrong: `/blog?page=2` canonicalizes to `/blog` and its title has no page number; `/engagement-rings/by-design?page=2` is self-canonical while its page 1 canonicalizes to `/engagement-rings` | `/blog?page=N`: self-canonical + title "Blog – Page N". `/engagement-rings/by-design?page=N`: canonical → `/engagement-rings?page=N`. Link page numbers 1…N, not only "next" | Each `?page=N` URL has a unique title and a consistent canonical |
| T-11 | **P1** | `/promo-codes-and-offers` | 200, indexable, not in the sitemap, thin (only "View gift: Princess Halo Stud Earrings") | If an offer is live, give the page real offer terms and add it to the sitemap; otherwise `noindex` it and remove the link | Page is either complete + in the sitemap, or noindex + unlinked |
| T-12 | **P2** | Media host root | `https://media.houseofdiams.com/` returns **403** (GSC "Blocked due to access forbidden") | Return 404 at the bucket root; add `X-Robots-Tag: noindex` on the media/content hosts for non-image responses | Root returns 404 |
| T-13 | **P2** | IndexNow (optional) | Ahrefs notice "Changed pages not submitted to IndexNow" (266) | Optional IndexNow ping (Bing/Yandex) on publish/update. Google doesn't use it | — |
| T-14 | **P2** | Search results page | `/search?q=ring` → **404**; pressing Enter in the search box does nothing | Add a `/search?q=` results page (`noindex,follow`, excluded from the sitemap); Enter submits to it | Enter in search opens results |

### C3. On-page SEO and content

| ID | Pri | Item | Current (2026-10-30) | Fix | Done when |
|---|---|---|---|---|---|
| O-01 | **P0** | Product-page claims (all PDPs) | Still on the PDP policy block: "returns within **30 days** of delivery" (**182** PDPs), "**craftsmanship warranty**" (**180** PDPs), "complimentary **UPS** Overnight shipping", "In-stock pieces usually ship within **2-3 business days**" | Returns: "Returns accepted within 15 days of delivery for unworn pieces; return shipping and duties are paid by the customer." Replace "craftsmanship warranty" with "Free lifetime warranty". Shipping: "Free, insured overnight shipping to every country." Remove "UPS" and "2–3 business days" | Sitewide text search finds 0 × "30 days", 0 × "craftsmanship warranty", 0 × "UPS" |
| O-02 | **P0** | "Apply September sale" promo | Still on **182** PDPs, the cart and checkout ("Apply September sale · Princess Halo Stud Earrings · On orders $1,000+ · FREE") | Remove it, or rename it to the current live offer with real terms (HOD to confirm an offer is running) | No "September" text on the site |
| O-03 | **P0** | Delivery-time conflict | The cart and checkout still show "**Approximately 3 to 4 weeks**" for an in-stock bracelet, next to "Same-day overnight dispatch" | Show the bespoke 3–4 weeks estimate only for made-to-order items; for ready-to-ship items show the Part B shipping promise. **Needs HOD:** which products are ready-to-ship vs made-to-order | An in-stock item in the cart shows the overnight-shipping line only |
| O-04 | **P0** | `/bespoke` "40+ countries" | Still "Fully insured worldwide delivery — complimentary to **40+ countries**" (contradicts "every country"). The confirmed timeline sentence is correct | "Fully insured delivery, free to every country." Keep the IGI/GIA line | No "40+" on the site |
| O-05 | **P1** | `/about` claims and founders | Still shows "Established networks in **20+ countries**", "**2018 New York office opens**", "**Conflict Free**", "**Ethically**", and the founder line "Akshar korat co founder" (lowercase). **Krish Babariya isn't mentioned at all** | Remove "20+ countries", the New York milestone and the ethics/conflict-free badges until HOD supplies proof. Founders block: "Krish Babariya, Co-founder" and "Akshar Korat, Co-founder" (bio text only from Part B). Fix image alt "Fine Jewellery" → "Fine jewelry" | No "20+", "New York", "Conflict Free" or "Ethically" on `/about`; both founders listed |
| O-06 | **P1** | Typos and labels | Nav "**T- BAR**"; menu mixes "**Toi-et moi**" (necklaces) and "**Toi-moi Rings**"; lowercase menu items "**solid**", "**pavé**", "**10K Rose gold**"; footer "Surat, Gujarat **india**"; cart "1 **items**" (Order Summary) and "Shape: **round**"; product material values "10k  Rose gold" (double space, lowercase); "Jewellery" still visible on `/fine-jewellery` (×2) and in old blog titles | "T-Bar"; one consistent label "Toi et Moi"; "Solid", "Pavé", "10K Rose Gold"; "Surat, Gujarat, India"; "1 item"; capitalized option values ("Round"); clean material values ("10K Rose Gold"). Keep URL slugs | Sitewide search finds 0 × "T- BAR", 0 × "india" (lowercase), 0 × "1 items" |
| O-07 | **P1** | Top-bar "FREE WORLDWIDE SHIPPING" link | Still links to `/fine-jewellery/earrings/stud-earrings` (unrelated) | Link to `/shipping`, or make it plain text | — |
| O-08 | **P1** | Homepage H1 must not change with the slider | Static HTML has one H1 "THE BEGINNING OF FOREVER" (approved). The JS build is unchanged since 29 Oct, when each slide rendered its own `<h1>` ("Where Diamonds Find Their Voice") | One fixed `<h1>` for the page ("The Beginning of Forever"); other slide headings as `<h2>`/`<p>` | One `<h1>` in the DOM after the carousel has moved through all slides |
| O-09 | **P1** | Title lengths | **84** indexable titles over 60 characters including " \| House of Diams" (**67 PDPs**, **16 blog** posts, 1 other) | PDPs: `{Product name} \| House of Diams` with the product name ≤ 45 characters (formula in `On-page SEO/07-PDP-ON-PAGE-SEO.md`); drop "Lab-Grown Diamond" from the title where it pushes over 60 (keep it in the H1/description). Blogs: shorten the non-refresh posts; leave the refresh posts (4Cs, shapes, ring size, 14K vs 18K, how-to-choose, certification) until the GSC baseline | Ahrefs "Title too long" ≤ the refresh-post count |
| O-10 | **P1** | Short / placeholder metas | **47** indexable pages have metas under 110 characters, including placeholder-style PDP metas (`/shop/round-radiant-drops` "Earrings · 10K White Gold - House of Diams", `/shop/round-hoop-drops`, `/shop/round-solitaire-studs`), boilerplate `/wedding-bands/for-her` "Browse For Her in Wedding Bands." and `/fine-jewellery/bracelet/bangles` "Browse Bangles in Fine Jewelry.", and one-liners on `/privacy-policy` (34 chars), `/terms` (40), `/about` (79), `/contact` (86) | Write 120–155-character metas for every indexable page. PDP pattern: "{Product}: {shape, total carat, setting} in 10K or 14K gold. Free insured shipping to every country from House of Diams." Category metas from `On-page SEO/01` | Ahrefs "Meta description too short" = 0 on indexable pages |
| O-11 | **P1** | Duplicates | Duplicate H1 "Round Baguette Three-Stone Ring" (2 PDPs). Duplicate metas: "A three-stone engagement ring featuring a round center diamo…" (2 PDPs), "Drop & Dangle · 10K White Gold - House of Diams", "Stud Earrings · 10K White Gold - House of Diams" | Make each product name/meta unique by adding the real distinguishing spec (carat, metal, setting) | No duplicate titles/H1s/metas |
| O-12 | **P1** | Open Graph incomplete | `og:image` and `twitter:image` still missing on **11** pages: `/t-bar` and 10 blog posts (christmas, wife, girlfriend, anniversary-by-year, 10-year anniversary, what-finger, push-present, necklace-layering, how-to-wear, custom-engagement-ring) | Default `og:image` = the article hero/featured image (fallback: brand image 1200×630) | Ahrefs "Open Graph tags incomplete" = 0 |
| O-13 | **P1** | Orphan products | Still **0 internal links** to 6 sitemap PDPs: `elaris-emerald-twist-diamond-ring`, `east-west-oval-diamond-bezel-pendant`, `aurevane-sunburst-round-diamond-halo-stud-earrings`, `virelle-round-twist-diamond-ring`, `seraphina-oval-diamond-pendant-with-accent-bail`, `amora-heart-cut-solitaire-pendant-necklace` | Assign each to its category so it appears in a listing and in related items | Each has ≥ 2 internal inlinks |
| O-14 | **P1** | Bangles taxonomy (F-E7) | `/fine-jewellery/bracelet/bangles` holds link bracelets; title still "Bangles \| Fine Jewelry", H1 "Explore Bangles" | Apply the spec title/H1/meta from `On-page SEO/01` ("Diamond Link Bracelets") until HOD adds real bangles | — |
| O-15 | **P2** | Nav missing key pages | Header nav has no link to **Bespoke**, **Education** or **Blog** (they're only in the footer/body) | Add "Bespoke", "Education" and "Blog" to the desktop and mobile nav | — |

**Already correct (don't redo):**
- The 10 blog packages (title, meta, H1, canonical, links, blog index).
- Titles/metas/H1s on 44 of 49 ready pages; the other 5 are refresh posts waiting for GSC.
- `/contact`, `/bespoke`, `/shipping`, `/returns` and `/about` titles + H1s.
- The `/bespoke` timeline sentence, including "depends on the selected stone".
- FAQPage only on `/faq`; Organization author on all articles; BreadcrumbList on 245/246 pages.
- `by-desgin` → `by-design` 301s.
- All 52 previously missing internal links present.
- "Fine Jewelry", "Solitaire" and "Anniversary" menu labels.
- Empty listings noindex + out of the sitemap and `llms.txt`.
- Test article/product removed from the site.
- The cart, checkout and `/returns` say 15-day returns, insured shipping, lifetime warranty, resizing and cleaning; "Order before 3 PM" and "tesxt 1" are gone.
- Organization `founder`, `email` and `sameAs` in schema.
- `media.*` and `/_next/image` cached at CloudFront.

### C4. Structured data

| ID | Pri | Item | Current (2026-10-30) | Fix | Done when |
|---|---|---|---|---|---|
| S-01 | **P0** | Merchant listing fields | No `shippingDetails` and no `hasMerchantReturnPolicy` on any PDP (checked on the bracelet and ring PDPs). `material` is now one array in page source, but its values are messy ("10k  Rose gold") | In every `Offer`: `shippingDetails` (`OfferShippingDetails`: `shippingRate` 0 USD, `shippingDestination` = the countries you ship to; add `deliveryTime` **only if HOD confirms transit time**) and `hasMerchantReturnPolicy` (`MerchantReturnPolicy`: `returnPolicyCategory` FiniteReturnWindow, `merchantReturnDays` 15, `returnMethod` ReturnByMail, `returnFees` ReturnShippingFees, `applicableCountry`). Or define the return policy once on the Organization and reference it. Clean the `material` values | Rich Results Test on 3 PDPs: no warnings; GSC Merchant listings warnings start validating |
| S-02 | **P0** | Unconfirmed New York address | Still in the Organization schema on **all 246 pages** (second `PostalAddress` New York, NY, US). Still shown in the **contact side panel** ("Address: 36 W 44th Street, Suite 1000B, New York, 10036, USA") | Remove both until HOD confirms it is a real, staffed location (see L-01) | No "New York" or "44th" in the HTML of any page |
| S-03 | **P1** | Organization address completeness | The Surat `PostalAddress` in schema still has no `streetAddress` or `postalCode` | `streetAddress` "831, Pragati IT World, Yogi Chowk", `addressLocality` Surat, `addressRegion` Gujarat, `postalCode` 395010, `addressCountry` IN, `telephone` "+91 93285 36178" (same as the footer). Keep `founder`/`sameAs` (already correct), `logo` ≥ 112×112 | — |
| S-04 | **P1** | Category ItemList | Still no `ItemList` on `/`, `/shop`, `/engagement-rings`, `/fine-jewellery` | Add an `ItemList` of the products shown (url + position) on those 4 | Ahrefs issue = 0 |
| S-05 | **P2** | Homepage BreadcrumbList (optional) | Missing only on `/` | Optional: leave as is, or add a single-item list | — |
| S-06 | **P2** | WebSite schema | Still not present | Add `WebSite` (`name`, `url`) on the homepage | — |

### C5. Performance (Lighthouse / PageSpeed)

**Measured on 30 Oct** with Lighthouse 13.6 (local run, simulated mobile throttling). Single runs vary by a few points; the changes from 29 Oct are within that noise, as expected with the same build.

| Template | Mobile Perf | Mobile LCP | Desktop Perf | A11y | Best Pr. | SEO | Agentic |
|---|---|---|---|---|---|---|---|
| Home | 71 | 6.0 s | 76 | 92 | 100 | 100 | 2/3 |
| /shop | 74 | 5.6 s | 76 | 92 | 100 | 100 | 2/3 |
| /engagement-rings | 33 | 7.7 s (TBT 2,450 ms) | 78 | 92 | 100 | 100 | 2/3 |
| Category (tennis bracelet) | 72 | 6.5 s | 79 | 92 | 100 | 100 | 2/3 |
| PDP (bracelet) | 69 | 6.1 s (4.2 MB mobile / 14.4 MB desktop) | 75 | 92–93 | 100 | 100 | 2/3 |
| /blog · article | 73 · 93 | 5.8 · 2.4 s | 78 · 85 | 96 | 100 | 100 | 2/3 |
| /bespoke · /about · /contact · /faq | 77 · 81 · 89 · 90 | 4.1 · 4.1 · 2.7 · 2.5 s | 84 · 81 · 86 · 85 | 91–96 | 100 | 100 | 2/3 |

| ID | Pri | Item | Evidence (30 Oct) | Fix |
|---|---|---|---|---|
| P-01 | **P0** | LCP image is lazy-loaded | The LCP element is still `loading="lazy"`: the home hero slide (`alt="SHOP ENGAGEMENT RINGS"`) and the first product card on /shop, /engagement-rings and categories (`lcp-discovery` fails) | First hero slide and the first 2 (mobile) / 4 (desktop) product-card images: `priority` (`fetchpriority="high"`, no lazy). The slider must not auto-advance before first paint; preload only slide 1 |
| P-02 | **P0** | PDP autoplay video (BUG-008) | The bracelet PDP still has `<video autoPlay preload="none">` pointing to a **16 MB** MP4; desktop page weight 14.4 MB; the LCP element is an `aria-hidden` poster image | Poster image first (priority); load the video only after interaction, or when idle and in the viewport; serve a ≤ 1.5 MB 720p H.264/WebM; no autoplay on mobile/save-data |
| P-03 | **P1** | Oversized images | "Improve image delivery": 477 KiB savings on the PDP (250 KB gift thumbnail shown at 46×46 px), 194 KiB on /engagement-rings | Route every image through `next/image` with correct `sizes`; thumbnails ≤ 15 KB; AVIF/WebP; quality 70–75 |
| P-04 | **P1** | Element render delay | Text LCP on article/FAQ/contact waits for client JS (fade-in animation / hydration) | Render text LCP elements server-side without an opacity animation; remove entry animations above the fold |
| P-05 | **P1** | Render-blocking CSS / legacy JS / unused JS | Render-blocking CSS, 14 KiB legacy polyfills and 21–70 KiB unused JS on every template | Inline critical CSS; modern `browserslist`; code-split filters/quiz/reels/cookie modal with `dynamic(() => …, { ssr:false })`; load GTM `afterInteractive`/`lazyOnload` |
| P-06 | **P1** | Third-party flag preload | Every page still preloads `cdn.jsdelivr.net/gh/lipis/flag-icons/.../us.svg` | Self-host the one flag SVG inline; drop the jsdelivr preload |
| P-07 | **P1** | Fonts | Inter variable font 109 KB | Subset to Latin, `font-display: swap`, preload only the weight used above the fold |
| P-08 | **P1** | Caching | `cache-insight` fails on all pages (product images under `/products/draft/…`) | Covered by T-02; also move published images out of the `draft/` path |

**Realistic targets:**
- Accessibility 100, Best Practices 100, SEO 100 and Agentic Browsing 3/3 are achievable on every template.
- Performance ≥ 95 desktop / ≥ 90 mobile on the key templates (home, category, PDP, blog) is achievable with T-02, T-04 and P-01…P-07.
- 100 mobile Performance on an image- and video-led store is not realistic, and not needed. The ranking signal is the field Core Web Vitals (LCP < 2.5 s, INP < 200 ms, CLS < 0.1).

### C6. Accessibility + Agentic Browsing

| ID | Pri | Item | Evidence (30 Oct) | Fix |
|---|---|---|---|---|
| A-01 | **P0** | `presentation-role-conflict` (fails Agentic Browsing + Accessibility on all 22 runs) | Currency selector flag is still `<img aria-label="United States" alt="" src=".../flags/4x3/us.svg">` | Use `alt="United States"` and remove `aria-label` (or `alt=""` + `aria-hidden="true"`, with the visible "United States (USD)" text as the button name). **This alone makes Agentic Browsing 3/3** |
| A-02 | **P1** | `color-contrast` (all 22 runs) | "USD ONLY" (`text-white/45`), the cookie banner eyebrow "COOKIES" (#91969e on white), PDP "On orders $1,000+" | Raise to ≥ 4.5:1 (e.g. `text-white/70`, `#6b7078`) |
| A-03 | **P1** | `button-name` on `/bespoke` | Select triggers "Piece Type *", "Preferred Stone", "Approx. Carat", "Preferred Metal" have no accessible name | `aria-labelledby` pointing to each field label |
| A-04 | **P1** | `aria-allowed-attr` on `/faq` | `<input type="search" aria-expanded …>` | Add `role="combobox"` (or drop `aria-expanded`) |
| A-05 | **P1** | `aria-prohibited-attr` on home | `<div aria-label="Instagram reel navigation">` | Add `role="group"` |
| A-06 | **P1** | `target-size` | Product-card image dots (5×5 / 10×5 px) on /shop, /engagement-rings, categories and the PDP | ≥ 24×24 px hit area (padding), or hide the dots on mobile |
| A-07 | **P1** | `label-content-name-mismatch` (new in this list; fails on /shop, /engagement-rings, categories, /blog, PDP) | The listing sort button (`aria-label="Sort products"`), the PDP gift block (`<aside aria-label="Gift of…">`) and a full-width PDP button have aria-labels that don't contain their visible text | Make each `aria-label` start with the visible text, or remove the `aria-label` so the visible text is the name |
| A-08 | **P2** | Image-only links | Mega-menu image tiles are links whose only content is an image | Give each tile `<img>` a meaningful `alt` (the category name) |

### C7. Frontend QA (payment/checkout not tested)

| ID | Pri | Bug | Evidence (30 Oct) | Fix |
|---|---|---|---|---|
| Q-01 | **P0** | Size silently pre-selected | Ring PDP (`/shop/elowen-round-halo-engagement-ring`) still has **US 4** pressed by default. The bracelet PDP still defaults to **6 Inch**, and Add To Bag adds it without the visitor choosing | No default size/length; Add To Bag disabled (or an inline error "Select your ring size") until one is chosen |
| Q-02 | **P1** | Search Enter does nothing | See T-14 (`/search` returns 404) | See T-14 |
| Q-03 | **P1** | Cookie banner over dialogs | On desktop on 30 Oct the love-letter dialog (z-index 3100) sat above the cookie banner (z-index 2000). The build is unchanged since the 29 Oct observation of the banner covering the dialog, so recheck at 375 px | Dialogs above the banner, or show the banner first and block other modals until it is answered |
| Q-04 | **P1** | Cart flashes "(0 items)" | Not reproduced on desktop on 30 Oct; the build is unchanged since it was seen on 29 Oct | Render a skeleton until the cart state is hydrated; verify on slow mobile |
| Q-06 | **P1** | Tax line for non-US visitors | From India the cart still adds **$40.20 tax** (12 %) on a $335 USD order | Developer to confirm the tax rules per destination; the owner checks at checkout |
| Q-07 | **P1** | Login host | Login still redirects to **`auth-uat.houseofdiams.com`** | Use a production auth host (e.g. `auth.houseofdiams.com`); `noindex` it |
| Q-08 | **P2** | Clear bag has no confirmation | One click still empties the bag | Optional confirm or "Undo" toast |
| Q-09 | **P2** | Contact page | `/contact` still shows no email/phone/address/reply time on the page itself | Show the approved NAP block + "Replies within 24 hours" (see L-02) |

**Regression checks before delivery (desktop + 375 px mobile):**
- Every header/mega-menu/footer link returns 200 and lands on a page with products.
- Search suggestions + Enter.
- PDP flow: option selection (metal, size/length, engraving) → Add To Bag → drawer → View Cart → quantity/remove/clear → Checkout opens (stop there).
- Wishlist logged out (should prompt login) and logged in.
- Contact and bespoke forms show validation on empty submit.
- WhatsApp, mailto and tel links.
- Cookie Reject/Accept/Customize persist across pages.
- An unknown URL returns HTTP 404 with `noindex`.

### C8. Local SEO (site side only)

| ID | Pri | Item | Fix |
|---|---|---|---|
| L-01 | **P0** | New York address | Still in the schema and in the contact side panel (S-02). It's not a confirmed HOD fact. Remove it until HOD confirms it is a real, staffed location |
| L-02 | **P1** | One consistent NAP everywhere | Footer, `/contact`, `/about` and schema must show the same block: **House of Diams, 831, Pragati IT World, Yogi Chowk, Surat, Gujarat 395010, India · +91 93285 36178 · admin@houseofdiams.com · Headquarters & workshop, by appointment only**. Fix the lowercase "india" in the footer |
| L-03 | **P1** | Contact page | Add the NAP block, "Replies within 24 hours", a click-to-load map of the Surat workshop (so it doesn't hurt LCP), and opening/appointment hours once HOD supplies them |
| L-04 | **P2** | LocalBusiness schema | Only after HOD confirms visiting hours: add `JewelryStore` on `/contact` with the L-02 NAP, `openingHoursSpecification`, `geo` and `hasMap` |
| L-05 | owner | Google Business Profile | Owner task (off-site): create/verify a GBP for the Surat workshop with the identical NAP and link it to `https://houseofdiams.com/contact` |

### C9. GA4 / GTM / consent

Observed on 30 Oct, before the visitor makes a cookie choice:
- `window.dataLayer` is empty and GTM is not loaded, so no consent default is sent.
- The site code still contains a hard-coded GA4 path (`NEXT_PUBLIC_GA_MEASUREMENT_ID || "G-0LVQJ1YDJ0"` with `gtag(... 'config' ...)` and `send_page_view`) next to GTM.
- No GA4 ecommerce event names (`view_item`, `view_item_list`, `begin_checkout`, `purchase`, …) are in the main JS bundles.
- From GA4 (29 Oct): `purchase` has no data and the funnel events are missing.

| ID | Pri | Fix |
|---|---|---|
| G-01 | **P0** | **Consent Mode v2 (advanced):** load GTM on every page. Before it, push `gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',wait_for_update:500})`. On the visitor's choice push `gtag('consent','update',{…})` (the update code exists) — never a second `default`. Re-apply the stored choice on each page load |
| G-02 | **P0** | **One GA4 path only:** remove the hard-coded `gtag('config','G-0LVQJ1YDJ0')` page-view component and fire GA4 only from GTM (or remove GA4 from GTM, not both). Send exactly one `page_view` per App Router navigation. Verify in GTM Preview + GA4 DebugView |
| G-03 | **P0** | **GA4 ecommerce dataLayer** (standard `items[]`: `item_id` = SKU, `item_name`, `item_category`, `item_variant` = metal, `price`, `quantity`, `currency:'USD'`): `view_item_list`, `select_item`, `view_item`, `add_to_cart`, `remove_from_cart`, `view_cart`, `add_to_wishlist`, `begin_checkout`, `add_shipping_info`, `add_payment_info`, `purchase` (order-confirmation page, once per `transaction_id`, with `value`, `tax`, `shipping`, `coupon`) |
| G-04 | **P1** | Lead events: `generate_lead` on successful contact/bespoke submit (with `form_name`), `sign_up`/`login`, `view_search_results` with `search_term`. Owner: mark `purchase` and `generate_lead` as key events; delete the unused `close_convert_lead`/`qualify_lead` |
| G-05 | owner | GA4 settings: stream URL → `https://houseofdiams.com`; data retention 14 months; internal-traffic filter; unwanted referral `razorpay.com`; link GA4 ↔ Search Console |
| G-06 | **P1** | The CSP is `report-only` and already allows GTM/GA/Clarity/Pinterest; keep it in sync with any new tag before enforcing |

### C10. Google Search Console (owner actions, after T-01)

As of 29 Oct: 148 indexed / 453 not indexed.

| ID | Who | Action |
|---|---|---|
| GSC-01 | owner | After T-01: submit `https://houseofdiams.com/sitemap.xml` and remove the `www` sitemap. URL-inspect + "Request indexing" for the homepage, `/engagement-rings`, `/fine-jewellery`, `/wedding-bands`, `/bespoke` and the top 5 blog posts |
| GSC-02 | owner | Start "Validate fix" on Server error (5xx), Redirect error, Not found (404), and Merchant listings warnings (after S-01) |
| GSC-03 | dev | The "Crawled – currently not indexed" category pages need unique, useful content: a 60–120-word intro above the grid, a short buying guide/FAQ block below it (text from `On-page SEO/04`, facts from Part B only), and links from relevant blog/education posts |
| GSC-04 | owner | Check that Settings → "Search generative AI" is not set to exclude; check Crawl stats for 5xx after T-02/T-03 |

---

## PART D — Items that need HOD (don't implement until answered)

1. Is "36 W 44th Street, Suite 1000B, New York" a real, staffed HOD location, and did a New York office open in 2018? (L-01, S-02, O-05)
2. Which products are ready-to-ship (overnight) vs made-to-order (3–4 weeks)? (O-03)
3. Is the carrier UPS? What is the real transit time, for `deliveryTime` in schema? (O-01, S-01)
4. Is any promo running now (to replace "September sale")? (O-02, T-11)
5. Proof for "20+ countries", "Conflict Free" and "Ethically"? (O-05)
6. Visiting / appointment hours for the Surat workshop? (L-03, L-04)
7. Should a 12 % tax apply to orders from India in USD? (Q-06)

## PART E — Acceptance checks (run all against production; paste the output into the delivery report)

```bash
# 0. Proof of deploy: the build must differ from the 29/30 Oct build (chunk 066_9qs-fr7km.js must be gone)
curl -s https://houseofdiams.com/ | grep -c '066_9qs-fr7km.js'
# 1. Host + redirects (expect one 301 each, straight to https://houseofdiams.com/...)
for u in http://www.houseofdiams.com/ https://www.houseofdiams.com/shop?page=2 http://houseofdiams.com/fine-jewellery; do curl -sI "$u" | grep -iE '^HTTP|^location'; done
# 2. Static assets cached (second call must say Hit)
u=https://houseofdiams.com$(curl -s https://houseofdiams.com/ | grep -oE '/_next/static/chunks/[^"]+\.js' | head -1); curl -sI $u >/dev/null; curl -sI $u | grep -i x-cache
# 3. Burst test: 0 non-200
curl -s https://houseofdiams.com/ | grep -oE '/_next/static/[^"]+\.(js|css)' | sort -u | sed 's#^#https://houseofdiams.com#' | xargs -P 50 -n 1 curl -s -o /dev/null -w '%{http_code}\n' | sort | uniq -c
# 4. Forbidden text sitewide (expect no output)
curl -s https://houseofdiams.com/sitemap.xml | grep -oE 'https://[^<]+' | xargs -P 6 -n 1 curl -s | grep -oiE '30 days|craftsmanship warranty|september sale|jwelery|jewelery|40\+ countries|20\+ countries|New York|44th Street|pin\.it|www\.houseofdiams|UPS Overnight|T- BAR' | sort | uniq -c
# 5. Lighthouse (mobile + desktop) on: / /shop /engagement-rings /fine-jewellery/bracelet/tennis-bracelet /shop/rosette-five-flower-bracelet /blog /bespoke
npx lighthouse@13.6.0 https://houseofdiams.com/ --only-categories=performance,accessibility,best-practices,seo,agentic-browsing --output=json --output-path=./lh-home-mobile.json
```

Also run:
- Google Rich Results Test on 3 PDPs (0 warnings).
- GTM Preview + GA4 DebugView walk-through: list → item → add_to_cart → view_cart → begin_checkout, one `page_view` per navigation, consent default denied before the choice.
- A new Ahrefs crawl of the apex project.
- PageSpeed Insights mobile + desktop on the same 7 URLs.

**Targets at delivery:**
- Ahrefs apex project: 100 % health, with no "links to redirect", "OG incomplete", "ItemList missing" or "meta too short" warnings.
- Lighthouse: Accessibility / Best Practices / SEO = 100 and Agentic Browsing 3/3 on every template; Performance ≥ 90 mobile / ≥ 95 desktop on key templates.
- GSC: apex sitemap "Success", Merchant listings without warnings.
- GA4: full ecommerce funnel + leads, one `page_view` per navigation, Consent Mode v2 active.
