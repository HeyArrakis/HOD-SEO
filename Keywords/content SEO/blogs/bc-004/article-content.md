# BC-004 — Article Content (CMS formatting map)

**Source:** `blogs/bc-004/BC-004-christmas-jewelry-gifts-a-holiday-gift-guide.md`. The wording is unchanged.

## How to enter it (recommended: paste)

The **Article Content** editor (TipTap) has no link button, and it doesn't support tables. The most reliable way to enter the article is a rich-text paste:

1. Open `bc-004/article-content.html` in Chrome.
2. Press **Cmd+A**, then **Cmd+C**.
3. Click into **Article Content** in the CMS and press **Cmd+V**.

The pasted content keeps the H2, H3, bold, italic, bullet lists, numbered lists, horizontal rule and links. It uses only tags the editor and the storefront sanitizer accept: `p, h2, h3, strong, em, ul, ol, li, a, hr`.

**After pasting, check:**
- **No H1 inside Article Content.** The storefront renders the H1 from **Display Title**.
- **No breadcrumb or byline in the body.** The page template renders "Back to Journal" and the **Written By** value.
- **9 live links**, each clickable, with the correct href (see `internal-links.md`).
- **2 conditional anchor(s)** are **plain text, not links**: "jewelry gifts for your wife", "jewelry gifts for your girlfriend".
- **No heading reads "FAQ" or "Frequently asked questions".** The storefront auto-generates FAQPage schema under such a heading; the Q&A heading in this article is worded to avoid that.

## What changed for the CMS (formatting only)

| Source element | CMS treatment | Why |
|---|---|---|
| H1 | Not in Article Content; goes in **Display Title** | `BlogPostBody` renders the H1 from the title fields |
| Breadcrumb line, "*By HOD Team*" | Not in Article Content | The template provides "Back to Journal" and the author meta |
| 2 table(s) | Converted to bullet lists. Column headings become inline labels in italics (e.g. "*Why it works:*"); in comparison tables with an empty first heading, each column becomes a bold label followed by a list. All cell text is kept word for word; only separating punctuation was added. | `sanitizeRichText` strips table tags, and the editor has no table extension |
| Relative links | Absolute `https://www.houseofdiams.com/...` | A browser copy from a local file turns relative links into `file:///` links. These are the same destinations. |
| `[CONDITIONAL]` links | Anchor kept as plain text | The target pages aren't live yet |
| "---" before About the author | Horizontal rule | Same as the source |

**Verified:** generated programmatically from the approved source and compared block by block. Article Content is about **1256 words** (including converted table labels).

## Block-by-block map

Use this as a fallback if you build the content by hand, or to check the paste.

### Block 1 — Paragraph

The most reliable Christmas jewelry gifts are **diamond stud earrings, a solitaire pendant and a tennis bracelet**. None of them needs a ring size, they go with almost any outfit, and they're the kind of piece people wear every day rather than save for special occasions. If you know the person's taste well, hoops, huggies, a heart pendant or a one-of-a-kind bespoke piece can be more personal choices.

### Block 2 — Paragraph

This guide covers Christmas and Hanukkah. It groups the best diamond jewelry gifts by what they suit, how to spend your budget, who you're buying for, and how much time you have left.

### Block 3 — H2

The best diamond jewelry gifts at a glance

### Block 4 — Bullet *(converted from table)*

- **Diamond stud earrings.** *Why it works:* Classic, discreet and worn daily. *Best for:* A first diamond gift; anyone who wears earrings. *Sizing risk:* None (pierced ears needed)
- **Solitaire or heart pendant.** *Why it works:* Sits close to the heart; easy to wear with anything. *Best for:* Partners, mothers, someone who wears little jewelry. *Sizing risk:* Low (chain length only)
- **Tennis bracelet.** *Why it works:* A continuous line of diamonds; feels like a statement but still wears every day. *Best for:* Milestone gifts, luxury gifts. *Sizing risk:* Medium (wrist size matters)
- **Diamond hoops or huggies.** *Why it works:* A modern everyday look with more sparkle than studs. *Best for:* Someone who already wears earrings daily. *Sizing risk:* None (pierced ears needed)
- **Eternity or half-eternity band.** *Why it works:* Sits beside an engagement ring or on its own. *Best for:* A wife, or a long-term partner. *Sizing risk:* High (needs an exact ring size)
- **Bespoke piece.** *Why it works:* Made to your design, so nobody else has it. *Best for:* Someone with a very specific taste. *Sizing risk:* Depends on the design.

### Block 5 — Paragraph

If you're unsure, choose earrings or a pendant. They carry the least risk of getting the size wrong and the best chance of being worn.

### Block 6 — H2

Christmas jewelry gifts by budget

### Block 7 — Paragraph

There's no right amount to spend on a jewelry gift. What matters more is where the money goes. Prices change, so check current prices on each product page; the table below shows how to approach each budget level instead.

### Block 8 — Bullet *(converted from table)*

- **Keeping it modest.** *What to look at:* Small diamond studs, a delicate solitaire pendant, huggies or a small diamond charm. *Where to put the money:* Choose a well-cut smaller diamond over a larger, poorly cut one. Cut has the biggest effect on how much a diamond sparkles.
- **A considered gift.** *What to look at:* Larger studs, a pendant with a more noticeable center stone, or diamond hoops. *Where to put the money:* Balance size and quality, and pick a design she can wear daily.
- **A statement gift.** *What to look at:* A tennis bracelet, a larger solitaire pendant, an eternity band or a bespoke piece. *Where to put the money:* Ask about the diamond's grading, and choose a design that will still feel right in ten years.

