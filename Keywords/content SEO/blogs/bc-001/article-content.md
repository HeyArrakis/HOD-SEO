# BC-001 — Article Content (CMS formatting map)

**Source:** `blogs/BC-001-how-long-does-a-custom-engagement-ring-take.md` (approved). The wording is unchanged.

## How to enter it (recommended: paste)

The **Article Content** editor (TipTap) has no link button, and it doesn't support tables. The most reliable way to enter the article is a rich-text paste:

1. Open `bc-001/article-content.html` in Chrome.
2. Press **Cmd+A**, then **Cmd+C**.
3. Click into **Article Content** in the CMS and press **Cmd+V**.

The pasted content keeps the H2, H3, bold, italic, bullet lists, numbered lists, horizontal rule and links. It uses only tags the editor and the storefront sanitizer accept: `p, h2, h3, strong, em, ul, ol, li, a, hr`.

**After pasting, check:**
- **No H1 inside Article Content.** The storefront renders the H1 from **Display Title**.
- **No breadcrumb or byline in the body.** The page template renders "Back to Journal" and the **Written By** value.
- **4 live links**, each clickable, with the correct href (see `internal-links.md`).
- **2 conditional anchors** ("a guide to jewelry metals", "ring setting styles explained") are **plain text, not links**.

## What changed for the CMS (formatting only)

| Source element | CMS treatment | Why |
|---|---|---|
| H1 | Not in Article Content; goes in **Display Title** | `BlogPostBody` renders the H1 from the title fields |
| Breadcrumb line, "*By HOD Team*" | Not in Article Content | The template provides "Back to Journal" and the author meta |
| 3 tables | Converted to numbered/bullet lists. Column headings become inline labels ("Timing:", "Why it adds time:", "How to keep it on track:", "Starting point:", and so on). All cell text is kept word for word; only separating punctuation was added. | `sanitizeRichText` strips table tags, and the editor has no table extension |
| Relative links (`/bespoke` etc.) | Absolute `https://www.houseofdiams.com/...` | A browser copy from a local file turns relative links into `file:///` links. These are the same destinations. |
| `[CONDITIONAL]` links | Anchor kept as plain text | The target pages aren't live yet |
| "---" before About the author | Horizontal rule | Same as the source |

**Verified:** I compared the source and the HTML word for word. The only differences are the table column labels (repeated per item instead of once in a header row) and the stage numbers, which now come from the numbered list.

## Block-by-block map

Use this as a fallback if you build the content by hand, or to check the paste.


### Block 1 — Paragraph

On average, a bespoke (custom-made) engagement ring from House of Diams takes **3–4 weeks from design approval to delivery**. That's typically **2–3 weeks of production**, followed by **approximately 6–9 days of insured shipping** to your door. The timeline can vary depending on the stone selected, so treat it as an average, not a guaranteed date.

### Block 2 — Paragraph

Across the industry, quoted timelines vary much more than that. Jeweler guides commonly quote anything from about four to twelve weeks, and some workshops quote several months for fully hand-built designs. A quote isn't comparable until you know what it covers and when it starts.

### Block 3 — Paragraph

At House of Diams, the clock starts when you approve your design. Your first inquiry and consultation, and the design discussions that follow, happen before that point. There's no set length for them; it depends on your ideas and how quickly you settle on a design. If you're working toward a fixed date, the day you approve your design is the one that matters most.

### Block 4 — H2

The custom engagement ring timeline at a glance

### Block 5 — Paragraph

A bespoke engagement ring from House of Diams moves through these stages. The 3–4 week average covers everything from design approval to delivery.

### Block 6 — Numbered *(converted from table)*

1. **Inquiry and consultation.** You share your ideas, reference images, budget range, ring size and the date you're working toward. *Timing:* Before the timeline starts; no set length
2. **Design development and approval.** The design is developed until you're happy with it, and you approve it. *Timing:* **The timeline starts when you approve the design**
3. **Production.** For a new bespoke design: sketching, a dedicated CAD model, diamond selection and sorting, ring making, quality checks, polishing and packaging. *Timing:* **Typically 2–3 weeks**
4. **Insured shipping.** The packaged ring is shipped, insured, to your door. *Timing:* **Approximately 6–9 days**

### Block 7 — Paragraph *(converted from table)*

**Design approval → delivery: 3–4 weeks on average; can vary depending on the stone selected**

### Block 8 — Paragraph

Diamond selection and sorting take place during production, after you approve the design, so they're already part of the 3–4 weeks.

### Block 9 — H2

Making time vs. delivery time: why the difference matters

### Block 10 — Paragraph

Two different clocks often get blurred together when people talk about how long a custom ring takes. At House of Diams they break down like this:

