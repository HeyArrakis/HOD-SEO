# BC-018 — Article Content (CMS formatting map)

**Source:** `blogs/bc-018/BC-018-anniversary-gifts-by-year-traditional-and-modern.md`. The wording is unchanged.

## How to enter it (recommended: paste)

The **Article Content** editor (TipTap) has no link button, and it doesn't support tables. The most reliable way to enter the article is a rich-text paste:

1. Open `bc-018/article-content.html` in Chrome.
2. Press **Cmd+A**, then **Cmd+C**.
3. Click into **Article Content** in the CMS and press **Cmd+V**.

The pasted content keeps the H2, H3, bold, italic, bullet lists, numbered lists, horizontal rule and links. It uses only tags the editor and the storefront sanitizer accept: `p, h2, h3, strong, em, ul, ol, li, a, hr`.

**After pasting, check:**
- **No H1 inside Article Content.** The storefront renders the H1 from **Display Title**.
- **No breadcrumb or byline in the body.** The page template renders "Back to Journal" and the **Written By** value.
- **5 live links**, each clickable, with the correct href (see `internal-links.md`).
- **1 conditional anchor(s)** are **plain text, not links**: "eternity ring meaning".
- **"10 year anniversary gift ideas"** links to BC-035 (`/blog/10-year-anniversary-gift-ideas-tin-and-diamond`). BC-035 is scheduled before this post; confirm that URL loads before publishing. If BC-035 isn't live yet, publish BC-035 first (it's scheduled earlier) or hold this post until it is.
- **No heading reads "FAQ" or "Frequently asked questions".** The storefront auto-generates FAQPage schema under such a heading; the Q&A heading in this article is worded to avoid that.

## What changed for the CMS (formatting only)

| Source element | CMS treatment | Why |
|---|---|---|
| H1 | Not in Article Content; goes in **Display Title** | `BlogPostBody` renders the H1 from the title fields |
| Breadcrumb line, "*By HOD Team*" | Not in Article Content | The template provides "Back to Journal" and the author meta |
| 2 table(s) | Converted to bullet lists. Column headings become inline labels in italics (e.g. "*Traditional gift:*"); in comparison tables with an empty first heading, each column becomes a bold label followed by a list. All cell text is kept word for word; only separating punctuation was added. | `sanitizeRichText` strips table tags, and the editor has no table extension |
| Relative links | Absolute `https://www.houseofdiams.com/...` | A browser copy from a local file turns relative links into `file:///` links. These are the same destinations. |
| `[CONDITIONAL]` links | Anchor kept as plain text | The target pages aren't live yet |
| "---" before About the author | Horizontal rule | Same as the source |

**Verified:** generated programmatically from the approved source and compared block by block. Article Content is about **1075 words** (including converted table labels).

## Block-by-block map

Use this as a fallback if you build the content by hand, or to check the paste.

### Block 1 — Paragraph

Anniversary gifts by year follow two lists. The **traditional list** assigns a material to each anniversary: paper for the 1st, wood for the 5th, tin for the 10th, silver for the 25th, gold for the 50th and diamond for the 60th. The **modern list**, used widely in the US, updates many of the early years, for example clocks for the 1st, diamond jewelry for the 10th and platinum for the 20th. Neither list is an official rule, and the details vary slightly from source to source.

### Block 2 — Paragraph

The full list is below, followed by short answers for the diamond, gold and platinum years.

### Block 3 — H2

Where the anniversary gift lists come from

### Block 4 — Paragraph

Some anniversary materials are long-standing customs: paper for the first anniversary, wood for the fifth and tin for the tenth were already being recommended in the nineteenth century. In 1937, the American National Retail Jewelers Association (today Jewelers of America) published an expanded list that gave a theme to many more years. The "modern" list grew later, as retailers and publishers suggested updated themes for the early years.

### Block 5 — Paragraph

That history explains two things you'll notice when you compare lists: many milestone years are fairly consistent, and the in-between years vary more.

### Block 6 — H2

The full list: traditional and modern anniversary gifts by year

### Block 7 — Bullet *(converted from table)*

- **1st.** *Traditional gift:* Paper. *Modern gift:* Clocks.
- **2nd.** *Traditional gift:* Cotton. *Modern gift:* China.
- **3rd.** *Traditional gift:* Leather. *Modern gift:* Crystal or glass.
- **4th.** *Traditional gift:* Fruit or flowers. *Modern gift:* Appliances.
- **5th.** *Traditional gift:* Wood. *Modern gift:* Silverware.
- **6th.** *Traditional gift:* Iron or candy. *Modern gift:* Wood.
- **7th.** *Traditional gift:* Wool or copper. *Modern gift:* Desk sets.
- **8th.** *Traditional gift:* Bronze or pottery. *Modern gift:* Linen or lace.
- **9th.** *Traditional gift:* Pottery or willow. *Modern gift:* Leather.
- **10th.** *Traditional gift:* Tin or aluminum. *Modern gift:* Diamond jewelry.
- **11th.** *Traditional gift:* Steel. *Modern gift:* Fashion jewelry.
- **12th.** *Traditional gift:* Silk or linen. *Modern gift:* Pearls.
- **13th.** *Traditional gift:* Lace. *Modern gift:* Textiles or furs.
- **14th.** *Traditional gift:* Ivory. *Modern gift:* Gold jewelry.
- **15th.** *Traditional gift:* Crystal. *Modern gift:* Watches.
- **20th.** *Traditional gift:* China. *Modern gift:* Platinum.
- **25th.** *Traditional gift:* Silver. *Modern gift:* Silver.
- **30th.** *Traditional gift:* Pearl. *Modern gift:* Diamond.
- **35th.** *Traditional gift:* Coral. *Modern gift:* Jade.
- **40th.** *Traditional gift:* Ruby. *Modern gift:* Ruby.
- **45th.** *Traditional gift:* Sapphire. *Modern gift:* Sapphire.
- **50th.** *Traditional gift:* Gold. *Modern gift:* Gold.
- **55th.** *Traditional gift:* Emerald. *Modern gift:* Emerald.
- **60th.** *Traditional gift:* Diamond. *Modern gift:* Diamond.
- **75th.** *Traditional gift:* Diamond or gold. *Modern gift:* Diamond or gold.

