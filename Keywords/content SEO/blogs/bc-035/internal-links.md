# BC-035 — Internal Links

**Source:** `blogs/bc-035/BC-035-10-year-anniversary-gift-ideas-tin-and-diamond.md` §3 (calendar link targets, Stage 16 anchor strategy).

In `article-content.html`, live links use absolute URLs (`https://www.houseofdiams.com/...`) so they survive a copy-paste from the browser. After pasting, hover over each link in the CMS editor or preview and confirm the href.

## Links in Article Content

| # | Anchor text (exact) | Destination | Section / placement | Purpose | Status |
|---|---|---|---|---|---|
| 1 | wedding bands to pair with her rings | `/wedding-bands` → https://www.houseofdiams.com/wedding-bands | H3 "An eternity or half-eternity band"; closing H2 (anchor "Wedding Bands") | Commercial: eternity/half-eternity bands | ✅ **LIVE** |
| 2 | earrings to give | `/fine-jewellery/earrings` → https://www.houseofdiams.com/fine-jewellery/earrings | H3 "Diamond stud earrings"; closing H2 (anchor "Earrings") | Commercial: earrings | ✅ **LIVE** |
| 3 | necklaces and pendants | `/fine-jewellery/necklaces` → https://www.houseofdiams.com/fine-jewellery/necklaces | H3 "A diamond pendant"; closing H2 (anchor "Necklaces & Pendants") | Commercial: necklaces | ✅ **LIVE** |
| 4 | bracelets for every occasion | `/fine-jewellery/bracelet` → https://www.houseofdiams.com/fine-jewellery/bracelet | H3 "A diamond tennis bracelet"; closing H2 (anchor "Bracelets") | Commercial: bracelets | ✅ **LIVE** |
| 5 | anniversary gifts by year | BC-018 (URL pending) | End of "How to choose the right diamond gift" | Link to the full by-year list | ⏸ **CONDITIONAL — plain text now.** Add the link when the page launches. |
| 6 | eternity ring meaning and styles | BC-023 (URL pending) | H3 "An eternity or half-eternity band" | Eternity ring detail | ⏸ **CONDITIONAL — plain text now.** Add the link when the page launches. |

## Template-level link (not entered in Article Content)

| # | Link | Destination | Status |
|---|---|---|---|
| 7 | Breadcrumb "Journal" (REQUIRED) | `/blog` | The blog template has no breadcrumb. It provides a **"Back to Journal"** link and lists the post on `/blog`, which covers the required hub ↔ post connection. Confirm the post appears on `/blog` after publishing. |

**Expected count after pasting:** 8 clickable links in Article Content and 2 conditional anchor(s) left as plain text.

## Later (not part of this publish)

- BC-018 (Oct 7) links here ("10 year anniversary gift ideas"). Once BC-018 is live (the day after this post), re-paste the "How to choose" closing paragraph with the link to `/blog/anniversary-gifts-by-year-traditional-and-modern`.
- Add the BC-023 link when it publishes (Nov 9).