### Block 11 — Bullet

- **Production** typically takes 2–3 weeks. It covers the full production process: CAD development, diamond selection and sorting, ring making, quality checks, polishing and packaging.
- **Insured shipping** takes approximately 6–9 days, from House of Diams to your door.

### Block 12 — Paragraph

Together they make up the 3–4 week average, which starts when you approve your design.

### Block 13 — Paragraph

Keeping the two separate means you don't plan around only half the timeline. When you compare jewelers, ask two questions:

### Block 14 — Numbered

1. **Does the quoted timeline include delivery?**
2. **When does the clock start?** Depending on the jeweler, it might start at your first inquiry, at design approval, or when the stone is confirmed. At House of Diams, it starts at design approval.

### Block 15 — Paragraph

Two quotes that look the same can mean very different things in practice.

### Block 16 — H2

The custom engagement ring process, step by step

### Block 17 — Paragraph

If you're wondering how to design your own engagement ring, the process is more structured than it sounds. Steps 1 and 2 happen before the timeline starts. Steps 3 to 5 make up the 3–4 weeks.

### Block 18 — H3

1. Start with a clear brief

### Block 19 — Paragraph

Your first inquiry and consultation happen before the timeline begins. The more you bring to that first conversation, the fewer rounds of changes you'll need later. A useful brief includes:

### Block 20 — Bullet

- photos of rings you love, and of rings you don't
- the diamond shape you're drawn to (if you're unsure, [explore diamond shapes before your consultation](/blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of-diams))
- your preferred metal and overall style
- a budget range
- the ring size, if you know it
- the date you need the ring by

### Block 21 — H3

2. Develop and approve the design

### Block 22 — Paragraph

The design is then developed until it's right for you. When you approve it, the production timeline begins. There's no fixed length for this stage; it depends on your ideas and how many changes you want. Approve the design only when you're genuinely happy with it, because changes are much harder once production has started.

### Block 23 — H3

3. CAD model and diamond selection

### Block 24 — Paragraph

Once you approve the design, production begins. For a new bespoke design, this includes sketching and creating a dedicated CAD (computer-aided design) model, which is a precise digital version of your ring. Your diamond is also selected and sorted at this stage. Both steps are part of the typical 2–3 week production period, and the overall timeline can vary depending on the stone selected.

### Block 25 — H3

4. Making, quality checks and finishing

### Block 26 — Paragraph

Next, the ring is made, quality-checked, polished and packaged. Together with the CAD work and diamond selection, this production period typically takes 2–3 weeks. The next section explains how a ring is made.

### Block 27 — H3

5. Insured delivery

### Block 28 — Paragraph

The packaged ring is then shipped, insured, from House of Diams to your door, which takes approximately 6–9 days. Build that into your plans, especially if the ring needs to arrive by a specific date. Allow extra time over the holidays, when transport delays can make shipping take longer.

### Block 29 — H2

How is a diamond ring made?

### Block 30 — Paragraph

Production turns an approved design into a finished ring, and at House of Diams it happens within the typical 2–3 week production period. Most fine jewelry today combines digital design with careful handwork. The exact methods vary by jeweler and by design, but a typical sequence of making steps looks like this:

### Block 31 — Numbered

1. **Model.** The CAD design is printed as a precise model in wax or castable resin.
2. **Casting.** In lost-wax casting, the model is encased in a plaster-like material called investment and heated until the wax burns away, leaving a hollow mold. Molten metal is then poured into that mold. The metal is usually a gold or platinum alloy; for help choosing, see [a guide to jewelry metals](URL_PENDING:EDU-MET-00) `[CONDITIONAL]`.
3. **Clean-up and assembly.** The rough casting is freed from the mold, filed and refined. Separate parts, such as prongs or a gallery, are joined by soldering or laser welding. Some pieces, or parts of them, are hand-fabricated from metal stock instead of being cast.
4. **Stone setting.** A stone setter secures the center stone and any accent stones in prongs, a bezel or a pavé setting. Each setting holds the stone differently; see [ring setting styles explained](URL_PENDING:EDU-RJG-01) `[CONDITIONAL]`.
5. **Finishing.** The ring is polished, cleaned and checked before it's packed and sent.

### Block 32 — Paragraph

Once the design is approved, these steps follow a known order. That's why production is the more predictable part of a custom timeline.

### Block 33 — H2

What can make a custom engagement ring take longer?

### Block 34 — Paragraph

Some factors affect when the clock starts. Others affect the weeks after you approve the design.

### Block 35 — Bullet *(converted from table)*

