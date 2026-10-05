# BC-007 — Internal Links

**Source:** `blogs/bc-007/BC-007-how-to-wear-an-engagement-ring-and-wedding-band.md` §3 (calendar link targets, Stage 16 anchor strategy).

In `article-content.html`, live links use absolute URLs (`https://www.houseofdiams.com/...`) so they survive a copy-paste from the browser. After pasting, hover over each link in the CMS editor or preview and confirm the href.

## Links in Article Content

| # | Anchor text (exact) | Destination | Section / placement | Purpose | Status |
|---|---|---|---|---|---|
| 1 | what finger a wedding ring goes on | `/blog/what-finger-does-a-wedding-ring-go-on` → https://www.houseofdiams.com/blog/what-finger-does-a-wedding-ring-go-on | H2 "Which ring goes on first…" | Hand-off for finger/hand and history | ✅ **LINKED — depends on BC-036 being published first** |
| 2 | a guide to jewelry metals | EDU-MET-00 (URL pending) | H2 "Should your engagement ring and wedding band match?" | Hand-off for metals | ⏸ **CONDITIONAL — plain text now.** Add the link when the page launches. |
| 3 | measure your ring size at home | `/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams` → https://www.houseofdiams.com/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams | H2 "Wearing your rings every day" | Education: ring size | ✅ **LIVE** |
| 4 | wedding bands to pair with it | `/wedding-bands` → https://www.houseofdiams.com/wedding-bands | Closing H2 | Commercial | ✅ **LIVE** |
| 5 | browse engagement rings | `/engagement-rings` → https://www.houseofdiams.com/engagement-rings | Closing H2 | Commercial | ✅ **LIVE** |

## Template-level link (not entered in Article Content)

| # | Link | Destination | Status |
|---|---|---|---|
| 6 | Breadcrumb "Journal" (REQUIRED) | `/blog` | The blog template has no breadcrumb. It provides a **"Back to Journal"** link and lists the post on `/blog`, which covers the required hub ↔ post connection. Confirm the post appears on `/blog` after publishing. |

**Expected count after pasting:** 4 clickable links in Article Content and 1 conditional anchor(s) left as plain text.

## Later (not part of this publish)

- BC-036 links here (plain text there until this post is live; re-paste afterwards).
- Add the EDU-MET-00 link when it launches.
