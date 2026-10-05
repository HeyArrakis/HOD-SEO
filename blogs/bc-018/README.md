# BC-018 publishing package (internal checklist)

**Blog:** Anniversary Gifts by Year: The Traditional and Modern List (and Where Diamonds Fit). Status: **READY FOR FINAL HUMAN REVIEW**.
**Source of truth:** `blogs/bc-018/BC-018-anniversary-gifts-by-year-traditional-and-modern.md` and `blogs/bc-018/BC-018-qa.md`

| File | Use |
|---|---|
| `BC-018-anniversary-gifts-by-year-traditional-and-modern.md` | The approved article, SEO metadata, link, product and visual recommendations |
| `BC-018-qa.md` | Internal QA record (don't share with the client) |
| `BC-018.md` | Client handoff |
| `cms-entry.md` | The value for every CMS field (**this is the CMS source**) |
| `article-content.html` | Open in Chrome, select all, copy, and paste into Article Content |
| `article-content.md` | Formatting notes and a block-by-block map (fallback/check) |
| `seo-metadata.md` | SEO values, the 9 keywords, and schema notes |
| `image-requirements.md` | The images to upload, with alt text |
| `internal-links.md` | The links to verify after pasting |

## Checklist

1. **Resolve the open items** in `BC-018-qa.md` §"Remaining human-review items" (especially any HIGH item).
2. **Open the HOD CMS:** CMS → Blog → **Create Blog**.
3. **Untick "Show on website" first.** It's ticked by default.
4. **Copy the field values from `cms-entry.md`.** Type the **Article Title** exactly ("Anniversary Gifts by Year: Traditional and Modern") before the first save, because it fixes the URL permanently.
5. **Add the images:** the Main Blog Image (a real HOD photo, ≥ 2,200 px wide) and its alt text. Leave Blog Card Image empty.
6. **Enter the Article Content** by pasting from `article-content.html`. No H1, breadcrumb or byline in the body; check lists and headings came through.
7. **Verify the SEO metadata:** Article Title = SEO title, Short Intro = the exact meta description, Display Title = the H1.
8. **Verify the links:** 5 live links and 1 conditional anchor(s) left as plain text (see `internal-links.md`). Confirm the `[DEPENDS ON]` target post is live first.
9. **Featured Products:** keep empty (0 selected).
10. **Final preview/QA:** the table has 25 rows (1st–15th, 20th–60th in fives, 75th) matching §1 of the article; the 20th row reads "China | Platinum"; the BC-035 link resolves; the BC-023 anchor is plain text.
11. **Only then publish:** tick "Show on website", then Save Changes. Afterward, confirm the post appears on `/blog`.
