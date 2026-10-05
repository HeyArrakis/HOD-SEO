# BC-035 publishing package (internal checklist)

**Blog:** 10 Year Anniversary Gift Ideas: Tin, Aluminum and the Modern Diamond Tradition. Status: **READY FOR FINAL HUMAN REVIEW**.
**Source of truth:** `blogs/bc-035/BC-035-10-year-anniversary-gift-ideas-tin-and-diamond.md` and `blogs/bc-035/BC-035-qa.md`

| File | Use |
|---|---|
| `BC-035-10-year-anniversary-gift-ideas-tin-and-diamond.md` | The approved article, SEO metadata, link, product and visual recommendations |
| `BC-035-qa.md` | Internal QA record (don't share with the client) |
| `BC-035.md` | Client handoff |
| `cms-entry.md` | The value for every CMS field (**this is the CMS source**) |
| `article-content.html` | Open in Chrome, select all, copy, and paste into Article Content |
| `article-content.md` | Formatting notes and a block-by-block map (fallback/check) |
| `seo-metadata.md` | SEO values, the 6 keywords, and schema notes |
| `image-requirements.md` | The images to upload, with alt text |
| `internal-links.md` | The links to verify after pasting |

## Checklist

1. **Resolve the open items** in `BC-035-qa.md` §"Remaining human-review items" (especially any HIGH item).
2. **Open the HOD CMS:** CMS → Blog → **Create Blog**.
3. **Untick "Show on website" first.** It's ticked by default.
4. **Copy the field values from `cms-entry.md`.** Type the **Article Title** exactly ("10 Year Anniversary Gift Ideas: Tin and Diamond") before the first save, because it fixes the URL permanently.
5. **Add the images:** the Main Blog Image (a real HOD photo, ≥ 2,200 px wide) and its alt text. Leave Blog Card Image empty.
6. **Enter the Article Content** by pasting from `article-content.html`. No H1, breadcrumb or byline in the body; check lists and headings came through.
7. **Verify the SEO metadata:** Article Title = SEO title, Short Intro = the exact meta description, Display Title = the H1.
8. **Verify the links:** 8 live links and 2 conditional anchor(s) left as plain text (see `internal-links.md`).
9. **Featured Products:** up to 3 candidates in `cms-entry.md`, pending HOD confirmation (or leave empty).
10. **Final preview/QA:** opening reads "traditional … tin or aluminum" and "modern … diamond jewelry"; the BC-018 and BC-023 anchors are plain text; no "FAQ" heading.
11. **Only then publish:** tick "Show on website", then Save Changes. Afterward, confirm the post appears on `/blog`.
