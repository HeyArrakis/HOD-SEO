# 05 — Final Pre-Delivery Master Fix List (developer work only — re-verified 2026-10-31)

**First audit:** 2026-10-29 · **Re-verified:** 2026-10-30 and 2026-10-31 (fresh scans of all 246 sitemap URLs, Lighthouse 13.6 on 11 templates × mobile/desktop on 30 Oct, browser QA). Evidence: `Technical/2026-10-30-live-validation/` and `Technical/2026-10-31-cms-changes/`.
**Site:** https://houseofdiams.com (canonical host = apex) · **Prepared for:** the developer, to hand directly to Claude Code.

> **Nothing new is deployed yet.** On 2026-10-31 the live site still serves the same JavaScript build as on 29 Oct (chunk `066_9qs-fr7km.js` is still present), `www` still answers 200 and CloudFront still misses on `/_next/static`. **Deploy your fixes, then ask for a re-check.**
>
> **This list is code, server and tracking work only.** Text and settings the owner manages in the admin (`manage.houseofdiams.com`) are handled there and are not in this file. These include product-page policy text, coupons, About page content, top bar, hero, category/product SEO fields and menu labels. **Don't hard-code or overwrite CMS content.**

**Not tested on purpose:** the payment step and order placement (the owner tests these).

---

## PART A — PROMPT FOR CLAUDE CODE (copy everything from here to the end of the file)

You are working in the House of Diams website codebase. It is a Next.js App Router site behind nginx + CloudFront on AWS, with an admin CMS at `manage.houseofdiams.com`. Media is served from `media.houseofdiams.com` / `content.houseofdiams.com`. Tags: GTM `GTM-TJ5HTTSD`, GA4 `G-0LVQJ1YDJ0`. Implement every item in Part C in the priority order given, **deploy to production**, then run the acceptance checks in Part D.

**Rules — follow exactly:**
1. **Do not invent business facts.** Customer-facing copy may only state the facts in Part B. If a fix would need any other fact, leave that text out.
2. **Do not touch payment/checkout logic** (Razorpay, order creation, pricing, tax calculation). Text and labels on the cart page are in scope; payment code is not.
3. **Do not change any URL slug** unless an item says so. Every URL that stops returning 200 must get a 1:1 301 to its replacement. Never use 302/307 for permanent moves.
4. **No test content on production.** Test products, articles and categories must stay unpublished, excluded from the sitemap, `noindex`, and out of listings, search and related items. Do QA on a staging host that sends `X-Robots-Tag: noindex` and is not linked from production.
5. **American English** in all customer-facing copy, labels, alt text and anchors ("jewelry", never "jewellery/jewelery/jwelery"). Do **not** rename the `/fine-jewellery/` URLs.
6. **Content comes from the CMS.** Don't hard-code text that the CMS manages, and don't overwrite CMS records in migrations or seeds.
7. **Do not add FAQPage schema** anywhere except `/faq`, where it is already correct. Do not fabricate reviews/ratings, GTINs, awards or certifications in schema.
8. Keep changes small and reviewable: one commit per item ID (e.g. `fix(T-01): www→apex 301`). Do not refactor unrelated code.
9. After each P0/P1 item, run the item's **Done when** check **against the live production site** and paste the result into your report.

---

## PART B — Confirmed HOD facts (the only claims allowed in code or schema)

| Topic | Approved wording basis |
|---|---|
| Shipping | Free shipping to every country; every order is insured; same-day overnight shipping; no order cut-off time |
| Returns | Returns within **15 days** of delivery, unworn; refund issued once the piece reaches HOD; return shipping and duties paid by the customer. Bespoke/custom pieces are not returnable unless the finished piece does not match the agreed design |
| Certification | IGI and GIA certificates |
| Services | Free resizing; free annual cleaning; free lifetime warranty (no terms published) |
| Bespoke timing | Typically 2–3 weeks to make + about 6–9 days delivery; about 3–4 weeks from design approval; depends on the selected stone; estimates, not guarantees |
| Company | Founders **Krish Babariya** and **Akshar Korat**; in the trade since 2014; public email **admin@houseofdiams.com** only |
| Address | **House of Diams, 831, Pragati IT World, Yogi Chowk, Surat, Gujarat 395010, India** · +91 93285 36178 · headquarters & workshop, by appointment only |
| Social | Instagram `https://www.instagram.com/houseofdiams_/`, Facebook `https://www.facebook.com/profile.php?id=61593287138869`, Pinterest `https://in.pinterest.com/HouseofDiams_/` |

