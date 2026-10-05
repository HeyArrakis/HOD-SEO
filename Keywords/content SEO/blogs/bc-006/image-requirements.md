# BC-006 — Image Requirements

**Source:** `blogs/bc-006/BC-006-necklace-layering-how-to-layer-necklaces.md` §5. Image sizes and ratios come from the storefront code (`HOD/components/blog/*`), as documented for BC-001.

**Rules:**
- Use real HOD photography. No stock images and no decorative padding.
- No image URLs are invented here. You upload the files in the CMS.
- Alt text describes what the image actually shows; don't add keywords that aren't in the picture.

**CMS upload behavior:** uploads are converted to WebP (quality 0.84) and scaled to a maximum width of 2,200 px. JPEG, PNG, WebP, AVIF and SVG are accepted. The Article Content editor can't hold images, and Extra Article Sections render **after** the whole article, so in-article images can't sit mid-article. Every visual in this article is optional except the hero; all information is already in the text.

---

## 1. Main Blog Image (hero): REQUIRED (strongly recommended)

| | |
|---|---|
| **Asset** | A real HOD photo of a layered stack on a model or bust: a fine chain, a diamond pendant and a longer necklace, clearly spaced |
| **Purpose** | Shows the spacing rule the article teaches |
| **CMS field / placement** | Main Blog Image field; article hero above the H1; also used for blog cards |
| **Aspect ratio** | **21:9** on the article hero (cropped with `object-cover`); upload at **≥ 2,200 × 943 px** and keep the subject centered so it survives card crops |
| **Alt text** | "Three layered diamond necklaces worn at different lengths" Adjust it to what the photo actually shows. |
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

## 3. Layering-lengths diagram: OPTIONAL

| | |
|---|---|
| **Asset** | A neck-and-shoulders outline with lines at 14, 16, 18, 20 and 22–24 inches |
| **Purpose** | Visualizes the lengths table |
| **CMS field / placement** | Approved placement: under the lengths H2. CMS reality: post-article only. |
| **Aspect ratio** | Portrait or square |
| **Alt text** | "Diagram of where 14, 16, 18, 20 and 22–24 inch necklaces usually sit" |
| **Original HOD photography preferred?** | Not applicable (illustration). Must say positions vary by neck size and build. |

**Product imagery:** None beyond the hero.

**Minimum to publish:** image #1 only, used for both the hero and the card.
