# Google tool changes: 2026-11-02

**Why:** the owner approved these in chat on 2026-11-02 ("Yes, start them"). They cover `FINAL-AUDIT-2026-11-01/changes.md` D-01 to D-05.

**Where:** the owner's Chrome profile, using Claude in Chrome. The live test ran in the built-in browser, so the owner's own bag wasn't touched. No code changed.

## Merchant Center (account 5837491424)

| Item | Before | After |
|---|---|---|
| Return policy restocking fee | 35 % | 15 % |
| Return policy website link | Not recorded | `https://houseofdiams.com/returns` |
| Return policy status | Rejected | Rejected label cleared; Google's review can take up to 10 days |
| Products | 236 in the audit (1 Nov) | Already 182, all from "main feed". The 54 extras had gone, so nothing was deleted |

**Left as they were, and not on the site or confirmed by the owner:**

- "Accept exchanges"
- "Refund processing time 25 days"

**Not changed, waiting for the owner:** "Shipping Policy 14 36" says Free, 18–32 days. The confirmed times are about 10–14 days to make plus 6–8 days delivery, so about 16–22 days.

## Search Console (`sc-domain:houseofdiams.com`)

- `https://houseofdiams.com/sitemap.xml` submitted: Success, 246 pages. It first showed "Couldn't fetch" and read Success a few minutes later.
- The `www` sitemap is still submitted. D-04 says to remove it once the apex one is read.
- Validation started on 5 of 6 merchant-listing issues:
  - Duplicate `material`
  - Missing `hasMerchantReturnPolicy`
  - Missing `shippingDetails`
  - `applicableCountry` limit
  - Missing `deliveryTime`
- **Not started:** missing `returnShippingFeesAmount` (4 items). A live product shows `returnFees` ReturnFeesCustomerResponsibility and no amount, so this may be a small code item under A-02.
- Read only: Search generative AI = Include. The robots.txt report's 3 critical errors are `uat.`, `content.` and `media.houseofdiams.com` not being fetched. The main host's robots.txt is fetched, with 1 warning that wasn't read.

**Found on the way, not fixed:** the sitemap is sometimes very slow: 76 s and 23.6 s on two tries, about 1.2 s on others (`x-cache: Miss from cloudfront`). It isn't linked to the Googlebot user agent. It may be related to the unexplained Lighthouse drop on 2 Nov.

## Tag Manager (`GTM-TJ5HTTSD`): published as Version 7

Before publishing, the workspace showed 28 changes.

- **12 GA4 event tags added**, each with its own Custom Event trigger, sending to `G-0LVQJ1YDJ0`: `view_item`, `add_to_cart`, `remove_from_cart`, `view_cart`, `add_to_wishlist`, `begin_checkout`, `add_shipping_info`, `add_payment_info`, `purchase`, `generate_lead`, `sign_up`, `login`. The nine ecommerce tags read their data from the dataLayer.
- **2 variables added:** `DLV - form_name`, `DLV - method`.
- **Microsoft Clarity:** requires `analytics_storage`.
- **Pinterest:** requires `ad_storage` and `ad_user_data`.

**Different from D-01, on purpose:**

- No tags for `page_view` or `view_search_results`. GA4's Enhanced Measurement already counts page views (including browser-history page changes) and site search, so tags would double-count. Checked in the stream settings; nothing changed there.
- No tags for `view_item_list` or `select_item`, because the site doesn't send them. Sending them would need a code change.

### Live test

| Check | Result |
|---|---|
| Published `gtm.js` contains the new events and consent names | Yes |
| `view_item` reaches GA4 | Yes: USD, value 1525, product details included |
| `add_to_cart`, `view_cart` | Yes, with product details |
| `begin_checkout` | Yes (page opened only, nothing submitted) |
| `remove_from_cart` | Yes, with product details |
| Clarity and Pinterest load with cookies refused (saved choice) | No, on the home, product and cart pages. The "pinterest" match on `/cart` is the site's own footer icon |
| Clarity and Pinterest load for a fresh visitor with no choice saved | No (one Lighthouse run on the homepage, 87 requests, none to Clarity or Pinterest) |
| Lighthouse Best Practices, homepage, desktop | **96** (was 77), then **100** after storefront PR #26. The 96 was a report-only Content Security Policy issue on Google's `pagead2.googlesyndication.com/ccm/collect` |
| Clarity and Pinterest load after "Accept" (owner approved the click, test browser only) | Yes, from the next page. Both loaded and sent data on the next page, and GA4 changed from `gcs=G100` to `G111`. Nothing fired within 5 seconds on the page where Accept was clicked, so that first page isn't recorded by them |
| After "Reject all" (withdrawing consent) | Neither loads on the next page, and GA4 is back to `G100`. The Clarity cookies were gone, but the Pinterest cookie `_pin_unauth` stayed in the browser. Fixed by storefront PR #26; see below. The test browser was left on "Reject all" |
| `purchase`, `add_shipping_info`, `add_payment_info` | **Not tested.** They need a real checkout, so the first real order is the test |
| `add_to_wishlist`, `generate_lead`, `sign_up`, `login` | **Not tested.** No form was submitted and no account was used |

The test item was removed from the test browser's bag afterwards.

