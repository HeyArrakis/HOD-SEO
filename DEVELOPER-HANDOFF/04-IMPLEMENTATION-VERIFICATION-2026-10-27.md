# 04 — Implementation Verification (final, re-verified 2026-10-28)

**What this is:** a from-scratch, read-only check of the public site (`https://houseofdiams.com`) after the developer reported the fixes complete. First check on 2026-10-27; **final re-check on 2026-10-28** after the developer reported more fixes. Nothing on the site was changed. No purchase, form submission or real enquiry was made. Test bags were created and then cleared, and the coupon quiz was stopped at the email step.
**Measured against:** the approved specs (`On-page SEO/01…10`), `DEVELOPER-HANDOFF/03`, the ten blog packages, `QA/main.md`, and your 31 decisions to the developer.
**Evidence:** `Technical/2026-10-28-live-validation/` (final: all 251 sitemap URLs + probes, spec comparison, page-by-page diff against 2026-10-27) and `Technical/2026-10-27-live-validation/`. Browser retests were done in the built-in browser on both days.

## 1. Verdict

A large part of the batch is done and verified. The ten blogs are correct, commercial titles/metas/H1s match the spec, and most empty listings are hidden. The boilerplate FAQ schema is gone, `/contact` and the `/bespoke` timeline are live, and seven of the ten developer QA bugs are fixed or no longer reproducible.

**The 2026-10-28 re-check found only one real fix (bracelet length in the cart, BUG-009) and three new problems.** A test blog post and a test product were published on the live site and linked from many pages. Because of the test product, the empty round-rings page is indexable again.

**Still not done:**
- The unverified shipping, returns and certification claims are shown across the site.
- The nav label typos are still live.
- Product-schema names still differ from H1s.
- The missing internal links were not added.
- The About page H1 is still the placeholder "Hero banner 1".

## 2. What changed between 2026-10-27 and 2026-10-28

| Change | Type |
|---|---|
| BUG-009: the cart page now shows "Bracelet Length: 7 Inch" (checkout already did) | **Fixed** |
| **Test blog post published:** `/blog/this-is-test-article` — title "This is title for seo and here is the in derpt details abott", H1 "title of card", meta "cdccdcdc…". It's indexable, in the sitemap, and linked from `/blog`, `/blog?page=2` and all 20 other articles (it displaced a real related-article link on each) | **New problem — CRITICAL** |
| **Test product published:** `/shop/produt-1` — title "seo n1", H1 "seo 2", meta "seo meta data for the description". It's indexable, in the sitemap, and linked from 40 pages: `/shop`, the By-Design page and its eight style pages, round-rings and 28 product pages (related items) | **New problem — CRITICAL** |
| `/engagement-rings/round-rings` is back in the sitemap and indexable (it now shows "1 piece", the test product) | **Regression** |
| Everything else on the 248 pages crawled on both days: titles, metas, H1s, canonicals, robots and schema are identical to 2026-10-27 | No change |

## 3. Fixed — verified live

| Item | Result (2026-10-28) |
|---|---|
| Ten blogs (BC-001, 003, 004, 006, 007, 008, 009, 018, 035, 036) | All 10: HTTP 200, title + meta + H1 exactly as in each package, self-canonical, in sitemap, listed in the `/blog` index, every package internal link present, article image has alt text, URLs unchanged |
| Commercial / homepage / bespoke / FAQ metadata | Of 49 live "ready" pages with a specified title, **44 match exactly**. The 5 that don't are refresh articles: four are on your Q26 wait list, and EDU-CERT-01 is also a refresh. Homepage title: "House of Diams \| Luxury Diamond Jewelry & Bespoke Rings" |
| Boilerplate "Browse X in Y" metas | 42 → 4: the deferred By-Design page, `/wedding-bands/for-her`, bangles, and round-rings again |
| Empty listings | 13 of 15 are `noindex, follow` and out of the sitemap. `/collection` was never fixed and round-rings regressed (§2) |
| FAQPage schema | Only on `/faq`; its 40 schema questions match the 40 visible questions |
| BreadcrumbList | Missing only on `/` and `/collection` (was 11 pages) |
| `/contact` | Real page: 200, indexable, self-canonical, in sitemap. Title "Contact Us", H1 "Contact House of Diams", meta as you supplied, no invented phone or address |
| `/bespoke` | Title, meta and H1 per spec; "4–6 weeks" removed; the timeline reads "Typically 2–3 weeks to make plus about 6–9 days delivery; about 3–4 weeks from design approval (estimates, not guarantees)" |
| `/shipping` placeholder | "new test black" / "test desc" removed |
| Drafts and Education hubs | The 6 hubs return 404 and none of the 30 drafts is public |
| Deferred items left alone (as instructed) | `by-desgin` URLs still 404, the By-Design page is still self-canonical, `tennis-bracelet` and the host are unchanged |
| Server speed | TTFB median about 1.0 s on both days (max 3.13 s on 2026-10-24) |

## 4. Not fixed — still with the developer

