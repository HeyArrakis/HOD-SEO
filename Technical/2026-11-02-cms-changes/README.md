# CMS changes: 2026-11-02 (New York office)

**Why:** the owner confirmed in chat on 2026-11-02 that the New York office is real and gave the exact address, with no suite number: 36 W 44th Street, New York, NY 10036, USA. Recorded in `Keywords/content SEO/content-strategy/blog-calendar/revision/confirmed_business_facts.md`, row 1.

**Where:** admin `manage.houseofdiams.com`, using Claude in Chrome in the owner's Chrome profile (the owner was signed in). The save went through the admin's own confirm dialog. Nothing was deleted.

## Change

| # | Admin place | Before | After |
|---|---|---|---|
| 1 | CMS → Contact → **Contact Info** | 3 cards: Email, Phone & WhatsApp, Atelier · India | New card 4: label `Office · USA`, value `36 W 44th Street, New York, NY 10036, USA`, no note, no link, no icon |

Cards 1 to 3 were not changed.

**Surat stays first on purpose.** The `/contact` map uses the first address card (the first label or note containing `address`, `location` or `atelier`). The new card comes after Surat, and its label contains none of those words, so the map keeps showing Surat.

**Note added later on 2026-11-02.** The owner confirmed that New York visits are by appointment only, and the card's note now reads `By appointment only` (see the last section of this file). The footer shows only the value and note, not the label, so the value carries the full address.

## Code that goes with it

Storefront PR #25, merged as `3102c0a` (branch `sonder-us-office`): Organization schema with both addresses, `llms.txt`, and the fallback rows used only when the database read fails.

## Live check

Checked on production on 2026-11-02, after the deploy of `3102c0a` succeeded:

- The public contact rows now list 4 cards, with `Office · USA` last.
- The address is in the HTML of `/`, `/contact`, `/returns`, `/about` and `/shipping`; "1000B" appears on none of them.
- The footer shows the address as its last contact line.
- The `/contact` "Show map" button still opens the map at Surat.
- Organization schema lists 2 addresses: Surat and New York.
- `llms.txt` names the New York office and both addresses.

# Google Business Profile: 2026-11-02

**Why:** the owner asked in chat to fix the whole profile and show the New York address.

**Where:** the profile editor on Google Search, in the owner's Chrome.

## New York address: not possible on this profile

The profile's Country/Region is locked to India. Google's note on the field: "This can't be edited. To change your country / region, you'll have to create a new Business Profile on Google." The address edit was cancelled and nothing was saved, so the profile still shows no address (service area only). Showing New York needs a new US profile, which the owner has to verify. The owner said yes and accepted Google's terms; see "New York profile" below.

## Saved (all "pending" Google's review; Google says up to about 10 minutes)

| Field | Before | After |
|---|---|---|
| Additional categories | None (primary: Jewelry manufacturer) | Jewellery Store, Jeweller. Primary unchanged |
| Description | Said "based in New York", "jewellery" and "solid 10K and 14K gold" | See below (695 of 750 characters, facts from the fact box only) |
| Website | `https://www.houseofdiams.com/` | `https://houseofdiams.com/?utm_source=gbp&utm_medium=organic` (returns 200) |

New description:

> House of Diams makes fine lab-grown diamond jewelry, with its headquarters and workshop in Surat, India, and an office in New York. We have been in the diamond trade since 2014, launched direct to customers in 2025, and now have a presence in over 20 countries.
>
> Every piece is made to order. We cut and process our own conflict-free, ethically sourced diamonds, and pieces come with IGI and GIA certificates.
>
> Our collections include engagement rings, wedding bands, earrings, necklaces, pendants and bracelets. We also take bespoke commissions, building custom pieces around your chosen stone, carat, metal and finish.
>
> Visits to our Surat workshop and New York office are by appointment only.

## Left as it was

- **Phone `093285 36178` and WhatsApp/text chat:** already entered and correct, but Google has them stuck: "Your edit is taking longer than expected. Contact support for assistance." Only the owner can contact support.
- **Hours:** Open 24 hours (owner: open 24/7).
- **Service area:** Canada, France, Germany, Australia, United States, United Kingdom, Dubai. Which countries to list is still open (F-06).
- **Opening date:** 29 November 2014.
- **Payments and attributes:** not confirmed by the owner, so not changed. These are: all card brands listed, "LGBTQ+ friendly", and "doesn't identify as women-owned".
- **Photos, posts and reviews:** nothing added. Photos must be real ones from the owner. The profile has 0 reviews, and only real ones may be used.

