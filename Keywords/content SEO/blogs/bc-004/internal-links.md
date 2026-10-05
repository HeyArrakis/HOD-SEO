# BC-004 — Internal Links

**Source:** `blogs/bc-004/BC-004-christmas-jewelry-gifts-a-holiday-gift-guide.md` §3 (calendar link targets, Stage 16 anchor strategy).

In `article-content.html`, live links use absolute URLs (`https://www.houseofdiams.com/...`) so they survive a copy-paste from the browser. After pasting, hover over each link in the CMS editor or preview and confirm the href.

## Links in Article Content

| # | Anchor text (exact) | Destination | Section / placement | Purpose | Status |
|---|---|---|---|---|---|
| 1 | Earrings to give | `/fine-jewellery/earrings` → https://www.houseofdiams.com/fine-jewellery/earrings | Closing "Shop … by category" list | Commercial: earrings category | ✅ **LIVE** |
| 2 | Necklaces and pendants | `/fine-jewellery/necklaces` → https://www.houseofdiams.com/fine-jewellery/necklaces | Closing "Shop … by category" list | Commercial: necklaces category | ✅ **LIVE** |
| 3 | Bracelets for every occasion | `/fine-jewellery/bracelet` → https://www.houseofdiams.com/fine-jewellery/bracelet | Closing "Shop … by category" list | Commercial: bracelets category | ✅ **LIVE** |
| 4 | the full fine jewelry collection | `/fine-jewellery` → https://www.houseofdiams.com/fine-jewellery | Last line | Commercial: umbrella category | ✅ **LIVE** |
| 5 | commission something one of a kind | `/bespoke` → https://www.houseofdiams.com/bespoke | H2 "A one-of-a-kind gift: bespoke jewelry" | Bespoke route for one-off gifts | ✅ **LIVE** |
| 6 | how diamonds are graded (the 4Cs) | `/blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat-house-of-diams` → https://www.houseofdiams.com/blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat-house-of-diams | Below the budget table | Education support for budget decisions | ✅ **LIVE** |
| 7 | how to find out a ring size discreetly | `/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams` → https://www.houseofdiams.com/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams | "Getting the details right", step 3 | Education support for ring gifts | ✅ **LIVE** |
| 8 | delivery details on our shipping page | `/shipping` → https://www.houseofdiams.com/shipping | "Last-minute…", ready-to-wear bullet | Policy page instead of stating cut-offs | ✅ **LIVE** |
| 9 | returns policy | `/returns` → https://www.houseofdiams.com/returns | "Getting the details right", step 5 | Policy page instead of stating a returns window | ✅ **LIVE** |
| 10 | jewelry gifts for your wife | BC-008 (URL pending) | H3 "Christmas jewelry gifts for your wife" | Hub → recipient spoke | ⏸ **CONDITIONAL — plain text now.** Add the link when the page launches. |
| 11 | jewelry gifts for your girlfriend | BC-009 (URL pending) | H3 "Christmas jewelry gifts for your girlfriend" | Hub → recipient spoke | ⏸ **CONDITIONAL — plain text now.** Add the link when the page launches. |

## Template-level link (not entered in Article Content)

| # | Link | Destination | Status |
|---|---|---|---|
| 12 | Breadcrumb "Journal" (REQUIRED) | `/blog` | The blog template has no breadcrumb. It provides a **"Back to Journal"** link and lists the post on `/blog`, which covers the required hub ↔ post connection. Confirm the post appears on `/blog` after publishing. |

**Expected count after pasting:** 9 clickable links in Article Content and 2 conditional anchor(s) left as plain text.

## Later (not part of this publish)

- BC-008 (Oct 12) and BC-009 (Oct 13) link back here ("holiday jewelry gift guide"). Once they are live, re-paste the two recipient paragraphs with links (expected URLs `/blog/meaningful-jewelry-gifts-for-your-wife` and `/blog/jewelry-gifts-for-your-girlfriend-diamond-ideas`).
- BC-004-DEC-REFRESH (Dec 7, same URL) adds the ready-to-ship / last-order section once HOD confirms holiday shipping cut-offs and the returns window.
