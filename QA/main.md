# House of Diams — Main QA Handoff

Website: [houseofdiams.com](https://www.houseofdiams.com/).

**12 selected open bugs: 2 Client fixes and 10 Developer fixes.** Original bug numbers are unchanged. Evidence was recorded on **5–6 October 2026 (Asia/Kolkata)**; this consolidated handoff was prepared on **7 October 2026**. No new live retest or website fix is claimed.

This is the single detailed file for the client, developer, Claude or GPT. [easy.md](easy.md) is the short, plain-language companion. The observations, steps, measurements, test results, limits and full page inventory are included here. Screenshots, raw captures, tools, CSVs and the ZIP were removed at the owner's request; this document has no dependency on them. Recorded observations are preserved as text, but original visual/raw attachments are no longer available.

## Contents

- [Summary](#summary)
- [All 12 bugs: owner, live links, steps, results and impact](#bugs)
- [Actions and retesting](#actions-and-retesting)
- [Checkout and accounts](#checkout-and-accounts)
- [Performance](#performance)
- [Navigation and resources](#navigation-and-resources)
- [Accessibility](#accessibility)
- [Responsive coverage](#responsive)
- [All 125 retained test cases](#test-results)
- [All 316 page-inventory rows](#page-inventory)
- [Instructions for Claude or GPT](#instructions-for-claude-or-gpt)

## Summary

**Current status: assigned fixes pending.**

| Selected bugs | Client | Developer | P0 | P1 | P2 high | P3 medium | P4 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 12 | 2 | 10 | 0 | 0 | 7 | 5 | 0 |

### Client fixes

- **BUG-006:** Returns page lacks return conditions and purchase surfaces disagree on the window.
- **BUG-013:** Shipping and order-trust sections expose placeholder text.

### Developer fixes

- **BUG-002:** Delivery line prices use USD numbers with an INR symbol.
- **BUG-003:** Forgot-password link returns to the login page.
- **BUG-004:** Hydrated WhatsApp links omit the business phone number.
- **BUG-005:** Closed mobile navigation remains in the keyboard tab order.
- **BUG-008:** Shopping pages have slow main-content rendering and heavy blocking work.
- **BUG-009:** Bracelet length is absent from cart and checkout review; cart shows a ring size.
- **BUG-010:** Promotion quiz advances with an invalid email address.
- **BUG-012:** Displayed support email and mailto recipient differ.
- **BUG-015:** Two public HipHop category SVGs return HTTP 400.
- **BUG-020:** Search suggests an unavailable test product that opens a 404.

### Coverage and measured performance

308 public URL variants were checked by HTTP; saved browser observations cover 35 distinct URLs / 30 paths. Manual checks were representative. Chrome and an independent Chromium session were used.

18 Lighthouse audits cover nine pages in mobile/desktop modes. Mobile performance scores: **35–64**; desktop: **37–91**. Product mobile LCP: **18.21 seconds** in the saved lab run. [Performance report](#performance).

### Safety and recommendation

No purchases, payments, production orders, account creation or successful enquiry submissions were made. Cart/wishlist baseline was preserved/restored. **Checkout success state could not be safely tested because reaching it requires a real payment/order.** The Continue to Payment action first calls a production order-placement endpoint, so it was not clicked. Safari, Firefox, Edge, physical phones, real screen-reader speech and actual 200% zoom remain untested.

Complete the assigned fixes and verify them. A safe account/payment environment is needed before full checkout sign-off. [Simple guide](easy.md) · [Assigned priorities](#actions-and-retesting) · [Bug register](#bugs).

## Bugs

All are **CONFIRMED — OPEN** in this historical audit. Open status means the assigned fix has not been verified here. P2 means high priority; P3 means medium priority. The owner assignments below are the client's requested work split.

| Bug ID | Fix Owner | Severity | Priority | Problem |
| --- | --- | --- | --- | --- |
| BUG-002 | Developer | P2 | Before release | Delivery line prices use USD numbers with an INR symbol |
| BUG-003 | Developer | P2 | Before release | Forgot-password link returns to the login page |
| BUG-004 | Developer | P2 | Before release | Hydrated WhatsApp links omit the business phone number |
| BUG-005 | Developer | P2 | Before release | Closed mobile navigation remains in the keyboard tab order |
| BUG-006 | Client | P2 | Before release | Returns page lacks return conditions and purchase surfaces disagree on the window |
| BUG-008 | Developer | P2 | Before release | Shopping pages have slow main-content rendering and heavy blocking work |
| BUG-009 | Developer | P3 | Next QA cycle | Bracelet length is absent from cart and checkout review; cart shows a ring size |
| BUG-010 | Developer | P3 | Next QA cycle | Promotion quiz advances with an invalid email address |
| BUG-012 | Developer | P3 | Next QA cycle | Displayed support email and mailto recipient differ |
| BUG-013 | Client | P3 | Next QA cycle | Shipping and order-trust sections expose placeholder text |
| BUG-015 | Developer | P3 | Next QA cycle | Two public HipHop category SVGs return HTTP 400 |
| BUG-020 | Developer | P2 | Before release | Search suggests an unavailable test product that opens a 404 |

Website: [https://www.houseofdiams.com/](https://www.houseofdiams.com/)

Only the selected client/developer work items are listed. No website fixes or new live retest were performed for this revision.

| Severity | Selected count |
| --- | --- |
| P0 | 0 |
| P1 | 0 |
| P2 | 7 |
| P3 | 5 |
| P4 | 0 |

### Client fixes

#### BUG-006 — Returns page lacks return conditions and purchase surfaces disagree on the window

**Fix owner:** Client · **Severity:** P2 · **Priority:** Before release

**Category:** Policies / checkout

**Environment:** Live production, macOS Chrome responsive emulation; independent Chromium/Lighthouse where noted. Primary viewport details are listed in this document; original raw captures are not retained.

**Affected pages:** [/returns](https://www.houseofdiams.com/returns) · [/faq](https://www.houseofdiams.com/faq) · [/cart](https://www.houseofdiams.com/cart) · [/shop/rosette-five-flower-bracelet](https://www.houseofdiams.com/shop/rosette-five-flower-bracelet) · [/shop/camille-two-tone-knot-t-bar](https://www.houseofdiams.com/shop/camille-two-tone-knot-t-bar) · [/shop/amara-pear-swirl-solitaire-ring](https://www.houseofdiams.com/shop/amara-pear-swirl-solitaire-ring)

**Steps to reproduce:**

1. Open Returns from support navigation or /returns.
2. Read the content.
3. Compare product return badges, product complimentary shipping & returns text, and cart/checkout promises.

**Expected result:** Show the approved return eligibility, window and process; purchase surfaces should agree.

**Actual result:** /returns shows “Is House of Diams legitimate?” and its general answer, with no return window/process. Product badges and cart/checkout say 15 days; expanded product text says returns within 30 days. FAQ directs customers back to the footer policy.

**Reproducibility:** Reproduced twice or more

**Customer impact:** Customers cannot determine which return conditions apply before purchasing.

**Business impact:** Support disputes and reduced trust around a material purchase decision.

**Action for assigned owner:** Client: decide the approved return window, eligibility and process. Replace unrelated Returns content and use consistent policy wording across product pages, cart and checkout. This audit does not decide whether 15 or 30 days is correct.


#### BUG-013 — Shipping and order-trust sections expose placeholder text

**Fix owner:** Client · **Severity:** P3 · **Priority:** Next QA cycle

**Category:** Content quality

**Environment:** Live production, macOS Chrome responsive emulation; independent Chromium/Lighthouse where noted. Primary viewport details are listed in this document; original raw captures are not retained.

**Affected pages:** [/shipping](https://www.houseofdiams.com/shipping) · [/cart](https://www.houseofdiams.com/cart) · [/checkout?mode=cart](https://www.houseofdiams.com/checkout?mode=cart) · [/](https://www.houseofdiams.com/)

**Steps to reproduce:**

1. Open Shipping and read the delivery information.
2. Open a populated cart or checkout and read Why house of diams.
3. Observe the rotating announcement bar during normal browsing.

**Expected result:** Publish final customer-facing copy in informational and purchase-trust sections.

**Actual result:** Shipping displays “NEW TEST BLACK” and “test desc”; cart/checkout displays “This is new pointer”. The announcement rotation also displayed “New line”. These are observed interface strings, not editorial style judgments.

**Reproducibility:** Reproduced twice or more

**Customer impact:** Shipping and purchase reassurance content is incomplete or unexplained.

**Business impact:** Undermines confidence at the point of purchase.

**Action for assigned owner:** Client: replace unfinished Shipping text, order-trust pointers and announcement messages with approved customer-facing content.


### Developer fixes

#### BUG-002 — Delivery line prices use USD numbers with an INR symbol

**Fix owner:** Developer · **Severity:** P2 · **Priority:** Before release

**Category:** Checkout

**Environment:** Live production, macOS Chrome responsive emulation; independent Chromium/Lighthouse where noted. Primary viewport details are listed in this document; original raw captures are not retained.

**Affected pages:** [/checkout?mode=cart](https://www.houseofdiams.com/checkout?mode=cart)

**Steps to reproduce:**

1. With India (INR) active, add or use a cart containing Rosette yellow gold and Asteria necklace.
2. Proceed from cart to checkout.
3. Compare Delivery line prices against the cart and Order Summary.

**Expected result:** All amounts use the selected currency and the same converted line values.

**Actual result:** Delivery cards showed ₹335 for Rosette and ₹1,515 for Asteria, while their cart prices were ₹32,257 and ₹1,45,880. The Order Summary used the converted subtotal. This is a display defect; the charged amount was not tested.

**Reproducibility:** Reproduced twice or more

**Customer impact:** The customer cannot reconcile individual products with the checkout total.

**Business impact:** Checkout trust and abandonment risk.

**Action for assigned owner:** Inspect delivery-item amount formatting versus shared Order Summary currency conversion. Include fractional-price and quantity cases in regression.


#### BUG-003 — Forgot-password link returns to the login page

**Fix owner:** Developer · **Severity:** P2 · **Priority:** Before release

**Category:** Authentication

**Environment:** Live production, macOS Chrome responsive emulation; independent Chromium/Lighthouse where noted. Primary viewport details are listed in this document; original raw captures are not retained.

**Affected pages:** [/login](https://www.houseofdiams.com/login)

**Steps to reproduce:**

1. Open Login.
2. Select Forgot your password?
3. Repeat at desktop and mobile widths.

**Expected result:** Open a password recovery form or a clear supported recovery path.

**Actual result:** The link destination is /login. Clicking leaves the customer on Login without a recovery form or instructions.

**Reproducibility:** Reproduced twice or more

**Customer impact:** A customer who has forgotten the password cannot recover the account through this link.

**Business impact:** Lost returning-customer purchases and avoidable support contacts.

**Action for assigned owner:** Inspect authentication route/link configuration and implement the approved recovery flow. Delivery of reset email and password change were not tested.


#### BUG-004 — Hydrated WhatsApp links omit the business phone number

**Fix owner:** Developer · **Severity:** P2 · **Priority:** Before release

**Category:** Navigation / contact

**Environment:** Live production, macOS Chrome responsive emulation; independent Chromium/Lighthouse where noted. Primary viewport details are listed in this document; original raw captures are not retained.

**Affected pages:** [/](https://www.houseofdiams.com/) · [/bespoke](https://www.houseofdiams.com/bespoke) · [/cart](https://www.houseofdiams.com/cart) · [/shop/camille-two-tone-knot-t-bar](https://www.houseofdiams.com/shop/camille-two-tone-knot-t-bar)

**Steps to reproduce:**

1. Open the page and allow its customer interface to load.
2. Inspect Chat with us or the product WhatsApp link destination.
3. Compare it with the displayed business telephone number.

**Expected result:** Use the complete business number in the WhatsApp destination.

**Actual result:** Client-rendered links repeatedly become https://wa.me/91?text=… instead of the full +91 93285 36178 number. Initial server HTML contains wa.me/919328536178. No WhatsApp message was sent.

**Reproducibility:** Reproduced twice or more

**Customer impact:** The support/product enquiry shortcut has an incomplete recipient.

**Business impact:** Lost high-intent enquiries and support friction.

**Action for assigned owner:** Inspect client CMS/contact hydration, phone sanitization and fallback values. Keep the country code plus subscriber number, and test after hydration rather than only server HTML.


#### BUG-005 — Closed mobile navigation remains in the keyboard tab order

**Fix owner:** Developer · **Severity:** P2 · **Priority:** Before release

**Category:** Accessibility

**Environment:** Live production, macOS Chrome responsive emulation; independent Chromium/Lighthouse where noted. Primary viewport details are listed in this document; original raw captures are not retained.

**Affected pages:** [/](https://www.houseofdiams.com/) · [/engagement-rings](https://www.houseofdiams.com/engagement-rings) · [/shop/rosette-five-flower-bracelet](https://www.houseofdiams.com/shop/rosette-five-flower-bracelet) · [/bespoke](https://www.houseofdiams.com/bespoke) · [/blog](https://www.houseofdiams.com/blog) · [/cart](https://www.houseofdiams.com/cart)

**Steps to reproduce:**

1. At desktop width, leave the mobile menu closed.
2. Focus the visible Search control and repeatedly press Tab.
3. After visible header controls, inspect where focus moves. Repeat the sequence.

**Expected result:** Tab should move only through visible, available controls; closed overlays must not take focus.

**Actual result:** After Sign up, focus enters off-screen SEARCH, HOME, category controls and other mobile-menu entries. Their ancestor has aria-hidden=true and their y coordinates are negative (e.g. -790). Eleven hidden menu stops occurred before the hero CTA. Lighthouse also flags the shared menu on multiple pages.

**Reproducibility:** Reproduced twice or more

**Customer impact:** Keyboard customers lose visible focus and must traverse unavailable controls.

**Business impact:** A shared navigation accessibility barrier affects shopping and informational pages.

**Action for assigned owner:** Inspect closed-overlay focusability. Consider inert/unmounting or removing descendants from tab order, coordinated with opening focus and restoration. Also inspect hidden product size-guide descendants identified by the automated audit.


#### BUG-008 — Shopping pages have slow main-content rendering and heavy blocking work

**Fix owner:** Developer · **Severity:** P2 · **Priority:** Before release

**Category:** Performance

**Environment:** Live production, macOS Chrome responsive emulation; independent Chromium/Lighthouse where noted. Primary viewport details are listed in this document; original raw captures are not retained.

**Affected pages:** [/](https://www.houseofdiams.com/) · [/engagement-rings](https://www.houseofdiams.com/engagement-rings) · [/shop/rosette-five-flower-bracelet](https://www.houseofdiams.com/shop/rosette-five-flower-bracelet) · [/bespoke](https://www.houseofdiams.com/bespoke) · [/blog](https://www.houseofdiams.com/blog) · [/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide](https://www.houseofdiams.com/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide) · [/cart](https://www.houseofdiams.com/cart) · [/login](https://www.houseofdiams.com/login) · [/checkout?mode=cart](https://www.houseofdiams.com/checkout?mode=cart)

**Steps to reproduce:**

1. Run Lighthouse navigation audits with the repeatable presets shown in the Performance section, using isolated sessions and both mobile and desktop presets.
2. Review LCP, TBT and network resource data.
3. For the product, inspect the large autoplay video and compare mobile/desktop results.

**Expected result:** Main shopping content should render promptly and interactions should avoid long blocking work; set and validate release performance budgets.

**Actual result:** All nine mobile scores were 35–64, with LCP 7.15–18.21 s. Rosette mobile was 35, LCP 18.21 s, TBT 3,508 ms and 26.30 MiB transferred; desktop was 37, LCP 16.68 s and 30.72 MiB. Its video alone transferred 23.56 MiB mobile / 27.92 MiB desktop. Shared font and script costs also appear on lightweight routes.

**Reproducibility:** 18 valid lab audits; product problem present in both modes. One sample per URL/mode, not field telemetry

**Customer impact:** Slow product visibility and delayed response, especially on constrained mobile connections.

**Business impact:** Conversion, bandwidth and abandonment risk.

**Action for assigned owner:** Prioritize product video delivery/poster/initial playback, main-thread profiling and client rendering dependencies. Then review shared font duplication, third-party execution, responsive images and caching. Causes are evidence-backed investigation directions, not a proof that one resource alone accounts for simulated LCP. See performance for per-URL metrics.


#### BUG-009 — Bracelet length is absent from cart and checkout review; cart shows a ring size

**Fix owner:** Developer · **Severity:** P3 · **Priority:** Next QA cycle

**Category:** Cart / product options

**Environment:** Live production, macOS Chrome responsive emulation; independent Chromium/Lighthouse where noted. Primary viewport details are listed in this document; original raw captures are not retained.

**Affected pages:** [/shop/rosette-five-flower-bracelet](https://www.houseofdiams.com/shop/rosette-five-flower-bracelet) · [/cart](https://www.houseofdiams.com/cart) · [/checkout?mode=cart](https://www.houseofdiams.com/checkout?mode=cart)

**Steps to reproduce:**

1. Select 7 Inch or 7.5 Inch Bracelet Length on Rosette.
2. Add To Bag and Skip for now, or use Buy Now.
3. Inspect cart variant text and expanded checkout item details.

**Expected result:** Show the selected bracelet length in the customer review, and do not show an unrelated ring size.

**Actual result:** Cart variant text showed “10K White Gold, US 4, Lab Grown Diamond, round” without the selected length. Checkout delivery and expanded summary omitted it too. Buy Now did preserve 7.5 Inch in its custom URL data; loss of backend option data is NOT established.

**Reproducibility:** Reproduced twice or more

**Customer impact:** The customer cannot confirm the intended bracelet fit before proceeding.

**Business impact:** Wrong-fit concerns and avoidable support contacts; fulfillment impact needs server-side verification.

**Action for assigned owner:** Inspect category-aware variant labels and custom-option rendering in cart/checkout. Verify stored/order custom options in a safe test environment.


#### BUG-010 — Promotion quiz advances with an invalid email address

**Fix owner:** Developer · **Severity:** P3 · **Priority:** Next QA cycle

**Category:** Forms / promotion

**Environment:** Live production, macOS Chrome responsive emulation; independent Chromium/Lighthouse where noted. Primary viewport details are listed in this document; original raw captures are not retained.

**Affected pages:** [/](https://www.houseofdiams.com/)

**Steps to reproduce:**

1. Open Get Your Coupon Code.
2. Enter a first name and advance to email.
3. Enter invalid and choose Next.
4. Go Previous and repeat the invalid email step. Do not submit Reveal my code.

**Expected result:** Reject invalid email format on the email step with an understandable error.

**Actual result:** The email input has type=email and invalid format, but Next advances to Step 3. This was reproduced through backward navigation. Final lead submission/server validation was not tested.

**Reproducibility:** Reproduced twice or more

**Customer impact:** A user can complete several steps before discovering an invalid contact address.

**Business impact:** Potential lead-quality and completion risk; stored invalid leads have not been demonstrated.

**Action for assigned owner:** Inspect per-step validation and error focus before changing the active step. Also validate on the final server endpoint.


#### BUG-012 — Displayed support email and mailto recipient differ

**Fix owner:** Developer · **Severity:** P3 · **Priority:** Next QA cycle

**Category:** Navigation / contact

**Environment:** Live production, macOS Chrome responsive emulation; independent Chromium/Lighthouse where noted. Primary viewport details are listed in this document; original raw captures are not retained.

**Affected pages:** [/](https://www.houseofdiams.com/) · [/contact](https://www.houseofdiams.com/contact) · [/returns](https://www.houseofdiams.com/returns) · [/bespoke](https://www.houseofdiams.com/bespoke)

**Steps to reproduce:**

1. Read the support email in the footer or Contact/Returns panel.
2. Inspect the email link destination without sending a message.

**Expected result:** The displayed address matches the mailto recipient, unless the routing is clearly explained.

**Actual result:** The interface displays Admin@houseofdiams.com but opens mailto:info@houseofdiams.com. No email was sent; mailbox delivery was not tested.

**Reproducibility:** Reproduced twice or more

**Customer impact:** Customers cannot tell which support address they are contacting.

**Business impact:** Contact identity confusion and possible misrouting.

**Action for assigned owner:** Inspect CMS contact labels and link values, and ask the merchant which address should be canonical. Do not assume either mailbox is nonexistent.


#### BUG-015 — Two public HipHop category SVGs return HTTP 400

**Fix owner:** Developer · **Severity:** P3 · **Priority:** Next QA cycle

**Category:** Network / images

**Environment:** Live production, macOS Chrome responsive emulation; independent Chromium/Lighthouse where noted. Primary viewport details are listed in this document; original raw captures are not retained.

**Affected pages:** [/hiphop/chains](https://www.houseofdiams.com/hiphop/chains) · [/hiphop/chains/cuban-links](https://www.houseofdiams.com/hiphop/chains/cuban-links) · [/hiphop/test-subcat](https://www.houseofdiams.com/hiphop/test-subcat)

**Steps to reproduce:**

1. Open HipHop Chains.
2. Inspect the Chains and category-option images.
3. Request the two public asset URLs listed in Navigation and resources; repeat GET.

**Expected result:** Category images load successfully or use an intentional accessible fallback.

**Actual result:** 004-battery-low.svg and 005-approximate-equals.svg return 400 on HEAD and on two GET attempts each. On /hiphop/chains the two img elements finished with naturalWidth=0; visible dimensions were about 138–140×209–211 px.

**Reproducibility:** HEAD plus two independent GETs for each asset; completed broken images observed in browser

**Customer impact:** Missing category imagery while browsing the HipHop taxonomy.

**Business impact:** Navigation presentation and catalog-quality issue.

**Action for assigned owner:** Inspect uploaded storage objects, permissions and CMS asset paths. The other 16 initially flagged asset URLs contained unencoded spaces in the QA checker and passed after proper encoding; they are not bugs.


#### BUG-020 — Search suggests an unavailable test product that opens a 404

**Fix owner:** Developer · **Severity:** P2 · **Priority:** Before release

**Category:** Search / broken navigation

**Environment:** Live production, macOS Chrome responsive emulation; independent Chromium/Lighthouse where noted. Primary viewport details are listed in this document; original raw captures are not retained.

**Affected pages:** [/](https://www.houseofdiams.com/) · [/shop/fine-jewellery-test-product](https://www.houseofdiams.com/shop/fine-jewellery-test-product)

**Steps to reproduce:**

1. Open Search and leave the query empty.
2. Select Fine Jewellery Test Product from the 16 product suggestions.
3. Inspect the destination. Repeat from the search interface.

**Expected result:** Only customer-visible, available product records should be suggested, and each suggestion should resolve to its product.

**Actual result:** The first empty-query suggestion is Fine Jewellery Test Product. Clicking opens /shop/fine-jewellery-test-product with “We couldn’t find that page”. The destination returned HTTP 404 on two independent GET checks. It was absent from the original server-link crawl.

**Reproducibility:** Two suggestion selections; two independent HTTP 404 checks

**Customer impact:** The search interface promotes an unavailable item and sends the customer to an error page.

**Business impact:** Product-discovery failure and exposed test data.

**Action for assigned owner:** Inspect search publication/status filtering and catalog index invalidation. Validate suggestion slugs against the public product resolver.


### Test limits

No purchases, payments, production orders, account creation or successful enquiry submissions were made. Cart/wishlist baseline was preserved/restored. **Checkout success state could not be safely tested because reaching it requires a real payment/order.** The Continue to Payment action first calls a production order-placement endpoint, so it was not clicked. Safari, Firefox, Edge, physical phones, real screen-reader speech and actual 200% zoom remain untested.

HTTP reachability is not a functional pass. Manual UI tests were representative. [Functional matrix](#test-results) · [Assigned priorities](#actions-and-retesting).

## Actions and retesting

Client: BUG-006 and BUG-013. Developer: BUG-002, BUG-003, BUG-004, BUG-005, BUG-008, BUG-009, BUG-010, BUG-012, BUG-015 and BUG-020. Use the assigned actions in each bug and the acceptance checks below. Priorities remain as shown in the register above.

Check client content against approved wording. Recheck the ten developer issues and repeat mobile/desktop speed checks. Use staging accounts and a sandbox payment gateway for account/payment completion.

### Acceptance checks for each selected bug

| Bug ID | Fix Owner | What to check before closing the bug |
| --- | --- | --- |
| BUG-002 | Developer | With India/INR selected, compare the same product and quantity in cart, checkout Delivery and summary. Unit and extended amounts must use the same currency conversion and rounding. Verify other supported currencies in staging; do not infer that a real charge was tested. |
| BUG-003 | Developer | Forgot your password must open a usable recovery flow on desktop/mobile. Verify the recovery request, reset link and password update using an approved test account and controlled inbox. |
| BUG-004 | Developer | After the page finishes loading and after refresh, all relevant WhatsApp links must retain the full approved business number. Check homepage, bespoke, cart and product templates without sending a real message. |
| BUG-005 | Developer | With the menu closed, Tab must skip every hidden menu item. With it open, its controls must be usable. Closing it should restore a sensible visible selection; verify keyboard behavior in supported browsers. |
| BUG-006 | Client | The client must approve one return window, eligibility and process, publish them on Returns, and make product, FAQ, cart and checkout promises agree. Do not assume whether 15 or 30 days is the intended rule. |
| BUG-008 | Developer | Repeat the same nine-page mobile/desktop Lighthouse presets, preferably three runs each and report the median. Measure loading, blocking work and transferred bytes after changes. Preserve gallery/video behavior and approved analytics; assess field LCP/INP/CLS separately. Agree the performance budget before claiming a pass. |
| BUG-009 | Developer | Select at least 7 Inch and 7.5 Inch bracelet lengths. Cart and expanded checkout review must show the chosen length and must not show an irrelevant ring size. Check both Add To Bag and Buy Now; URL retention alone is not proof of visible review or backend storage. |
| BUG-010 | Developer | Empty or invalid email must keep the customer on the email step with a clear error. A valid-format email should advance. Repeat after Previous/Next navigation. Test final delivery only against a controlled staging endpoint. |
| BUG-012 | Developer | Use the merchant-approved support address for both the visible text and email recipient in all affected templates. Verify the link without sending a real email. Neither mailbox was demonstrated to be nonexistent. |
| BUG-013 | Client | The client must replace unfinished Shipping, order-trust and announcement text with approved wording. Check desktop/mobile Shipping, populated cart/checkout and the complete announcement rotation. |
| BUG-015 | Developer | Both named category assets must load successfully and display actual image content on the affected HipHop routes. Check correctly encoded URLs and both browser rendering and HTTP results. |
| BUG-020 | Developer | Search suggestions must contain only available public products with working destinations. Recheck empty-query suggestions and typed searches after index/cache updates; selecting every returned suggestion should open the intended product rather than a 404. |

Fixes must be verified against the current build. The historical audit does not prove that any issue still exists today or that a later change resolved it. Retest financial, account and successful form actions in a safe test environment.

## Checkout and accounts

Audit: 5–6 October 2026. Production safety limits govern the final transitions. “TESTED” describes execution; “PASSED/FAILED” applies to the particular outcome. See [full matrix](#test-results).

### Login, registration and account

| Area | Execution | Outcome | Evidence / limits |
| --- | --- | --- | --- |
| Login empty/invalid format | TESTED | PASSED | Native required/email validation; no request with incomplete fields |
| Incorrect synthetic login | TESTED | PASSED | One qa-audit@example.com incorrect credential attempt; understandable error; no real customer credentials |
| Password visibility toggle | TESTED | PASSED | Show/Hide works; dummy values cleared |
| Forgot password | TESTED | FAILED — BUG-003 | Link points back to /login; no recovery UI |
| Signup empty/invalid email/short password | TESTED | PASSED | Required/email/pattern checks; no account created |
| Valid signup / duplicate email / otherwise-valid mismatch submission | NOT SAFELY TESTABLE | No pass claimed | No approved safe account mechanism; final account submission avoided |
| Valid login / remembered session / logout / back after logout | NOT SAFELY TESTABLE | No pass claimed | No approved test credentials supplied |
| Unauthenticated profile and orders deep link | TESTED | PASSED | Sign-in gate; no personal/order data displayed |
| Authenticated profile/orders/addresses | NOT SAFELY TESTABLE | No pass claimed | Requires approved test account |
| Reset email / reset completion | NOT SAFELY TESTABLE | No pass claimed | Recovery entry is broken; no mailbox/credential changes |

### Cart and purchase entry

The initial Chrome cart contained Rosette Five-Flower Bracelet (10K Yellow Gold, quantity 1) and Asteria Seven-Stone Necklace (quantity 1). QA added a white-gold Rosette line, increased/decreased quantity, refreshed and removed that QA line. The two original merchandise lines remained quantity one. The interface’s automatic Princess Halo gift was observed; no order was placed or inventory edited. Original wishlist was empty and was restored to empty after a reversible Camille save/remove test. An independent in-app Chromium cart started empty and returned to empty after QA.

| Case | Outcome | Notes |
| --- | --- | --- |
| Add / optional letter skip | PASSED for bag entry | QA line added; no purchase made |
| Quantity 1→2→1 | PASSED | Values and summary updated; no stress/max-stock test |
| Decrement at one in isolated cart | PASSED | Removed sole QA line and showed empty state |
| Cart refresh / remove / cleanup | PASSED | Original two lines preserved |
| Empty cart / Explore Products | PASSED for displayed recovery | Independent empty-session evidence |
| Variant/customization review | FAILED — BUG-009 | Length absent; irrelevant US 4 shown; URL custom data retained |
| Buy Now | PASSED for preview navigation | Selected product entered direct checkout; no final order |
| Invalid coupon | PASSED | QA_INVALID_20261005 rejected; checking state disabled Apply |
| Valid coupon / complete gift boundaries | PARTIAL | Gift included state observed; no full eligibility regression |

### Checkout fields and safe review

| Case | Outcome | Observed result |
| --- | --- | --- |
| Load populated checkout desktop/mobile | PASSED | Shipping form and summary rendered |
| Empty required fields | PASSED | Inline validation on required identity/address fields |
| Invalid email/phone/postal | PASSED | not-an-email, abc and !@# rejected |
| India lookup 395007 | PASSED | Surat/Gujarat/India autofill; shipping review reached |
| US 10001 lookup | NEEDS VERIFICATION | Early failure; independent retest succeeded with New York/United States |
| Shipping option | TESTED / limited choice | Complimentary signature/insured overnight shown; no alternative method selector |
| Subtotal/tax arithmetic | PARTIAL | ₹1,78,156 + ₹21,379 = ₹1,99,535; 12% arithmetic consistent within rounding; correctness of jurisdiction/rate not certified |
| Delivery line amounts | FAILED — BUG-002 | USD numeric values formatted as INR |
| Edit / back / refresh | TESTED / mixed | Edit retained data; Back returned to cart/product; reload cleared customer fields |
| Server quote error | NEEDS VERIFICATION | White-gold independent preview showed pricing could not be confirmed |
| Responsive layout | TESTED at 390×844 | Captured safe steps; full payment overlay not rendered |

### Exact safety stop: before Continue to Payment

The shipping review was reached using fictitious QA data (reserved example.com email and a fictional phone), without real payment information. Inspection of the publicly served checkout JavaScript shows that **Continue to Payment first POSTs to `/api/checkout/place`**, then opens Razorpay after order creation. The bundle indicates stock reservation/order creation in that path. It is not a harmless gateway-preview button. This action was not clicked. No `/api/checkout/place` request was intentionally issued by QA.


**Payment screen: NOT SAFELY TESTABLE** through the exposed flow without first creating a production order. No gateway credentials, payment details, authorization, decline/cancel or refund was attempted.

**Checkout success state could not be safely tested because reaching it requires a real payment/order.** Confirmation page, receipt/email, inventory/order state and success/error transitions require a sandbox or staging test checkout. No safe test-order mechanism was discovered in the customer UI.

### Cleanup and handoff

Viewport overrides were reset. No successful contact/bespoke/promotion submissions, account changes, production purchases were made. Only QA documentation and requested local ignore rules were changed.


### Assigned work

Developer: BUG-002 (currency), BUG-003 (recovery), BUG-009 (bracelet review). Client: BUG-006 (returns), BUG-013 (unfinished trust text). [Assigned priorities](#actions-and-retesting).

### Recorded public checkout-code observation

The saved public bundle contained this order-placement call before opening the payment popup. The following is a truncated diagnostic excerpt, not implementation code. This is a client-code observation, not a tested server transaction. No order-placement request was intentionally made.

```javascript
fetch("/api/checkout/place",{method:"POST",headers:{"content-type":"application/json",...a?{authorization:`Bearer ${a}`}:{"x-guest-checkout-token":r}},body:JSON.stringify({idempotencyKey:n,item:eJ?null:w(eW),items:eJ?eX.map(w):void 0,customer:B,loveLetter:eQ,currencyCode:z,coupon:ei?{id:ei.id,code:ei.code}:null})}),l=await i.json().catch(()=>null);return i.ok?(ey(l),l):(l?.retryable&&(e$.current=null),e&&Q(l?.error??"Unable to start payment."),null)})();eL.current=t;try{return await t}finally{eL.current=null}},tc=async()=>{let t=to();if(ee(t),Object.keys(t).length>0)return void Q("Please complete all required customer and shipping details bef
```

The public client code also referenced payment verification and redirecting to a checkout success route. Those paths were not exercised. The code extract must not be treated as proof that payment, stock release, receipts or order confirmation work.

## Performance

Test dates: 5 October 2026 for the saved lab runs; functional follow-up on 6 October. Website: https://www.houseofdiams.com/

### Method and practical limits

Official Lighthouse 13.5.0 ran against nine live URLs in mobile and desktop navigation modes. Each valid row is a single cold navigation sample in a separate headless Chrome profile. The mobile preset simulated a Moto G Power; desktop used `--preset=desktop`. The run settings and timestamps are preserved in this document below. Runtime environment can influence timings. [Lighthouse variability guidance](https://github.com/GoogleChrome/lighthouse/blob/main/docs/variability.md) explains this limitation.

Cart and checkout lab runs had **empty isolated carts**. They measure the public empty-state/guard page, not the populated checkout tested manually. A score of 100 for those empty states does not validate the populated form or payment integration. The first homepage desktop run ended with PAGE_HUNG and null scores; the failed attempt is excluded from scoring. The successful retry scored 84. The PageSpeed API returned 429 quota exhaustion; no PageSpeed or CrUX result was fabricated.

### Measured scores and timings

FCP, LCP and Speed Index are seconds; TBT is milliseconds. CLS is unitless. SEO is recorded only because Lighthouse reports it; no SEO strategy audit was performed.

| URL / saved HTML report | Device | Performance | Accessibility | Best Practices | SEO | FCP s | LCP s | TBT ms | CLS | Speed Index s | Key Issues |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [/](https://www.houseofdiams.com/) | mobile | 42 | 92 | 73 | 100 | 2.17 | 8.15 | 1071 | 0.0015 | 9.33 | Slow LCP, Blocking work |
| [/](https://www.houseofdiams.com/) | desktop | 84 | 92 | 73 | 100 | 0.79 | 1.85 | 15 | 0.0005 | 3.25 | Shared asset costs |
| [/engagement-rings](https://www.houseofdiams.com/engagement-rings) | mobile | 45 | 91 | 73 | 100 | 1.58 | 10.83 | 1086 | 0.0000 | 6.82 | Slow LCP, Blocking work |
| [/engagement-rings](https://www.houseofdiams.com/engagement-rings) | desktop | 48 | 96 | 73 | 100 | 0.86 | 2.67 | 1095 | 0.0009 | 3.29 | Blocking work |
| [/shop/rosette-five-flower-bracelet](https://www.houseofdiams.com/shop/rosette-five-flower-bracelet) | mobile | 35 | 88 | 73 | 100 | 2.05 | 18.21 | 3508 | 0.0005 | 9.16 | Slow LCP, Blocking work, Large autoplay video |
| [/shop/rosette-five-flower-bracelet](https://www.houseofdiams.com/shop/rosette-five-flower-bracelet) | desktop | 37 | 89 | 73 | 100 | 1.21 | 16.68 | 678 | 0.0002 | 5.72 | Slow LCP, Blocking work, Large autoplay video |
| [/bespoke](https://www.houseofdiams.com/bespoke) | mobile | 43 | 90 | 73 | 100 | 1.49 | 15.35 | 2096 | 0.0000 | 5.15 | Slow LCP, Blocking work |
| [/bespoke](https://www.houseofdiams.com/bespoke) | desktop | 75 | 91 | 73 | 100 | 0.89 | 2.12 | 241 | 0.0001 | 2.32 | Blocking work |
| [/blog](https://www.houseofdiams.com/blog) | mobile | 42 | 96 | 73 | 100 | 1.80 | 16.72 | 1246 | 0.0001 | 7.38 | Slow LCP, Blocking work |
| [/blog](https://www.houseofdiams.com/blog) | desktop | 81 | 96 | 73 | 100 | 0.78 | 2.12 | 104 | 0.0001 | 2.95 | Shared asset costs |
| [/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide](https://www.houseofdiams.com/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide) | mobile | 64 | 96 | 73 | 100 | 1.81 | 9.02 | 278 | 0.0000 | 5.72 | Slow LCP, Blocking work |
| [/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide](https://www.houseofdiams.com/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide) | desktop | 60 | 96 | 73 | 100 | 0.86 | 4.99 | 240 | 0.0002 | 2.94 | Slow LCP, Blocking work |
| [/cart](https://www.houseofdiams.com/cart) | mobile | 53 | 96 | 73 | 66 | 1.72 | 8.28 | 904 | 0.0000 | 3.40 | Slow LCP, Blocking work, Empty session only |
| [/cart](https://www.houseofdiams.com/cart) | desktop | 91 | 96 | 73 | 66 | 0.85 | 1.61 | 72 | 0.0001 | 1.48 | Empty session only |
| [/login](https://www.houseofdiams.com/login) | mobile | 61 | 100 | 73 | 66 | 1.19 | 7.15 | 595 | 0.0000 | 2.12 | Slow LCP, Blocking work |
| [/login](https://www.houseofdiams.com/login) | desktop | 65 | 100 | 54 | 66 | 0.51 | 1.44 | 1486 | 0.0000 | 1.03 | Blocking work |
| [/checkout?mode=cart](https://www.houseofdiams.com/checkout?mode=cart) | mobile | 53 | 100 | 73 | 63 | 1.56 | 8.57 | 842 | 0.0000 | 4.00 | Slow LCP, Blocking work, Empty session only |
| [/checkout?mode=cart](https://www.houseofdiams.com/checkout?mode=cart) | desktop | 68 | 100 | 54 | 63 | 0.41 | 1.32 | 888 | 0.0600 | 0.99 | Blocking work, Empty session only |

All nine mobile LCP samples were above 4 seconds; mobile performance ranged from 35 to 64. Desktop ranged from 37 to 91. Observed CLS was below 0.1 in every lab run. These lab findings do not establish a field Core Web Vitals pass/fail. Good field targets are LCP ≤2.5 seconds, INP ≤200 ms and CLS ≤0.1 at the 75th percentile. [Google Web Vitals definitions](https://web.dev/articles/vitals).

**INP: NOT AVAILABLE.** Navigation Lighthouse runs did not provide real-user INP; TBT is a lab responsiveness diagnostic and must not be relabelled as INP. **CrUX / field CWV status: NOT AVAILABLE** in the obtained evidence. [Chrome TBT documentation](https://developer.chrome.com/docs/lighthouse/performance/lighthouse-total-blocking-time).

### Transfer size and request count

Bytes are recorded network transfer, including third parties during the audit window. Counts are Lighthouse network request records, including repeated/range requests; they are not unique URLs.

| Page | Device | Transfer bytes | MiB | Network records | Largest transfer |
| --- | --- | --- | --- | --- | --- |
| home | mobile | 4807167 | 4.58 | 268 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz,wght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| home | desktop | 4589911 | 4.38 | 359 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz%2Cwght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| collection | mobile | 2654948 | 2.53 | 159 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz%2Cwght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| collection | desktop | 2755698 | 2.63 | 264 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz,wght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| product | mobile | 27581771 | 26.30 | 124 | https://pub-0ea48ff8bc25421e949ac1de2d305b1a.r2.dev/products/bracelet/BR050110/BR050110%20-%20YL-compressed.mp4 |
| product | desktop | 32213957 | 30.72 | 223 | https://pub-0ea48ff8bc25421e949ac1de2d305b1a.r2.dev/products/bracelet/BR050110/BR050110%20-%20YL-compressed.mp4 |
| bespoke | mobile | 2561200 | 2.44 | 118 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz,wght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| bespoke | desktop | 2571365 | 2.45 | 218 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz%2Cwght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| blog | mobile | 2527696 | 2.41 | 112 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz,wght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| blog | desktop | 2646326 | 2.52 | 223 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz,wght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| article | mobile | 2483236 | 2.37 | 104 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz,wght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| article | desktop | 2536068 | 2.42 | 206 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz%2Cwght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| cart | mobile | 2468155 | 2.35 | 120 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz,wght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| cart | desktop | 2523379 | 2.41 | 222 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz%2Cwght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| login | mobile | 1939034 | 1.85 | 65 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz%2Cwght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| login | desktop | 1757971 | 1.68 | 67 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz%2Cwght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| checkout | mobile | 3133837 | 2.99 | 260 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz%2Cwght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |
| checkout | desktop | 3133098 | 2.99 | 263 | https://www.houseofdiams.com/_next/static/media/Inter_VariableFont_opsz%2Cwght-s.p.0oy~rb7-bgeiw.ttf?dpl=dpl_A3E3TGjeMQrMfSzzhzZWM6Ddbd8h |

### Developer investigation priorities — BUG-008

#### Product video and LCP

Rosette transferred 27,581,771 bytes mobile and 32,213,957 bytes desktop. The bracelet MP4 accounts for 24,700,186 / 29,275,283 bytes respectively. The LCP audit identifies an autoplay, loop, muted video in the gallery. Mobile LCP was 18.21 seconds, desktop 16.68 seconds. Review an appropriately compressed video ladder, initial poster, range delivery and whether immediate autoplay/full video acquisition is necessary. Profile the gallery’s resource discovery and render delay. This is the largest measured resource; its size alone does not explain every millisecond of simulated LCP.

#### Shared blocking work and client rendering

Mobile TBT was 3,508 ms product, 2,096 ms bespoke, 1,247 ms blog and 1,087 ms collection. Investigate hydration/initial rendering long tasks and defer nonessential UI work. Lighthouse estimated unused JavaScript savings of about 368 KiB on home and 213 KiB on the product. These are audit estimates, not guaranteed savings or instructions to remove functionality.

#### Fonts and duplicated URLs

The Inter variable TTF appears twice with a literal comma versus an encoded `%2C` in the URL. Home mobile recorded 456,412 and 456,240 bytes for those entries. Review preload/CSS URL normalization and consolidate actual font families/weights needed for each route. Prefer appropriate web font formats and subsets. Font-display audits did not identify a failed swap strategy; do not assume invisible text was observed.

#### Third-party cost

Product mobile recorded Google Tag Manager/gtag at about 337 KB and 299 ms main-thread time, Clarity at 109 ms, and Pinterest at 68 ms. Home also loaded Instagram embeds and two gtag URL variants. Review duplicate tag loading, consent/initialization dependencies and deferred below-fold embeds while preserving approved analytics requirements. Main-thread time is the audit’s recorded CPU time, not TBT or causal LCP attribution. No tracking settings were changed.

#### Images, CSS, cache and compression

Image-delivery audits estimated savings of 484 KiB product, 50 KiB collection, 32 KiB bespoke and 99 KiB login desktop. Review responsive dimensions and generated formats. Product image optimization remains relevant even though its MP4 dominates weight. The cache audit estimated 493 KiB product and 317 KiB home mobile; inspect the exact URLs and storage/cache headers, especially repeatedly reused assets. No bulk CSS-removal issue was established: unused CSS audit numeric savings were zero in the inspected runs. Shared CSS is render-blocking; inspect the measured waterfall before splitting it. Lighthouse did not expose a separate text-compression failure in these reports. HTTP headers were saved; this audit does not assert a blanket compression defect.

### Per-URL audit opportunities

#### https://www.houseofdiams.com/

- Reduce unused JavaScript: Est savings of 368 KiB.
- Use efficient cache lifetimes: Est savings of 317 KiB.


#### https://www.houseofdiams.com/engagement-rings

- Reduce unused JavaScript: Est savings of 209 KiB.
- Improve image delivery: Est savings of 50 KiB.
- Use efficient cache lifetimes: Est savings of 154 KiB.


#### https://www.houseofdiams.com/shop/rosette-five-flower-bracelet

- Reduce unused JavaScript: Est savings of 213 KiB.
- Improve image delivery: Est savings of 484 KiB.
- Use efficient cache lifetimes: Est savings of 493 KiB.


#### https://www.houseofdiams.com/bespoke

- Reduce unused JavaScript: Est savings of 214 KiB.
- Improve image delivery: Est savings of 32 KiB.
- Use efficient cache lifetimes: Est savings of 241 KiB.


#### https://www.houseofdiams.com/blog

- Reduce unused JavaScript: Est savings of 214 KiB.
- Use efficient cache lifetimes: Est savings of 114 KiB.
- Render-blocking requests: Est savings of 180 ms.


#### https://www.houseofdiams.com/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide

- Reduce unused JavaScript: Est savings of 250 KiB.
- Improve image delivery: Est savings of 62 KiB.
- Use efficient cache lifetimes: Est savings of 149 KiB.
- Render-blocking requests: Est savings of 230 ms.


#### https://www.houseofdiams.com/cart

- Reduce unused JavaScript: Est savings of 321 KiB.
- Use efficient cache lifetimes: Est savings of 68 KiB.
- Render-blocking requests: Est savings of 240 ms.


#### https://www.houseofdiams.com/login

- Reduce unused JavaScript: Est savings of 331 KiB.
- Improve image delivery: Est savings of 62 KiB.
- Use efficient cache lifetimes: Est savings of 17 KiB.


#### https://www.houseofdiams.com/checkout?mode=cart

- Reduce unused JavaScript: Est savings of 233 KiB.
- Use efficient cache lifetimes: Est savings of 76 KiB.
- Render-blocking requests: Est savings of 230 ms.


### Validation after developer changes

Repeat the same presets against the same routes, preferably three runs per route with the median reported; separately capture field telemetry. Verify populated cart/checkout in a staging test-payment environment. Recheck visual fidelity, video/gallery operation, promo behavior and third-party requirements after delivery changes. No performance fixes were made during this audit.

### Repeatable lab command templates

The original runs used the official npm Lighthouse CLI. For a reproducible follow-up, pin the observed version 13.5.0 and use a fresh isolated browser profile per sample. The examples below are retest templates, not commands executed during this consolidation. Replace URL with one of the nine live URLs in the measured table. Mobile is the default preset; desktop adds the desktop preset. Output files are only for a future authorised retest.

```bash
npm exec --yes --package=lighthouse@13.5.0 -- lighthouse "URL" --chrome-flags="--headless --disable-gpu" --output=json --output=html --output-path="mobile-result" --quiet
npm exec --yes --package=lighthouse@13.5.0 -- lighthouse "URL" --chrome-flags="--headless --disable-gpu" --output=json --output=html --output-path="desktop-result" --preset=desktop --quiet
```

### Preserved lab settings

Lighthouse 13.5.0, HeadlessChrome 154, axe-core 4.13.0. These are simulated lab configurations, not physical-device measurements. Mobile used the Moto G Power simulation; desktop used the desktop preset. Cart/checkout lab states were empty isolated sessions.

#### Mobile settings

```json
{
  "formFactor": "mobile",
  "throttlingMethod": "simulate",
  "throttling": {
    "rttMs": 150,
    "throughputKbps": 1638.4,
    "requestLatencyMs": 562.5,
    "downloadThroughputKbps": 1474.5600000000002,
    "uploadThroughputKbps": 675,
    "cpuSlowdownMultiplier": 4
  },
  "screenEmulation": {
    "mobile": true,
    "width": 412,
    "height": 823,
    "deviceScaleFactor": 1.75,
    "disabled": false
  }
}
```

#### Desktop settings

```json
{
  "formFactor": "desktop",
  "throttlingMethod": "simulate",
  "throttling": {
    "rttMs": 40,
    "throughputKbps": 10240,
    "requestLatencyMs": 0,
    "downloadThroughputKbps": 0,
    "uploadThroughputKbps": 0,
    "cpuSlowdownMultiplier": 1
  },
  "screenEmulation": {
    "mobile": false,
    "width": 1350,
    "height": 940,
    "deviceScaleFactor": 1,
    "disabled": false
  }
}
```

### Original run timestamps

| Page / mode | Live URL | Run timestamp UTC | Benchmark index |
| --- | --- | --- | --- |
| article-desktop | [https://www.houseofdiams.com/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide](https://www.houseofdiams.com/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide) | 2026-10-05T13:58:54.769Z | 754.5 |
| article-mobile | [https://www.houseofdiams.com/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide](https://www.houseofdiams.com/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide) | 2026-10-05T13:58:14.854Z | 739 |
| bespoke-desktop | [https://www.houseofdiams.com/bespoke](https://www.houseofdiams.com/bespoke) | 2026-10-05T13:54:52.331Z | 734.5 |
| bespoke-mobile | [https://www.houseofdiams.com/bespoke](https://www.houseofdiams.com/bespoke) | 2026-10-05T13:54:05.839Z | 749 |
| blog-desktop | [https://www.houseofdiams.com/blog](https://www.houseofdiams.com/blog) | 2026-10-05T13:56:56.587Z | 712.5 |
| blog-mobile | [https://www.houseofdiams.com/blog](https://www.houseofdiams.com/blog) | 2026-10-05T13:56:03.661Z | 697 |
| cart-desktop | [https://www.houseofdiams.com/cart](https://www.houseofdiams.com/cart) | 2026-10-05T14:00:27.293Z | 994 |
| cart-mobile | [https://www.houseofdiams.com/cart](https://www.houseofdiams.com/cart) | 2026-10-05T13:59:54.575Z | 1052.5 |
| checkout-desktop | [https://www.houseofdiams.com/checkout?mode=cart](https://www.houseofdiams.com/checkout?mode=cart) | 2026-10-05T14:03:13.130Z | 746.5 |
| checkout-mobile | [https://www.houseofdiams.com/checkout?mode=cart](https://www.houseofdiams.com/checkout?mode=cart) | 2026-10-05T14:02:17.104Z | 776 |
| collection-desktop | [https://www.houseofdiams.com/engagement-rings](https://www.houseofdiams.com/engagement-rings) | 2026-10-05T13:49:07.917Z | 808.5 |
| collection-mobile | [https://www.houseofdiams.com/engagement-rings](https://www.houseofdiams.com/engagement-rings) | 2026-10-05T13:47:40.338Z | 700 |
| home-desktop | [https://www.houseofdiams.com/](https://www.houseofdiams.com/) | 2026-10-05T14:06:14.840Z | 2431 |
| home-mobile | [https://www.houseofdiams.com/](https://www.houseofdiams.com/) | 2026-10-05T13:43:31.187Z | 2750 |
| login-desktop | [https://www.houseofdiams.com/login](https://www.houseofdiams.com/login) | 2026-10-05T14:01:43.408Z | 718.5 |
| login-mobile | [https://www.houseofdiams.com/login](https://www.houseofdiams.com/login) | 2026-10-05T14:01:16.958Z | 1115.5 |
| product-desktop | [https://www.houseofdiams.com/shop/rosette-five-flower-bracelet](https://www.houseofdiams.com/shop/rosette-five-flower-bracelet) | 2026-10-05T13:52:10.739Z | 756 |
| product-mobile | [https://www.houseofdiams.com/shop/rosette-five-flower-bracelet](https://www.houseofdiams.com/shop/rosette-five-flower-bracelet) | 2026-10-05T13:50:39.898Z | 811 |

## Navigation and resources

Initial crawl: **308 unique internal URLs, all HTTP 200**; 28,249 recorded server-HTML link occurrences. These repeated occurrences share destinations and were resolved by the unique-URL crawl. No 500 or redirect loop was observed in that set. Additional JavaScript search navigation found a genuine 404. Deliberately invalid QA paths also returned proper 404s and are not bugs.

| Source URL | Link text | Destination | HTTP / behavior | Issue | Severity / ID |
| --- | --- | --- | --- | --- | --- |
| https://www.houseofdiams.com/ | Fine Jewellery Test Product | https://www.houseofdiams.com/shop/fine-jewellery-test-product | 404 twice; visible error page | Unavailable product promoted by search | P2 / BUG-020 — Developer |
| https://www.houseofdiams.com/login | Forgot your password? | https://www.houseofdiams.com/login | 200, self-link | No recovery flow | P2 / BUG-003 — Developer |
| https://www.houseofdiams.com/ and multiple templates | Chat with us / WhatsApp | https://wa.me/91?text=… | Incomplete recipient; destination chat not submitted | Missing subscriber number after hydration | P2 / BUG-004 — Developer |
| https://www.houseofdiams.com/ and contact panels | Admin@houseofdiams.com | mailto:info@houseofdiams.com | Not an HTTP link; no email sent | Displayed and actual recipients disagree | P3 / BUG-012 — Developer |
| https://www.houseofdiams.com/returns | Returns | /returns | 200; wrong policy content | Return terms unavailable | P2 / BUG-006 — Client |

Reproduction steps, expected/actual behavior and affected locations are in [Full report](#bugs); the recorded observations are included here. HTTP reachability alone does not validate destination correctness.

### Resource sweep

| Result | Count |
| --- | --- |
| 200 | 1539 |
| 400 | 2 |
| 429 | 1 |

Checked 1542 unique asset/external destinations using read-only HEAD, with GET rechecks for failures. Sixteen URLs initially failed because the QA script had not percent-encoded spaces; **all 16 passed once correctly encoded**. These environment/checker errors are excluded from bugs. Two Supabase SVGs remained 400 on two GET attempts each (BUG-015 — Developer). The external advertising opt-out destination returned 429 and needs a later external-service check; it is not asserted as a site 404. No failed first-party JS/CSS/font URL remained in the effective sweep.

| Affected source pages | Asset destination | Repeated GET status | ID |
| --- | --- | --- | --- |
| /hiphop/chains; /hiphop/chains/cuban-links; /hiphop/test-subcat | https://ztvqqgisjlswztrcosgk.supabase.co/storage/v1/object/public/hod/catalog/options/004-battery-low.svg | 400 / 400 | BUG-015 — Developer |
| /hiphop/chains; /hiphop/chains/cuban-links | https://ztvqqgisjlswztrcosgk.supabase.co/storage/v1/object/public/hod/catalog/subcategories/005-approximate-equals.svg | 400 / 400 | BUG-015 — Developer |

External Instagram and Pinterest links were checked for public HTTP reachability and destination structure; authenticated social actions were not performed. Email/telephone destinations were inspected without sending messages or placing calls. Instagram iframe interactions, liking, sharing and commenting were not clicked because they would affect external accounts or communications.

### Recovery checks

Deliberately invalid QA paths returned 404 pages with recovery links. The unavailable product suggested by Search remains BUG-020 — Developer. Crafted invalid paths are not bugs.

### Console and network interpretation

One incorrect synthetic login produced an expected authentication error. ObjectMultiplex/MaxListeners warnings came from the browser environment and were excluded from site bugs. No customer-flow fatal exception or hydration failure was established in the captured manual logs. Lighthouse recorded Pinterest report-only CSP warnings and an ignored report-only upgrade-insecure-requests directive; these do not prove that a purchase resource was blocked. No intrusive security testing or protected-data access was performed.

## Accessibility

### BUG-005 — Developer fix

With the mobile menu closed, Tab moved from the visible header into eleven invisible menu controls. Two keyboard checks reproduced this. Customers cannot see what is selected. Closed menu items should not receive keyboard focus; verify opening, closing and focus restoration after the fix.

### Other tested interactions

Contact modal: 18 consecutive keyboard stops stayed inside; Escape closed it. Product viewer and size guide: Escape closed them. Search: ArrowDown/Enter selected a suggestion and Escape closed search. Checkout: required/invalid fields displayed errors; spoken announcements were not verified.

### Original automated scores

These measurements do not add other bugs to the selected work list.

| Lab state | Accessibility score |
| --- | --- |
| article-desktop | 96 |
| article-mobile | 96 |
| bespoke-desktop | 91 |
| bespoke-mobile | 90 |
| blog-desktop | 96 |
| blog-mobile | 96 |
| cart-desktop | 96 |
| cart-mobile | 96 |
| checkout-desktop | 100 |
| checkout-mobile | 100 |
| collection-desktop | 96 |
| collection-mobile | 91 |
| home-desktop | 92 |
| home-mobile | 92 |
| login-desktop | 100 |
| login-mobile | 100 |
| product-desktop | 89 |
| product-mobile | 88 |

### Limits and evidence

This is not an accessibility compliance certificate. No screen-reader speech pass, physical-device test or Safari/Firefox keyboard regression was available. Actual 200% zoom remains unverified. Empty checkout/cart lab scores do not validate populated flows.

## Responsive

Original Chrome viewport emulation: 1920×1080, 1440×900, 1024×1366, 768×1024, 430×932, 390×844, 375×812 and 844×390 landscape. Representative product, collection, cart, checkout, form and content pages were also inspected at desktop and 375/390-pixel mobile widths. These are inspection sizes, not a claim that every layout passed.

### Selected issues

| Bug | Fix Owner | Issue |
| --- | --- | --- |
| BUG-002 | Developer | Delivery line prices use USD numbers with an INR symbol |
| BUG-003 | Developer | Forgot-password link returns to the login page |
| BUG-004 | Developer | Hydrated WhatsApp links omit the business phone number |
| BUG-005 | Developer | Closed mobile navigation remains in the keyboard tab order |
| BUG-008 | Developer | Shopping pages have slow main-content rendering and heavy blocking work |
| BUG-009 | Developer | Bracelet length is absent from cart and checkout review; cart shows a ring size |
| BUG-015 | Developer | Two public HipHop category SVGs return HTTP 400 |


### Limits

Physical touch/rotation, on-screen keyboard overlap, Safari safe areas, actual 200% zoom and payment overlays remain unverified. Viewport overrides were reset.  · [Functional matrix](#test-results).

## Test results

All 125 retained test cases are included below. Original FT numbers are unchanged; gaps are intentional. Removed cases were not reclassified as passes. PASSED concerns only the exact case; PARTIAL, NEEDS VERIFICATION and test limits are not full-feature passes. NOT APPLICABLE is scoped to observed samples.

| Status | Cases |
| --- | --- |
| PASSED | 61 |
| FAILED | 15 |
| NOT TESTABLE | 3 |
| PARTIAL | 25 |
| NEEDS VERIFICATION | 4 |
| NOT TESTED | 3 |
| NOT APPLICABLE | 4 |
| NOT SAFELY TESTABLE | 10 |

| Feature | Test Case | Expected Result | Actual Result | Status | Severity | Bug ID | Fix Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Inventory | FT-001 — Sitemap and recursive public crawl | Reachable public destinations | 256 sitemap entries; 308 unique URL variants all returned 200 | PASSED | — | — | — |
| Inventory | FT-002 — Dynamic UI discovery | Include client-generated routes | Search exposed an additional unpublished 404 product | FAILED | P2 | BUG-020 | Developer |
| Navigation | FT-003 — Header/mobile menu opens | Usable menu | Menu and nested Engagement Rings choices opened | PASSED | — | — | — |
| Navigation | FT-004 — Mobile category selection | Close overlay and navigate | Shop All selection closed menu and loaded Engagement Rings | PASSED | — | — | — |
| Navigation | FT-005 — Desktop keyboard header sequence | Visible controls only | Closed mobile menu descendants took focus | FAILED | P2 | BUG-005 | Developer |
| Navigation | FT-006 — Desktop hover/mega-menu state | All hover targets usable | Hover automation not available; no complete hover pass claimed | NOT TESTABLE | — | — | — |
| Navigation | FT-007 — Sticky/scrolling header | Usable navigation while scrolling | Header/navigation snapshots inspected; exhaustive scroll threshold behavior not recorded | PARTIAL | — | — | — |
| Navigation | FT-008 — Cart icon/drawer | Open current cart | Drawer displayed current merchandise | PASSED | — | — | — |
| Navigation | FT-009 — Search icon and Escape | Open/close search | Search opened; Escape removed the search overlay | PASSED | — | — | — |
| Navigation | FT-010 — Account access | Account sign-in path | Login and unauthenticated profile/orders guards rendered | PASSED | — | — | — |
| Footer | FT-011 — All discovered destination reachability | Links resolve | Policy, category and informational destinations returned 200; correctness exceptions tracked | PARTIAL | — | — | — |
| Footer | FT-012 — Mobile support expansion | Expose policy links | Native accessibility action expanded Support and revealed FAQ/shipping/returns/terms/privacy | PASSED | — | — | — |
| Footer | FT-013 — Support email recipient | Text matches mailto | Admin label targets info mailbox | FAILED | P3 | BUG-012 | Developer |
| Footer | FT-014 — WhatsApp recipient after hydration | Full business number | wa.me/91 lacks subscriber number | FAILED | P2 | BUG-004 | Developer |
| Footer | FT-015 — Telephone/social destinations | Correct callable/social URLs | tel number correct; Instagram/Pinterest HTTP destinations checked; no calls/messages | PASSED | — | — | — |
| Footer | FT-016 — Country/currency control | Consistent supported selection | INR active earlier; later disabled USD-only fallback appeared | NEEDS VERIFICATION | — | — | — |
| Homepage | FT-017 — Hero/category/collection links | Correct destinations | Destinations crawled; representative linked pages loaded | PARTIAL | — | — | — |
| Homepage | FT-020 — Recommendation quiz happy path | Return matched shopping route | Rings → Budget → Under $1,000 → Shop This Match opened type=ring&price=0-1000 | PASSED | — | — | — |
| Homepage | FT-021 — Recommendation quiz all modules | All metal/shape/style/budget branches | Budget completed; saved previous match and Style entry inspected; exhaustive branches not run | PARTIAL | — | — | — |
| Homepage | FT-022 — Embedded Instagram playback/social actions | Usable embeds | Embeds rendered; exhaustive playback/social actions not performed | PARTIAL | — | — | — |
| Collections | FT-023 — Fine jewellery/wedding/T-bar content | Render listings | Representative desktop/mobile listings inspected | PASSED | — | — | — |
| Collections | FT-024 — Mobile shape filter | Reduce results and preserve URL | Pear filter changed 61 engagement pieces to 8 with shape=pear | PASSED | — | — | — |
| Collections | FT-025 — Price low-to-high sorting | Ascending prices | Eight pear results sorted ascending and URL included sort=price-low | PASSED | — | — | — |
| Collections | FT-026 — Filtered URL refresh | Retain selections | shape=pear&sort=price-low survived refresh; loaded values observed | PASSED | — | — | — |
| Collections | FT-027 — Load More | Append products | Fine Jewellery increased 24 to 48 cards; remaining count changed 88→64 | PASSED | — | — | — |
| Collections | FT-028 — Shop pagination Next/Back/Forward | Correct page state | Page 2 of 8 loaded; back restored page 1; forward restored page 2 | PASSED | — | — | — |
| Collections | FT-029 — Empty collection and clear filters | Recoverable empty state | Showcase /collection had 0 pieces with no active filters; clear retained truthful empty state | PASSED | — | — | — |
| Collections | FT-030 — Desktop Shape click after expansion | Expose choices | One run did not expose choices; mobile worked; hover/loading not ruled out | NEEDS VERIFICATION | — | — | — |
| Collections | FT-033 — HipHop category image resources | Successful image load | Two SVGs 400 twice and completed broken images | FAILED | P3 | BUG-015 | Developer |
| Products | FT-034 — Representative bracelet/ring/necklace/earring render | Correct controls/media/details | Rosette, Amara, Camille and Adeline samples inspected; most controls rendered | PASSED | — | — | — |
| Products | FT-035 — Metal selector and ring size | Show selected option | Amara 14K White Gold and US 7 selected; product price changed | PASSED | — | — | — |
| Products | FT-037 — Bracelet length review | Selected length visible in cart/checkout | 7 / 7.5 inch choice omitted; unrelated US 4 in cart | FAILED | P3 | BUG-009 | Developer |
| Products | FT-038 — Image viewer Next and Escape | Advance and dismiss | Amara viewer changed 1/5→2/5; Escape closed it | PASSED | — | — | — |
| Products | FT-039 — T-bar gallery image/video switching | Select media and play video | Image selection switched; video 1 entered playing state without media error observed | PASSED | — | — | — |
| Products | FT-040 — Size guide and How to Measure tab | Show readable guide/instructions | Guide opened, measurement tab showed instructions at 375 px, Escape closed | PASSED | — | — | — |
| Products | FT-041 — Wishlist add/refresh/remove | Persist and remove selected item | Camille persisted after refresh; removing restored empty wishlist | PASSED | — | — | — |
| Products | FT-042 — Wishlist final cleanup | Preserve baseline | Original empty wishlist remained empty | PASSED | — | — | — |
| Products | FT-043 — Optional love letter skip | Allow purchase entry without message | Skip for now added QA line or entered Buy Now preview | PASSED | — | — | — |
| Products | FT-044 — Gift messaging full field boundaries | Preserve text/customization | Optional dialog inspected; complete long-message/rapid entry regression not recorded | PARTIAL | — | — | — |
| Products | FT-045 — Incomplete/invalid variant | Reject unsupported selection | Samples default to valid choices; invalid identifiers not injected | NOT TESTED | — | — | — |
| Products | FT-046 — Out-of-stock/backorder | Clear inventory behavior | No suitable sample state discovered on selected products | NOT APPLICABLE | — | — | — |
| Products | FT-047 — Reviews/engraving | Usable dedicated controls | Not exposed on selected samples; catalog-wide absence not asserted | NOT APPLICABLE | — | — | — |
| Search | FT-048 — Exact/partial/case query suggestions | Relevant safe results | Exact Rosette, rosette and uppercase query paths inspected; matching product found | PARTIAL | — | — | — |
| Search | FT-049 — Submitted mobile Rosette result | Show matching product | One Rosette result loaded | PASSED | — | — | — |
| Search | FT-050 — Generic diamond/misspelling | Graceful suggestions/results | Suggestion boundary cases inspected; exhaustive relevance ranking not scored | PARTIAL | — | — | — |
| Search | FT-051 — No-results submission | Understandable recovery | 0 products; Try another term message | PASSED | — | — | — |
| Search | FT-052 — Special characters | Safe rendering and no crash | &<> quote query rendered as text and returned fallback products; no execution observed | PARTIAL | — | — | — |
| Search | FT-053 — Very long query | Handle boundary safely | 300-character input exercised in suggestion tests; full submitted result not separately verified | PARTIAL | — | — | — |
| Search | FT-054 — Empty search | Available suggestions | 16 suggestions included unavailable test item | FAILED | P2 | BUG-020 | Developer |
| Search | FT-055 — ArrowDown/Enter selection | Select suggestion and search | Rosette suggestion selected and matching submitted result loaded | PASSED | — | — | — |
| Search | FT-056 — Search pagination | Navigate paginated results | Observed search is a result panel; no pagination control exposed in tested queries | NOT APPLICABLE | — | — | — |
| Cart | FT-057 — Add QA variant | Create one customer bag line | Added white-gold Rosette after Skip for now | PASSED | — | — | — |
| Cart | FT-058 — Quantity increase/decrease | Update quantity and totals | QA quantity 1→2→1; totals recomputed; no order submitted | PASSED | — | — | — |
| Cart | FT-059 — Decrease at quantity one | Safe nonnegative cart state | Independent one-line cart returned to empty; no negative quantity | PASSED | — | — | — |
| Cart | FT-060 — Arbitrary quantity/max stock boundary | Reject invalid/out-of-range values | Stepper only observed; no free quantity field or maximum-stock test executed | NOT TESTED | — | — | — |
| Cart | FT-061 — Refresh persistence | Retain bag contents | Test variant and existing lines survived refresh | PASSED | — | — | — |
| Cart | FT-062 — Remove QA line | Remove only QA addition | White-gold line removed; original two lines preserved | PASSED | — | — | — |
| Cart | FT-063 — Empty state and continue shopping | Recover to catalog | Independent empty bag showed Explore Products; link was activated | PASSED | — | — | — |
| Cart | FT-064 — Subtotal arithmetic | Match lines and quantities | Original USD merchandise subtotal $335+$1,515=$1,850; INR conversion/rounding differed with live FX | PASSED | — | — | — |
| Cart | FT-065 — Original state preservation | Leave original bag intact | Yellow Rosette and Asteria stayed quantity 1; QA white line gone; automatic gift remained | PASSED | — | — | — |
| Cart | FT-066 — Variant Edit workflow | Preserve editing and updates | Edit destinations observed; full editing replacement sequence not executed | PARTIAL | — | — | — |
| Checkout | FT-067 — Cart checkout entry | Load customer information form | Populated cart mode loaded in desktop/mobile | PASSED | — | — | — |
| Checkout | FT-068 — Buy Now entry | Preview selected product safely | Direct single-product checkout URL loaded after optional message skip | PASSED | — | — | — |
| Checkout | FT-069 — Empty required fields | Block with specific errors | Email/name/phone/address/postal/city/state/country errors displayed | PASSED | — | — | — |
| Checkout | FT-070 — Invalid email/phone/postal | Reject invalid formats | not-an-email, abc phone and !@# postal produced inline errors | PASSED | — | — | — |
| Checkout | FT-071 — India postal lookup | Resolve valid location | 395007 populated Surat / Gujarat / India and allowed shipping review | PASSED | — | — | — |
| Checkout | FT-072 — US postal lookup | Resolve supported international address | Early failure; independent retest populated New York / United States | NEEDS VERIFICATION | — | — | — |
| Checkout | FT-073 — Shipping method | Present available choice/cost | Complimentary insured overnight/signature method shown; no alternative selector exposed | PARTIAL | — | — | — |
| Checkout | FT-074 — Tax and total arithmetic | Internally consistent quote | Observed ₹1,78,156 subtotal + ₹21,379 tax = ₹1,99,535; jurisdiction/rate correctness not validated | PARTIAL | — | — | — |
| Checkout | FT-075 — Line-item currency | Consistent line and summary currency | Raw USD numbers presented with INR symbol in Delivery | FAILED | P2 | BUG-002 | Developer |
| Checkout | FT-076 — Expanded order review options | Show selected customization | Expanded Buy Now summary omitted bracelet length | FAILED | P3 | BUG-009 | Developer |
| Checkout | FT-077 — Invalid coupon | Reject with clear message | QA_INVALID_20261005 rejected as invalid/inactive; loading button disabled while checking | PASSED | — | — | — |
| Checkout | FT-078 — Valid coupon and gift eligibility | Apply approved business rules | Offer state observed, but full valid-code boundary/eligibility regression not executed | PARTIAL | — | — | — |
| Checkout | FT-079 — Continue to shipping review | Display editable information before payment | India address reached shipping review with Edit / Continue to Payment | PASSED | — | — | — |
| Checkout | FT-080 — Edit/back navigation | Return to editable step/product/cart | Edit retained entered data; Back returned to cart/product | PASSED | — | — | — |
| Checkout | FT-081 — Refresh state | Recover safe checkout | Refresh cleared entered address; product/cart state remained. Persistence requirement not established | PARTIAL | — | — | — |
| Checkout | FT-082 — Server pricing error recovery | Block unconfirmed price | Independent white-gold preview showed quote-unavailable banner; no payment attempted | NEEDS VERIFICATION | — | — | — |
| Checkout | FT-083 — Continue to Payment / Razorpay | Use safe test order/payment only | Public bundle calls /api/checkout/place before opening gateway; action not clicked | NOT SAFELY TESTABLE | — | — | — |
| Checkout | FT-084 — Payment decline/cancel/success/confirmation | Test controlled transaction outcomes | No sandbox exposed; requires a real order/payment | NOT SAFELY TESTABLE | — | — | — |
| Account | FT-085 — Login empty/invalid email | Block invalid input | Required/email checks blocked invalid inputs | PASSED | — | — | — |
| Account | FT-086 — Incorrect synthetic credentials | Clear login error | One reserved example.com login attempt returned incorrect-email/password message | PASSED | — | — | — |
| Account | FT-087 — Password Show/Hide | Intentional visibility toggle | Show/Hide worked; dummy values cleared | PASSED | — | — | — |
| Account | FT-088 — Registration empty/invalid email | Block required/format failures | Required fields and invalid email blocked; no account created | PASSED | — | — | — |
| Account | FT-089 — Short password | Enforce advertised requirement | short violated password pattern and could not submit; fields cleared | PASSED | — | — | — |
| Account | FT-090 — Password mismatch/duplicate email | Block and explain safely | No final otherwise-valid account submission performed | NOT SAFELY TESTABLE | — | — | — |
| Account | FT-091 — Valid signup/login/session/logout | Operate with approved test account | No approved account/credentials supplied; no production account created | NOT SAFELY TESTABLE | — | — | — |
| Account | FT-092 — Forgot password link | Show recovery flow | Self-link to /login | FAILED | P2 | BUG-003 | Developer |
| Account | FT-093 — Reset email and new password | Verify recovery safely | Recovery UI unreachable; no email or credential change attempted | NOT SAFELY TESTABLE | — | — | — |
| Account | FT-094 — Unauthenticated profile/orders | Protect account data | Sign-in prompt; no profile/order data exposed | PASSED | — | — | — |
| Account | FT-095 — Authenticated profile/orders/addresses | Correct authorized customer details | No signed-in test account; not inspected | NOT SAFELY TESTABLE | — | — | — |
| Contact | FT-096 — Empty and invalid-email submit | Block contact request | Required name/email/message and invalid email prevented submission | PASSED | — | — | — |
| Contact | FT-097 — Long text/special characters/whitespace | Safe text and validation | Long <>& message and whitespace name entered with invalid email retained; final success not sent | PARTIAL | — | — | — |
| Contact | FT-098 — Optional phone format | Clear optional validation behavior | abc entered but email prevented final submit; no phone server-validation conclusion | PARTIAL | — | — | — |
| Contact | FT-099 — Topic selection | Select requested enquiry topic | Bespoke Order selection worked | PASSED | — | — | — |
| Contact | FT-100 — Focus trap/Escape | Keep keyboard focus in modal and dismiss | 18 consecutive stops remained inside; Escape closed | PASSED | — | — | — |
| Contact | FT-101 — Valid/rapid/duplicate submission and success | Single controlled enquiry delivery | Would contact a real team; no production success/rapid-submit tests | NOT SAFELY TESTABLE | — | — | — |
| Bespoke | FT-102 — Empty and invalid email | Block incomplete enquiry | Vision/required/email checks prevented final request | PASSED | — | — | — |
| Bespoke | FT-103 — Piece type / FAQ interaction | Select type and expand answer | Engagement Ring selected; reference-image FAQ expanded | PASSED | — | — | — |
| Bespoke | FT-105 — Upload/success/duplicate-submit | Controlled reference/inquiry processing | No upload or final real-team enquiry; outcome not tested | NOT SAFELY TESTABLE | — | — | — |
| Promotion | FT-106 — Empty first name / required age | Reject missing step answers | Valid-first-name and age selection errors displayed | PASSED | — | — | — |
| Promotion | FT-107 — Invalid email step | Stop invalid address | invalid advanced to step 3 twice | FAILED | P3 | BUG-010 | Developer |
| Promotion | FT-108 — Wizard navigation / mobile layout | Navigate without clipping | Seven steps explored; final timing step inspected at 390 px; previous navigation worked | PASSED | — | — | — |
| Promotion | FT-109 — Reveal code / marketing subscription | Controlled lead/consent test | Reveal not submitted; marketing checkbox left unchecked | NOT SAFELY TESTABLE | — | — | — |
| Content | FT-110 — Blog/article desktop/mobile rendering | Readable article and navigation | Representative listing/article/education pages inspected | PASSED | — | — | — |
| Content | FT-111 — Article Back to Journal | Return to listing | Returned to /blog in independent session | PASSED | — | — | — |
| Content | FT-112 — Blog alphabetical sort | Order articles by title | Title A-Z moved 14K vs 18K Gold first | PASSED | — | — | — |
| Content | FT-114 — All article filters/share/pagination | Usable complete content navigation | Destination crawl broad; exhaustive content-filter/share actions not executed | PARTIAL | — | — | — |
| Policies | FT-115 — Returns information | Actual approved return terms | Legitimacy FAQ instead; 15/30-day conflict | FAILED | P2 | BUG-006 | Client |
| Policies | FT-116 — Shipping / trust copy | Final customer content | Test shipping block and new-pointer trust text | FAILED | P3 | BUG-013 | Client |
| Policies | FT-117 — Privacy / terms readability | Accessible policy content | Desktop/mobile rendered without root overflow; legal adequacy not assessed | PASSED | — | — | — |
| Responsive | FT-119 — Mobile major page types | No horizontal root overflow | Captured ring/earrings/cart/checkout/forms/content/policies at 375/390; detailed coverage in responsive report | PARTIAL | — | — | — |
| Browsers | FT-120 — Independent Chromium session | Basic alternate-session behavior | Empty cart, Buy Now, coupon, US lookup, article and recommendation path exercised | PARTIAL | — | — | — |
| Browsers | FT-121 — Safari desktop/mobile, Firefox, Edge | Cross-engine compatibility | Not connected; not represented as passes | NOT TESTABLE | — | — | — |
| Accessibility | FT-124 — Icon naming / alt / headings / errors | Meaningful semantics | Sampled automated/manual checks; major named controls work; exhaustive screen-reader pass not performed | PARTIAL | — | — | — |
| Accessibility | FT-125 — 200% browser zoom | Verify reflow at actual 200% | Native shortcuts under viewport override did not change measured scale; no zoom pass claimed | NOT TESTABLE | — | — | — |
| Console | FT-126 — Fatal exceptions/hydration failures | No customer-flow fatal error | None established in captured manual logs; known invalid-login error expected | PARTIAL | — | — | — |
| Console | FT-127 — Third-party CSP warnings | Distinguish warning from blocking | Report-only Pinterest/CSP messages in Lighthouse; not evidence of blocked purchase | PARTIAL | — | — | — |
| Network | FT-128 — Images/JS/CSS/fonts/external HEAD sweep | Successful assets | 1,542 destinations checked; 2 real SVG failures; 16 checker-encoding errors corrected | FAILED | P3 | BUG-015 | Developer |
| Performance | FT-129 — Nine pages × two modes | Measured meaningful lab results | 18 valid results; slow mobile LCP and product video | FAILED | P2 | BUG-008 | Developer |
| Errors | FT-130 — Deliberate invalid URLs | 404 and recovery path | Two QA paths returned actual 404 and understandable page copy | PASSED | — | — | — |
| Errors | FT-131 — Offline/failed API injection/expired session | Recover safely without data loss | Not fault-injected in production; no authenticated session available | NOT TESTED | — | — | — |
| Security adjacent | FT-132 — Password visibility/account guard/HTTPS | No obvious customer exposure | Passwords masked except intentional toggle; unauthenticated account/orders guarded; TLS verified | PARTIAL | — | — | — |
| Security adjacent | FT-133 — Intrusive security/URL price tampering | Outside authorized QA scope | No exploitation or protected-data probes | NOT APPLICABLE | — | — | — |
| Exploratory | FT-134 — Repeated menu/step/quantity/image interactions | Stable state | Quantity reversal, quiz Back/Next, image-dot repeats, gallery/size guide Escape and refresh performed | PARTIAL | — | — | — |
| Exploratory | FT-135 — Rapid purchase/form submission / physical gestures | Controlled state testing | Rapid submissions not attempted; physical touch gestures unavailable | NOT SAFELY TESTABLE | — | — | — |

### Phase coverage and remaining limits

| Requested phase | Coverage / limit |
| --- | --- |
| 1. Website inventory | Broad sitemap and recursive GET inventory plus representative JavaScript states |
| 2. Broken links | All discovered server-link destinations checked; dynamic search 404 identified; social actions not performed |
| 3. Header | Mobile nesting/selection and keyboard sequence; exhaustive desktop hover unavailable |
| 4. Footer | Link destinations and support expansion; contact destinations inspected without messaging |
| 5. Homepage | Layout, linked pages, recommendation/promotion flows; embedded social actions and every animation not exhaustively tested |
| 6. Product/collection | Four product types, gallery/size, metal/length, wishlist, filter/sort/load-more/pagination; stock/invalid identifier permutations not injected |
| 7. Search | Boundary suggestions and representative submitted results; full long-query/relevance ranking remains partial |
| 8. Cart | Reversible add/quantity/refresh/remove/empty with baseline preserved; max-stock boundary not tested |
| 9. Accounts | Public invalid validation/guard paths; valid authenticated operations need test account |
| 10. Forms | Every discovered form family inspected safely; production delivery/duplicate-submit not tested |
| 11. Checkout | Shipping review reached; stopped before production order-placement call |
| 12. Responsive | All requested homepage dimensions; representative mobile page types; physical gestures unavailable |
| 13. Cross-browser | Chrome plus independent Chromium session; other engines not connected |
| 14. Visual | Important page types inspected; missing category assets in the selected scope; no subjective brand defects |
| 15. Console | Manual and lab logs captured; environment and report-only warnings separated |
| 16. Network | 1,542 public asset/external destinations plus saved Lighthouse network records; authenticated API faults not injected |
| 17. Performance | All nine requested page types × both modes; no field INP/CrUX result available |
| 18. Accessibility | Automated plus actual sequential keyboard/modal tests; no WCAG certification or physical assistive session |
| 19. Error states | 404, search, invalid login/forms/coupon, empty cart, guards; no offline fault injection |
| 20. History/state | Cart/filter/wishlist refresh, shop Back/Forward, checkout Edit/Back/refresh; authenticated state unavailable |
| 21. Security-adjacent | Normal masks/guards/TLS only; no penetration testing |
| 22. SEO quality only | HTTP/404/navigation checked; SEO score recorded without SEO-strategy recommendations |
| 23. Exploratory | Repeated reversible interactions, boundaries, alternate session, orientation; no rapid financial/lead actions |


Cross-reference [checkout and accounts](#checkout-and-accounts) for external-effect limits and [actions and retesting](#actions-and-retesting) for controlled follow-up. The full requested scope is mapped here; it is not represented as fully executed where safety or capabilities prevented testing.

## Page inventory

| Coverage | Count |
| --- | --- |
| Sitemap URL entries | 256 |
| Crawled unique internal URL variants | 308 |
| Recorded server-HTML link occurrences | 28249 |
| Saved UI observations | 96 |
| Distinct URLs with saved UI observations | 35 |
| Distinct UI paths | 30 |
| Inventory rows including extra browser/error cases | 316 |
| Valid Lighthouse audits | 18 |

The complete page inventory is included below with URL, type, HTTP status, desktop/mobile coverage, functional status, selected issues and owners. “Yes” indicates at least one saved observation at that exact URL/width class, **not exhaustive testing of every interaction**. Most product/category URLs have HTTP-only coverage. A successful HTTP response is not a functional pass. Query variants are separate rows. Product Buy Now parameters contain product-option data only.

### Discovered functionality

| Feature | Exists? | Coverage |
| --- | --- | --- |
| Desktop / responsive mobile navigation | Yes | Chrome viewport tests; menu nesting, close and selection; hidden tab-order defect |
| Authentication / registration / account | Yes | Public validation and unauthenticated profile/orders guards; no created account |
| Forgot password | UI link exists | Failed link; no reset flow reached |
| Logout / authenticated orders / addresses | Requires signed-in state | NOT SAFELY TESTABLE without approved test account |
| Cart / Buy Now / checkout | Yes | Reversible QA cart operations and safe shipping review; stopped before order creation |
| Wishlist | Yes | Add, refresh persistence, remove, empty restored |
| Search | Yes | Suggestions and submitted result states; one broken unpublished suggestion |
| Collection filters / sort / load more / shop pagination | Yes | Mobile filter and sort; collection expansion; shop Next/Back/Forward |
| Gallery / zoom viewer / video / size guide | Yes | Representative ring and T-bar image/video controls; viewer Next/Escape; guide tabs |
| Bespoke / contact forms | Yes | Empty/invalid input and safe field exploration; no successful production lead |
| Coupon / promotion wizard | Yes | Seven steps inspected; invalid email advance; no final lead submit |
| Product recommendation quiz | Yes | Independent budget flow through Shop This Match; other modules partially inspected |
| Blogs / education / policies / FAQs | Yes | HTTP crawl and representative desktop/mobile inspection; article Back and sorting |
| Reviews / engraving / stock/backorder variants | Not exposed on selected samples | NOT APPLICABLE to those observed samples; no catalog-wide absence claim |
| Standalone newsletter email form | Not discovered | NOT APPLICABLE; promotional lead wizard is the observed signup-like flow |
| Safe payment/test-order mode | Not exposed | NOT SAFELY TESTABLE |


Discovery used the public sitemap and recursive GET link discovery (two workers), followed by UI inspection of JavaScript-generated states. API/admin/private actions were excluded. The JavaScript-only test-product suggestion demonstrates why the HTTP crawl alone was insufficient. Dynamic recommendations, authenticated/private records and external social embeds may expose additional URLs beyond this point-in-time inventory.


### Current fix ownership

- BUG-002 — Developer
- BUG-003 — Developer
- BUG-004 — Developer
- BUG-005 — Developer
- BUG-006 — Client
- BUG-008 — Developer
- BUG-009 — Developer
- BUG-010 — Developer
- BUG-012 — Developer
- BUG-013 — Client
- BUG-015 — Developer
- BUG-020 — Developer

The table below retains original URL coverage and only selected issue IDs and owners.

### Complete inventory

The full 316-row inventory follows. Yes means a recorded observation at that exact URL and width class, not that all interactions passed. HTTP-only pages were not individually verified as functional. Query variants are separate rows. The listed URLs are the historical discovered destinations; live content may change.

| URL | Page type | Status | Desktop tested? | Mobile tested? | Functional status | Issues found | Issue owners |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [https://www.houseofdiams.com/](https://www.houseofdiams.com/) | Homepage | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-004; BUG-005; BUG-008; BUG-010; BUG-012; BUG-013; BUG-020 | BUG-004 — Developer; BUG-005 — Developer; BUG-008 — Developer; BUG-010 — Developer; BUG-012 — Developer; BUG-013 — Client; BUG-020 — Developer |
| [https://www.houseofdiams.com/about](https://www.houseofdiams.com/about) | Information / policy | 200 | No | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/bespoke](https://www.houseofdiams.com/bespoke) | Enquiry / form | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-004; BUG-005; BUG-008; BUG-012 | BUG-004 — Developer; BUG-005 — Developer; BUG-008 — Developer; BUG-012 — Developer |
| [https://www.houseofdiams.com/blog](https://www.houseofdiams.com/blog) | Content listing | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-005; BUG-008 | BUG-005 — Developer; BUG-008 — Developer |
| [https://www.houseofdiams.com/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams](https://www.houseofdiams.com/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams) | Blog article | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide](https://www.houseofdiams.com/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide) | Blog article | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-008 | BUG-008 — Developer |
| [https://www.houseofdiams.com/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams](https://www.houseofdiams.com/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams) | Blog article | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-of-diams](https://www.houseofdiams.com/blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-of-diams) | Blog article | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide](https://www.houseofdiams.com/blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide) | Blog article | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams](https://www.houseofdiams.com/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams) | Blog article | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of-diams](https://www.houseofdiams.com/blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of-diams) | Blog article | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams](https://www.houseofdiams.com/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams) | Blog article | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat-house-of-diams](https://www.houseofdiams.com/blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat-house-of-diams) | Blog article | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of-diams](https://www.houseofdiams.com/blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of-diams) | Blog article | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/cart](https://www.houseofdiams.com/cart) | Commerce / customer state | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-004; BUG-005; BUG-006; BUG-008; BUG-009; BUG-013 | BUG-004 — Developer; BUG-005 — Developer; BUG-006 — Client; BUG-008 — Developer; BUG-009 — Developer; BUG-013 — Client |
| [https://www.houseofdiams.com/checkout?mode=cart](https://www.houseofdiams.com/checkout?mode=cart) | Commerce / customer state | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-002; BUG-008; BUG-009; BUG-013 | BUG-002 — Developer; BUG-008 — Developer; BUG-009 — Developer; BUG-013 — Client |
| [https://www.houseofdiams.com/checkout?slug=rosette-five-flower-bracelet&name=Rosette+Five-Flower+Bracelet+&price=0.1&image=https%3A%2F%2Fpub-0ea48ff8bc25421e949ac1de2d305b1a.r2.dev%2Fproducts%2Fdraft%2Fimages%2Fa0453c7b-89d2-4837-8a7c-de7474bff678.webp&variant=d7ba18eb-7754-4798-b6e3-8e63ef207570&metal=10K+White+Gold&ring_size=US+4&gemstone=Lab+Grown+Diamond&shape=round&custom=%255B%257B%2522dropdownId%2522%253A%2522f4d5a1f3-791e-444a-b48b-4b68d7481d2f%2522%252C%2522optionId%2522%253A%2522a4c0dfe8-19b2-4601-af2b-27dcefe20dfa%2522%252C%2522label%2522%253A%2522Bracelet%2520Length%2522%252C%2522optionLabel%2522%253A%25227.5%2520Inch%2522%257D%255D](https://www.houseofdiams.com/checkout?slug=rosette-five-flower-bracelet&name=Rosette+Five-Flower+Bracelet+&price=0.1&image=https%3A%2F%2Fpub-0ea48ff8bc25421e949ac1de2d305b1a.r2.dev%2Fproducts%2Fdraft%2Fimages%2Fa0453c7b-89d2-4837-8a7c-de7474bff678.webp&variant=d7ba18eb-7754-4798-b6e3-8e63ef207570&metal=10K+White+Gold&ring_size=US+4&gemstone=Lab+Grown+Diamond&shape=round&custom=%255B%257B%2522dropdownId%2522%253A%2522f4d5a1f3-791e-444a-b48b-4b68d7481d2f%2522%252C%2522optionId%2522%253A%2522a4c0dfe8-19b2-4601-af2b-27dcefe20dfa%2522%252C%2522label%2522%253A%2522Bracelet%2520Length%2522%252C%2522optionLabel%2522%253A%25227.5%2520Inch%2522%257D%255D) | Commerce / customer state | Browser observed; HTTP not separately recorded | Yes — original observation | No | INSPECTED / MIXED RESULTS — see matrix | BUG-002; BUG-008; BUG-009; BUG-013 | BUG-002 — Developer; BUG-008 — Developer; BUG-009 — Developer; BUG-013 — Client |
| [https://www.houseofdiams.com/collection](https://www.houseofdiams.com/collection) | Catalog / collection | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/contact](https://www.houseofdiams.com/contact) | Enquiry / form | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/education](https://www.houseofdiams.com/education) | Content listing | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/education#education-articles](https://www.houseofdiams.com/education#education-articles) | Content listing | Browser observed; HTTP not separately recorded | Yes — original observation | No | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/education/lab-grown-diamond-certification-explained-gia-vs-igi-house-of-diams](https://www.houseofdiams.com/education/lab-grown-diamond-certification-explained-gia-vs-igi-house-of-diams) | Education article | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings](https://www.houseofdiams.com/engagement-rings) | Catalog / collection | 200 | No | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-005; BUG-008 | BUG-005 — Developer; BUG-008 — Developer |
| [https://www.houseofdiams.com/engagement-rings/by-design](https://www.houseofdiams.com/engagement-rings/by-design) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings/by-design/bezel-rings](https://www.houseofdiams.com/engagement-rings/by-design/bezel-rings) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings/by-design/halo-ring](https://www.houseofdiams.com/engagement-rings/by-design/halo-ring) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings/by-design/nature-inspired-rings](https://www.houseofdiams.com/engagement-rings/by-design/nature-inspired-rings) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings/by-design/pave](https://www.houseofdiams.com/engagement-rings/by-design/pave) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings/by-design/pave?page=2](https://www.houseofdiams.com/engagement-rings/by-design/pave?page=2) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings/by-design/side-stone-rings](https://www.houseofdiams.com/engagement-rings/by-design/side-stone-rings) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings/by-design/solitare-rings](https://www.houseofdiams.com/engagement-rings/by-design/solitare-rings) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings/by-design/three-stone-rings](https://www.houseofdiams.com/engagement-rings/by-design/three-stone-rings) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings/by-design/toi-moi-rings](https://www.houseofdiams.com/engagement-rings/by-design/toi-moi-rings) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings/by-design?page=2](https://www.houseofdiams.com/engagement-rings/by-design?page=2) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings/by-design?page=3](https://www.houseofdiams.com/engagement-rings/by-design?page=3) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings/round-rings](https://www.houseofdiams.com/engagement-rings/round-rings) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/engagement-rings?metal=10k-rose-gold](https://www.houseofdiams.com/engagement-rings?metal=10k-rose-gold) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?metal=10k-rose-gold&page=2](https://www.houseofdiams.com/engagement-rings?metal=10k-rose-gold&page=2) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?metal=10k-rose-gold&page=3](https://www.houseofdiams.com/engagement-rings?metal=10k-rose-gold&page=3) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?metal=10k-white-gold](https://www.houseofdiams.com/engagement-rings?metal=10k-white-gold) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?metal=10k-white-gold&page=2](https://www.houseofdiams.com/engagement-rings?metal=10k-white-gold&page=2) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?metal=10k-white-gold&page=3](https://www.houseofdiams.com/engagement-rings?metal=10k-white-gold&page=3) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?metal=10k-yellow-gold](https://www.houseofdiams.com/engagement-rings?metal=10k-yellow-gold) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?metal=10k-yellow-gold&page=2](https://www.houseofdiams.com/engagement-rings?metal=10k-yellow-gold&page=2) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?metal=10k-yellow-gold&page=3](https://www.houseofdiams.com/engagement-rings?metal=10k-yellow-gold&page=3) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?page=2](https://www.houseofdiams.com/engagement-rings?page=2) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?page=3](https://www.houseofdiams.com/engagement-rings?page=3) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?shape=asscher](https://www.houseofdiams.com/engagement-rings?shape=asscher) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?shape=cushion](https://www.houseofdiams.com/engagement-rings?shape=cushion) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?shape=elongated-cushion](https://www.houseofdiams.com/engagement-rings?shape=elongated-cushion) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?shape=emerald](https://www.houseofdiams.com/engagement-rings?shape=emerald) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?shape=marquise](https://www.houseofdiams.com/engagement-rings?shape=marquise) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?shape=oval](https://www.houseofdiams.com/engagement-rings?shape=oval) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?shape=pear](https://www.houseofdiams.com/engagement-rings?shape=pear) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?shape=pear&sort=price-low](https://www.houseofdiams.com/engagement-rings?shape=pear&sort=price-low) | Catalog / collection | Browser observed; HTTP not separately recorded | No | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-005; BUG-008 | BUG-005 — Developer; BUG-008 — Developer |
| [https://www.houseofdiams.com/engagement-rings?shape=princess](https://www.houseofdiams.com/engagement-rings?shape=princess) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?shape=radiant](https://www.houseofdiams.com/engagement-rings?shape=radiant) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/engagement-rings?shape=round](https://www.houseofdiams.com/engagement-rings?shape=round) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/faq](https://www.houseofdiams.com/faq) | Information / policy | 200 | No | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-006 | BUG-006 — Client |
| [https://www.houseofdiams.com/fine-jewellery](https://www.houseofdiams.com/fine-jewellery) | Catalog / collection | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/fine-jewellery/bracelet](https://www.houseofdiams.com/fine-jewellery/bracelet) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/bracelet/bangles](https://www.houseofdiams.com/fine-jewellery/bracelet/bangles) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/bracelet/chain-link](https://www.houseofdiams.com/fine-jewellery/bracelet/chain-link) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/bracelet/tennis](https://www.houseofdiams.com/fine-jewellery/bracelet/tennis) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/earrings](https://www.houseofdiams.com/fine-jewellery/earrings) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/earrings/drop-dangle](https://www.houseofdiams.com/fine-jewellery/earrings/drop-dangle) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/earrings/hoops-huggies](https://www.houseofdiams.com/fine-jewellery/earrings/hoops-huggies) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/earrings/personalized-charm](https://www.houseofdiams.com/fine-jewellery/earrings/personalized-charm) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/earrings/stud-earrings](https://www.houseofdiams.com/fine-jewellery/earrings/stud-earrings) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/earrings/stud-earrings?page=2](https://www.houseofdiams.com/fine-jewellery/earrings/stud-earrings?page=2) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/earrings/tennis-earrings](https://www.houseofdiams.com/fine-jewellery/earrings/tennis-earrings) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/earrings?page=2](https://www.houseofdiams.com/fine-jewellery/earrings?page=2) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/earrings?page=3](https://www.houseofdiams.com/fine-jewellery/earrings?page=3) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/necklaces](https://www.houseofdiams.com/fine-jewellery/necklaces) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/necklaces/charm-necklace](https://www.houseofdiams.com/fine-jewellery/necklaces/charm-necklace) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/necklaces/initials](https://www.houseofdiams.com/fine-jewellery/necklaces/initials) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/necklaces/lariat-necklace](https://www.houseofdiams.com/fine-jewellery/necklaces/lariat-necklace) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/necklaces/multi-stone](https://www.houseofdiams.com/fine-jewellery/necklaces/multi-stone) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/necklaces/pendant-necklace](https://www.houseofdiams.com/fine-jewellery/necklaces/pendant-necklace) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/necklaces/solitare](https://www.houseofdiams.com/fine-jewellery/necklaces/solitare) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/necklaces/solitare?page=2](https://www.houseofdiams.com/fine-jewellery/necklaces/solitare?page=2) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/necklaces/tennis-necklace](https://www.houseofdiams.com/fine-jewellery/necklaces/tennis-necklace) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/necklaces/toi-et-moi](https://www.houseofdiams.com/fine-jewellery/necklaces/toi-et-moi) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/necklaces?page=2](https://www.houseofdiams.com/fine-jewellery/necklaces?page=2) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/necklaces?page=3](https://www.houseofdiams.com/fine-jewellery/necklaces?page=3) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/rings](https://www.houseofdiams.com/fine-jewellery/rings) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery/rings/eternity-rings](https://www.houseofdiams.com/fine-jewellery/rings/eternity-rings) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery?page=2](https://www.houseofdiams.com/fine-jewellery?page=2) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery?page=3](https://www.houseofdiams.com/fine-jewellery?page=3) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery?page=4](https://www.houseofdiams.com/fine-jewellery?page=4) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/fine-jewellery?page=5](https://www.houseofdiams.com/fine-jewellery?page=5) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/hiphop](https://www.houseofdiams.com/hiphop) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/hiphop/chains](https://www.houseofdiams.com/hiphop/chains) | Catalog / collection | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-015 | BUG-015 — Developer |
| [https://www.houseofdiams.com/hiphop/chains/cuban-links](https://www.houseofdiams.com/hiphop/chains/cuban-links) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/hiphop/test-subcat](https://www.houseofdiams.com/hiphop/test-subcat) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Shared-template defects may apply; not individually verified |  |
| [https://www.houseofdiams.com/login](https://www.houseofdiams.com/login) | Authentication / account | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-003; BUG-008 | BUG-003 — Developer; BUG-008 — Developer |
| [https://www.houseofdiams.com/privacy-policy](https://www.houseofdiams.com/privacy-policy) | Information / policy | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/profile](https://www.houseofdiams.com/profile) | Authentication / account | Browser observed; HTTP not separately recorded | No | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/profile?tab=orders](https://www.houseofdiams.com/profile?tab=orders) | Authentication / account | 200 | Yes — original observation | No | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/qa-nonexistent-20261006](https://www.houseofdiams.com/qa-nonexistent-20261006) | Catalog / collection | 404 | No | No | PASSED deliberate invalid-path recovery / HTTP 404 | Not individually inspected |  |
| [https://www.houseofdiams.com/returns](https://www.houseofdiams.com/returns) | Information / policy | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-006; BUG-012 | BUG-006 — Client; BUG-012 — Developer |
| [https://www.houseofdiams.com/shipping](https://www.houseofdiams.com/shipping) | Information / policy | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-013 | BUG-013 — Client |
| [https://www.houseofdiams.com/shop](https://www.houseofdiams.com/shop) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/adeline-round-solitaire-stud-earrings](https://www.houseofdiams.com/shop/adeline-round-solitaire-stud-earrings) | Product detail | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/shop/alternating-pear-diamond-eternity-ring](https://www.houseofdiams.com/shop/alternating-pear-diamond-eternity-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/amara-pear-swirl-ring](https://www.houseofdiams.com/shop/amara-pear-swirl-ring) | Product detail | 404 | Yes — original observation | No | PASSED deliberate invalid-path recovery / HTTP 404 |  |  |
| [https://www.houseofdiams.com/shop/amara-pear-swirl-solitaire-ring](https://www.houseofdiams.com/shop/amara-pear-swirl-solitaire-ring) | Product detail | 200 | No | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-006 | BUG-006 — Client |
| [https://www.houseofdiams.com/shop/amora-heart-cut-solitaire-pendant-necklace](https://www.houseofdiams.com/shop/amora-heart-cut-solitaire-pendant-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/amora-heart-hidden-halo-bridal-set](https://www.houseofdiams.com/shop/amora-heart-hidden-halo-bridal-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/amora-three-prong-heart-solitaire-diamond-necklace](https://www.houseofdiams.com/shop/amora-three-prong-heart-solitaire-diamond-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/amorette-four-heart-diamond-clover-necklace-200](https://www.houseofdiams.com/shop/amorette-four-heart-diamond-clover-necklace-200) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/amorette-four-heart-diamond-clover-necklace-400](https://www.houseofdiams.com/shop/amorette-four-heart-diamond-clover-necklace-400) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/amorette-two-heart-diamond-drop-necklace](https://www.houseofdiams.com/shop/amorette-two-heart-diamond-drop-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/aria-round-bezel-pendant-necklace](https://www.houseofdiams.com/shop/aria-round-bezel-pendant-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/arielle-toi-et-moi-necklace](https://www.houseofdiams.com/shop/arielle-toi-et-moi-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/asscher-statement-row-ring](https://www.houseofdiams.com/shop/asscher-statement-row-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/aster-crown-diamond-hoop-earrings](https://www.houseofdiams.com/shop/aster-crown-diamond-hoop-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/asteria-seven-stone-necklace](https://www.houseofdiams.com/shop/asteria-seven-stone-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/aurelia-emerald-diamond-halo-ring](https://www.houseofdiams.com/shop/aurelia-emerald-diamond-halo-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/aurelia-emerald-hidden-halo-bridal-set](https://www.houseofdiams.com/shop/aurelia-emerald-hidden-halo-bridal-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/aurelia-round-solitaire-diamond-pendant](https://www.houseofdiams.com/shop/aurelia-round-solitaire-diamond-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/aurelia-scalloped-diamond-eternity-ring](https://www.houseofdiams.com/shop/aurelia-scalloped-diamond-eternity-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/aureline-round-side-stone-engagement-ring](https://www.houseofdiams.com/shop/aureline-round-side-stone-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/aurevane-sunburst-round-diamond-halo-stud-earrings](https://www.houseofdiams.com/shop/aurevane-sunburst-round-diamond-halo-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/aurevelle-interlocking-curve-gold-stud-earrings](https://www.houseofdiams.com/shop/aurevelle-interlocking-curve-gold-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/aurora-triple-row-diamond-huggies](https://www.houseofdiams.com/shop/aurora-triple-row-diamond-huggies) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/aveline-emerald-stud-earrings](https://www.houseofdiams.com/shop/aveline-emerald-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/aveline-oval-solitaire-engagement-ring](https://www.houseofdiams.com/shop/aveline-oval-solitaire-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/bezel-oval-half-eternity-band](https://www.houseofdiams.com/shop/bezel-oval-half-eternity-band) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/bezel-pear-half-eternity-band](https://www.houseofdiams.com/shop/bezel-pear-half-eternity-band) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/calista-triple-row-diamond-hoop-earrings](https://www.houseofdiams.com/shop/calista-triple-row-diamond-hoop-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/camellia-cluster-stud-earrings](https://www.houseofdiams.com/shop/camellia-cluster-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/camille-two-tone-knot-t-bar](https://www.houseofdiams.com/shop/camille-two-tone-knot-t-bar) | Product detail | 200 | No | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix | BUG-004; BUG-006 | BUG-004 — Developer; BUG-006 — Client |
| [https://www.houseofdiams.com/shop/celesse-graduated-diamond-ring](https://www.houseofdiams.com/shop/celesse-graduated-diamond-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/celeste-pav-circle-diamond-link-bracelet](https://www.houseofdiams.com/shop/celeste-pav-circle-diamond-link-bracelet) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/celeste-riviera-diamond-hoops](https://www.houseofdiams.com/shop/celeste-riviera-diamond-hoops) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/celeste-round-diamond-bezel-solitaire-stud-earrings-150](https://www.houseofdiams.com/shop/celeste-round-diamond-bezel-solitaire-stud-earrings-150) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/celeste-round-diamond-bezel-solitaire-stud-earrings-200](https://www.houseofdiams.com/shop/celeste-round-diamond-bezel-solitaire-stud-earrings-200) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/celeste-round-solitaire-necklace](https://www.houseofdiams.com/shop/celeste-round-solitaire-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/celestial-arc-oval-pav-bridal-set](https://www.houseofdiams.com/shop/celestial-arc-oval-pav-bridal-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/celestine-dewdrop-pear-diamond-station-necklace](https://www.houseofdiams.com/shop/celestine-dewdrop-pear-diamond-station-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/celestine-interlocking-diamond-statement-stud-earrings](https://www.houseofdiams.com/shop/celestine-interlocking-diamond-statement-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/celestine-oval-hidden-halo-bridal-set](https://www.houseofdiams.com/shop/celestine-oval-hidden-halo-bridal-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/celestine-radiant-diamond-stud-earrings](https://www.houseofdiams.com/shop/celestine-radiant-diamond-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/celestine-round-diamond-stud-earrings](https://www.houseofdiams.com/shop/celestine-round-diamond-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/cherivelle-heart-prong-round-diamond-stud-earrings](https://www.houseofdiams.com/shop/cherivelle-heart-prong-round-diamond-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/classic-round-side-stone-solitaire-ring](https://www.houseofdiams.com/shop/classic-round-side-stone-solitaire-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/corinne-ridged-t-bar](https://www.houseofdiams.com/shop/corinne-ridged-t-bar) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/crestline-oval-pav-engagement-ring](https://www.houseofdiams.com/shop/crestline-oval-pav-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/crownline-princess-cut-diamond-tennis-bracelet](https://www.houseofdiams.com/shop/crownline-princess-cut-diamond-tennis-bracelet) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/crownline-princess-pav-bridal-set](https://www.houseofdiams.com/shop/crownline-princess-pav-bridal-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/cushion-cut-bezel-solitaire](https://www.houseofdiams.com/shop/cushion-cut-bezel-solitaire) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/cushion-solitaire-studs](https://www.houseofdiams.com/shop/cushion-solitaire-studs) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/delphine-marquise-pendant-necklace](https://www.houseofdiams.com/shop/delphine-marquise-pendant-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/diamond-leaf-tassel-lariat-necklace](https://www.houseofdiams.com/shop/diamond-leaf-tassel-lariat-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/east-west-oval-diamond-bezel-pendant](https://www.houseofdiams.com/shop/east-west-oval-diamond-bezel-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/eight-prong-framed-oval-diamond-pendant](https://www.houseofdiams.com/shop/eight-prong-framed-oval-diamond-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elara-radiant-drop-earrings](https://www.houseofdiams.com/shop/elara-radiant-drop-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elaris-emerald-twist-diamond-ring](https://www.houseofdiams.com/shop/elaris-emerald-twist-diamond-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elaris-round-bridal-ring-set](https://www.houseofdiams.com/shop/elaris-round-bridal-ring-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/eloise-multi-stone-necklace](https://www.houseofdiams.com/shop/eloise-multi-stone-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elowen-cushion-halo-engagement-ring](https://www.houseofdiams.com/shop/elowen-cushion-halo-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elowen-emerald-halo-engagement-ring](https://www.houseofdiams.com/shop/elowen-emerald-halo-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elowen-heart-halo-engagement-ring](https://www.houseofdiams.com/shop/elowen-heart-halo-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elowen-marquise-halo-engagement-ring](https://www.houseofdiams.com/shop/elowen-marquise-halo-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elowen-oval-halo-engagement-ring](https://www.houseofdiams.com/shop/elowen-oval-halo-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elowen-pear-halo-engagement-ring](https://www.houseofdiams.com/shop/elowen-pear-halo-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elowen-princess-halo-engagement-ring](https://www.houseofdiams.com/shop/elowen-princess-halo-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elowen-radiant-halo-engagement-ring](https://www.houseofdiams.com/shop/elowen-radiant-halo-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elowen-round-halo-engagement-ring](https://www.houseofdiams.com/shop/elowen-round-halo-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elyra-round-solitaire-diamond-pendant](https://www.houseofdiams.com/shop/elyra-round-solitaire-diamond-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elyra-twist-solitaire-diamond-ring](https://www.houseofdiams.com/shop/elyra-twist-solitaire-diamond-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/elysian-pear-diamond-accent-hoops](https://www.houseofdiams.com/shop/elysian-pear-diamond-accent-hoops) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/emerald-bezel-statement-solitaire](https://www.houseofdiams.com/shop/emerald-bezel-statement-solitaire) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/emerald-cut-eight-prong-diamond-pendant](https://www.houseofdiams.com/shop/emerald-cut-eight-prong-diamond-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/emerald-horizon-diamond-pendant-1786691308867](https://www.houseofdiams.com/shop/emerald-horizon-diamond-pendant-1786691308867) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/emerald-horizon-diamond-pendant-1786691308867-copy-2c3ce70d1b8c](https://www.houseofdiams.com/shop/emerald-horizon-diamond-pendant-1786691308867-copy-2c3ce70d1b8c) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/emerald-radiance-pav-bridal-set](https://www.houseofdiams.com/shop/emerald-radiance-pav-bridal-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/emerald-row-half-eternity-band](https://www.houseofdiams.com/shop/emerald-row-half-eternity-band) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/endless-orbit-round-diamond-tennis-bracelet](https://www.houseofdiams.com/shop/endless-orbit-round-diamond-tennis-bracelet) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/eternal-orbit-round-diamond-pav-bridal-set](https://www.houseofdiams.com/shop/eternal-orbit-round-diamond-pav-bridal-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/evadne-multi-stone-necklace](https://www.houseofdiams.com/shop/evadne-multi-stone-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/evelina-knot-t-bar](https://www.houseofdiams.com/shop/evelina-knot-t-bar) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/evren-emerald-cut-stud-earrings](https://www.houseofdiams.com/shop/evren-emerald-cut-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/fine-jewellery-test-product](https://www.houseofdiams.com/shop/fine-jewellery-test-product) | Product detail | 404 | No | Yes — original observation | FAILED search navigation / HTTP 404 | BUG-020 | BUG-020 — Developer |
| [https://www.houseofdiams.com/shop/floating-four-prong-diamond-necklace-1787998848157](https://www.houseofdiams.com/shop/floating-four-prong-diamond-necklace-1787998848157) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/floating-four-prong-diamond-necklace-1787998848157-copy-7f837d3c7e63](https://www.houseofdiams.com/shop/floating-four-prong-diamond-necklace-1787998848157-copy-7f837d3c7e63) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/fortuna-diamond-horn-pendant-necklace](https://www.houseofdiams.com/shop/fortuna-diamond-horn-pendant-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/four-petal-pear-marquise-diamond-ring](https://www.houseofdiams.com/shop/four-petal-pear-marquise-diamond-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/graduated-diamond-open-circle-necklace](https://www.houseofdiams.com/shop/graduated-diamond-open-circle-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/graduated-round-diamond-c-shaped-stud-earrings](https://www.houseofdiams.com/shop/graduated-round-diamond-c-shaped-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/heartlace-duet-two-row-heart-diamond-tennis-bracelet](https://www.houseofdiams.com/shop/heartlace-duet-two-row-heart-diamond-tennis-bracelet) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/isadora-pear-stud-earrings](https://www.houseofdiams.com/shop/isadora-pear-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/isolde-east-west-marquise-necklace](https://www.houseofdiams.com/shop/isolde-east-west-marquise-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/lattice-rose-gold-diamond-link-bracelet](https://www.houseofdiams.com/shop/lattice-rose-gold-diamond-link-bracelet) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/liora-heart-diamond-charm](https://www.houseofdiams.com/shop/liora-heart-diamond-charm) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/lisette-sculptural-loop-necklace](https://www.houseofdiams.com/shop/lisette-sculptural-loop-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/lumielle-round-pav-diamond-ring](https://www.houseofdiams.com/shop/lumielle-round-pav-diamond-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/luminelle-cadence-marquise-and-round-diamond-bracelet](https://www.houseofdiams.com/shop/luminelle-cadence-marquise-and-round-diamond-bracelet) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/luminous-arc-diamond-hoops](https://www.houseofdiams.com/shop/luminous-arc-diamond-hoops) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/luminous-crest-radiant-diamond-pav-bridal-set](https://www.houseofdiams.com/shop/luminous-crest-radiant-diamond-pav-bridal-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/luminous-point-pear-pav-bridal-set](https://www.houseofdiams.com/shop/luminous-point-pear-pav-bridal-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/lunette-classic-hoop-earrings](https://www.houseofdiams.com/shop/lunette-classic-hoop-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/marcelline-interlocking-t-bar-pendant](https://www.houseofdiams.com/shop/marcelline-interlocking-t-bar-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/marielle-duo-stud-earrings](https://www.houseofdiams.com/shop/marielle-duo-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/marquise-cluster-halo-ring](https://www.houseofdiams.com/shop/marquise-cluster-halo-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/marquise-contrast-prong-solitaire](https://www.houseofdiams.com/shop/marquise-contrast-prong-solitaire) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/marquise-diamond-framed-solitaire-pendant](https://www.houseofdiams.com/shop/marquise-diamond-framed-solitaire-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/marquise-diamond-solitaire-pendant](https://www.houseofdiams.com/shop/marquise-diamond-solitaire-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/marquise-pinnacle-diamond-pendant](https://www.houseofdiams.com/shop/marquise-pinnacle-diamond-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/milgrain-bezel-round-diamond-necklace-1788000835747](https://www.houseofdiams.com/shop/milgrain-bezel-round-diamond-necklace-1788000835747) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/milgrain-bezel-round-diamond-necklace-1788000835747-copy-baae7d47cd58](https://www.houseofdiams.com/shop/milgrain-bezel-round-diamond-necklace-1788000835747-copy-baae7d47cd58) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/monaco-statement-hoop-earrings](https://www.houseofdiams.com/shop/monaco-statement-hoop-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/noir-accent-diamond-tennis-bracelet](https://www.houseofdiams.com/shop/noir-accent-diamond-tennis-bracelet) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/noir-pear-solitaire-necklace](https://www.houseofdiams.com/shop/noir-pear-solitaire-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/odette-five-stone-huggie-earrings](https://www.houseofdiams.com/shop/odette-five-stone-huggie-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/orbit-bezel-set-diamond-tennis-bracelet](https://www.houseofdiams.com/shop/orbit-bezel-set-diamond-tennis-bracelet) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/orion-cross-halo-diamond-stud-earrings](https://www.houseofdiams.com/shop/orion-cross-halo-diamond-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/oval-cluster-side-stone-engagement-ring](https://www.houseofdiams.com/shop/oval-cluster-side-stone-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/oval-cut-twisted-pav-split-shank-engagement-ring](https://www.houseofdiams.com/shop/oval-cut-twisted-pav-split-shank-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/oval-diamond-framed-solitaire-pendant](https://www.houseofdiams.com/shop/oval-diamond-framed-solitaire-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/oval-floral-diamond-ring](https://www.houseofdiams.com/shop/oval-floral-diamond-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/oval-radiance-pav-bridal-set](https://www.houseofdiams.com/shop/oval-radiance-pav-bridal-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/oval-swirl-solitaire-ring](https://www.houseofdiams.com/shop/oval-swirl-solitaire-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/pav-bail-bezel-emerald-diamond-pendant](https://www.houseofdiams.com/shop/pav-bail-bezel-emerald-diamond-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/pear-crest-diamond-pendant](https://www.houseofdiams.com/shop/pear-crest-diamond-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/pear-duo-toi-moi-two-stone-engagement-ring](https://www.houseofdiams.com/shop/pear-duo-toi-moi-two-stone-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/pear-frame-eternity-band](https://www.houseofdiams.com/shop/pear-frame-eternity-band) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/pear-hidden-halo-pav-bridal-set](https://www.houseofdiams.com/shop/pear-hidden-halo-pav-bridal-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/pear-meridian-diamond-pendant](https://www.houseofdiams.com/shop/pear-meridian-diamond-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/pear-pear-swirl-diamond-ring-set](https://www.houseofdiams.com/shop/pear-pear-swirl-diamond-ring-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/princess-halo-stud-earrings](https://www.houseofdiams.com/shop/princess-halo-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/princess-swirl-diamond-ring-set](https://www.houseofdiams.com/shop/princess-swirl-diamond-ring-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/prism-terrace-emerald-pav-bridal-set](https://www.houseofdiams.com/shop/prism-terrace-emerald-pav-bridal-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/radiant-avenue-diamond-tennis-bracelet](https://www.houseofdiams.com/shop/radiant-avenue-diamond-tennis-bracelet) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/radiant-halo-drops](https://www.houseofdiams.com/shop/radiant-halo-drops) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/radiant-swirl-diamond-ring-set](https://www.houseofdiams.com/shop/radiant-swirl-diamond-ring-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/rosette-five-flower-bracelet](https://www.houseofdiams.com/shop/rosette-five-flower-bracelet) | Product detail | 200 | Yes — original observation | No | INSPECTED / MIXED RESULTS — see matrix | BUG-005; BUG-006; BUG-008; BUG-009 | BUG-005 — Developer; BUG-006 — Client; BUG-008 — Developer; BUG-009 — Developer |
| [https://www.houseofdiams.com/shop/round-and-radiant-two-stone-diamond-pendant](https://www.houseofdiams.com/shop/round-and-radiant-two-stone-diamond-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-angular-prong-solitaire](https://www.houseofdiams.com/shop/round-angular-prong-solitaire) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-baguette-three-stone-ring-1787141900680](https://www.houseofdiams.com/shop/round-baguette-three-stone-ring-1787141900680) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-baguette-three-stone-ring-1787142818857](https://www.houseofdiams.com/shop/round-baguette-three-stone-ring-1787142818857) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-diamond-halo-pendant-with-diamond-bail](https://www.houseofdiams.com/shop/round-diamond-halo-pendant-with-diamond-bail) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-diamond-split-bail-solitaire-pendant-1786684531556](https://www.houseofdiams.com/shop/round-diamond-split-bail-solitaire-pendant-1786684531556) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-diamond-split-bail-solitaire-pendant-1786685287191](https://www.houseofdiams.com/shop/round-diamond-split-bail-solitaire-pendant-1786685287191) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-framed-side-stone-engagement-ring](https://www.houseofdiams.com/shop/round-framed-side-stone-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-hoop-drops](https://www.houseofdiams.com/shop/round-hoop-drops) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-radiant-drops](https://www.houseofdiams.com/shop/round-radiant-drops) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-scalloped-halo-ring](https://www.houseofdiams.com/shop/round-scalloped-halo-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-scrollwork-solitaire-ring](https://www.houseofdiams.com/shop/round-scrollwork-solitaire-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-solitaire-studs](https://www.houseofdiams.com/shop/round-solitaire-studs) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-split-band-solitaire](https://www.houseofdiams.com/shop/round-split-band-solitaire) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/round-swirl-diamond-ring-set](https://www.houseofdiams.com/shop/round-swirl-diamond-ring-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/seraphina-cushion-stud-earrings](https://www.houseofdiams.com/shop/seraphina-cushion-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/seraphina-graduated-diamond-drop-earrings](https://www.houseofdiams.com/shop/seraphina-graduated-diamond-drop-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/seraphina-oval-diamond-pendant-with-accent-bail](https://www.houseofdiams.com/shop/seraphina-oval-diamond-pendant-with-accent-bail) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/seraphine-radiant-pav-diamond-ring](https://www.houseofdiams.com/shop/seraphine-radiant-pav-diamond-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/serenelle-pear-pav-ring](https://www.houseofdiams.com/shop/serenelle-pear-pav-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/seven-shape-diamond-circle-pendant](https://www.houseofdiams.com/shop/seven-shape-diamond-circle-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solara-loop-round-diamond-link-bracelet](https://www.houseofdiams.com/shop/solara-loop-round-diamond-link-bracelet) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solenne-asscher-necklace](https://www.houseofdiams.com/shop/solenne-asscher-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solenne-cushion-stud-earrings](https://www.houseofdiams.com/shop/solenne-cushion-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solenne-emerald-stud-earrings](https://www.houseofdiams.com/shop/solenne-emerald-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solenne-marquise-hidden-halo-bridal-set](https://www.houseofdiams.com/shop/solenne-marquise-hidden-halo-bridal-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solenne-oval-stud-earrings](https://www.houseofdiams.com/shop/solenne-oval-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solenne-pear-diamond-drop-earrings](https://www.houseofdiams.com/shop/solenne-pear-diamond-drop-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solenne-princess-stud-earrings](https://www.houseofdiams.com/shop/solenne-princess-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solenne-radiant-bridal-ring-set](https://www.houseofdiams.com/shop/solenne-radiant-bridal-ring-set) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solenne-radiant-stud-earrings](https://www.houseofdiams.com/shop/solenne-radiant-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solenne-round-seven-stone-hoop-earrings](https://www.houseofdiams.com/shop/solenne-round-seven-stone-hoop-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solenne-round-stud-earrings](https://www.houseofdiams.com/shop/solenne-round-stud-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solis-wave-diamond-hoop-earrings](https://www.houseofdiams.com/shop/solis-wave-diamond-hoop-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/solvienne-east-west-marquise-diamond-ring](https://www.houseofdiams.com/shop/solvienne-east-west-marquise-diamond-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/trielle-three-row-diamond-hoop-earrings](https://www.houseofdiams.com/shop/trielle-three-row-diamond-hoop-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/trillion-diamond-solitaire-pendant](https://www.houseofdiams.com/shop/trillion-diamond-solitaire-pendant) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/trinity-oval-three-stone-ring](https://www.houseofdiams.com/shop/trinity-oval-three-stone-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/trivelle-three-stone-diamond-ring](https://www.houseofdiams.com/shop/trivelle-three-stone-diamond-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/trivessa-cascade-three-stone-diamond-huggie-earrings](https://www.houseofdiams.com/shop/trivessa-cascade-three-stone-diamond-huggie-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/twin-arc-round-diamond-engagement-ring](https://www.houseofdiams.com/shop/twin-arc-round-diamond-engagement-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/two-tone-marquise-solitaire-necklace](https://www.houseofdiams.com/shop/two-tone-marquise-solitaire-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/valencia-heart-drop-earrings](https://www.houseofdiams.com/shop/valencia-heart-drop-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/vela-graduated-diamond-hoop-earrings](https://www.houseofdiams.com/shop/vela-graduated-diamond-hoop-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/verona-emerald-cut-diamond-bezel-stud-earrings-150](https://www.houseofdiams.com/shop/verona-emerald-cut-diamond-bezel-stud-earrings-150) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/verona-emerald-cut-diamond-bezel-stud-earrings-200](https://www.houseofdiams.com/shop/verona-emerald-cut-diamond-bezel-stud-earrings-200) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/verona-oval-bezel-pendant-necklace](https://www.houseofdiams.com/shop/verona-oval-bezel-pendant-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/vespera-pendant-necklace](https://www.houseofdiams.com/shop/vespera-pendant-necklace) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/virelle-oval-halo-diamond-drop-earrings](https://www.houseofdiams.com/shop/virelle-oval-halo-diamond-drop-earrings) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/virelle-round-twist-diamond-ring](https://www.houseofdiams.com/shop/virelle-round-twist-diamond-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop/willow-oval-diamond-vine-ring](https://www.houseofdiams.com/shop/willow-oval-diamond-vine-ring) | Product detail | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop?page=2](https://www.houseofdiams.com/shop?page=2) | Catalog / collection | 200 | No | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/shop?page=3](https://www.houseofdiams.com/shop?page=3) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop?page=4](https://www.houseofdiams.com/shop?page=4) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop?page=5](https://www.houseofdiams.com/shop?page=5) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop?page=6](https://www.houseofdiams.com/shop?page=6) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop?page=7](https://www.houseofdiams.com/shop?page=7) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop?page=8](https://www.houseofdiams.com/shop?page=8) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/shop?type=ring&price=0-1000](https://www.houseofdiams.com/shop?type=ring&price=0-1000) | Catalog / collection | Browser observed; HTTP not separately recorded | Yes — original observation | No | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/signup](https://www.houseofdiams.com/signup) | Authentication / account | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/t-bar](https://www.houseofdiams.com/t-bar) | Catalog / collection | 200 | No | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/terms](https://www.houseofdiams.com/terms) | Information / policy | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/wedding-bands](https://www.houseofdiams.com/wedding-bands) | Catalog / collection | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix |  |  |
| [https://www.houseofdiams.com/wedding-bands/for-her](https://www.houseofdiams.com/wedding-bands/for-her) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wedding-bands/for-her/anniversay](https://www.houseofdiams.com/wedding-bands/for-her/anniversay) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wedding-bands/for-her/cigar-band](https://www.houseofdiams.com/wedding-bands/for-her/cigar-band) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wedding-bands/for-her/eternity](https://www.houseofdiams.com/wedding-bands/for-her/eternity) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wedding-bands/for-her/nature](https://www.houseofdiams.com/wedding-bands/for-her/nature) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wedding-bands/for-her/pavee](https://www.houseofdiams.com/wedding-bands/for-her/pavee) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wedding-bands/for-her/solid](https://www.houseofdiams.com/wedding-bands/for-her/solid) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wedding-bands/for-him](https://www.houseofdiams.com/wedding-bands/for-him) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wedding-bands/for-him/classic](https://www.houseofdiams.com/wedding-bands/for-him/classic) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wedding-bands/for-him/designer](https://www.houseofdiams.com/wedding-bands/for-him/designer) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wedding-bands/for-him/diamonds](https://www.houseofdiams.com/wedding-bands/for-him/diamonds) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wedding-bands?metal=10k-rose-gold](https://www.houseofdiams.com/wedding-bands?metal=10k-rose-gold) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wedding-bands?metal=10k-white-gold](https://www.houseofdiams.com/wedding-bands?metal=10k-white-gold) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wedding-bands?metal=10k-yellow-gold](https://www.houseofdiams.com/wedding-bands?metal=10k-yellow-gold) | Catalog / collection | 200 | No | No | HTTP ONLY — interactions not tested | Not individually inspected |  |
| [https://www.houseofdiams.com/wishlist](https://www.houseofdiams.com/wishlist) | Commerce / customer state | 200 | Yes — original observation | Yes — original observation | INSPECTED / MIXED RESULTS — see matrix |  |  |

## Instructions for Claude or GPT

Use this document as the complete selected QA brief. Preserve the original bug IDs and requested owners: Client owns BUG-006 and BUG-013; Developer owns BUG-002, BUG-003, BUG-004, BUG-005, BUG-008, BUG-009, BUG-010, BUG-012, BUG-015 and BUG-020. Do not add discarded issues back into this work list.

Reproduce the historical findings against the current site/build before proposing a fix. Distinguish recorded observations, suspected implementation causes and facts confirmed by current code. Investigate the areas named in each bug; they are directions, not proof of a particular root cause. Follow each acceptance check and report what was actually verified.

This document authorizes no deployment, account change, purchase, payment, production order or successful production lead submission. Any implementation or production changes require the owner's instructions. Use approved staging accounts, controlled inboxes and sandbox payments for actions that create records or send messages. Never mark an untested success path as passed.

Screenshots, raw trace files and scripts are intentionally not retained. All important recorded results for the selected scope are written here. If fresh visual proof or a new benchmark is required, collect it during the authorised retest.