Review link for customers (F-08): https://g.page/r/CVTzG331vUIBEBM/review

## New York profile: created, not verified, not public

Created on 2026-11-02 at the owner's request, under the same Business Manager "House of Diams". Shop code `09959926181983663697`. Status in Business Profile Manager: **Verification required**. Google says edits are not visible to customers until verification is complete.

| Field | Value |
|---|---|
| Business name | House of Diams |
| Category | Jewellery Store |
| Address | 36 W 44th St, New York, NY 10036, United States (Google's short form of the owner's address; no suite) |
| Customers can visit | Yes |
| Deliveries or home and office visits from here | No |
| Phone | +91 93285 36178 |
| Website | `https://houseofdiams.com/?utm_source=gbp&utm_medium=organic&utm_campaign=new-york` |
| Chat | Not added |
| Hours | Skipped. No New York visiting hours are confirmed, and "Open 24 hours" would mislead for an appointment-only office |
| Description | **Not saved.** Next did nothing on 3 tries and the box was empty when the step was reopened. Enter the description above after verification |

Google offered a possible match, "House of Diamonds" at 50 W 47th St #2018, (212) 944-9441. It has a different name, address and phone, so "This doesn't match" was chosen and nothing was claimed.

**Verification:** the only method offered is a business video showing the location, equipment and proof of management. "Verify later" was chosen. Only the owner can do this, from the "Get verified" button on the profile. The office's street, inside and proof of management need to appear in the video.

**Risks to check before verifying:**

- Google can refuse or suspend a location that isn't staffed. Its rules are about locations open to customers, and appointment-only offices need staff present during stated hours.
- The profile has an Indian phone number on a US address, and no hours.
- The India profile stays as it is and still shows no address.

**After verification:** add the description, hours (once the owner has them), real photos, and the additional category if wanted.

# Home page Best Sellers: 2026-11-02

At the owner's request, **Rosette Five-Flower Bracelet** was removed from Best Sellers (admin: CMS > Home > Best Sellers). Only the list changed; the product itself wasn't touched.

| | Products, in order |
|---|---|
| Before | Seraphina Oval Diamond Pendant with Accent Bail; Amora Heart-Cut Solitaire Pendant Necklace; Celeste Pavé Circle Diamond Link Bracelet; Marcelline Interlocking T-Bar; Rosette Five-Flower Bracelet |
| After | The same first four, in the same order |

To undo: add the product back on the same admin page, then move it to the wanted position.

# Exchanges, refunds and the New York note: 2026-11-02

The owner signed in and gave access. The wording uses only what the owner confirmed in writing that day. Each edit went through the admin's own confirm dialog.

| # | Admin place | Before | After |
|---|---|---|---|
| 1 | CMS → Support → FAQ → "Can I return or exchange an engagement ring if she does not like it?" | "You can return a piece within 15 days of delivery if it is unworn. Your refund is issued once the returned piece reaches us. Return shipping, duties and delivery costs are paid by the customer. Bespoke and custom pieces are made to order and cannot be returned, unless the finished piece does not match the design we agreed with you." | Same as the `/returns` text: adds "A 15% restocking fee applies. We also accept exchanges within 15 days of delivery. Refunds are processed in 15–25 days after we receive the piece, while we inspect it, check it is not damaged and verify the diamond."; removes the "refund is issued once" sentence |
| 2 | CMS → Service Banner → block "COMPLIMENTARY SHIPPING & 15-DAY RETURNS", second paragraph (shown on product pages) | "Returns are accepted within 15 days of delivery for unworn pieces; return shipping and duties are paid by the customer. Learn more" | "Returns are accepted within 15 days of delivery for unworn pieces, with a 15% restocking fee; return shipping and duties are paid by the customer. We also accept exchanges within 15 days of delivery. Refunds are processed in 15–25 days after we receive the piece. Learn more" |
| 3 | CMS → Contact → Contact Info → `Office · USA` | Note empty | Note `By appointment only` |

Catalog Setup → Policies → Standard Shipping was opened and closed without saving; it doesn't cover returns.

**Not changed, for the owner to decide:** that block's title still says "COMPLIMENTARY SHIPPING & 15-DAY RETURNS", which could read as free returns even though the customer pays a 15% fee and return shipping.

**Still not stated anywhere, because the owner hasn't answered:** whether the 15% fee and shipping costs apply to exchanges, whether the piece must be unworn, and whether bespoke pieces can be exchanged.

