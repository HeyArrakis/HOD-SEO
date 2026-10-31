# 05 — Final Pre-Delivery Master Fix List (remaining items only — re-verified 2026-10-31, after the developer's last release)

**Status:** the developer's contract has ended. His last release went live on 2026-10-31. This file now lists **only what is still open on the live site**, for the owner to finish (with Claude Code for code items, and in the admin for CMS items).
**Checked:** 2026-10-31 from scratch: all 246 sitemap URLs, a sitewide text/schema scan, Lighthouse 13.6 on 11 templates × mobile/desktop, and browser tests. Evidence: `Technical/2026-10-31-live-validation/` and `Technical/2026-10-31-cms-changes/`.
**CMS work done on 31 Oct (afternoon), removed from Part D.** Before/after for every change is in `Technical/2026-10-31-cms-changes/README.md` (changes 13–33):
- Menu: "T-Bar" label fixed and Bespoke shown.
- Option labels: Toi et Moi, Multi-Stone, Solid, Pavé.
- "40+ countries" removed; "half a century" replaced; Fine Jewelry banner text fixed.
- CMS-typed titles and buttons in capitals.
- FAQ: test item hidden; US spelling.
- 67 product SEO titles shortened; 8 placeholder or duplicate metas and 2 duplicate H1s fixed.
- 5 approved article SEO titles applied.
**Site:** https://houseofdiams.com (canonical host = apex).

**Fixed by the developer and verified on 31 Oct (removed from the list):**
- `www` → apex 301.
- CloudFront now caches `/_next/static` (Hit on repeat).
- `<lastmod>` on all 246 sitemap URLs.
- New York address removed from schema and the contact panel; full Surat address in the Organization schema.
- Footer social links (Pinterest, Instagram, Facebook) correct.
- `og:image` on every page.
- `/promo-codes-and-offers` is `noindex, follow`.
- `/contact` shows email, phone and the Surat address.
- Ring size is no longer pre-selected ("Please select your ring size").
- Cart says "1 item" and "Shape: Round".
- Currency-flag accessibility error fixed: Accessibility is 96–100 everywhere and Agentic Browsing is 3/3 on every template except the product page.

---

## PART A — BEFORE YOU START + PROMPT FOR CLAUDE CODE

**Get these from the developer first (needed for every code item):**
1. The **latest code**: GitHub repos `dhruval12098/HOD` (storefront) and `dhruval12098/admin-hod` (admin), with ownership or admin access transferred to you. The copy on this Mac (`~/Desktop/HOD/`) is from **4 Sep 2026**, before the AWS move, so don't work from it.
2. **AWS access**: CloudFront distribution, the server/hosting that runs Next.js, the media bucket(s) behind `media.` / `content.houseofdiams.com`, and the **deploy steps** (how a change goes live).
3. **Keycloak** admin for `auth-uat.houseofdiams.com`, plus **GTM** (`GTM-TJ5HTTSD`) and **GA4** admin.

**Prompt (copy from here to the end of Part C into Claude Code, opened in the latest storefront code):**

You are working in the House of Diams storefront: Next.js App Router behind nginx + CloudFront on AWS, content from the admin CMS (`manage.houseofdiams.com`). Implement every item in Part C in priority order, deploy to production, then run the checks in Part E.

**Rules:**
1. Customer-facing copy may only state the facts in Part B. Don't invent business facts.
2. Don't touch payment/checkout logic (Razorpay, order creation, pricing, tax calculation).
3. Don't change URL slugs. Anything that stops returning 200 gets a 1:1 301.
4. No test content on production.
5. American English in visible copy ("jewelry"); keep the `/fine-jewellery/` URLs.
6. Text the CMS manages stays in the CMS. Don't hard-code it.
7. FAQPage schema only on `/faq`. No fake reviews, ratings, GTINs or awards.
8. One commit per item ID, small changes, and run each item's **Done when** check against production.

---

## PART B — Confirmed HOD facts (the only claims allowed)

