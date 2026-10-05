# BC-008 — Internal Links

**Source:** `blogs/bc-008/BC-008-meaningful-jewelry-gifts-for-your-wife.md` §3 (calendar link targets, Stage 16 anchor strategy).

In `article-content.html`, live links use absolute URLs (`https://www.houseofdiams.com/...`) so they survive a copy-paste from the browser. After pasting, hover over each link in the CMS editor or preview and confirm the href.

## Links in Article Content

| # | Anchor text (exact) | Destination | Section / placement | Purpose | Status |
|---|---|---|---|---|---|
| 1 | holiday jewelry gift guide | `/blog/christmas-jewelry-gifts-a-holiday-gift-guide` → https://www.houseofdiams.com/blog/christmas-jewelry-gifts-a-holiday-gift-guide | H2 "Christmas gifts for your wife: plan ahead" | Spoke → hub | ✅ **LINKED — depends on BC-004 being published first** |
| 2 | shipping page | `/shipping` → https://www.houseofdiams.com/shipping | H2 "Christmas gifts for your wife…" | Policy instead of cut-offs | ✅ **LIVE** |
| 3 | returns policy | `/returns` → https://www.houseofdiams.com/returns | H2 "Christmas gifts for your wife…" | Policy instead of returns window | ✅ **LIVE** |
| 4 | earrings to give | `/fine-jewellery/earrings` → https://www.houseofdiams.com/fine-jewellery/earrings | Closing H2 | Commercial | ✅ **LIVE** |
| 5 | necklaces and pendants | `/fine-jewellery/necklaces` → https://www.houseofdiams.com/fine-jewellery/necklaces | Closing H2 | Commercial | ✅ **LIVE** |
| 6 | bracelets for every occasion | `/fine-jewellery/bracelet` → https://www.houseofdiams.com/fine-jewellery/bracelet | Closing H2 | Commercial | ✅ **LIVE** |
| 7 | wedding bands | `/wedding-bands` → https://www.houseofdiams.com/wedding-bands | Closing H2 | Commercial: anniversary bands | ✅ **LIVE** |

## Template-level link (not entered in Article Content)

| # | Link | Destination | Status |
|---|---|---|---|
| 8 | Breadcrumb "Journal" (REQUIRED) | `/blog` | The blog template has no breadcrumb. It provides a **"Back to Journal"** link and lists the post on `/blog`, which covers the required hub ↔ post connection. Confirm the post appears on `/blog` after publishing. |

**Expected count after pasting:** 7 clickable links in Article Content and 0 conditional anchor(s) left as plain text.

## Later (not part of this publish)

- BC-004 links here (plain text in BC-004 until this post is live; re-paste there afterwards).