- **The stone:** *Why it adds time:* House of Diams' timeline can vary depending on the stone selected. *How to keep it on track:* Be clear about which stone details matter most to you, and where you're flexible.
- **Design complexity:** *Why it adds time:* In general, details such as pavé, halos, intricate galleries or engraving add making steps. *How to keep it on track:* Decide early which details really matter to you.
- **Reaching design approval:** *Why it adds time:* The 3–4 weeks starts at approval, so the rounds of changes before then decide when the clock starts. *How to keep it on track:* Bring a strong brief and give consolidated feedback.
- **Changes after approval:** *Why it adds time:* Late changes can mean redoing completed work. *How to keep it on track:* Approve the design only when you're sure.
- **Unknown ring size:** *Why it adds time:* A wrong guess can mean resizing after delivery. *How to keep it on track:* Find the size discreetly before you start, if you can.
- **Holiday shipping:** *Why it adds time:* Holiday transport delays can make shipping take longer than usual. *How to keep it on track:* Plan ahead if you have a fixed date, and confirm current delivery timing with House of Diams.

### Block 36 — H3

Can a custom engagement ring be rushed?

### Block 37 — Paragraph

The most reliable way to get your ring sooner is to reach design approval sooner. Arrive with a clear brief, and give clear, consolidated feedback on the design. After approval, production typically takes 2–3 weeks. Its steps, including quality checks, are there for a reason, and skipping them isn't a good trade for a ring meant to last. If you're working to a fixed date, say so at the start. House of Diams' timelines are averages, not guarantees, so ask about timing for your specific design and stone.

### Block 38 — H2

Planning a holiday proposal? Work backward from the date

### Block 39 — Paragraph

If you're planning to propose at Christmas, on New Year's Eve or on Valentine's Day, work backward from the proposal:

### Block 40 — Numbered

1. **Pick the date you want the ring in your hands.** Make this earlier than the proposal itself, so you have a buffer.
2. **Count back about 3–4 weeks.** That's House of Diams' average from design approval to delivery, so it tells you roughly when to approve your design.
3. **Count back further** for your inquiry, consultation and design discussions, which happen before the timeline starts.
4. **Add a margin** for anything unexpected, such as a late change or a holiday shipping delay.

### Block 41 — Paragraph

The House of Diams workshop continues operating over Christmas, but shipping may take longer because of holiday transport delays. This is planning guidance, not an order-by date. Start well ahead of your proposal date rather than leaving the order until December, and confirm current delivery timing with House of Diams when you get in touch. Every timeline here is an average, not a guarantee.

### Block 42 — H2

Custom vs. ready-to-buy: which fits your timeline?

### Block 43 — Paragraph

A custom ring and a ready-to-buy ring are different routes. Choose the one that matches your priorities.

### Block 44 — Paragraph *(converted from table)*

**Custom (bespoke)**

### Block 45 — Bullet *(converted from table)*

- **Starting point:** Your idea
- **Decisions:** Design, stone, metal and details
- **Timeline:** At House of Diams, 3–4 weeks on average from design approval to delivery; your inquiry and design discussions come first
- **Best for:** A one-of-a-kind ring, a specific stone, or a design you can't find anywhere else

### Block 46 — Paragraph *(converted from table)*

**Ready-to-buy**

### Block 47 — Bullet *(converted from table)*

- **Starting point:** An existing design
- **Decisions:** Mainly choosing the design
- **Timeline:** Depends on the product; check the product page
- **Best for:** Seeing finished designs and making a quicker decision

### Block 48 — Paragraph

If you'd rather choose from existing designs, [browse finished engagement rings](https://www.houseofdiams.com/engagement-rings).

### Block 49 — H2

Does a custom ring cost more?

### Block 50 — Paragraph

No single number answers this. The cost of a custom ring is influenced by choices such as the stone, the metal and the complexity of the design. Share a realistic budget range at the start. It steers the design and stone toward options that fit, and it avoids rounds of redesign that push back design approval.

### Block 51 — H2

Start your custom engagement ring

### Block 52 — Paragraph

If you have a date in mind, start early. Tell House of Diams about your idea, your stone preferences and the date you're working toward. Once you approve your design, your ring takes 3–4 weeks on average to reach you, so the sooner you start the conversation, the more room you have.

### Block 53 — Paragraph

**[Start your own commission](https://www.houseofdiams.com/bespoke)**

### Block 54 — Paragraph

To learn more about the people behind your ring, read [the House of Diams story](https://www.houseofdiams.com/about).

### Block 55 — Divider

— (horizontal rule)

### Block 56 — Paragraph

**About the author**

### Block 57 — Paragraph

**HOD Team.** The team behind House of Diams shares insights into bespoke engagement rings, diamond selection, and the process of bringing a ring design to life.
