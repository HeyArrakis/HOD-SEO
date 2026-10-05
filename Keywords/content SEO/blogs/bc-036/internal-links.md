# BC-036 — Internal Links

**Source:** `blogs/bc-036/BC-036-what-finger-does-a-wedding-ring-go-on.md` §3 (calendar link targets, Stage 16 anchor strategy).

In `article-content.html`, live links use absolute URLs (`https://www.houseofdiams.com/...`) so they survive a copy-paste from the browser. After pasting, hover over each link in the CMS editor or preview and confirm the href.

## Links in Article Content

| # | Anchor text (exact) | Destination | Section / placement | Purpose | Status |
|---|---|---|---|---|---|
| 1 | how to wear your engagement ring and wedding band | BC-007 (URL pending) | H2 "What hand does the engagement ring go on?" | Hand-off for stacking order | ⏸ **CONDITIONAL — plain text now.** Add the link when the page launches. |
| 2 | ring finger meanings | BC-038 (URL pending) | End of "Can you wear your wedding ring on a different finger?" | Hand-off for finger meanings | ⏸ **CONDITIONAL — plain text now.** Add the link when the page launches. |
| 3 | measure your ring size at home | `/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams` → https://www.houseofdiams.com/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams | H2 "Getting the ring size right…" | Education: ring size | ✅ **LIVE** |
| 4 | engagement rings | `/engagement-rings` → https://www.houseofdiams.com/engagement-rings | Closing H2 | Commercial: engagement rings | ✅ **LIVE** |
| 5 | wedding bands to pair with it | `/wedding-bands` → https://www.houseofdiams.com/wedding-bands | Closing H2 | Commercial: wedding bands | ✅ **LIVE** |

## Template-level link (not entered in Article Content)

| # | Link | Destination | Status |
|---|---|---|---|
| 6 | Breadcrumb "Journal" (REQUIRED) | `/blog` | The blog template has no breadcrumb. It provides a **"Back to Journal"** link and lists the post on `/blog`, which covers the required hub ↔ post connection. Confirm the post appears on `/blog` after publishing. |

**Expected count after pasting:** 3 clickable links in Article Content and 2 conditional anchor(s) left as plain text.

## Later (not part of this publish)

- BC-007 (Oct 15) links here; BLOG-WR-HISTORY (Feb 1) links here for the left-hand history.
- Add the BC-007 link here when BC-007 is live (expected `/blog/how-to-wear-an-engagement-ring-and-wedding-band`) and the BC-038 link when it publishes (Nov 6).
