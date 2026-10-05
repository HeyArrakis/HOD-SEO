# BC-006 — SEO Metadata

**Source:** `blogs/bc-006/BC-006-necklace-layering-how-to-layer-necklaces.md` §2 and `blogs/bc-006/BC-006-qa.md`.

| Field | Value | Which CMS field sets it |
|---|---|---|
| **SEO title** | Necklace Layering: How to Layer Necklaces | **Article Title.** The site template adds " \| House of Diams", so it renders as "Necklace Layering: How to Layer Necklaces \| House of Diams" (58 characters). |
| **H1** | Necklace Layering: How to Layer Necklaces by Length, Weight and Pendant (Without Tangling) | **Display Title** |
| **Meta description** | How to layer necklaces: space them about 2 inches apart, finest chain on top, heaviest at the bottom. Lengths, example stacks and how to stop tangling. (151 characters) | **Short Intro** |
| **URL slug** | `/blog/necklace-layering-how-to-layer-necklaces` | Generated automatically from **Article Title** on the first save, and fixed after that |
| **Canonical** | Generated automatically by the site for the slug | — |
| **Author (byline)** | HOD Team | **Written By** |

## Target keywords (6)

**Primary**
1. `necklace layering` (14800/mo US; KD 0)

**Secondary**
2. `how to layer necklaces` (2400)
3. `layering necklaces` (14800)
4. `how to keep layered necklaces from tangling` (210)
5. `popular layered necklaces` (170)
6. `necklace layering lengths` (30)

Volumes are US monthly figures from the calendar (DataForSEO research rounds R0–R3). KD is DataForSEO's third-party difficulty estimate, not a ranking probability. No keywords outside the calendar row are targeted.

## Search intent

INFORMATIONAL (SERP-verified MIXED: product/category pages from Tiffany, Mejuri and others beside retailer guides). Commercial intent: HIGH. Funnel: AWARENESS.

## SERP / AEO notes (from existing research; no new paid calls)

- **SERP:** MIXED. James Michelle, Tiffany, Mejuri, Reddit, Hello Adorn; popular products.
- **AIO:** Core rules (2-inch spacing; mix textures; light to heavy; mix metals) and Preventing Tangles (layer clasp; pendant weight).
- **PAA:** rule/trick for layering; current trends; in style in 2026; 2:1:1 rule.
- **AEO approach:** two-rule answer first; numbered rules; lengths table; step-by-step; tangling list; neckline table.

## Schema

**Recommendation:** `BlogPosting` and `BreadcrumbList`. **Not recommended:** `FAQPage` (Google no longer shows FAQ rich results, and the site would only generate it under an "FAQ" heading, which this article avoids); `HowTo` (Google no longer shows HowTo rich results, and styling advice isn't a materials-and-steps task); `Product`/`Offer` (no product is the page's main entity); `QAPage` (not a user-answer page); `ItemList` (not needed for a guide).

**What the live site generates automatically** (from `HOD/lib/structured-data.ts`, `HOD/lib/blog-faq.ts` and `HOD/app/blog/[slug]/page.tsx`; there's no CMS field for schema):

| Element | Site output | Matches the recommendation? |
|---|---|---|
| `BlogPosting` headline / description | Article Title / Short Intro | ✅ |
| Publisher | Organization "House of Diams" with logo | ✅ |
| `FAQPage` | Generated only under a heading that reads "FAQ"/"FAQs"/"Frequently asked questions". This article has no heading matching that pattern, so **no FAQPage** is generated. | ✅ |
| Author | `{"@type": "Person", "name": "HOD Team"}` | ⚠️ Recommended: `Organization` (a team, not a person). Site template issue, same as BC-001. |
| `datePublished` / `dateModified` | Uses the **Publish Date Text** string, not an ISO date | ⚠️ Same as BC-001 |
| `BreadcrumbList` | Not generated for blog posts | ⚠️ Same as BC-001 |

The three ⚠️ items are template/code issues already logged for BC-001; they can't be fixed from the CMS and don't block this post.