### Block 8 — Paragraph

A few notes on reading the list:

### Block 9 — Bullet

- **Variations are normal.** Some lists give candy for the 6th, willow for the 9th or a different modern gift for the 60th. Follow the one that suits you.
- **The 14th (ivory)** is now usually interpreted as an ivory color or theme rather than the material itself.
- **After the 15th, most lists jump in five-year steps.** The milestone years are the ones most couples mark.

### Block 10 — H2

What anniversary is diamond?

### Block 11 — Paragraph

**The 60th anniversary is the traditional diamond anniversary**, and some lists also name diamond for the 75th. On the modern list, **diamond jewelry is the gift for the 10th anniversary**, and diamond also appears for the 30th.

### Block 12 — Paragraph

So diamonds can mark three very different points in a marriage: the first decade, the thirtieth year and a lifetime together. If you're planning for the 10th, see our [10 year anniversary gift ideas](https://www.houseofdiams.com/blog/10-year-anniversary-gift-ideas-tin-and-diamond).

### Block 13 — H2

What is the 50th anniversary gift?

### Block 14 — Paragraph

**Gold is the 50th anniversary gift** on both the traditional and the modern list, which is why the 50th is called the golden anniversary. Gold jewelry also appears on the modern list for the 14th anniversary.

### Block 15 — H2

What is the 60th anniversary gift?

### Block 16 — Paragraph

**Diamond is the 60th anniversary gift**, which is why the 60th is known as the diamond anniversary. A diamond piece that can be passed down, such as a pendant or a pair of studs, suits a milestone this rare.

### Block 17 — H2

What is the 20th anniversary gift?

### Block 18 — Paragraph

**China is the traditional 20th anniversary gift, and platinum is the modern one.** Platinum is a dense, durable white metal, which suits a marriage that has lasted two decades. Some lists outside the US also name platinum for the 70th anniversary.

### Block 19 — H2

Silver, pearl and ruby: the other milestone years

### Block 20 — Bullet

- **25th: silver.** The silver anniversary is the first of the big milestones on most lists.
- **30th: pearl** on the traditional list, **diamond** on the modern list.
- **40th: ruby** on both lists.
- **45th: sapphire** and **55th: emerald**, again on both lists.

### Block 21 — H2

Anniversary jewelry: the years that suit diamonds and fine jewelry

### Block 22 — Paragraph

If you'd like to give jewelry, these are the years where it fits the tradition most naturally:

### Block 23 — Bullet *(converted from table)*

- **10th.** *Theme:* Diamond jewelry (modern) *Jewelry that fits:* Diamond studs, a pendant, an eternity band or a tennis bracelet.
- **11th.** *Theme:* Fashion jewelry (modern) *Jewelry that fits:* An everyday piece in her usual style.
- **14th.** *Theme:* Gold jewelry (modern) *Jewelry that fits:* A gold pendant, hoops or a bracelet.
- **25th.** *Theme:* Silver. *Jewelry that fits:* A white-metal piece, or diamonds set in white gold.
- **30th.** *Theme:* Diamond (modern) *Jewelry that fits:* A larger diamond piece, or an eternity band.
- **50th.** *Theme:* Gold. *Jewelry that fits:* Gold jewelry, with or without diamonds.
- **60th.** *Theme:* Diamond. *Jewelry that fits:* A diamond heirloom piece.

### Block 24 — Paragraph

You don't have to wait for a "jewelry year". Many couples mark any anniversary with an eternity or half-eternity band that sits beside the engagement ring. For more on that tradition, see eternity ring meaning.

### Block 25 — H2

How to use the list without being too literal

### Block 26 — Paragraph

The lists work best as a starting point, not a rulebook:

### Block 27 — Numbered

1. **Use the theme as an idea, not a requirement.** A 5th anniversary "wood" gift can be a wooden jewelry box with something inside it.
2. **Combine the traditional and modern gifts.** A tin box holding a diamond piece marks the 10th both ways.
3. **Match the gift to the person.** A theme only works if the gift is something they'll use or wear.
4. **Save the bigger gifts for the milestones.** Most couples mark the 10th, 25th, 40th, 50th and 60th more than the years in between.

### Block 28 — H2

Shop anniversary jewelry

### Block 29 — Paragraph

For the diamond and gold years, or any anniversary you'd like to mark with something lasting, explore [wedding bands](https://www.houseofdiams.com/wedding-bands) to wear beside her rings, [earrings to give](https://www.houseofdiams.com/fine-jewellery/earrings), [necklaces and pendants](https://www.houseofdiams.com/fine-jewellery/necklaces) and [bracelets for every occasion](https://www.houseofdiams.com/fine-jewellery/bracelet).

### Block 30 — Divider

— (horizontal rule)

### Block 31 — Paragraph

**About the author**

### Block 32 — Paragraph

**HOD Team.** The team behind House of Diams shares insights into bespoke engagement rings, diamond selection, and the process of bringing a ring design to life.