**Not allowed anywhere in code or schema:** the New York address ("36 W 44th Street, Suite 1000B"), "UPS", "40+ countries", "20+ countries", "Conflict Free", "Ethically", "2–3 business days", or a reply-time promise.

---

## PART C — FIX LIST (all items below were still open on the live site on 2026-10-31)

Priority: **P0** = must fix before delivery (blocks indexing, tracking or trust) · **P1** = needed for the 100/100 targets · **P2** = polish.

### C1. Why Ahrefs shows two different scores

| Project | Score | Why |
|---|---|---|
| `www.houseofdiams.com` | **69 %**, 312 URLs with errors | `www` is still a full copy of the site (HTTP 200, no redirect; still true on 31 Oct). During its 28 Oct crawl, 8 core JavaScript chunks returned 500/502 from the origin, so Ahrefs flagged "Page has broken JavaScript" on 304 pages. The other errors come from the `www` pages canonicalizing to the apex |
| `houseofdiams.com` | **100 %**, 0 errors | The apex host. Its remaining warnings are covered by C2–C4 |

**Root causes (both still present on 31 Oct):**
1. CloudFront does not cache `/_next/static/*`. Repeat requests still say `x-cache: Miss from cloudfront`.
2. `www` is not redirected to the apex.

Fixing T-01, T-02 and T-03 removes the `www` errors. The owner will then re-crawl in Ahrefs.

### C2. Technical SEO