### Code follow-up: storefront PR #26

Merged as `d19247b` at the owner's request; the deploy succeeded. GitHub's checks passed and the Claude review found no problems. Local checks on Node 24: typecheck 0 errors, lint 0 errors, tests 397 of 397, build OK.

- **Cookies:** "Reject all" and "Save preferences" now remove refused cookies on every choice. Analytics covers Google plus Clarity's `_clck` and `_clsk`. Marketing covers Pinterest's `_pin_unauth`, `_epik` and `_derived_epik`.
- **Security policy:** `connect-src` allows `https://pagead2.googlesyndication.com`. It's still report-only.

Live check after the deploy:

| Check | Result |
|---|---|
| Real `_pin_unauth` cookie after "Reject all" | Gone, and still gone on the next page |
| Clarity and Pinterest after "Reject all" | Don't load; GA4 stays on `G100` |
| New address in the live policy header | Yes |
| Best Practices (Lighthouse, fresh visitor) | 100 on homepage desktop, homepage mobile and one product page desktop |
| `/`, a product page, `/contact`, `/cart`, `/checkout` | All 200 (page loads only, nothing submitted) |

**Not checked on production:** removing Clarity's cookies, because none were present (it worked on the local build). `_epik` and `_derived_epik` were only checked locally too. The Clarity tag may also set cookies such as `CLID` and `MR` on its own domain, which the site can't remove.

## GA4 (property `543052053`)

| Item | Before | After |
|---|---|---|
| Currency | Indian Rupee | US Dollar (saved, "Success") |
| Stream → Create custom events | 1 rule: create `add_to_cart` on every `page_view` where `page_path` starts with `/cart` | No rules. Deleted at the owner's request; Google says this can't be undone. The conditions are recorded here if it's ever wanted again |

**Why the rule went:** opening `/cart` sent an `add_to_cart` with no product. `add_to_cart` is a key event, so every cart page view counted as a conversion, on top of the real event added today.

**Check after deleting:** opening `/cart` in the test browser sent only `page_view`, with no `add_to_cart`. Add-to-bag numbers and key events before 2 Nov still include these false hits, so don't compare them with later numbers.

**Found, not changed, waiting for the owner:**

- **Team visits filter:** a data filter "Internal Traffic" exists but is only in Testing, and no internal-traffic rules exist. It needs the office and developer IP addresses from the owner.
- **Unwanted referrals:** none listed. D-03 lists `accounts.google.com`, `auth-uat.houseofdiams.com`, `checkout.razorpay.com`, `api.razorpay.com`.
- **Key events:** `add_to_cart`, `close_convert_lead`, `purchase`, `qualify_lead`. `generate_lead` isn't one yet.
- **Stream URL:** still shows `https://www.houseofdiams.com/`.

# Owner's answers, 2 Nov 2026 (later the same day)

The owner sent the three outstanding answers in writing, and these changes followed.

| Where | Before | After | Status |
|---|---|---|---|
| GA4 internal traffic rules | None | Rule "Office", `traffic_type` = internal, the one office IP the owner gave (entered as a single-address range) | Saved and seen in the list |
| GA4 data filter "Internal Traffic" | Testing | **Active** | Saved and seen in the list. Not tested with a real office visit. Google warns that excluded data can't be recovered and that the filter wasn't tested first; it can be switched back to Testing |
| Merchant Center "Shipping Policy 14 36" | Handling 8–15, transit 10–17, so 18–32 business days | Handling 10–14, transit 6–8, so **16–22 business days** | Saved; Merchant Center's confirmation page shows 16–22 |
| Merchant Center return policy | 15 days, customer pays shipping + 15 % fee, "Verified" | Not changed | "Accept exchanges" and "Refund processing time 25 days" are now confirmed true |
| Site `/returns` and `llms.txt` facts (`RETURNS_POLICY`) | No exchanges or refund timing | Adds both | [Storefront PR #27](https://github.com/House-of-diams/aws-houseofdiams-storefront/pull/27), merged as `7538c84` and live |

The IP itself is kept in GA4, not in this file.

**Other things to know:**

- Google's "business days" are Monday to Saturday in this policy, so its 16–22 can run longer in calendar days than the site's wording.
- The Merchant Center order cut-off is still 2:00 PM Pacific. The site says there's no cut-off time; the field is required, so it was left alone.
- Only one IP is filtered. Developer visits, and office visits if this IP changes, still count.

**Waiting for the owner to sign in to the admin (its session ended, and Claude doesn't type passwords):**

- FAQ "Can I return or exchange an engagement ring if she does not like it?": add exchanges, refund timing and the 15 % fee, which that answer also lacks.
- Product page returns line ("Returns are accepted within 15 days of delivery for unworn pieces; return shipping and duties are paid by the customer."): add the same, after checking which admin field holds it.

**Not asked yet:** whether the 15 % fee and shipping costs apply to exchanges, whether the piece must be unworn, and whether bespoke pieces can be exchanged. PR #27 leaves these out on purpose. The GitHub review pointed out that the exchange sentence sits between the fee and shipping sentences, so a reader may assume the same terms apply, or that an exchange is free. The owner merged it knowing the rules were open; fix the wording once they're answered.