| Topic | Approved wording basis |
|---|---|
| Shipping | Free shipping to every country; every order insured; same-day overnight shipping; no order cut-off time |
| Returns | Within **15 days** of delivery, unworn; refund once the piece reaches HOD; return shipping and duties paid by the customer. Bespoke/custom pieces not returnable unless the piece doesn't match the agreed design |
| Certification | IGI and GIA certificates |
| Services | Free resizing; free annual cleaning; free lifetime warranty (no terms published) |
| Bespoke timing | Typically 2–3 weeks to make + about 6–9 days delivery; about 3–4 weeks from design approval; depends on the selected stone; estimates, not guarantees |
| Company | Founders Krish Babariya and Akshar Korat; in the trade since 2014; public email admin@houseofdiams.com |
| Address | House of Diams, 831, Pragati IT World, Yogi Chowk, Surat, Gujarat 395010, India · +91 93285 36178 · by appointment only |

**Not allowed:** New York address, "UPS", "40+ countries", "20+ countries", "Conflict Free", "Ethically", "2–3 business days".

---

## PART C — CODE FIXES STILL OPEN (2026-10-31)

Priority: **P0** = fix first (trust, tracking, sales) · **P1** = needed for the targets · **P2** = polish.

### C1. Ahrefs (status)

Both root causes of the 69 % `www` project are fixed: `www` now 301s, and CloudFront caches JS. One part of the deploy problem remains: **files from the previous build return 404 after a release** (T-03), and crawlers that still hold the old HTML then see broken JavaScript. After T-03, re-crawl the apex project in Ahrefs and archive the `www` project.

### C2. Technical SEO

| ID | Pri | Item | Current (2026-10-31) | Fix | Done when |
|---|---|---|---|---|---|
| T-03 | **P0** | Keep old JS chunks after a release | Chunks of the 30 Oct build (e.g. `1lztb9ya7g43q.js`, `1nwrofmes_805.js`, `1wl6s8jwyyu-s.js`) now return **404**. Unknown chunks correctly return 404, not 500 | Keep the previous build's `/_next/static` files for ≥ 7 days after each release (upload new files, don't delete old ones) | After the next release, a chunk from the release before still returns 200 |
| T-04 | **P1** | HTML caching / TTFB | Every HTML page is `private, no-cache, no-store`, sets `detected_country`/`detected_currency` cookies, and misses CloudFront. TTFB ≈ 0.9 s. Lighthouse `bf-cache` fails on all 22 runs | Public pages (home, categories, PDPs, blog, education, policy pages) use ISR/`revalidate` + `Cache-Control: public, s-maxage=300, stale-while-revalidate=86400`, revalidated on CMS save. Country/currency detection at the edge (`CloudFront-Viewer-Country`) or client side, so public HTML doesn't `Set-Cookie`. `no-store` only on cart/checkout/account/API | TTFB < 200 ms on a CloudFront hit; `bf-cache` passes on content pages |
| T-05 | **P1** | Test-product leftover | `/shop/produt-1` still **301s to `/engagement-rings`** | Return 404/410. Add a publish guard: items with "test"/"qa"/"uat" in the name/slug, or drafts, never reach the sitemap, listings, search, related items or `llms.txt` | `curl -sI https://houseofdiams.com/shop/produt-1` → 404/410 |
| T-09 | **P1** | Menu links to empty pages | The mega-menu still links to **10** empty `noindex` listings: `/wedding-bands/for-him/classic`, `/diamonds`, `/designer`; `/wedding-bands/for-her/nature`, `/solid`, `/cigar-band`, `/pavee`; `/fine-jewellery/necklaces/initials`, `/tennis-necklace`; `/fine-jewellery/rings/eternity-rings` | Hide a menu item automatically while its category/option has 0 published products | No menu/footer link points to a page with 0 products |
| T-10 | **P1** | Pagination | `/blog?page=2` canonicalizes to `/blog` and its title has no page number. `/engagement-rings/by-design?page=2` is self-canonical, while its page 1 canonicalizes to `/engagement-rings` | `/blog?page=N`: self-canonical + title "Blog – Page N". `/engagement-rings/by-design?page=N`: canonical → `/engagement-rings?page=N` | Each `?page=N` has a unique title and a consistent canonical |
| T-14 | **P1** | Search results page | `/search?q=ring` → **404**; Enter in the search box does nothing | Add `/search?q=` (`noindex,follow`, not in the sitemap); Enter submits to it | Enter opens results |
| T-01 | **P2** | `http://www` takes 2 hops | `http://www.houseofdiams.com/about` → `https://www…/about` → `https://houseofdiams.com/about` | Let the CloudFront Function also handle `http://www` (viewer protocol "HTTP and HTTPS" for that host, or a function on both) | One 301 straight to `https://houseofdiams.com/about` |
| T-08 | **P2** | Absolute internal links | `href="https://houseofdiams.com"` (logo/home) and `href="https://houseofdiams.com/engagement-rings"` (hero button; the CMS value is `/engagement-rings`) | Render internal links as relative paths | `curl -s https://houseofdiams.com/ \| grep -c 'href="https://houseofdiams.com'` = 0 |
| T-12 | **P2** | Media host root | `https://media.houseofdiams.com/` → **403** | Return 404 at the bucket root; `X-Robots-Tag: noindex` on non-image responses | Root returns 404 |
| T-13 | **P2** | IndexNow (optional) | Ahrefs notice "Changed pages not submitted to IndexNow" | Optional ping to Bing/Yandex on publish; Google doesn't use it | — |