| ID | Pri | Item | Current (2026-10-31) | Fix | Done when |
|---|---|---|---|---|---|
| T-01 | **P0** | `www` → apex 301 | `https://www.houseofdiams.com/` and `/shop?page=2` return **200**. `http://www…/x` → 301 → `https://www…/x` (200), a 2-hop chain to a duplicate | One rule at CloudFront (viewer-request Function) or nginx: any request with `Host: www.houseofdiams.com` (http or https) → **301** to `https://houseofdiams.com` + same path + same query. Single hop from every variant | `curl -sI "https://www.houseofdiams.com/shop?page=2"` → `301` `location: https://houseofdiams.com/shop?page=2`; `curl -sI http://www.houseofdiams.com/x` → one 301 straight to `https://houseofdiams.com/x` |
| T-02 | **P0** | Cache static JS/CSS at CloudFront | `/_next/static/chunks/*.js` sends `cache-control: public, max-age=31536000, immutable` but CloudFront still answers **Miss** on repeat requests (`media.*` and `/_next/image` already return Hit) | Add a cache behavior for `/_next/static/*` with the managed **CachingOptimized** policy (no cookies, no query strings, no headers except Accept-Encoding). Enable Brotli/Gzip | Second request to any `/_next/static/chunks/*.js` returns `x-cache: Hit from cloudfront` |
| T-03 | **P0** | Keep old chunks available across deploys | Ahrefs/GSC saw 5xx on JS chunks and `www` blog pages during deploy windows (23–24 and 28 Oct) | Keep the previous build's `/_next/static` assets for ≥ 7 days after each deploy (don't delete on deploy). An unknown chunk returns **404**, never 500 | A chunk URL from the previous build still returns 200 after a new deploy |
| T-04 | **P1** | HTML caching / TTFB | Every HTML response is `private, no-cache, no-store` and sets `detected_country`/`detected_currency` cookies. TTFB ≈ 0.97 s. Lighthouse `bf-cache` fails on all 22 runs | Serve public pages (home, categories, PDPs, blog, education, policy pages) with ISR/`revalidate` + `Cache-Control: public, s-maxage=300, stale-while-revalidate=86400`, and revalidate on CMS save. Move country/currency detection to the edge (`CloudFront-Viewer-Country`) or client side, so public HTML doesn't `Set-Cookie`. Keep `no-store` only on cart/checkout/account/API | TTFB < 200 ms on a CloudFront hit; Lighthouse `bf-cache` passes on content pages |
| T-05 | **P1** | Test-content leftover | `/shop/produt-1` still **301s to `/engagement-rings`** | Remove that 301 so it returns 404/410. Add a publish guard: items with "test"/"qa"/"uat" in the title/slug, or flagged draft, are excluded from the sitemap, listings, search, related items and `llms.txt` | `curl -sI https://houseofdiams.com/shop/produt-1` → 404 or 410 |
| T-06 | **P1** | Sitemap `<lastmod>` | Only **182 of 246** sitemap URLs have `<lastmod>` (the product pages) | Add a real content-modified `<lastmod>` to the remaining 64 URLs (categories, blog, education, policy pages) | All sitemap URLs have `<lastmod>` |
| T-07 | **P1** | Footer social links | Pinterest is still `https://pin.it/3G2ogNJNq` (a redirect, flagged on 600+ pages by Ahrefs). Instagram still has tracking parameters (`?igsh=…&utm_source=qr`). There's no Facebook link | Pinterest → `https://in.pinterest.com/HouseofDiams_/`. Instagram → `https://www.instagram.com/houseofdiams_/`. Add Facebook → `https://www.facebook.com/profile.php?id=61593287138869`. If the footer reads these from a CMS field, read them from the CMS "Official profile links" (SEO page) so there is one source | Ahrefs "Page has links to redirect" = 0 |
| T-08 | **P2** | Absolute internal link | One absolute `href="https://houseofdiams.com"` (logo/home link) remains on every page | Use relative `/` | `curl -s https://houseofdiams.com/ \| grep -c 'href="https://houseofdiams.com'` = 0 |
| T-09 | **P1** | Menu links to empty `noindex` pages | The mega-menu still links to **10** empty listings: `/wedding-bands/for-him/classic`, `/diamonds`, `/designer`; `/wedding-bands/for-her/nature`, `/solid`, `/cigar-band`, `/pavee`; `/fine-jewellery/necklaces/initials`, `/tennis-necklace`; `/fine-jewellery/rings/eternity-rings` | Hide a menu item automatically while its category/option has 0 published products; show it again when it has stock. Keep the pages themselves `noindex,follow` and out of the sitemap while empty (already correct) | No rendered menu/footer link points to a page with 0 products |
| T-10 | **P1** | Pagination | `/shop?page=2` and `/engagement-rings?page=2` are OK. Still wrong: `/blog?page=2` canonicalizes to `/blog` and its title has no page number; `/engagement-rings/by-design?page=2` is self-canonical while its page 1 canonicalizes to `/engagement-rings` | `/blog?page=N`: self-canonical + title "Blog – Page N". `/engagement-rings/by-design?page=N`: canonical → `/engagement-rings?page=N`. Link page numbers 1…N, not only "next" | Each `?page=N` URL has a unique title and a consistent canonical |
| T-11 | **P1** | `/promo-codes-and-offers` | 200, indexable, not in the sitemap, thin (two offer images and a gift link; the active offer changes over time) | `noindex,follow`, keep it out of the sitemap | The page sends `noindex,follow` |
| T-12 | **P2** | Media host root | `https://media.houseofdiams.com/` returns **403** (GSC "Blocked due to access forbidden") | Return 404 at the bucket root; add `X-Robots-Tag: noindex` on the media/content hosts for non-image responses | Root returns 404 |
| T-13 | **P2** | IndexNow (optional) | Ahrefs notice "Changed pages not submitted to IndexNow" (266) | Optional IndexNow ping (Bing/Yandex) on publish/update. Google doesn't use it | — |
| T-14 | **P2** | Search results page | `/search?q=ring` → **404**; pressing Enter in the search box does nothing | Add a `/search?q=` results page (`noindex,follow`, excluded from the sitemap); Enter submits to it | Enter in search opens results |

