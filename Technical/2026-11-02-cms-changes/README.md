# CMS changes: 2026-11-02 (New York office)

**Why:** the owner confirmed in chat on 2026-11-02 that the New York office is real and gave the exact address, with no suite number: 36 W 44th Street, New York, NY 10036, USA. Recorded in `Keywords/content SEO/content-strategy/blog-calendar/revision/confirmed_business_facts.md`, row 1.

**Where:** admin `manage.houseofdiams.com`, using Claude in Chrome in the owner's Chrome profile (the owner was signed in). The save went through the admin's own confirm dialog. Nothing was deleted.

## Change

| # | Admin place | Before | After |
|---|---|---|---|
| 1 | CMS → Contact → **Contact Info** | 3 cards: Email, Phone & WhatsApp, Atelier · India | New card 4: label `Office · USA`, value `36 W 44th Street, New York, NY 10036, USA`, no note, no link, no icon |

Cards 1 to 3 were not changed.

**Surat stays first on purpose.** The `/contact` map uses the first address card (the first label or note containing `address`, `location` or `atelier`). The new card comes after Surat, and its label contains none of those words, so the map keeps showing Surat.

**Note still to add.** The owner confirmed later on 2026-11-02 that New York visits are by appointment only. The card's note should read `By appointment only`. Not done yet: the admin session had expired and asks for a password, which only the owner types. The footer shows only the value and note, not the label, so the value carries the full address.

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

The profile's Country/Region is locked to India. Google's note on the field: "This can't be edited. To change your country / region, you'll have to create a new Business Profile on Google." The address edit was cancelled and nothing was saved, so the profile still shows no address (service area only). Showing New York needs a new US profile, which the owner has to verify. Decision pending.

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
