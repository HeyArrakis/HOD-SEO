# changes.md — every fix from the final audit (1 November 2026)

**For:** the House of Diams developer (Parts A–D), the admin/CMS editor (Part E) and the owner (Parts F–G).
**Supersedes:** `DEVELOPER-HANDOFF/05-FINAL-PRE-DELIVERY-MASTER-FIX-LIST-2026-10-29.md`. Every open item from 05 is merged here; the 05 IDs are shown in brackets.
**Evidence:** `FINAL-AUDIT-2026-11-01/report.md` and `Technical/2026-11-01-live-validation/`.
**Repos:**
- Storefront: `House-of-diams/aws-houseofdiams-storefront` (audited at `main` `210235e`; `main` is now `5a00843`). Merging to `main` deploys production.
- Admin: `House-of-diams/House-of-diams-admin-` (audited at `main` `3ac13cd`; `main` is now `05716eb`).

**Priority:** **P0** = do now (tracking, trust, errors) · **P1** = next (rankings, speed) · **P2** = later (polish).

**Rules (unchanged):**
- Customer-facing text may only state the facts in Part F's fact box.
- Don't change URL slugs without a 1:1 301.
- Payment, pricing and tax logic stays untouched.
- US English.
- Text the CMS manages stays in the CMS.
- One commit per ID. Run typecheck, lint and tests, and the "Done when" check on production.

---

## Branch `sonder-hod-seo` — merged and live 2 Nov 2026 (storefront `2c8071f`, admin `3666e0e`)

Claude implemented the code items below on a branch called `sonder-hod-seo` in each repo, on top of the latest `main` (storefront `5a00843`, admin `05716eb`). Both branches are on GitHub: storefront head `c9281e0` (15 commits plus a merge of `main`), admin head `43e55f5` (9 commits plus a merge of `main`). Both were merged on 2 Nov at the owner's request and both deploys succeeded; live results are under "Live check, 2 Nov" below. Tick an item in the checklist only after its "Done when" check passes on production.

**Who answers for these changes:** the handover (2 Nov) says changes pushed by House of Diams or another team are tested and, if needed, reverted by that team. The agency's free bug-fix period (2–16 Nov) covers its own delivered features, not these.

**Checks run on the final commits (local, Node 24.22.0, the same steps as `.github/workflows/ci.yml`):**
- Storefront: typecheck 0 errors; lint 0 errors (149 warnings, same as `main`); tests 394/394; production build OK.
- Storefront, local production build in a browser:
  - 5 × 410 and 6 × 301 as listed under A-03 (the 301 targets return 200 on the live site); no `X-Powered-By`.
  - `/shipping` shows 10–14 + 6–8 days; `/returns` shows the 15 % fee; "within 12 hours" shows.
  - After load and a scroll to the footer: 0 route prefetches (`?_rsc`), no empty product search, only the 3 used fonts. Hovering a footer link prefetches only that page; hovering the search button loads the suggestions.
- Storefront, real `ProductGallery` with a real video in a test page: on desktop the video in view plays, and an off-screen one doesn't load until scrolled to. On a phone a tap plays one video. No console errors.
- Admin: tests 959/959 (784 core + 175 render); typecheck 0 errors; `test-admin-release-cleanup.py` OK; lint 0 errors (110 warnings, same as `main`); format OK; `migrations:check` OK; production build OK; browser suite 120/120 scenarios (2 new ones cover B-06: no write is sent, the error shows next to the field, and it clears when the field is filled).
- Both: no changes under `db/` or `.github/`, no env, package or lock files; secret scan of both diffs found 0 matches.
- **Claude's code review of both pull requests (2 Nov; the owner wants Claude, not Copilot, to review everything):** 20 findings. The bugs found are fixed in new commits, with tests:
  - Admin: a new catalog record was treated as the homepage in the SEO title meter; the meter now measures the title the website will really use; a replaced menu image keeps no old alt text; the retired B2B row is hidden in SEO settings.
  - Storefront: every article now gets a link from at least one other (simulated on the 20 live titles: 5 unlinked before, 0 after, but 12 still have fewer than 3 from related posts alone); `llms.txt` wording is back within the fact box; dead code removed; new claims recorded in `seo/client-dependencies.md`.
  - Left open on purpose: A-07 covers only the category chips (a fresh crawl will show if a grid or the homepage promo still links to an empty listing); the server rejects only an explicit empty meta description (a missing value keeps the stored one, so an already-empty stored description is caught only in the editors); the `ready_to_ship` field still exists in both repos; two unused fonts stay in the code with `preload: false`.
- **First automatic Claude reviews (2 Nov), each finding checked by Claude in the session; no code change needed:**
  - Reworded claims: all match the owner's answers in `confirmed_business_facts.md` (rows 2, 4, 11, 14, 16).
  - `restockingFee: 15`: schema.org and Google say a Number is a percentage; neither says 15 or 0.15. Kept. Google lists this field for organization-level policies, not product-level ones, so it may ignore it on products.
  - `returnFees: ReturnFeesCustomerResponsibility`: correct per Google for a customer who arranges and pays for return shipping.
  - 12 countries: Google allows at most 50 in `applicableCountry`, so the old 249 had to shrink. Merchant Center's shipping settings cover the rest.
  - Meta rule browser-only: fixed in `43e55f5`. The save route now answers 400 for an explicit empty description on a published article.
  - **Owner's answer, 2 Nov:** the two product 301s in A-03 point to the same pieces, so both stay as they are.
  - **Owner's answer, 2 Nov:** appraisals are not offered. `c9281e0` changes "Certificate & Appraisal" to "Diamond Certificate" on the home strip and the product trust icon. The icon file was renamed so a cached copy can't keep showing the claim.
