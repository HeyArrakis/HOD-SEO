# BC-001 — CMS Entry Sheet

**CMS:** manage.houseofdiams.com → CMS → Blog → **Create Blog** (`/dashboard/cms/blog/new`)
**Source of truth:** `blogs/BC-001-how-long-does-a-custom-engagement-ring-take.md` (approved) and `blogs/BC-001-qa.md`

**How each field behaves:** checked read-only in the HOD codebase (`~/Desktop/HOD`: `admin-hod/components/blog-editor-page.tsx`, `admin-hod/lib/blog-slug.ts`, `HOD/app/blog/[slug]/page.tsx`, `HOD/lib/seo.ts`, `HOD/lib/structured-data.ts`, `HOD/lib/sanitize-html.ts`, `HOD/components/blog/*`) and against the 2026-10-04 CMS screenshots. The live CMS has two fields the local code doesn't show yet (**Blog Card Title** and **Master Catalog Category**). For those, I used the helper text on the screenshots.

> ⚠️ **Before the first save:**
> 1. **Article Title sets the URL permanently on the first save.** Edits later don't change the slug. Type the Article Title exactly as below *before* you click Save Changes.
> 2. **"Show on website" is ticked by default.** Saving with it ticked makes the post live. Untick it while you enter and check the content, and tick it only for the final publish.

---

## Left column

### 1. Article Title
```
How Long Does a Custom Engagement Ring Take?
```
This one field drives three things:
- **SEO title.** The site template adds the brand, so the `<title>` renders as "How Long Does a Custom Engagement Ring Take? | House of Diams". That's the approved SEO title for a CMS that adds the brand automatically.
- **URL slug.** It's generated automatically as `/blog/how-long-does-a-custom-engagement-ring-take`, which is the approved slug.
- **BlogPosting `headline`** in the structured data.

❌ Don't use "How Long Does a Custom Engagement Ring Take? Full Timeline". The slug would become `…-take-full-timeline`.

### 2. Display Title
```
How Long Does a Custom Engagement Ring Take? From Design to Delivery
```
This is the approved **H1**. It's rendered as the article hero and the H1, and it's also used on cards. The field accepts only `<em>` for styling. Plain text, as above, is the approved default. Existing posts sometimes italicize part of the title (e.g. `…Take? <em>From Design to Delivery</em>`); that's optional styling that doesn't change the wording.

### 3. Blog Card Title
```
(leave blank)
```
It falls back to the Article Title. The approved BC-001 package doesn't specify a separate card title.

### 4. Short Intro
```
A House of Diams bespoke ring takes 3–4 weeks on average from design approval to delivery: typically 2–3 weeks of production, then 6–9 days of insured shipping.
```
This is the approved **meta description** (160 characters). On this site, Short Intro is also:
- the page's **meta description** and Open Graph description,
- the BlogPosting `description`,
- the visible **"Article summary"** box above the article body.

It's the only field that sets the meta description, so it has to be this exact approved text. The API requires this field.

### 5. Editorial Topic
```
Craft & Making
```
This is the approved Blog category for BC-001 (owner **BLOG-CRAFT**, "Blog: Craft & Making", Stage 13/16). It's shown as the badge on cards and on the article hero. The legacy storefront fallback data uses "Craft" for a similar post; use "Craft & Making" unless the live CMS already uses a different label for this category.

### 6. Master Catalog Category
```
Not associated
```
BC-001's approved product category is "COM-BESPOKE / n/a (bespoke service)", and bespoke isn't a master catalog category. Don't pick Engagement Rings: this article covers the custom route, not ready-to-buy rings. If the dropdown offers a Bespoke option, using it is an admin decision.

### 7. Written By
```
HOD Team
```
This is confirmed. The storefront shows it in the article meta and on cards.

### 8. Publish Date Text
```
[FINAL PUBLISH DATE — e.g. Oct 4, 2026]
```
The calendar date for BC-001 is 2026-10-04. Enter the actual publish date in the CMS display format (placeholder: "Apr 22, 2026"). This text is shown on the page and cards, and it's also passed into the structured data as `datePublished`/`dateModified` (see the open notes in `seo-metadata.md`).

### 9. Reading Time
```
8 min read
```
The article content is about 1,820 words of prose (about 1,870 including the list labels from the converted tables). The codebase has no reading-time formula, so this uses the standard reading speed of about 230 words per minute. The "X min read" format matches the existing posts.

### 10. Card Style Key
```
bg-0
```
This is the CMS default. The storefront defines `bg-0` to `bg-4`.

### 11. Card Background Color
```
#EEF1F8
```
This is the color paired with `bg-0` in the storefront's `bgColors` map. If you change the key, use its matching color:

| Key | Color |
|---|---|
| bg-0 | #EEF1F8 |
| bg-1 | #EDF3EE |
| bg-2 | #F2EFF8 |
| bg-3 | #EDF2FA |
| bg-4 | #EEF1F8 |

### 12. Display Order
```
[CMS/ADMIN DECISION — default 1]
```
The approved package doesn't set a strategic order. Set it relative to the posts already live.

### 13. Show on website
```
☐ while entering and checking  →  ☑ only at final publish
```

---

## Right column

### 14. Main Blog Image
Upload the approved hero image: a **real HOD bespoke engagement ring photo**. It renders at **21:9** on the article hero. The CMS converts uploads to WebP at a maximum width of 2,200 px, so upload at least 2,200 px wide. Full details are in `image-requirements.md`. Don't use stock imagery.

### 15. Blog Card Image
```
(leave empty)
```
The CMS uses the Main Blog Image for cards ("Uses main blog image"). Add a separate card image only if the hero crop doesn't work on cards.

### 16. Main Image Alt Text
```
Custom diamond engagement ring made by House of Diams
```
This is the approved alt text. **Adjust it to what the uploaded photo actually shows** (e.g. the setting style or stage of work). Without alt text, the site falls back to the Article Title.

### 17. Tags
```
(optional — leave empty unless you use tags)
```
The approved BC-001 package doesn't specify tags. If you want them, the existing storefront convention for a bespoke-process post is **Bespoke**, **Craft**, **Process**. They're display labels, not keywords. Don't add keyword phrases as tags.

### 18. Featured Products
```
NONE — 0 selected
```
The approved BC-001 strategy recommends **zero** products. Don't add any of the listed products (Rosette Five-Flower Bracelet, Asteria Seven-Stone Necklace, etc.).

---

## Bottom section

### 19. Article Content
Paste from **`bc-001/article-content.html`**. The method and the block-by-block map are in **`article-content.md`**. Don't put the H1, breadcrumb or byline in this field.

### 20. Extra Article Sections
```
None (default)
```
Extra Article Sections render **after** the whole article body, and the main editor can't hold images. That means the optional in-article images (timeline graphic, CAD-to-ring photo, making-stage photo) **can't be placed mid-article** as approved. Recommendation:
- **Default:** publish with the hero image only and no extra sections. All the content is already in text form, including the timeline list.
- **If the timeline graphic is ready:** you can add it as an **Add Image** block. It will appear after the "About the author" box, not under the timeline section. Decide whether that placement is still useful; if it isn't, leave it out.

Don't use **Add Heading** blocks: they render as large H3s after the article and would add sections that aren't in the approved structure.