### C3. On-page (code side)

| ID | Pri | Item | Current (2026-10-31) | Fix | Done when |
|---|---|---|---|---|---|
| O-03 | **P0** | Delivery-time line in cart/checkout | The cart and checkout show "**Approximately 3 to 4 weeks**" for every item, including an in-stock bracelet, next to "Same-day overnight dispatch" | Add a per-product "Made to order" flag in the product editor (default off). Show the 3–4-week bespoke estimate only for made-to-order and bespoke items; other items show only the shipping line from Part B. The owner sets the flag per product | An item without the flag shows no "3 to 4 weeks" line |
| O-06 | **P1** | Code-generated labels | Cart Order Summary "1 **items**"; cart line "Shape: **round**" (the slug is shown instead of the shape name); breadcrumb on `/fine-jewellery` "Fine Jewellery" | Pluralize correctly ("1 item"); show the shape's display name ("Round"); build breadcrumbs from the category **name** ("Fine Jewelry"), never from the slug or banner text | Cart shows "1 item" and "Shape: Round"; breadcrumb shows "Fine Jewelry" |
| O-08 | **P2** | Homepage H1 must not change with the slider | Today the hero has one slide (H1 "THE BEGINNING OF FOREVER"). The code renders each slide's heading as an `<h1>`, so adding slides creates several H1s | One fixed `<h1>` for the page; slide headings as `<h2>`/`<p>` | One `<h1>` in the DOM with two or more slides |
| O-12 | **P1** | Open Graph image fallback | `og:image`/`twitter:image` missing on **11** pages: `/t-bar` and 10 blog posts (christmas, wife, girlfriend, anniversary-by-year, 10-year anniversary, what-finger, push-present, necklace-layering, how-to-wear, custom-engagement-ring). Other pages fall back to `logo.jpeg` | Fallback order: page share image (CMS) → article featured/hero image or category banner → CMS "Default share image" (SEO page) → brand image 1200×630 | Every indexable page has `og:image` and `twitter:image` |
| O-14 | **P1** | Bangles page metadata | `/fine-jewellery/bracelet/bangles` still "Bangles \| Fine Jewelry", H1 "Explore Bangles", meta "Browse Bangles in Fine Jewelry." (it holds link bracelets) | Apply the spec values the same way as the other option pages (e.g. tennis-bracelet): title "Diamond Link Bracelets", meta "Shop House of Diams diamond link bracelets in open-link designs set with pavé diamonds." (`On-page SEO/01`). If option pages have no SEO fields in the CMS, add SEO title / H1 / meta / intro fields to the option editor, like top-level categories have | Title, H1 and meta match the spec |
| O-15 | **P2** | Nav links to Blog and Education | The Navbar Builder only offers items tied to a category, so "Blog" and "Education" can't be added (the "Bespoke" item exists and the owner can show it) | Allow plain direct-link items in the Navbar Builder (label + URL, no category), on desktop and mobile | Owner can add "Blog" and "Education" from the admin |

### C4. Structured data

