# BC-001 — Image Requirements

**Source:** the approved visual recommendations (`blogs/BC-001-…md` §5). Image sizes and ratios come from the storefront code (`HOD/components/blog/*`; the approved package didn't specify them).

**Rules (approved):**
- Use real HOD photography only. No stock images and no decorative padding.
- No image URLs are invented here. You upload the files in the CMS.
- Any timeline graphic must keep "on average"/"typically"/"about", show **design approval** as the start point, and never show 3–4 weeks as a promise or as starting at inquiry.

**CMS upload behavior:** uploads are converted to WebP (quality 0.84) and scaled to a maximum width of 2,200 px. JPEG, PNG, WebP, AVIF and SVG are accepted.

---

## 1. Main Blog Image (hero): REQUIRED (strongly recommended)

| | |
|---|---|
| **Asset** | A real HOD bespoke engagement ring: finished, or in progress on a jeweler's bench |
| **Purpose** | Signals first-hand making and sets the bespoke context |
| **CMS field** | Main Blog Image |
| **Placement** | Article hero, above the H1; also used for the blog cards |
| **Aspect ratio** | **21:9** on the article hero (cropped with `object-cover`); upload at **≥ 2,200 × 943 px** and keep the ring centered so it survives card crops |
| **Alt text (Main Image Alt Text)** | "Custom diamond engagement ring made by House of Diams". Adjust it to what the photo actually shows, e.g. the setting style or stage of work. |

If no real photo is available, the hero shows the card background color (#EEF1F8). Don't use stock imagery in its place.

## 2. Blog Card Image: OPTIONAL (same image as the hero)

| | |
|---|---|
| **Asset** | **Same as the Main Blog Image.** Leave the field empty and the CMS uses the main image. |
| **Purpose** | Blog listing, homepage and related-post cards |
| **Placement** | Cards only |
| **Aspect ratio** | Cards crop with `object-cover`; the related-posts card is **16:10**. Upload a separate card image only if the 21:9 hero crops badly. |
| **Alt text** | Cards reuse the Main Image Alt Text |

## 3. Timeline graphic: OPTIONAL

| | |
|---|---|
| **Asset** | Inquiry & consultation and design development (before the timeline; no set length) → **design approval (timeline starts)** → production, typically 2–3 weeks (CAD development, diamond selection and sorting, making, quality checks, polishing, packaging) → insured shipping, about 6–9 days. A bracket from approval to delivery reads "3–4 weeks on average". |
| **Purpose** | Makes the answer scannable and separates production from shipping |
| **Approved placement** | Under the H2 "The custom engagement ring timeline at a glance" |
| **CMS reality** | The Article Content editor can't hold images, and Extra Article Sections render **after the whole article**. So this graphic can't sit mid-article, and the timeline is already in the text. Add it as an Extra Article Sections → Add Image block **only** if a post-article placement is still useful. Otherwise leave it out. |
| **Aspect ratio** | Not specified; a landscape graphic that's readable on mobile |
| **Alt text** | "Bespoke engagement ring timeline: after design approval, production typically takes 2–3 weeks and insured shipping about 6–9 days, about 3–4 weeks on average" |

## 4. CAD model beside the finished ring: OPTIONAL

| | |
|---|---|
| **Asset** | One real HOD commission: its CAD model next to the finished ring (client consent required for a client piece) |
| **Purpose** | Shows how the dedicated CAD model becomes the finished ring |
| **Approved placement** | Step 3 "CAD model and diamond selection". The CMS can't place it there, so it would be post-article only (see #3). |
| **Alt text** | "CAD model of a custom engagement ring beside the finished ring" |

## 5. Making-stage photo: OPTIONAL

| | |
|---|---|
| **Asset** | A real photo of stone setting or casting |
| **Purpose** | Supports "How is a diamond ring made?" |
| **Approved placement** | Near step 4 of that section. The CMS can't place it there, so it would be post-article only (see #3). |
| **Alt text** | "Jeweler setting a diamond into the prongs of an engagement ring" |

**Product imagery:** none, because no products are featured.

**Minimum to publish:** image #1 only, used for both the hero and the card.
