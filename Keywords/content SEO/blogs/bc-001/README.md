# BC-001 publishing package (internal checklist)

**Blog:** How Long Does a Custom Engagement Ring Take? From Design to Delivery. Approved, with business facts confirmed.
**Source of truth:** `blogs/BC-001-how-long-does-a-custom-engagement-ring-take.md` and `blogs/BC-001-qa.md`

| File | Use |
|---|---|
| `cms-entry.md` | The value for every CMS field |
| `article-content.html` | Open in Chrome, select all, copy, and paste into Article Content |
| `article-content.md` | Formatting notes and a block-by-block map (fallback/check) |
| `seo-metadata.md` | Approved SEO values, the 7 keywords, and schema notes |
| `image-requirements.md` | The images to upload, with alt text |
| `internal-links.md` | The links to verify after pasting |

## Checklist

1. **Open the HOD CMS:** CMS → Blog → **Create Blog**.
2. **Untick "Show on website" first.** It's ticked by default, and saving would make the post live.
3. **Copy the field values from `cms-entry.md`.** Type the **Article Title** exactly ("How Long Does a Custom Engagement Ring Take?") before the first save, because it fixes the URL permanently.
4. **Add the images:** the Main Blog Image (a real HOD photo, ≥ 2,200 px wide) and its alt text. Leave Blog Card Image empty so the card uses the main image.
5. **Enter the Article Content** by pasting from `article-content.html`. Make sure there's no H1, breadcrumb or byline in the body, and that the lists and headings came through.
6. **Verify the SEO metadata:** Article Title = SEO title, Short Intro = the exact meta description, Display Title = the H1.
7. **Verify the links:** 4 live links (`/bespoke` CTA, shapes guide, `/engagement-rings`, `/about`) and 2 conditional anchors left as plain text.
8. **Keep Featured Products empty** (0 selected).
9. **Do a final preview/QA:** the timeline reads "3–4 weeks on average from design approval to delivery", "2–3 weeks of production" and "6–9 days of insured shipping"; there's no 4–6 week figure and no holiday cutoff; the author is HOD Team; the URL is `/blog/how-long-does-a-custom-engagement-ring-take`.
10. **Only then publish:** tick "Show on website", then Save Changes. Afterward, confirm the post appears on `/blog`.

**Separate from this package:** update the live `/bespoke` page's "4-6 week" wording (you're handling it). The schema items flagged in `seo-metadata.md` need a website code change.
