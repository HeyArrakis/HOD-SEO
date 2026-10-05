# BC-007 — Article Content (CMS formatting map)

**Source:** `blogs/bc-007/BC-007-how-to-wear-an-engagement-ring-and-wedding-band.md`. The wording is unchanged.

## How to enter it (recommended: paste)

The **Article Content** editor (TipTap) has no link button, and it doesn't support tables. The most reliable way to enter the article is a rich-text paste:

1. Open `bc-007/article-content.html` in Chrome.
2. Press **Cmd+A**, then **Cmd+C**.
3. Click into **Article Content** in the CMS and press **Cmd+V**.

The pasted content keeps the H2, H3, bold, italic, bullet lists, numbered lists, horizontal rule and links. It uses only tags the editor and the storefront sanitizer accept: `p, h2, h3, strong, em, ul, ol, li, a, hr`.

**After pasting, check:**
- **No H1 inside Article Content.** The storefront renders the H1 from **Display Title**.
- **No breadcrumb or byline in the body.** The page template renders "Back to Journal" and the **Written By** value.
- **4 live links**, each clickable, with the correct href (see `internal-links.md`).
- **1 conditional anchor(s)** are **plain text, not links**: "a guide to jewelry metals".
- **"what finger a wedding ring goes on"** links to BC-036 (`/blog/what-finger-does-a-wedding-ring-go-on`). BC-036 is scheduled before this post; confirm that URL loads before publishing. If BC-036 isn't live yet, publish BC-036 first (it's scheduled earlier) or hold this post until it is.
- **No heading reads "FAQ" or "Frequently asked questions".** The storefront auto-generates FAQPage schema under such a heading; the Q&A heading in this article is worded to avoid that.

## What changed for the CMS (formatting only)

| Source element | CMS treatment | Why |
|---|---|---|
| H1 | Not in Article Content; goes in **Display Title** | `BlogPostBody` renders the H1 from the title fields |
| Breadcrumb line, "*By HOD Team*" | Not in Article Content | The template provides "Back to Journal" and the author meta |
| 2 table(s) | Converted to bullet lists. Column headings become inline labels in italics (e.g. "*How it's worn:*"); in comparison tables with an empty first heading, each column becomes a bold label followed by a list. All cell text is kept word for word; only separating punctuation was added. | `sanitizeRichText` strips table tags, and the editor has no table extension |
| Relative links | Absolute `https://www.houseofdiams.com/...` | A browser copy from a local file turns relative links into `file:///` links. These are the same destinations. |
| `[CONDITIONAL]` links | Anchor kept as plain text | The target pages aren't live yet |
| "---" before About the author | Horizontal rule | Same as the source |

**Verified:** generated programmatically from the approved source and compared block by block. Article Content is about **926 words** (including converted table labels).

## Block-by-block map

Use this as a fallback if you build the content by hand, or to check the paste.

### Block 1 — Paragraph

Traditionally, you wear the **wedding band first**, on your left ring finger closest to your hand, with the **engagement ring on top**. The idea is that the wedding band sits closest to the heart. Plenty of people wear the rings the other way round, or on separate hands, and that's fine too: the order is a tradition, not a rule.

### Block 2 — Paragraph

This guide covers the traditional order, the alternatives, what to do with your engagement ring on the wedding day, and whether to solder your rings together.

### Block 3 — H2

Which ring goes on first: wedding band or engagement ring?

### Block 4 — Paragraph

**The wedding band goes on first** in the traditional order, with the engagement ring stacked above it. The reasoning is symbolic: the wedding band represents the marriage itself, so it sits closest to the heart, and the engagement ring "guards" it from the outside.

### Block 5 — Paragraph