### C3. Typography — titles and buttons in capitals (new, owner's design rule)

**The rule** (matches what is already right on the homepage hero and "SHOP BY CATEGORY"):
- **Titles** (page titles and section headings) use **Montserrat, weight 600, CAPITALS**. Use CSS `text-transform: uppercase`, so the text stays normal-case in the HTML.
- **Subtext** under a title stays normal: Inter, sentence case. Example: "Discover engagement rings, crafted for your love story".
- **Every CTA button** uses **Montserrat, CAPITALS**.
- **Keep normal case:**
  - product names (product cards and the product-page H1, e.g. "Rosette Five-Flower Bracelet");
  - blog post titles and the headings inside an article;
  - FAQ questions;
  - option selectors (metal, size, length) and form labels;
  - email, phone, address and copyright text.

| ID | Pri | Where | Still not in capitals on 31 Oct (code-rendered) | Fix |
|---|---|---|---|---|
| TY-01 | **P1** | Section titles in code | Product page: "Know Your Setting", "Product FAQs", the "Description" / "Details" tabs. Cart: "Order Summary" and the "Why house of diams" heading style. `/about`: H1 "About House of Diams" and the founder-name headings (left normal-case in the CMS because the names also feed the schema). `/contact`: H1 "Contact House of Diams" (hard-coded; the CMS Contact hero is not used). Homepage: the four blog tiles ("Lab-Grown Diamond", "Buyers Guide", "The Perfect Pick", "CVD vs HPHT"; their text is each article's card title, so style them on the homepage only) | Give the shared section-title component (or a `.section-title` class) `font-family: var(--font-family-primary); font-weight: 600; text-transform: uppercase;` and use it for every page/section title. CMS-managed titles get the same class, so new CMS text is capitalized automatically |
| TY-02 | **P1** | CTA buttons | "Add To Bag", "Buy Now", "View bag", "Load more (87) products" (listings), "Submit Enquiry" (`/bespoke`), "Apply Free gift offer" (product page coupon button), cart "ADD TO CART" / "Add To Bag" mix | One button style for all CTAs: Montserrat, uppercase, same letter-spacing as "SHOP ENGAGEMENT RINGS". Use one wording everywhere: "ADD TO BAG". US spelling: "SUBMIT INQUIRY" |
| TY-03 | **P1** | Footer | Links are Inter, normal case: Home, Explore Collection, About Us, Bespoke, Blog, Education, Contact, Engagement Rings, Wedding Bands, Fine Jewelry, T-Bar, FAQ, Shipping, Returns, Terms & Conditions, Privacy Policy, Cookie Settings, "United States (USD)" | `footer.site-footer a, footer.site-footer button { font-family: var(--font-family-primary); text-transform: uppercase; }`. Leave the contact details (email, phone, address, appointment note) and the copyright line as they are |
| TY-04 | **P1** | Exclusive-offer band above the footer | "Get a Free Gift" heading (also on `/contact` and `/shipping`) | Apply the TY-01 title style. The text comes from CMS Home → Offer Section |

**Done when:** on `/`, `/fine-jewellery`, a category, a product page, `/cart`, `/bespoke`, `/about`, `/contact`, `/blog` and `/faq`, every section title, CTA and footer link renders in Montserrat capitals, and product names, article headings and FAQ questions are still normal case.

### C4. On-page (code side)

| ID | Pri | Item | Current (2026-10-31) | Fix | Done when |
|---|---|---|---|---|---|
| O-03 | **P0** | Delivery-time line in cart/checkout | The cart shows "**Approximately 3 to 4 weeks**" for an in-stock bracelet, next to "Same-day overnight dispatch" | Add a per-product "Made to order" flag in the product editor (default off). Show the 3–4-week estimate only for made-to-order/bespoke items | An item without the flag shows no "3 to 4 weeks" line |
| O-14 | **P1** | Bangles page metadata | `/fine-jewellery/bracelet/bangles` still "Bangles \| Fine Jewelry", H1 "Explore Bangles", meta "Browse Bangles in Fine Jewelry." | Apply it like the other option pages: title "Diamond Link Bracelets", meta "Shop House of Diams diamond link bracelets in open-link designs set with pavé diamonds." If option pages have no SEO fields in the CMS, add SEO title / H1 / meta / intro fields to the option editor | Title, H1 and meta match |
| O-15 | **P2** | Blog and Education in the menu | The Navbar Builder only offers items tied to a category | Allow plain link items (label + URL) in the Navbar Builder | Owner can add "Blog" and "Education" |
| O-16 | **P2** | Menu featured image alt | The Fine Jewelry mega-menu image has `alt="Fine Jewellery"` on every page. The Navbar Builder has no alt field, and re-saving does not refresh it | Take the alt from the category name ("Fine Jewelry") or add an alt field to the Navbar Builder featured image | `alt="Fine Jewelry"` |
| O-08 | **P2** | One H1 with several hero slides | Today one slide, one H1. Slide headings are rendered as `<h1>`, so a second slide adds a second H1 | Fixed page `<h1>`; other slide headings as `<h2>`/`<p>` | One `<h1>` with 2+ slides |

### C5. Structured data

| ID | Pri | Item | Current | Fix | Done when |
|---|---|---|---|---|---|
| S-01 | **P0** | Merchant listing fields | No `shippingDetails` and no `hasMerchantReturnPolicy` on any of the 182 PDPs | In every `Offer`: `shippingDetails` (`shippingRate` 0 USD, `shippingDestination` all countries; no `deliveryTime`) and `hasMerchantReturnPolicy` (FiniteReturnWindow, 15 days, ReturnByMail, ReturnShippingFees, `applicableCountry`). Or define the policy once on the Organization and reference it | Rich Results Test: 0 warnings on 3 PDPs |
| S-04 | **P1** | Category ItemList | No `ItemList` on `/`, `/shop`, `/engagement-rings`, `/fine-jewellery` | `ItemList` of the products shown (url + position) | Ahrefs issue = 0 |
| S-06 | **P2** | WebSite schema | Not present | `WebSite` (`name`, `url`) on the homepage | — |
| S-05 | **P2** | Homepage BreadcrumbList | Missing only on `/` | Optional single-item list | — |

### C6. Performance

**Lighthouse 13.6, 31 Oct** (simulated mobile throttling; single runs vary by a few points):

| Template | Mobile Perf | Mobile LCP | Desktop Perf | A11y | Agentic |
|---|---|---|---|---|---|
| Home | 67 | 6.3 s | 74 | 96 | 3/3 |
| /shop · /engagement-rings | 71 · 70 | 5.9 · 6.7 s | 76 · 78 | 100 | 3/3 |
| Category (tennis bracelet) | 72 | 6.2 s | 79 | 100 | 3/3 |
| PDP (bracelet) | 75 | 5.2 s | 77 | 96–97 | **2/3** |
| /blog · article | 73 · 91 | 5.7 · 2.6 s | 77 · 85 | 100 | 3/3 |
| /bespoke · /about · /contact · /faq | 66 · 77 · 93 · 83 | 5.1 · 4.5 · 2.4 · 2.5 s | 80 · 80 · 86 · 85 | 100 | 3/3 |

Best Practices 100 and SEO 100 on all 22 runs.

| ID | Pri | Item | Evidence (31 Oct) | Fix |
|---|---|---|---|---|
| P-01 | **P0** | LCP image found late | `lcp-discovery` fails on /shop, /engagement-rings, categories, PDP, /blog, /bespoke, /about | First hero/banner image and the first 2 (mobile) / 4 (desktop) product images: `priority` / `fetchpriority="high"`, no `loading="lazy"`; preload only the first slide |
| P-02 | **P0** | Product videos | The bracelet PDP references 26 MP4s of **≈ 26 MB each** (files named "-compressed" are still 26 MB); `<video autoPlay preload="none">` | Poster image first; load video only on interaction or when idle and in view; transcode to ≤ 1.5 MB 720p H.264/WebM (re-encode the existing files); no autoplay on mobile/save-data |
| P-03 | **P1** | Oversized images | "Improve image delivery" savings on PDP and listings | `next/image` with correct `sizes`; thumbnails ≤ 15 KB; AVIF/WebP, quality 70–75 |
| P-04 | **P1** | Render delay | Text LCP waits for client JS (fade-in) on article/FAQ/contact | Render above-the-fold text server-side without opacity animation |
| P-05 | **P1** | CSS / JS weight | Render-blocking CSS, legacy polyfills, unused JS on every template | Inline critical CSS; modern `browserslist`; code-split filters/quiz/reels/cookie modal; GTM `afterInteractive` |
| P-06 | **P1** | Third-party flag file | The `us.svg` flag still loads from `cdn.jsdelivr.net` (preloaded on every page) | Inline/self-host the one flag SVG; drop the preload |
| P-07 | **P1** | Fonts | Inter variable font ≈ 109 KB | Subset to Latin, `font-display: swap`, preload only the above-the-fold weight |

### C7. Accessibility + Agentic Browsing

| ID | Pri | Item | Evidence (31 Oct) | Fix |
|---|---|---|---|---|
| A-07 | **P0** | `label-content-name-mismatch`: keeps the **PDP at Agentic 2/3** | PDP metal buttons have `aria-label`s that don't match their visible text (e.g. visible "10K / Yellow Gold"); `/blog` "Filter articles by category" and "Sort articles" buttons | Make each `aria-label` start with the visible text, or remove the `aria-label` |
| A-06 | **P1** | `target-size` on PDP | Gift-offer "Apply …" button has a small hit area | ≥ 24×24 px hit area |
| A-02 | **P1** | `color-contrast` on home (mobile) | The top-bar announcement link (`/shipping`) | Raise contrast to ≥ 4.5:1 |

### C8. Frontend QA

| ID | Pri | Bug | Evidence (31 Oct) | Fix |
|---|---|---|---|---|
| Q-01 | **P0** | Bracelet length silently pre-selected | Bracelet PDP: "6 Inch" is pre-selected and Add To Bag adds it without a choice (cart shows "Bracelet Length: 6 Inch"). Ring size is fixed | Same as rings: no default length; "Please select your bracelet length" until chosen |
| Q-07 | **P1** | Login host | Customer and admin login go to **`auth-uat.houseofdiams.com`** | Production auth host (e.g. `auth.houseofdiams.com`), `noindex` |
| Q-03 | **P2** | Cookie banner vs dialogs | Seen on 29 Oct (banner covering the love-letter dialog); recheck at 375 px | Dialogs above the banner, or banner first |
| Q-08 | **P2** | Clear bag has no confirmation | One click empties the bag | Confirm or "Undo" toast |

### C9. GA4 / GTM / consent

Observed on 31 Oct:
- Before the cookie choice, and after "Reject non-essential", GTM is not loaded and `dataLayer` is empty, so no Consent Mode signal is sent.
- The hard-coded GA4 path (`NEXT_PUBLIC_GA_MEASUREMENT_ID || "G-0LVQJ1YDJ0"`, `send_page_view`) is still in the bundle.
- No ecommerce event names (`view_item`, `add_to_cart`, `begin_checkout`, `purchase`, …) exist in the home, PDP, cart or checkout bundles.

| ID | Pri | Fix |
|---|---|---|
| G-01 | **P0** | Consent Mode v2 (advanced): load GTM on every page; before it push `gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',wait_for_update:500})`; on the visitor's choice push `gtag('consent','update',…)`; re-apply the stored choice on each load |
| G-02 | **P0** | One GA4 path only: remove the hard-coded `gtag('config','G-0LVQJ1YDJ0')` component and fire GA4 from GTM; exactly one `page_view` per App Router navigation |
| G-03 | **P0** | GA4 ecommerce `dataLayer` (`items[]` with `item_id` = SKU, `item_name`, `item_category`, `item_variant` = metal, `price`, `quantity`, `currency:'USD'`): `view_item_list`, `select_item`, `view_item`, `add_to_cart`, `remove_from_cart`, `view_cart`, `add_to_wishlist`, `begin_checkout`, `add_shipping_info`, `add_payment_info`, `purchase` (once per `transaction_id`, with `value`, `tax`, `shipping`, `coupon`) |
| G-04 | **P1** | `generate_lead` on contact/bespoke submit (`form_name`), `sign_up`/`login`, `view_search_results` (`search_term`) |
| G-06 | **P1** | Keep the report-only CSP in sync with any new tag before enforcing it |

---

## PART D — CMS ITEMS (admin `manage.houseofdiams.com`, no code needed)

CMS-01 to CMS-08 and most of CMS-10 were done or closed on 31 Oct (see the status note at the top). Still open:

| ID | CMS place | Change |
|---|---|---|
| CMS-09 | Catalog → Categories → each main category (intro text / buying guide) | Add a short unique intro and buying guide on `/engagement-rings`, `/wedding-bands`, `/fine-jewellery` and its earrings, rings, necklaces and bracelet pages. Use the content plan in `On-page SEO/04` §6 (what is here, how to choose, 1–2 Education links, bespoke link) and only Part B facts |
| CMS-10 | Blog → "14K vs 18K Gold for Diamond Jewellery" → SEO title | Change to "14K vs 18K Gold (and 10K) for Diamond Jewelry" only after the Search Console baseline for that page is saved (Step 2 status GSC BASELINE REQUIRED). All other long article titles are either approved packages or kept as they are by the spec |

---

## PART E — Checks after each release (run against production)

```bash
# 1. www and http (expect one 301 each, straight to https://houseofdiams.com/...)
for u in http://www.houseofdiams.com/about "https://www.houseofdiams.com/shop?page=2" http://houseofdiams.com/fine-jewellery; do curl -sI "$u" | grep -iE '^HTTP|^location'; done
# 2. Old chunks survive a release (run the day after a release with a chunk name from the day before; expect 200)
curl -s -o /dev/null -w '%{http_code}\n' https://houseofdiams.com/_next/static/chunks/<old-chunk>.js
# 3. Static assets cached (second call must say Hit)
u=https://houseofdiams.com$(curl -s https://houseofdiams.com/ | grep -oE '/_next/static/chunks/[^"]+\.js' | head -1); curl -sI $u >/dev/null; curl -sI $u | grep -i x-cache
# 4. Old test product gone, search page exists
curl -sI https://houseofdiams.com/shop/produt-1 | head -1; curl -s -o /dev/null -w '%{http_code}\n' "https://houseofdiams.com/search?q=ring"
# 5. Forbidden text sitewide (expect no output)
curl -s https://houseofdiams.com/sitemap.xml | grep -oE 'https://[^<]+' | xargs -P 6 -n 1 curl -s | grep -oE 'New York|44th Street|40\+ countries|20\+ countries|30 days|craftsmanship warranty|T- BAR|Fine Jewellery|Quetsion QA|half a century' | sort | uniq -c
# 6. Lighthouse (mobile + desktop): / /shop /engagement-rings /fine-jewellery/bracelet/tennis-bracelet /shop/rosette-five-flower-bracelet /blog /bespoke
npx lighthouse@13.6.0 https://houseofdiams.com/ --only-categories=performance,accessibility,best-practices,seo,agentic-browsing --output=json --output-path=./lh-home-mobile.json
```

Also:
- Rich Results Test on 3 PDPs.
- GTM Preview + GA4 DebugView walk-through (list → item → add_to_cart → view_cart → begin_checkout; consent default denied before the choice).
- A new Ahrefs crawl of the apex project.

**Targets:**
- Lighthouse Accessibility / Best Practices / SEO = 100 and Agentic 3/3 on every template; Performance ≥ 90 mobile / ≥ 95 desktop on key templates. The ranking signal is field Core Web Vitals: LCP < 2.5 s, INP < 200 ms, CLS < 0.1.
- Ahrefs apex 100 %.
- GSC Merchant listings without warnings.
- GA4 full ecommerce funnel with Consent Mode v2.
