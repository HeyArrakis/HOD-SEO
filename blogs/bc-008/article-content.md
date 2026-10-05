# BC-008 — Article Content (CMS formatting map)

**Source:** `blogs/bc-008/BC-008-meaningful-jewelry-gifts-for-your-wife.md`. The wording is unchanged.

## How to enter it (recommended: paste)

The **Article Content** editor (TipTap) has no link button, and it doesn't support tables. The most reliable way to enter the article is a rich-text paste:

1. Open `bc-008/article-content.html` in Chrome.
2. Press **Cmd+A**, then **Cmd+C**.
3. Click into **Article Content** in the CMS and press **Cmd+V**.

The pasted content keeps the H2, H3, bold, italic, bullet lists, numbered lists, horizontal rule and links. It uses only tags the editor and the storefront sanitizer accept: `p, h2, h3, strong, em, ul, ol, li, a, hr`.

**After pasting, check:**
- **No H1 inside Article Content.** The storefront renders the H1 from **Display Title**.
- **No breadcrumb or byline in the body.** The page template renders "Back to Journal" and the **Written By** value.
- **7 live links**, each clickable, with the correct href (see `internal-links.md`).
- **0 conditional anchor(s)** are **plain text, not links**: none.
- **"holiday jewelry gift guide"** links to BC-004 (`/blog/christmas-jewelry-gifts-a-holiday-gift-guide`). BC-004 is scheduled before this post; confirm that URL loads before publishing. If BC-004 isn't live yet, publish BC-004 first (it's scheduled earlier) or hold this post until it is.
- **No heading reads "FAQ" or "Frequently asked questions".** The storefront auto-generates FAQPage schema under such a heading; the Q&A heading in this article is worded to avoid that.

## What changed for the CMS (formatting only)

| Source element | CMS treatment | Why |
|---|---|---|
| H1 | Not in Article Content; goes in **Display Title** | `BlogPostBody` renders the H1 from the title fields |
| Breadcrumb line, "*By HOD Team*" | Not in Article Content | The template provides "Back to Journal" and the author meta |
| 1 table(s) | Converted to bullet lists. Column headings become inline labels in italics (e.g. "*Strong choices:*"); in comparison tables with an empty first heading, each column becomes a bold label followed by a list. All cell text is kept word for word; only separating punctuation was added. | `sanitizeRichText` strips table tags, and the editor has no table extension |
| Relative links | Absolute `https://www.houseofdiams.com/...` | A browser copy from a local file turns relative links into `file:///` links. These are the same destinations. |
| `[CONDITIONAL]` links | Anchor kept as plain text | The target pages aren't live yet |
| "---" before About the author | Horizontal rule | Same as the source |

**Verified:** generated programmatically from the approved source and compared block by block. Article Content is about **873 words** (including converted table labels).

## Block-by-block map

Use this as a fallback if you build the content by hand, or to check the paste.

### Block 1 — Paragraph

The best jewelry gifts for a wife are pieces she'll wear every day: **diamond stud earrings, a solitaire pendant or a tennis bracelet**. For an anniversary or another milestone, an **eternity or half-eternity band** that sits beside her engagement ring is the most personal choice, as long as you know her ring size.

### Block 2 — Paragraph

The right choice depends less on the piece itself than on what she already wears. Start there, and the decision gets much easier.

### Block 3 — H2

Before you choose: three quick checks

### Block 4 — Numbered

1. **What does she wear every day?** Look at her jewelry box and her daily habits. If she always wears earrings, buy earrings. If she rarely takes off one necklace, a pendant is a safe bet.
2. **What metal does she wear?** Match the yellow, white or rose gold she already reaches for, especially if the gift will sit beside her rings.
3. **What's the occasion?** A Christmas gift can be playful or practical. An anniversary gift should feel more lasting.

### Block 5 — H2

Jewelry gift ideas for your wife, by style

### Block 6 — H3

If her style is classic

### Block 7 — Bullet

- **Diamond stud earrings.** The most versatile diamond gift. They go with everything, and she'll wear them daily.
- **A solitaire pendant.** A single diamond on a fine chain. Simple, elegant and easy to wear with her other jewelry.

### Block 8 — H3

If her style is modern and minimal

### Block 9 — Bullet

- **Diamond huggies.** Small hoops that hug the earlobe. Everyday sparkle that's more current than studs.
- **A bezel-set pendant.** The diamond is held in a smooth metal rim rather than prongs, which gives a clean, contemporary look.

