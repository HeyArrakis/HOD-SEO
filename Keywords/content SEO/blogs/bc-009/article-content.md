# BC-009 — Article Content (CMS formatting map)

**Source:** `blogs/bc-009/BC-009-jewelry-gifts-for-your-girlfriend-diamond-ideas.md`. The wording is unchanged.

## How to enter it (recommended: paste)

The **Article Content** editor (TipTap) has no link button, and it doesn't support tables. The most reliable way to enter the article is a rich-text paste:

1. Open `bc-009/article-content.html` in Chrome.
2. Press **Cmd+A**, then **Cmd+C**.
3. Click into **Article Content** in the CMS and press **Cmd+V**.

The pasted content keeps the H2, H3, bold, italic, bullet lists, numbered lists, horizontal rule and links. It uses only tags the editor and the storefront sanitizer accept: `p, h2, h3, strong, em, ul, ol, li, a, hr`.

**After pasting, check:**
- **No H1 inside Article Content.** The storefront renders the H1 from **Display Title**.
- **No breadcrumb or byline in the body.** The page template renders "Back to Journal" and the **Written By** value.
- **6 live links**, each clickable, with the correct href (see `internal-links.md`).
- **1 conditional anchor(s)** are **plain text, not links**: "what a promise ring means".
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

**Verified:** generated programmatically from the approved source and compared block by block. Article Content is about **736 words** (including converted table labels).

## Block-by-block map

Use this as a fallback if you build the content by hand, or to check the paste.

### Block 1 — Paragraph

For most girlfriends, the best jewelry gift is a **delicate diamond pendant or a pair of small diamond studs**. Both can be worn every day, neither needs a ring size, and both feel personal without carrying the weight of a ring. Match the piece to the stage of your relationship: simple and wearable for a first Christmas together, more personal the longer you've been together.

### Block 2 — H2

Jewelry gifts by relationship stage

### Block 3 — Bullet *(converted from table)*

- **A few months in.** *Strong choices:* Small diamond studs, or a simple pendant on a fine chain. *Why:* Thoughtful without feeling like too much, too soon.
- **Your first Christmas together.** *Strong choices:* A heart or solitaire pendant, or diamond huggies. *Why:* Personal enough to mark the occasion, and wearable every day.
- **A year or more.** *Strong choices:* Diamond hoops, drop earrings or a slim bracelet. *Why:* You know her style well enough to choose something less obvious.
- **A long-term, serious relationship.** *Strong choices:* A tennis bracelet, a larger pendant, or a promise ring. *Why:* A piece that says you're planning a future together.

### Block 4 — Paragraph

If you're unsure which stage you're in, go one step simpler. A small piece she wears every day means more than a big piece she saves for occasions.

### Block 5 — H2

First Christmas gift for your girlfriend

### Block 6 — Paragraph

A first Christmas together calls for something that marks the moment without overwhelming it. A **pendant** is the classic choice: it sits close to the heart, and she can wear it every day. A **heart pendant** says what the gift means; a **solitaire** is subtler and suits almost any style.

### Block 7 — Paragraph

Diamond **huggies** or **small studs** are just as good if she wears earrings more than necklaces. Whatever you choose, a short handwritten note about why you chose it often matters as much as the piece.

### Block 8 — H2

Meaningful necklaces for your girlfriend

### Block 9 — Paragraph

Necklaces are the easiest jewelry gift to get right, which is why they're also a good choice for a birthday. Three styles that work:

### Block 10 — Bullet

- **A heart pendant**: romantic, and clear about what it means
- **A solitaire pendant**: one diamond on a fine chain; timeless and easy to wear
- **A bezel-set pendant**: the diamond sits in a smooth metal rim, which gives a modern, minimal look

### Block 11 — Paragraph

Choose a chain length she already wears. 16 and 18 inches are common lengths, and 18 inches is the most common pendant length.

### Block 12 — H2

Earrings and bracelets she'll wear every day

### Block 13 — Bullet

- **Diamond studs** suit every style and every day.
- **Huggies** are small hoops that hug the earlobe. They're a little more current than studs.
- **A slim diamond bracelet** is a good choice if she already wears bracelets. Check her wrist size against a bracelet she owns.

### Block 14 — H2

Should you give your girlfriend a ring?

### Block 15 — Paragraph

A ring sends a stronger message than any other piece of jewelry, so choose one only if that's the message you intend. If you want to make a commitment without proposing, a promise ring is the usual choice; see what a promise ring means. If you'd simply like to give jewelry, earrings, a pendant or a bracelet avoid both the sizing risk and the question of what the ring means.

### Block 16 — H2

How to read her style before you buy

### Block 17 — Numbered

1. **Check her metal.** Does she wear yellow, white or rose gold? Match it.
2. **Check what she wears most.** Earrings, necklaces or bracelets? Buy into the habit she already has.
3. **Check that her ears are pierced** before you choose studs, huggies or hoops.
4. **Notice her scale.** If she wears small, delicate pieces, don't jump to a statement piece.

### Block 18 — H2

More questions about jewelry gifts for a girlfriend

### Block 19 — Paragraph

**Is jewelry too much for a new relationship?** Not if you keep it small. A delicate pendant or small studs feel thoughtful rather than intense.

### Block 20 — Paragraph

**What's the best jewelry gift for a girlfriend's birthday?** A necklace in her style, or earrings if she wears them more. Both are easy to wear straight away.

### Block 21 — Paragraph

**What if she doesn't like it?** Read the [returns policy](https://www.houseofdiams.com/returns) before you order, and check our [shipping page](https://www.houseofdiams.com/shipping) for current delivery details, especially before Christmas.

### Block 22 — Paragraph

For more holiday ideas across every budget and recipient, see our [holiday jewelry gift guide](https://www.houseofdiams.com/blog/christmas-jewelry-gifts-a-holiday-gift-guide).

### Block 23 — H2

Shop jewelry gifts for your girlfriend

### Block 24 — Paragraph

Start with the piece that matches what she wears most: [necklaces and pendants](https://www.houseofdiams.com/fine-jewellery/necklaces), [earrings to give](https://www.houseofdiams.com/fine-jewellery/earrings) or [bracelets for every occasion](https://www.houseofdiams.com/fine-jewellery/bracelet).

### Block 25 — Divider

— (horizontal rule)

### Block 26 — Paragraph

**About the author**

### Block 27 — Paragraph

**HOD Team.** The team behind House of Diams shares insights into bespoke engagement rings, diamond selection, and the process of bringing a ring design to life.
