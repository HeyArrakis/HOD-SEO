# BC-003 — Article Content (CMS formatting map)

**Source:** `blogs/bc-003/BC-003-push-present-what-it-is-and-jewelry-ideas.md`. The wording is unchanged.

## How to enter it (recommended: paste)

The **Article Content** editor (TipTap) has no link button, and it doesn't support tables. The most reliable way to enter the article is a rich-text paste:

1. Open `bc-003/article-content.html` in Chrome.
2. Press **Cmd+A**, then **Cmd+C**.
3. Click into **Article Content** in the CMS and press **Cmd+V**.

The pasted content keeps the H2, H3, bold, italic, bullet lists, numbered lists, horizontal rule and links. It uses only tags the editor and the storefront sanitizer accept: `p, h2, h3, strong, em, ul, ol, li, a, hr`.

**After pasting, check:**
- **No H1 inside Article Content.** The storefront renders the H1 from **Display Title**.
- **No breadcrumb or byline in the body.** The page template renders "Back to Journal" and the **Written By** value.
- **11 live links**, each clickable, with the correct href (see `internal-links.md`).
- **0 conditional anchor(s)** are **plain text, not links**: none.
- **No heading reads "FAQ" or "Frequently asked questions".** The storefront auto-generates FAQPage schema under such a heading; the Q&A heading in this article is worded to avoid that.

## What changed for the CMS (formatting only)

| Source element | CMS treatment | Why |
|---|---|---|
| H1 | Not in Article Content; goes in **Display Title** | `BlogPostBody` renders the H1 from the title fields |
| Breadcrumb line, "*By HOD Team*" | Not in Article Content | The template provides "Back to Journal" and the author meta |
| 1 table(s) | Converted to bullet lists. Column headings become inline labels in italics (e.g. "*Why couples choose it:*"); in comparison tables with an empty first heading, each column becomes a bold label followed by a list. All cell text is kept word for word; only separating punctuation was added. | `sanitizeRichText` strips table tags, and the editor has no table extension |
| Relative links | Absolute `https://www.houseofdiams.com/...` | A browser copy from a local file turns relative links into `file:///` links. These are the same destinations. |
| `[CONDITIONAL]` links | Anchor kept as plain text | The target pages aren't live yet |
| "---" before About the author | Horizontal rule | Same as the source |

**Verified:** generated programmatically from the approved source and compared block by block. Article Content is about **980 words** (including converted table labels).

## Block-by-block map

Use this as a fallback if you build the content by hand, or to check the paste.

### Block 1 — Paragraph

A **push present** is a gift a partner gives a new mother to mark the birth of their baby: a thank-you for pregnancy, labor and delivery. It's also called a push gift. Jewelry is the classic choice, especially diamond studs, a pendant or a band. There's no fixed rule about timing: some partners give it before the birth, some in the hospital, and some in the days or weeks after.

### Block 2 — Paragraph

A push present is a custom, not an obligation. Some couples love the idea, some prefer a different kind of gift, and some skip it altogether.

### Block 3 — H2

What is a push present?

### Block 4 — Paragraph

The name comes from the "push" of labor. The gift recognizes what the mother has been through, from nine months of pregnancy to the birth itself. Many people now use the term more broadly, for any parent welcoming a child, including through adoption or surrogacy.

### Block 5 — Paragraph

**What does a push present mean?** It's a way of saying thank you, and of marking the day your family changed. That's why jewelry is such a common choice: it's something she can wear for years that is tied to that one moment.

### Block 6 — H2

When did push presents become a thing?

### Block 7 — Paragraph

The term "push present" is fairly recent. It became widely used in the United States in the 2000s. Giving a gift to celebrate a birth is much older: one famous example is the diamond necklace Napoleon gave his wife, Marie Louise, in 1811 to celebrate the birth of their son.

### Block 8 — H2

When do you give a push present?

### Block 9 — Paragraph

There's no correct moment. Choose the one that suits you both:

### Block 10 — Bullet *(converted from table)*

- **Before the birth.** *Why couples choose it:* It can be worn or packed in the hospital bag. *Keep in mind:* Avoid rings: fingers often swell late in pregnancy.
- **In the hospital.** *Why couples choose it:* The most traditional moment, right after the birth. *Keep in mind:* Keep it small and easy to put on.
- **Coming home.** *Why couples choose it:* A quieter moment once you're settled. *Keep in mind:* Easier to plan than a hospital handover.
- **In the weeks after.** *Why couples choose it:* Gives you time to choose, and her time to rest. *Keep in mind:* Still marks the birth, and ring sizes have had time to settle.

