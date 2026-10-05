# BC-035 — Image Requirements

**Source:** `blogs/bc-035/BC-035-10-year-anniversary-gift-ideas-tin-and-diamond.md` §5. Image sizes and ratios come from the storefront code (`HOD/components/blog/*`), as documented for BC-001.

**Rules:**
- Use real HOD photography. No stock images and no decorative padding.
- No image URLs are invented here. You upload the files in the CMS.
- Alt text describes what the image actually shows; don't add keywords that aren't in the picture.

**CMS upload behavior:** uploads are converted to WebP (quality 0.84) and scaled to a maximum width of 2,200 px. JPEG, PNG, WebP, AVIF and SVG are accepted. The Article Content editor can't hold images, and Extra Article Sections render **after** the whole article, so in-article images can't sit mid-article. Every visual in this article is optional except the hero; all information is already in the text.

---

## 1. Main Blog Image (hero): REQUIRED (strongly recommended)

| | |
|---|---|
| **Asset** | A real HOD diamond piece suited to a 10th anniversary, such as an eternity band or studs, optionally presented with or in a small tin box (the tin + diamond idea from the article) |
| **Purpose** | Illustrates the article's "traditional + modern" combination |
| **CMS field / placement** | Main Blog Image field; article hero above the H1; also used for blog cards |
| **Aspect ratio** | **21:9** on the article hero (cropped with `object-cover`); upload at **≥ 2,200 × 943 px** and keep the subject centered so it survives card crops |
| **Alt text** | "Diamond eternity band from House of Diams beside a small engraved tin box" Adjust it to what the photo actually shows. |
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

**Product imagery:** None in the body.

**Minimum to publish:** image #1 only, used for both the hero and the card.
