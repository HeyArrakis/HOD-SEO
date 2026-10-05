# BC-006 — Internal Links

**Source:** `blogs/bc-006/BC-006-necklace-layering-how-to-layer-necklaces.md` §3 (calendar link targets, Stage 16 anchor strategy).

In `article-content.html`, live links use absolute URLs (`https://www.houseofdiams.com/...`) so they survive a copy-paste from the browser. After pasting, hover over each link in the CMS editor or preview and confirm the href.

## Links in Article Content

| # | Anchor text (exact) | Destination | Section / placement | Purpose | Status |
|---|---|---|---|---|---|
| 1 | necklace length chart | EDU-RJG-NL (URL pending) | Below the lengths table | Hand-off for sizing | ⏸ **CONDITIONAL — plain text now.** Add the link when the page launches. |
| 2 | Diamond Leaf Tassel Lariat Necklace | `/shop/diamond-leaf-tassel-lariat-necklace` → https://www.houseofdiams.com/shop/diamond-leaf-tassel-lariat-necklace | Below the example-stacks table | Example of a lariat-led stack | ✅ **LIVE** |
| 3 | Celestine Dewdrop Pear Diamond Station Necklace | `/shop/celestine-dewdrop-pear-diamond-station-necklace` → https://www.houseofdiams.com/shop/celestine-dewdrop-pear-diamond-station-necklace | Below the example-stacks table | Example of a station necklace in a stack | ✅ **LIVE** |
| 4 | a guide to jewelry metals | EDU-MET-00 (URL pending) | H2 "Can you mix metals…" | Hand-off for metals | ⏸ **CONDITIONAL — plain text now.** Add the link when the page launches. |
| 5 | necklaces and pendants | `/fine-jewellery/necklaces` → https://www.houseofdiams.com/fine-jewellery/necklaces | Closing section | Commercial: necklaces | ✅ **LIVE** |
| 6 | the full fine jewelry collection | `/fine-jewellery` → https://www.houseofdiams.com/fine-jewellery | Closing section | Commercial: umbrella | ✅ **LIVE** |

## Template-level link (not entered in Article Content)

| # | Link | Destination | Status |
|---|---|---|---|
| 7 | Breadcrumb "Journal" (REQUIRED) | `/blog` | The blog template has no breadcrumb. It provides a **"Back to Journal"** link and lists the post on `/blog`, which covers the required hub ↔ post connection. Confirm the post appears on `/blog` after publishing. |

**Expected count after pasting:** 4 clickable links in Article Content and 2 conditional anchor(s) left as plain text.

## Later (not part of this publish)

- EDU-RJG-NL (Nov 4) should link back here for styling (two-way link per its calendar row). Add the EDU-RJG-NL and EDU-MET-00 links here when those pages launch.
