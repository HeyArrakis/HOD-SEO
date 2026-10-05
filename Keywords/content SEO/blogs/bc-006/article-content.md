# BC-006 — Article Content (CMS formatting map)

**Source:** `blogs/bc-006/BC-006-necklace-layering-how-to-layer-necklaces.md`. The wording is unchanged.

## How to enter it (recommended: paste)

The **Article Content** editor (TipTap) has no link button, and it doesn't support tables. The most reliable way to enter the article is a rich-text paste:

1. Open `bc-006/article-content.html` in Chrome.
2. Press **Cmd+A**, then **Cmd+C**.
3. Click into **Article Content** in the CMS and press **Cmd+V**.

The pasted content keeps the H2, H3, bold, italic, bullet lists, numbered lists, horizontal rule and links. It uses only tags the editor and the storefront sanitizer accept: `p, h2, h3, strong, em, ul, ol, li, a, hr`.

**After pasting, check:**
- **No H1 inside Article Content.** The storefront renders the H1 from **Display Title**.
- **No breadcrumb or byline in the body.** The page template renders "Back to Journal" and the **Written By** value.
- **4 live links**, each clickable, with the correct href (see `internal-links.md`).
- **2 conditional anchor(s)** are **plain text, not links**: "necklace length chart", "a guide to jewelry metals".
- **No heading reads "FAQ" or "Frequently asked questions".** The storefront auto-generates FAQPage schema under such a heading; the Q&A heading in this article is worded to avoid that.

## What changed for the CMS (formatting only)

| Source element | CMS treatment | Why |
|---|---|---|
| H1 | Not in Article Content; goes in **Display Title** | `BlogPostBody` renders the H1 from the title fields |
| Breadcrumb line, "*By HOD Team*" | Not in Article Content | The template provides "Back to Journal" and the author meta |
| 3 table(s) | Converted to bullet lists. Column headings become inline labels in italics (e.g. "*Where it usually sits:*"); in comparison tables with an empty first heading, each column becomes a bold label followed by a list. All cell text is kept word for word; only separating punctuation was added. | `sanitizeRichText` strips table tags, and the editor has no table extension |
| Relative links | Absolute `https://www.houseofdiams.com/...` | A browser copy from a local file turns relative links into `file:///` links. These are the same destinations. |
| `[CONDITIONAL]` links | Anchor kept as plain text | The target pages aren't live yet |
| "---" before About the author | Horizontal rule | Same as the source |

**Verified:** generated programmatically from the approved source and compared block by block. Article Content is about **1044 words** (including converted table labels).

## Block-by-block map

Use this as a fallback if you build the content by hand, or to check the paste.

### Block 1 — Paragraph

To layer necklaces, wear **two to four necklaces at clearly different lengths, about 2 inches apart**, with the **finest chain at the top and the heaviest chain or pendant at the bottom**. The spacing keeps each necklace visible, and putting the weight at the bottom helps the layers hang separately instead of twisting together.

### Block 2 — Paragraph

Everything else in necklace layering, from mixing metals to choosing a focal pendant, builds on those two rules.

### Block 3 — H2

The five rules of necklace layering

### Block 4 — Numbered

1. **Space the lengths.** Leave about 1–2 inches between each necklace, and closer to 2 inches with pendants. Necklaces of the same length sit on top of each other and tangle.
2. **Go light to heavy.** Put the most delicate chain highest and the heaviest chain or largest pendant lowest. Weight at the bottom pulls the stack into place.
3. **Choose one focal point.** Let one piece, usually a pendant, be the star. The other layers frame it.
4. **Vary the texture.** Mixing a fine chain with a more structured one, or a plain chain with a diamond-set piece, keeps the stack from looking flat.
5. **Keep the metals intentional.** One metal throughout always works. If you mix metals, let one dominate, or repeat each metal more than once so the mix looks planned.

### Block 5 — H2

Necklace layering lengths: where each length sits

### Block 6 — Paragraph

Necklace lengths are measured end to end, including the clasp. Where a length sits depends on your neck size and build, so treat these positions as a guide:

### Block 7 — Bullet *(converted from table)*

- **14 inches.** *Where it usually sits:* High on the neck, like a choker. *Role in a layered stack:* The top layer, for a fine chain.
- **16 inches.** *Where it usually sits:* Around the base of the neck. *Role in a layered stack:* A fine chain, or a small pendant.
- **18 inches.** *Where it usually sits:* Just below the collarbone. *Role in a layered stack:* The most common pendant length, often the focal layer.
- **20 inches.** *Where it usually sits:* A little below the collarbone. *Role in a layered stack:* A second pendant, or a station necklace.
- **22–24 inches.** *Where it usually sits:* Around the top of the chest. *Role in a layered stack:* The bottom layer, with a heavier chain or pendant.

