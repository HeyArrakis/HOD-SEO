# BC-009 — CMS Entry Sheet

**CMS:** manage.houseofdiams.com → CMS → Blog → **Create Blog** (`/dashboard/cms/blog/new`)
**Source of truth:** `blogs/bc-009/BC-009-jewelry-gifts-for-your-girlfriend-diamond-ideas.md` and `blogs/bc-009/BC-009-qa.md`

**How each field behaves:** as documented for BC-001 (checked read-only in the HOD codebase: `admin-hod/components/blog-editor-page.tsx`, `admin-hod/lib/blog-slug.ts`, `HOD/app/blog/[slug]/page.tsx`, `HOD/lib/seo.ts`, `HOD/lib/structured-data.ts`, `HOD/lib/blog-faq.ts`).

> ⚠️ **Before the first save:**
> 1. **Article Title sets the URL permanently on the first save.** Type the Article Title exactly as below *before* you click Save Changes.
> 2. **"Show on website" is ticked by default.** Saving with it ticked makes the post live. Untick it while you enter and check the content, and tick it only for the final publish.

---

## Left column

### 1. Article Title
```
Jewelry Gifts for Your Girlfriend: Diamond Ideas
```
This field drives the **SEO title** (rendered as "Jewelry Gifts for Your Girlfriend: Diamond Ideas | House of Diams"), the **URL slug** (`/blog/jewelry-gifts-for-your-girlfriend-diamond-ideas`) and the BlogPosting `headline`. 

### 2. Display Title
```
Jewelry Gifts for Your Girlfriend: First-Christmas and Meaningful Diamond Ideas
```
The approved **H1**. Plain text is the approved default; the field accepts only `<em>` for optional styling that doesn't change the wording.

### 3. Blog Card Title
```
(leave blank)
```
It falls back to the Article Title. 

### 4. Short Intro
```
Jewelry gifts for your girlfriend by relationship stage: first-Christmas pendants and studs, meaningful necklaces, and when a promise ring makes sense.
```
The approved **meta description** (151 characters). It is also the Open Graph description, the BlogPosting `description` and the visible "Article summary" box. The API requires this field.

### 5. Editorial Topic
```
Gifts & Occasions
```
Owner **BLOG-GIFTS** ("Blog: Gifts & Occasions", Stage 13 §5 category). Use this label unless the live CMS already uses a different label for the same category.

### 6. Master Catalog Category
```
Not associated
```
Spans several categories.

### 7. Written By
```
HOD Team
```
Confirmed byline (same as BC-001).

### 8. Publish Date Text
```
[FINAL PUBLISH DATE — calendar date 2026-10-13, e.g. Oct 13, 2026]
```
Enter the actual publish date in the CMS display format. It's shown on the page and cards and passed into the structured data.

### 9. Reading Time
```
4 min read
```
About 736 words of Article Content at ~230 words per minute (same method as BC-001).

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
Upload the hero: **A real HOD photo of a delicate diamond pendant (heart or solitaire) or small studs, gift-presented** It renders at **21:9** on the article hero; upload at least 2,200 px wide. Full details are in `image-requirements.md`. Don't use stock imagery.

### 15. Blog Card Image
```
(leave empty)
```
The CMS uses the Main Blog Image for cards. Add a separate card image only if the hero crop doesn't work on cards.

### 16. Main Image Alt Text
```
Diamond heart pendant necklace from House of Diams
```
**Adjust it to what the uploaded photo actually shows.** Without alt text, the site falls back to the Article Title.

### 17. Tags
```
(optional) Gifts, Christmas
```
Display labels, not keywords.

### 18. Featured Products
```
Up to 3 — HOD to confirm (candidates below)
```
Candidates match the first-Christmas picks. Confirm or leave empty.

| # | Product (select by this name) | Live URL |
|---|---|---|
| 1 | Amora Three-Prong Heart Solitaire Diamond Necklace | `/shop/amora-three-prong-heart-solitaire-diamond-necklace` |
| 2 | Odette Five-Stone Huggie Earrings | `/shop/odette-five-stone-huggie-earrings` |
| 3 | Celeste Round Solitaire Necklace | `/shop/celeste-round-solitaire-necklace` |

---

## Bottom section

### 19. Article Content
Paste from **`bc-009/article-content.html`**. The method and the block-by-block map are in **`article-content.md`**. Don't put the H1, breadcrumb or byline in this field.

### 20. Extra Article Sections
```
None (default)
```
Extra Article Sections render **after** the whole article body. All content is already in the text, so no extra sections are needed. Don't use **Add Heading** blocks: they would add sections that aren't in the approved structure.