### Block 10 — H3

If she loves a statement

### Block 11 — Bullet

- **A diamond tennis bracelet.** An unbroken row of diamonds around the wrist: a statement piece she can still wear to work.
- **Diamond hoops or drop earrings.** More movement and presence than studs, for evenings and events.

### Block 12 — H3

If you want it to be meaningful

### Block 13 — Bullet

- **A heart pendant.** The most direct way to say what the gift means.
- **An eternity or half-eternity band.** It sits beside her engagement ring and wedding band, so it's part of the set she wears every day. It's the most traditional anniversary gift, but it needs her exact ring size.
- **A piece that marks a number.** Ten diamonds for ten years, or one diamond for each child: a detail that turns a classic piece into a personal one.

### Block 14 — H2

The no-ring-size-risk rule

### Block 15 — Paragraph

If you're not sure of her ring size, **choose earrings, a pendant or a bracelet**. None of them needs a ring size, so there's no risk of a ring that doesn't fit on the day.

### Block 16 — Paragraph

If you do choose a ring, measure a ring she already wears on the **same finger**, because ring sizes can differ between fingers and between hands.

### Block 17 — H2

Jewelry gifts for a wife who has everything

### Block 18 — Paragraph

When she already owns the classics, these ideas still feel new:

### Block 19 — Bullet

- **Upgrade a piece she wears every day.** Larger studs, or a more substantial pendant than the one she wears now.
- **Complete a set.** A pendant to match the earrings she loves, or a bracelet in the same metal as her rings.
- **Add to her ring stack.** A half-eternity band that sits beside her rings.
- **Choose a different shape.** If all her diamonds are round, an oval, pear or emerald-cut piece adds something different.

### Block 20 — H2

Matching the gift to the occasion

### Block 21 — Bullet *(converted from table)*

- **Christmas.** *Strong choices:* Diamond studs, a pendant or a tennis bracelet. *Why:* Easy to wear straight away, and no sizing risk.
- **Anniversary.** *Strong choices:* An eternity or half-eternity band, or a tennis bracelet. *Why:* Lasting pieces that mark the years.
- **Birthday.** *Strong choices:* A pendant or earrings in her style. *Why:* Personal, and something she'll wear daily.
- **A new baby.** *Strong choices:* Studs or a pendant. *Why:* Practical for life with a newborn.
- **Just because.** *Strong choices:* Huggies or a delicate pendant. *Why:* A small surprise she'll actually wear.

### Block 22 — H2

Christmas gifts for your wife: plan ahead

### Block 23 — Paragraph

The easiest way to get a Christmas jewelry gift right is to choose it before the holiday rush. Check the product page and our [shipping page](https://www.houseofdiams.com/shipping) for current delivery details, and read the [returns policy](https://www.houseofdiams.com/returns) before you order. For more Christmas ideas across every budget, see our [holiday jewelry gift guide](https://www.houseofdiams.com/blog/christmas-jewelry-gifts-a-holiday-gift-guide).

### Block 24 — H2

More questions about jewelry gifts for your wife

### Block 25 — Paragraph

**What is the most meaningful jewelry gift for a wife?** A piece that connects to your marriage: an eternity band beside her rings, or a pendant that marks a number that matters to you both, such as ten diamonds for ten years.

### Block 26 — Paragraph

**Should I buy my wife a ring as a gift?** Only if you know her ring size and her style. A ring is the riskiest jewelry gift to get wrong; earrings and pendants are safer.

### Block 27 — Paragraph

**How much should I spend on jewelry for my wife?** There's no correct amount. It's better to spend on a well-cut diamond in a design she'll wear than on the largest stone you can afford in a piece she won't.

### Block 28 — H2

Shop jewelry gifts for your wife

### Block 29 — Paragraph

Start with what she wears most: [earrings to give](https://www.houseofdiams.com/fine-jewellery/earrings), [necklaces and pendants](https://www.houseofdiams.com/fine-jewellery/necklaces), [bracelets for every occasion](https://www.houseofdiams.com/fine-jewellery/bracelet), or [wedding bands](https://www.houseofdiams.com/wedding-bands) to sit beside her engagement ring.

### Block 30 — Divider

— (horizontal rule)

### Block 31 — Paragraph

**About the author**

### Block 32 — Paragraph

**HOD Team.** The team behind House of Diams shares insights into bespoke engagement rings, diamond selection, and the process of bringing a ring design to life.