### Block 8 — Paragraph

A classic three-layer stack uses **16, 18 and 20 inches**: a fine chain, a pendant, and a longer chain or second pendant. For a full guide to how each length looks and how to measure, see the necklace length chart.

### Block 9 — H2

How to layer necklaces, step by step

### Block 10 — Numbered

1. **Start with your anchor piece.** Choose the necklace you wear most, usually a pendant, and set it at around 18 inches.
2. **Add a shorter, finer chain.** A delicate chain at 16 inches frames the neckline without competing with the pendant.
3. **Add a longer layer.** A chain, station necklace or second pendant at 20–22 inches completes the stack.
4. **Check it against your neckline.** Put on the top you'll wear and adjust the lengths so each layer sits clearly on skin or fabric.
5. **Edit.** If the stack feels busy, remove one layer. Two well-spaced necklaces look better than four crowded ones.

### Block 11 — H2

Necklace layering ideas: three stacks that work

### Block 12 — Bullet *(converted from table)*

- **Everyday two-layer.** *Layers:* A fine chain at 16 inches + a solitaire pendant at 18 inches. *Why it works:* Simple, wears with anything and rarely tangles.
- **Classic three-layer.** *Layers:* A fine chain at 16 inches + a pendant at 18 inches + a station necklace or longer chain at 20 inches. *Why it works:* Balanced spacing with one clear focal point.
- **Lariat-led.** *Layers:* A fine chain at 16 inches + a lariat. *Why it works:* The lariat's drop creates its own vertical line, so you need fewer layers.

### Block 13 — Paragraph

Diamond pieces work well in any of these, as the focal pendant or as a station necklace that adds sparkle along the chain. For example, a lariat such as the [Diamond Leaf Tassel Lariat Necklace](https://www.houseofdiams.com/shop/diamond-leaf-tassel-lariat-necklace) can lead a stack on its own, and a station design such as the [Celestine Dewdrop Pear Diamond Station Necklace](https://www.houseofdiams.com/shop/celestine-dewdrop-pear-diamond-station-necklace) can sit beneath a fine chain.

### Block 14 — H2

How to keep layered necklaces from tangling

### Block 15 — Paragraph

Layered necklaces tangle when chains of similar length and weight slide over each other. To stop it:

### Block 16 — Bullet

- **Keep the spacing.** About 2 inches between layers is the single most effective fix.
- **Add weight to the lower layers.** A pendant or a heavier chain keeps the bottom layers hanging straight.
- **Mix chain styles.** Very fine, flexible chains twist easily. Flatter or more structured chains, such as box, snake or paperclip chains, tend to hold their shape better.
- **Use a layering clasp.** A multi-strand connector, sometimes called a necklace separator, holds the clasps apart at the back of the neck.
- **Put them on one at a time.** Start with the shortest necklace and finish with the longest.
- **Store them separately.** Hang them, or keep each one in its own pouch, so they don't knot in the jewelry box.

### Block 17 — H2

Layering necklaces with different necklines

### Block 18 — Bullet *(converted from table)*

- **V-neck.** *How to layer:* Follow the V with a pendant at the bottom of the stack.
- **Scoop or square neck.** *How to layer:* Almost any stack works; the open neckline gives every layer space.
- **Crew neck.** *How to layer:* Keep the layers above the neckline, or wear a longer stack over the fabric.
- **Turtleneck.** *How to layer:* Wear longer necklaces over the top, and skip short chains.
- **Open-collar shirt.** *How to layer:* Keep a short stack of two layers inside the collar.

### Block 19 — H2

Can you mix metals when layering necklaces?

### Block 20 — Paragraph

Yes, as long as it looks intentional. Yellow, white and rose gold can all sit together. The easiest way is to let one metal make up most of the stack, or to repeat each metal more than once. If you're deciding which metal to build around, see a guide to jewelry metals.

### Block 21 — H2

Building a layered look with diamond necklaces

### Block 22 — Paragraph

A layered stack doesn't need many pieces. One diamond pendant at 18 inches, framed by a fine chain above and a longer layer below, is enough to look finished. Start with the piece you'll wear most, then add layers around it.

### Block 23 — Paragraph

Explore [necklaces and pendants](https://www.houseofdiams.com/fine-jewellery/necklaces) to find your focal piece, or browse [the full fine jewelry collection](https://www.houseofdiams.com/fine-jewellery).

### Block 24 — Divider

— (horizontal rule)

### Block 25 — Paragraph

**About the author**

### Block 26 — Paragraph

**HOD Team.** The team behind House of Diams shares insights into bespoke engagement rings, diamond selection, and the process of bringing a ring design to life.
