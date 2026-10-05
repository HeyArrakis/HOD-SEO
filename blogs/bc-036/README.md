# BC-036 publishing package (internal checklist)

**Blog:** What Finger Does a Wedding Ring Go On? (And Which Hand for the Engagement Ring). Status: **READY FOR FINAL HUMAN REVIEW**.
**Source of truth:** `blogs/bc-036/BC-036-what-finger-does-a-wedding-ring-go-on.md` and `blogs/bc-036/BC-036-qa.md`

| File | Use |
|---|---|
| `BC-036-what-finger-does-a-wedding-ring-go-on.md` | The approved article, SEO metadata, link, product and visual recommendations |
| `BC-036-qa.md` | Internal QA record (don't share with the client) |
| `BC-036.md` | Client handoff |
| `cms-entry.md` | The value for every CMS field (**this is the CMS source**) |
| `article-content.html` | Open in Chrome, select all, copy, and paste into Article Content |
| `article-content.md` | Formatting notes and a block-by-block map (fallback/check) |
| `seo-metadata.md` | SEO values, the 8 keywords, and schema notes |
| `image-requirements.md` | The images to upload, with alt text |
| `internal-links.md` | The links to verify after pasting |

## Checklist

1. **Resolve the open items** in `BC-036-qa.md` §"Remaining human-review items" (especially any HIGH item).
2. **Open the HOD CMS:** CMS → Blog → **Create Blog**.
3. **Untick "Show on website" first.** It's ticked by default.
4. **Copy the field values from `cms-entry.md`.** Type the **Article Title** exactly ("What Finger Does a Wedding Ring Go On?") before the first save, because it fixes the URL permanently.
5. **Add the images:** the Main Blog Image (a real HOD photo, ≥ 2,200 px wide) and its alt text. Leave Blog Card Image empty.
6. **Enter the Article Content** by pasting from `article-content.html`. No H1, breadcrumb or byline in the body; check lists and headings came through.
7. **Verify the SEO metadata:** Article Title = SEO title, Short Intro = the exact meta description, Display Title = the H1.
8. **Verify the links:** 3 live links and 2 conditional anchor(s) left as plain text (see `internal-links.md`).
9. **Featured Products:** keep empty (0 selected).
10. **Final preview/QA:** opening reads "fourth finger of the left hand"; the country table lists left: US, Canada, UK, Sweden, Finland; right: Germany, Austria, Poland, Russia, Bulgaria, Greece, India (common); 2 conditional anchors are plain text.
11. **Only then publish:** tick "Show on website", then Save Changes. Afterward, confirm the post appears on `/blog`.
