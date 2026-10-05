# BC-035 — Article Content (CMS formatting map)

**Source:** `blogs/bc-035/BC-035-10-year-anniversary-gift-ideas-tin-and-diamond.md`. The wording is unchanged.

## How to enter it (recommended: paste)

The **Article Content** editor (TipTap) has no link button, and it doesn't support tables. The most reliable way to enter the article is a rich-text paste:

1. Open `bc-035/article-content.html` in Chrome.
2. Press **Cmd+A**, then **Cmd+C**.
3. Click into **Article Content** in the CMS and press **Cmd+V**.

The pasted content keeps the H2, H3, bold, italic, bullet lists, numbered lists, horizontal rule and links. It uses only tags the editor and the storefront sanitizer accept: `p, h2, h3, strong, em, ul, ol, li, a, hr`.

**After pasting, check:**
- **No H1 inside Article Content.** The storefront renders the H1 from **Display Title**.
- **No breadcrumb or byline in the body.** The page template renders "Back to Journal" and the **Written By** value.
- **8 live links**, each clickable, with the correct href (see `internal-links.md`).
- **2 conditional anchor(s)** are **plain text, not links**: "anniversary gifts by year", "eternity ring meaning and styles".
- **No heading reads "FAQ" or "Frequently asked questions".** The storefront auto-generates FAQPage schema under such a heading; the Q&A heading in this article is worded to avoid that.

## What changed for the CMS (formatting only)

| Source element | CMS treatment | Why |
|---|---|---|
| H1 | Not in Article Content; goes in **Display Title** | `BlogPostBody` renders the H1 from the title fields |
| Breadcrumb line, "*By HOD Team*" | Not in Article Content | The template provides "Back to Journal" and the author meta |
| 1 table(s) | Converted to bullet lists. Column headings become inline labels in italics (e.g. "*Traditional:*"); in comparison tables with an empty first heading, each column becomes a bold label followed by a list. All cell text is kept word for word; only separating punctuation was added. | `sanitizeRichText` strips table tags, and the editor has no table extension |
| Relative links | Absolute `https://www.houseofdiams.com/...` | A browser copy from a local file turns relative links into `file:///` links. These are the same destinations. |
| `[CONDITIONAL]` links | Anchor kept as plain text | The target pages aren't live yet |
| "---" before About the author | Horizontal rule | Same as the source |

**Verified:** generated programmatically from the approved source and compared block by block. Article Content is about **884 words** (including converted table labels).

## Block-by-block map

Use this as a fallback if you build the content by hand, or to check the paste.

### Block 1 — Paragraph

The **traditional 10 year anniversary gift is tin or aluminum**, and the **modern 10th anniversary gift is diamond jewelry**. Many anniversary gemstone lists also name diamond for the 10th year. You can follow either tradition, or combine them: a diamond piece presented in an engraved tin box marks both.

### Block 2 — Paragraph

Ten years is the first decade-long milestone in a marriage, and many couples mark it more than the years around it. The ideas below are grouped the same way the traditions are: modern diamond gifts, traditional tin and aluminum gifts, and sentimental gifts and experiences.

### Block 3 — H2

10th anniversary gifts: traditional vs. modern

### Block 4 — Paragraph *(converted from table)*

**Traditional**

### Block 5 — Bullet *(converted from table)*

- **Material:** Tin or aluminum
- **What it's said to represent:** Durability, and a bond that can bend without breaking
- **Typical gifts:** Engraved keepsakes, metal prints, a tin box of letters
- **Best for:** A thoughtful, personal or lower-cost gift

### Block 6 — Paragraph *(converted from table)*

**Modern**

### Block 7 — Bullet *(converted from table)*

- **Material:** Diamond jewelry
- **What it's said to represent:** Strength and permanence: a decade that has lasted
- **Typical gifts:** Diamond studs, a pendant, an eternity band or a tennis bracelet
- **Best for:** A lasting gift you'll see worn every day

### Block 8 — Paragraph

Neither list is an official rule. Both are customs, and lists vary slightly from source to source. Choose the one that suits the person, not the one that looks most correct.

### Block 9 — H2

Modern diamond gift ideas for your 10th anniversary

### Block 10 — Paragraph

Diamond jewelry fits the 10th anniversary well, because a decade-long marriage is exactly what diamonds have come to stand for: something that lasts. These are the pieces that work best as 10 year anniversary gifts for a wife.

### Block 11 — H3

An eternity or half-eternity band

### Block 12 — Paragraph