| ID | Pri | Item | Current (2026-10-31) | Fix | Done when |
|---|---|---|---|---|---|
| S-01 | **P0** | Merchant listing fields | No `shippingDetails` and no `hasMerchantReturnPolicy` on any PDP | In every `Offer`: `shippingDetails` (`OfferShippingDetails`: `shippingRate` 0 USD, `shippingDestination` = all countries) and `hasMerchantReturnPolicy` (`MerchantReturnPolicy`: `returnPolicyCategory` FiniteReturnWindow, `merchantReturnDays` 15, `returnMethod` ReturnByMail, `returnFees` ReturnShippingFees, `applicableCountry`). Or define the return policy once on the Organization and reference it. Don't add `deliveryTime` | Rich Results Test on 3 PDPs: no warnings; GSC Merchant listings warnings start validating |
| S-02 | **P0** | New York address (schema + contact side panel) | Still in the Organization schema on **all 246 pages** (second `PostalAddress` New York, NY, US) and in the **contact side panel** ("Address: 36 W 44th Street, Suite 1000B, New York, 10036, USA"). It is not in the CMS contact cards, so it is hard-coded | Remove both. The side panel should show the CMS Contact Info cards (email, phone, Surat atelier) | No "New York" or "44th" in the HTML of any page |
| S-03 | **P1** | Organization address completeness | The Surat `PostalAddress` has no `streetAddress` or `postalCode` | `streetAddress` "831, Pragati IT World, Yogi Chowk", `addressLocality` Surat, `addressRegion` Gujarat, `postalCode` 395010, `addressCountry` IN, `telephone` "+91 93285 36178". Keep `founder`/`email`/`sameAs` (already correct), `logo` ≥ 112×112 | — |
| S-04 | **P1** | Category ItemList | No `ItemList` on `/`, `/shop`, `/engagement-rings`, `/fine-jewellery` | Add an `ItemList` of the products shown (url + position) on those 4 | Ahrefs issue = 0 |
| S-05 | **P2** | Homepage BreadcrumbList (optional) | Missing only on `/` | Optional single-item list | — |
| S-06 | **P2** | WebSite schema | Not present | Add `WebSite` (`name`, `url`) on the homepage | — |

### C5. Performance (Lighthouse / PageSpeed)

**Measured on 30 Oct** with Lighthouse 13.6 (local run, simulated mobile throttling). The build is unchanged on 31 Oct.

| Template | Mobile Perf | Mobile LCP | Desktop Perf | A11y | Best Pr. | SEO | Agentic |
|---|---|---|---|---|---|---|---|
| Home | 71 | 6.0 s | 76 | 92 | 100 | 100 | 2/3 |
| /shop | 74 | 5.6 s | 76 | 92 | 100 | 100 | 2/3 |
| /engagement-rings | 33 | 7.7 s (TBT 2,450 ms) | 78 | 92 | 100 | 100 | 2/3 |
| Category (tennis bracelet) | 72 | 6.5 s | 79 | 92 | 100 | 100 | 2/3 |
| PDP (bracelet) | 69 | 6.1 s (4.2 MB mobile / 14.4 MB desktop) | 75 | 92–93 | 100 | 100 | 2/3 |
| /blog · article | 73 · 93 | 5.8 · 2.4 s | 78 · 85 | 96 | 100 | 100 | 2/3 |
| /bespoke · /about · /contact · /faq | 77 · 81 · 89 · 90 | 4.1 · 4.1 · 2.7 · 2.5 s | 84 · 81 · 86 · 85 | 91–96 | 100 | 100 | 2/3 |

