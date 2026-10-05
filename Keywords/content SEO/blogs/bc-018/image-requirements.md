# BC-018 — Image Requirements

**Source:** `blogs/bc-018/BC-018-anniversary-gifts-by-year-traditional-and-modern.md` §5. Image sizes and ratios come from the storefront code (`HOD/components/blog/*`), as documented for BC-001.

**Rules:**
- Use real HOD photography. No stock images and no decorative padding.
- No image URLs are invented here. You upload the files in the CMS.
- Alt text describes what the image actually shows; don't add keywords that aren't in the picture.

**CMS upload behavior:** uploads are converted to WebP (quality 0.84) and scaled to a maximum width of 2,200 px. JPEG, PNG, WebP, AVIF and SVG are accepted. The Article Content editor can't hold images, and Extra Article Sections render **after** the whole article, so in-article images can't sit mid-article. Every visual in this article is optional except the hero; all information is already in the text.

---

## 1. Main Blog Image (hero): REQUIRED (strongly recommended)

| | |
|---|---|
| **Asset** | A real HOD photo of anniversary-appropriate pieces, such as an eternity band beside a diamond pendant |
| **Purpose** | Connects the by-year list to diamond and gold anniversary jewelry |
| **CMS field / placement** | Main Blog Image field; article hero above the H1; also used for blog cards |
| **Aspect ratio** | **21:9** on the article hero (cropped with `object-cover`); upload at **≥ 2,200 × 943 px** and keep the subject centered so it survives card crops |
| **Alt text** | "Diamond eternity band and pendant from House of Diams" Adjust it to what the photo actually shows. |
| **Original HOD photography preferred?** | Yes. Real HOD pieces only; no stock or AI-generated jewelry presented as HOD products. |

## 2. Blog Card Image: OPTIONAL (same image as the hero)

| | |
|---|---|
| **Asset** | Same as the Main Blog Image. Leave the field empty and the CMS uses the main image. |
| **Purpose** | Blog listing, homepage and related-post cards |
| **CMS field / placement** | Cards only |
| **Aspect ratio** | Cards crop with `object-cover`; the related-posts card is **16:10**. Upload a separate card image only if the 21:9 hero crops badly. |
| **Alt text** | "Cards reuse the Main Image Alt Text" |
| **Original HOD photography preferred?** | Yes. Real HOD pieces only; no stock or AI-generated jewelry presented as HOD products. |

## 3. By-year chart graphic: OPTIONAL

| | |
|---|---|
| **Asset** | The traditional/modern list as a clean chart (years 1–15 and milestones) |
| **Purpose** | A saveable reference that restates the table |
| **CMS field / placement** | Approved placement: under the full-list H2. CMS reality: post-article only (Extra Article Sections); the full list is already in the text. |
| **Aspect ratio** | Portrait or square; must be readable on mobile |
| **Alt text** | "Chart of traditional and modern anniversary gifts by year, from paper for the 1st to diamond for the 60th" |
| **Original HOD photography preferred?** | Not applicable (graphic). Must match the article table exactly. |

**Product imagery:** None.

**Minimum to publish:** image #1 only, used for both the hero and the card.