An eternity band has diamonds set all the way around; a half-eternity band has them across the top half only. Either can be worn beside an engagement ring and wedding band, or on its own. It's a classic anniversary gift, but it does need her exact ring size. Browse [wedding bands to pair with her rings](https://www.houseofdiams.com/wedding-bands). For the difference between full and half designs, see eternity ring meaning and styles.

### Block 13 — H3

Diamond stud earrings

### Block 14 — Paragraph

Studs are the safest diamond gift: no ring size, worn daily and easy to match with everything else she owns. If she already has a small pair, a larger pair marks the milestone. Browse [earrings to give](https://www.houseofdiams.com/fine-jewellery/earrings).

### Block 15 — H3

A diamond pendant

### Block 16 — Paragraph

A solitaire or heart pendant sits close to the heart and suits almost any style. For a 10th anniversary, a pendant with ten small diamonds, one for each year, turns a classic gift into a personal one. Browse [necklaces and pendants](https://www.houseofdiams.com/fine-jewellery/necklaces).

### Block 17 — H3

A diamond tennis bracelet

### Block 18 — Paragraph

A tennis bracelet is a continuous line of diamonds. It feels like an occasion but still wears every day, which makes it a strong choice for a milestone. Measure a bracelet she already wears so the fit is right. Browse [bracelets for every occasion](https://www.houseofdiams.com/fine-jewellery/bracelet).

### Block 19 — H2

Traditional tin and aluminum gift ideas

### Block 20 — Paragraph

Tin and aluminum are inexpensive metals, so the value of a traditional gift lies in the thought behind it. Ideas that work well:

### Block 21 — Bullet

- an engraved aluminum print of the place you met or married
- a tin keepsake box holding ten letters, one for each year
- a hammered tin or aluminum tray or vase engraved with your wedding date
- an aluminum-framed photo from each year of your marriage

### Block 22 — H2

Sentimental and experience ideas

### Block 23 — Paragraph

Some couples prefer to mark ten years with time together rather than an object:

### Block 24 — Bullet

- revisit the place you got engaged or married
- plan a trip you've talked about for years
- book a portrait session to capture where you are now
- make a photo book of the decade

### Block 25 — H2

Combine the traditions: tin and diamond

### Block 26 — Paragraph

The most memorable 10th anniversary gifts often use both lists. Give a diamond piece inside an engraved tin box, or pair diamond studs with ten letters, one written for each year. The tin honors tradition; the diamond is the piece she'll keep wearing.

### Block 27 — H2

10 year anniversary gifts for a couple

### Block 28 — Paragraph

If you're buying for a couple, or for both of you, choose something shared: an experience, a framed print, or a trip. Diamond jewelry is usually a gift from one partner to the other rather than something friends or family give to a couple.

### Block 29 — H2

How to choose the right diamond gift

### Block 30 — Paragraph

Before you buy, check three things:

### Block 31 — Numbered

1. **What she wears most.** Earrings, necklaces, bracelets or rings? Choose the type she already reaches for.
2. **Her metal color.** Match the yellow, white or rose gold she wears every day.
3. **Whether you need a size.** Earrings and pendants don't; bands and bracelets do.

### Block 32 — Paragraph

For the materials and gifts for every other year, see the full list of anniversary gifts by year.

### Block 33 — H2

10th anniversary questions, answered

### Block 34 — Paragraph

**What represents 10 years of marriage?** Tin or aluminum on the traditional list, and diamond on the modern list.

### Block 35 — Paragraph

**What stone is the 10th anniversary?** Diamond is the gemstone most commonly given for the 10th anniversary.

### Block 36 — Paragraph

**Is a 10 year anniversary a big deal?** For many couples, yes. It's the first decade-long milestone, and the next big markers on most lists are the 15th (crystal) and 20th (china).

### Block 37 — H2

Shop diamond anniversary gifts

### Block 38 — Paragraph

Ten years deserves a gift she'll wear for the next ten. Explore [Wedding Bands](https://www.houseofdiams.com/wedding-bands), [Earrings](https://www.houseofdiams.com/fine-jewellery/earrings), [Necklaces & Pendants](https://www.houseofdiams.com/fine-jewellery/necklaces) and [Bracelets](https://www.houseofdiams.com/fine-jewellery/bracelet).

### Block 39 — Divider

— (horizontal rule)

### Block 40 — Paragraph

**About the author**

### Block 41 — Paragraph

**HOD Team.** The team behind House of Diams shares insights into bespoke engagement rings, diamond selection, and the process of bringing a ring design to life.
