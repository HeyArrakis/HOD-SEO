# BC-003 — Internal Links

**Source:** `blogs/bc-003/BC-003-push-present-what-it-is-and-jewelry-ideas.md` §3 (calendar link targets, Stage 16 anchor strategy).

In `article-content.html`, live links use absolute URLs (`https://www.houseofdiams.com/...`) so they survive a copy-paste from the browser. After pasting, hover over each link in the CMS editor or preview and confirm the href.

## Links in Article Content

| # | Anchor text (exact) | Destination | Section / placement | Purpose | Status |
|---|---|---|---|---|---|
| 1 | earrings to give | `/fine-jewellery/earrings` → https://www.houseofdiams.com/fine-jewellery/earrings | H3 "Diamond stud earrings"; closing H2 | Commercial | ✅ **LIVE** |
| 2 | necklaces and pendants | `/fine-jewellery/necklaces` → https://www.houseofdiams.com/fine-jewellery/necklaces | H3 "A solitaire or heart pendant"; closing H2 | Commercial | ✅ **LIVE** |
| 3 | measure your ring size at home | `/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams` → https://www.houseofdiams.com/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams | H3 "A half-eternity band" | Education: ring size | ✅ **LIVE** |
| 4 | wedding bands to pair with her rings | `/wedding-bands` → https://www.houseofdiams.com/wedding-bands | H3 "A half-eternity band"; closing H2 ("wedding bands") | Commercial | ✅ **LIVE** |
| 5 | bracelets for every occasion | `/fine-jewellery/bracelet` → https://www.houseofdiams.com/fine-jewellery/bracelet | H3 "A diamond tennis bracelet"; closing H2 | Commercial | ✅ **LIVE** |
| 6 | commission something one of a kind / our bespoke service | `/bespoke` → https://www.houseofdiams.com/bespoke | H3 "A piece that marks the baby"; closing H2 | Bespoke for personalized pieces | ✅ **LIVE** |

## Template-level link (not entered in Article Content)

| # | Link | Destination | Status |
|---|---|---|---|
| 7 | Breadcrumb "Journal" (REQUIRED) | `/blog` | The blog template has no breadcrumb. It provides a **"Back to Journal"** link and lists the post on `/blog`, which covers the required hub ↔ post connection. Confirm the post appears on `/blog` after publishing. |

**Expected count after pasting:** 11 clickable links in Article Content and 0 conditional anchor(s) left as plain text.

## Later (not part of this publish)

- None scheduled. BC-008's "new baby" row could link here at its first refresh (not an approved target today).