This connects to an old belief that a vein ran from the left ring finger straight to the heart, which is also why the rings are worn on the left hand in the US. For that history, and for wedding ring customs in other countries, see [what finger a wedding ring goes on](https://www.houseofdiams.com/blog/what-finger-does-a-wedding-ring-go-on).

### Block 6 — H2

Ways to wear your engagement ring and wedding band

### Block 7 — Bullet *(converted from table)*

- **Traditional.** *How it's worn:* Wedding band first, engagement ring on top, both on the left ring finger. *Why people choose it:* Keeps the wedding band closest to the heart.
- **Chronological.** *How it's worn:* Engagement ring first, wedding band on top. *Why people choose it:* Follows the order you received them, and suits some ring shapes better.
- **Separate hands.** *How it's worn:* Engagement ring on the right hand, wedding band on the left. *Why people choose it:* Useful when the rings don't sit well together, or to wear each on its own.
- **Band only, day to day.** *How it's worn:* Wedding band daily; engagement ring for occasions. *Why people choose it:* Practical for active work, sport or travel.

### Block 8 — Paragraph

There's no correct answer. Try both orders and choose the one that looks and feels right.

### Block 9 — H2

Do you wear your engagement ring on your wedding day?

### Block 10 — Paragraph

Yes, most people do, but they usually move it for the ceremony so the wedding band can go on first. A common way to do it:

### Block 11 — Numbered

1. **Before the ceremony,** move your engagement ring to your right ring finger, or give it to someone you trust to hold.
2. **During the ceremony,** your partner places the wedding band on your left ring finger, so it takes the place closest to your hand.
3. **After the ceremony,** move your engagement ring back to your left hand and wear it on top of the wedding band.

### Block 12 — Paragraph

If you'd rather keep your engagement ring on, that's fine too. Your partner can slide the wedding band on above it, which gives you the chronological order.

### Block 13 — H2

Should your engagement ring and wedding band match?

### Block 14 — Paragraph

They don't have to match, but they should work together. Three things matter:

### Block 15 — Bullet

- **Fit against each other.** Some engagement rings have a center stone or setting that sits low, which can leave a gap beside a straight band. A curved or contoured band follows the outline of the engagement ring and closes that gap. Bridal sets are designed to sit flush together from the start.
- **Metal.** Matching metals look seamless, but mixed metals can look deliberate and modern. Rings that touch every day can rub against each other over time, which is worth considering when you combine different metals. For help choosing, see a guide to jewelry metals.
- **Style.** A plain band lets the engagement ring stand out; a diamond band adds sparkle to the whole stack. Choose based on whether you want one focal ring or a matched set.

### Block 16 — H2

Should you solder your engagement ring and wedding band together?

### Block 17 — Paragraph

Soldering joins the two rings permanently into one piece. A jeweler fuses them at the point where they touch.

### Block 18 — Paragraph *(converted from table)*

**Soldering them together**

### Block 19 — Bullet *(converted from table)*

- **Alignment:** The rings stay perfectly aligned and don't spin
- **Wear:** The rings no longer rub against each other
- **Flexibility:** You always wear them as a set
- **Resizing and repairs:** Both rings are resized or repaired together
- **Changing your mind:** A jeweler can usually separate them later, but it's extra work

### Block 20 — Paragraph *(converted from table)*

**Keeping them separate**

### Block 21 — Bullet *(converted from table)*

- **Alignment:** The engagement ring can twist or slide out of line
- **Wear:** The rings can rub and wear against each other over time
- **Flexibility:** You can wear either ring on its own
- **Resizing and repairs:** Each ring can be resized or repaired on its own
- **Changing your mind:** Nothing to undo

### Block 22 — Paragraph

If you're unsure, wait. Many couples wear the rings separately for a while first, to be sure of the order and the fit, before deciding whether to solder them.

### Block 23 — H2

Wearing your rings every day

### Block 24 — Bullet

- **Check the fit with both rings on.** Two rings worn together cover more of the finger than one, so the stack can feel snugger than a single ring. Here's how to [measure your ring size at home](https://www.houseofdiams.com/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams).
- **Take them off for heavy work.** Lifting weights, gardening and cleaning with chemicals are all easier on your rings when you're not wearing them.
- **Store them together, but separately.** Keep them in the same place so they don't get lost, but in separate compartments so they don't scratch each other.

### Block 25 — H2

Find the band to wear with your engagement ring

### Block 26 — Paragraph

If you're still choosing, explore [wedding bands to pair with it](https://www.houseofdiams.com/wedding-bands), or [browse engagement rings](https://www.houseofdiams.com/engagement-rings) if you're shopping for both.

### Block 27 — Divider

— (horizontal rule)

### Block 28 — Paragraph

**About the author**

### Block 29 — Paragraph

**HOD Team.** The team behind House of Diams shares insights into bespoke engagement rings, diamond selection, and the process of bringing a ring design to life.
