# CMS changes — 2026-11-01 (owner's answers to the 13 questions)

**Why:** the owner answered the open questions in writing on 2026-11-01 (recorded in `Keywords/content SEO/content-strategy/blog-calendar/revision/confirmed_business_facts.md`, section "Added 2026-11-01") and asked for the CMS to be updated to match.

**Where:** admin `manage.houseofdiams.com`, using Claude in Chrome in the owner's Chrome profile (the owner was signed in). Every save went through the admin's own confirm dialog. Nothing was deleted.

## Changes (before → after)

| # | Admin place | Before | After | Answer |
|---|---|---|---|---|
| 1 | Catalog Setup → Policies → **Standard Shipping** (body; product-page "Shipping" tab on 180 products) | "Free, insured overnight shipping to every country, with no order cut-off time. Made-to-order pieces vary by complexity and destination. Duties and taxes may apply depending on the delivery country." | "Free, insured shipping to every country, with no order cut-off time. Every piece is made to order for you. All import duties and taxes are included in the price, so there is nothing more to pay on delivery." | 2, 4 |
| 2 | CMS → **Service Banner** → block 1 "COMPLIMENTARY SHIPPING & 15-DAY RETURNS" (every product page) | "We offer free, insured overnight shipping to every country, with no order cut-off time." | "We offer free, insured shipping to every country, with no order cut-off time. Import duties and taxes are included in the price." (the returns half and the "Learn more" links are unchanged) | 2, 4 |
| 3 | CMS → **Service Banner** → block 3 "COMPLIMENTARY SHIPPING" | "Delivery: A signature is required, and we may ask for ID." | "Delivery: A signature may be required, depending on the value of your piece." (the rest of the sentence is unchanged) | 5 |
| 4 | CMS → Support → **FAQ** → "How long does delivery take?" | "We offer overnight shipping, with delivery times varying by region — typically within 2 weeks worldwide. …" | "Every piece is made to order for you, so the time depends on the piece and the destination. Bespoke pieces typically take 2–3 weeks to make, followed by approximately 6–9 days for delivery. Shipping is free and insured to every country. …" (the last two sentences on the footer and urgent orders are unchanged) | 2, 3 |
| 5 | CMS → Support → **FAQ** → "Do you ship internationally?" | "Yes, we ship worldwide for Free with secure insured shipping." | "Yes. We ship to every country for free, and every order is insured. All import duties and taxes are included in the price, so there is nothing more to pay on delivery." | 4 |
| 6 | CMS → Support → **FAQ** → "Can I speak to someone before buying?" (also shown on category pages) | "… We respond within 24 hours." | "… We generally respond within 12 hours." | 11 |
| 7 | CMS → Contact → **Contact Info** → Email card note (footer on every page, `/contact`, `/returns`) | "Replies within 24 hours" | "Replies within 12 hours" | 11 |
| 8 | CMS → Contact → **Contact Hero** subtitle | "… Reach out - we reply within 24 hours." | "… Reach out - we reply within 12 hours." | 11 |
| 9 | Bespoke → **Form Settings** → intro | "… our workshop team will reply within 24 hours with stone options, pricing, and a personalised design proposal." | "… will reply within 12 hours with stone options, pricing, and a personalized design proposal." | 11 |
| 10 | Bespoke → **Form Settings** → footer note | "We will reply within 24 hours. Your details stay confidential." | "We will reply within 12 hours. Your details stay confidential." | 11 |
| 11 | CMS → About → **Founders** → Krish Babariya | Designation "Founder"; bio "Krish Babariya founded House of Diams together with Akshar Korat. The business has been in the diamond trade since 2014 and works from Surat, India." | Designation "Co-founder"; bio "Krish co-founded House of Diams with Akshar Korat. He oversees online sales, design development, and sales strategy, playing a key role in product development and business growth." | 8 |
| 12 | CMS → About → **Timeline** | 2014 Surat / 2016 Supplying the global trade / 2022 Lab-grown diamonds added to the line / 2023 A decade in the trade / 2025 Direct to client, worldwide | Same, plus **2020 "Established networks in 20+ countries"** restored between 2016 and 2022. The admin has no reorder control, so the rows were re-filled in year order. The 2018 "New York office opens" row stays removed (no address or city). | 6, 1 |
| 13 | CMS → About → **Values** | 4 cards (Certified Jewelry, Built to Last, Bespoke by Nature, Precision Crafted) | Added **"CONFLICT FREE"**: "Our diamonds are conflict-free. We cut and process our own stones, so we control where they come from and their quality." and **"ETHICALLY SOURCED"**: "Our diamonds are ethically sourced, and the people who cut and set them are treated fairly and paid properly." Both have no image yet (grey tile, like Precision Crafted). The owner can add photos with "Upload Image". | 6 |
| 14 | CMS → About → **Wide Banner** paragraph | "Discover how House of Diams has grown since 2014." | "Discover how House of Diams has grown since 2014, from our workshop in Surat to clients in over 20 countries and a presence in the USA." | 1, 6 |

The other 38 FAQ answers were read; none had the outdated phrases.

## Not CMS (hard-coded; added to `DEVELOPER-HANDOFF/05` as O-17)

- The homepage strip "Complimentary Overnight Shipping".
- "Overnight Shipping" icons on the homepage and product page.
- The "Ready to Ship" badge.
- The `/shipping` text "same-day overnight dispatch" and the "Same-day overnight dispatch" include line.
- The FAQ fallback "Customs and duties may vary by country".
- Checkout: "Complimentary Overnight Shipping with Signature".
- "within 24 hours" in the contact panel on every page and in several enquiry forms and toasts.

## Not changed (waiting for the owner)

- Courier name and transit days.
- India tax.
- The new name for `/fine-jewellery/bracelet/bangles`.
- Capitals for blog, article and FAQ headings, and the category intros: the owner said to leave them for now.

## Live check (2026-11-01, all 246 sitemap pages fetched twice; the first request refreshes the server cache)

All 14 changes are live:

| Check | Pages |
|---|---|
| New Shipping policy text (product "Shipping" tab) | 180 |
| New Service Banner texts (duties included; signature may be required) | 182 |
| "within 12 hours" | 246 |
| "Duties and taxes may apply" or "signature is required" | 0 |

Also checked on the live site:
- `/faq`: the three FAQ answers appear in the FAQ schema with the new text.
- Category pages: "We generally respond within 12 hours".
- `/bespoke`: both "12 hours" lines.
- `/about` data (`/api/public/about/*`): Krish is "Co-founder" with the new bio; the timeline reads 2014, 2016, 2020, 2022, 2023, 2025; the values include CONFLICT FREE and ETHICALLY SOURCED; the wide banner mentions the USA.

**Still on the live site, all hard-coded (O-17 in 05):**
- "Complimentary Overnight Shipping" on `/`.
- "same-day overnight dispatch" on `/shipping`.
- "Our team normally replies within 24 hours" in the contact panel on all 246 pages.