| # | Item | Evidence (2026-10-28) | Decision it breaks |
|---|---|---|---|
| 1 | **Remove the test article and test product** | See §2. Unpublish both, remove them from the sitemap and listings, and restore the related links they displaced | New (no test content on the live site) |
| 2 | **Unverified claims still shown sitewide** | See the breakdown below this table | Q16, Q17 |
| 3 | Placeholder text and expired promo | Cart and checkout: "Why house of diams — **tesxt 1**". "Apply September sale" on product pages, cart and checkout | Q15, OD-08 |
| 4 | Empty pages | `/collection` ("0 pieces") is still indexable, in the sitemap and in `/llms.txt`. `/engagement-rings/round-rings` is indexable again (§2) | OD-07, Q11 |
| 5 | Nav and category label typos | "Solitare" and "Anniversay" are still in the menu on `/`, `/engagement-rings`, `/wedding-bands` and `/fine-jewellery`; the menu still says "Fine Jewellery" (American English rule). Cart recommendation still shows a product named "Solatire Ring" | Q9, OD-05 |
| 6 | Product pages | Product schema name ≠ visible H1 on **109 of 183** PDPs; 65 PDP titles are over 60 characters; one duplicate title ("Round Solitaire Diamond Pendant 2.00 CT") | Q4, Q29, MD-02 |
| 7 | Internal links | Of the 52 specified links that were missing, **51 are still missing**. Of 65 required links between live pages, 36 are missing (up from 34, because the test article replaced real related links) | Q22, MD-07 |
| 8 | Article author | Person author still on `/blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide` and `/education/lab-grown-diamond-certification-explained-gia-vs-igi-house-of-diams`, plus the test article | Q19 |
| 9 | About page | H1 is still the placeholder "**Hero banner 1**" (it was "About House of Diams" on 2026-10-24); the page also says "Certified Jewelery" | Regression |
| 10 | Safe policy metadata | `/shipping` and `/returns` titles not set to the spec values ("Shipping & Delivery", "Returns & Exchanges"); `/about` title/meta not per spec | Q1 |
| 11 | Bespoke wording | The timeline omits "depends on the selected stone" from your approved wording | Q13 |
| 12 | Performance (BUG-008) | The bracelet page still autoplays a **16 MB** video (`preload="none"` but `autoPlay`). Page load (LCP) not re-measured | QA BUG-008 |

**Breakdown of item 2 (unverified claims still shown):**
- **Homepage strip:** "Complimentary Overnight Shipping · IGI Certified · Free Worldwide Delivery · Lifetime Warranty".
- **Top bar:** "Free Worldwide Shipping".
- **Cart drawer on every page, and the cart page:** "Complimentary Insured Shipping · Complimentary 15-Day Returns".
- **Checkout:** "Complimentary Overnight Shipping with Signature", "Order before 3 PM".
- **`/bespoke`:** "Full IGI / GIA certification included", "Fully insured worldwide delivery — complimentary to 40+ countries".
- **Every product page:** "Worldwide insured shipping is complimentary", "UPS Overnight shipping", "returns within 30 days", "craftsmanship warranty".
- **`/faq` and `/returns`:** "Every piece is expertly certified".

## 5. QA bugs

| Bug | Final result |
|---|---|
| BUG-002 checkout currency | **Not reproducible**: only "United States (USD)" is offered; all cart/checkout prices are consistent USD (re-checked 2026-10-28) |
| BUG-003 password recovery | **Fixed**: "Forgot your password?" opens the Reset Password page (link re-checked 2026-10-28; reset email not sent) |
| BUG-004 WhatsApp | **Fixed**: full number (wa.me/91…), re-checked 2026-10-28 |
| BUG-005 keyboard order | **Fixed** (desktop, 2026-10-27): no hidden menu item receives focus |
| BUG-008 performance | **Not fixed** (§4 #12) |
| BUG-009 bracelet length | **Fixed 2026-10-28**: cart and checkout both show "Bracelet Length: 7 Inch"; no wrong ring size |
| BUG-010 coupon email | **Fixed** (2026-10-27): "invalid" shows "Enter a valid email address" and does not advance. The popup did not appear during the 2026-10-28 session, so it was not re-run |
| BUG-012 email mismatch | **Fixed**: each displayed address matches its link. Two addresses are shown (Admin@ and info@); HOD should pick one (F-C2) |
| BUG-015 HipHop images | **Not applicable**: those pages were removed (404) |
| BUG-020 test product in search | **Fixed**: neither the old test product nor the new test items appear in suggestions (2026-10-28); the old URL is still 404 + noindex |
| BUG-006 / BUG-013 (client) | Return-window numbers are still shown (15 and 30 days, §4 #2); "tesxt 1" remains (§4 #3) |

## 6. Waiting on HOD or deferred by you (not counted as failures)

* **BC-001** still says "6–9 days of insured shipping". It was left as you decided (Q14) and needs HOD's answer to F-A1.
* Waiting on HOD facts: real shipping and returns terms, About/founder facts, and `sameAs`/contact details (F-A1, F-A2, F-C1, F-C2).
* Deferred to the technical phase:
  - The nine `by-desgin` 301s.
  - The By-Design page canonical.
  - Apex vs www host (www still answers 200).
  - The `tennis-bracelet` slug.
  - The two 404 product URLs.
  - Pagination "Page N" titles.
* Waiting for GSC: the refresh articles (EDU-CERT-01 included) and the oval PDP rename.
* Not to publish yet: the 30 drafts and the Education hubs.

## 7. Other things to raise

* Login sends customers to **`auth-uat.houseofdiams.com`** (still true on 2026-10-28), a test-environment ("UAT") name on the live site. Ask the developer to confirm this is the intended production login.
* The test article and test product suggest the developer is testing the admin's SEO fields on production. Ask them to use a staging site, or to keep test items unpublished.

## 8. Limits

These are static-HTML checks plus a browser session from one location (India), at desktop width. Not measured:
- Core Web Vitals/LCP.
- Mobile keyboard behavior.
- Password-reset email delivery.
- The payment step.
- Googlebot rendering.
- GSC.

Raw data is in `Technical/2026-10-28-live-validation/` and `Technical/2026-10-27-live-validation/`.