### Block 11 — H2

Push present ideas: jewelry she'll keep

### Block 12 — H3

Diamond stud earrings

### Block 13 — Paragraph

The classic push present. Studs are safe for life with a newborn, because they sit close to the ear and have nothing for a baby to grab. Browse [earrings to give](https://www.houseofdiams.com/fine-jewellery/earrings).

### Block 14 — H3

A solitaire or heart pendant

### Block 15 — Paragraph

A pendant sits close to the heart and goes with everything. Choose a shorter chain if she'll be holding the baby a lot, since long necklaces are easy for little hands to catch. Browse [necklaces and pendants](https://www.houseofdiams.com/fine-jewellery/necklaces).

### Block 16 — H3

A half-eternity band

### Block 17 — Paragraph

A half-eternity band can sit beside her engagement ring and wedding band, so the birth becomes part of the rings she wears every day. Wait until her ring size has settled before you buy. Here's how to [measure your ring size at home](https://www.houseofdiams.com/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams). Browse [wedding bands to pair with her rings](https://www.houseofdiams.com/wedding-bands).

### Block 18 — H3

A diamond tennis bracelet

### Block 19 — Paragraph

A continuous line of diamonds that marks a big moment. Check her wrist size against a bracelet she owns before you buy. Browse [bracelets for every occasion](https://www.houseofdiams.com/fine-jewellery/bracelet).

### Block 20 — H3

A piece that marks the baby

### Block 21 — Paragraph

A diamond for each child, or a design that reflects the baby's birth date, makes a piece unmistakably personal. For something made to your own design, you can [commission something one of a kind](https://www.houseofdiams.com/bespoke). At House of Diams, a bespoke piece takes about **3–4 weeks on average from design approval to delivery**: typically 2–3 weeks of production and approximately 6–9 days of insured shipping. The timeline can vary depending on the stone selected, so it's an average, not a guarantee. Babies rarely arrive on schedule, so start well before the due date or plan to give it in the weeks after.

### Block 22 — H2

How to choose jewelry for a new mom

### Block 23 — Paragraph

New-parent life is hard on jewelry. A few practical points:

### Block 24 — Bullet

- **Choose smooth, secure designs.** Bezel settings, where a metal rim holds the diamond, are smoother than tall prongs and less likely to snag on clothing or blankets.
- **Keep earrings close to the ear.** Studs and huggies are safer than long drops or large hoops while the baby is small.
- **Be careful with rings.** Fingers often swell during pregnancy and can take a while to settle afterwards. If you want to give a ring, consider giving it later, once her ring size is stable.
- **Match her everyday metal.** She'll wear it most if it goes with the jewelry she already has on.

### Block 25 — H2

Do you have to give a push present?

### Block 26 — Paragraph

No. A push present is a choice, not an expectation, and some people dislike the idea of a gift tied to giving birth. If jewelry doesn't feel right, practical support can be just as meaningful: help with meals, cleaning or night feeds in the first weeks. The best push present is the one that fits the two of you.

### Block 27 — H2

More questions about push presents

### Block 28 — Paragraph

**Who gives the push present?** Usually the partner. Sometimes grandparents or other family members give a gift too.

### Block 29 — Paragraph

**What is a typical push present?** Jewelry is the classic choice, especially diamond studs, a pendant or a band.

### Block 30 — Paragraph

**Is a push present an American thing?** The term became popular in the US, but celebrating a birth with a gift is a much older custom, and similar traditions are described in other cultures.

### Block 31 — H2

Shop push present jewelry

### Block 32 — Paragraph

Once you know which type of piece suits her, start with [necklaces and pendants](https://www.houseofdiams.com/fine-jewellery/necklaces), [earrings to give](https://www.houseofdiams.com/fine-jewellery/earrings), [bracelets for every occasion](https://www.houseofdiams.com/fine-jewellery/bracelet) or [wedding bands](https://www.houseofdiams.com/wedding-bands) to wear beside her rings. For something entirely her own, explore [our bespoke service](https://www.houseofdiams.com/bespoke).

### Block 33 — Divider

— (horizontal rule)

### Block 34 — Paragraph

**About the author**

### Block 35 — Paragraph

**HOD Team.** The team behind House of Diams shares insights into bespoke engagement rings, diamond selection, and the process of bringing a ring design to life.
