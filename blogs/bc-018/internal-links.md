# BC-018 — Internal Links

**Source:** `blogs/bc-018/BC-018-anniversary-gifts-by-year-traditional-and-modern.md` §3 (calendar link targets, Stage 16 anchor strategy).

In `article-content.html`, live links use absolute URLs (`https://www.houseofdiams.com/...`) so they survive a copy-paste from the browser. After pasting, hover over each link in the CMS editor or preview and confirm the href.

## Links in Article Content

| # | Anchor text (exact) | Destination | Section / placement | Purpose | Status |
|---|---|---|---|---|---|
| 1 | 10 year anniversary gift ideas | `/blog/10-year-anniversary-gift-ideas-tin-and-diamond` → https://www.houseofdiams.com/blog/10-year-anniversary-gift-ideas-tin-and-diamond | H2 "What anniversary is diamond?" | Depth for the 10th anniversary | ✅ **LINKED — depends on BC-035 being published first** |
| 2 | eternity ring meaning | BC-023 (URL pending) | End of "Anniversary jewelry…" section | Eternity ring tradition | ⏸ **CONDITIONAL — plain text now.** Add the link when the page launches. |
| 3 | wedding bands | `/wedding-bands` → https://www.houseofdiams.com/wedding-bands | Closing H2 "Shop anniversary jewelry" | Commercial: anniversary bands | ✅ **LIVE** |
| 4 | earrings to give | `/fine-jewellery/earrings` → https://www.houseofdiams.com/fine-jewellery/earrings | Closing H2 | Commercial | ✅ **LIVE** |
| 5 | necklaces and pendants | `/fine-jewellery/necklaces` → https://www.houseofdiams.com/fine-jewellery/necklaces | Closing H2 | Commercial | ✅ **LIVE** |
| 6 | bracelets for every occasion | `/fine-jewellery/bracelet` → https://www.houseofdiams.com/fine-jewellery/bracelet | Closing H2 | Commercial | ✅ **LIVE** |

## Template-level link (not entered in Article Content)

| # | Link | Destination | Status |
|---|---|---|---|
| 7 | Breadcrumb "Journal" (REQUIRED) | `/blog` | The blog template has no breadcrumb. It provides a **"Back to Journal"** link and lists the post on `/blog`, which covers the required hub ↔ post connection. Confirm the post appears on `/blog` after publishing. |

**Expected count after pasting:** 5 clickable links in Article Content and 1 conditional anchor(s) left as plain text.

## Later (not part of this publish)

- BC-035 links here (plain text until this post is live; re-paste it there afterwards).
- Add the BC-023 link when it publishes (Nov 9).