- **New York office, 2 Nov:** storefront PR #25 merged and live as `3102c0a`; CMS card `Office · USA` added after Surat (log: `Technical/2026-11-02-cms-changes/README.md`). Checked live: footer, schema, `llms.txt`; the `/contact` map still shows Surat.
- **Live check, 2 Nov, after the merge (evidence `Technical/2026-11-02-live-validation/`):**
  - **Passed:** A-01 and A-17 (scan of all 246 pages finds no withdrawn claim; the one "appraisal" is an educational line in an article); A-02 (182 of 182 products: one `material`, `itemCondition`, `deliveryTime`, `restockingFee`; largest product JSON-LD 3.4 KB); A-03 (6 × 301 to pages that return 200, 5 × 410); A-08 (`llms.txt` 7 KB); A-09 and A-10 (Accessibility 100 on all 28 Lighthouse runs); A-14 (`/b2b` 410); A-16 (entity fields present); `X-Powered-By` absent. Titles, metas, H1s and canonicals: no changes against 1 Nov.
  - **Browser:** product page, cart, checkout up to the shipping step, search and contact page work, with no console errors except the report-only CSP line below. Test item removed from the bag. No payment, no form sent, no sign-in, no admin save.
  - **A-06:** product page weight fell (bracelet desktop 17.6 → 2.4 MB, earrings mobile 14.8 → 1.6 MB). Earrings desktop is 5.5 MB, still over the 3 MB target until the MP4s are transcoded.
  - **A-13:** 19 of 21 articles have at least 3 links; `/blog/10-year-anniversary-gift-ideas-tin-and-diamond` and `/blog/push-present-what-it-is-and-jewelry-ideas` have 2.
  - **A-05 speed not proven:** requests fell (for example `/contact` mobile 103 → 83), but Lighthouse scores fell too (`/contact` mobile 89 → 56) with server latency 1–5 s against 0.3 s on 1 Nov. A real unthrottled load of `/faq` showed first paint 1.4 s and no file over 0.6 s, and 12 parallel requests answered within 1.3 s. Single connections to the site's CloudFront edge sometimes stalled for about 22 s before any website code runs. Cause not proven. Re-test from another network or PageSpeed Insights (the API quota was exhausted and the web report didn't finish on 2 Nov).
  - **New items:**
    - Checkout shows "Import duties and taxes included" and adds 12 % tax for India on the same screen; waits for the owner's India tax answer (F-05).
    - `/about` now loads a 3.7 MB video (not loaded on 1 Nov; the merge didn't change the About code).
    - Report-only CSP `frame-src` lacks `https://api.razorpay.com`; add it before enforcing CSP (A-11), or the payment window will break.
    - `components/home/Certifications.tsx` isn't rendered anywhere, so the home strip wording is not visible on the site.
- **Pull requests (opened 2 Nov):** [storefront #23](https://github.com/House-of-diams/aws-houseofdiams-storefront/pull/23) and [admin #31](https://github.com/House-of-diams/House-of-diams-admin-/pull/31). Let GitHub CI pass on each before merging.
- **Not checked locally** (a laptop must not connect to the production database): real product pages, and the admin forms against the real database. Check these on production right after the merge, using the smoke list in the runbook.

| ID | On the branch | Storefront / admin commit | Still open after the merge |
|---|---|---|---|
| A-14 | Done: `app/b2b` and `components/b2b` deleted; PRD.md now says there is no public B2B page | `848ff0b` | — |
| A-01, A-17 | Done: all wording from the fact box; 15 % restocking fee on `/returns`; "Free Return" → "15-Day Returns"; 24 → 12 hours; `/shipping` gets the 10–14 + 6–8 days timeline | `325c918` | Sitewide text scan after deploy; then D-05 |
| A-02, A-16 | Done: one `material`, `itemCondition`, 12 main-market countries, `deliveryTime` (10–14 + 6–8 days), `restockingFee: 15`; Organization `foundingDate` 2014, co-founder `jobTitle`, `areaServed`. Feed gets transit 6–8 days | `6f5ab2f` | A-16: the Business Profile URL is not added (unknown); add it in CMS → SEO → profile links |
| A-03 | Done: 6 × 301 in `next.config.ts`; 410 for `/b2b`, `/blog/hip-hop-jewellery-culture-meets-craft`, `/education/education-copy`, `/shop/fine-jewellery-test-product-1787569248925`, `/shop/produt-1` (in `proxy.ts`) | `9fcda4a` | `curl -sI` each URL after deploy |
| A-09, A-10 | Done | `6e98a58` | Lighthouse Accessibility 100 |
| A-11 | Part: `X-Powered-By` removed. CSP stays report-only | `6e98a58` | Enforce CSP after a week of clean reports |
| A-07 | Done: category pages hide chips to empty listings (same check as the menu) | `483b3b4` | Fresh crawl |
| A-08 | Done: `llms.txt` starts with key facts, links categories, products moved to `llms-full.txt` | `307db85`, `fa21160` | — |
| A-13 | Done: related posts by shared tags/words (newest first on ties), last place goes to the next article by id so none is left unlinked; guide links on 6 category pages | `7f58589`, `e5614ac` | Fresh crawl: "at least 3 links" also counts category guides and links inside articles |
| A-06 | Code done: poster first; phones, tablets, reduced-motion and Save-Data/slow connections tap to play (square play button, as `DESIGN.md` requires); desktop loads the video only when it is on screen | `9287f29` | **Transcode the MP4s** to ≤ 1.5 MB (needs ffmpeg + S3 access) |
| A-05 | Part: menu, footer, cart drawer and cookie banner links prefetch on hover/focus/touch only; search suggestions load on intent; Aureva and Roman Cavalry no longer preloaded. (Settings/footer/promotion were already fetched once per page on 1 Nov.) | `788feba`, `b33c9be` | Profile `/engagement-rings` long tasks; code-split filters, quiz, reels; re-run Lighthouse |
| A-04, A-12, A-15 | Not done | — | A-04 is an architecture + CloudFront change (C-03); A-12 needs B-05; A-15 was skipped because icon paths may be stored in the database |
| B-01 | Part: renaming no longer changes an existing slug (10 forms); the slug field says it is the live address | `49377db` | The 301 on a deliberate slug change comes from the DB trigger in migration `202610190030`; its production status is "unknown" in `db/migrations/applied/production.json`. Confirm it is installed |
| B-06 | Done: articles set to "Show on website" can't be saved without a meta description, and the reason shows next to the field; title meters count " \| House of Diams" (not on the homepage); product SEO fields get meters too; with no SEO title the meter measures the title the website will use | `2fec02b`, `8a28970`, `43e55f5` | — |
| B-03 | Part: "Image alt text" field for the mega-menu featured image. The "Link item" part was delivered by the developer (`05716eb`, already in `main`). A new image resets the alt to the menu label | `9d40eed`, `3fc7c7a` | Change the Fine Jewelry image alt to "Fine Jewelry" in the Navbar Builder after the merge |
| A-14 (admin) | Done: the Navbar Builder no longer suggests a `/b2b` link (owner: no B2B page), and SEO settings hides the retired row | `95d4eab`, `3fc7c7a` | — |
| B-02, B-04, B-05 | Not done | — | B-02 and B-04 need a database migration first (the admin role can only read `seo_redirects`; options have no SEO columns). B-05 needs S3 object moves |

---

## Quick checklist (P0 first)

- [x] **D-01** GA4 event tags in Tag Manager (published 2 Nov; `purchase` is checked on the first real order)
- [x] **D-02** Consent on Clarity and Pinterest tags (published 2 Nov; Best Practices 100 after storefront PR #26)
- [ ] **D-04** Apex sitemap submitted and 5 of 6 validations started on 2 Nov; the `www` sitemap removal and 1 validation are still open
- [ ] **D-05** Return policy fixed and resubmitted on 2 Nov, waiting for Google's review; stale products already gone; shipping time waits for the owner
- [ ] **A-01** Remove hard-coded "overnight / same-day / Ready to Ship / 24 hours" wording
- [ ] **A-02** Product schema: single `material`, `itemCondition`, short country lists, `deliveryTime`
- [ ] **A-03** 301/410 for old 404 URLs
- [ ] **A-06** Product video weight
- [ ] **E-01** Spec metas and H1s on the 8 ranking articles
- [ ] **A-04 / A-05 / C-03** Speed: HTML caching, prefetch, duplicate calls, fonts, JS
- [ ] **B-01 / B-02** Auto-301 on slug change and a redirect manager in the admin
- [ ] The rest by priority

---

## Fact box (the only claims allowed — owner-confirmed, latest 2026-11-01)

- **Production and shipping:** every piece is made to order. Standard pieces take about 10–14 days to make; delivery takes about 6–8 days. Open 24/7. Free and insured shipping to every country; no order cut-off time.
- **Duties and delivery:** import duties and taxes are included in the price, with nothing to pay on delivery. A signature may be required, depending on the piece's value.
- **Returns:** within 15 days of delivery, unworn. Refund once the piece reaches House of Diams. Return shipping and duties are paid by the customer. **15 % restocking fee** (owner, 2026-11-01); the customer also pays return shipping and any import duties on the return. Bespoke/custom pieces can't be returned unless the piece doesn't match the agreed design.
- **Certificates and services:** IGI and GIA certificates; free resizing; free annual cleaning; free lifetime warranty (no terms published).
- **Bespoke timing:** typically 2–3 weeks to make plus about 6–9 days delivery; about 3–4 weeks from design approval; depends on the selected stone; an estimate, not a guarantee.
- **Company:**
  - Co-founders Krish Babariya and Akshar Korat.
  - In the diamond trade since 2014 (B2B); House of Diams is the direct-to-consumer arm (2025).
  - New York office (address below) and a presence in over 20 countries.
  - Conflict-free, ethically sourced diamonds, cut and processed in-house.
  - admin@houseofdiams.com, replies within 12 hours.
  - 831, Pragati IT World, Yogi Chowk, Surat, Gujarat 395010, India · +91 93285 36178 · by appointment only.
  - 36 W 44th Street, New York, NY 10036, USA (owner, 2026-11-02; no suite number).

**Not allowed:** any US address other than the New York office (36 W 44th Street, New York, NY 10036, USA; owner, 2026-11-02; no suite number); "same-day", "overnight", "ready to ship", "in stock" (for dispatch); "duties and taxes may apply/vary"; "a signature is required"; a courier name (until confirmed); "40+ countries"; "2–3 business days"; "within 24 hours"; a restocking fee other than 15 %; "Free Return" (returns are not free).

---

## PART A — Storefront code (`aws-houseofdiams-storefront`)

| ID | Pri | Where | Problem (evidence, 1 Nov) | Fix | Done when |
|---|---|---|---|---|---|
| **A-01** [O-17, O-03] | **P0** | `components/home/HomeTrustStripe.tsx`; `components/home/Certifications.tsx`; `components/product/ProductTrustRow.jsx` (+ icon `public/produc page svgs/01-overnight-shipping.svg`); `components/product/ProductTagLine.jsx`; `lib/policy-text.ts` (`SHIPPING_POLICY`, `PRODUCT_INCLUDES`); `app/faq/page.tsx` + `components/home/FAQ.tsx` fallback; `components/checkout/CheckoutDeliveryPreview.tsx`; `components/contact/ContactDrawer.tsx`, `ContactBody.tsx`, `ContactHero.tsx`; `components/home/EnquireModal.tsx`, `BespokeEnquiryModal.tsx`; `components/bespoke/BespokeForm.tsx`; `components/pages/BespokeClient.tsx` | The live site still says: "Complimentary Overnight Shipping" (home strip), "Overnight Shipping" (home + product trust row), "Ready to Ship" badge, "We offer free, insured shipping to every country, with same-day overnight dispatch" (`/shipping`), "Same-day overnight dispatch" (cart "your order includes"), "Customs and duties may vary by country" (FAQ fallback), "Complimentary Overnight Shipping with Signature" (checkout), "Our team normally replies within 24 hours" (contact panel on **all 246 pages**), and "within 24 hours" in the enquiry modals and toasts. All of these contradict the fact box | Use only fact-box wording:<br>• Home strip item → "Duties & Taxes Included" or "Made to Order".<br>• Trust-row "Overnight Shipping" → "Free Insured Shipping" (rename the icon).<br>• Remove the "Ready to Ship" badge.<br>• `SHIPPING_POLICY` = "We offer free, insured shipping to every country, with no order cut-off time. Every piece is made to order, and all import duties and taxes are included in the price."<br>• Remove the "Same-day overnight dispatch" line from `PRODUCT_INCLUDES`.<br>• FAQ fallback → "All import duties and taxes are included in the price."<br>• Checkout → "Complimentary Insured Shipping".<br>• Every "24 hours" → "12 hours" (fallbacks too) | A sitewide text scan of all 246 pages finds none of: overnight, same-day, ready to ship, duties may, signature is required, 24 hours |
| **A-02** [S-01 follow-up] | **P0** | Product JSON-LD builder (`lib/` product schema helper used by `app/shop/[slug]`) | Ahrefs: "Structured data has Google rich results validation error" on **182 product pages**: `Missing required deliveryTime` in `OfferShippingDetails`.<br>GSC merchant listings: "Duplicate field `material`" (6 metals as an array).<br>Each product lists **249 countries** in `applicableCountry` and 249 `shippingDestination` objects (≈ 15 KB of JSON-LD per page).<br>No `itemCondition` | 1. `material`: the default variant's metal as one string; or model the metals as `ProductGroup` + `hasVariant` (each variant with its own `material`, `sku`, `offers.price`).<br>2. Add `itemCondition: https://schema.org/NewCondition`.<br>3. Replace the 249-country lists: define `hasMerchantReturnPolicy` and `hasShippingService` once on the **Organization** (Google supports organization-level policies), and in each Offer keep `shippingDetails` with `shippingDestination` for the main markets only (US, CA, GB, AU, AE, IN …) or a reference.<br>4. Add `deliveryTime` (owner, 2026-11-01): `handlingTime` minValue 10 / maxValue 14, `transitTime` minValue 6 / maxValue 8, unitCode `DAY` (standard pieces).<br>5. In `hasMerchantReturnPolicy` add `restockingFee: 15` (a number = percent of price). | Rich Results Test on 3 product pages: 0 errors; GSC merchant listings: no "Duplicate field material"; product JSON-LD < 4 KB |
| **A-03** | **P0** | Redirects (`next.config.ts` `redirects()` or the `seo_redirects` table) | Old URLs Google still knows return **404 with no redirect**: `/blog/cvd-vs-natural-diamonds`, `/blog/choosing-your-engagement-ring`, `/blog/the-4cs-decoded-simply`, `/blog/surat-diamond-capital`, `/blog/hip-hop-jewellery-culture-meets-craft` (GSC listed them as 5xx), `/shop/pear-drop-diamond-station-necklace-1786613669264`, `/shop/liora-pear-diamond-eternity-band-1786789632304`, `/shop/fine-jewellery-test-product-1787569248925`, `/education/education-copy`. `/shop/produt-1` 301s to `/engagement-rings` (test leftover) [T-05] | 301 (one hop):<br>• `/blog/cvd-vs-natural-diamonds` → `/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams`<br>• `/blog/choosing-your-engagement-ring` → `/blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-of-diams`<br>• `/blog/the-4cs-decoded-simply` → `/blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat-house-of-diams`<br>• `/blog/surat-diamond-capital` → `/about`<br>• `/shop/pear-drop-diamond-station-necklace-1786613669264` → `/shop/celestine-dewdrop-pear-diamond-station-necklace` (if it is the same piece; otherwise 410)<br>• `/shop/liora-pear-diamond-eternity-band-1786789632304` → `/shop/pear-frame-eternity-band` (if equivalent; otherwise 410)<br>**410** for `/blog/hip-hop-jewellery-culture-meets-craft`, `/shop/fine-jewellery-test-product-1787569248925`, `/shop/produt-1`, `/education/education-copy` | `curl -sI` shows one 301 to a 200 page, or 410, for each URL |
| **A-04** [T-04] | **P1** | Layout/middleware (country and currency cookie), page `revalidate` | HTML is `private, no-store` on 246/246 pages, a CloudFront Miss every time; TTFB median **0.97 s**, p90 1.27 s, max 3.2 s | Public pages (home, categories, product pages, blog, education, policy pages) use ISR / `revalidate` + `Cache-Control: public, s-maxage=300, stale-while-revalidate=86400`, revalidated on CMS save. Move country/currency detection to the edge (`CloudFront-Viewer-Country` header) or client side, so the cached HTML carries no visitor-specific price. Keep `no-store` on cart, checkout, account and API | TTFB < 200 ms on a CloudFront Hit; prices still correct per currency; `bf-cache` passes |
| **A-05** [P-03, P-04, P-05, P-07] | **P1** | Navbar/menu `Link`s, `app/layout.tsx` data fetching, fonts (`app/fonts.ts`), listing grid | Mobile Lighthouse: Perf 38–89 (median ≈ 66), LCP 4.6–7.2 s on commerce pages; `/engagement-rings` TBT **5.2 s**, main thread 11 s. Each page load prefetches ≈ 25 menu routes (`?_rsc`), fetches `/api/public/settings`, `footer-content` and `promotion-popup` **twice**, and runs `/api/public/products/search?q=` with an empty query. 5 font families (Aureva, Cinzel, Inter, Montserrat, Roman Cavalry) + more load sitewide. 190–240 KB unused JS | `prefetch={false}` on mega-menu/footer links (prefetch on hover only); fetch settings/footer/promotion once (server or a shared cache); don't search until the user types; load only the fonts each page uses (drop Aureva/Roman Cavalry/Cinzel where unused; preload only the above-the-fold weight); profile `/engagement-rings` (filters/cards/carousels) and remove the long tasks; code-split filters, quiz and reels | Mobile Perf ≥ 85 and LCP < 2.5 s on home, `/shop`, `/engagement-rings`, `/fine-jewellery`, a category, a product page, `/blog` (Lighthouse 13.6, simulated throttling) |
| **A-06** [P-02] | **P0** | Product gallery video (`components/product/ProductGallery.tsx`) + media files | Product pages download **14–22 MB** (bracelet 17 MB desktop, earrings 22 MB desktop / 14 MB mobile) because of the product MP4s | Poster image first; load the video only on click or when it is in view and the connection isn't Save-Data/slow; transcode the files to ≤ 1.5 MB 720p H.264 + WebM; never autoplay on mobile | Product page total weight < 3 MB on desktop and < 2 MB on mobile |
| **A-07** [T-09 remainder] | **P1** | Category and sub-category grids/chips; homepage promo link | 13 internal links still point to empty `noindex` listings: `/wedding-bands/for-him/classic`, `/designer`, `/diamonds`; `/wedding-bands/for-her/nature`, `/solid`, `/cigar-band`, `/pavee`; `/fine-jewellery/necklaces/initials`, `/tennis-necklace`; `/fine-jewellery/rings/eternity-rings`; `/fine-jewellery/earrings/personalized-charm`, `/tennis-earrings` (linked from `/fine-jewellery`, `/fine-jewellery/necklaces`, `/wedding-bands`, `/wedding-bands/for-him` …). The menu was fixed; the page grids weren't | Apply the same "0 published products → hide" rule to category grids, sub-category chips and footer | No page links to a listing with 0 products |
| **A-08** | **P1** | `app/llms.txt/route.ts`, `app/llms-full.txt/route.ts` | `llms.txt` is mostly a product list; it has no key facts, buying guides or Education links | Start `llms.txt` with a "Key facts" section (the fact box above, in plain sentences), then: main categories (one line each), the 10 best guides (`/blog/...`) and Education pages, policies (shipping, returns, bespoke timing), contact. Keep products in `llms-full.txt` | `llms.txt` < 10 KB, starts with facts, links guides |
| **A-09** | **P1** | `components/ui/shadcn-select.tsx` | "Select Bracelet Length" placeholder `#8B94A5` on white = **3.05:1** (product page Accessibility 96) | `data-[placeholder]:text-[#8B94A5]` → `data-[placeholder]:text-[#5F6878]` | Product page Accessibility 100 |
| **A-10** [A-02] | **P2** | Top announcement bar link (`/shipping`) | Home mobile Lighthouse still flags the top-bar link contrast | Raise the link color contrast to ≥ 4.5:1 on the bar background | Home mobile Accessibility 100 |
| **A-11** | **P2** | `next.config.ts` | Response header `X-Powered-By: Next.js`; CSP is report-only | `poweredByHeader: false`; after a week of clean `/api/csp-report` logs, switch to an enforced `Content-Security-Policy` | Header absent; CSP enforced with no breakage |
| **A-12** [P-08] | **P2** | Media URLs | Published product images and `og:image`/`twitter:image` live under `/products/draft/…` | Serve published media from `/products/…` (see B-05); keep the old paths working | No live page references `/draft/` |
| **A-13** | **P1** | `components/pages/BlogPostPage.tsx` → `BlogRelatedPosts` (and `EducationPostPage`) | Related posts show the **same 3 articles** on every post (lab-grown vs natural, are lab-grown real, how to choose), so 18 of 21 posts get only one internal link (from `/blog`). Category pages don't link to any guide | Pick related posts by shared tag/category/cluster, exclude the current post, rotate in newer posts; add a server-rendered "Guides" block on category pages (e.g. engagement rings → ring size, 4Cs, shapes, lab vs natural; fine jewelry → necklace layering, 14K vs 18K) | Every article has ≥ 3 internal links from other articles or categories in a fresh crawl |
| **A-17** | **P0** | `lib/policy-text.ts` (`RETURNS_POLICY`); `components/home/Certifications.tsx:145`; `components/product/ProductTrustRow.jsx:16` | The site doesn't state the 15 % restocking fee (owner, 2026-11-01), so Merchant Center rejects the return policy (D-05). The home certifications strip and the product trust row say **"Free Return"**, which is false (the customer pays return shipping and a 15 % fee) | `RETURNS_POLICY`: after "…if it is unworn." add "A 15% restocking fee applies." Change "Free Return" to "Easy Returns" or "15-Day Returns" in both files (rename the icon file `03-15-days-free-return.svg`) | `/returns` shows the 15 % fee; a sitewide scan finds no "Free Return" |
| **A-14** | **P2** | `app/b2b/page.tsx`, `components/b2b/*` | **Owner decision 2026-11-01: no B2B/wholesale page.** `/b2b` already returns 404 and **no live page, sitemap or llms file links to it** (checked all 246 pages). The route and the 13 `components/b2b/*` files are unused leftovers (`B2BCtaBanner.jsx` still says "within 24 hours") | Delete `app/b2b/` and `components/b2b/` (dead code). Optional: return **410 Gone** for `/b2b` (via `seo_redirects` / B-02 or `proxy.ts`) so Google drops it faster. Keep the "B2B Wholesale" topic in the enquiry form (it is not a link) | `/b2b` returns 404 or 410; no `components/b2b` in the repo; GSC drops `/b2b` from the 404 report over time |
| **A-15** | **P2** | `public/Navbar svgs/`, `public/produc page svgs/` | Asset paths contain spaces and a typo ("produc"), so URLs are `%20`-encoded | Rename to `navbar-icons/`, `product-icons/` and update references | No asset URL contains `%20` |
| **A-16** | **P1** | Organization JSON-LD (all pages) | `sameAs` lacks the Google Business Profile; no `foundingDate`; founders are listed but without the co-founder role | Add the Business Profile (Maps) URL to `sameAs`; `foundingDate: "2014"` (in the trade since 2014 — owner confirmed); founders as `Person` with `jobTitle: "Co-founder"`; `areaServed` as worldwide | Rich Results Test valid; entity fields present |

## PART B — Admin code (`House-of-diams-admin-`)

| ID | Pri | Where | Problem | Fix | Done when |
|---|---|---|---|---|---|
| **B-01** | **P1** | `app/dashboard/catalog/catalog-client.tsx` (lines ≈ 505, 867, 1164), `metals/metal-form.tsx`, `stone-shapes`, `ring-sizes`, `material-values`, `[slug]/page-client.tsx`, `bespoke-client.tsx`, education hubs editor | Renaming a category/option/metal regenerates its slug (`prev.slug === slugify(prev.name) ? slugify(nextName)`), which changes a live URL with **no redirect**. It happened twice during the 31 Oct CMS edits and had to be reset by hand | After first publish, lock the slug (show it read-only with an "Edit URL" button and a warning). When a slug is changed on purpose, write a 301 (`old → new`) into `public.seo_redirects` in the same transaction | Renaming never changes a URL; a deliberate change creates a 301 automatically |
| **B-02** | **P1** | New admin page "Redirects" | `public.seo_redirects` is only **read** by the admin (`lib/db/admin-repositories/product-save.ts:41`); there is no screen to add, edit or remove a redirect (needed for A-03, T-05) | CRUD page: source path, target path or "410 Gone", type 301/410, note, created by/at; validate there are no chains or loops | The owner can add and remove redirects without SQL |
| **B-03** [O-15, O-16] | **P2** | Navbar Builder | Only category-bound items can be added (no plain "Blog"/"Education" links); the featured-image alt can't be edited (the Fine Jewelry image still has `alt="Fine Jewellery"`) | Add "Link item" (label + URL) and an "Image alt text" field on featured images | The owner can add Blog/Education to the menu; alt reads "Fine Jewelry" |
| **B-04** [O-14] | **P1** | Catalog → Options editor | Option pages (e.g. `/fine-jewellery/bracelet/bangles`) have no SEO title / H1 / meta / intro fields, so they fall back to "Bangles \| Fine Jewelry" / "Explore Bangles" / "Browse Bangles in Fine Jewelry." | Add SEO title, H1, meta description, intro text and "show in search" fields to options (as on categories) | Option pages show their own metadata |
| **B-05** [P-08] | **P2** | Product media upload | Published product images are stored under `/products/draft/` | Store under `/products/` on publish (move the object, keep the old key working) | New uploads never use `/draft/` once published |
| **B-06** | **P1** | Blog + Education editors (step "5 Publish") | When the SEO meta is empty, the site uses the article's first paragraph, which is why the ranking articles have untargeted metas; titles have no length guide | Make "SEO meta description" required on publish, with a 70–160 character counter; show the SEO-title length including " \| House of Diams" (warn > 60) | No published article uses its intro as the meta |

## PART C — Server / AWS / infrastructure

| ID | Pri | Problem | Fix | Done when |
|---|---|---|---|---|
| **C-01** [T-01] | P2 | `http://www.houseofdiams.com/x` → `https://www…/x` → `https://houseofdiams.com/x` (2 hops) | Let the CloudFront Function also redirect `http://www` straight to `https://houseofdiams.com` | One 301 |
| **C-02** [T-12] | P2 | `https://media.houseofdiams.com/` → **403** | 404 at the bucket root; `X-Robots-Tag: noindex` on non-image responses | Root returns 404 |
| **C-03** [T-04] | P1 | CloudFront doesn't cache HTML (see A-04) | Cache behaviors per path pattern with the cache key free of the currency cookie once A-04 moves detection to the edge; invalidate on CMS save | `x-cache: Hit` on repeat page views |
| **C-04** [T-13] | P2 | `app/api/cron/indexnow` exists, but its schedule and key file aren't confirmed (`/indexnow.txt` 404) | Schedule it (`docs/operations/scheduled-jobs.md`) and serve the key file; submit on publish | Bing Webmaster shows IndexNow submissions |
| **C-05** | P2 | Deploy keeps old JS for 7 days (verified working on 1 Nov) | Keep as is | — |

## PART D — Tracking and tool configuration

| ID | Pri | Tool | Problem (evidence) | Fix | Done when |
|---|---|---|---|---|---|
| **D-01** [G-03, G-04] | **P0** | Google Tag Manager `GTM-TJ5HTTSD` | **Update 2 Nov (log: `Technical/2026-11-02-platform-changes/README.md`):** 12 GA4 event tags published as Version 7. `view_item`, `add_to_cart`, `view_cart`, `begin_checkout` and `remove_from_cart` were seen live in GA4 requests; `purchase` is checked on the first real order. No tags for `page_view` or `view_search_results` because Enhanced Measurement already counts them, and none for `view_item_list` or `select_item` because the site doesn't send them. The old GA4 rule that created `add_to_cart` on every `/cart` page view was deleted the same day, at the owner's request. Baseline 1 Nov: the container has 4 tags (Conversion Linker, GA4 Google tag, Clarity, Pinterest) and **no GA4 event tags**. GA4 (4–31 Oct) has no `view_item`, `begin_checkout`, `purchase` or `generate_lead`; revenue ₹0. The site already pushes them to `dataLayer` | Create one "GA4 Event" tag per event: `view_item_list`, `select_item`, `view_item`, `add_to_cart`, `remove_from_cart`, `view_cart`, `add_to_wishlist`, `begin_checkout`, `add_shipping_info`, `add_payment_info`, `purchase`, `generate_lead`, `sign_up`, `login`, `view_search_results`. Each fires on a Custom Event trigger with the same name and sends ecommerce data from the dataLayer. Google tag: `send_page_view` off and a GA4 Event `page_view` on the custom `page_view` event (one per navigation). Test in Preview + DebugView, then publish | DebugView shows the full funnel; a test order shows `purchase` once with value |
| **D-02** | **P0** | Tag Manager consent | **Update 2 Nov:** done and published (Version 7). Neither tag loads for a fresh visitor or with cookies refused. After "Accept" both load from the next page. Storefront PR #26 (`d19247b`, live) removes refused Pinterest and Clarity cookies and allows `pagead2.googlesyndication.com` in the report-only policy: Best Practices is **100** on homepage desktop and mobile and one product page, and the real `_pin_unauth` cookie goes on "Reject all". Baseline 1 Nov: Microsoft Clarity and Pinterest fire on All Pages before the cookie choice; Lighthouse Best Practices **77** on every page (third-party cookies) | Clarity: "Require additional consent" → `analytics_storage`; Pinterest: `ad_storage` + `ad_user_data`. Fire them only after the consent update | Best Practices 100; no Clarity or Pinterest cookies before "Accept" |
| **D-03** | P1 | GA4 property `p543052053` | **Update 2 Nov:** currency is now USD. The "Internal Traffic" filter is now **Active** with the office IP (rule "Office"); no developer IPs were given, and it hasn't been tested with a real visit. Referrals, the `generate_lead` key event and the stream URL are unchanged. Baseline 1 Nov: currency **INR** (US market); no internal-traffic filter (Surat 46 and Satara 27 of the top cities); `accounts.google.com / referral` = 82 sessions (login flow) | Currency USD; define internal traffic (office/developer IPs) and activate the filter; unwanted referrals: `accounts.google.com`, `auth-uat.houseofdiams.com`, `checkout.razorpay.com`, `api.razorpay.com`; mark `purchase` and `generate_lead` as key events; link GA4 ↔ Search Console and GA4 ↔ Merchant Center | Clean source/medium report; revenue in USD |
| **D-04** | **P0** | Google Search Console | **Update 2 Nov:** apex sitemap submitted (Success, 246 pages). Validation started on 5 of 6 merchant-listing issues; `returnShippingFeesAmount` (4 items) wasn't started and may be a small code item. Search generative AI = Include. **Still open:** remove the `www` sitemap; request indexing. Baseline 1 Nov: only `https://www.houseofdiams.com/sitemap.xml` is submitted; merchant listings show `hasMerchantReturnPolicy`/`shippingDetails` warnings from before 31 Oct | Submit `https://houseofdiams.com/sitemap.xml`; after the apex one is read, remove the www one; click "Validate fix" on the two merchant-listing issues (after A-02 also on "material"); request indexing for the 10 blog posts and key categories; check Settings → "Search generative AI" is included | Apex sitemap "Success"; validations "Passed" |
| **D-05** | **P0** | Merchant Center (5837491424) | **Update 2 Nov:** restocking fee changed to 15 % and resubmitted; Google's review can take up to 10 days. Products are 182, from one source, so nothing was deleted. Shipping policy changed to 10–14 + 6–8, so 16–22 days. **Still open:** the owner confirmed "Accept exchanges" and refunds in 15–25 days, and [storefront PR #27](https://github.com/House-of-diams/aws-houseofdiams-storefront/pull/27) (`7538c84`, live) adds them to `/returns`. The FAQ and product page text are updated too. The exchange fee and condition rules aren't confirmed. Baseline 1 Nov: return policy "Standard for United Arab Emirates +101 more" is **Rejected**: "Return information provided does not match your online store". It says **customer pays shipping + 35 % restocking fee**, which isn't on the site and isn't a confirmed fact. 236 products in Merchant Center vs 182 in the site feed. Store quality "missing signals" (US, AU, IN) | Edit the return policy to match the site (15 days, unworn, customer pays return shipping and any duties, **restocking fee 15 %**, not 35 %), then resubmit **after A-17 is live** (the site must state the same fee). Handling time 10–14 days is confirmed; set shipping transit 6–8 days. Data sources: keep the site feed `/feeds/google-products.xml`; remove or merge the source that adds the 54 extra/old products. Add shipping speed once the courier is known (F-02); turn on the checkout link (the Buy link exists) | Return policy "Approved"; product count = feed count |
| **D-06** | P1 | Bing Webmaster Tools | Verified (meta present); state of the sitemap and IndexNow unknown | Submit the apex sitemap; enable IndexNow (C-04); import from GSC | Bing shows the sitemap processed |
| **D-07** | P1 | Google Business Profile | **Update 2 Nov (log: `Technical/2026-11-02-cms-changes/README.md`):** Jewellery Store + Jeweller, new description and website link with UTM saved, pending Google's review. Phone and chat are stuck in Google's review (owner must contact support). The country is locked to India, so a new New York profile was created (name, category, address, phone, website); it is **not verified and not public**. The owner must verify it by video, and its description goes in afterwards because Google's form would not save it. Photos and reviews still open. Baseline 1 Nov: Verified, "Jewelry manufacturer", products synced; **no phone**, hours "Open 24 hours", **0 reviews**, no photos, 1 pending Google update | Add the phone **+91 93285 36178** (owner confirmed 2026-11-01; same as the site); keep hours "Open 24 hours" (owner: open 24/7); add secondary categories (Jewelry store / Jeweler); description from the fact box; 10+ photos (workshop, pieces, team); review the pending update; website link with UTM (`?utm_source=gbp&utm_medium=organic`); start a review request after delivery (F-08) | Profile complete; first reviews arrive |

## PART E — CMS content in the admin (Claude can make these with the owner's OK; log every change)

| ID | Pri | Where | Problem | Fix | Done when |
|---|---|---|---|---|---|
| **E-01** | **P0** | Blog editor → SEO title/meta + H1 for 8 ranking articles | These articles (status `GSC BASELINE REQUIRED`; **baseline captured 1 Nov**, see `platforms_2026-11-01.md`) use their first paragraph as the meta, and some H1s differ from the approved spec (`On-page SEO/01`, `03`, `04`): lab-grown vs natural (6,256 impressions, position 26.5), 14K vs 18K (1,142; 11.6), ring size (1,049; 27.5), CVD vs HPHT (921; 32.5), diamond shapes (845; 8.2), 4Cs (321; 8.7), IGI certification, how to choose | Apply the spec title, meta and H1 per row (URL unchanged). 14K vs 18K title → "14K vs 18K Gold (and 10K) for Diamond Jewelry" (CMS-10) | Spec comparison: 0 mismatches on these 8 rows |
| **E-02** | P1 | Blog SEO titles | 13 blog titles are 61–78 characters (truncated in Google) | Shorten to ≤ 60 characters including " \| House of Diams", keeping the main keyword first (approved package titles only with the owner's OK) | No indexable title > 60 characters |
| **E-03** | P1 | Category/option metas | 3 boilerplate metas ("Browse … in …"): `/wedding-bands/for-her`, `/fine-jewellery/bracelet/bangles`, `/fine-jewellery/necklaces/pendant-necklace`; 9 short metas (31–68 characters): bangles, for-her, privacy, terms, `/fine-jewellery/bracelet`, lariat, chain-link, drop-dangle, toi-et-moi | Write 120–155-character metas with the page keyword and a fact-box benefit (bangles after F-04) | 0 boilerplate; 0 metas < 70 characters on indexable pages |
| **E-04** | P1 | Product `/shop/oval-floral-diamond-ring` | Decision OD-15 waited for the baseline (now captured): title/H1 should be "Oval Marquise Diamond Engagement Ring", slug unchanged | Apply title, H1 and meta from `On-page SEO/07` | Spec matches |
| **E-05** | **P1** | Blog/Education publishing | 11 calendar items are past their date and not live: BC-011, BC-037, BC-014, **EDU-LG-00 (MUST_PUBLISH)**, BC-015 (needs where-grown facts), BC-024, BC-016, BC-017, EDU-RJG-BR, BC-005 (now possible: in-house cutting confirmed), **BC-019 Black Friday**. 32 more are due in Nov–Dec. Education has 1 live article; the 6 hubs return 404 | Write with the existing system (calendar row + Stage 19 brief + facts), owner review, publish in this order: EDU-LG-00 → BC-019 (before 27 Nov) → BC-017 / BC-016 → BC-024 → the rest; publish an Education hub when it has ≥ 3 articles | Overdue list = 0; Education ≥ 15 pages by 1 Feb |
| **E-06** | on hold | Category intros (CMS-09) | Category pages have product cards only (364–659 words) | Owner said leave for now; revisit after E-05 | — |
| **E-07** | P2 | About → Values | The new "Conflict Free" and "Ethically Sourced" cards have no image (grey tile) | Upload two photos (workshop / cutting) | Cards show images |
| **E-08** | **P1** | `/blog/necklace-layering-how-to-layer-necklaces` | Ranks **3.3 for "how to layer necklaces" with 172 impressions and 0 clicks** | Title "How to Layer Necklaces: Lengths, Chains & Easy Rules" (≤ 60 incl. brand) and a meta that answers the question and promises the length chart | CTR > 3 % in GSC after 4 weeks |
| **E-09** | P1 | Article bodies | High-impression articles don't link to the commercial pages or to each other in the body text | In each of the top 8 articles add 2–4 natural links: guide ↔ guide, and guide → category/product (e.g. lab vs natural → `/engagement-rings`, shapes → by-design shape pages, ring size → `/engagement-rings`, 14K vs 18K → `/fine-jewellery`) per Stage 16 | Each article has ≥ 3 contextual internal links |

## PART F — Owner decisions and facts needed (answer in chat; nothing is published until answered)

| ID | Question | Blocks |
|---|---|---|
| **F-01** | ~~35 % restocking fee?~~ **Answered 2026-11-01: 15 %**, plus return shipping and any duties paid by the customer | A-17, A-02, D-05 |
| **F-02** | ~~Courier?~~ **Answered 2026-11-02: FedEx.** Transit days **answered 2026-11-01: about 6–8 days** | A-02 `deliveryTime`, D-05 shipping speed |
| **F-03** | ~~Making time for standard pieces?~~ **Answered 2026-11-01: about 10–14 days (1.5–2 weeks)** | A-02 `handlingTime`, feed |
| **F-04** | New name for `/fine-jewellery/bracelet/bangles` (designer bracelets, distinct from Tennis Bracelet) | B-04, E-03 |
| **F-05** | India tax (owner will answer next time). Checkout shows "taxes included" and adds 12 % for India | Checkout copy |
| **F-06** | Hours **answered: open 24/7**. Phone **answered: +91 93285 36178** (same as the site). Countries/areas still open | D-07 |
| **F-07** | ~~Should `/b2b` be a real wholesale page?~~ **Answered 2026-11-01: no** (owner confirmed "No B2B page"). Keep it removed; delete the unused code | A-14 |
| **F-08** | Reviews: start collecting (Google review link after delivery; on-site reviews later). Only real reviews may be shown or marked up | D-07, A-02 ratings |
| **F-09** | Spam backlinks (46 of the top 50 domains): recommendation is **no disavow** (no manual action; Google ignores them); confirm | — |
| **F-10** | Content production: Claude writes, owner reviews, then publishes in the CMS? Who signs off? | E-05 |

## PART G — SEO growth tasks (SEO side, not developer)

| ID | Pri | Task | Done when |
|---|---|---|---|
| **G-01** | P1 | Entity building for AI and Google: consistent brand bio (fact box) on Instagram, Facebook, Pinterest, LinkedIn, Crunchbase; claim profiles that are missing; same NAP everywhere | 6+ consistent profiles |
| **G-02** | P1 | Start outreach from `Off-page SEO/Backlink Acquisition/` (77-row database): wedding/jewelry directories, supplier/partner pages, lab-grown diamond explainers, local Surat/Indian press, US wedding blogs; brand-mention reclamation | 30 real referring domains by 1 Feb |
| **G-03** | P1 | Monthly re-audit with the same scripts (`Technical/<date>-live-validation/_scripts/`), plus the GSC/GA4/Merchant Center snapshot | A dated folder each month |
| **G-04** | P2 | Track AI visibility: GA4 AI referrals (chatgpt.com, perplexity.ai, gemini, copilot); quarterly manual check of 20 key questions in ChatGPT/Perplexity/Google AI Mode | Log in the report |

---

### Closed from the old 05 list (verified live, 1 Nov 2026)

| Item | Status |
|---|---|
| T-03 | Old JS survives deploys |
| T-08 | Only the canonical is absolute |
| T-10 | By-Design canonical |
| T-14 | `/search` |
| O-08 | One H1 |
| S-01 | Shipping/returns in offers (now see A-02) |
| S-04, S-05, S-06 | ItemList, home breadcrumb, WebSite |
| P-01 | Priority images |
| P-06 | Self-hosted flags |
| G-01, G-02 | Consent default + single page_view in code; GTM part is D-01/D-02 |
| A-06, A-07, TY-01…TY-04, Q-01 | change.md (commit `33f4a08`) |
| Q-07 | Sign-in host stays `auth-uat` (decision) |
| Q-08 | Clear-bag confirmation (developer, 31 Oct) |
