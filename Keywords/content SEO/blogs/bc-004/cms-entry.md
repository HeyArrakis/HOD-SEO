# BC-004 — CMS Entry Sheet

**CMS:** manage.houseofdiams.com → CMS → Blog → **Create Blog** (`/dashboard/cms/blog/new`)
**Source of truth:** `blogs/bc-004/BC-004-christmas-jewelry-gifts-a-holiday-gift-guide.md` and `blogs/bc-004/BC-004-qa.md`

**How each field behaves:** as documented for BC-001 (checked read-only in the HOD codebase: `admin-hod/components/blog-editor-page.tsx`, `admin-hod/lib/blog-slug.ts`, `HOD/app/blog/[slug]/page.tsx`, `HOD/lib/seo.ts`, `HOD/lib/structured-data.ts`, `HOD/lib/blog-faq.ts`).

> ⚠️ **Before the first save:**
> 1. **Article Title sets the URL permanently on the first save.** Type the Article Title exactly as below *before* you click Save Changes.
> 2. **"Show on website" is ticked by default.** Saving with it ticked makes the post live. Untick it while you enter and check the content, and tick it only for the final publish.

---

## Left column

### 1. Article Title
```
Christmas Jewelry Gifts: A Holiday Gift Guide
```
This field drives the **SEO title** (rendered as "Christmas Jewelry Gifts: A Holiday Gift Guide | House of Diams"), the **URL slug** (`/blog/christmas-jewelry-gifts-a-holiday-gift-guide`) and the BlogPosting `headline`. 

### 2. Display Title
```
Christmas Jewelry Gifts: A Holiday Diamond Gift Guide by Budget, Recipient and Style
```
The approved **H1**. Plain text is the approved default; the field accepts only `<em>` for optional styling that doesn't change the wording.

### 3. Blog Card Title
```
(leave blank)
```
It falls back to the Article Title. 

### 4. Short Intro
```
The best Christmas jewelry gifts are diamond studs, a solitaire pendant and a tennis bracelet. Ideas by budget and recipient, plus Hanukkah timing.
```
The approved **meta description** (147 characters). It is also the Open Graph description, the BlogPosting `description` and the visible "Article summary" box. The API requires this field.

### 5. Editorial Topic
```
Gifts & Occasions
```
Owner **BLOG-GIFTS** ("Blog: Gifts & Occasions", Stage 13 §5 category). Use this label unless the live CMS already uses a different label for the same category.

### 6. Master Catalog Category
```
Not associated
```
The guide spans earrings, necklaces, bracelets and bands, so no single master catalog category fits. **[CMS/ADMIN DECISION]** if the team prefers "Fine Jewellery".

### 7. Written By
```
HOD Team
```
Confirmed byline (same as BC-001).

### 8. Publish Date Text
```
[FINAL PUBLISH DATE — calendar date 2026-10-05, e.g. Oct 5, 2026]
```
Enter the actual publish date in the CMS display format. It's shown on the page and cards and passed into the structured data.

### 9. Reading Time
```
6 min read
```
About 1256 words of Article Content at ~230 words per minute (same method as BC-001).

### 10. Card Style Key
```
bg-0
```
CMS default. **[CMS/ADMIN DECISION]** The storefront defines `bg-0` to `bg-4`; the package doesn't set a strategic choice.

### 11. Card Background Color
```
#EEF1F8
```
The color paired with `bg-0`. If you change the key, use its matching color: bg-0 #EEF1F8 · bg-1 #EDF3EE · bg-2 #F2EFF8 · bg-3 #EDF2FA · bg-4 #EEF1F8.

### 12. Display Order
```
[CMS/ADMIN DECISION — default 1]
```
Not set strategically by the package. Set it relative to the posts already live.

### 13. Show on website
```
☐ while entering and checking  →  ☑ only at final publish
```

---

## Right column

### 14. Main Blog Image
Upload the hero: **A real HOD photo of two or three gift pieces together (for example studs, a pendant and a tennis bracelet), styled simply, optionally with restrained holiday props** It renders at **21:9** on the article hero; upload at least 2,200 px wide. Full details are in `image-requirements.md`. Don't use stock imagery.

### 15. Blog Card Image
```
(leave empty)
```
The CMS uses the Main Blog Image for cards. Add a separate card image only if the hero crop doesn't work on cards.

### 16. Main Image Alt Text
```
Diamond stud earrings, a solitaire pendant and a tennis bracelet from House of Diams
```
**Adjust it to what the uploaded photo actually shows.** Without alt text, the site falls back to the Article Title.

### 17. Tags
```
(optional) Gifts, Christmas, Hanukkah
```
Display labels, not keywords. Leave empty if the site doesn't use tags.

### 18. Featured Products
```
Up to 4 — HOD to confirm (candidates below)
```
Commercial-research gift guide, so a small product module fits the intent. These are verified live product pages; confirm stock and price before selecting, or leave empty.

| # | Product (select by this name) | Live URL |
|---|---|---|
| 1 | Adeline Round Solitaire Stud Earrings | `/shop/adeline-round-solitaire-stud-earrings` |
| 2 | Aurelia Round Solitaire Diamond Pendant | `/shop/aurelia-round-solitaire-diamond-pendant` |
| 3 | Endless Orbit Round Diamond Tennis Bracelet | `/shop/endless-orbit-round-diamond-tennis-bracelet` |
| 4 | Odette Five-Stone Huggie Earrings | `/shop/odette-five-stone-huggie-earrings` |

---

## Bottom section

### 19. Article Content
Paste from **`bc-004/article-content.html`**. The method and the block-by-block map are in **`article-content.md`**. Don't put the H1, breadcrumb or byline in this field.

### 20. Extra Article Sections
```
None (default)
```
Extra Article Sections render **after** the whole article body. All content is already in the text, so no extra sections are needed. Don't use **Add Heading** blocks: they would add sections that aren't in the approved structure.