| ID | Pri | Item | Evidence | Fix |
|---|---|---|---|---|
| P-01 | **P0** | LCP image is lazy-loaded | The LCP element is `loading="lazy"`: the home hero slide and the first product card on /shop, /engagement-rings and categories (`lcp-discovery` fails) | First hero slide and the first 2 (mobile) / 4 (desktop) product-card images: `priority` (`fetchpriority="high"`, no lazy). The slider must not auto-advance before first paint; preload only slide 1 |
| P-02 | **P0** | PDP autoplay video (BUG-008) | The bracelet PDP has `<video autoPlay preload="none">` pointing to a **16 MB** MP4; desktop page weight 14.4 MB; the LCP element is an `aria-hidden` poster image | Poster image first (priority); load the video only after interaction, or when idle and in the viewport; transcode uploads to ≤ 1.5 MB 720p H.264/WebM; no autoplay on mobile/save-data. The same applies to the CMS banner videos (bespoke showcase, service banner) |
| P-03 | **P1** | Oversized images | "Improve image delivery": 477 KiB savings on the PDP (250 KB gift thumbnail shown at 46×46 px), 194 KiB on /engagement-rings | Route every image through `next/image` with correct `sizes`; thumbnails ≤ 15 KB; AVIF/WebP; quality 70–75 |
| P-04 | **P1** | Element render delay | Text LCP on article/FAQ/contact waits for client JS (fade-in animation / hydration) | Render text LCP elements server-side without an opacity animation; remove entry animations above the fold |
| P-05 | **P1** | Render-blocking CSS / legacy JS / unused JS | Render-blocking CSS, 14 KiB legacy polyfills and 21–70 KiB unused JS on every template | Inline critical CSS; modern `browserslist`; code-split filters/quiz/reels/cookie modal with `dynamic(() => …, { ssr:false })`; load GTM `afterInteractive`/`lazyOnload` |
| P-06 | **P1** | Third-party flag preload | Every page preloads `cdn.jsdelivr.net/gh/lipis/flag-icons/.../us.svg` | Self-host the one flag SVG inline; drop the jsdelivr preload |
| P-07 | **P1** | Fonts | Inter variable font 109 KB | Subset to Latin, `font-display: swap`, preload only the weight used above the fold |
| P-08 | **P1** | Caching / image paths | `cache-insight` fails on all pages (product images under `/products/draft/…`) | Covered by T-02; also move published images out of the `draft/` path |

**Realistic targets:**
- Accessibility 100, Best Practices 100, SEO 100 and Agentic Browsing 3/3 are achievable on every template.
- Performance ≥ 95 desktop / ≥ 90 mobile on the key templates (home, category, PDP, blog) is achievable with T-02, T-04 and P-01…P-07.
- 100 mobile Performance on an image- and video-led store is not realistic, and not needed. The ranking signal is the field Core Web Vitals (LCP < 2.5 s, INP < 200 ms, CLS < 0.1).

### C6. Accessibility + Agentic Browsing

