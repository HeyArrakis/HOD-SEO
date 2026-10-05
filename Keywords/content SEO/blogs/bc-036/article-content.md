# BC-036 — Article Content (CMS formatting map)

**Source:** `blogs/bc-036/BC-036-what-finger-does-a-wedding-ring-go-on.md`. The wording is unchanged.

## How to enter it (recommended: paste)

The **Article Content** editor (TipTap) has no link button, and it doesn't support tables. The most reliable way to enter the article is a rich-text paste:

1. Open `bc-036/article-content.html` in Chrome.
2. Press **Cmd+A**, then **Cmd+C**.
3. Click into **Article Content** in the CMS and press **Cmd+V**.

The pasted content keeps the H2, H3, bold, italic, bullet lists, numbered lists, horizontal rule and links. It uses only tags the editor and the storefront sanitizer accept: `p, h2, h3, strong, em, ul, ol, li, a, hr`.

**After pasting, check:**
- **No H1 inside Article Content.** The storefront renders the H1 from **Display Title**.
- **No breadcrumb or byline in the body.** The page template renders "Back to Journal" and the **Written By** value.
- **3 live links**, each clickable, with the correct href (see `internal-links.md`).
- **2 conditional anchor(s)** are **plain text, not links**: "how to wear your engagement ring and wedding band", "ring finger meanings".
- **No heading reads "FAQ" or "Frequently asked questions".** The storefront auto-generates FAQPage schema under such a heading; the Q&A heading in this article is worded to avoid that.

## What changed for the CMS (formatting only)

| Source element | CMS treatment | Why |
|---|---|---|
| H1 | Not in Article Content; goes in **Display Title** | `BlogPostBody` renders the H1 from the title fields |
| Breadcrumb line, "*By HOD Team*" | Not in Article Content | The template provides "Back to Journal" and the author meta |
| 1 table(s) | Converted to bullet lists. Column headings become inline labels in italics (e.g. "*Where it's common:*"); in comparison tables with an empty first heading, each column becomes a bold label followed by a list. All cell text is kept word for word; only separating punctuation was added. | `sanitizeRichText` strips table tags, and the editor has no table extension |
| Relative links | Absolute `https://www.houseofdiams.com/...` | A browser copy from a local file turns relative links into `file:///` links. These are the same destinations. |
| `[CONDITIONAL]` links | Anchor kept as plain text | The target pages aren't live yet |
| "---" before About the author | Horizontal rule | Same as the source |

**Verified:** generated programmatically from the approved source and compared block by block. Article Content is about **812 words** (including converted table labels).

## Block-by-block map

Use this as a fallback if you build the content by hand, or to check the paste.

### Block 1 — Paragraph

In the United States, a **wedding ring goes on the fourth finger of the left hand**, the finger between your middle finger and your little finger, which is why it's called the ring finger. The **engagement ring goes on the same finger**, and most people wear both rings there together after the wedding. Men in the US traditionally wear their wedding band on the same finger, too.

### Block 2 — Paragraph

That's the custom, not a rule. In several countries, including Germany, Russia, Poland, Greece and India, it's common to wear the wedding ring on the right hand instead. Many people also choose a different finger for comfort or for practical reasons.

### Block 3 — H2

Which finger is the ring finger?

### Block 4 — Paragraph

The ring finger is the **fourth finger, counting your thumb as the first**. On the left hand, it's the finger traditionally reserved for engagement and wedding rings. The same finger on your right hand is also often called the ring finger, but in the US a ring worn there doesn't usually signal marriage.

### Block 5 — H2

What hand does the engagement ring go on?

### Block 6 — Paragraph

In the US, the **engagement ring goes on the left hand**, on the ring finger. When you propose, it's the left ring finger the ring is slid onto.

### Block 7 — Paragraph

After the wedding, most people keep the engagement ring on the same finger and wear the wedding band with it. The traditional order puts the wedding band on first, closest to the hand, with the engagement ring on top. For the full etiquette, including what to do with the engagement ring on the wedding day, see how to wear your engagement ring and wedding band.

### Block 8 — H2

Left or right hand? Wedding ring customs by country

### Block 9 — Paragraph

Which hand you wear a wedding ring on depends largely on where you live, and on your family's religious and cultural traditions.

### Block 10 — Bullet *(converted from table)*

- **Left hand.** *Where it's common:* The United States, Canada, the United Kingdom, Sweden and Finland, and much of Western culture.
- **Right hand.** *Where it's common:* Germany, Austria, Poland, Russia, Bulgaria and Greece; also common in India.

### Block 11 — Paragraph

Customs can vary within a country, too, depending on religion, region and family. In Germany and Austria, for example, couples traditionally wear their engagement rings on the left hand and then wear their wedding rings on the right hand once they're married.

### Block 12 — Paragraph

**What hand does a wedding ring go on in America?** The left hand. In the US, both partners traditionally wear their wedding rings on the left ring finger.

### Block 13 — H2

Why is the wedding ring on the left hand?

### Block 14 — Paragraph

The best-known explanation goes back to ancient Rome. It was believed that a vein, the *vena amoris* or "vein of love", ran directly from the fourth finger of the left hand to the heart. A ring on that finger was therefore the closest a ring could be to the heart.

### Block 15 — Paragraph

Modern anatomy doesn't support the idea: the veins of the ring finger are no different from those of the other fingers. The tradition stayed anyway. A more practical reason is often given as well: most people are right-handed, so a ring on the left hand is exposed to less day-to-day wear.

### Block 16 — H2

Where do married men wear their rings?

### Block 17 — Paragraph

In the US, married men traditionally wear their wedding band on the **fourth finger of the left hand**, the same finger as their partner. Wedding rings for both spouses became widespread in the US and Canada during the twentieth century. In right-hand countries, men usually follow the right-hand custom.

### Block 18 — H2

Can you wear your wedding ring on a different finger?

### Block 19 — Paragraph

Yes. There's no rule that says you have to use the left ring finger, and people choose other fingers or the other hand for many reasons:

### Block 20 — Bullet

- **Comfort or work.** Some jobs and sports make a ring on the dominant hand, or on a particular finger, impractical.
- **Being left-handed.** Some left-handed people prefer the right hand for the same reason most people choose the left.
- **Culture or family.** Following the custom of the country or tradition you come from.
- **Personal choice.** Some couples simply prefer another finger.

### Block 21 — Paragraph

Rings worn on other fingers can carry their own meanings, from the thumb to the little finger. For what a ring on each finger can signify, see ring finger meanings.

### Block 22 — H2

Getting the ring size right for the ring finger

### Block 23 — Paragraph

Ring sizes can differ between your left and right hands, and between fingers, so measure the exact finger the ring will be worn on. If you move a ring to the other hand, check that it still fits. Here's how to [measure your ring size at home](https://www.houseofdiams.com/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams).

### Block 24 — H2

Choosing rings for the ring finger

### Block 25 — Paragraph

If you're choosing an engagement ring or wedding band for that left ring finger, explore [engagement rings](https://www.houseofdiams.com/engagement-rings) and [wedding bands to pair with it](https://www.houseofdiams.com/wedding-bands).

### Block 26 — Divider

— (horizontal rule)

### Block 27 — Paragraph

**About the author**

### Block 28 — Paragraph

**HOD Team.** The team behind House of Diams shares insights into bespoke engagement rings, diamond selection, and the process of bringing a ring design to life.
