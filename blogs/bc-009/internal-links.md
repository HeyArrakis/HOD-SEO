# BC-009 — Internal Links

**Source:** `blogs/bc-009/BC-009-jewelry-gifts-for-your-girlfriend-diamond-ideas.md` §3 (calendar link targets, Stage 16 anchor strategy).

In `article-content.html`, live links use absolute URLs (`https://www.houseofdiams.com/...`) so they survive a copy-paste from the browser. After pasting, hover over each link in the CMS editor or preview and confirm the href.

## Links in Article Content

| # | Anchor text (exact) | Destination | Section / placement | Purpose | Status |
|---|---|---|---|---|---|
| 1 | what a promise ring means | BC-011 (URL pending) | H2 "Should you give your girlfriend a ring?" | Hand-off for promise rings | ⏸ **CONDITIONAL — plain text now.** Add the link when the page launches. |
| 2 | returns policy | `/returns` → https://www.houseofdiams.com/returns | Q&A "What if she doesn't like it?" | Policy | ✅ **LIVE** |
| 3 | shipping page | `/shipping` → https://www.houseofdiams.com/shipping | Q&A "What if she doesn't like it?" | Policy | ✅ **LIVE** |
| 4 | holiday jewelry gift guide | `/blog/christmas-jewelry-gifts-a-holiday-gift-guide` → https://www.houseofdiams.com/blog/christmas-jewelry-gifts-a-holiday-gift-guide | After the Q&A | Spoke → hub | ✅ **LINKED — depends on BC-004 being published first** |
| 5 | necklaces and pendants | `/fine-jewellery/necklaces` → https://www.houseofdiams.com/fine-jewellery/necklaces | Closing H2 | Commercial | ✅ **LIVE** |
| 6 | earrings to give | `/fine-jewellery/earrings` → https://www.houseofdiams.com/fine-jewellery/earrings | Closing H2 | Commercial | ✅ **LIVE** |
| 7 | bracelets for every occasion | `/fine-jewellery/bracelet` → https://www.houseofdiams.com/fine-jewellery/bracelet | Closing H2 | Commercial | ✅ **LIVE** |

## Template-level link (not entered in Article Content)

| # | Link | Destination | Status |
|---|---|---|---|
| 8 | Breadcrumb "Journal" (REQUIRED) | `/blog` | The blog template has no breadcrumb. It provides a **"Back to Journal"** link and lists the post on `/blog`, which covers the required hub ↔ post connection. Confirm the post appears on `/blog` after publishing. |

**Expected count after pasting:** 6 clickable links in Article Content and 1 conditional anchor(s) left as plain text.

## Later (not part of this publish)

- BC-004 links here (plain text there until this post is live).
- Add the BC-011 link when BC-011 is live (Oct 16).