| ID | Pri | Item | Evidence | Fix |
|---|---|---|---|---|
| A-01 | **P0** | `presentation-role-conflict` (fails Agentic Browsing + Accessibility on all 22 runs) | Currency selector flag is `<img aria-label="United States" alt="" src=".../flags/4x3/us.svg">` | Use `alt="United States"` and remove `aria-label` (or `alt=""` + `aria-hidden="true"`, with the visible "United States (USD)" text as the button name). **This alone makes Agentic Browsing 3/3** |
| A-02 | **P1** | `color-contrast` (all 22 runs) | "USD ONLY" (`text-white/45`), the cookie banner eyebrow "COOKIES" (#91969e on white), PDP "On orders $1,000+" | Raise to ≥ 4.5:1 (e.g. `text-white/70`, `#6b7078`) |
| A-03 | **P1** | `button-name` on `/bespoke` | Select triggers "Piece Type *", "Preferred Stone", "Approx. Carat", "Preferred Metal" have no accessible name | `aria-labelledby` pointing to each field label |
| A-04 | **P1** | `aria-allowed-attr` on `/faq` | `<input type="search" aria-expanded …>` | Add `role="combobox"` (or drop `aria-expanded`) |
| A-05 | **P1** | `aria-prohibited-attr` on home | `<div aria-label="Instagram reel navigation">` | Add `role="group"` |
| A-06 | **P1** | `target-size` | Product-card image dots (5×5 / 10×5 px) on /shop, /engagement-rings, categories and the PDP | ≥ 24×24 px hit area (padding), or hide the dots on mobile |
| A-07 | **P1** | `label-content-name-mismatch` (/shop, /engagement-rings, categories, /blog, PDP) | The listing sort button (`aria-label="Sort products"`), the PDP gift block (`<aside aria-label="Gift of…">`) and a full-width PDP button have aria-labels that don't contain their visible text | Make each `aria-label` start with the visible text, or remove the `aria-label` so the visible text is the name |
| A-08 | **P2** | Image-only links | Mega-menu image tiles are links whose only content is an image | When the CMS alt text is empty, use the category name as the image `alt` |

### C7. Frontend QA (payment/checkout not tested)

| ID | Pri | Bug | Evidence | Fix |
|---|---|---|---|---|
| Q-01 | **P0** | Size silently pre-selected | Ring PDP (`/shop/elowen-round-halo-engagement-ring`) has **US 4** pressed by default. The bracelet PDP defaults to **6 Inch**, and Add To Bag adds it without the visitor choosing | No default size/length; Add To Bag disabled (or an inline error "Select your ring size") until one is chosen |
| Q-03 | **P1** | Cookie banner over dialogs | On 29 Oct the cookie banner covered the love-letter dialog; on 30 Oct (desktop) the dialog (z-index 3100) sat above the banner (z-index 2000). Recheck at 375 px | Dialogs above the banner, or show the banner first and block other modals until it is answered |
| Q-04 | **P1** | Cart flashes "(0 items)" | Seen on 29 Oct, not reproduced on desktop on 30 Oct | Render a skeleton until the cart state is hydrated; verify on slow mobile |
| Q-07 | **P1** | Login host | Customer login **and** the admin login redirect to **`auth-uat.houseofdiams.com`** | Use a production auth host (e.g. `auth.houseofdiams.com`); `noindex` it |
| Q-08 | **P2** | Clear bag has no confirmation | One click empties the bag | Optional confirm or "Undo" toast |
| Q-09 | **P1** | Contact page shows no contact details | `/contact` shows no email/phone/address on the page itself | Render the CMS Contact Info cards (email, phone & WhatsApp, Surat atelier) on `/contact`, and a click-to-load map of the Surat address (so it doesn't hurt LCP). Footer, `/contact` and schema must show the same details (Part B) |

**Regression checks before delivery (desktop + 375 px mobile):**
- Every header/mega-menu/footer link returns 200 and lands on a page with products.
- Search suggestions + Enter.
- PDP flow: option selection (metal, size/length, engraving) → Add To Bag → drawer → View Cart → quantity/remove/clear → Checkout opens (stop there).
- Wishlist logged out (should prompt login) and logged in.
- Contact and bespoke forms show validation on empty submit.
- WhatsApp, mailto and tel links.
- Cookie Reject/Accept/Customize persist across pages.
- An unknown URL returns HTTP 404 with `noindex`.
- A CMS edit (e.g. a policy text) shows on the live page within minutes.

### C8. GA4 / GTM / consent

Observed before the visitor makes a cookie choice (30 Oct; build unchanged on 31 Oct):
- `window.dataLayer` is empty and GTM is not loaded, so no consent default is sent.
- The site code contains a hard-coded GA4 path (`NEXT_PUBLIC_GA_MEASUREMENT_ID || "G-0LVQJ1YDJ0"` with `gtag(... 'config' ...)` and `send_page_view`) next to GTM.
- No GA4 ecommerce event names (`view_item`, `view_item_list`, `begin_checkout`, `purchase`, …) are in the main JS bundles.
- GA4 (29 Oct): `purchase` has no data and the funnel events are missing.

| ID | Pri | Fix |
|---|---|---|
| G-01 | **P0** | **Consent Mode v2 (advanced):** load GTM on every page. Before it, push `gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',wait_for_update:500})`. On the visitor's choice push `gtag('consent','update',{…})` (the update code exists) — never a second `default`. Re-apply the stored choice on each page load |
| G-02 | **P0** | **One GA4 path only:** remove the hard-coded `gtag('config','G-0LVQJ1YDJ0')` page-view component and fire GA4 only from GTM (or remove GA4 from GTM, not both). Send exactly one `page_view` per App Router navigation. Verify in GTM Preview + GA4 DebugView |
| G-03 | **P0** | **GA4 ecommerce dataLayer** (standard `items[]`: `item_id` = SKU, `item_name`, `item_category`, `item_variant` = metal, `price`, `quantity`, `currency:'USD'`): `view_item_list`, `select_item`, `view_item`, `add_to_cart`, `remove_from_cart`, `view_cart`, `add_to_wishlist`, `begin_checkout`, `add_shipping_info`, `add_payment_info`, `purchase` (order-confirmation page, once per `transaction_id`, with `value`, `tax`, `shipping`, `coupon`) |
| G-04 | **P1** | Lead events: `generate_lead` on successful contact/bespoke submit (with `form_name`), `sign_up`/`login`, `view_search_results` with `search_term` |
| G-06 | **P1** | The CSP is `report-only` and already allows GTM/GA/Clarity/Pinterest; keep it in sync with any new tag before enforcing |

**Already correct (don't redo):**
- The 10 blog packages (title, meta, H1, canonical, links, blog index).
- `by-desgin` → `by-design` 301s; all 52 previously missing internal links.
- FAQPage only on `/faq`; Organization author on all articles; BreadcrumbList on 245/246 pages.
- Empty listings `noindex` + out of the sitemap and `llms.txt`; test article/product removed from listings.
- Organization `founder`, `email` and `sameAs` in schema.
- `media.*` and `/_next/image` cached at CloudFront.
- Product-page shipping/returns/warranty text, the coupon name, About page content, the top bar and the hero link are correct and managed in the CMS. Leave them to the CMS.

---

## PART D — Acceptance checks (run all against production; paste the output into the delivery report)

```bash
# 0. Proof of deploy: the build must differ from the 29–31 Oct build (chunk 066_9qs-fr7km.js must be gone)
curl -s https://houseofdiams.com/ | grep -c '066_9qs-fr7km.js'
# 1. Host + redirects (expect one 301 each, straight to https://houseofdiams.com/...)
for u in http://www.houseofdiams.com/ "https://www.houseofdiams.com/shop?page=2" http://houseofdiams.com/fine-jewellery; do curl -sI "$u" | grep -iE '^HTTP|^location'; done
# 2. Static assets cached (second call must say Hit)
u=https://houseofdiams.com$(curl -s https://houseofdiams.com/ | grep -oE '/_next/static/chunks/[^"]+\.js' | head -1); curl -sI $u >/dev/null; curl -sI $u | grep -i x-cache
# 3. Burst test: 0 non-200
curl -s https://houseofdiams.com/ | grep -oE '/_next/static/[^"]+\.(js|css)' | sort -u | sed 's#^#https://houseofdiams.com#' | xargs -P 50 -n 1 curl -s -o /dev/null -w '%{http_code}\n' | sort | uniq -c
# 4. Forbidden code-side text sitewide (expect no output)
curl -s https://houseofdiams.com/sitemap.xml | grep -oE 'https://[^<]+' | xargs -P 6 -n 1 curl -s | grep -oiE 'New York|44th Street|pin\.it|igsh=|www\.houseofdiams|1 items' | sort | uniq -c
# 5. Old test product gone
curl -sI https://houseofdiams.com/shop/produt-1 | head -1
# 6. Lighthouse (mobile + desktop) on: / /shop /engagement-rings /fine-jewellery/bracelet/tennis-bracelet /shop/rosette-five-flower-bracelet /blog /bespoke
npx lighthouse@13.6.0 https://houseofdiams.com/ --only-categories=performance,accessibility,best-practices,seo,agentic-browsing --output=json --output-path=./lh-home-mobile.json
```

Also run:
- Google Rich Results Test on 3 PDPs (0 warnings).
- GTM Preview + GA4 DebugView walk-through: list → item → add_to_cart → view_cart → begin_checkout, one `page_view` per navigation, consent default denied before the choice.
- PageSpeed Insights mobile + desktop on the same 7 URLs.

**Targets at delivery:**
- Ahrefs apex project: 100 % health, with no "links to redirect", "OG incomplete" or "ItemList missing" warnings; the `www` project has nothing left to crawl except 301s.
- Lighthouse: Accessibility / Best Practices / SEO = 100 and Agentic Browsing 3/3 on every template; Performance ≥ 90 mobile / ≥ 95 desktop on key templates.
- GSC: Merchant listings without warnings.
- GA4: full ecommerce funnel + leads, one `page_view` per navigation, Consent Mode v2 active.
