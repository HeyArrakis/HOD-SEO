# BC-001 — Internal Links (approved)

**Source:** `blogs/BC-001-…md` §3 (Stage 16 link map and anchor strategy). The strategy is unchanged.

In `article-content.html`, live links use absolute URLs (`https://www.houseofdiams.com/...`) so they survive a copy-paste from the browser. These are the same destinations as the approved relative paths. After pasting, hover over each link in the CMS editor or preview and confirm the href.

## Links in Article Content

| # | Anchor text (exact) | Destination | Section / placement | Status |
|---|---|---|---|---|
| 1 | Start your own commission | `/bespoke` → https://www.houseofdiams.com/bespoke | "Start your custom engagement ring", the bold CTA line | ✅ **LIVE — REQUIRED** (primary CTA) |
| 2 | explore diamond shapes before your consultation | `/blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of-diams` | Step 1 "Start with a clear brief", 2nd bullet | ✅ LIVE. Update the link if this page later moves to `/education/diamond-shapes`. |
| 3 | browse finished engagement rings | `/engagement-rings` | End of "Custom vs. ready-to-buy: which fits your timeline?" | ✅ LIVE (secondary, for the ready-to-buy route only) |
| 4 | the House of Diams story | `/about` | Last line of "Start your custom engagement ring" | ✅ LIVE (recommended) |
| 5 | a guide to jewelry metals | EDU-MET-00 (URL pending) | "How is a diamond ring made?", step 2 Casting | ⏸ **CONDITIONAL — plain text now.** Add the link when the page launches. |
| 6 | ring setting styles explained | EDU-RJG-01 (URL pending) | "How is a diamond ring made?", step 4 Stone setting | ⏸ **CONDITIONAL — plain text now.** Add the link when the page launches. |

## Template-level link (not entered in Article Content)

| # | Link | Destination | Status |
|---|---|---|---|
| 7 | Breadcrumb "Journal" (approved, REQUIRED) | `/blog` | The blog template has no breadcrumb. It provides a **"Back to Journal"** link and lists the post on `/blog`, which covers the required hub ↔ post connection. Confirm the post appears on `/blog` after publishing. |

**Expected count after pasting:** 4 clickable links in Article Content (#1–4) and 0 links on #5–6.

## Later (not part of this publish)

- When they're published, BC-016, BC-017, BC-034 and BLOG-NPD should link **to** BC-001. BC-017's timing checklist should link here rather than repeat the timeline.
- The conditional `/bespoke` → BC-001 craft link would be a website edit. It's out of scope.