### Block 9 — Paragraph

Before you compare two diamonds on price, it helps to know [how diamonds are graded (the 4Cs)](https://www.houseofdiams.com/blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat-house-of-diams). If size matters more to you than origin, lab-grown diamonds usually cost considerably less than natural diamonds of a similar size and quality.

### Block 10 — H2

Jewelry gifts by recipient

### Block 11 — H3

Christmas jewelry gifts for your wife

### Block 12 — Paragraph

A wife usually already owns the pieces she wears most: her engagement ring, her wedding band and perhaps one favorite necklace. The best gifts sit alongside those rather than compete with them. Diamond studs, a tennis bracelet or an eternity band that stacks with her rings are the classic choices. For ideas by style and occasion, see jewelry gifts for your wife.

### Block 13 — H3

Christmas jewelry gifts for your girlfriend

### Block 14 — Paragraph

For a girlfriend, match the gift to the stage of your relationship. A delicate pendant or small studs suit a first Christmas together; a more personal piece suits a long relationship. A ring can read as a bigger statement than you intend at Christmas, so save it for when that's the point. For ideas by relationship stage, see jewelry gifts for your girlfriend.

### Block 15 — H3

Jewelry gifts for mom

### Block 16 — Paragraph

Mothers often prefer jewelry they can wear every day without thinking about it. A solitaire pendant on a fine chain, diamond studs or a slim bracelet all work. For a more sentimental gift, choose a pendant with a small diamond for each of her children.

### Block 17 — H3

For someone who wears very little jewelry

### Block 18 — Paragraph

Keep it small and simple: small studs or a solitaire pendant on a fine chain. Both are low-profile enough to wear all the time without feeling conspicuous. Avoid statement pieces for someone who doesn't already wear them.

### Block 19 — H3

Luxury jewelry gifts

### Block 20 — Paragraph

If you want the gift to feel like an occasion, a diamond tennis bracelet, larger studs or statement hoops make the biggest impression while staying wearable. For a piece that's entirely theirs, consider a bespoke design (see below).

### Block 21 — H2

Hanukkah jewelry gifts: plan for December 4

### Block 22 — Paragraph

**Hanukkah 2026 begins at sundown on Friday, December 4 and ends on Saturday, December 12.** That's about three weeks earlier than Christmas. If a jewelry gift is meant for the first night, treat December 4 as your deadline, not December 25.

### Block 23 — Paragraph

Everything else in this guide applies: studs, pendants and bracelets avoid sizing problems, and a bespoke piece needs the most lead time. Work back from the night you want to give it.

### Block 24 — H2

Last-minute jewelry gifts and stocking stuffers

### Block 25 — Paragraph

Small pieces make the best jewelry stocking stuffers: diamond studs, huggies, a delicate pendant or a small charm. They fit in a stocking, and they don't need a ring size.

### Block 26 — Paragraph

How much time you need depends on the kind of piece:

### Block 27 — Bullet

- **Ready-to-wear pieces.** Check the product page, then see [delivery details on our shipping page](https://www.houseofdiams.com/shipping) before you order. Holiday transport delays can make shipping take longer than usual, so don't leave it until the last few days.
- **Bespoke pieces.** At House of Diams, a bespoke piece takes about **3–4 weeks on average from design approval to delivery**: typically 2–3 weeks of production, then approximately 6–9 days of insured shipping. Your inquiry and design discussions come before that. The timeline can vary depending on the stone selected, so treat it as an average, not a guaranteed date.

### Block 28 — H2

Getting the details right

### Block 29 — Paragraph

A few checks make a jewelry gift much more likely to land:

### Block 30 — Numbered

1. **Look at what she already wears.** Note the metal color (yellow, white or rose gold) and whether she reaches for earrings, necklaces or bracelets.
2. **Check that her ears are pierced** before you buy studs, huggies or hoops.
3. **Avoid rings unless you know the size.** If you do need a ring size, here's [how to find out a ring size discreetly](https://www.houseofdiams.com/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams).
4. **Measure a bracelet she already owns** if you're choosing a tennis bracelet.
5. **Read the [returns policy](https://www.houseofdiams.com/returns) before you order**, especially for made-to-order pieces.

### Block 31 — H2

A one-of-a-kind gift: bespoke jewelry

### Block 32 — Paragraph

If nothing ready-made feels right, you can [commission something one of a kind](https://www.houseofdiams.com/bespoke). A bespoke piece starts with your idea: a shape, a stone or a design she has mentioned. It's then made to that design. Allow for the 3–4 week average from design approval to delivery, plus the design discussions before it.

### Block 33 — H2

Shop Christmas jewelry gifts by category

### Block 34 — Paragraph

Start with the category that matches what she wears most:

### Block 35 — Bullet

- [Earrings to give](https://www.houseofdiams.com/fine-jewellery/earrings): stud, huggie, hoop and drop earrings
- [Necklaces and pendants](https://www.houseofdiams.com/fine-jewellery/necklaces): solitaire, heart and bezel-set pendants
- [Bracelets for every occasion](https://www.houseofdiams.com/fine-jewellery/bracelet): tennis and link bracelets

### Block 36 — Paragraph

Or browse [the full fine jewelry collection](https://www.houseofdiams.com/fine-jewellery).

### Block 37 — Divider

— (horizontal rule)

### Block 38 — Paragraph

**About the author**

### Block 39 — Paragraph

**HOD Team.** The team behind House of Diams shares insights into bespoke engagement rings, diamond selection, and the process of bringing a ring design to life.
