# BC-004 — Image Requirements

**Source:** `blogs/bc-004/BC-004-christmas-jewelry-gifts-a-holiday-gift-guide.md` §5. Image sizes and ratios come from the storefront code (`HOD/components/blog/*`), as documented for BC-001.

**Rules:**
- Use real HOD photography. No stock images and no decorative padding.
- No image URLs are invented here. You upload the files in the CMS.
- Alt text describes what the image actually shows; don't add keywords that aren't in the picture.

**CMS upload behavior:** uploads are converted to WebP (quality 0.84) and scaled to a maximum width of 2,200 px. JPEG, PNG, WebP, AVIF and SVG are accepted. The Article Content editor can't hold images, and Extra Article Sections render **after** the whole article, so in-article images can't sit mid-article. Every visual in this article is optional except the hero; all information is already in the text.

---

## 1. Main Blog Image (hero): REQUIRED (strongly recommended)

| | |
|---|---|
| **Asset** | A real HOD photo of two or three gift pieces together (for example studs, a pendant and a tennis bracelet), styled simply, optionally with restrained holiday props |
| **Purpose** | Shows the three lead gift types the article recommends |
| **CMS field / placement** | Main Blog Image field; article hero above the H1; also used for blog cards |
| **Aspect ratio** | **21:9** on the article hero (cropped with `object-cover`); upload at **≥ 2,200 × 943 px** and keep the subject centered so it survives card crops |
| **Alt text** | "Diamond stud earrings, a solitaire pendant and a tennis bracelet from House of Diams" Adjust it to what the photo actually shows. |
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

## 3. Gift-type comparison graphic: OPTIONAL

| | |
|---|---|
| **Asset** | A simple graphic of the "at a glance" table: gift type and sizing risk (none / low / medium / high) |
| **Purpose** | Makes the at-a-glance answer scannable |
| **CMS field / placement** | Approved placement: under H2 "The best diamond jewelry gifts at a glance". CMS reality: post-article only (Extra Article Sections), so leave it out unless that placement is useful. |
| **Aspect ratio** | Not specified; landscape, readable on mobile |
| **Alt text** | "Diamond jewelry gift types compared by sizing risk: studs and pendants carry the least risk, rings the most" |
| **Original HOD photography preferred?** | Not applicable (graphic). |

**Product imagery:** None in the article body. Featured Products use their own product images.

**Minimum to publish:** image #1 only, used for both the hero and the card.
